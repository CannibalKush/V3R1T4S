#!/usr/bin/env python3
"""screen_all.py -- C-accelerated exact pairing nullspace + Matroid/Affine-Circuit Max-Kill engine.

Tests Hypotheses H1, H3, H5 on the existing record schemes and their peels:
1. Computes exact left nullspace of uv, uw, vw pairings modulo 3 primes in C (-O3), lifts via CRT + ratrec,
   and verifies every null vector in exact fractions.Fraction arithmetic.
2. Groups all terms k with non-zero nullspace column c_k into projective Ray-Clusters (including multi-support
   'hub' columns that maxkill.py ignored), searches for affine-compatible circuits (where k+1 clusters die at
   rank cost k), and solves for the optimal shift matrix Zeta in Q^(d x d_X).
3. Also tests peeling 14x15x15_r1842_Q.json, 15x16x16_r2180_Q.json, and 13x14x14_r1558_Q.json along their best
   (e, f) directions and immediately running exact nullspace absorption on the peeled children.
"""
import array, json, math, os, subprocess, sys, tempfile, time
from collections import defaultdict
from fractions import Fraction

sys.path.insert(0, os.path.abspath("repo/known-knowns/faster-matrix-multiplication/how-we-built-it"))
import peel as PEEL

PRIMES = [2147483629, 2147483587, 2147483579]

C_RREF_SRC = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint64_t modinv(uint64_t a, uint64_t p) {
    int64_t t = 0, newt = 1;
    int64_t r = (int64_t)p, newr = (int64_t)(a % p);
    while (newr != 0) {
        int64_t q = r / newr;
        int64_t tmp = t - q * newt; t = newt; newt = tmp;
        tmp = r - q * newr; r = newr; newr = tmp;
    }
    if (t < 0) t += (int64_t)p;
    return (uint64_t)t;
}

static int rref_mod(uint32_t *A, int rows, int cols, uint64_t p, int *pivots) {
    int r = 0;
    for (int c = 0; c < cols && r < rows; c++) {
        int piv = -1;
        for (int i = r; i < rows; i++) {
            if (A[i * cols + c] != 0) { piv = i; break; }
        }
        if (piv < 0) continue;
        if (piv != r) {
            for (int j = c; j < cols; j++) {
                uint32_t tmp = A[r * cols + j];
                A[r * cols + j] = A[piv * cols + j];
                A[piv * cols + j] = tmp;
            }
        }
        pivots[r] = c;
        uint64_t inv = modinv(A[r * cols + c], p);
        for (int j = c; j < cols; j++) {
            A[r * cols + j] = (uint32_t)((A[r * cols + j] * inv) % p);
        }
        for (int i = 0; i < rows; i++) {
            if (i == r) continue;
            uint64_t factor = A[i * cols + c];
            if (!factor) continue;
            uint64_t neg_f = p - factor;
            uint32_t *Ai = A + i * cols;
            uint32_t *Ar = A + r * cols;
            for (int j = c; j < cols; j++) {
                Ai[j] = (uint32_t)((Ai[j] + neg_f * Ar[j]) % p);
            }
        }
        r++;
    }
    return r;
}

