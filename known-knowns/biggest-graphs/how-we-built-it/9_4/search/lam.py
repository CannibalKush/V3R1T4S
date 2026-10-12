"""lam.py: build Lambda(B, alpha, S) = K_2-fibre lift of a GQ incidence graph with the point fibres deleted,
plus twins of the line copies over a spread S, plus twin fibres.  Generic: takes the line list, the Z_2 voltage of
every incidence and the spread from an .npz produced by symsearch.py (keys lines, ends, alpha, spread, P).

Vertex labels: (p,i) -> 2p+i (points p < P), (line l, i) -> 2(P+l)+i, twin z_(S[s],c) -> 4P + 2s + c.
Max degree q+2, order 4P + 2|S| = 4(q+1)(q^2+1) + 2(q^2+1).

usage: python lam.py IN.npz OUT.edges [--nofibre-twins]
"""
import argparse
import numpy as np


def build(lines, ends, alpha, spread, P, twinfibre=True):
    A = {}
    for e in range(len(ends)):
        p, Lv = int(ends[e, 0]), int(ends[e, 1])
        A[(p, Lv - P)] = int(alpha[e]) % 2
    E = []
    for (p, l), a in A.items():
        for i in range(2):
            E.append((2 * p + i, 2 * (P + l) + (i + a) % 2))
    for l in range(P):
        E.append((2 * (P + l), 2 * (P + l) + 1))
    base = 4 * P
    for s, l in enumerate(spread):
        l = int(l)
        for c in range(2):
            z = base + 2 * s + c
            for p in lines[l]:
                E.append((z, 2 * int(p) + (c - A[(int(p), l)]) % 2))
        if twinfibre:
            E.append((base + 2 * s, base + 2 * s + 1))
    E = np.array(E, np.int64)
    E.sort(axis=1)
    E = E[np.lexsort((E[:, 1], E[:, 0]))]
    return E


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('npz', help='voltage file written by symsearch.py')
    ap.add_argument('out', help='output edge list')
    ap.add_argument('--nofibre-twins', action='store_true')
    a = ap.parse_args()
    z = np.load(a.npz)
    E = build(z['lines'], z['ends'], z['alpha'], z['spread'], int(z['P']), not a.nofibre_twins)
    with open(a.out, 'w') as f:
        for u, v in E:
            f.write('%d %d\n' % (u, v))
    print('N', int(E.max()) + 1, 'edges', len(E), '->', a.out)
