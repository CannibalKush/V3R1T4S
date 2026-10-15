#!/usr/bin/env python3
"""Rebuild the [175, 25, 61] generator matrix from its stated parameters (Python standard library only).

Usage: python3 rebuild.py [OBJECT.json]
Prints the rebuilt matrix's sha256 over its rows and, if OBJECT.json is given, whether its "G" equals the rebuilt one.

Construction (polynomials over GF(2), an integer's bit i is the coefficient of x^i):
- m = 85, h = 0x36a5431 = (x+1)(x^8+x^5+x^4+x^3+x^2+x+1)(x^8+x^6+x^5+x^4+x^2+x+1)(x^8+x^6+x^5+x^4+x^3+x+1), a divisor
  of x^85 - 1 of degree 25, and g = (x^85 - 1) / h.
- Row i (i = 0..24) is built from the message a = x^i: its first 85 entries are the coefficients of g*a mod (x^85 - 1),
  its next 85 the coefficients of g*(a*f mod h) mod (x^85 - 1) with f = 0xe600fc, both listed from x^0 to x^84.
- Five more columns, each a linear functional on messages: entry (i, j) is bit i of
  F = [0x1e80373, 0xa194c, 0x1fefae8, 0x19cf5ed, 0x16091f4][j].
"""
import hashlib
import json
import sys

M = 85
H = 0x36A5431
F = 0xE600FC
EXTRA = [0x1E80373, 0xA194C, 0x1FEFAE8, 0x19CF5ED, 0x16091F4]


def mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def mod(a, p):
    dp = p.bit_length() - 1
    while a and a.bit_length() - 1 >= dp:
        a ^= p << (a.bit_length() - 1 - dp)
    return a


def div_exact(a, p):
    q, dp = 0, p.bit_length() - 1
    while a and a.bit_length() - 1 >= dp:
        s = a.bit_length() - 1 - dp
        q |= 1 << s
        a ^= p << s
    assert a == 0, "h does not divide x^85 - 1"
    return q


def main():
    xm1 = (1 << M) | 1  # x^85 - 1 = x^85 + 1 over GF(2)
    assert H.bit_length() - 1 == 25
    g = div_exact(xm1, H)
    rows = []
    for i in range(25):
        a = 1 << i
        left = mod(mul(g, a), xm1)
        right = mod(mul(g, mod(mul(a, F), H)), xm1)
        row = [(left >> t) & 1 for t in range(M)] + [(right >> t) & 1 for t in range(M)]
        row += [(e >> i) & 1 for e in EXTRA]
        rows.append(row)
    digest = hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()
    print(f"rebuilt a 25 x {len(rows[0])} matrix; sha256 of its rows (compact JSON) = {digest}")
    if len(sys.argv) > 1:
        G = json.load(open(sys.argv[1]))["G"]
        if G == rows:
            print("IDENTICAL to the object's G")
            return 0
        print("DIFFERENT from the object's G")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
