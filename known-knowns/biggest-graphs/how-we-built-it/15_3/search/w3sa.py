#!/usr/bin/env python3
"""
w3sa.py -- W3 deficit of a graph given as bitmask adjacency (n <= 64).

A "W3 controller" is a regular simple graph in which every NON-ADJACENT ordered pair (u,v), u = v included, is joined
by a walk of length exactly 3.  Cost = sum_u #{v : v not adjacent to u (v = u allowed) and no 3-walk u..v}.
(Only w3_cost is kept here; it is used by vsa5.py.  The original module also held annealers for 4-regular
controllers that are not used for the (15,3) graph.)
"""
import numpy as np
from numba import njit


@njit(cache=True)
def w3_cost(adj, n):
    full = (np.uint64(1) << np.uint64(n)) - np.uint64(1) if n < 64 else ~np.uint64(0)
    r2 = np.zeros(n, dtype=np.uint64)
    for u in range(n):
        m = adj[u]
        acc = np.uint64(0)
        for v in range(n):
            if (m >> np.uint64(v)) & np.uint64(1):
                acc |= adj[v]
        r2[u] = acc
    c = 0
    for u in range(n):
        m = adj[u]
        r3 = np.uint64(0)
        for v in range(n):
            if (m >> np.uint64(v)) & np.uint64(1):
                r3 |= r2[v]
        miss = full & ~r3 & ~adj[u]
        # popcount
        x = miss
        while x:
            x &= x - np.uint64(1)
            c += 1
    return c
