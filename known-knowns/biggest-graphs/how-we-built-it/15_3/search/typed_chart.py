#!/usr/bin/env python3
"""
typed_chart.py -- transports for route-chart lifts over F_q^3.

For a controller edge (a,b) with port directions d_a (at a towards b) and d_b (at b towards a), TransportFinder
searches transports T (a->b) with T d_a = d_b at the pencil level (the induced map F^3/<d_a> -> F^3/<d_b> ranges over
GL(2,q)), minimising (#incomplete pencil planes, #singular turns), or forcing a prescribed set of singular turns.
(Only the parts used by k5sat.py are kept here; the original module also held a command-line driver for 4-regular
typed controllers that is not used for the (15,3) graph.)
"""
import itertools
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcl3 import pencil


def mat_inv3(F, A):
    """inverse of a 3x3 matrix over F (rows as tuples)."""
    q = F.q
    M = [list(A[i]) + [1 if i == j else 0 for j in range(3)] for i in range(3)]
    for c in range(3):
        piv = next(i for i in range(c, 3) if M[i][c])
        M[c], M[piv] = M[piv], M[c]
        iv = int(F.inv[M[c][c]])
        M[c] = [int(F.mul[iv, x]) for x in M[c]]
        for i in range(3):
            if i != c and M[i][c]:
                f = M[i][c]
                M[i] = [int(F.add[x, F.neg[F.mul[f, y]]]) for x, y in zip(M[i], M[c])]
    return tuple(tuple(r[3:]) for r in M)


def complete_basis(F, d):
    """vectors x1, x2 with (d, x1, x2) a basis."""
    E = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    for x1, x2 in itertools.combinations(E, 2):
        if F.rank([d, x1, x2]) == 3:
            return x1, x2
    raise RuntimeError


