#!/usr/bin/env python3
"""fmmcheck.py SCHEME.json [SCHEME.json ...] [--primes K]
Check that a rational scheme for <n1,n2,n3> matrix multiplication satisfies the Brent equations, and count its rank.
Written for the V3R1T4S release from the definition; needs python3 + numpy only.

Scheme format (as in Perminov's FastMatrixMultiplication repository): JSON with
  n = [n1, n2, n3], u (r rows of length n1*n2), v (r rows of length n2*n3), w (r rows of length n3*n1),
  coefficients are integers or strings "p/q".
  Term k computes m_k = (sum_{ij} u[k][i*n2+j] A_ij) * (sum_{jl} v[k][j*n3+l] B_jl) and contributes
  w[k][l*n1+i] * m_k to C_il.
Brent equations: for all a=(i,j), b=(j',l), c=(l',i'):
  sum_k u[k][a] v[k][b] w[k][c] = [j = j'] [l = l'] [i = i'].
The rank is the number of terms k with u[k], v[k] and w[k] all nonzero (a term with a zero factor contributes nothing).

Method: the residual R(a,b,c) = sum_k u v w - delta is a rational number.  Let L be the lcm over k of
den(u[k]) * den(v[k]) * den(w[k]) (den = lcm of the denominators in that row).  Then L*R is an integer with
|L*R| <= L * (S + 1), where S = sum_k max|u[k]| max|v[k]| max|w[k]|.  We compute R modulo K primes p < 2^20 that do
not divide L (exact: residues < 2^20, numpy float64 matrix products of at most r terms stay below 2^53).  If R is 0
modulo every prime and the product of the primes exceeds 2*L*(S+1), then R = 0 exactly (Chinese remainder theorem).
The script adds primes until that bound is met (at least K, default 4), so a PASS is a proof, not a probabilistic test.
Last line: "FMMCHECK PASS ..." or "FMMCHECK FAIL ...".  Exit code 0 iff every scheme passes.
"""
import hashlib
import json
import math
import sys
from fractions import Fraction

import numpy as np


def primes_below(limit, count, avoid):
    out, x = [], limit - 1
    while len(out) < count:
        if x % 2 and all(x % d for d in range(3, int(x ** 0.5) + 1, 2)) and avoid % x:
            out.append(x)
        x -= 1
    return out


def check(path, min_primes):
    raw = open(path, "rb").read()
    d = json.loads(raw)
    n1, n2, n3 = (int(x) for x in d["n"])
    U, V, W = d["u"], d["v"], d["w"]
    r = len(U)
    assert len(V) == r and len(W) == r, "u, v, w have different lengths"
    assert all(len(x) == n1 * n2 for x in U) and all(len(x) == n2 * n3 for x in V) and all(len(x) == n3 * n1 for x in W), "bad row widths"
    cache = {}

    def fr(x):
        if x not in cache:
            cache[x] = Fraction(x) if isinstance(x, (int, str)) else Fraction(str(x))
        return cache[x]

    def row_stats(row):
        den, mx, nz = 1, Fraction(0), False
        for x in row:
            f = fr(x)
            if f:
                nz = True
                den = den * f.denominator // math.gcd(den, f.denominator)
                mx = max(mx, abs(f))
        return den, mx, nz

    L, S, rank = 1, Fraction(0), 0
    for k in range(r):
        du, mu, nu = row_stats(U[k]); dv, mv, nv = row_stats(V[k]); dw, mw, nw = row_stats(W[k])
        if nu and nv and nw:
            rank += 1
        t = du * dv * dw
        L = L * t // math.gcd(L, t)
        S += mu * mv * mw
    bound = 2 * L * (math.floor(S) + 2)
    primes = primes_below(1 << 20, min_primes, L)
    while math.prod(primes) <= bound:
        primes = primes_below(1 << 20, len(primes) + 1, L)

    A1, B1, C1 = n1 * n2, n2 * n3, n3 * n1
    bad_total = 0
    for p in primes:
        def mod(x):
            f = fr(x)
            return (f.numerator % p) * pow(f.denominator % p, -1, p) % p
        Um = np.array([[mod(x) for x in row] for row in U], dtype=np.float64)
        Vm = np.array([[mod(x) for x in row] for row in V], dtype=np.float64)
        Wm = np.array([[mod(x) for x in row] for row in W], dtype=np.float64)
        bad = 0
        for i in range(n1):
            for j in range(n2):
                a = i * n2 + j
                ks = np.nonzero(Um[:, a])[0]
                if len(ks):
                    blk = np.fmod(Um[ks, a][:, None] * Vm[ks, :], p)          # |ks| x B1, entries < p
                    with np.errstate(all="ignore"):   # some BLAS builds raise spurious FP flags; checked below
                        res = blk.T @ Wm[ks, :]                               # B1 x C1, exact (< 2^53)
                    if not np.isfinite(res).all() or res.max() >= 2.0 ** 53:
                        raise SystemExit("FMMCHECK FAIL non-exact floating point product")
                    res = np.fmod(res, p)
                else:
                    res = np.zeros((B1, C1))
                want = np.zeros((B1, C1))
                for l in range(n3):
                    want[j * n3 + l, l * n1 + i] = 1.0
                bad += int(np.count_nonzero(np.fmod(res - want + p, p)))
        bad_total += bad
        print(f"  mod {p}: violated Brent equations = {bad}")
    ok = bad_total == 0
    print(f"  checked {A1}*{B1}*{C1} = {A1 * B1 * C1} Brent equations modulo {len(primes)} primes; "
          f"log2(prod primes) = {math.log2(math.prod(primes)):.1f} > log2(2 L (S+1)) = {math.log2(bound):.1f}")
    status = "PASS" if ok else "FAIL"
    print(f"FMMCHECK {status} file={path.split('/')[-1]} format=<{n1},{n2},{n3}> sorted=<{','.join(map(str, sorted([n1, n2, n3])))}> "
          f"terms={r} rank_nonzero_terms={rank} sha256={hashlib.sha256(raw).hexdigest()}")
    return ok


def main():
    args = sys.argv[1:]
    k = 4
    if "--primes" in args:
        i = args.index("--primes"); k = int(args[i + 1]); del args[i:i + 2]
    if not args:
        print(__doc__); sys.exit(2)
    allok = True
    for f in args:
        allok &= check(f, k)
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
