#!/usr/bin/env python3
"""
k5sat.py -- exact SAT for the q=3 'A-design' chart of a 5-regular W3 controller (Delta = 15, N = 27 n):
choose a perfect matching M (the off-ports) AND, on every M-edge {a,b}, the bijection between N(a)-b and N(b)-a that
marks its 4 singular turns (every bijection is realisable: PGL(2,3) = S4 on the 4 planes through the off direction),
such that every non-adjacent ordered pair (u,v), u = v included, keeps a NB 3-walk u-a-b-v whose middle edge is not in
M or whose turn (u,v) is not marked. H-edges (line ports, vectors (3,1,0,0)) have no singular turn and complete pencils;
M-edges have complete pencils. If SAT: transports are realised (TransportFinder with the wanted bad set), the lift is
built and checked by exact all-pairs bitset BFS.
Usage: k5sat.py controller.json --out prefix
"""
import argparse, json, os, sys, time, itertools
import numpy as np
import networkx as nx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcl3 import GF, build_lift_edges, bitset_bad_pairs
from typed_chart import TransportFinder
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

LINE = [(1, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0)]
OFF = (0, 0, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('controller')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    rec = json.load(open(a.controller))
    n = rec['n']
    E = sorted(set((min(x, y), max(x, y)) for x, y in rec['edges']))
    G = nx.Graph(E)
    nbrs = [sorted(G[v]) for v in range(n)]
    assert all(len(x) == 5 for x in nbrs)
    eidx = {e: i for i, e in enumerate(E)}
    t0 = time.time()
    top = 0
    X = {}
    for e in range(len(E)):
        top += 1; X[e] = top
    Y = {}
    for e, (p, r) in enumerate(E):
        for x in nbrs[p]:
            if x == r:
                continue
            for y in nbrs[r]:
                if y == p:
                    continue
                top += 1; Y[(e, x, y)] = top
    cls = []
    # perfect matching
    for v in range(n):
        lits = [X[eidx[(min(v, w), max(v, w))]] for w in nbrs[v]]
        enc = CardEnc.equals(lits=lits, bound=1, top_id=top, encoding=EncType.pairwise)
        cls.extend(enc.clauses)
    # bijection iff x_e
    for e, (p, r) in enumerate(E):
        Np = [x for x in nbrs[p] if x != r]; Nr = [y for y in nbrs[r] if y != p]
        for x in Np:
            row = [Y[(e, x, y)] for y in Nr]
            for l in row:
                cls.append([-l, X[e]])            # y -> x
            cls.append([-X[e]] + row)             # x -> at least one in the row
            for l1, l2 in itertools.combinations(row, 2):
                cls.append([-l1, -l2])
        for y in Nr:
            col = [Y[(e, x, y)] for x in Np]
            cls.append([-X[e]] + col)
            for l1, l2 in itertools.combinations(col, 2):
                cls.append([-l1, -l2])
    # pair clauses
    adjset = [set(x) for x in nbrs]
    npairs = 0
    for u in range(n):
        for v in range(n):
            if v in adjset[u]:
                continue
            lits = []
            for a1 in nbrs[u]:
                for b1 in nbrs[a1]:
                    if b1 == u or v not in adjset[b1] or v == a1:
                        continue
                    if a1 < b1:
                        lits.append(-Y[(eidx[(a1, b1)], u, v)])
                    else:
                        lits.append(-Y[(eidx[(b1, a1)], v, u)])
            assert lits, 'controller is not W3'
            cls.append(sorted(set(lits)))
            npairs += 1
    print(f'n={n}: {top} variables, {len(cls)} clauses ({npairs} pair clauses) ({time.time()-t0:.1f}s)', flush=True)
    with Cadical153(bootstrap_with=cls) as S:
        sat = S.solve()
        model = set(l for l in S.get_model() if l > 0) if sat else None
    print(f'SAT: {sat} ({time.time()-t0:.1f}s)', flush=True)
    if not sat:
        if a.out:
            json.dump({'sat': False, 'n': n}, open(a.out + '.k5sat.json', 'w'))
        return
    M = [E[e] for e in range(len(E)) if X[e] in model]
    mate = {}
    for p, r in M:
        mate[p] = r; mate[r] = p
    F = GF(3); TF = TransportFinder(F)
    d = {}
    for v in range(n):
        hs = [x for x in nbrs[v] if x != mate[v]]
        for i, x in enumerate(hs):
            d[(v, x)] = LINE[i]
        d[(v, mate[v])] = OFF
    T = {}
    for e, (p, r) in enumerate(E):
        Dp = tuple(d[(p, x)] for x in nbrs[p] if x != r)
        Dr = tuple(d[(r, y)] for y in nbrs[r] if y != p)
        if X[e] in model:
            Np = [x for x in nbrs[p] if x != r]; Nr = [y for y in nbrs[r] if y != p]
            want = tuple(sorted((i, j) for i, x in enumerate(Np) for j, y in enumerate(Nr) if Y[(e, x, y)] in model))
            res = TF.find(d[(p, r)], Dp, d[(r, p)], Dr, want_bad=want)
            assert res is not None and res[2], 'wanted bijection not realisable'
            T[(p, r)] = res[0]
        else:
            res = TF.find(d[(p, r)], Dp, d[(r, p)], Dr)
            assert res[1] == () and res[2], 'H-edge without zero-bad complete transport'
            T[(p, r)] = res[0]
    edges = build_lift_edges(F, n, E, d, T)
    bad, dmax, dmin = bitset_bad_pairs(27 * n, edges, 3)
    print(f'lift: N={27*n}, edges={len(edges)}, degree {dmin}..{dmax}, ordered pairs at distance > 3: {bad} '
          f'({time.time()-t0:.1f}s)', flush=True)
    if a.out:
        json.dump({'sat': True, 'n': n, 'q': 3, 'E': [list(e) for e in E], 'M': [list(e) for e in M],
                   'd': {f'{u},{v}': list(x) for (u, v), x in d.items()},
                   'T': {f'{u},{v}': [list(r) for r in T[(u, v)]] for (u, v) in E}, 'lift_bad_pairs': bad,
                   'controller_source': os.path.basename(a.controller)}, open(a.out + '.k5sat.json', 'w'))
        if bad == 0:
            with open(a.out + '.edges.txt', 'w') as f:
                for i, j in edges:
                    f.write(f'{i} {j}\n')
            print('SUCCESS', flush=True)


if __name__ == '__main__':
    main()