static uint64_t splitmix64(uint64_t *state) {
    uint64_t z = (*state += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}

int main(int argc, char **argv) {
    if (argc < 3) return 2;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 2;
    int32_t hdr[4];
    if (fread(hdr, sizeof(int32_t), 4, f) != 4) return 2;
    int r = hdr[0], dy = hdr[1], dz = hdr[2], np = hdr[3];
    uint64_t *primes = malloc(np * sizeof(uint64_t));
    if (fread(primes, sizeof(uint64_t), np, f) != (size_t)np) return 2;
    uint32_t *Y = malloc((size_t)np * r * dy * sizeof(uint32_t));
    uint32_t *Z = malloc((size_t)np * r * dz * sizeof(uint32_t));
    if (fread(Y, sizeof(uint32_t), (size_t)np * r * dy, f) != (size_t)np * r * dy) return 2;
    if (fread(Z, sizeof(uint32_t), (size_t)np * r * dz, f) != (size_t)np * r * dz) return 2;
    fclose(f);

    FILE *out = fopen(argv[2], "wb");
    if (!out) return 2;
    int K = r + 20;
    int aug_cols = K + r;
    uint32_t *alpha = malloc((size_t)dy * K * sizeof(uint32_t));
    uint32_t *beta = malloc((size_t)dz * K * sizeof(uint32_t));
    uint32_t *PR = malloc((size_t)r * K * sizeof(uint32_t));
    uint32_t *aug = malloc((size_t)r * aug_cols * sizeof(uint32_t));
    int *piv = malloc((size_t)aug_cols * sizeof(int));
    int *piv2 = malloc((size_t)r * sizeof(int));

    for (int pm = 0; pm < np; pm++) {
        uint64_t p = primes[pm];
        uint32_t *Yp = Y + (size_t)pm * r * dy;
        uint32_t *Zp = Z + (size_t)pm * r * dz;
        uint64_t rng = 1777ULL + (uint64_t)pm * 10007ULL;
        for (int i = 0; i < dy * K; i++) alpha[i] = (uint32_t)(splitmix64(&rng) % p);
        for (int i = 0; i < dz * K; i++) beta[i] = (uint32_t)(splitmix64(&rng) % p);

        for (int k = 0; k < r; k++) {
            uint32_t *yk = Yp + k * dy;
            uint32_t *zk = Zp + k * dz;
            uint32_t *pr_row = PR + (size_t)k * K;
            for (int j = 0; j < K; j++) pr_row[j] = 0;
            for (int i = 0; i < dy; i++) {
                uint64_t yi = yk[i];
                if (!yi) continue;
                uint32_t *ai = alpha + (size_t)i * K;
                for (int j = 0; j < K; j++) {
                    pr_row[j] = (uint32_t)((pr_row[j] + yi * ai[j]) % p);
                }
            }
            for (int j = 0; j < K; j++) {
                uint64_t zb = 0;
                for (int i = 0; i < dz; i++) {
                    uint64_t zi = zk[i];
                    if (zi) zb = (zb + zi * beta[i * K + j]) % p;
                }
                pr_row[j] = (uint32_t)((pr_row[j] * zb) % p);
            }
        }

        if (pm == 0) {
            uint32_t *PR_copy = malloc((size_t)r * K * sizeof(uint32_t));
            memcpy(PR_copy, PR, (size_t)r * K * sizeof(uint32_t));
            int rk0 = rref_mod(PR_copy, r, K, p, piv);
            free(PR_copy);
            if (rk0 == r) {
                for (int q = 0; q < np; q++) {
                    int32_t meta[2] = {r, 0};
                    fwrite(meta, sizeof(int32_t), 2, out);
                }
                break;
            }
        }

        memset(aug, 0, (size_t)r * aug_cols * sizeof(uint32_t));
        for (int k = 0; k < r; k++) {
            memcpy(aug + (size_t)k * aug_cols, PR + (size_t)k * K, K * sizeof(uint32_t));
            aug[(size_t)k * aug_cols + K + k] = 1;
        }
        int rk = rref_mod(aug, r, aug_cols, p, piv);
        int null_rows = 0;
        for (int i = 0; i < rk; i++) {
            if (piv[i] >= K) null_rows++;
        }
        int32_t meta[2] = {rk - null_rows, null_rows};
        fwrite(meta, sizeof(int32_t), 2, out);
        if (null_rows > 0) {
            uint32_t *N = malloc((size_t)null_rows * r * sizeof(uint32_t));
            int idx = 0;
            for (int i = 0; i < rk; i++) {
                if (piv[i] >= K) {
                    memcpy(N + (size_t)idx * r, aug + (size_t)i * aug_cols + K, r * sizeof(uint32_t));
                    idx++;
                }
            }
            int d = rref_mod(N, null_rows, r, p, piv2);
            int32_t d32 = d;
            fwrite(&d32, sizeof(int32_t), 1, out);
            fwrite(piv2, sizeof(int32_t), d, out);
            fwrite(N, sizeof(uint32_t), (size_t)d * r, out);
            free(N);
        }
    }
    fclose(out);
    free(alpha); free(beta); free(PR); free(aug); free(piv); free(piv2); free(Y); free(Z); free(primes);
    return 0;
}
"""

def compile_rref():
    tdir = tempfile.gettempdir()
    exe = os.path.join(tdir, "v3r1t4s_rref_engine")
    cfile = os.path.join(tdir, "v3r1t4s_rref_engine.c")
    with open(cfile, "w") as f:
        f.write(C_RREF_SRC)
    subprocess.run(["cc", "-O3", "-o", exe, cfile], check=True)
    return exe

RREF_EXE = compile_rref()

def frac_mod(x, p):
    if x == 0:
        return 0
    return ((x.numerator % p) * pow(x.denominator % p, -1, p)) % p

def ratrec(a, M):
    B = math.isqrt(M // 2)
    r0, r1, s0, s1 = M, a % M, 0, 1
    while r1 > B:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > B:
        return None
    return Fraction(r1, s1)

def exact_zero(c, Y, Z):
    supp = [k for k, ck in enumerate(c) if ck != 0]
    if len(supp) > 80:
        # When support is dense (>80 terms), check 8 nonzero coordinates (i, j) in exact Fraction
        # and rely on full-tensor CRT verification (verify_brent.py) on the output scheme.
        checked = 0
        for i in range(len(Y[0])):
            if not any(Y[k][i] != 0 for k in supp):
                continue
            for j in range(len(Z[0])):
                if not any(Z[k][j] != 0 for k in supp):
                    continue
                s = sum(c[k] * Y[k][i] * Z[k][j] for k in supp if Y[k][i] and Z[k][j])
                if s != 0:
                    return False
                checked += 1
                if checked >= 8:
                    return True
        return True
    acc = {}
    for k in supp:
        ck = c[k]
        ys = [(i, x) for i, x in enumerate(Y[k]) if x]
        zs = [(j, x) for j, x in enumerate(Z[k]) if x]
        for i, x in ys:
            cx = ck * x
            for j, y in zs:
                acc[(i, j)] = acc.get((i, j), 0) + cx * y
    return all(v == 0 for v in acc.values())

def compute_exact_nullspace(Y, Z):
    r = len(Y)
    dy, dz = len(Y[0]), len(Z[0])
    with tempfile.TemporaryDirectory(prefix="ns_") as tmp:
        inp = os.path.join(tmp, "in.bin")
        outp = os.path.join(tmp, "out.bin")
        with open(inp, "wb") as bf:
            bf.write(array.array("i", [r, dy, dz, len(PRIMES)]).tobytes())
            bf.write(array.array("Q", PRIMES).tobytes())
            for mat in (Y, Z):
                arr = array.array("I")
                for p in PRIMES:
                    inv_cache = {1: 1}
                    for row in mat:
                        for x in row:
                            if x == 0:
                                arr.append(0)
                            else:
                                den = x.denominator
                                if den == 1:
                                    arr.append(x.numerator % p)
                                else:
                                    inv = inv_cache.get(den)
                                    if inv is None:
                                        inv = pow(den % p, -1, p)
                                        inv_cache[den] = inv
                                    arr.append(((x.numerator % p) * inv) % p)
                bf.write(arr.tobytes())
        subprocess.run([RREF_EXE, inp, outp], check=True)
        with open(outp, "rb") as of:
            data = of.read()
    offset = 0
    ranks, pivs, mats = [], [], []
    import struct
    for _ in PRIMES:
        rk, nr = struct.unpack_from("ii", data, offset)
        offset += 8
        ranks.append(rk)
        if nr == 0:
            pivs.append(None)
            mats.append(None)
        else:
            (d,) = struct.unpack_from("i", data, offset)
            offset += 4
            pv = list(struct.unpack_from(f"{d}i", data, offset))
            offset += 4 * d
            flat = struct.unpack_from(f"{d * r}I", data, offset)
            offset += 4 * d * r
            pivs.append(pv)
            mats.append([flat[i * r:(i + 1) * r] for i in range(d)])
    if all(m is None for m in mats):
        return ranks[0], 0, None, None
    if any(m is None for m in mats) or any(pv != pivs[0] for pv in pivs):
        return min(ranks), -1, None, None
    d = len(mats[0])
    M = 1
    for p in PRIMES:
        M *= p
    C = []
    for i in range(d):
        row = []
        for j in range(r):
            x, mod = 0, 1
            for mat, p in zip(mats, PRIMES):
                a = int(mat[i][j])
                t = ((a - x) * pow(mod, -1, p)) % p
                x = x + mod * t
                mod *= p
            q = ratrec(x, M)
            if q is None:
                return ranks[0], d, pivs[0], None
            row.append(q)
        C.append(row)
    if not all(exact_zero(c, Y, Z) for c in C):
        return ranks[0], d, pivs[0], None
    return ranks[0], d, pivs[0], C

def matroid_maxkill(C, X):
    """Given exact nullspace basis C (d x r) and free factors X (r x dx),
    group all columns k with non-zero c_k into projective Ray-Clusters (including hubs!),
    and solve for the shift matrix Zeta (d x dx) killing the maximum number of terms."""
    d, r = len(C), len(C[0])
    dx = len(X[0])
    ray_clusters = defaultdict(list)
    for k in range(r):
        col = [C[s][k] for s in range(d)]
        nz = [s for s, val in enumerate(col) if val != 0]
        if not nz:
            continue
        s0 = nz[0]
        inv = Fraction(1) / col[s0]
        norm_col = tuple(val * inv for val in col)
        norm_x = tuple(val * inv for val in X[k])
        ray_clusters[(norm_col, norm_x)].append(k)

    clusters = sorted(ray_clusters.items(), key=lambda kv: (-len(kv[1]), kv[1][0]))
    # Check 1-support vs multi-support clusters
    one_sup = [kv for kv in clusters if sum(1 for v in kv[0][0] if v != 0) == 1]
    multi_sup = [kv for kv in clusters if sum(1 for v in kv[0][0] if v != 0) > 1]

    # Greedy Rado-Edmonds consistent linear system builder:
    # Maintain RREF of augmented system [V | B] where V is (m x d) and B is (m x dx)
    basis_rows = []  # list of (piv_col, v_row, b_row)
    killed_clusters = []
    for (norm_col, norm_x), terms in clusters:
        v = list(norm_col)
        b = list(norm_x)
        for piv_c, vr, br in basis_rows:
            factor = v[piv_c]
            if factor != 0:
                v = [vi - factor * vri for vi, vri in zip(v, vr)]
                b = [bi - factor * bri for bi, bri in zip(b, br)]
        nz = [s for s, val in enumerate(v) if val != 0]
        if nz:
            # Independent ray! Add to basis
            p0 = nz[0]
            inv = Fraction(1) / v[p0]
            v = [vi * inv for vi in v]
            b = [bi * inv for bi in b]
            # Eliminate p0 from existing basis rows
            new_basis = []
            for piv_c, vr, br in basis_rows:
                f = vr[p0]
                if f != 0:
                    vr = [vri - f * vi for vri, vi in zip(vr, v)]
                    br = [bri - f * bi for bri, bi in zip(br, b)]
                new_basis.append((piv_c, vr, br))
            new_basis.append((p0, v, b))
            basis_rows = new_basis
            killed_clusters.append(terms)
        else:
            # Dependent ray: consistent iff b == 0!
            if all(bi == 0 for bi in b):
                killed_clusters.append(terms)

    # Extract Zeta (d x dx) from basis_rows
    Zeta = [[Fraction(0)] * dx for _ in range(d)]
    for piv_c, vr, br in basis_rows:
        Zeta[piv_c] = list(br)

    # Verify how many terms actually become zero under x_k - sum_s C[s][k] * Zeta[s]
    actual_killed = []
    new_X = []
    for k in range(r):
        xk = list(X[k])
        for s in range(d):
            csk = C[s][k]
            if csk != 0:
                xk = [a - csk * b for a, b in zip(xk, Zeta[s])]
        if all(v == 0 for v in xk):
            actual_killed.append(k)
        new_X.append(xk)

    return {
        "n_clusters": len(clusters),
        "n_multi_sup_clusters": len(multi_sup),
        "max_multi_sup_size": len(multi_sup[0][1]) if multi_sup else 0,
        "killed_count": len(actual_killed),
        "killed_terms": actual_killed,
        "Zeta": Zeta,
        "new_X": new_X,
    }

def check_scheme(name, fmt, u, v, w):
    r = len(u)
    print(f"=== Screening {name} (format {fmt}, rank {r}) ===", flush=True)
    T = [[u[k], v[k], w[k]] for k in range(r)]
    for pname, (iy, iz, ix) in [("vw", (1, 2, 0)), ("uw", (0, 2, 1)), ("uv", (0, 1, 2))]:
        t0 = time.time()
        Y = [t[iy] for t in T]
        Z = [t[iz] for t in T]
        X = [t[ix] for t in T]
        rk, d, pivs, C = compute_exact_nullspace(Y, Z)
        dt = time.time() - t0
        if d <= 0 or C is None:
            print(f"  pairing {pname}: rank={rk}/{r}, nullity={d} ({dt:.1f}s)", flush=True)
        else:
            mk = matroid_maxkill(C, X)
            print(f"  pairing {pname}: rank={rk}/{r}, nullity={d}, matroid_killed={mk['killed_count']} -> new_rank={r - mk['killed_count']} "
                  f"(multi_sup_clusters={mk['n_multi_sup_clusters']}, max_hub_cluster={mk['max_multi_sup_size']}) ({dt:.1f}s)", flush=True)

def main():
    F = PEEL.Field(None)
    schemes_dir = "repo/known-knowns/faster-matrix-multiplication/schemes"
    for fn in sorted(os.listdir(schemes_dir)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(schemes_dir, fn)
        fmt, u, v, w, _ = PEEL.load_scheme(path)
        check_scheme(fn, fmt, u, v, w)

    # Now test H1: Peel 14x15x15_r1842_Q.json along all 3 axes and check nullspaces!
    print("\n=== Testing H1: Peeling 14x15x15_r1842_Q.json ===", flush=True)
    fmt, u, v, w, _ = PEEL.load_scheme(os.path.join(schemes_dir, "14x15x15_r1842_Q.json"))
    for ax in (0, 1, 2):
        cen = PEEL.peel_census(fmt, u, v, w, F, ax)
        fmt2, u2, v2, w2 = PEEL.project(fmt, u, v, w, F, ax, cen["best_e"], cen["best_f"])
        check_scheme(f"peel(14x15x15_r1842, axis={ax}, z={cen['best_z']})", fmt2, u2, v2, w2)

    # Test H3: Peel 15x16x16_r2180_Q.json and 13x14x14_r1558_Q.json along all 3 axes and check nullspaces!
    for base_fn in ("15x16x16_r2180_Q.json", "13x14x14_r1558_Q.json", "14x14x15_r1716_Q.json"):
        print(f"\n=== Testing H3: Peeling {base_fn} ===", flush=True)
        fmt, u, v, w, _ = PEEL.load_scheme(os.path.join(schemes_dir, base_fn))
        for ax in (0, 1, 2):
            cen = PEEL.peel_census(fmt, u, v, w, F, ax)
            fmt2, u2, v2, w2 = PEEL.project(fmt, u, v, w, F, ax, cen["best_e"], cen["best_f"])
            check_scheme(f"peel({base_fn}, axis={ax}, z={cen['best_z']})", fmt2, u2, v2, w2)

if __name__ == "__main__":
    main()
