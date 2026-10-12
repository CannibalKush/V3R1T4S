#!/usr/bin/env python3
"""certify.py SUMMARY.json E  ->  certificate JSON on stdout (exit 0 iff the verdict holds).

Verdict "no Lehmer number N <= 10^E" follows from three exact steps:
 (A) 3 | N  =>  every other prime factor p has p == 2 (mod 3) (p == 1 would give 3 | p-1 | phi(N) | N-1), so
     phi(N) == 2 * 1 == 2 and N - 1 == 2 (mod 3)... precisely: N-1 = k phi(N) with phi(N) = 2 prod(p-1), prod(p-1) == 1
     (mod 3), N == 0 => -1 == 2k (mod 3) => k == 1 (mod 3) => k >= 4 (k = 1 iff N prime)  =>  N/phi(N) > 4.
     But the prime factors lie in L3 = [3] + primes == 2 (mod 3), so omega(N) <= m3 (the product of the m3+1 smallest
     elements of L3 exceeds 10^E) and N/phi(N) <= prod over the m3 smallest elements of L3 of p/(p-1) < 4.
 (B) 3 does not divide N  =>  N/phi(N) <= prod over the m5 smallest primes >= 5 of p/(p-1) < 3 (m5 likewise), and
     k < N/phi(N), k >= 2 (k = 1 iff N prime)  =>  k = 2, i.e. P - 2*Phi = 1 with all prime factors >= 5.
 (C) the LCRT run bound to X = 10^E (sigma = +1, pmin = 5, CRT prune on) is complete (every task present, no
     conflicting duplicates, DONE marker) and reports no integral completion that is a SOLUTION; events of any other
     reason are listed (they are not Lehmer numbers by construction: cap / C-violation / composite r).
All ratios are exact Fractions; primes from sympy.
"""
import json, sys, hashlib
from fractions import Fraction
from sympy import nextprime

def bound(E, first):
    """first=3: list L3 = [3] + primes == 2 (mod 3); first=5: all primes >= 5.  Returns (omega_max, ratio bound)."""
    X = 10 ** E
    m, prod, ratio, p = 0, 1, Fraction(1), first
    while prod * p <= X:
        prod *= p; ratio *= Fraction(p, p - 1); m += 1
        p = nextprime(p)
        if first == 3:
            while p % 3 != 2: p = nextprime(p)
    return m, ratio

def main():
    path, E = sys.argv[1], int(sys.argv[2])
    raw = open(path, 'rb').read()
    s = json.loads(raw)
    X = 10 ** E
    m3, r3 = bound(E, 3)
    m5, r5 = bound(E, 5)
    A_ok = r3 < 4
    B_ok = r5 < 3
    bind_ok = (str(s.get('X')) == str(X) and int(str(s.get('sigma'))) == 1 and int(s.get('pmin')) == 5
               and int(s.get('crt')) == 1)
    complete = bool(s.get('complete')) and s.get('missing_tasks') == 0 and s.get('duplicate_conflicts') == 0
    sols = [e for e in s.get('events', []) if e.get('reason') == 'SOLUTION']
    C_ok = bind_ok and complete and not sols
    verdict = A_ok and B_ok and C_ok
    out = {
        "summary_file": path, "summary_sha256": hashlib.sha256(raw).hexdigest(), "E": E, "X": str(X),
        "A_3_divides_N": {"omega_max": m3, "ratio_bound": float(r3), "ratio_bound_exact_lt_4": A_ok},
        "B_k_ge_3": {"omega_max": m5, "ratio_bound": float(r5), "ratio_bound_exact_lt_3": B_ok},
        "C_search": {"X_bound_to_summary": bind_ok, "complete": complete, "kmax": s.get('kmax'),
                     "live_nodes": s.get('live_total'), "digest_live": s.get('digest_live'),
                     "visited_nodes": s.get('nodes_total'), "events": s.get('events'), "solutions": sols},
        "VERDICT": ("NO LEHMER NUMBER N <= 10^%d" % E) if verdict else "NOT CERTIFIED",
    }
    print(json.dumps(out, indent=1))
    sys.exit(0 if verdict else 1)

if __name__ == '__main__':
    main()
