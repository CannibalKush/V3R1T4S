#!/usr/bin/env python3
"""Rebuild the [213, 26, 77] generator matrix from its polynomial description (Python standard library only).

Usage: python3 rebuild.py [OBJECT.json]
Prints the rebuilt matrix's sha256 over its rows and, if OBJECT.json is given, whether its "G" equals the rebuilt one.

Construction (Construction X on an index-2 quasi-cyclic code). Polynomials over GF(2) are integers, bit j = the
coefficient of x^j.
- m = 105; h = (x+1)(x^3+x^2+1)(x^4+x^3+x^2+x+1)(x^6+x^4+x^2+x+1)(x^12+x^8+x^6+x^5+x^3+x^2+1), degree 26, a divisor
  of x^105 - 1 (checked); g = (x^105 - 1) / h, degree 79; f = 0x2d547; q = x^3 + x^2 + 1, one of the factors of h.
- For a message a(x) of degree < 26 the codeword is ( g*a mod (x^105-1) | g*((a*f) mod h) mod (x^105-1) | a mod q ):
  two circulant blocks of 105 columns (the quasi-cyclic code C1 = [210, 26, 76]) and three columns holding the
  residue a mod q. Rows of G are the messages a = x^i, i = 0..25, each block listed from x^0 upward.
- Why d >= 77 (the exact value is what the checkers compute): if q divides a, the word lies in the submodule subcode
  C2 = {a : q | a} = [210, 23, 77] and its tail is zero; otherwise the tail is nonzero and the C1 part has weight >= 76.
"""
import hashlib
import json
import sys

M = 105
FACTORS = [0x3, 0xD, 0x1F, 0x57, 0x116D]
F = 0x2D547
Q = 0xD


def mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def mod(a, b):
    db = b.bit_length() - 1
    while a and a.bit_length() - 1 >= db:
        a ^= b << (a.bit_length() - 1 - db)
    return a


def div(a, b):
    q, db = 0, b.bit_length() - 1
    while a and a.bit_length() - 1 >= db:
        s = a.bit_length() - 1 - db
        q ^= 1 << s
        a ^= b << s
    return q, a


def main():
    h = 1
    for fct in FACTORS:
        h = mul(h, fct)
    xm1 = (1 << M) | 1  # x^105 - 1 = x^105 + 1 over GF(2)
    g, rem = div(xm1, h)
    assert rem == 0, "h does not divide x^105 - 1"
    assert h.bit_length() - 1 == 26
    for fct in FACTORS:  # irreducibility: no polynomial of degree 1..deg/2 divides it
        dd = fct.bit_length() - 1
        for c in range(2, 1 << (dd // 2 + 1)):
            assert c == fct or mod(fct, c) != 0, hex(fct)
    rows = []
    for i in range(26):
        a = 1 << i
        b0 = mod(mul(g, a), xm1)
        b1 = mod(mul(g, mod(mul(a, F), h)), xm1)
        t = mod(a, Q)
        rows.append([(b0 >> j) & 1 for j in range(M)] + [(b1 >> j) & 1 for j in range(M)] + [(t >> j) & 1 for j in range(3)])
    digest = hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()
    print(f"h = {hex(h)} (degree 26) divides x^105 - 1; rebuilt a 26 x {len(rows[0])} matrix; sha256 of its rows (compact JSON) = {digest}")
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
