#!/usr/bin/env python3
"""Bigger Theorem-3 cut sets for Rajiv's compound surgery (Zenodo 23052995, Lemma 5 / Theorem 3).

The block geometry I (incidence graph of the generalized hexagon H(q)) is extracted from block 0 of Rajiv's OWN edge
file, so all labels are his: points = [0, P), lines = [P, 2P) (witness layout: block i = [2iP, 2(i+1)P), points
first). A cut set on the point side must be a set of pairwise non-collinear points (every line holds at most one of
them); on the line side a set of pairwise non-concurrent lines (every point lies on at most one of them).

Both are packings in a linear (q+1)-uniform, (q+1)-regular hypergraph; we run an ARW-style iterated local search:
  * (1,c)-swap: for a chosen element x, every 'neighbour line' through x that holds a 1-tight candidate (an element
    whose ONLY conflict is x) contributes one candidate; candidates on different lines through x are pairwise
    compatible (girth of the incidence graph >= 8), so removing x and inserting one candidate per such line gains
    c-1 >= 1 whenever c >= 2.
  * perturbation: force a random non-chosen element in (removing its conflicts), local search, accept if not worse
    than current-1, restart from the best after a stall.
Warm start: Rajiv's witness sets (deleted_points / deleted_lines), or a previous output of this script (--init).
Output: JSON with the best set (Rajiv labels) and an independent re-check of the packing property.
The random stream is numba's (np.random.seed inside the jitted kernel), so results can depend on the numba version.

Usage: cutsets.py --rajiv graph.edges.xz --witness cs.json --side points|lines --iters N [--rounds R] [--stall S]
                  --seed s [--init previous.json] [--cache block0.npz] --out out.json
"""
import argparse, json, lzma, time, os, sys
import numpy as np
import pandas as pd
from numba import njit


def read_block0(path, P):
    """Return incidence arrays (pt_lines[P,k], ln_pts[P,k]) of block 0 (vertices < 2P)."""
    op = lzma.open if path.endswith('.xz') else open
    chunks = []
    with op(path, 'rt') as f:
        first = f.readline().split()
        for df in pd.read_csv(f, sep=r'\s+', header=None, dtype=np.int64, engine='c', chunksize=4_000_000):
            E = df.values
            keep = (E[:, 0] < 2 * P) & (E[:, 1] < 2 * P)
            chunks.append(E[keep])
    E = np.concatenate(chunks)
    # header line may itself be an edge (no header) -- Rajiv's files have 'n m' header; check
    E = np.sort(E, 1)
    assert (E[:, 0] < P).all() and (E[:, 1] >= P).all(), 'block 0 is not point-line bipartite'
    u = E[:, 0]; v = E[:, 1] - P
    k = len(E) // P
    assert len(E) == k * P
    o = np.lexsort((v, u)); pt_lines = v[o].reshape(P, k)
    o = np.lexsort((u, v)); ln_pts = u[o].reshape(P, k)
    assert (np.bincount(u, minlength=P) == k).all() and (np.bincount(v, minlength=P) == k).all()
    return pt_lines.astype(np.int32), ln_pts.astype(np.int32), first


@njit(cache=True)
def _add(x, el_c, c_el, occ, tight, inS):
    inS[x] = True
    for j in range(el_c.shape[1]):
        c = el_c[x, j]
        occ[c] = x
        for jj in range(c_el.shape[1]):
            u = c_el[c, jj]
            if u != x:
                tight[u] += 1


@njit(cache=True)
def _rem(x, el_c, c_el, occ, tight, inS):
    inS[x] = False
    for j in range(el_c.shape[1]):
        c = el_c[x, j]
        occ[c] = -1
        for jj in range(c_el.shape[1]):
            u = c_el[c, jj]
            if u != x:
                tight[u] -= 1


