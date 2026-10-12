#!/usr/bin/env python3
"""Generic shortcut repair for a graph G = base part B (vertices < off) + 'top' part (vertices off..off+t-1)
whose only possibly-bad pairs are top-top pairs (all other pairs are guaranteed by a theorem: tower theorem or
Rajiv's Theorem 3), and must then be confirmed by a full all-pairs BFS.

For every bad top pair (x, y) (exact bitset BFS, depth D) we add one shortcut edge s1--s2 between two base vertices
with free degree (Delta - deg > 0), s1 within distance d1 of a base neighbour u of x and s2 within d2 of a base
neighbour v of y (distances inside B), d1 + d2 <= D - 3, so that x-u-..-s1-s2-..-v-y has length <= D.
Shortcuts must respect free-slot capacities (a vertex with c free slots can host c shortcuts). Assignment:
constrained-first greedy + WalkSAT-style ejections. Adding edges never lengthens a path, so after the assignment
no bad pair remains among the original ones (and no new one can appear); a final exact re-evaluation confirms.
Usage: assign_generic.py --graph G.edges --delta 15 --off 1417248 --t 7648 --D 6 --out OUT.edges [--seed 1]
          [--iters 3000000] [--hours 0.5] [--write_partial]
Writes OUT.edges (only if no bad pair is left) and OUT.edges.shortcuts.npy (the added shortcut edges).
"""
import argparse, os, sys, time, hashlib
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toppairs import csr, bad_pairs  # noqa: E402


