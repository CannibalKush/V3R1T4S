#!/usr/bin/env python3
"""
rcl3.py -- route-chart lifts over F_q^3 (q in {2,3,4,5}) with typed ports, plus exact checks.

Lift of a k-regular controller C: vertices (u, x), x in F_q^3; for each controller edge {a,b} (a<b):
    (a, x) ~ (b, T_ab x + lam * w_ab),  lam in F_q,      w_ab = T_ab d[a][b]  (so <w_ab> = <d[b][a]>)
where d[a][b] is the 'incoming direction' at a of the lines towards b.  Degree k*q, order q^3 * |C|.

Port-vector calculus (see NOTES.md): for a NB 3-walk u-a-b-v the controllability matrix has rank 3 iff
T_ab span(d[a][u], d[a][b]) != span(d[b][a], d[b][v]); the 6 backtracking 3-walks a-x-a-b / a-b-y-b reach the
planes T_ab span(d[a][x], d[a][b]) and span(d[b][a], d[b][y]) through the common point T_ab x.

Field elements are ints 0..q-1; q=4 uses F_2[w]/(w^2+w+1) with addition = XOR.
"""
import itertools
import numpy as np


class GF:
    def __init__(self, q):
        self.q = q
        if q in (2, 3, 5):
            self.add = np.array([[(a + b) % q for b in range(q)] for a in range(q)], dtype=np.int64)
            self.mul = np.array([[(a * b) % q for b in range(q)] for a in range(q)], dtype=np.int64)
        elif q == 4:
            # elements: 0, 1, w=2, w^2=w+1=3 ; addition is XOR of the 2-bit representation
            self.add = np.array([[a ^ b for b in range(4)] for a in range(4)], dtype=np.int64)
            def m(a, b):
                # polynomial multiplication mod w^2+w+1 over F_2
                r = 0
                for i in range(2):
                    if (b >> i) & 1:
                        r ^= a << i
                if r & 4:
                    r ^= 0b111
                return r
            self.mul = np.array([[m(a, b) for b in range(4)] for a in range(4)], dtype=np.int64)
        else:
            raise ValueError('unsupported q')
        self.neg = np.array([next(b for b in range(q) if self.add[a, b] == 0) for a in range(q)], dtype=np.int64)
        self.inv = np.array([0] + [next(b for b in range(q) if self.mul[a, b] == 1) for a in range(1, q)],
                            dtype=np.int64)
        # points of F_q^3 coded as integers x0*q^2 + x1*q + x2
        self.pts = np.array(list(itertools.product(range(q), repeat=3)), dtype=np.int64)
        self.code = {tuple(p): i for i, p in enumerate(self.pts.tolist())}

    def mv(self, A, x):
        q = self.q
        out = []
        for i in range(3):
            s = 0
            for j in range(3):
                s = self.add[s, self.mul[A[i][j], x[j]]]
            out.append(int(s))
        return tuple(out)

    def mm(self, A, B):
        cols = [self.mv(A, [B[0][j], B[1][j], B[2][j]]) for j in range(3)]
        return tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))

    def vadd(self, x, y):
        return tuple(int(self.add[a, b]) for a, b in zip(x, y))

    def smul(self, c, x):
        return tuple(int(self.mul[c, a]) for a in x)

    def rank(self, vecs):
        M = [list(v) for v in vecs]
        r = 0
        ncol = 3
        for c in range(ncol):
            piv = next((i for i in range(r, len(M)) if M[i][c]), None)
            if piv is None:
                continue
            M[r], M[piv] = M[piv], M[r]
            iv = int(self.inv[M[r][c]])
            M[r] = [int(self.mul[iv, a]) for a in M[r]]
            for i in range(len(M)):
                if i != r and M[i][c]:
                    f = M[i][c]
                    M[i] = [int(self.add[a, self.neg[self.mul[f, b]]]) for a, b in zip(M[i], M[r])]
            r += 1
        return r

    def span(self, vecs):
        """frozenset of all F_q-combinations."""
        out = set()
        for co in itertools.product(range(self.q), repeat=len(vecs)):
            v = (0, 0, 0)
            for c, x in zip(co, vecs):
                v = self.vadd(v, self.smul(c, x))
            out.add(v)
        return frozenset(out)

    def line(self, v):
        return self.span([v])

    def normalize(self, v):
        """projective representative: first nonzero coordinate = 1."""
        for a in v:
            if a:
                iv = int(self.inv[a])
                return self.smul(iv, v)
        return v

    def gl3(self):
        """all invertible 3x3 matrices (as tuple-of-rows)."""
        q = self.q
        vecs = [tuple(p) for p in self.pts.tolist() if any(p)]
        out = []
        for c0 in vecs:
            for c1 in vecs:
                if self.rank([c0, c1]) < 2:
                    continue
                for c2 in vecs:
                    if self.rank([c0, c1, c2]) < 3:
                        continue
                    out.append(tuple(tuple((c0, c1, c2)[j][i] for j in range(3)) for i in range(3)))
        return out


