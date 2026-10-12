#!/usr/bin/env python3
"""delsarte_check.py cert.json [cert.json ...]  --  exact check of a Delsarte-LP dual certificate (pure python3).

A certificate proves A(n, d, w) <= U for a binary constant-weight code in the Johnson scheme J(n, w).

Johnson scheme J(n,w): vertices are the w-subsets of an n-set; x, y are in relation i (0 <= i <= w) iff |x \\ y| = i,
i.e. their characteristic vectors have Hamming distance 2i.
  valencies        v_i = C(w,i) C(n-w,i)
  multiplicities   m_k = C(n,k) - C(n,k-1)
  eigenvalues      E_i(k) = sum_j (-1)^j C(k,j) C(w-k,i-j) C(n-w-k,i-j)      (Eberlein polynomials)
  dual eigenvalues Q_k(i) = m_k E_i(k) / v_i
Delsarte LP for A(n, 2*delta, w): maximise 1 + sum_{i>=delta} a_i subject to a_i >= 0 and
  m_k + sum_i a_i Q_k(i) >= 0 for k = 1..w.  Its dual: minimise 1 + sum_k m_k y_k subject to y_k >= 0 and
  1 + sum_k y_k Q_k(i) <= 0 for every i in [delta, w].  Weak duality gives |C| <= 1 + sum_k m_k y_k for any dual
  feasible y, so A(n,2delta,w) <= floor(1 + sum_k m_k y_k).

Certificate JSON fields used: n, d, w, y (dual multipliers, rationals as strings), U (claimed floor), and optionally
a (a primal solution; if present, the checker verifies primal feasibility and primal = dual, i.e. LP optimality)
and lp_optimum.  All arithmetic is exact (fractions.Fraction).  The checker also verifies P Q = C(n,w) I as a sanity
check of its own eigenmatrices.

Exit code 0 iff every certificate is valid.
"""
import json
import sys
from fractions import Fraction as F
from math import comb


def eberlein(n, w, i, k):
    return sum((-1) ** j * comb(k, j) * comb(w - k, i - j) * comb(n - w - k, i - j) for j in range(i + 1))


def matrices(n, w):
    v = [comb(w, i) * comb(n - w, i) for i in range(w + 1)]
    m = [comb(n, k) - (comb(n, k - 1) if k >= 1 else 0) for k in range(w + 1)]
    P = [[F(eberlein(n, w, i, k)) for k in range(w + 1)] for i in range(w + 1)]   # P[i][k] = E_i(k)
    Q = [[F(m[k]) * P[i][k] / v[i] for i in range(w + 1)] for k in range(w + 1)]  # Q[k][i]
    return v, m, P, Q


def check(path):
    c = json.load(open(path))
    n, d, w = c["n"], c["d"], c["w"]
    assert d % 2 == 0, "d must be even"
    delta = d // 2
    v, m, P, Q = matrices(n, w)
    Nv = comb(n, w)
    for i in range(w + 1):
        for j in range(w + 1):
            s = sum(P[i][k] * Q[k][j] for k in range(w + 1))
            assert s == (Nv if i == j else 0), "eigenmatrix sanity check P Q = N I failed"
    y = {int(k): F(val) for k, val in c["y"].items()}
    problems = []
    if any(val < 0 for val in y.values()):
        problems.append("negative dual multiplier")
    if any(not (1 <= k <= w) for k in y):
        problems.append("dual index outside 1..w")
    worst = None
    for i in range(delta, w + 1):
        s = 1 + sum(yk * Q[k][i] for k, yk in y.items())
        worst = s if worst is None or s > worst else worst
        if s > 0:
            problems.append("dual constraint violated at i=%d: %s > 0" % (i, s))
    bound = 1 + sum(yk * m[k] for k, yk in y.items())
    U = bound.numerator // bound.denominator
    if U != c["U"]:
        problems.append("floor(bound) = %d != stated U = %d" % (U, c["U"]))
    if "lp_optimum" in c and F(c["lp_optimum"]) != bound:
        problems.append("stated lp_optimum differs from the dual objective")
    primal_eq = None
    if "a" in c:
        a = {int(i): F(val) for i, val in c["a"].items()}
        full = [F(0)] * (w + 1)
        full[0] = F(1)
        for i, ai in a.items():
            if not (delta <= i <= w) or ai < 0:
                problems.append("bad primal entry a_%d" % i)
            full[i] = ai
        for k in range(w + 1):
            if sum(full[i] * Q[k][i] for i in range(w + 1)) < 0:
                problems.append("primal Delsarte inequality violated at k=%d" % k)
        primal_eq = (sum(full) == bound)
        if not primal_eq:
            problems.append("primal objective != dual objective")
    valid = not problems
    print("%s  A(%d,%d,%d) <= %d   dual bound = %s = %.6f   worst dual row = %s   primal==dual: %s   %s" %
          (path.split("/")[-1], n, d, w, U, bound, float(bound), worst, primal_eq, "VALID" if valid else "INVALID: " + "; ".join(problems)))
    return valid


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    ok = True
    for p in sys.argv[1:]:
        ok &= check(p)
    print("ALL CERTIFICATES VALID" if ok else "SOME CERTIFICATE INVALID")
    sys.exit(0 if ok else 1)
