#!/usr/bin/env python3
"""Independent exact check of the two analytic reductions (independent engine 2).

Definition used: a Lehmer number is a composite n with phi(n) | n - 1.
Write n - 1 = k*phi(n).  Standard facts (see ../README.md):
  n odd, squarefree, k >= 2, and p | n, q | n  =>  p does not divide q - 1.
  n/phi(n) = k + 1/phi(n) > k.

Lemma A: 3 | n  =>  every other prime p | n has p == 2 (mod 3) (since 3 does not divide p-1),
         phi(n) == 2 (mod 3), n-1 == 2 (mod 3), so 2k == 2 (mod 3), k == 1 (mod 3), k >= 4,
         so n/phi(n) > 4.  For n <= X the largest possible n/phi(n) is reached by the greedy
         prefix 3, 5, 11, 17, ... (primes == 2 mod 3) of maximal length with product <= X.
Lemma B: 3 does not divide n => all primes >= 5; k >= 3 needs n/phi(n) > 3; greedy prefix 5,7,11,...
All ratios are exact Fractions.
"""
from fractions import Fraction
import sys
from sympy import nextprime

def greedy(X, first, pred):
    primes = list(first)
    prod = 1
    for p in primes:
        prod *= p
    assert prod <= X
    p = primes[-1] if primes else 2
    while True:
        p = nextprime(p)
        if not pred(p):
            continue
        if prod * p > X:
            break
        primes.append(p)
        prod *= p
    r = Fraction(1)
    for q in primes:
        r *= Fraction(q, q - 1)
    return primes, prod, r

def main():
    for E in [int(e) for e in (sys.argv[1:] or ["46", "48", "50"])]:
        X = 10 ** E
        pa, proda, ra = greedy(X, [3], lambda p: p % 3 == 2)
        pb, prodb, rb = greedy(X, [], lambda p: p >= 5)
        print(f"E={E}: Lemma A (3|n): omega<= {len(pa)} ratio_max={float(ra):.12f} <4: {ra < 4}"
              f" | Lemma B (3!|n): omega<= {len(pb)} ratio_max={float(rb):.12f} <3: {rb < 3}"
              f" | kmin needs omega>= {min(i+1 for i in range(len(pb)) if __import__('math').prod(Fraction(q,q-1) for q in pb[:i+1]) > 2)}")

if __name__ == "__main__":
    main()