@njit(cache=True)
def _ils_improve(el_c, c_el, occ, tight, inS, queue, qlen, size):
    """queue holds candidate elements to (re)examine (members: swap; non-members: free insert)."""
    k = el_c.shape[1]
    cand = np.empty(k, np.int64)
    while qlen > 0:
        qlen -= 1
        x = queue[qlen]
        if not inS[x]:
            if tight[x] == 0:
                _add(x, el_c, c_el, occ, tight, inS)
                size += 1
            continue
        # count lines through x holding a 1-tight candidate
        c = 0
        for j in range(k):
            ln = el_c[x, j]
            best = -1
            cnt = 0
            for jj in range(c_el.shape[1]):
                u = c_el[ln, jj]
                if u != x and tight[u] == 1:
                    cnt += 1
                    if np.random.randint(cnt) == 0:
                        best = u
            if best >= 0:
                cand[c] = best
                c += 1
        if c >= 2:
            _rem(x, el_c, c_el, occ, tight, inS)
            size -= 1
            for i in range(c):
                u = cand[i]
                if tight[u] == 0 and not inS[u]:
                    _add(u, el_c, c_el, occ, tight, inS)
                    size += 1
            # re-examine the new members and members collinear with them
            for i in range(c):
                u = cand[i]
                if inS[u] and qlen < queue.shape[0]:
                    queue[qlen] = u
                    qlen += 1
            for j in range(k):
                ln = el_c[x, j]
                for jj in range(c_el.shape[1]):
                    u = c_el[ln, jj]
                    if tight[u] == 0 and not inS[u]:
                        _add(u, el_c, c_el, occ, tight, inS)
                        size += 1
    return size


@njit(cache=True)
def ils(el_c, c_el, init, seconds_iters, seed, stall_restart):
    np.random.seed(seed)
    n = el_c.shape[0]
    nc = c_el.shape[0]
    k = el_c.shape[1]
    occ = -np.ones(nc, np.int64)
    tight = np.zeros(n, np.int64)
    inS = np.zeros(n, np.bool_)
    size = 0
    for x in init:
        _add(x, el_c, c_el, occ, tight, inS)
        size += 1
    queue = np.empty(4 * n, np.int64)
    # initial: all members + free insertion everywhere
    qlen = 0
    for x in range(n):
        queue[qlen] = x
        qlen += 1
    size = _ils_improve(el_c, c_el, occ, tight, inS, queue, qlen, size)
    best = inS.copy()
    bsize = size
    cur_iter = 0
    since = 0
    for it in range(seconds_iters):
        cur_iter += 1
        # perturb: force a random non-member with low tightness
        v = np.random.randint(n)
        tries = 0
        while (inS[v] or tight[v] > 2) and tries < 50:
            v = np.random.randint(n)
            tries += 1
        if inS[v]:
            continue
        qlen = 0
        for j in range(k):
            o = occ[el_c[v, j]]
            if o >= 0:
                _rem(o, el_c, c_el, occ, tight, inS)
                size -= 1
                # its other lines' points may become free
                for jj in range(k):
                    ln = el_c[o, jj]
                    for t in range(c_el.shape[1]):
                        u = c_el[ln, t]
                        if qlen < queue.shape[0]:
                            queue[qlen] = u
                            qlen += 1
        _add(v, el_c, c_el, occ, tight, inS)
        size += 1
        # examine members near v
        for j in range(k):
            ln = el_c[v, j]
            for t in range(c_el.shape[1]):
                u = c_el[ln, t]
                for j2 in range(k):
                    o = occ[el_c[u, j2]]
                    if o >= 0 and qlen < queue.shape[0]:
                        queue[qlen] = o
                        qlen += 1
        if qlen < queue.shape[0]:
            queue[qlen] = v
            qlen += 1
        size = _ils_improve(el_c, c_el, occ, tight, inS, queue, qlen, size)
        if size > bsize:
            bsize = size
            best[:] = inS
            since = 0
        else:
            since += 1
        if since > stall_restart:
            # restart from best
            for x in range(n):
                if inS[x]:
                    _rem(x, el_c, c_el, occ, tight, inS)
            size = 0
            for x in range(n):
                if best[x]:
                    _add(x, el_c, c_el, occ, tight, inS)
                    size += 1
            since = 0
    return best, bsize


