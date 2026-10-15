#!/usr/bin/env python3
"""Independent exact solver (branch and bound, pure Python, no SAT library) for
g(n,r) = max size of an r-uniform 3-sunflower-free family on [n].

Written by fable-sun from the definition, as a second method to cross-check opus-sun's
CP-SAT values.  Vertices = r-subsets as bitmasks.  For every pair (A,B) of candidate sets the
set of 'completers' D (A&B <= D, D disjoint from A^B) is precomputed as a bitmask over the
vertex index.  DFS over vertices in a fixed order with:
  - forbidden mask: vertices that would complete a sunflower with two chosen ones,
  - bound: chosen + popcount(remaining & ~forbidden) and the (r-1)-shadow bound
    (every (r-1)-set lies in at most 2 chosen sets) -> remaining capacity.
Symmetry: the first chosen set is fixed to {0..r-1} (vertex-transitivity of S_n) when the
optimum is nonzero, which is valid since S_n acts transitively on r-sets.

Usage: exact_bb.py n r [target]   (target: stop when a family of this size is found)
Prints the maximum and one extremal family; exit code 0.
"""
import sys, itertools, time

def popcount(x):
    return bin(x).count("1")

def main():
    n, r = int(sys.argv[1]), int(sys.argv[2])
    target = int(sys.argv[3]) if len(sys.argv) > 3 else None
    sets = [sum(1 << p for p in c) for c in itertools.combinations(range(n), r)]
    N = len(sets)
    idx = {m: i for i, m in enumerate(sets)}
    # completers[i][j] = bitmask over vertices k such that (i,j,k) is a sunflower
    comp = [[0] * N for _ in range(N)]
    for i in range(N):
        A = sets[i]
        for j in range(i + 1, N):
            B = sets[j]
            core = A & B
            sym = A ^ B
            mask = 0
            for k in range(N):
                D = sets[k]
                if k != i and k != j and (D & core) == core and (D & sym) == 0:
                    mask |= 1 << k
            comp[i][j] = mask
            comp[j][i] = mask
    # (r-1)-shadow bookkeeping
    shadows = []
    for m in sets:
        sh = []
        mm = m
        while mm:
            b = mm & -mm
            sh.append(m ^ b)
            mm ^= b
        shadows.append(sh)
    best = [0, []]
    t0 = time.time()
    nodes = [0]

    def dfs(start, chosen, forbidden, cnt, shadow_cnt):
        nodes[0] += 1
        size = len(chosen)
        if size > best[0]:
            best[0] = size
            best[1] = list(chosen)
            if target is not None and size >= target:
                raise StopIteration
        # candidates: vertices >= start, not forbidden, shadow-compatible
        cand = []
        for k in range(start, N):
            if (forbidden >> k) & 1:
                continue
            ok = True
            for sh in shadows[k]:
                if shadow_cnt.get(sh, 0) >= 2:
                    ok = False
                    break
            if ok:
                cand.append(k)
        if size + len(cand) <= best[0]:
            return
        for pos, k in enumerate(cand):
            if size + (len(cand) - pos) <= best[0]:
                return
            newforb = forbidden
            for c in chosen:
                newforb |= comp[c][k]
            for sh in shadows[k]:
                shadow_cnt[sh] = shadow_cnt.get(sh, 0) + 1
            chosen.append(k)
            dfs(k + 1, chosen, newforb, cnt, shadow_cnt)
            chosen.pop()
            for sh in shadows[k]:
                shadow_cnt[sh] -= 1

    try:
        # fix the first set to vertex 0 = {0..r-1} (transitivity), then also allow empty start
        first = 0
        chosen = [first]
        shadow_cnt = {}
        for sh in shadows[first]:
            shadow_cnt[sh] = 1
        dfs(1, chosen, 0, 0, shadow_cnt)
    except StopIteration:
        pass
    fam = [[p + 1 for p in range(n) if (sets[k] >> p) & 1] for k in best[1]]
    print({"n": n, "r": r, "max": best[0], "nodes": nodes[0], "seconds": round(time.time() - t0, 1),
           "target": target, "family": fam})

if __name__ == "__main__":
    main()
