#!/usr/bin/env python3
"""check_maxdet.py OBJECT.txt [--expect-norm VALUE]
Standalone checker for the determinant of a {+1,-1} matrix, written from the definition.

The object is a text file with n lines of n integers, each +1 or -1. The determinant of such a matrix is divisible
by 2^(n-1), so the checker reports the integer |det| / 2^(n-1) ("normalized determinant").

Checks: the matrix is square with entries +-1; |det| exactly by fraction-free Bareiss elimination on Python integers;
a second, independent exact value from determinants modulo distinct primes combined by the Chinese remainder theorem,
with enough primes that their product exceeds twice the Hadamard bound n^(n/2) (so the CRT value is exact); and, if
sympy is installed, a third cross-check with sympy's Bareiss. For n = 1 mod 4 it also prints the ratio to the Barba
bound sqrt(2n - 1) (n - 1)^((n-1)/2) and fails if that bound is exceeded. Standard library only (sympy optional).
Last line: "PASS ..." or "FAIL ...".
"""
import sys
from fractions import Fraction


def bareiss(m):
    a = [row[:] for row in m]
    n = len(a)
    sign, prev = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            for i in range(k + 1, n):
                if a[i][k]:
                    a[k], a[i] = a[i], a[k]
                    sign = -sign
                    break
            else:
                return 0
        akk = a[k][k]
        for i in range(k + 1, n):
            aik = a[i][k]
            ri, rk = a[i], a[k]
            for j in range(k + 1, n):
                ri[j] = (ri[j] * akk - aik * rk[j]) // prev
        prev = akk
    return sign * a[n - 1][n - 1]


def det_mod(m, p):
    a = [[x % p for x in row] for row in m]
    n = len(a)
    det = 1
    for c in range(n):
        piv = next((r for r in range(c, n) if a[r][c]), None)
        if piv is None:
            return 0
        if piv != c:
            a[c], a[piv] = a[piv], a[c]
            det = -det
        det = det * a[c][c] % p
        inv = pow(a[c][c], p - 2, p)
        for r in range(c + 1, n):
            f = a[r][c] * inv % p
            if f:
                ar, ac = a[r], a[c]
                for j in range(c, n):
                    ar[j] = (ar[j] - f * ac[j]) % p
    return det % p


def is_prime(q):
    if q < 2:
        return False
    i = 2
    while i * i <= q:
        if q % i == 0:
            return False
        i += 1
    return True


def main():
    args = sys.argv[1:]
    path = args[0]
    expect = int(args[args.index("--expect-norm") + 1]) if "--expect-norm" in args else None
    try:
        rows = [list(map(int, line.split())) for line in open(path).read().split("\n") if line.strip()]
        n = len(rows)
        assert n > 1 and all(len(r) == n for r in rows), "not a square matrix"
        assert all(x in (1, -1) for r in rows for x in r), "entry other than +1 or -1"
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL could not read a square +-1 matrix: {exc}")
        return 1
    d1 = abs(bareiss(rows))
    # CRT over primes just below 2^31 until the product exceeds 2 * n^(n/2)
    bound2 = 4 * n ** n  # (2 * n^(n/2))^2
    primes, prod, q = [], 1, (1 << 31) - 1
    while prod * prod <= bound2:
        if is_prime(q):
            primes.append(q)
            prod *= q
        q -= 2
    res, mod = 0, 1
    for p in primes:
        r = det_mod(rows, p)
        res = res + mod * ((r - res) * pow(mod, -1, p) % p)
        mod *= p
    if res > mod // 2:
        res -= mod
    d2 = abs(res)
    print(f"n={n} bareiss |det| and CRT |det| ({len(primes)} primes) {'agree' if d1 == d2 else 'DISAGREE'}")
    if d1 != d2:
        print("FAIL the two exact determinant methods disagree")
        return 1
    try:
        import sympy  # optional third method
        d3 = abs(int(sympy.Matrix(rows).det(method="bareiss")))
        print(f"sympy bareiss cross-check {'agrees' if d3 == d1 else 'DISAGREES'}")
        if d3 != d1:
            print("FAIL sympy disagrees")
            return 1
    except ImportError:
        print("sympy not installed: two exact methods used")
    if d1 % (1 << (n - 1)):
        print("FAIL |det| is not divisible by 2^(n-1)")
        return 1
    norm = d1 >> (n - 1)
    print(f"|det| / 2^{n - 1} = {norm}")
    if n % 4 == 1:
        barba_sq = Fraction((2 * n - 1) * (n - 1) ** (n - 1), 4 ** (n - 1))
        ratio_sq = Fraction(norm * norm) / barba_sq
        print(f"ratio to the Barba bound = {float(ratio_sq) ** 0.5:.6f}")
        if ratio_sq > 1:
            print("FAIL exceeds the Barba bound")
            return 1
    if expect is not None and norm != expect:
        print(f"FAIL normalized determinant {norm} != expected {expect}")
        return 1
    print(f"PASS n={n} norm_det={norm}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