def check_packing(S, el_c, nc):
    """Independent check: every constraint (line for points / point for lines) contains <= 1 element of S."""
    cnt = np.bincount(el_c[np.asarray(S)].ravel(), minlength=nc)
    return int(cnt.max()) if len(S) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rajiv', required=True)
    ap.add_argument('--witness', required=True)
    ap.add_argument('--side', choices=['points', 'lines'], required=True)
    ap.add_argument('--iters', type=int, default=2_000_000)
    ap.add_argument('--rounds', type=int, default=1, help='repeat ILS rounds, warm-starting from the best')
    ap.add_argument('--stall', type=int, default=200_000)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--out', required=True)
    ap.add_argument('--cache', default=None, help='npz cache of block-0 incidence')
    ap.add_argument('--init', default=None, help='warm start from a previous cutsets.py JSON (same side)')
    a = ap.parse_args()
    W = json.load(open(a.witness))
    q, k6 = W['q'], W['k']
    P = (q ** k6 - 1) // (q - 1)
    t0 = time.time()
    if a.cache and os.path.exists(a.cache):
        z = np.load(a.cache); pt_lines, ln_pts = z['pt_lines'], z['ln_pts']
    else:
        pt_lines, ln_pts, first = read_block0(a.rajiv, P)
        if a.cache:
            np.savez(a.cache, pt_lines=pt_lines, ln_pts=ln_pts)
    print(f'block 0 incidence: P={P}, k={pt_lines.shape[1]} ({time.time()-t0:.1f}s)', flush=True)
    if a.side == 'points':
        el_c, c_el = pt_lines, ln_pts       # elements = points, constraints = lines
        init = np.array(W['deleted_points'], np.int64)
    else:
        el_c, c_el = ln_pts, pt_lines       # elements = lines, constraints = points
        init = np.array(W['deleted_lines'], np.int64)
        if init.max() >= P:                 # in case lines are stored with the +P offset
            init = init - P
    if a.init:
        J = json.load(open(a.init)); assert J['side'] == a.side
        init = np.array(J['set'], np.int64)
        print(f'warm start from {a.init}: {len(init)}', flush=True)
    viol0 = check_packing(init, el_c, P)
    print(f'start {a.side}: |S| = {len(init)}, max per constraint = {viol0}', flush=True)
    assert viol0 <= 1, 'start set is not a packing in this labelling'
    rajiv_size = len(W['deleted_points'] if a.side == 'points' else W['deleted_lines'])
    best = init.copy(); bsize = len(init)
    log = []
    for r in range(a.rounds):
        t1 = time.time()
        B, bs = ils(el_c, c_el, best, a.iters, a.seed + 1000 * r, a.stall)
        S = np.flatnonzero(B)
        mx = check_packing(S, el_c, P)
        assert mx <= 1 and len(S) == bs
        log.append({'round': r, 'size': int(bs), 'seconds': round(time.time() - t1, 1)})
        print(f'round {r}: best {bs} (start {len(init)}, Rajiv {rajiv_size}), {time.time()-t1:.1f}s', flush=True)
        if bs >= bsize:
            best = S.astype(np.int64); bsize = bs
    out = {'side': a.side, 'q': q, 'P': P, 'rajiv_size': int(rajiv_size), 'start_size': int(len(init)), 'best_size': int(bsize),
           'labels': 'Rajiv block-0 labels; points 0..P-1, lines 0..P-1 (line vertex = P + label in block 0)',
           'set': [int(x) for x in sorted(best)], 'rounds': log, 'iters': a.iters, 'seed': a.seed,
           'max_per_constraint': check_packing(best, el_c, P)}
    json.dump(out, open(a.out, 'w'))
    print(f'wrote {a.out}: {a.side} best {bsize} vs Rajiv {rajiv_size}; total {time.time()-t0:.1f}s')


if __name__ == '__main__':
    main()
