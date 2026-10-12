#!/usr/bin/env python3
"""exact_sc.py: EXACT shortcut repair of the remaining bad new-new pairs of a relaxed-Y
compound-surgery graph. For a bad pair (x,y): BFS from x and from y (depth D-2) in the CURRENT graph; any two base vertices
s1, s2 with a free slot, s1 != s2, (s1,s2) not an edge, and d(x,s1) + d(y,s2) <= D-1 give the walk x..s1-s2..y of length
<= D. Adding edges never lengthens any path, so every pair fixed this way stays fixed and no pair becomes bad; an exact
re-evaluation (bad_new in newpairs.py) confirms 0 bad new-new pairs at the end. Candidate choice: smallest total distance,
then prefer vertices with 2 free slots. (Unlike assign_generic.py of the (15,6) search, s1/s2 may be reached through
Y-neighbours or be an attachment itself.)
usage: exact_sc.py IN.edges Delta off OUT.edges [--D 6] [--threads 6] [--rebuild-every 50] [--quiet] [--pairs PAIRS.txt]
Writes OUT.edges and OUT.edges.extra_shortcuts.npy. The pair order is shuffled with numpy default_rng(1).
"""
import sys, time, argparse, hashlib, os
import numpy as np, pandas as pd
import numba as nb
from numba import njit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from newpairs import bad_new, csr  # noqa: E402


@njit(cache=True)
def bfs_depth(ip, ix, n, s, r, dist, q):
    dist[s] = 0; q[0] = s; h = 0; t = 1
    while h < t:
        v = q[h]; h += 1
        if dist[v] >= r:
            continue
        for p in range(ip[v], ip[v + 1]):
            u = ix[p]
            if dist[u] < 0:
                dist[u] = dist[v] + 1; q[t] = u; t += 1
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('inp'); ap.add_argument('Delta', type=int); ap.add_argument('off', type=int); ap.add_argument('out')
    ap.add_argument('--D', type=int, default=6); ap.add_argument('--threads', type=int, default=6)
    ap.add_argument('--rebuild-every', type=int, default=50); ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--pairs', default=None, help='file of vertex pairs to fix (e.g. xchk XCHK_DUMP output) instead of bad new-new pairs')
    a = ap.parse_args(); nb.set_num_threads(a.threads); t0 = time.time(); D = a.D
    E = np.sort(pd.read_csv(a.inp, sep=r'\s+', header=None, usecols=[0, 1], dtype=np.int64, engine='c').to_numpy(), 1)
    n = int(E.max()) + 1; off = a.off
    ip, ix = csr(n, E)
    if a.pairs:
        P = np.loadtxt(a.pairs, dtype=np.int64, comments='#').reshape(-1, 2); c = len(P)
        print(f"start N={n} M={len(E)} pairs to fix from {a.pairs}: {c} ({time.time()-t0:.0f}s)", flush=True)
    else:
        c, P = bad_new(ip, ix, n, off, D)
        print(f"start N={n} M={len(E)} bad new-new pairs {c} ({time.time()-t0:.0f}s)", flush=True)
        assert c == len(P)
    deg = np.bincount(E.ravel(), minlength=n)
    free = (a.Delta - deg).astype(np.int64); free[off:] = 0      # only base vertices may take shortcuts
    eset = set((E[:, 0] * n + E[:, 1]).tolist())
    dist = np.full(n, -1, np.int64); q = np.empty(n, np.int64)
    dist2 = np.full(n, -1, np.int64); q2 = np.empty(n, np.int64)
    added = []; nfixed_before = 0
    order = np.random.default_rng(1).permutation(len(P))
    since = 0
    for (x, y) in P[order].tolist():
        if since >= a.rebuild_every:
            ip, ix = csr(n, np.concatenate([E, np.array(added, np.int64)], 0)); since = 0
        tx = bfs_depth(ip, ix, n, x, D - 2, dist, q)
        ty = bfs_depth(ip, ix, n, y, D - 2, dist2, q2)
        if dist[y] >= 0 and dist[y] <= D:
            pass
        # already fixed by an earlier shortcut? d(x,y) <= D iff some v has dist_x(v) + dist_y(v) <= D (depth-(D-2) balls
        # suffice for D <= 2(D-2), i.e. D >= 4: a shortest path of length <= D has a vertex within floor(D/2) of both ends)
        QX = q[:tx]; both = QX[dist2[QX] >= 0]
        if len(both) and int((dist[both] + dist2[both]).min()) <= D:
            dist[q[:tx]] = -1; dist2[q2[:ty]] = -1; nfixed_before += 1
            continue
        X = q[:tx]; X = X[(X < off) & (free[X] > 0)]
        Y = q2[:ty]; Y = Y[(Y < off) & (free[Y] > 0)]
        best = None
        # group by distance
        dX = dist[X]; dY = dist2[Y]
        for k in range(1, D - 1):
            Xs = X[dX == k]
            if not len(Xs):
                continue
            Ys = Y[dY <= D - 1 - k]
            if not len(Ys):
                continue
            # pick a pair not already adjacent, prefer more free slots
            Xs = Xs[np.argsort(-free[Xs], kind='stable')][:200]; Ys = Ys[np.argsort(dist2[Ys] * 10 - free[Ys], kind='stable')][:200]
            for s1 in Xs.tolist():
                for s2 in Ys.tolist():
                    if s1 == s2 or free[s1] <= 0 or free[s2] <= 0:
                        continue
                    kk = min(s1, s2) * n + max(s1, s2)
                    if kk in eset:
                        continue
                    tot = k + int(dist2[s2])
                    if best is None or tot < best[0]:
                        best = (tot, s1, s2)
                    break
                if best is not None and best[0] <= k + 1:
                    break
        dist[q[:tx]] = -1; dist2[q2[:ty]] = -1
        if best is None:
            print(f"  pair ({x},{y}): NO exact candidate", flush=True); continue
        tot, s1, s2 = best
        added.append((min(s1, s2), max(s1, s2))); eset.add(min(s1, s2) * n + max(s1, s2))
        free[s1] -= 1; free[s2] -= 1; since += 1
        if not a.quiet:
            print(f"  pair ({x},{y}): shortcut {s1}-{s2} (d(x,s1)+d(y,s2) = {tot}, walk length {tot+1})", flush=True)
    print(f"pairs already fixed by earlier shortcuts: {nfixed_before}; shortcuts added: {len(added)}", flush=True)
    if added:
        E = np.concatenate([E, np.array(added, np.int64)], 0)
    E = np.sort(E, 1); E = E[np.lexsort((E[:, 1], E[:, 0]))]
    ip, ix = csr(n, E)
    c2, P2 = bad_new(ip, ix, n, off, D)
    deg = np.bincount(E.ravel(), minlength=n); key = E[:, 0] * n + E[:, 1]
    assert len(np.unique(key)) == len(key) and (E[:, 0] != E[:, 1]).all() and deg.max() <= a.Delta
    print(f"exact re-evaluation with {len(added)} extra shortcuts: bad new-new pairs {c2}; maxdeg {deg.max()} ({time.time()-t0:.0f}s)", flush=True)
    pd.DataFrame(E).to_csv(a.out, sep=' ', header=False, index=False)
    np.save(a.out + '.extra_shortcuts.npy', np.array(added, np.int64))
    print(f"WROTE {a.out} N={n} M={len(E)} bad {c2} sha256 {hashlib.sha256(open(a.out,'rb').read()).hexdigest()} ({time.time()-t0:.0f}s)", flush=True)


if __name__ == '__main__':
    main()
