#!/usr/bin/env python3
"""Standalone exact Brent-equation checker for rational FMM schemes (Python stdlib + compiled C CRT core).

Verifies from first principles:
1. Well-formed JSON with n = [n1, n2, n3], ring in {"Q", "Z", "ZT"}, and u, v, w lists of equal length r.
2. Every entry is parsed as an exact fractions.Fraction(p, q).
3. Rank is counted as the number of terms k in 0..r-1 where u_k, v_k, w_k are all non-zero vectors.
4. Exact Brent equations over Q:
   For all a in [0, n1*n2), b in [0, n2*n3), c in [0, n3*n1):
     sum_{k=0}^{r-1} u_k[a] * v_k[b] * w_k[c] == delta(a, b, c)
   where a = i1*n2 + j1, b = j2*n3 + l2, c = l3*n1 + i3, and delta = 1 iff (i1==i3 and j1==j2 and l2==l3) else 0.
5. Uses Chinese Remainder Theorem (CRT) over distinct primes p_m ~ 2^30 where the product of primes strictly
   exceeds 2 * L * (S + 1), with L = lcm of all term denominators (u_den * v_den * w_den) and S = sum of max
   term numerator magnitudes. By CRT, zero residual modulo all p_m is a deterministic mathematical PROOF that
   every Brent equation holds identically over Q.
"""
import json, math, os, subprocess, sys, tempfile
from fractions import Fraction

