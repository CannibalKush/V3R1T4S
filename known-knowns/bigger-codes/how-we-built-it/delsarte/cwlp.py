#!/usr/bin/env python3
"""cwlp.py -- library: Delsarte LP for constant-weight codes, plus SECOND-MOMENT (shortening)
constraints that couple the LP to upper bounds of shortened cells.

The dual eigenvalues Q_k(x) of the Johnson scheme J(n,w) (w <= n/2) are computed from
Delsarte's dual-Hahn closed form
    Q_k(x) = m_k * sum_{j=0}^{k} (-1)^j C(k,j) C(n+1-k,j) / (C(w,j) C(n-w,j)) * C(x,j),   m_k = C(n,k) - C(n,k-1),
(x = Johnson distance = half the Hamming distance), and cross-checked (selftest) against
  (a) the Eberlein form Q_k(x) = m_k E_x(k) / v_x, and
  (b) brute force: Q_k(x) = N * (E_k)_{uv} for d(u,v) = x, with E_k the primitive idempotents of small Johnson graphs
      computed numerically from the adjacency matrix.

Inner distribution a_x = |{(u,v) in C^2 : d_J(u,v) = x}| / |C|, a_0 = 1, a_x = 0 for 0 < x < delta = d/2.
Constraints used (all valid for every (n,d,w) code C):
  (D_k)   sum_x a_x Q_k(x) >= 0                                   [Delsarte 1973]
  (M_{t,s}) for 0<=s<=t:  sum_x C(w-x,s) C(n-w-x,t-s) a_x <= U(n-t,d,w-s) * C(w,s) C(n-w,t-s)
          [proof: for disjoint S1,S2 with |S1|=s, |S2|=t-s, C_{S1,S2} = {u in C : S1 <= u, S2 & u = 0} is an
           (n-t,d,w-s) code, so 0 <= |C_{S1,S2}| <= U; hence |C_{S1,S2}|^2 <= U |C_{S1,S2}|. Sum over (S1,S2):
           LHS = sum_{u,v in C} C(|u&v|,s) C(n-|u|v|,t-s) = |C| sum_x a_x C(w-x,s)C(n-w-x,t-s),
           RHS = U * sum_u C(w,s)C(n-w,t-s) = U |C| C(w,s)C(n-w,t-s). Divide by |C|.]
"""
from fractions import Fraction
from math import comb, floor
import numpy as np


def mult(n, k):
    return comb(n, k) - (comb(n, k - 1) if k > 0 else 0)


def Q_hahn(n, w, k, x):
    """Exact dual eigenvalue Q_k(x) of J(n,w), w <= n/2 (Delsarte's dual Hahn polynomial)."""
    s = Fraction(0)
    for j in range(k + 1):
        s += Fraction((-1) ** j * comb(k, j) * comb(n + 1 - k, j), comb(w, j) * comb(n - w, j)) * comb(x, j)
    return mult(n, k) * s


def E_eber(n, w, x, k):
    return sum((-1) ** j * comb(k, j) * comb(w - k, x - j) * comb(n - w - k, x - j) for j in range(x + 1))


def Q_eber(n, w, k, x):
    return Fraction(mult(n, k) * E_eber(n, w, x, k), comb(w, x) * comb(n - w, x))


def moment_coef(n, w, t, s, x):
    return comb(w - x, s) * comb(n - w - x, t - s) if (w - x >= 0 and n - w - x >= 0) else 0


