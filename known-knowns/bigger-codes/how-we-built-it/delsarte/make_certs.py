#!/usr/bin/env python3
"""make_certs.py -- EXACT optimal Delsarte-LP primal/dual pair for A(n,d,w) (Johnson scheme).

Method:
  1. float LP (HiGHS) only to GUESS the optimal basis: support K of the dual y and support X* of the primal a;
  2. solve the two square systems EXACTLY over Q (fractions, Gaussian elimination):
        dual   : sum_{k in K} y_k Q_k(x) = -1        for x in X*
        primal : sum_{x in X*} a_x Q_k(x) = -m_k     for k in K       (m_k = Q_k(0))
  3. check exactly: y >= 0, sum_k y_k Q_k(x) <= -1 for ALL x = delta..w (dual feasible),
                    a >= 0, sum_x a_x Q_k(x) >= -m_k for ALL k = 1..w   (primal feasible),
     then LP optimum = 1 + sum a_x = 1 + sum y_k m_k exactly (weak duality both ways).
  If the basis guess is degenerate, fall back to rational rounding of y + exact rescaling (valid, maybe not optimal).
Output: one JSON certificate per cell (y as exact fraction strings, the exact LP optimum, the primal a for the record).
usage: make_certs.py N D W OUTDIR
"""
import json, os, sys
from fractions import Fraction
from math import comb, floor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cwlp import Q_hahn, mult, lp_float
import numpy as np
from scipy.optimize import linprog


def solve_exact(M, b):
    """Gaussian elimination over Q; M square list of lists of Fractions. Returns x or None if singular."""
    n = len(M)
    A = [list(map(Fraction, row)) + [Fraction(bi)] for row, bi in zip(M, b)]
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None:
            return None
        A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


def exact_delsarte(n, d, w):
    w = min(w, n - w)
    delta = d // 2
    X = list(range(delta, w + 1))
    K = list(range(1, w + 1))
    Q = {(k, x): Q_hahn(n, w, k, x) for k in range(w + 1) for x in range(w + 1)}
    m = {k: mult(n, k) for k in range(w + 1)}
    # float dual: min sum_k y_k m_k  s.t. sum_k y_k Q_k(x) <= -1 (x in X), y >= 0 ; scale by z_k = y_k m_k
    A = np.array([[float(Q[(k, x)] / m[k]) for k in K] for x in X])
    r = linprog(np.ones(len(K)), A_ub=A, b_ub=-np.ones(len(X)), bounds=[(0, None)] * len(K), method="highs")
    assert r.status == 0, r.message
    z = r.x
    a_float = -r.ineqlin.marginals          # primal a_x (dual of the dual)
    Ks = [k for k, zk in zip(K, z) if zk > 1e-9]
    Xs = [x for x, ax in zip(X, a_float) if ax > 1e-9]
    res = dict(n=n, d=d, w=w, delta=delta, float_value=1 + float(r.fun))
    if len(Ks) == len(Xs):
        y = solve_exact([[Q[(k, x)] for k in Ks] for x in Xs], [-1] * len(Xs))
        a = solve_exact([[Q[(k, x)] for x in Xs] for k in Ks], [-m[k] for k in Ks])
        if y is not None and a is not None:
            yd = dict(zip(Ks, y)); ad = dict(zip(Xs, a))
            dual_ok = all(v >= 0 for v in y) and all(sum(yd[k] * Q[(k, x)] for k in Ks) <= -1 for x in X)
            primal_ok = all(v >= 0 for v in a) and all(sum(ad[x] * Q[(k, x)] for x in Xs) >= -m[k] for k in K)
            if dual_ok and primal_ok:
                Ud = 1 + sum(yd[k] * m[k] for k in Ks)
                Up = 1 + sum(a)
                assert Ud == Up, (Ud, Up)
                res.update(y={str(k): str(v) for k, v in yd.items()}, a={str(x): str(v) for x, v in ad.items()},
                           lp_optimum=str(Ud), U=floor(Ud), optimal=True,
                           method="exact optimal basis (float LP guess, exact Gaussian elimination over Q)")
                return res
    # fallback: rounding + rescale
    zr = [max(Fraction(0), Fraction(float(v)).limit_denominator(10 ** 7)) for v in z]
    y = {k: zk / m[k] for k, zk in zip(K, zr) if zk != 0}
    s = [sum(y[k] * Q[(k, x)] for k in y) for x in X]
    assert all(si < 0 for si in s)
    c = max(Fraction(1), max(Fraction(-1) / si for si in s))
    y = {k: c * v for k, v in y.items()}
    Ud = 1 + sum(y[k] * m[k] for k in y)
    res.update(y={str(k): str(v) for k, v in y.items()}, lp_optimum=None, bound=str(Ud), U=floor(Ud), optimal=False,
               method="rounded float dual + exact rescale (valid, not proved optimal)")
    return res


if __name__ == "__main__":
    n, d, w, outdir = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    os.makedirs(outdir, exist_ok=True)
    c = exact_delsarte(n, d, w)
    c["claimed_U"] = c["U"]
    fn = os.path.join(outdir, f"cert_A{n}_{d}_{w}.json")
    json.dump(c, open(fn, "w"), indent=1)
    lo = c.get("lp_optimum") or c.get("bound")
    print(f"A({n},{d},{w}): float {c['float_value']:.6f}  exact {'LP optimum' if c['optimal'] else 'bound'} {lo} "
          f"= {float(Fraction(lo)):.6f}  -> U = {c['U']}  [{fn}]")