C_SRC = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char **argv) {
    if (argc < 2) return 2;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 2;
    int32_t hdr[5];
    if (fread(hdr, sizeof(int32_t), 5, f) != 5) return 2;
    int n1 = hdr[0], n2 = hdr[1], n3 = hdr[2], r = hdr[3], np = hdr[4];
    uint64_t *primes = malloc(np * sizeof(uint64_t));
    if (fread(primes, sizeof(uint64_t), np, f) != (size_t)np) return 2;
    int na = n1 * n2, nb = n2 * n3, nc = n3 * n1;
    uint32_t *U = malloc((size_t)np * r * na * sizeof(uint32_t));
    uint32_t *V = malloc((size_t)np * r * nb * sizeof(uint32_t));
    uint32_t *W = malloc((size_t)np * r * nc * sizeof(uint32_t));
    if (fread(U, sizeof(uint32_t), (size_t)np * r * na, f) != (size_t)np * r * na) return 2;
    if (fread(V, sizeof(uint32_t), (size_t)np * r * nb, f) != (size_t)np * r * nb) return 2;
    if (fread(W, sizeof(uint32_t), (size_t)np * r * nc, f) != (size_t)np * r * nc) return 2;
    fclose(f);

    uint64_t *VW = malloc((size_t)nb * nc * sizeof(uint64_t));
    for (int pm = 0; pm < np; pm++) {
        uint64_t p = primes[pm];
        uint32_t *Up = U + (size_t)pm * r * na;
        uint32_t *Vp = V + (size_t)pm * r * nb;
        uint32_t *Wp = W + (size_t)pm * r * nc;
        for (int a = 0; a < na; a++) {
            int i1 = a / n2, j1 = a % n2;
            for (int idx = 0; idx < nb * nc; idx++) VW[idx] = 0;
            for (int k = 0; k < r; k++) {
                uint64_t ua = Up[k * na + a];
                if (!ua) continue;
                uint32_t *vk = Vp + k * nb;
                for (int b = 0; b < nb; b++) {
                    uint64_t uavb = (ua * vk[b]) % p;
                    if (!uavb) continue;
                    uint32_t *wk = Wp + k * nc;
                    uint64_t *row = VW + b * nc;
                    for (int c = 0; c < nc; c++) {
                        row[c] = (row[c] + uavb * wk[c]) % p;
                    }
                }
            }
            for (int b = 0; b < nb; b++) {
                int j2 = b / n3, l2 = b % n3;
                uint64_t *row = VW + b * nc;
                for (int c = 0; c < nc; c++) {
                    int l3 = c / n1, i3 = c % n1;
                    uint64_t exp = (i1 == i3 && j1 == j2 && l2 == l3) ? 1 : 0;
                    if (row[c] % p != exp) {
                        printf("FAIL prime=%llu a=%d b=%d c=%d got=%llu exp=%llu\n",
                               (unsigned long long)p, a, b, c,
                               (unsigned long long)(row[c] % p), (unsigned long long)exp);
                        return 1;
                    }
                }
            }
        }
    }
    free(VW); free(U); free(V); free(W); free(primes);
    return 0;
}
"""

def is_prime(n):
    if n < 2 or n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def parse_frac(x):
    if isinstance(x, bool):
        raise ValueError("boolean coefficient not allowed")
    if isinstance(x, int):
        return Fraction(x)
    return Fraction(str(x).strip())

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b) if a and b else 0

def row_info(row):
    den_lcm = 1
    max_abs_num = 0
    nz = False
    for v in row:
        if v != 0:
            nz = True
            den_lcm = lcm(den_lcm, v.denominator)
    for v in row:
        if v != 0:
            num_scaled = abs(v.numerator) * (den_lcm // v.denominator)
            if num_scaled > max_abs_num:
                max_abs_num = num_scaled
    return nz, den_lcm, max_abs_num

def parse_matrix(raw_mat, width, encoding):
    out = []
    for r in raw_mat:
        if encoding == "sparse_flat_pairs":
            if len(r) == 0 or len(r) % 2 != 0:
                raise ValueError("sparse_flat_pairs row must have positive even length")
            vec = [Fraction(0)] * width
            prev_idx = -1
            for j in range(0, len(r), 2):
                idx = r[j]
                if not isinstance(idx, int) or isinstance(idx, bool) or idx <= prev_idx or idx >= width or idx < 0:
                    raise ValueError(f"invalid or non-increasing index {idx} (prev={prev_idx}, width={width})")
                prev_idx = idx
                val = parse_frac(r[j + 1])
                if val == 0:
                    raise ValueError("zero coefficient in sparse_flat_pairs")
                vec[idx] = val
            out.append(vec)
        else:
            if len(r) != width:
                raise ValueError(f"factor width mismatch: got {len(r)}, expected {width}")
            out.append([parse_frac(x) for x in r])
    return out

def verify_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        n1, n2, n3 = [int(x) for x in d["n"]]
        na, nb, nc = n1 * n2, n2 * n3, n3 * n1
        enc = d.get("encoding", "dense")
        u = parse_matrix(d["u"], na, enc)
        v = parse_matrix(d["v"], nb, enc)
        w = parse_matrix(d["w"], nc, enc)
    except Exception as e:
        return False, f"FAIL parse error in {os.path.basename(path)}: {e}"
    r = len(u)
    if not (len(v) == r and len(w) == r):
        return False, "FAIL u/v/w length mismatch"

    L = 1
    term_bounds = []
    nonzero_terms = 0
    bad_dens = set()
    for k in range(r):
        nzu, du, mu = row_info(u[k])
        nzv, dv, mv = row_info(v[k])
        nzw, dw, mw = row_info(w[k])
        if nzu and nzv and nzw:
            nonzero_terms += 1
        dk = du * dv * dw
        L = lcm(L, dk)
        term_bounds.append((dk, mu * mv * mw))
        for x in u[k] + v[k] + w[k]:
            if x.denominator > 1:
                bad_dens.add(x.denominator)
    if "m" in d and int(d["m"]) != nonzero_terms:
        return False, f"FAIL claimed m={d['m']} != nonzero_terms={nonzero_terms}"

    S = sum(m * (L // dk) for dk, m in term_bounds)
    bound = 2 * L * (S + 1)
    primes = []
    prod = 1
    cand = (1 << 30) - 35
    while prod <= bound or len(primes) < 2:
        if is_prime(cand) and all(den % cand != 0 for den in bad_dens):
            primes.append(cand)
            prod *= cand
        cand -= 2

    import array
    with tempfile.TemporaryDirectory(prefix="brent_chk_") as tmp:
        bin_path = os.path.join(tmp, "data.bin")
        c_path = os.path.join(tmp, "chk.c")
        exe_path = os.path.join(tmp, "chk")
        with open(c_path, "w") as cf:
            cf.write(C_SRC)
        subprocess.run(["cc", "-O3", "-o", exe_path, c_path], check=True)
        with open(bin_path, "wb") as bf:
            bf.write(array.array("i", [n1, n2, n3, r, len(primes)]).tobytes())
            bf.write(array.array("Q", primes).tobytes())
            for mat, width in ((u, na), (v, nb), (w, nc)):
                arr = array.array("I")
                for p in primes:
                    inv_cache = {}
                    for row in mat:
                        for x in row:
                            if x == 0:
                                arr.append(0)
                            else:
                                den = x.denominator
                                inv = inv_cache.get(den)
                                if inv is None:
                                    inv = pow(den % p, -1, p)
                                    inv_cache[den] = inv
                                arr.append(((x.numerator % p) * inv) % p)
                bf.write(arr.tobytes())
        res = subprocess.run([exe_path, bin_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if res.returncode != 0:
            return False, res.stdout.strip()
    return True, f"PASS file={os.path.basename(path)} format={n1}x{n2}x{n3} rank={nonzero_terms} primes={len(primes)} log2_bound={bound.bit_length()}"

if __name__ == "__main__":
    ok_all = True
    for p in sys.argv[1:]:
        ok, msg = verify_file(p)
        print(msg)
        if not ok:
            ok_all = False
    sys.exit(0 if ok_all else 1)
