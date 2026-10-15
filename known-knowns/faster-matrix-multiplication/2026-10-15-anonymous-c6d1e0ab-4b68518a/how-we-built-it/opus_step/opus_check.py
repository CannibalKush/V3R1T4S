#!/usr/bin/env python3
"""opus_check.py: standalone exact checker for matrix multiplication schemes (opus-fmm), standard library only.

Definition checked (the sparse JSON convention of data/sa.py): a scheme for <n1,n2,n3> is a list of terms (U,V,W);
term t computes (sum_a U[a] A_a) * (sum_b V[b] B_b) and adds W[c] times it to C, with a = i*n2+j (A is n1 x n2),
b = j*n3+l (B is n2 x n3), c = l*n1+i (C_il).  The scheme multiplies matrices iff for all a, b, c
    sum_t U_t[a] V_t[b] W_t[c] = 1 if (a, b, c) = (i*n2+j, j*n3+l, l*n1+i) for some i, j, l, and 0 otherwise.
Method: exact.  Every coefficient is parsed as a Fraction; the whole identity is multiplied by the common
denominator D (lcm over terms of the product of the three per-factor denominators), so every summand is an exact
Python integer.  The identity is then checked for every output index c separately, with no sampling, no
modular arithmetic and no floating point.  Usage: python3 opus_check.py scheme.json [--expect-rank R]
"""
import json
import sys
from fractions import Fraction
from math import lcm


def parse(row, length, enc):
    if enc == 'sparse_flat_pairs':
        out = {}
        for k in range(0, len(row), 2):
            v = Fraction(row[k + 1]) if not isinstance(row[k + 1], int) else Fraction(row[k + 1])
            if v:
                out[int(row[k])] = out.get(int(row[k]), Fraction(0)) + v
        return {a: v for a, v in out.items() if v}
    assert len(row) == length
    return {a: Fraction(v) for a, v in enumerate(row) if Fraction(v) != 0}


def main():
    path = sys.argv[1]
    expect = None
    if '--expect-rank' in sys.argv:
        expect = int(sys.argv[sys.argv.index('--expect-rank') + 1])
    d = json.load(open(path))
    n1, n2, n3 = map(int, d['n'])
    enc = d.get('encoding', 'dense')
    terms = []
    for u, v, w in zip(d['u'], d['v'], d['w']):
        U, V, W = parse(u, n1 * n2, enc), parse(v, n2 * n3, enc), parse(w, n3 * n1, enc)
        if U and V and W:
            terms.append((U, V, W))
    rank = len(terms)
    # integer form: factor * its own denominator lcm; term scale = 1/(dU dV dW)
    ints = []
    D = 1
    for U, V, W in terms:
        ds = [1, 1, 1]
        for k, F in enumerate((U, V, W)):
            for x in F.values():
                ds[k] = lcm(ds[k], x.denominator)
        prod = ds[0] * ds[1] * ds[2]
        D = lcm(D, prod)
        ints.append((prod, {a: int(x * ds[0]) for a, x in U.items()}, {b: int(x * ds[1]) for b, x in V.items()},
                     {c: int(x * ds[2]) for c, x in W.items()}))
    # group terms by output index c
    by_c = {}
    for t, (prod, Ui, Vi, Wi) in enumerate(ints):
        for c, wc in Wi.items():
            by_c.setdefault(c, []).append((t, wc))
    bad = 0
    products = 0
    for c in range(n3 * n1):
        l, i = divmod(c, n1)
        acc = {}
        for t, wc in by_c.get(c, []):
            prod, Ui, Vi, _ = ints[t]
            scale = (D // prod) * wc
            for a, ua in Ui.items():
                s = scale * ua
                base = a * (n2 * n3)
                for b, vb in Vi.items():
                    key = base + b
                    acc[key] = acc.get(key, 0) + s * vb
                    products += 1
        # target: D at (a, b) = (i*n2+j, j*n3+l) for every j
        for j in range(n2):
            key = (i * n2 + j) * (n2 * n3) + (j * n3 + l)
            if acc.pop(key, 0) != D:
                bad += 1
        bad += sum(1 for x in acc.values() if x != 0)
    ok = bad == 0 and (expect is None or expect == rank)
    print(f'opus_check: format={n1}x{n2}x{n3} rank={rank} expect={expect} common_denominator_bits={D.bit_length()} '
          f'products={products} wrong_coefficients={bad}')
    print('PASS (exact integer arithmetic over every coefficient)' if ok else 'FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
