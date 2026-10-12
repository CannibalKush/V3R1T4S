"""Edge pruning: remove edges whose deletion keeps diameter <= D (frees degree slots for further insertions).
Screen each candidate edge (a,c) with BFS from a and c (if a or c loses any vertex within D -> critical, keep);
otherwise confirm with an exact full evaluation."""
import numpy as np
from numba import njit
from ddlib import bfs_dist, add_edge, rm_edge, bad_pairs


@njit(cache=True)
def prune(adj, deg, n, D, order_a, order_b):
    W = (n + 63) // 64
    R = np.zeros((n, W), np.uint64); Rn = np.zeros((n, W), np.uint64); df = np.zeros(n, np.int64)
    dist = np.empty(n, np.int32); q = np.empty(n, np.int32)
    removed = 0
    for t in range(len(order_a)):
        a = order_a[t]; c = order_b[t]
        # still an edge?
        ok = False
        for j in range(deg[a]):
            if adj[a, j] == c:
                ok = True
        if not ok:
            continue
        rm_edge(adj, deg, a, c)
        crit = False
        for s in (a, c):
            bfs_dist(adj, deg, n, s, dist, q)
            for v in range(n):
                if dist[v] < 0 or dist[v] > D:
                    crit = True
                    break
            if crit:
                break
        if not crit:
            if bad_pairs(adj, deg, n, D, W, R, Rn, df) != 0:
                crit = True
        if crit:
            add_edge(adj, deg, a, c)
        else:
            removed += 1
    return removed
