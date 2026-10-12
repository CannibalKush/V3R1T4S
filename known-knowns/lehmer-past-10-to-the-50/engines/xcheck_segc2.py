#!/usr/bin/env python3
"""xcheck_segc2.py LOGFILE E [--primepi]

Independent algebraic cross-check of the C2 ranges that lcrt5 enumerated with its segmented sieve (the "SEGC2" lines
it prints for ranges longer than 1e8 beyond the main sieve).  It does NOT use any prime enumeration:

For a node with prefix (P, Phi), A = 2 Phi - P > 0, sigma = 1, a C2 completion is a prime q with u = A q - 2 Phi > 0
dividing n = 2 Phi (q - 1) - sigma (then r = n / u).  Since A n = 2 Phi u + D with D = 4 Phi^2 - 2 Phi A - A sigma,
u | n implies u | D.  So every integral C2 completion with q in [qa, qb] gives a divisor d = u of D with
d == -2 Phi (mod A) and A qa - 2 Phi <= d <= A qb - 2 Phi.  We factor D completely (sympy factorint, every factor
proven prime by isprime, which is deterministic below 2^64 and BPSW above), enumerate those divisors, and test each
for u | n.  "0 hits" is an independent proof that the range has no integral completion (the engine says c2i = 0).

It also recomputes qa and qb from the LCAP-1 definitions (exact integers):
  lo = max(p_last + 1, floor(2 Phi / A) + 1), qmax0 = isqrt(floor(X / P)),
  h(q) = A q^2 - 4 Phi q + 2 Phi + sigma, qb = largest q in [lo, qmax0] with h(q) < 0,
  cap(q): P q n(q) <= X u(q);  qa = least q in [lo, qb] with cap(q) (the cap set is a final segment).
With --primepi it also counts the primes in [qa, qb] with sympy.primepi (an independent prime-counting algorithm) and
compares with the engine's segprimes count (the engine's count covers only (max(qa, sieve_last), qb], see 'seg_from').
"""
import sys, re, json
from math import isqrt, prod
from sympy import factorint, isprime, primepi, prevprime
from itertools import product as iproduct

def divisors_from(f):
    items = list(f.items())
    for exps in iproduct(*[range(e + 1) for _, e in items]):
        d = 1
        for (p, _), e in zip(items, exps):
            d *= p ** e
        yield d

def qa_qb(pref, X, sigma=1):
    P = prod(pref); Phi = prod(p - 1 for p in pref); A = 2 * Phi - P
    assert A > 0
    lo = max(pref[-1] + 1, (2 * Phi) // A + 1)
    qmax0 = isqrt(X // P)
    h = lambda q: A * q * q - 4 * Phi * q + 2 * Phi + sigma
    cap = lambda q: P * q * (2 * Phi * (q - 1) - sigma) <= X * (A * q - 2 * Phi)
    if not h(lo) < 0:
        return None
    # largest q in [lo, qmax0] with h(q) < 0: h is a convex quadratic, negative on an interval containing lo
    a, b = lo, qmax0
    if h(b) < 0:
        qb = b
    else:
        while b - a > 1:
            m = (a + b) // 2
            if h(m) < 0: a = m
            else: b = m
        qb = a
    if not cap(qb):
        return None
    if cap(lo):
        qa = lo
    else:
        a, b = lo, qb          # cap(a) false, cap(b) true
        while b - a > 1:
            m = (a + b) // 2
            if cap(m): b = m
            else: a = m
        qa = b
    return P, Phi, A, lo, qa, qb

def main():
    log, E = sys.argv[1], int(sys.argv[2])
    do_pi = '--primepi' in sys.argv
    X = 10 ** E
    sigma = 1
    sieve_last = None
    out = []
    for line in open(log):
        m = re.search(r'sieve: \d+ primes >= 3 up to (\d+)', line)
        if m:
            sieve_last = prevprime(int(m.group(1)) + 1)
        if not line.startswith('SEGC2'):
            continue
        m = re.match(r'SEGC2 depth (\d+) prefix ([\d ]+) qa (\d+) qb (\d+) segprimes (\d+)', line)
        depth, pref, qa_e, qb_e, segp = int(m.group(1)), [int(x) for x in m.group(2).split()], int(m.group(3)), int(m.group(4)), int(m.group(5))
        assert len(pref) == depth
        r = qa_qb(pref, X, sigma)
        P, Phi, A, lo, qa, qb = r
        D = 4 * Phi * Phi - 2 * Phi * A - A * sigma
        f = factorint(D)
        assert prod(p ** e for p, e in f.items()) == D and all(isprime(p) for p in f)
        dlo, dhi = A * qa - 2 * Phi, A * qb - 2 * Phi
        cand = hits = 0
        for d in divisors_from(f):
            if dlo <= d <= dhi and (d + 2 * Phi) % A == 0:
                cand += 1
                q = (d + 2 * Phi) // A
                if (2 * Phi * (q - 1) - sigma) % d == 0:
                    hits += 1
        rec = {"prefix": pref, "qa_engine": qa_e, "qb_engine": qb_e, "qa_recomputed": qa, "qb_recomputed": qb,
               "range_match": (qa, qb) == (qa_e, qb_e), "D_digits": len(str(D)), "D_factors": {str(p): e for p, e in f.items()},
               "n_divisors": prod(e + 1 for e in f.values()), "divisors_in_range_and_class": cand, "integral_completions": hits}
        if do_pi:
            seg_from = max(qa, sieve_last + 1)
            cnt = int(primepi(qb) - primepi(seg_from - 1))
            rec.update({"seg_from": seg_from, "segprimes_engine": segp, "primepi_count": cnt, "count_match": cnt == segp})
        out.append(rec)
        print(json.dumps(rec), flush=True)
    ok = all(r["range_match"] and r["integral_completions"] == 0 and r.get("count_match", True) for r in out)
    print(json.dumps({"E": E, "ranges": len(out), "ALL_OK": ok}))

if __name__ == '__main__':
    main()
