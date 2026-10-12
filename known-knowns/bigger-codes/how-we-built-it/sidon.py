#!/usr/bin/env python3
"""S2 sets (all ordered differences distinct => all sums of two distinct elements distinct) for the
Graham-Sloane construction of constant-weight codes with d = 6.  Pure-python finite fields (no galois).

bose(q)   : q elements in Z_{q^2-1}      (Bose 1942)     {log_theta(theta + c) : c in GF(q)}
singer(q) : q+1 elements in Z_{q^2+q+1} (Singer 1938)   {log_theta(c0 + c1 theta) mod (q^2+q+1)}
Every set returned is verified to be Sidon by is_sidon().
"""
import itertools
import sys


def factor_primes(N):
    ps, d = [], 2
    while d * d <= N:
        if N % d == 0:
            ps.append(d)
            while N % d == 0:
                N //= d
        d += 1
    if N > 1:
        ps.append(N)
    return ps


def prime_power(q):
    for p in range(2, q + 1):
        if q % p == 0:
            e, t = 0, q
            while t % p == 0:
                t //= p
                e += 1
            assert t == 1, "q must be a prime power"
            return p, e


def mulmod(a, b, f, p):
    """polys as tuples low->high, f monic of degree K given as tuple of K low coeffs (x^K = -sum f_i x^i)."""
    K = len(f)
    r = [0] * (2 * K - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    r[i + j] = (r[i + j] + ai * bj) % p
    for deg in range(2 * K - 2, K - 1, -1):
        c = r[deg]
        if c:
            r[deg] = 0
            for i in range(K):
                r[deg - K + i] = (r[deg - K + i] - c * f[i]) % p
    return tuple(r[:K])


def powmod(a, e, f, p):
    K = len(f)
    res = tuple([1] + [0] * (K - 1))
    while e:
        if e & 1:
            res = mulmod(res, a, f, p)
        a = mulmod(a, a, f, p)
        e >>= 1
    return res


def primitive_poly(p, K):
    N = p ** K - 1
    ps = factor_primes(N)
    one = tuple([1] + [0] * (K - 1))
    x = tuple([0, 1] + [0] * (K - 2)) if K >= 2 else None
    for coeffs in itertools.product(range(p), repeat=K):
        if coeffs[0] == 0:
            continue
        f = coeffs
        if powmod(x, N, f, p) != one:
            continue
        if all(powmod(x, N // r, f, p) != one for r in ps):
            return f
    raise RuntimeError("no primitive poly")


def field_tables(p, K):
    f = primitive_poly(p, K)
    N = p ** K - 1
    x = tuple([0, 1] + [0] * (K - 2))
    pw = [tuple([1] + [0] * (K - 1))]
    for a in range(1, N):
        pw.append(mulmod(pw[-1], x, f, p))
    log = {v: a for a, v in enumerate(pw)}
    assert len(log) == N
    return f, pw, log


def add(a, b, p):
    return tuple((u + v) % p for u, v in zip(a, b))


def is_sidon(A, m):
    seen = set()
    for x in A:
        for y in A:
            if x != y:
                dlt = (x - y) % m
                if dlt in seen:
                    return False
                seen.add(dlt)
    return True


def is_weak_sidon(A, m):
    seen = set()
    A = list(A)
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            s = (A[i] + A[j]) % m
            if s in seen:
                return False
            seen.add(s)
    return True


def subfield(q, p, K, pw):
    N = p ** K - 1
    step = N // (q - 1)
    zero = tuple([0] * K)
    return [zero] + [pw[j * step] for j in range(q - 1)]


def bose(q):
    p, e = prime_power(q)
    K = 2 * e
    f, pw, log = field_tables(p, K)
    th = pw[1]
    A = sorted(log[add(th, c, p)] for c in subfield(q, p, K, pw))
    m = q * q - 1
    assert len(set(A)) == q and is_sidon(A, m)
    return A, m


def singer(q):
    p, e = prime_power(q)
    K = 3 * e
    f, pw, log = field_tables(p, K)
    th = pw[1]
    m = q * q + q + 1
    sub = subfield(q, p, K, pw)
    zero = tuple([0] * K)
    S = set()
    for c0 in sub:
        for c1 in sub:
            v = add(c0, mulmod(c1, th, f, p), p)
            if v != zero:
                S.add(log[v] % m)
    A = sorted(S)
    assert len(A) == q + 1 and is_sidon(A, m)
    return A, m


if __name__ == "__main__":
    for q in (23, 25, 27, 29):
        A, m = bose(q)
        print("bose", q, m, len(A), A, flush=True)
    for q in (23, 25, 27):
        A, m = singer(q)
        print("singer", q, m, len(A), A, flush=True)
