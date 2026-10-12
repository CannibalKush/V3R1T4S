"""Helpers for exact_sc.py, copied without change from the original search code:
  bad_new - exact bit-parallel BFS (numba, parallel over batches of 512 sources) from every new vertex off..n-1 to
            depth D; returns (count, list) of unordered new-new pairs (s < v) at distance > D;
  csr     - compressed adjacency (indptr, neighbours, both int64) of an undirected edge array.
"""
import numpy as np
from numba import njit, prange


@njit(parallel=True, cache=True)
def bad_new(ip, ix, n, off, D):
    """count + list bad unordered pairs (s,v), s<v, both >= off, d(s,v) > D. 512 sources per batch."""
    T = n - off
    W = 8; S = 512
    nbt = (T + S - 1) // S
    cnt = np.zeros(nbt, np.int64)
    cap = 20000
    out = np.zeros((nbt, cap, 2), np.int64)
    for b in prange(nbt):
        base = off + b * S
        ns = min(S, n - base)
        vis = np.zeros((n, W), np.uint64); fr = np.zeros((n, W), np.uint64); nf = np.zeros((n, W), np.uint64)
        full = np.zeros(W, np.uint64)
        act = np.empty(n, np.int64); na = 0
        for t in range(ns):
            bit = np.uint64(1) << np.uint64(t & 63)
            vis[base + t, t >> 6] |= bit; fr[base + t, t >> 6] |= bit; full[t >> 6] |= bit
            act[na] = base + t; na += 1
        done = np.zeros(n, np.bool_)
        act2 = np.empty(n, np.int64); inn = np.zeros(n, np.bool_)
        for lev in range(D):
            work = 0
            for i in range(na):
                work += ip[act[i] + 1] - ip[act[i]]
            na2 = 0
            if work < ip[n] // 16:
                for i in range(na):
                    u = act[i]
                    for p in range(ip[u], ip[u + 1]):
                        v = ix[p]
                        if done[v]:
                            continue
                        anyb = False
                        for w in range(W):
                            x = fr[u, w] & ~vis[v, w]
                            if x:
                                nf[v, w] |= x; anyb = True
                        if anyb and not inn[v]:
                            inn[v] = True; act2[na2] = v; na2 += 1
            else:
                for v in range(n):
                    if done[v]:
                        continue
                    anyb = False
                    for w in range(W):
                        acc = np.uint64(0)
                        for p in range(ip[v], ip[v + 1]):
                            acc |= fr[ix[p], w]
                        x = acc & ~vis[v, w]
                        nf[v, w] = x
                        if x:
                            anyb = True
                    if anyb:
                        act2[na2] = v; na2 += 1
            for i in range(na):
                u = act[i]
                for w in range(W):
                    fr[u, w] = np.uint64(0)
            for i in range(na2):
                v = act2[i]; inn[v] = False
                f = True
                for w in range(W):
                    vis[v, w] |= nf[v, w]; fr[v, w] = nf[v, w]; nf[v, w] = np.uint64(0)
                    if (vis[v, w] & full[w]) != full[w]:
                        f = False
                if f:
                    done[v] = True
            tmp = act; act = act2; act2 = tmp; na = na2
        c = 0
        for v in range(off, n):
            for w in range(W):
                miss = full[w] & ~vis[v, w]
                while miss:
                    t = 0
                    x = miss
                    while (x & np.uint64(1)) == 0:
                        x >>= np.uint64(1); t += 1
                    miss &= miss - np.uint64(1)
                    s = base + w * 64 + t
                    if s < v:
                        if c < cap:
                            out[b, c, 0] = s; out[b, c, 1] = v
                        c += 1
        cnt[b] = c
    tot = 0
    for b in range(nbt):
        tot += min(cnt[b], cap)
    res = np.zeros((tot, 2), np.int64); k = 0
    for b in range(nbt):
        for i in range(min(cnt[b], cap)):
            res[k, 0] = out[b, i, 0]; res[k, 1] = out[b, i, 1]; k += 1
    return cnt.sum(), res


def csr(n, E):
    u = np.concatenate([E[:, 0], E[:, 1]]); v = np.concatenate([E[:, 1], E[:, 0]])
    o = np.argsort(u, kind='stable')
    ip = np.zeros(n + 1, np.int64); np.add.at(ip, u + 1, 1); ip = np.cumsum(ip)
    return ip, v[o].astype(np.int64)