def selftest(verbose=True):
    """Cross-check Q_hahn against Q_eber (exact, many (n,w)) and against brute-force idempotents (float, small)."""
    from itertools import combinations
    for n in range(2, 41):
        for w in range(0, n // 2 + 1):
            for k in range(w + 1):
                for x in range(w + 1):
                    assert Q_hahn(n, w, k, x) == Q_eber(n, w, k, x), (n, w, k, x)
    for (n, w) in [(6, 3), (7, 3), (8, 4), (9, 4), (10, 3), (10, 5), (11, 4)]:
        V = [frozenset(c) for c in combinations(range(n), w)]
        N = len(V)
        D = np.array([[w - len(a & b) for b in V] for a in V])
        A1 = (D == 1).astype(float)
        ev, U = np.linalg.eigh(A1)
        # eigenvalue of A1 on V_k is (w-k)(n-w-k)-k
        for k in range(w + 1):
            th = (w - k) * (n - w - k) - k
            idx = np.abs(ev - th) < 1e-6
            assert idx.sum() == mult(n, k), (n, w, k, idx.sum(), mult(n, k))
            Ek = U[:, idx] @ U[:, idx].T
            for x in range(w + 1):
                vals = N * Ek[D == x]
                q = float(Q_hahn(n, w, k, x))
                assert np.allclose(vals, q, atol=1e-6), (n, w, k, x, vals[:3], q)
    if verbose:
        print("selftest OK: Q_hahn == Q_eber exactly for n<=40; == N*E_k(u,v) by brute force for 7 small schemes")
    return True


# ---------------------------------------------------------------- float LP (search heuristic only, never a proof)
def lp_float(n, d, w, moments=(), caps=None, return_dual=False):
    """max 1 + sum_{x>=delta} a_x  s.t. Delsarte + moment rows.  moments: list of (t, s, U)."""
    from scipy.optimize import linprog
    w = min(w, n - w)
    delta = d // 2
    X = list(range(delta, w + 1))
    if not X:
        return 1.0, None
    A, b, names = [], [], []
    for k in range(1, w + 1):
        A.append([-float(Q_hahn(n, w, k, x)) for x in X]); b.append(float(mult(n, k))); names.append(("D", k))
    for (t, s, U) in moments:
        c0 = moment_coef(n, w, t, s, 0)
        if c0 == 0:
            continue
        row = [moment_coef(n, w, t, s, x) / c0 for x in X]
        A.append(row); b.append(float(U) - 1.0); names.append(("M", t, s, U))
    bounds = [(0, None)] * len(X)
    if caps:
        bounds = [(0, caps.get(x)) for x in X]
    r = linprog(-np.ones(len(X)), A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method="highs")
    if r.status != 0:
        return None, None
    val = 1 - r.fun
    if return_dual:
        return val, (names, -r.ineqlin.marginals, X, r.x)
    return val, None


# ---------------------------------------------------------------- doubly-constant-weight codes (product scheme)
def T_lp_float(w1, n1, w2, n2, d, return_sol=False):
    """Float Delsarte LP for T(w1,n1,w2,n2,d): codes in J(n1,w1) x J(n2,w2), Hamming distance >= d.
    Variables a_{x1,x2} (Johnson distances in each factor), (x1,x2) != (0,0), 2x1+2x2 >= d.
    Constraints: for every (k1,k2) != (0,0): sum a_{x1,x2} Q1_{k1}(x1) Q2_{k2}(x2) >= -Q1_{k1}(0) Q2_{k2}(0)."""
    from scipy.optimize import linprog
    w1 = min(w1, n1 - w1); w2 = min(w2, n2 - w2)
    X = [(x1, x2) for x1 in range(w1 + 1) for x2 in range(w2 + 1) if (x1, x2) != (0, 0) and 2 * x1 + 2 * x2 >= d]
    if not X:
        return 1.0
    Q1 = [[float(Q_hahn(n1, w1, k, x)) for x in range(w1 + 1)] for k in range(w1 + 1)]
    Q2 = [[float(Q_hahn(n2, w2, k, x)) for x in range(w2 + 1)] for k in range(w2 + 1)]
    A, b = [], []
    for k1 in range(w1 + 1):
        for k2 in range(w2 + 1):
            if (k1, k2) == (0, 0):
                continue
            A.append([-Q1[k1][x1] * Q2[k2][x2] for (x1, x2) in X]); b.append(Q1[k1][0] * Q2[k2][0])
    r = linprog(-np.ones(len(X)), A_ub=np.array(A), b_ub=np.array(b), bounds=[(0, None)] * len(X), method="highs")
    if r.status != 0:
        return None
    return (1 - r.fun, X, r.x) if return_sol else 1 - r.fun