def read(path):
    with open(path) as f:
        df = pd.read_csv(f, sep=r'\s+', header=None, dtype=np.int64, engine='c', comment='#')
    E = np.sort(df.values[:, :2], 1)
    return E


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--graph', required=True); ap.add_argument('--delta', type=int, required=True)
    ap.add_argument('--off', type=int, required=True); ap.add_argument('--t', type=int, required=True)
    ap.add_argument('--D', type=int, default=6); ap.add_argument('--out', required=True)
    ap.add_argument('--seed', type=int, default=1); ap.add_argument('--iters', type=int, default=5000000)
    ap.add_argument('--hours', type=float, default=1.0)
    ap.add_argument('--write_partial', action='store_true')
    a = ap.parse_args()
    t0 = time.time()
    rng = np.random.default_rng(a.seed)
    E = read(a.graph)
    N = int(E.max()) + 1
    assert N == a.off + a.t, (N, a.off, a.t)
    deg = np.bincount(E.ravel(), minlength=N)
    assert deg.max() <= a.delta
    ip, ix = csr(N, E)
    ix32 = ix.astype(np.int32)
    cnt, out = bad_pairs(ip, ix32, N, a.off, a.t, a.D, 4, 200000)
    P = np.concatenate([out[b, :min(cnt[b], 200000)] for b in range(len(cnt)) if cnt[b]], 0) if cnt.sum() else np.zeros((0, 2), np.int64)
    print(f'N={N} m={len(E)}: bad top pairs {int(cnt.sum())} ({time.time()-t0:.0f}s)', flush=True)
    assert len(P) == cnt.sum()
    cap0 = np.zeros(N, np.int64); cap0[:a.off] = a.delta - deg[:a.off]
    # base adjacency (inside B only)
    def nb_base(u):
        nb = ix[ip[u]:ip[u + 1]]
        return nb[nb < a.off]
    cache = {}

    def balls(u):
        if u in cache:
            return cache[u]
        n1 = nb_base(u)
        n2 = np.unique(np.concatenate([nb_base(w) for w in n1])) if len(n1) else np.zeros(0, np.int64)
        n2 = n2[n2 != u]
        cache[u] = (n1, n2)
        return cache[u]

    att = {}
    def attachments(x):
        if x not in att:
            nb = ix[ip[x]:ip[x + 1]]
            att[x] = nb[nb < a.off]
        return att[x]
    K = a.D - 3   # d1 + d2 <= K
    blocks = []
    for i in range(len(P)):
        x, y = int(P[i, 0]), int(P[i, 1])
        bl = []
        for u in attachments(x):
            n1u, n2u = balls(int(u))
            for v in attachments(y):
                n1v, n2v = balls(int(v))
                combos = [(n1u, n1v)]
                if K >= 3:
                    combos += [(n1u, n2v), (n2u, n1v)]
                for A, B in combos:
                    As = A[cap0[A] > 0]; Bs = B[cap0[B] > 0]
                    if len(As) and len(Bs):
                        bl.append((As, Bs))
        blocks.append(bl)
    ncand = np.array([sum(len(A) * len(B) for A, B in bl) for bl in blocks])
    print(f'candidates per pair: min {ncand.min() if len(ncand) else 0} median {int(np.median(ncand)) if len(ncand) else 0}; '
          f'zero: {int((ncand == 0).sum())}; free slots {int(cap0.sum())} ({time.time()-t0:.0f}s)', flush=True)
    use = np.zeros(N, np.int64)            # slots used
    holders = {}                           # vertex -> set of pair ids using it
    assign = [None] * len(P)
    eset = set(map(tuple, E.tolist())) if len(E) < 5_000_000 else None
    used_edges = set()

    def adjacent(s1, s2):
        k = (min(s1, s2), max(s1, s2))
        return (k in eset) if eset is not None else (s2 in set(ix[ip[s1]:ip[s1 + 1]].tolist()))

    def place(i, s1, s2):
        k = (min(s1, s2), max(s1, s2))
        assign[i] = k; used_edges.add(k)
        for s in k:
            use[s] += 1; holders.setdefault(s, set()).add(i)

    def unplace(j):
        k = assign[j]
        used_edges.discard(k); assign[j] = None
        for s in k:
            use[s] -= 1; holders[s].discard(j)

    def try_assign(i):
        bl = list(blocks[i]); rng.shuffle(bl)
        for A, B in bl:
            Af = A[use[A] < cap0[A]]; Bf = B[use[B] < cap0[B]]
            if not len(Af) or not len(Bf):
                continue
            for _ in range(4):
                s1 = int(rng.choice(Af)); s2 = int(rng.choice(Bf))
                if s1 == s2 or adjacent(s1, s2) or (min(s1, s2), max(s1, s2)) in used_edges:
                    continue
                place(i, s1, s2); return True
        return False

    order = np.argsort(ncand + rng.random(len(P)))
    U = [int(i) for i in order if not try_assign(int(i))]
    print(f'greedy: unassigned {len(U)} of {len(P)} ({time.time()-t0:.0f}s)', flush=True)
    it = 0; tabu = {}; best = len(U)
    while U and it < a.iters and time.time() - t0 < a.hours * 3600:
        if it % 1000 == 0 and all(len(blocks[j]) == 0 for j in U):
            break   # only candidate-less pairs remain
        it += 1
        k = int(rng.integers(len(U))); i = U[k]; U[k] = U[-1]; U.pop()
        if try_assign(i):
            pass
        elif blocks[i]:
            A, B = blocks[i][int(rng.integers(len(blocks[i])))]
            s1 = int(rng.choice(A)); s2 = int(rng.choice(B))
            key = (min(s1, s2), max(s1, s2))
            if s1 == s2 or adjacent(s1, s2) or key in used_edges:
                U.append(i); continue
            victims = set()
            for s in key:
                if use[s] >= cap0[s]:
                    victims.add(int(rng.choice(sorted(holders[s]))))
            if any(tabu.get(j, -10 ** 9) > it - 50 for j in victims) and rng.random() < 0.8:
                U.append(i); continue
            for j in victims:
                unplace(j); U.append(j)
            place(i, s1, s2); tabu[i] = it
        else:
            U.append(i)
        if len(U) < best:
            best = len(U)
            if best % 50 == 0 or best < 20:
                print(f'  it {it}: unassigned {best} ({time.time()-t0:.0f}s)', flush=True)
    print(f'search end: unassigned {len(U)} after {it} iterations ({time.time()-t0:.0f}s)', flush=True)
    S = np.array([assign[i] for i in range(len(P)) if assign[i] is not None], np.int64).reshape(-1, 2)
    E2 = np.concatenate([E, S], 0)
    E2 = np.sort(E2, 1)
    key = E2[:, 0] * N + E2[:, 1]
    assert len(np.unique(key)) == len(key) and (E2[:, 0] != E2[:, 1]).all()
    deg2 = np.bincount(E2.ravel(), minlength=N)
    assert deg2.max() <= a.delta
    ip2, ix2 = csr(N, E2)
    cnt2, _ = bad_pairs(ip2, ix2.astype(np.int32), N, a.off, a.t, a.D, 4, 1000)
    print(f'exact re-evaluation with {len(S)} shortcuts: bad {int(cnt2.sum())}; maxdeg {deg2.max()} ({time.time()-t0:.0f}s)', flush=True)
    np.save(a.out + '.shortcuts.npy', S)
    if cnt2.sum() > 0 and a.write_partial:
        o = np.lexsort((E2[:, 1], E2[:, 0])); E3 = E2[o]
        pd.DataFrame(E3).to_csv(a.out + '.partial.edges', sep=' ', header=False, index=False)
        print('WROTE partial', a.out + '.partial.edges', flush=True)
    if cnt2.sum() == 0:
        o = np.lexsort((E2[:, 1], E2[:, 0])); E2 = E2[o]
        pd.DataFrame(E2).to_csv(a.out, sep=' ', header=False, index=False)
        print('WROTE', a.out, N, hashlib.sha256(open(a.out, 'rb').read()).hexdigest(), flush=True)


if __name__ == '__main__':
    main()
