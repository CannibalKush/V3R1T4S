#!/usr/bin/env python3
"""Low-blocker exact LNS for d = 6 constant-weight codes.

Round:
 1. one parallel pass over ALL C(n,w) words computes, for every non-code word, its blockers (codewords sharing a
    (w-2)-subset), keeping words with <= KB blockers ("low-blocked" words);
 2. removal sets R are taken from the blocker hypergraph: singletons, the blocker pairs/triples of 2-/3-blocked words,
    and random connected clusters (|R| <= rmax) of the co-blocking graph;
 3. for each R the candidate set is every low-blocked word whose blockers lie inside R, plus R itself, and an EXACT
    maximum independent set is computed (bitset branch and bound from lns6.mis_exact);
 4. all improving moves (|MIS| > |R|) with disjoint R and mutually compatible insertions are applied at once; if there
    are none, a random batch of disjoint plateau moves (|MIS| = |R|, different words) is applied instead.
The code is re-validated (owner rebuild: no (w-2)-subset used twice) after every round and saved when it grows.
Candidates with more than KB blockers are not enumerated, so step 3 is exact over the enumerated candidate set only.

usage: lb_lns.py SEED.npy N W OUT_PREFIX [--rounds R] [--seconds S] [--rmax 8] [--kb 3] [--seed X] [--plateau-frac F]
"""
import sys, os, time, json, random
import numpy as np
import numba as nb
from math import comb
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lns6 import binom_table, sub_ranks, build_owner, mis_exact, popc, KMAX
from gslib import _unrank_colex, _next_comb


@nb.njit(parallel=True, cache=True)
def lowblock(n, w, owner, words, KB, nchunks, cap):
    B = binom_table(63)
    total = B[n, w]
    step = (total + nchunks - 1) // nchunks
    outw = np.zeros((nchunks, cap), dtype=np.int64)
    outb = -np.ones((nchunks, cap, KB), dtype=np.int64)
    outn = np.zeros((nchunks, cap), dtype=np.int8)
    cnt = np.zeros(nchunks, dtype=np.int64)
    for ch in nb.prange(nchunks):
        r0 = ch * step
        r1 = min(total, r0 + step)
        if r0 >= r1:
            continue
        rk = np.zeros(w * w, dtype=np.int64)
        e = np.zeros(64, dtype=np.int64)
        S0 = np.zeros(65, dtype=np.int64)
        S1 = np.zeros(65, dtype=np.int64)
        S2 = np.zeros(65, dtype=np.int64)
        bl = np.zeros(KB + 1, dtype=np.int64)
        x = _unrank_colex(r0, w, B)
        for r in range(r0, r1):
            m = sub_ranks(x, n, w, B, rk, e, S0, S1, S2)
            nbk = 0
            iscode = False
            for i in range(m):
                o = owner[rk[i]]
                if o != -1:
                    dup = False
                    for j in range(nbk):
                        if bl[j] == o:
                            dup = True
                            break
                    if not dup:
                        if words[o] == x:
                            iscode = True
                            break
                        bl[nbk] = o
                        nbk += 1
                        if nbk > KB:
                            break
            if (not iscode) and nbk <= KB:
                c = cnt[ch]
                if c < cap:
                    outw[ch, c] = x
                    outn[ch, c] = nbk
                    for j in range(nbk):
                        outb[ch, c, j] = bl[j]
                cnt[ch] += 1
            if r + 1 < r1:
                x = _next_comb(x)
    return outw, outb, outn, cnt


