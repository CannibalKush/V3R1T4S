#!/usr/bin/env python3
"""check_code.py OBJECT.json [--expect-d D]
Standalone checker for a binary linear code given by a generator matrix, written from the definition.

Definition (codetables.de): an [n, k, d]_2 code is a k-dimensional subspace of GF(2)^n; d is the smallest Hamming
weight of a nonzero codeword. The object is JSON with key "G": a list of k rows, each a list of n entries in {0, 1}.

Checks: every entry is 0 or 1; all rows have length n; the rank over GF(2) is exactly k; the exact minimum distance
is computed twice by full enumeration of all 2^k - 1 nonzero codewords (a Gray-code walk, and a direct walk over
messages in binary order), and the two must agree. Standard library only. Last line: "PASS ..." or "FAIL ...".
"""
import json
import sys


def main():
    args = sys.argv[1:]
    path = args[0]
    expect = int(args[args.index("--expect-d") + 1]) if "--expect-d" in args else None
    try:
        data = json.load(open(path))
        G = data["G"]
        k, n = len(G), len(G[0])
        assert k > 0 and all(len(r) == n for r in G), "ragged generator matrix"
        assert all(x in (0, 1) for r in G for x in r), "entry outside {0,1}"
    except Exception as exc:  # noqa: BLE001 - any parse failure is a FAIL
        print(f"FAIL could not read a 0/1 generator matrix: {exc}")
        return 1
    rows = [int("".join(map(str, r)), 2) for r in G]
    basis = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r)
    rank = len(basis)
    if rank != k:
        print(f"FAIL rank over GF(2) is {rank}, not k = {k}")
        return 1
    # method 1: Gray-code walk
    d1, a1, cw = n + 1, 0, 0
    for i in range(1, 1 << k):
        cw ^= rows[(i & -i).bit_length() - 1]
        w = bin(cw).count("1")
        if w < d1:
            d1, a1 = w, 1
        elif w == d1:
            a1 += 1
    # method 2: direct enumeration of messages m = 1 .. 2^k - 1
    d2, a2 = n + 1, 0
    for m in range(1, 1 << k):
        c, j, mm = 0, 0, m
        while mm:
            if mm & 1:
                c ^= rows[j]
            mm >>= 1
            j += 1
        w = bin(c).count("1")
        if w < d2:
            d2, a2 = w, 1
        elif w == d2:
            a2 += 1
    print(f"gray-code walk: d={d1} A_d={a1}; direct enumeration: d={d2} A_d={a2}")
    if (d1, a1) != (d2, a2):
        print("FAIL the two enumerations disagree")
        return 1
    if expect is not None and d1 != expect:
        print(f"FAIL minimum distance {d1} != expected {expect}")
        return 1
    print(f"PASS code=[{n},{k},{d1}]_2 rank={rank} A_d={a1} codewords_enumerated={(1 << k) - 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
