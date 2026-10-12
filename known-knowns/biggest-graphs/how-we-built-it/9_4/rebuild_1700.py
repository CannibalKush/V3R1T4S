"""rebuild_1700.py: standalone rebuild of the (9,4) graph on 1700 vertices (pure Python 3, no numpy).
Reads W7_points.txt (coordinates over GF(7) + Gram matrix J of the symplectic form), W7_lines.txt,
voltage_q7_Z2.txt, spread_q7.txt.  Re-verifies: J alternating and non-degenerate; points distinct projective
points; every line = 8 pairwise orthogonal points spanning a 2-space; every point on 8 lines; two lines share
<= 1 point; spread lines partition the points; voltage invariant under k -> k+48 (mod 400) on points.
Writes G_9_4_n1700.rebuilt.edges and prints its sha256 (must equal that of G_9_4_n1700.edges).
Vertex labels: (p,i) -> 2p+i, (line l, i) -> 2(400+l)+i, twin of (S[s],c) -> 1600+2s+c.
"""
import hashlib
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
p_ = 7


def rows(fn):
    with open(os.path.join(HERE, fn)) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            yield [int(x) for x in line.split()]


hdr = open(os.path.join(HERE, 'W7_points.txt')).read().split('\n')[1]
J = [[int(v) for v in r] for r in re.findall(r'\[([0-9, ]+)\]', hdr.split('J =')[1])[0:4] for r in [r.split(',')]]
assert len(J) == 4 and all(len(r) == 4 for r in J)
for i in range(4):
    assert J[i][i] % p_ == 0
    for j in range(4):
        assert (J[i][j] + J[j][i]) % p_ == 0


def det4(M):
    M = [r[:] for r in M]
    d = 1
    for c in range(4):
        piv = next((r for r in range(c, 4) if M[r][c] % p_), None)
        if piv is None:
            return 0
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            d = -d
        d = d * M[c][c] % p_
        inv = pow(M[c][c], p_ - 2, p_)
        for r in range(c + 1, 4):
            f = M[r][c] * inv % p_
            for k in range(4):
                M[r][k] = (M[r][k] - f * M[c][k]) % p_
    return d % p_


assert det4(J) != 0, 'degenerate form'


def B(x, y):
    return sum(x[i] * J[i][j] * y[j] for i in range(4) for j in range(4)) % p_


def norm(v):
    for c in v:
        if c % p_:
            ic = pow(c, p_ - 2, p_)
            return tuple(x * ic % p_ for x in v)


pts = {r[0]: r[1:] for r in rows('W7_points.txt')}
assert len(pts) == 400 and len({norm(v) for v in pts.values()}) == 400
lines = {r[0]: r[1:] for r in rows('W7_lines.txt')}
assert len(lines) == 400
on = {k: 0 for k in pts}
pairs = set()
for l, L in lines.items():
    assert len(L) == 8 and len(set(L)) == 8
    for a in range(8):
        on[L[a]] += 1
        for b in range(a + 1, 8):
            assert B(pts[L[a]], pts[L[b]]) == 0
            key = (min(L[a], L[b]), max(L[a], L[b]))
            assert key not in pairs
            pairs.add(key)
    # the 8 points lie in the span of the first two (a projective line has exactly q+1 = 8 points)
    x, y = pts[L[0]], pts[L[1]]
    span = {norm(tuple((a * x[i] + b * y[i]) % p_ for i in range(4))) for a in range(p_) for b in range(p_) if (a, b) != (0, 0)}
    assert {norm(tuple(pts[t])) for t in L} == span
assert all(v == 8 for v in on.values())
alpha = {}
for pt, l, a in rows('voltage_q7_Z2.txt'):
    assert pt in lines[l]
    alpha[(pt, l)] = a % 2
assert len(alpha) == 3200
spread = next(rows('spread_q7.txt'))
cov = {}
for l in spread:
    for pt in lines[l]:
        cov[pt] = cov.get(pt, 0) + 1
assert len(spread) == 50 and len(cov) == 400 and all(v == 1 for v in cov.values())
P = 400
E = []
for (pt, l), a in alpha.items():
    for i in range(2):
        E.append((2 * pt + i, 2 * (P + l) + (i + a) % 2))
for l in range(P):
    E.append((2 * (P + l), 2 * (P + l) + 1))
base = 4 * P
for s, l in enumerate(spread):
    for c in range(2):
        z = base + 2 * s + c
        for pt in lines[l]:
            E.append((z, 2 * pt + (c - alpha[(pt, l)]) % 2))
    E.append((base + 2 * s, base + 2 * s + 1))
E = sorted(tuple(sorted(e)) for e in E)
out = os.path.join(HERE, 'G_9_4_n1700.rebuilt.edges')
with open(out, 'w') as f:
    for u, v in E:
        f.write('%d %d\n' % (u, v))
print('geometry OK; N =', base + 2 * len(spread), 'edges =', len(E))
print('sha256', hashlib.sha256(open(out, 'rb').read()).hexdigest())
