#!/usr/bin/env python3
"""
vsa5.py (k-regular version of vsa.py) -- simulated annealing for W3 controllers with a built-in symmetry group G (order m): the controller is a
G-voltage lift of a 4-regular base multigraph on b vertices; BOTH the base graph and the voltages are annealed.
Base edge e = (bi[e], bj[e], volt[e]); lift edges (i,g) ~ (j, g*volt) for all g in G (loops allowed; an involution
loop is a semi-edge). Moves: (1) change one voltage; (2) 'endpoint swap' of two base edges (i-j, i'-j') ->
(i-j', i'-j) with fresh random voltages. The lift must stay simple and 4-regular (else rejected).
Cost = W3 deficit of the lift (every non-adjacent ordered pair incl. u=u needs a walk of length exactly 3).
Usage: vsa5.py --b 4 --group Z15 --k 5 --iters 1000000 --restarts 30 --seed 5 --out prefix   (writes prefix.json)
"""
import argparse, json, os, sys, time
import numpy as np
from numba import njit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w3sa import w3_cost
from vlift_w3 import make_group
import numba


@njit(cache=True)
def build_adj_k(b, m, bi, bj, volt, mul, inv, adj, k):
    """returns True if simple and every vertex has degree 4."""
    n = b * m
    for x in range(n):
        adj[x] = np.uint64(0)
    for e in range(bi.shape[0]):
        i = bi[e]; j = bj[e]; h = volt[e]
        for g in range(m):
            u = i * m + g
            v = j * m + mul[g, h]
            if u == v:
                return False
            bit = np.uint64(1) << np.uint64(v)
            if i == j and h == inv[h]:
                # involution loop: each pair added twice (from g and from g*h); add once
                if (adj[u] & bit) and v < u:
                    continue
            if adj[u] & bit:
                return False
            adj[u] |= bit
            adj[v] |= np.uint64(1) << np.uint64(u)
    for x in range(n):
        c = 0
        y = adj[x]
        while y:
            y &= y - np.uint64(1)
            c += 1
        if c != k:
            return False
    return True



@njit(cache=True)
def anneal(b, m, bi, bj, volt, mul, inv, iters, T0, T1, seed, period, pswap, k):
    np.random.seed(seed)
    n = b * m
    adj = np.zeros(n, dtype=np.uint64)
    BIG = 10 ** 6
    ok = build_adj_k(b, m, bi, bj, volt, mul, inv, adj, k)
    cost = w3_cost(adj, n) if ok else BIG
    best = cost
    bbi = bi.copy(); bbj = bj.copy(); bv = volt.copy()
    ne = bi.shape[0]
    for it in range(iters):
        ph = (it % period) / period
        T = T0 * (T1 / T0) ** ph
        if np.random.random() < pswap:
            e1 = np.random.randint(ne); e2 = np.random.randint(ne)
            if e1 == e2:
                continue
            o1i, o1j, o1v = bi[e1], bj[e1], volt[e1]
            o2i, o2j, o2v = bi[e2], bj[e2], volt[e2]
            if np.random.random() < 0.5:
                bj[e1] = o2j; bj[e2] = o1j
            else:
                bj[e1] = o2i; bi[e2] = o1j
            volt[e1] = np.random.randint(m); volt[e2] = np.random.randint(m)
            ok = build_adj_k(b, m, bi, bj, volt, mul, inv, adj, k)
            nc = w3_cost(adj, n) if ok else BIG
            if nc <= cost or np.random.random() < np.exp(-(nc - cost) / T):
                cost = nc
            else:
                bi[e1], bj[e1], volt[e1] = o1i, o1j, o1v
                bi[e2], bj[e2], volt[e2] = o2i, o2j, o2v
        else:
            e = np.random.randint(ne)
            old = volt[e]
            volt[e] = np.random.randint(m)
            ok = build_adj_k(b, m, bi, bj, volt, mul, inv, adj, k)
            nc = w3_cost(adj, n) if ok else BIG
            if nc <= cost or np.random.random() < np.exp(-(nc - cost) / T):
                cost = nc
            else:
                volt[e] = old
        if cost < best:
            best = cost
            bbi[:] = bi; bbj[:] = bj; bv[:] = volt
            if best == 0:
                break
        if (it + 1) % period == 0 and np.random.random() < 0.5:
            bi[:] = bbi; bj[:] = bbj; volt[:] = bv; cost = best
    return best, bbi, bbj, bv


