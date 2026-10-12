#!/usr/bin/env python3
"""
Algebraic certificate for diameter <= 3 of a route-chart lift over F_q^3 (q prime), independent of BFS.
Lift: (a,x) ~ (b, T_ab x + lam*w_ab) for stored edges a<b; reverse direction T_ba = T_ab^{-1}, w_ba = T_ab^{-1} w_ab.
Theorem 2 (route-chart diameter criterion): diam <= 3 if
 (R) every ordered pair (u,v) of controller vertices with v = u or v not adjacent to u has a walk u-a-b-v with
     rank[ T_bv T_ab w_ua , T_bv w_ab , w_bv ] = 3;
 (P) every ordered adjacent pair (a,b): the planes  T_ab span(w_xa, w_ba)  (x in N(a)-b)  and  span(w_ab, w_yb)
     (y in N(b)-a) are genuine planes and include all q+1 planes of F_q^3 containing the line <w_ab>.
This script recomputes everything from T and w only (directions d are NOT used).
Usage: check_route_certificate.py params.json controller.adj
"""
import itertools, json, sys
from collections import deque

P = json.load(open(sys.argv[1]))
q, n = int(P['q']), int(P['n'])
rows = [list(map(int, l.split())) for l in open(sys.argv[2]) if l.strip()]
k = len(rows[0])
assert len(rows) == n and all(len(set(r)) == len(r) == k for r in rows)
E = sorted(set((min(u, v), max(u, v)) for u, r in enumerate(rows) for v in r))
assert E == sorted(tuple(e) for e in P['E']), 'controller mismatch'
nb = [sorted(r) for r in rows]
assert all(u not in nb[u] for u in range(n)) and all(u in nb[v] for u in range(n) for v in nb[u])


def mv(A, x):
    return tuple(sum(A[i][j] * x[j] for j in range(3)) % q for i in range(3))


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) % q for j in range(3)] for i in range(3)]


def rank(vs):
    M = [list(v) for v in vs]
    r = 0
    for c in range(3):
        piv = next((i for i in range(r, len(M)) if M[i][c] % q), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        iv = pow(M[r][c], q - 2, q)
        M[r] = [(x * iv) % q for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % q:
                f = M[i][c]
                M[i] = [(x - f * y) % q for x, y in zip(M[i], M[r])]
        r += 1
    return r


def inv3(A):
    M = [list(A[i]) + [int(i == j) for j in range(3)] for i in range(3)]
    for c in range(3):
        piv = next(i for i in range(c, 3) if M[i][c] % q)
        M[c], M[piv] = M[piv], M[c]
        iv = pow(M[c][c], q - 2, q)
        M[c] = [(x * iv) % q for x in M[c]]
        for i in range(3):
            if i != c and M[i][c] % q:
                f = M[i][c]
                M[i] = [(x - f * y) % q for x, y in zip(M[i], M[c])]
    return [r[3:] for r in M]


def span(vs):
    return frozenset(tuple(sum(c * v[i] for c, v in zip(co, vs)) % q for i in range(3))
                     for co in itertools.product(range(q), repeat=len(vs)))


Tm, Wv = {}, {}
for (a, b) in E:
    T = [[x % q for x in r] for r in P['T'][f'{a},{b}']]
    w = tuple(x % q for x in P['w'][f'{a},{b}'])
    assert rank([tuple(T[i][j] for i in range(3)) for j in range(3)]) == 3 and any(w)
    Ti = inv3(T)
    assert mm(T, Ti) == [[int(i == j) for j in range(3)] for i in range(3)]
    Tm[(a, b)], Wv[(a, b)] = T, w
    Tm[(b, a)], Wv[(b, a)] = Ti, mv(Ti, w)
# (C0) controller BFS diameter
ecc = 0
for s in range(n):
    dist = [-1] * n; dist[s] = 0; dq = deque([s])
    while dq:
        x = dq.popleft()
        for y in nb[x]:
            if dist[y] < 0:
                dist[y] = dist[x] + 1; dq.append(y)
    assert min(dist) >= 0
    ecc = max(ecc, max(dist))
print(f'(C0) controller: n={n}, {k}-regular, simple, diameter {ecc}')
# (R)
nR = 0
for u in range(n):
    for v in range(n):
        if v in nb[u]:
            continue
        ok = False
        for a in nb[u]:
            for b in nb[a]:
                if b == u or v not in nb[b] or v == a:
                    continue
                M = [mv(Tm[(b, v)], mv(Tm[(a, b)], Wv[(u, a)])), mv(Tm[(b, v)], Wv[(a, b)]), Wv[(b, v)]]
                if rank(M) == 3:
                    ok = True; break
            if ok:
                break
        assert ok, f'(R) fails for pair {(u, v)}'
        nR += 1
print(f'(R) ok: all {nR} non-adjacent ordered pairs (incl. u=u) have a rank-3 walk of length 3')
# (P)
lines_planes = {}
nP = 0
for a in range(n):
    for b in nb[a]:
        L = Wv[(a, b)]
        planes = set()
        for x in nb[a]:
            if x == b:
                continue
            vs = [mv(Tm[(a, b)], Wv[(x, a)]), L]
            assert rank(vs) == 2
            planes.add(span(vs))
        for y in nb[b]:
            if y == a:
                continue
            vs = [L, Wv[(y, b)]]
            assert rank(vs) == 2
            planes.add(span(vs))
        pencil = set()
        for z in itertools.product(range(q), repeat=3):
            if rank([L, z]) == 2:
                pencil.add(span([L, z]))
        assert len(pencil) == q + 1
        assert pencil <= planes, f'(P) fails for adjacent pair {(a, b)}: {len(pencil & planes)} of {q+1} planes'
        nP += 1
print(f'(P) ok: all {nP} adjacent ordered pairs have a complete pencil of q+1 = {q+1} planes')
print(f'CERTIFICATE VALID: by Theorem 2 the lift (order {n * q**3}, {k*q}-regular) has diameter <= 3')
