"""gq.py: incidence graph of the symplectic generalized quadrangle W(q) (order (q,q)), q any prime power.

Points  = 1-subspaces of GF(q)^4 (normalised: first nonzero coordinate = 1), (q+1)(q^2+1) of them.
Lines   = totally isotropic 2-subspaces for B(x,y) = x0y1 - x1y0 + x2y3 - x3y2, (q+1)(q^2+1) of them.
Vertices 0..P-1 = points, P..2P-1 = lines.  adj[v] = the q+1 neighbours of v (sorted).
For q odd W(q) is the dual of Q(4,q), so the incidence graph is the same for both models; for q even W(q) = Q(4,q).

build(q) -> dict(q, P, adj (2P x (q+1) int32), pts (P x 4), lines (P x (q+1) point ids))
self-test: python gq.py q   (checks regularity, bipartite, girth 8, diameter 4, q+1 geodesics per opposite pair)
"""
import sys
import numpy as np
import galois


def field_tables(q):
    GF = galois.GF(q)
    a = GF(np.arange(q))
    add = np.array(a[:, None] + a[None, :], dtype=np.int64)
    mul = np.array(a[:, None] * a[None, :], dtype=np.int64)
    neg = np.array(-a, dtype=np.int64)
    inv = np.zeros(q, np.int64)
    inv[1:] = np.array(GF(np.arange(1, q)) ** -1, dtype=np.int64)
    return add, mul, neg, inv


def build(q):
    add, mul, neg, inv = field_tables(q)
    # all normalised points
    pts = []
    for lead in range(4):
        # first nonzero coordinate at position `lead`, equal to 1
        rest = 3 - lead
        for t in range(q ** rest):
            v = [0] * 4
            v[lead] = 1
            x = t
            for j in range(lead + 1, 4):
                v[j] = x % q
                x //= q
            pts.append(tuple(v))
    P = len(pts)
    assert P == (q + 1) * (q * q + 1)
    code = {}
    for i, v in enumerate(pts):
        code[v] = i
    Pa = np.array(pts, dtype=np.int64)

    def normalise(v):
        for c in v:
            if c:
                ic = inv[c]
                return tuple(int(mul[ic, x]) for x in v)
        return None

    def Bform_all(x):
        t1 = add[mul[x[0], Pa[:, 1]], neg[mul[x[1], Pa[:, 0]]]]
        t2 = add[mul[x[2], Pa[:, 3]], neg[mul[x[3], Pa[:, 2]]]]
        return add[t1, t2]

    lines = []
    line_of = {}
    for i in range(P):
        x = pts[i]
        perp = np.where(Bform_all(x) == 0)[0]
        for j in perp:
            if j == i:
                continue
            y = pts[j]
            # points of span(x,y): x + b y (b in GF(q)) and y
            L = [i, int(j)]
            for b in range(1, q):
                v = tuple(int(add[x[k], mul[b, y[k]]]) for k in range(4))
                L.append(code[normalise(v)])
            key = tuple(sorted(L))
            if key not in line_of:
                line_of[key] = len(lines)
                lines.append(key)
    assert len(lines) == P, (len(lines), P)
    lines = np.array(lines, dtype=np.int32)
    k = q + 1
    adj = np.zeros((2 * P, k), dtype=np.int32)
    fill = np.zeros(P, np.int64)
    for l in range(P):
        for p in lines[l]:
            adj[p, fill[p]] = P + l
            fill[p] += 1
        adj[P + l] = lines[l]
    assert (fill == k).all()
    adj.sort(axis=1)
    return dict(q=q, P=P, adj=adj, pts=Pa, lines=lines)


def selftest(g):
    from collections import deque
    q, P, adj = g['q'], g['P'], g['adj']
    V = 2 * P
    k = q + 1
    # BFS from a point and from a line
    for s in (0, P):
        dist = -np.ones(V, np.int64)
        dist[s] = 0
        dq = deque([s])
        npaths = np.zeros(V, np.int64)
        npaths[s] = 1
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if dist[y] < 0:
                    dist[y] = dist[x] + 1
                    dq.append(y)
                if dist[y] == dist[x] + 1:
                    npaths[y] += npaths[x]
        hist = np.bincount(dist)
        print('BFS from', 'point' if s < P else 'line', 'dist hist', hist.tolist(),
              'geodesic counts at d4:', sorted(set(npaths[dist == 4].tolist())),
              'd3:', sorted(set(npaths[dist == 3].tolist())))
        assert dist.max() == 4 and (dist >= 0).all()
        assert hist.tolist() == [1, k, k * q, k * q * q, q ** 3]
        assert set(npaths[dist == 4].tolist()) == {k}
        assert set(npaths[dist == 3].tolist()) == {1}


if __name__ == '__main__':
    import time
    q = int(sys.argv[1])
    t = time.time()
    g = build(q)
    print('W(%d): P=%d, V=%d, build %.1fs' % (q, g['P'], 2 * g['P'], time.time() - t))
    selftest(g)
    print('OK')