def random_base(b, m, mul, inv, rng, k, tries=100000):
    """random 4-regular base multigraph (configuration model; loops allowed) with random voltages giving a simple
    4-regular lift (2b base edges, no semi-edges at init)."""
    for _ in range(tries):
        stubs = np.repeat(np.arange(b), k)
        rng.shuffle(stubs)
        E = stubs.reshape(-1, 2)
        bi = E[:, 0].astype(np.int64).copy(); bj = E[:, 1].astype(np.int64).copy()
        for _ in range(50):
            volt = rng.integers(0, m, size=len(bi)).astype(np.int64)
            adj = np.zeros(b * m, dtype=np.uint64)
            if build_adj_k(b, m, bi, bj, volt, mul, inv, adj, k):
                return bi, bj, volt
    raise RuntimeError('no valid start')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--b', type=int, required=True)
    ap.add_argument('--k', type=int, default=5)
    ap.add_argument('--base', default=None, help='fixed base edges i-j,... (use with --pswap 0)')
    ap.add_argument('--group', required=True)
    ap.add_argument('--iters', type=int, default=2_000_000)
    ap.add_argument('--restarts', type=int, default=5)
    ap.add_argument('--T0', type=float, default=1.0)
    ap.add_argument('--T1', type=float, default=0.05)
    ap.add_argument('--period', type=int, default=200000)
    ap.add_argument('--pswap', type=float, default=0.4)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    mul = make_group(a.group)
    m = mul.shape[0]
    inv = np.array([int(np.where(mul[g] == 0)[0][0]) for g in range(m)], dtype=np.int64)
    n = a.b * m
    assert n <= 64
    rng = np.random.default_rng(a.seed)
    t0 = time.time()
    best = None
    for r in range(a.restarts):
        if a.base:
            pr = [tuple(map(int, t.split('-'))) for t in a.base.split(',')]
            bi = np.array([x for x, _ in pr], dtype=np.int64); bj = np.array([y for _, y in pr], dtype=np.int64)
            while True:
                volt = rng.integers(0, m, size=len(pr)).astype(np.int64)
                if build_adj_k(a.b, m, bi, bj, volt, mul, inv, np.zeros(a.b * m, dtype=np.uint64), a.k):
                    break
        else:
            bi, bj, volt = random_base(a.b, m, mul, inv, rng, a.k)
        c, bbi, bbj, bv = anneal(a.b, m, bi, bj, volt, mul, inv, a.iters, a.T0, a.T1,
                                 int(rng.integers(1 << 30)), a.period, a.pswap, a.k)
        print(f'n={n} b={a.b} {a.group} restart {r}: best W3 deficit {c} ({time.time()-t0:.1f}s)', flush=True)
        if best is None or c < best[0]:
            best = (int(c), bbi.tolist(), bbj.tolist(), bv.tolist())
        if c == 0:
            break
    print(f'BEST {best[0]}', flush=True)
    if a.out:
        c, bi, bj, volt = best
        adj = np.zeros(n, dtype=np.uint64)
        assert build_adj_k(a.b, m, np.array(bi), np.array(bj), np.array(volt), mul, inv, adj, a.k)
        edges = sorted(set((min(u, v), max(u, v)) for u in range(n) for v in range(n) if (int(adj[u]) >> v) & 1))
        json.dump({'n': n, 'w3_deficit': c, 'group': a.group, 'b': a.b, 'bi': bi, 'bj': bj, 'volt': volt,
                   'edges': edges}, open(a.out + '.json', 'w'))
        print('saved', a.out + '.json')


if __name__ == '__main__':
    main()
