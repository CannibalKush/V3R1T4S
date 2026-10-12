"""vsearch.py: geodesic enumeration helpers (numba) used by symsearch.py.

Background.  B = incidence graph of the generalized quadrangle W(q); every pair of opposite vertices (distance 4 in B)
is joined by q+1 geodesics.  A Z_n voltage alpha on the edges of B (edge = (point p, line L)) gives the lift
(p,i) ~ (L, i + alpha_e); condition (C4): for every opposite pair (u,w) the q+1 geodesic voltages (signed sums
along the geodesic) cover Z_n.  count_bad(alpha, n, D) returns the number of opposite pairs violating (C4).

This file keeps, verbatim, only the functions of the original vsearch.py that symsearch.py calls (the plain,
non-symmetric WalkSAT search and its command-line driver were used for a different table cell and are omitted).
"""
import numpy as np
from numba import njit


def edge_index(adj, P):
    """edges = (point p, line L); eid[v, j] = id of edge {v, adj[v,j]}."""
    V, k = adj.shape
    eid = -np.ones((V, k), np.int64)
    ends = []
    for p in range(P):
        for j in range(k):
            eid[p, j] = len(ends)
            ends.append((p, int(adj[p, j])))
    ends = np.array(ends, np.int64)
    lookup = {(int(a), int(b)): i for i, (a, b) in enumerate(ends)}
    for L in range(P, V):
        for j in range(k):
            eid[L, j] = lookup[(int(adj[L, j]), L)]
    return eid, ends


@njit(cache=True)
def _count_geod(adj, P):
    V, k = adj.shape
    G = 0
    for u in range(V):
        for ia in range(k):
            a = adj[u, ia]
            for ib in range(k):
                b = adj[a, ib]
                if b == u:
                    continue
                for ic in range(k):
                    c = adj[b, ic]
                    if c == a:
                        continue
                    for iw in range(k):
                        w = adj[c, iw]
                        if w == b:
                            continue
                        if u < w:
                            G += 1
    return G


@njit(cache=True)
def _enum_geod(adj, eid, P, G, pid):
    """geodesics u-a-b-c-w with u < w.  ge[g] = 4 edge ids, gsign[g] = +1 if u is a point, gpair[g] = pair id.
    pid: V x V int32 array initialised to -1 (filled here)."""
    V, k = adj.shape
    ge = np.empty((G, 4), np.int32)
    gsign = np.empty(G, np.int8)
    gpair = np.empty(G, np.int32)
    npair = 0
    g = 0
    for u in range(V):
        s = 1 if u < P else -1
        for ia in range(k):
            a = adj[u, ia]
            e1 = eid[u, ia]
            for ib in range(k):
                b = adj[a, ib]
                if b == u:
                    continue
                e2 = eid[a, ib]
                for ic in range(k):
                    c = adj[b, ic]
                    if c == a:
                        continue
                    e3 = eid[b, ic]
                    for iw in range(k):
                        w = adj[c, iw]
                        if w == b:
                            continue
                        if u < w:
                            e4 = eid[c, iw]
                            if pid[u, w] < 0:
                                pid[u, w] = npair
                                npair += 1
                            ge[g, 0] = e1
                            ge[g, 1] = e2
                            ge[g, 2] = e3
                            ge[g, 3] = e4
                            gsign[g] = s
                            gpair[g] = pid[u, w]
                            g += 1
    return ge, gsign, gpair, npair


@njit(cache=True)
def _csr(keys, nkeys, width):
    """keys: (G, width) -> CSR over key values: ptr, (row index, column position)."""
    G = keys.shape[0]
    cnt = np.zeros(nkeys + 1, np.int64)
    for g in range(G):
        for j in range(width):
            cnt[keys[g, j] + 1] += 1
    for i in range(nkeys):
        cnt[i + 1] += cnt[i]
    ptr = cnt.copy()
    rows = np.empty(cnt[nkeys], np.int32)
    pos = np.empty(cnt[nkeys], np.int8)
    fill = cnt[:nkeys].copy()
    for g in range(G):
        for j in range(width):
            kk = keys[g, j]
            rows[fill[kk]] = g
            pos[fill[kk]] = j
            fill[kk] += 1
    return ptr, rows, pos


@njit(cache=True)
def _init_state(alpha, ge, gsign, gpair, npair, n):
    G = ge.shape[0]
    gval = np.empty(G, np.int8)
    cnt = np.zeros((npair, n), np.int32)
    for g in range(G):
        s = gsign[g]
        v = s * alpha[ge[g, 0]] - s * alpha[ge[g, 1]] + s * alpha[ge[g, 2]] - s * alpha[ge[g, 3]]
        v %= n
        gval[g] = v
        cnt[gpair[g], v] += 1
    return gval, cnt


def count_bad(alpha, n, D):
    gval, cnt = _init_state(alpha, D['ge'], D['gsign'], D['gpair'], D['npair'], n)
    return int((cnt == 0).any(axis=1).sum())
