#!/usr/bin/env python3
"""check_fmm.py SCHEME.json [--expect-rank R]
Standalone exact checker for a bilinear matrix multiplication scheme, written from the definition.
Standard library only.

Format (Perminov style): JSON with n = [n1, n2, n3] and rows u, v, w, either dense lists (lengths n1*n2, n2*n3,
n3*n1) or, when encoding == "sparse_flat_pairs", flat lists [index, value, index, value, ...], or, when
encoding == "vocab_rle_v1", strings of indices into the list "vocab" with "i*k" for k repeats of index i. Values are integers
or "p/q" strings. Term k computes (sum_ij u[k][i*n2+j] A_ij) * (sum_jl v[k][j*n3+l] B_jl) and adds w[k][l*n1+i]
times it to C_il.

Brent equations: for all index triples, sum_k u[k][i*n2+j] v[k][j2*n3+l] w[k][l2*n1+i2] = [i=i2][j=j2][l=l2].

Exactness: with D = lcm over all coefficients' denominators, D^3 * (residual) is an integer for every triple, and
|D^3 * residual| <= D^3 * (S + 1), where S = sum_k max|u_k| max|v_k| max|w_k|. The residuals are computed modulo
distinct primes near 2^61 until the primes' product exceeds 2 D^3 (S + 1); a residual that is zero modulo all of
them is exactly zero (Chinese remainder theorem). So PASS is a proof, not a probabilistic test.
The rank is the number of terms whose three factors are all nonzero. Last line: "PASS ..." or "FAIL ...".
"""
import json
import sys
from fractions import Fraction
from math import gcd


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):  # deterministic for n < 3.3e24
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


def rle_row(row, vocab, length):
    """vocab_rle_v1: a comma-separated row of vocabulary indices, 'i*k' meaning index i repeated k times."""
    dense = []
    for tok in row.split(","):
        if "*" in tok:
            i, k = tok.split("*")
            dense += [vocab[int(i)]] * int(k)
        else:
            dense.append(vocab[int(tok)])
    if len(dense) != length:
        raise ValueError(f"decoded row has length {len(dense)}, expected {length}")
    return list(enumerate(dense))


def rows(d, key, length):
    out = []
    for row in d[key]:
        if d.get("encoding") == "sparse_flat_pairs":
            pairs = list(zip(row[0::2], row[1::2]))
        elif d.get("encoding") == "vocab_rle_v1":
            pairs = rle_row(row, d["vocab"], length)
        else:
            if len(row) != length:
                raise ValueError(f"{key} row has length {len(row)}, expected {length}")
            pairs = list(enumerate(row))
        r = {}
        for a, x in pairs:
            if not (isinstance(a, int) and 0 <= a < length):
                raise ValueError(f"{key} index {a!r} out of range")
            if isinstance(x, bool) or not isinstance(x, (int, str)):
                raise ValueError(f"{key} coefficient {x!r} is not an integer or 'p/q' string")
            v = Fraction(x)
            if v:
                r[a] = r.get(a, 0) + v
        out.append({a: v for a, v in r.items() if v})
    return out


def main():
    args = sys.argv[1:]
    path = args[0]
    expect = int(args[args.index("--expect-rank") + 1]) if "--expect-rank" in args else None
    try:
        d = json.load(open(path))
        n1, n2, n3 = d["n"]
        U, V, W = rows(d, "u", n1 * n2), rows(d, "v", n2 * n3), rows(d, "w", n3 * n1)
        if not (len(U) == len(V) == len(W)):
            raise ValueError("u, v, w have different numbers of rows")
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL could not read the scheme: {exc}")
        return 1
    terms = [(u, v, w) for u, v, w in zip(U, V, W) if u and v and w]
    rank = len(terms)
    den, S = 1, 0
    for u, v, w in terms:
        for f in (u, v, w):
            for x in f.values():
                den = den * x.denominator // gcd(den, x.denominator)
        S += max(abs(x) for x in u.values()) * max(abs(x) for x in v.values()) * max(abs(x) for x in w.values())
    bound = 2 * den ** 3 * (S + 1)
    target = {(i * n2 + j, j * n3 + l, l * n1 + i) for i in range(n1) for j in range(n2) for l in range(n3)}
    primes, prod, q = [], 1, (1 << 61) - 1
    while prod <= bound:
        if is_prime(q):
            primes.append(q)
            prod *= q
        q -= 2
    for p in primes:
        def m(x):
            return x.numerator % p * pow(x.denominator % p, -1, p) % p
        acc = {}
        for u, v, w in terms:
            um = [(a, m(x)) for a, x in u.items()]
            vm = [(b, m(x)) for b, x in v.items()]
            wm = [(c, m(x)) for c, x in w.items()]
            for a, xa in um:
                for b, xb in vm:
                    ab = xa * xb % p
                    for c, xc in wm:
                        key = (a, b, c)
                        acc[key] = (acc.get(key, 0) + ab * xc) % p
        bad = 0
        for key in target:
            if acc.pop(key, 0) != 1 % p:
                bad += 1
        bad += sum(1 for val in acc.values() if val)
        if bad:
            print(f"FAIL {bad} Brent equations violated modulo p = {p}")
            return 1
    print(f"Brent equations hold modulo {len(primes)} primes whose product exceeds 2 * D^3 * (S + 1) "
          f"(D = {den}, S = {S}); hence exactly over Q")
    if expect is not None and rank != expect:
        print(f"FAIL rank {rank} != expected {expect}")
        return 1
    print(f"PASS format={n1}x{n2}x{n3} rank={rank} max_den={den}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
