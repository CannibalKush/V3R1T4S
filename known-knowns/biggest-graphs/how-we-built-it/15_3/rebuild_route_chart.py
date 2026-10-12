#!/usr/bin/env python3
"""
Standalone rebuild (pure Python, no numpy) of a route-chart lift over F_q^3, q PRIME, from a params JSON.
Vertex (u, x), x = (x0,x1,x2) in F_q^3, has index u*q^3 + x0*q^2 + x1*q + x2.
For every controller edge [a,b] in E (a<b), every x and every lam in F_q:
      (a, x) ~ (b, T[a,b] x + lam * w[a,b])           (arithmetic mod q)
The controller edge list is also cross-checked against the controller adjacency file (one line per vertex, 4 nbrs).
Usage: rebuild_route_chart.py params.json out_edges.txt [controller.adj]
"""
import itertools, json, sys

P = json.load(open(sys.argv[1]))
q, n = int(P['q']), int(P['n'])
assert q in (2, 3, 5, 7), 'this rebuild script handles prime q only'
m = q ** 3
E = [tuple(e) for e in P['E']]
if len(sys.argv) > 3:
    rows = [list(map(int, l.split())) for l in open(sys.argv[3]) if l.strip()]
    E2 = sorted(set((min(u, v), max(u, v)) for u, r in enumerate(rows) for v in r))
    assert sorted(E) == E2, 'controller edge set in params differs from the controller file'
    print('controller file matches params: n=%d, %d edges' % (len(rows), len(E2)))
pts = list(itertools.product(range(q), repeat=3))
code = lambda x: x[0] * q * q + x[1] * q + x[2]


def mv(A, x):
    return tuple(sum(A[i][j] * x[j] for j in range(3)) % q for i in range(3))


def det3(A):
    a = A
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])) % q


edges = set()
for (a, b) in E:
    key = f'{a},{b}'
    T = P['T'][key]
    w = tuple(x % q for x in P['w'][key])
    assert det3(T) != 0, 'T not invertible'
    assert any(w), 'w = 0'
    assert tuple(mv(T, P['d'][key])) == w, 'w != T d'
    for x in pts:
        y0 = mv(T, x)
        for lam in range(q):
            y = tuple((y0[i] + lam * w[i]) % q for i in range(3))
            i1, i2 = a * m + code(x), b * m + code(y)
            assert i1 != i2
            edges.add((min(i1, i2), max(i1, i2)))
with open(sys.argv[2], 'w') as f:
    for i1, i2 in sorted(edges):
        f.write(f'{i1} {i2}\n')
print(f'wrote {len(edges)} edges on {n * m} vertices to {sys.argv[2]}')
