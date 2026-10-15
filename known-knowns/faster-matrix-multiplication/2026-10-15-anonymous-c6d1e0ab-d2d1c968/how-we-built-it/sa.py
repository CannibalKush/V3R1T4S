"""Slice and absorb: exact rank reduction of matrix multiplication schemes over Q.

A scheme for <n1,n2,n3> is a list of terms (U, V, W); U, V, W are dicts {flat index: Fraction}.
Convention (Perminov / V3R1T4S): term computes (sum U[i*n2+j] A_ij) * (sum V[j*n3+l] B_jl)
and adds W[l*n1+i] times it to C_il.

Moves
  slice   restrict dimension n1 -> n1-1 along a direction pair (f, e) with f.e != 0:
          terms with U = f x^T or W = y e^T vanish.
  absorb  find exact dependencies sum_t lam_t U_t (x) V_t = 0; then W_t += lam_t . Z keeps the
          tensor for every Z; choose Z to zero as many W_t as possible (matroid greedy over rays).
Other dimensions and pairings are reached by cyclic rotation (U,V,W) -> (V,W,U), (n1,n2,n3) -> (n2,n3,n1).

Exactness: all scheme arithmetic is in Fractions. A random prime-field projection only proposes
which terms take part in a dependency; the dependencies themselves are recomputed exactly over Q.
"""
import json
import random
import sys
import time
from collections import defaultdict
from fractions import Fraction
from math import gcd

import numpy as np
from flint import nmod_mat

P = 16777213  # prime < 2^24: products and 256-term sums stay inside int64


# ---------------------------------------------------------------- I/O

def _frac(x):
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(x)
    raise ValueError(f"bad coefficient {x!r}")


def _row(d, row, length):
    if d.get("encoding") == "sparse_flat_pairs":
        out = {}
        for a, b in zip(row[0::2], row[1::2]):
            v = _frac(b)
            if v:
                out[a] = v
        return out
    assert len(row) == length
    return {a: _frac(b) for a, b in enumerate(row) if b not in (0, "0")}


def load(path):
    d = json.load(open(path))
    n1, n2, n3 = d["n"]
    terms = []
    for u, v, w in zip(d["u"], d["v"], d["w"]):
        U, V, W = _row(d, u, n1 * n2), _row(d, v, n2 * n3), _row(d, w, n3 * n1)
        if U and V and W:
            terms.append((U, V, W))
    return (n1, n2, n3), terms


def _enc(x):
    return x.numerator if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def save(path, n, terms, note=""):
    def flat(row):
        out = []
        for a in sorted(row):
            out += [a, _enc(row[a])]
        return out
    d = {"n": list(n), "m": len(terms), "ring": "Q", "encoding": "sparse_flat_pairs", "note": note,
         "u": [flat(t[0]) for t in terms], "v": [flat(t[1]) for t in terms], "w": [flat(t[2]) for t in terms]}
    with open(path, "w") as fh:
        json.dump(d, fh, separators=(",", ":"))


# ---------------------------------------------------------------- exact check

def brent_ok(n, terms):
    n1, n2, n3 = n
    acc = defaultdict(Fraction)
    for U, V, W in terms:
        for a, ua in U.items():
            for b, vb in V.items():
                uv = ua * vb
                for c, wc in W.items():
                    acc[(a, b, c)] += uv * wc
    for i in range(n1):
        for j in range(n2):
            for l in range(n3):
                key = (i * n2 + j, j * n3 + l, l * n1 + i)
                if acc.pop(key, 0) != 1:
                    return False
    return all(v == 0 for v in acc.values())


# ---------------------------------------------------------------- symmetry

def rotate(n, terms):
    """(U,V,W) for (n1,n2,n3) -> (V,W,U) for (n2,n3,n1)."""
    n1, n2, n3 = n
    return (n2, n3, n1), [(V, W, U) for U, V, W in terms]


def rotate_to(n, terms, k):
    for _ in range(k % 3):
        n, terms = rotate(n, terms)
    return n, terms


# ---------------------------------------------------------------- directions