def pencil(F, d):
    """the q+1 planes (frozensets) containing the line <d>."""
    planes = set()
    for v in F.pts.tolist():
        v = tuple(v)
        if F.rank([d, v]) == 2:
            planes.add(F.span([d, v]))
    return sorted(planes, key=lambda s: sorted(s))


def edge_turn_report(F, T, da, Da_other, db, Db_other):
    """T: transport (a->b) with T da || db.  Da_other: directions at a of the other ports (list),
    Db_other: directions at b of the other ports.  Returns (bad turns list [(i,j)], pencil_complete_ab,
    pencil_complete_ba)."""
    Tplanes_a = [frozenset(F.mv(T, v) for v in F.span([x, da])) for x in Da_other]
    planes_b = [F.span([db, y]) for y in Db_other]
    bad = [(i, j) for i, P in enumerate(Tplanes_a) for j, Q in enumerate(planes_b) if P == Q]
    pen = pencil(F, db)
    have = set(Tplanes_a) | set(planes_b)
    complete_ab = all(P in have for P in pen)
    # reverse direction: planes at a: span(da, x) and T^-1 planes of b -- complete iff same set mapped back
    complete_ba = complete_ab  # bijection T^-1 maps the union back; equality of unions is symmetric
    return bad, complete_ab, complete_ba


def build_lift_edges(F, n, E, d, T):
    """E: list of (a,b) a<b; d[(a,b)] = direction at a towards b; T[(a,b)] = transport a->b.
    returns sorted list of lift edges (i,j) with i<j, vertex index u*q^3 + code(x)."""
    q = F.q
    m = q ** 3
    edges = set()
    pts = [tuple(p) for p in F.pts.tolist()]
    for (a, b) in E:
        A = T[(a, b)]
        w = F.mv(A, d[(a, b)])
        assert F.rank([w]) == 1
        for x in pts:
            y0 = F.mv(A, x)
            for lam in range(q):
                y = F.vadd(y0, F.smul(lam, w))
                i, j = a * m + F.code[x], b * m + F.code[y]
                assert i != j
                edges.add((min(i, j), max(i, j)))
    return sorted(edges)


def bitset_bad_pairs(N, edges, D):
    """exact count of ordered pairs at distance > D (multi-source bitset BFS, numpy)."""
    E = np.array(edges, dtype=np.int64)
    W = (N + 63) // 64
    cur = np.zeros((N, W), dtype=np.uint64)
    ar = np.arange(N)
    cur[ar, ar // 64] |= (np.uint64(1) << (ar % 64).astype(np.uint64))
    src = np.concatenate([E[:, 0], E[:, 1]])
    dst = np.concatenate([E[:, 1], E[:, 0]])
    for _ in range(D):
        nxt = cur.copy()
        np.bitwise_or.at(nxt, src, cur[dst])
        cur = nxt
    reached = np.zeros(N, dtype=np.int64)
    for w in range(W):
        x = cur[:, w].copy()
        x = x - ((x >> np.uint64(1)) & np.uint64(0x5555555555555555))
        x = (x & np.uint64(0x3333333333333333)) + ((x >> np.uint64(2)) & np.uint64(0x3333333333333333))
        x = (x + (x >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
        reached += ((x * np.uint64(0x0101010101010101)) >> np.uint64(56)).astype(np.int64)
    deg = np.bincount(E.ravel(), minlength=N)
    return int((N - reached).sum()), int(deg.max()), int(deg.min())
