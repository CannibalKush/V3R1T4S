#!/usr/bin/env python3
"""rebuild_lift.py PARAMS.json OUT.edges.txt -- rebuild the frame-lift edge list from its parameters (numpy only).
Vertex (u,p) has id 81*u + code(p), code(p) = 27 p0 + 9 p1 + 3 p2 + p3 for p in F_3^4.
Edges: (u,p) ~ (w, A p + c + lam*b) for every arc u->w and lam in F_3;  (u,p) ~ (u, p + t_u)."""
import itertools, json, sys
import numpy as np
P = json.load(open(sys.argv[1]))
ALL = np.array(list(itertools.product(range(3), repeat=4)), dtype=np.int64)
POW = np.array([27, 9, 3, 1])
m = 81
E = []
for (u, w), A, b, c in zip(P['arcs'], P['A'], P['b'], P['c']):
    A, b, c = np.array(A), np.array(b), np.array(c)
    img = (ALL @ A.T + c) % 3
    for lam in range(3):
        E.append(np.stack([u * m + np.arange(m), w * m + ((img + lam * b) % 3) @ POW], axis=1))
for u in range(P['n']):
    E.append(np.stack([u * m + np.arange(m), u * m + ((ALL + np.array(P['t'][u])) % 3) @ POW], axis=1))
E = np.unique(np.sort(np.concatenate(E), axis=1), axis=0)
np.savetxt(sys.argv[2], E, fmt='%d')
print('wrote', sys.argv[2], len(E), 'edges')