def analyse(words, n, w, KB, nchunks=256):
    B = binom_table(63)
    owner = -np.ones(comb(n, w - 2), dtype=np.int32)
    bad = build_owner(words, len(words), n, w, B, owner)
    assert bad == 0, f"INVALID code: {bad} shared (w-2)-subsets"
    cap = max(20000, int(comb(n, w) // nchunks // 20))
    while True:
        ow, ob, on, cnt = lowblock(n, w, owner, words, KB, nchunks, cap)
        if cnt.max() <= cap:
            break
        cap = int(cnt.max()) + 1000
    W, BL, NB = [], [], []
    for ch in range(nchunks):
        c = int(cnt[ch])
        W.append(ow[ch, :c]); BL.append(ob[ch, :c]); NB.append(on[ch, :c])
    return np.concatenate(W), np.concatenate(BL), np.concatenate(NB).astype(np.int64)


def compatible(x, y, w):
    return bin(int(x) & int(y)).count("1") <= w - 3


def run_round(words, n, w, KB, rmax, rng, node_cap, ncluster, plateau_frac, log):
    t0 = time.time()
    lw, lb, ln = analyse(words, n, w, KB)
    t1 = time.time()
    # index: blocker-set (sorted tuple) -> list of words ; codeword -> list of low-blocked word indices
    byset = defaultdict(list)
    bycw = defaultdict(list)
    for i in range(len(lw)):
        k = int(ln[i])
        s = tuple(sorted(int(v) for v in lb[i, :k]))
        byset[s].append(int(lw[i]))
        for c in s:
            bycw[c].append(i)
    free0 = byset.get((), [])
    hist = np.bincount(ln, minlength=KB + 1)
    log(f"  analyse: {len(lw)} low-blocked words, by #blockers {hist.tolist()} ({t1-t0:.0f}s)")
    # co-blocking graph adjacency from 2-/3-blocked words
    adj = defaultdict(set)
    for s in byset:
        if len(s) >= 2:
            for a in s:
                for b in s:
                    if a != b:
                        adj[a].add(b)
    Rs = set()
    for s in byset:
        if len(s) >= 1:
            Rs.add(s)
    # random clusters
    keys = list(adj.keys())
    for _ in range(ncluster if keys else 0):
        c = rng.choice(keys)
        R = {c}
        target = rng.randint(3, rmax)
        frontier = list(adj[c])
        while len(R) < target and frontier:
            v = frontier.pop(rng.randrange(len(frontier)))
            if v not in R:
                R.add(v)
                frontier.extend(u for u in adj[v] if u not in R)
        Rs.add(tuple(sorted(R)))
    improving, plateau = [], []
    nsolved = 0
    for R in Rs:
        Rset = set(R)
        cand = set()
        for c in R:
            for i in bycw[c]:
                k = int(ln[i])
                if all(int(v) in Rset for v in lb[i, :k]):
                    cand.add(int(lw[i]))
        if not cand:
            continue
        K = len(cand) + len(R)
        if K > KMAX:
            continue
        cl = sorted(cand)
        rng.shuffle(cl)
        candl = np.array(cl + [int(words[c]) for c in R], dtype=np.int64)  # R last: prefer new words on ties
        best, bestC, complete = mis_exact(candl, len(candl), w, node_cap)
        nsolved += 1
        if best < len(R):
            continue
        chosen = [int(candl[i]) for i in range(len(candl)) if (int(bestC[i >> 6]) >> (i & 63)) & 1]
        if best > len(R):
            improving.append((R, chosen))
        elif set(chosen) != set(int(words[c]) for c in R):
            plateau.append((R, chosen))
    t2 = time.time()
    log(f"  moves: {len(Rs)} removal sets, {nsolved} MIS solved, improving={len(improving)} plateau={len(plateau)} "
        f"({t2-t1:.0f}s)")
    # free words first (R = ())
    applied = []
    used, ins = set(), []

    def try_apply(R, S):
        if any(c in used for c in R):
            return False
        for x in S:
            for y in ins:
                if not compatible(x, y, w):
                    return False
        used.update(R)
        ins.extend(S)
        applied.append((R, S))
        return True

    # greedy maximal independent set of free words
    for x in free0:
        try_apply((), [x])
    improving.sort(key=lambda t: -(len(t[1]) - len(t[0])))
    for R, S in improving:
        try_apply(R, S)
    gain = sum(len(S) - len(R) for R, S in applied)
    if gain == 0 and plateau:
        rng.shuffle(plateau)
        for R, S in plateau[: max(1, int(len(plateau) * plateau_frac))]:
            try_apply(R, S)
    if not applied:
        return words, 0, 0
    rm = set(c for R, S in applied for c in R)
    keep = np.array([int(words[i]) for i in range(len(words)) if i not in rm], dtype=np.int64)
    new = np.unique(np.concatenate([keep, np.array(ins, dtype=np.int64)]))
    assert len(new) == len(keep) + len(ins), "duplicate insertion"
    return new, len(new) - len(words), len(applied)


def main():
    seedfile, n, w, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    arg = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
    rounds = arg("--rounds", 1000)
    seconds = arg("--seconds", 3600.0)
    rmax = arg("--rmax", 8)
    KB = arg("--kb", 3)
    rs = arg("--seed", 1)
    ncl = arg("--clusters", 3000)
    pf = arg("--plateau-frac", 0.3)
    node_cap = arg("--nodecap", 100000)
    rng = random.Random(rs)
    words = np.unique(np.load(seedfile).astype(np.int64))
    M0 = len(words)
    best = M0
    logf = open(outp + ".log", "a")

    def log(s):
        print(s, flush=True)
        logf.write(s + "\n"); logf.flush()

    log(f"start {seedfile} M={M0} n={n} w={w} rmax={rmax} KB={KB} seed={rs}")
    t0 = time.time()
    for r in range(rounds):
        if time.time() - t0 > seconds:
            break
        words, gain, napp = run_round(words, n, w, KB, rmax, rng, node_cap, ncl, pf, log)
        M = len(words)
        log(f"round {r}: M={M} gain={gain} applied={napp} best={max(best, M)} t={time.time()-t0:.0f}s")
        if M > best:
            best = M
            np.save(outp + f"_best.npy", words)
            with open(outp + "_best.json", "w") as f:
                json.dump({"M": M, "n": n, "w": w, "d": 6, "round": r, "t": time.time() - t0, "seed": seedfile}, f)
        np.save(outp + "_cur.npy", words)
    log(f"done best={best}")


if __name__ == "__main__":
    main()