def _primitive(vec):
    """Normalize a Fraction vector (dict index->value) to a primitive integer tuple key, sign fixed."""
    items = sorted(vec.items())
    den = 1
    for _, v in items:
        den = den * v.denominator // gcd(den, v.denominator)
    ints = [(k, int(v * den)) for k, v in items]
    g = 0
    for _, v in ints:
        g = gcd(g, abs(v))
    if ints[0][1] < 0:
        g = -g
    return tuple((k, v // g) for k, v in ints)


def u_col_direction(U, n):
    """If U (n1 x n2, index i*n2+j) is rank one, return its column direction over i, else None."""
    n1, n2, _ = n
    rows = defaultdict(dict)
    for a, v in U.items():
        rows[a // n2][a % n2] = v
    keys = sorted(rows)
    base = rows[keys[0]]
    j0 = min(base)
    coef = {}
    for i in keys:
        r = rows[i]
        if set(r) != set(base):
            return None
        s = r[j0] / base[j0]
        if any(r[j] != s * base[j] for j in base):
            return None
        coef[i] = s
    return _primitive(coef)


def w_row_direction(W, n):
    """If W (n3 x n1, index l*n1+i) is rank one, return its row direction over i, else None."""
    n1, _, n3 = n
    rows = defaultdict(dict)
    for c, v in W.items():
        rows[c // n1][c % n1] = v
    keys = sorted(rows)
    base = rows[keys[0]]
    i0 = min(base)
    for l in keys:
        r = rows[l]
        if set(r) != set(base):
            return None
        s = r[i0] / base[i0]
        if any(r[i] != s * base[i] for i in base):
            return None
    return _primitive(base)


def slice_candidates(n, terms, top=8):
    """Rank (f, e) pairs for restricting n1 by the number of terms they remove immediately."""
    fu = defaultdict(set)
    ew = defaultdict(set)
    for t, (U, V, W) in enumerate(terms):
        f = u_col_direction(U, n)
        if f is not None:
            fu[f].add(t)
        e = w_row_direction(W, n)
        if e is not None:
            ew[e].add(t)
    fs = sorted(fu, key=lambda k: -len(fu[k]))[:40]
    es = sorted(ew, key=lambda k: -len(ew[k]))[:40]
    n1 = n[0]
    unit = [((i, 1),) for i in range(n1)]
    cands = []
    for f in fs + unit:
        for e in es + unit:
            fd, ed = dict(f), dict(e)
            dot = sum(fd[i] * ed.get(i, 0) for i in fd)
            if dot == 0:
                continue
            kills = len(fu.get(f, set()) | ew.get(e, set()))
            cands.append((kills, f, e))
    cands.sort(key=lambda c: -c[0])
    seen, out = set(), []
    for c in cands:
        if (c[1], c[2]) in seen:
            continue
        seen.add((c[1], c[2]))
        out.append(c)
        if len(out) >= top:
            break
    return out


# ---------------------------------------------------------------- slice

def slice_dim1(n, terms, f, e):
    """Restrict n1 -> n1-1 along (f, e); f, e are primitive tuples ((index, value), ...)."""
    n1, n2, n3 = n
    fd = {i: Fraction(v) for i, v in f}
    ed = {i: Fraction(v) for i, v in e}
    fe = sum(fd[i] * ed.get(i, 0) for i in fd)
    assert fe != 0
    k = min(fd, key=lambda i: (abs(fd[i]) != 1, i))  # pivot with f_k = +-1 when possible
    keep = [i for i in range(n1) if i != k]
    newi = {i: x for x, i in enumerate(keep)}
    m1 = n1 - 1
    out = []
    for U, V, W in terms:
        # U' row j = U row j - (f_j / f_k) U row k
        Ur = defaultdict(dict)
        for a, v in U.items():
            Ur[a // n2][a % n2] = v
        rowk = Ur.get(k, {})
        U2 = {}
        for i in keep:
            r = dict(Ur.get(i, {}))
            fj = fd.get(i, 0)
            if fj and rowk:
                s = fj / fd[k]
                for j, v in rowk.items():
                    r[j] = r.get(j, 0) - s * v
            for j, v in r.items():
                if v:
                    U2[newi[i] * n2 + j] = v
        # W' (l, j) = W(l, j) - (e_j / f.e) * (W f)_l
        Wr = defaultdict(dict)
        for c, v in W.items():
            Wr[c // n1][c % n1] = v
        W2 = {}
        for l, r in Wr.items():
            wf = sum(v * fd.get(i, 0) for i, v in r.items())
            rr = {i: v for i, v in r.items() if i != k}
            if wf:
                for i, ev in ed.items():
                    if i != k:
                        rr[i] = rr.get(i, 0) - ev / fe * wf
            for i, v in rr.items():
                if v:
                    W2[l * m1 + newi[i]] = v
        if U2 and V and W2:
            out.append((U2, dict(V), W2))
    return (m1, n2, n3), out


# ---------------------------------------------------------------- exact linear algebra helpers

def _modp(x):
    return (x.numerator % P) * pow(x.denominator % P, -1, P) % P


def _dense_mod(rows, length):
    a = np.zeros((len(rows), length), dtype=np.int64)
    for t, r in enumerate(rows):
        for k, v in r.items():
            a[t, k] = _modp(v)
    return a


def candidate_support(n, terms, rng):
    """Terms that can take part in a dependency sum lam_t U_t (x) V_t = 0 (prime-field projection)."""
    n1, n2, n3 = n
    r = len(terms)
    s = r + 16
    Um = _dense_mod([t[0] for t in terms], n1 * n2)
    Vm = _dense_mod([t[1] for t in terms], n2 * n3)
    g1 = np.array([[rng.randrange(P) for _ in range(n1 * n2)] for _ in range(s)], dtype=np.int64)
    g2 = np.array([[rng.randrange(P) for _ in range(n2 * n3)] for _ in range(s)], dtype=np.int64)
    A1 = (Um @ g1.T) % P
    A2 = (Vm @ g2.T) % P
    A = (A1 * A2) % P  # r x s, entry (t, c) = <U_t (x) V_t, g1_c (x) g2_c>
    M = nmod_mat(s, r, A.T.flatten().tolist(), P)
    X, nullity = M.nullspace()
    if nullity == 0:
        return [], 0
    sup = set()
    for col in range(nullity):
        for t in range(r):
            if int(X[t, col]) != 0:
                sup.add(t)
    return sorted(sup), nullity


def exact_left_nullspace(vectors):
    """vectors: list of dicts (sparse rows over Q). Returns a basis of {lam : sum lam_t v_t = 0}
    as dicts {position in list: Fraction}."""
    pivots = {}  # pivot column -> (row dict, comb dict)
    order = []
    basis = []
    for t, v in enumerate(vectors):
        row = dict(v)
        comb = {t: Fraction(1)}
        for c in order:
            if c in row:
                prow, pcomb = pivots[c]
                fct = row[c] / prow[c]
                for k, x in prow.items():
                    y = row.get(k, 0) - fct * x
                    if y:
                        row[k] = y
                    else:
                        row.pop(k, None)
                for k, x in pcomb.items():
                    y = comb.get(k, 0) - fct * x
                    if y:
                        comb[k] = y
                    else:
                        comb.pop(k, None)
        if not row:
            basis.append(comb)
        else:
            c = min(row)
            pivots[c] = (row, comb)
            order.append(c)
    return basis


def outer(U, V, n2n3):
    return {a * n2n3 + b: ua * vb for a, ua in U.items() for b, vb in V.items()}


def _is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 7, 61):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


PRIMES = []
_c = (1 << 24) - 1
while len(PRIMES) < 16:
    if _is_prime(_c):
        PRIMES.append(_c)
    _c -= 2


def _ratrec(a, m):
    """Rational reconstruction of a mod m: n/d with |n|, d <= sqrt(m/2), or None."""
    bound = int((m // 2) ** 0.5)
    r0, r1, s0, s1 = m, a % m, 0, 1
    while r1 > bound:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > bound:
        return None
    if s1 < 0:
        r1, s1 = -r1, -s1
    return Fraction(r1, s1)


def _nullspace_rref_mod(n, terms, rng, p):
    """RREF basis (k x r, as list of dicts col->value) of the projected left nullspace mod p."""
    n1, n2, n3 = n
    r = len(terms)
    s = r + 16

    def dense(rows, length):
        a = np.zeros((len(rows), length), dtype=np.int64)
        for t, row in enumerate(rows):
            for k, v in row.items():
                a[t, k] = (v.numerator % p) * pow(v.denominator % p, -1, p) % p
        return a

    Um = dense([t[0] for t in terms], n1 * n2)
    Vm = dense([t[1] for t in terms], n2 * n3)
    g1 = np.array([[rng.randrange(p) for _ in range(n1 * n2)] for _ in range(s)], dtype=np.int64)
    g2 = np.array([[rng.randrange(p) for _ in range(n2 * n3)] for _ in range(s)], dtype=np.int64)
    A = ((Um @ g1.T) % p) * ((Vm @ g2.T) % p) % p
    M = nmod_mat(s, r, A.T.flatten().tolist(), p)
    X, k = M.nullspace()
    if k == 0:
        return []
    B = nmod_mat(k, r, [int(X[t, c]) for c in range(k) for t in range(r)], p)
    R, rank = B.rref()
    rows = []
    for i in range(rank):
        rows.append({t: int(R[i, t]) for t in range(r) if int(R[i, t]) != 0})
    return rows


def exact_nullspace_crt(n, terms, rng, max_primes=12):
    """Exact basis over Q of {lam : sum lam_t U_t (x) V_t = 0}, via RREF mod several primes, CRT,
    rational reconstruction and an exact check. Returns a list of dicts term -> Fraction."""
    n2n3 = n[1] * n[2]
    collected = []  # (p, rows)
    pivots_ref = None
    for p in PRIMES[:max_primes]:
        rows = _nullspace_rref_mod(n, terms, rng, p)
        piv = tuple(min(row) for row in rows)
        if pivots_ref is None or len(piv) > len(pivots_ref):
            # a larger nullity mod p than before means the earlier primes were unlucky; restart
            if pivots_ref is not None and len(piv) > len(pivots_ref):
                collected = []
            pivots_ref = piv
        if piv != pivots_ref:
            continue  # unlucky prime (smaller nullity or different pivots): skip it
        collected.append((p, rows))
        if not pivots_ref:
            return []
        if len(collected) < 2:
            continue
        # CRT combine and reconstruct
        m = 1
        for q, _ in collected:
            m *= q
        basis = []
        ok = True
        for i in range(len(pivots_ref)):
            support = set()
            for _, rows_q in collected:
                support |= set(rows_q[i])
            vec = {}
            for t in support:
                acc, mod = 0, 1
                for q, rows_q in collected:
                    v = rows_q[i].get(t, 0)
                    # CRT step: acc mod `mod` and v mod q
                    inv = pow(mod % q, -1, q)
                    acc = acc + mod * ((v - acc) * inv % q)
                    mod *= q
                f = _ratrec(acc % mod, mod)
                if f is None:
                    ok = False
                    break
                if f:
                    vec[t] = f
            if not ok:
                break
            basis.append(vec)
        if not ok:
            continue
        # exact verification over Q
        good = True
        for vec in basis:
            acc = defaultdict(Fraction)
            for t, lam in vec.items():
                U, V, _ = terms[t]
                for a, ua in U.items():
                    for b, vb in V.items():
                        acc[a * n2n3 + b] += lam * ua * vb
            if any(x != 0 for x in acc.values()):
                good = False
                break
        if good:
            return basis
    raise RuntimeError("exact nullspace reconstruction failed; increase max_primes")


def _solve_rays(rays, rhs, k):
    """Solve rays[i] . Z = rhs[i] for Z (k rows of dicts) given independent rays (lists of Fractions)."""
    m = len(rays)
    R = [list(r) + [i] for i, r in enumerate(rays)]
    piv_cols = []
    rowsR = [list(r) for r in rays]
    rhsR = [dict(x) for x in rhs]
    # Gauss-Jordan on the m x k ray matrix, carrying rhs dicts
    prow = 0
    for col in range(k):
        sel = next((i for i in range(prow, m) if rowsR[i][col] != 0), None)
        if sel is None:
            continue
        rowsR[prow], rowsR[sel] = rowsR[sel], rowsR[prow]
        rhsR[prow], rhsR[sel] = rhsR[sel], rhsR[prow]
        pv = rowsR[prow][col]
        rowsR[prow] = [x / pv for x in rowsR[prow]]
        rhsR[prow] = {a: x / pv for a, x in rhsR[prow].items()}
        for i in range(m):
            if i != prow and rowsR[i][col] != 0:
                fct = rowsR[i][col]
                rowsR[i] = [x - fct * y for x, y in zip(rowsR[i], rowsR[prow])]
                d = dict(rhsR[i])
                for a, y in rhsR[prow].items():
                    z = d.get(a, 0) - fct * y
                    if z:
                        d[a] = z
                    else:
                        d.pop(a, None)
                rhsR[i] = d
        piv_cols.append(col)
        prow += 1
        if prow == m:
            break
    Z = [dict() for _ in range(k)]
    for i, col in enumerate(piv_cols):
        Z[col] = rhsR[i]
    return Z


def absorb_uv(n, terms, rng, log=None):
    """One absorption round on the (U,V) pairing, modifying W. Returns (terms, kills)."""
    n1, n2, n3 = n
    t0 = time.time()
    full = exact_nullspace_crt(n, terms, rng)
    t1 = time.time()
    if not full:
        return terms, 0
    sup = sorted(set().union(*[set(v) for v in full]))
    nullity = len(full)
    pos = {t: p for p, t in enumerate(sup)}
    basis = [{pos[t]: x for t, x in v.items()} for v in full]
    t2 = time.time()
    k = len(basis)
    # ell_t in Q^k for t in support (positions in sup)
    ell = [[b.get(p, Fraction(0)) for b in basis] for p in range(len(sup))]
    clusters = defaultdict(list)
    for p, t in enumerate(sup):
        lt = ell[p]
        nz = next((x for x in lt if x != 0), None)
        if nz is None:
            continue
        ray = tuple(x / nz for x in lt)
        W = terms[t][2]
        val = tuple(sorted((a, x / nz) for a, x in W.items()))
        clusters[(ray, val)].append(p)
    order = sorted(clusters, key=lambda key: -len(clusters[key]))
    chosen, span = [], []  # span: echelon rows of chosen rays
    for key in order:
        ray = list(key[0])
        r = list(ray)
        for piv, row in span:
            if r[piv] != 0:
                fct = r[piv] / row[piv]
                r = [x - fct * y for x, y in zip(r, row)]
        piv = next((i for i, x in enumerate(r) if x != 0), None)
        if piv is None:
            continue
        span.append((piv, r))
        chosen.append(key)
        if len(chosen) == k:
            break
    rays = [list(key[0]) for key in chosen]
    rhs = [{a: -x for a, x in key[1]} for key in chosen]
    Z = _solve_rays(rays, rhs, k)
    new_terms = list(terms)
    kills = 0
    for p, t in enumerate(sup):
        U, V, W = terms[t]
        W2 = dict(W)
        for j in range(k):
            lj = ell[p][j]
            if lj:
                for a, z in Z[j].items():
                    y = W2.get(a, 0) + lj * z
                    if y:
                        W2[a] = y
                    else:
                        W2.pop(a, None)
        new_terms[t] = (U, V, W2) if W2 else None
        if not W2:
            kills += 1
    if log:
        log(f"    absorb {n}: r={len(terms)} support={len(sup)} nullity(mod p)={nullity} exact={k} kills={kills}"
            f" t_proj={t1 - t0:.1f}s t_exact={t2 - t1:.1f}s t_kill={time.time() - t2:.1f}s")
    return [t for t in new_terms if t is not None], kills


def absorb_all(n, terms, rng, log=None, max_rounds=50):
    """Cycle through the three pairings until no pairing removes a term."""
    total = 0
    quiet = 0
    rot = 0
    for _ in range(max_rounds * 3):
        nn, tt = rotate_to(n, terms, rot)
        tt, kills = absorb_uv(nn, tt, rng, log)
        n, terms = rotate_to(nn, tt, 3 - rot)
        total += kills
        quiet = 0 if kills else quiet + 1
        if quiet >= 3:
            break
        rot = (rot + 1) % 3
    return terms, total


# ---------------------------------------------------------------- driver

def fmt(n):
    return "x".join(map(str, n))


def run(parent_path, axis, top, seed, outdir, verify=True, verbose=False):
    """Slice the parent along `axis` (0, 1, 2 = which of n1, n2, n3 shrinks), absorb, keep the best."""
    t0 = time.time()
    n, terms = load(parent_path)
    log = lambda s: print(s, flush=True)
    log(f"parent {fmt(n)} rank {len(terms)} ({parent_path}); shrinking axis {axis}")
    nr, tr = rotate_to(n, terms, axis)  # bring the axis to position 0
    cands = slice_candidates(nr, tr, top=top)
    best = None
    for idx, (kills, f, e) in enumerate(cands):
        rng = random.Random(seed + idx)
        ns, ts = slice_dim1(nr, tr, f, e)
        sliced = len(ts)
        ts2, absorbed = absorb_all(ns, ts, rng, log=log if verbose else None)
        child_n, child_t = rotate_to(ns, ts2, 3 - axis)
        log(f"  cand {idx}: f={dict(f)} e={dict(e)} slice-kills={len(tr) - sliced} "
            f"-> {sliced}, absorb -{absorbed} -> {len(child_t)}  [{fmt(child_n)}]  {time.time() - t0:.0f}s")
        if best is None or len(child_t) < len(best[1]):
            best = (child_n, child_t, f, e, len(tr) - sliced, absorbed)
    child_n, child_t, f, e, sk, ab = best
    ok = brent_ok(child_n, child_t) if verify else None
    out = f"{outdir}/{fmt(child_n)}_r{len(child_t)}_Q.json"
    note = (f"{fmt(child_n)} rank {len(child_t)} over Q: slice of {fmt(n)} rank {len(terms)} along axis {axis} "
            f"(f={dict(f)}, e={dict(e)}, -{sk}) then exact absorption (-{ab}).")
    save(out, child_n, child_t, note)
    log(f"BEST {fmt(child_n)} rank {len(child_t)} brent={'PASS' if ok else ok} -> {out} ({time.time() - t0:.0f}s)")
    return child_n, len(child_t), ok


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("parent")
    ap.add_argument("--axis", type=int, default=0)
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default=".")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    run(a.parent, a.axis, a.top, a.seed, a.out, verbose=a.verbose)
