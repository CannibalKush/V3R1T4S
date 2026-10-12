"""Helpers for assign_generic.py, copied without change from the original search code:
  csr        - compressed adjacency (indptr int64, neighbours int32) of an undirected edge array;
  bad_pairs  - exact bit-parallel BFS (numba, parallel over batches of 64*W sources) from every 'top' vertex
               off..off+T-1 to depth D; returns, per batch, the unordered top-top pairs (s < v) at distance > D.
"""
import numpy as np
from numba import njit, prange


def csr(n, E):
    u = np.concatenate([E[:, 0], E[:, 1]])
    v = np.concatenate([E[:, 1], E[:, 0]])
    o = np.argsort(u, kind='stable')
    u, v = u[o], v[o]
    indptr = np.zeros(n + 1, np.int64)
    np.add.at(indptr, u + 1, 1)
    indptr = np.cumsum(indptr)
    return indptr, v.astype(np.int32)


@njit(parallel=True, cache=True)
def bad_pairs(ip, ix, n, off, T, D, W, cap):
    S = 64 * W
    nbt = (T + S - 1) // S
    cnt = np.zeros(nbt, np.int64)
    out = np.zeros((nbt, cap, 2), np.int64)
    for b in prange(nbt):
        base = off + b * S
        nb = min(S, off + T - base)
        vis = np.zeros((n, W), np.uint64); fr = np.zeros((n, W), np.uint64); nf = np.zeros((n, W), np.uint64)
        full = np.zeros(W, np.uint64)
        for t in range(nb):
            bit = np.uint64(1) << np.uint64(t & 63)
            vis[base + t, t >> 6] |= bit; fr[base + t, t >> 6] |= bit; full[t >> 6] |= bit
        for lev in range(D):
            for v in range(n):
                for w in range(W):
                    if vis[v, w] == full[w]:
                        nf[v, w] = np.uint64(0)
                        continue
                    acc = np.uint64(0)
                    for p in range(ip[v], ip[v + 1]):
                        acc |= fr[ix[p], w]
                    nf[v, w] = acc & ~vis[v, w]
            for v in range(n):
                for w in range(W):
                    fr[v, w] = nf[v, w]; vis[v, w] |= nf[v, w]
        c = 0
        for v in range(off, off + T):
            for w in range(W):
                miss = full[w] & ~vis[v, w]
                while miss:
                    t = 0
                    x = miss
                    while (x & np.uint64(1)) == 0:
                        x >>= np.uint64(1); t += 1
                    miss &= miss - np.uint64(1)
                    s = base + w * 64 + t
                    if s < v:  # record each unordered pair once (from the smaller endpoint)
                        if c < cap:
                            out[b, c, 0] = s; out[b, c, 1] = v
                        c += 1
        cnt[b] = c
    return cnt, out
