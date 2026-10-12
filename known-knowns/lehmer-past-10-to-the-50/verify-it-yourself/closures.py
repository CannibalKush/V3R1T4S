#!/usr/bin/env python3
"""closures.py [E ...]  --  exact rational check of the two analytic reductions used for X = 10^E (pure python3).

Definitions.  A Lehmer number is a composite N with phi(N) | N - 1; write N - 1 = k phi(N), k >= 2.
Standard facts (re-derived in README.md): N is odd and squarefree, and if p, q are prime factors then p does not
divide q - 1 (otherwise p | phi(N) | N - 1 and p | N).  Also N/phi(N) = k + 1/phi(N) > k.

Lemma A (3 | N).  Every other prime factor p satisfies p == 2 (mod 3), so phi(N) == 2 (mod 3), N - 1 == 2 (mod 3),
  hence 2k == 2 (mod 3), k == 1 (mod 3), and k >= 4, so N/phi(N) > 4.  But for N <= X the ratio N/phi(N) is at most
  the product of p/(p-1) over the greedy prefix 3, 5, 11, 17, 23, ... (3 and primes == 2 mod 3) of maximal length with
  product <= X.  If that product of ratios is < 4, no Lehmer number N <= X is divisible by 3.
Lemma B (3 does not divide N).  All prime factors are >= 5, so N/phi(N) <= product of p/(p-1) over the greedy prefix
  5, 7, 11, 13, ... with product <= X.  If that is < 3 then k = 2, i.e. N - 1 = 2 phi(N).

So for X = 10^50 the exhaustive search only has to cover N - 1 = 2 phi(N) with all prime factors >= 5.
Expected output for E = 50: Lemma A omega_max 27, ratio 2.928933... < 4; Lemma B omega_max 30, ratio 2.949927... < 3.
Both lemmas keep holding up to E = 56 and Lemma B fails at E = 58 (ratio 3.013 > 3); the shipped search is for E = 50.
"""
import json
import sys
from fractions import Fraction


def primes_upto(limit):
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytearray(len(sieve[p * p::p]))
    return [i for i, s in enumerate(sieve) if s]


def greedy(X, candidates):
    prod, ratio, m = 1, Fraction(1), 0
    for p in candidates:
        if prod * p > X:
            return m, ratio
        prod *= p
        ratio *= Fraction(p, p - 1)
        m += 1
    raise RuntimeError("prime table too small")


def main():
    Es = [int(e) for e in sys.argv[1:]] or [50]
    limit = 10 ** 5
    primes = primes_upto(limit)
    for E in Es:
        X = 10 ** E
        L3 = [3] + [p for p in primes if p % 3 == 2 and p >= 5]
        L5 = [p for p in primes if p >= 5]
        mA, rA = greedy(X, L3)
        mB, rB = greedy(X, L5)
        out = {"E": E,
               "lemma_A_3_divides_N": {"omega_max": mA, "ratio_max": str(rA), "ratio_float": float(rA), "ratio_lt_4": rA < 4},
               "lemma_B_3_not_divides_N": {"omega_max": mB, "ratio_max": str(rB), "ratio_float": float(rB), "ratio_lt_3": rB < 3},
               "search_reduces_to_k_eq_2_primes_ge_5": bool(rA < 4 and rB < 3)}
        print(json.dumps(out))


if __name__ == "__main__":
    main()