class TransportFinder:
    """Transports T (a->b) with T d_a = d_b, searched at the pencil level: the induced map on the quotient
    F^3/<d_a> -> F^3/<d_b> ranges over GL(2,q) (all of PGL(2,q) on the pencils)."""

    def __init__(self, F):
        self.F = F
        q = F.q
        self.GL2 = [((a, b), (c, e)) for a, b, c, e in itertools.product(range(q), repeat=4)
                    if F.add[F.mul[a, e], F.neg[F.mul[b, c]]] != 0]
        self.cache = {}

    def quot(self, Binv, v):
        """coordinates of v in basis (d, x1, x2): returns (c1, c2) projectively normalised."""
        F = self.F
        c = F.mv(Binv, v)
        return F.normalize((c[1], c[2], 0))[:2]

    def find(self, da, Da, db, Db, prefer_bad=None, want_bad=None):
        """da: direction at a towards b; Da: other directions at a (ordered); db, Db similarly at b.
        Returns (T, bad_turns, pencil_complete) minimising (#incomplete pencil planes, #bad, preference).
        want_bad: if given, a tuple of turns that must be exactly the bad set (returns None if impossible)."""
        key = (da, tuple(Da), db, tuple(Db), prefer_bad, want_bad)
        if key in self.cache:
            return self.cache[key]
        F = self.F
        q = F.q
        xa1, xa2 = complete_basis(F, da)
        xb1, xb2 = complete_basis(F, db)
        Ba = tuple(tuple((da, xa1, xa2)[j][i] for j in range(3)) for i in range(3))
        Bb = tuple(tuple((db, xb1, xb2)[j][i] for j in range(3)) for i in range(3))
        Bainv = mat_inv3(F, Ba)
        Bbinv = mat_inv3(F, Bb)
        Pa = [self.quot(Bainv, x) for x in Da]
        Qb = [self.quot(Bbinv, y) for y in Db]
        allpts = sorted(set(F.normalize((c1, c2, 0))[:2] for c1 in range(q) for c2 in range(q) if c1 or c2))
        best = None
        for M in self.GL2:
            img = []
            for (c1, c2) in Pa:
                y1 = F.add[F.mul[M[0][0], c1], F.mul[M[0][1], c2]]
                y2 = F.add[F.mul[M[1][0], c1], F.mul[M[1][1], c2]]
                img.append(F.normalize((int(y1), int(y2), 0))[:2])
            bad = tuple((i, j) for i, P in enumerate(img) for j, Q in enumerate(Qb) if P == Q)
            if want_bad is not None and bad != want_bad:
                continue
            have = set(img) | set(Qb)
            missing = sum(1 for P in allpts if P not in have)
            score = (missing, len(bad), 0 if (prefer_bad is None or bad == prefer_bad) else 1)
            if best is None or score < best[0]:
                best = (score, M, bad, missing == 0)
                if score == (0, 0, 0):
                    break
        if best is None:
            self.cache[key] = None
            return None
        M = best[1]
        # T: d_a -> d_b, x_a1 -> M00 x_b1 + M10 x_b2, x_a2 -> M01 x_b1 + M11 x_b2
        Tx1 = F.vadd(F.smul(M[0][0], xb1), F.smul(M[1][0], xb2))
        Tx2 = F.vadd(F.smul(M[0][1], xb1), F.smul(M[1][1], xb2))
        img_cols = (db, Tx1, Tx2)
        C = tuple(tuple(img_cols[j][i] for j in range(3)) for i in range(3))
        T = F.mm(C, Bainv)
        assert F.mv(T, da) == db
        # independent re-check of the bad turns / pencil in 3D
        planes_a = [F.span([x, da]) for x in Da]
        planes_b = [F.span([db, y]) for y in Db]
        Tp = [frozenset(F.mv(T, v) for v in P) for P in planes_a]
        bad3 = tuple((i, j) for i, P in enumerate(Tp) for j, Q in enumerate(planes_b) if P == Q)
        pen = pencil(F, db)
        have3 = set(Tp) | set(planes_b)
        comp3 = all(P in have3 for P in pen)
        assert bad3 == best[2] and comp3 == best[3], (bad3, best[2], comp3, best[3])
        out = (T, best[2], best[3])
        self.cache[key] = out
        return out

    def options(self, da, Da, db, Db, require_complete=True, minimal=True):
        """all distinct bad-turn sets realisable by a transport with a complete pencil (if required).
        returns list of (bad_set_tuple, T)."""
        F = self.F
        q = F.q
        xa1, xa2 = complete_basis(F, da)
        xb1, xb2 = complete_basis(F, db)
        Ba = tuple(tuple((da, xa1, xa2)[j][i] for j in range(3)) for i in range(3))
        Bb = tuple(tuple((db, xb1, xb2)[j][i] for j in range(3)) for i in range(3))
        Bainv = mat_inv3(F, Ba)
        Bbinv = mat_inv3(F, Bb)
        Pa = [self.quot(Bainv, x) for x in Da]
        Qb = [self.quot(Bbinv, y) for y in Db]
        allpts = sorted(set(F.normalize((c1, c2, 0))[:2] for c1 in range(q) for c2 in range(q) if c1 or c2))
        found = {}
        for M in self.GL2:
            img = []
            for (c1, c2) in Pa:
                y1 = F.add[F.mul[M[0][0], c1], F.mul[M[0][1], c2]]
                y2 = F.add[F.mul[M[1][0], c1], F.mul[M[1][1], c2]]
                img.append(F.normalize((int(y1), int(y2), 0))[:2])
            bad = tuple((i, j) for i, P in enumerate(img) for j, Q in enumerate(Qb) if P == Q)
            have = set(img) | set(Qb)
            if require_complete and any(P not in have for P in allpts):
                continue
            if bad not in found:
                Tx1 = F.vadd(F.smul(M[0][0], xb1), F.smul(M[1][0], xb2))
                Tx2 = F.vadd(F.smul(M[0][1], xb1), F.smul(M[1][1], xb2))
                img_cols = (db, Tx1, Tx2)
                C = tuple(tuple(img_cols[j][i] for j in range(3)) for i in range(3))
                found[bad] = F.mm(C, Bainv)
        items = sorted(found.items(), key=lambda kv: (len(kv[0]), kv[0]))
        if minimal:
            keep = []
            for bad, T in items:
                if not any(set(b2) <= set(bad) and b2 != bad for b2, _ in keep):
                    keep.append((bad, T))
            items = keep
        return items
