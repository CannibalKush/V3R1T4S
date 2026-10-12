#!/usr/bin/env python3
"""lb_lns_inc.py: INCREMENTAL version of the plateau-walk exact LNS
(lb_lns_gen.py).

Bottleneck removed: lb_lns_gen re-enumerates ALL C(n,w) words every round to find the low-blocked words
(C(28,14) * C(14,3) = 1.5e10 subset ranks for A(28,8,14): ~200 s/round, >90% of the round).  Here a blocker-count
array cnt[colex rank of x] (int16, one entry per weight-w word) is maintained incrementally:
  cnt[x] = number of codewords y with |x & y| >= t (t = w - d/2 + 1), codewords carry the sentinel SENT.
Changing one codeword touches only its sum_{j=1}^{d/2-1} C(w,j) C(n-w,j) conflicting words (141k for (28,8,14)).
Each round:  owner table rebuilt from the current code (validates it: no t-subset used twice),
             low-blocked words = {x : cnt[x] <= KB} by a vectorised scan, their blockers read from the owner table,
             and |blockers(x)| == cnt[x] is ASSERTED for every low word (consistency of the incremental counts),
             then exactly lb_lns_gen's move selection (exact MIS per removal set, improving moves first, else a
             random fraction of disjoint plateau moves), then cnt is updated for removed / inserted words
             (an inserted word must have cnt == 0 after the removals: asserted).
Every --verify-every rounds the counts are recomputed from scratch and compared (full consistency check).

usage: lb_lns_inc.py SEED.npy N D W OUT_PREFIX [--seconds S] [--rounds R] [--rmax 12] [--kb 4] [--max4 20000]
                     [--clusters 6000] [--seed X] [--plateau-frac 0.3] [--verify-every 25]
"""
import sys, os, time, json, random
import numpy as np
import numba as nb
from math import comb
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lns6 import binom_table, KMAX
from gslib import _unrank_colex
from lb_lns_gen import sub_ranks_g, build_owner_g, mis_exact_g

SENT = np.int16(30000)


@nb.njit(cache=True)
def rank_w(x, n, B):
    r = 0
    k = 0
    for p in range(n):
        if (x >> p) & 1:
            k += 1
            r += B[p, k]
    return r


@nb.njit(cache=True)
def _submasks(pos, m, jmax, out):
    """all j-subsets (j = 1..jmax <= 3) of pos[0:m] as bitmasks, grouped by j; returns offsets off[0..jmax]."""
    off = np.zeros(4, dtype=np.int64)
    k = 0
    one = np.int64(1)
    off[0] = 0
    for i1 in range(m):
        out[k] = one << pos[i1]
        k += 1
    off[1] = k
    if jmax >= 2:
        for i1 in range(m):
            for i2 in range(i1 + 1, m):
                out[k] = (one << pos[i1]) | (one << pos[i2])
                k += 1
    off[2] = k
    if jmax >= 3:
        for i1 in range(m):
            for i2 in range(i1 + 1, m):
                for i3 in range(i2 + 1, m):
                    out[k] = (one << pos[i1]) | (one << pos[i2]) | (one << pos[i3])
                    k += 1
    off[3] = k
    return off


@nb.njit(cache=True)
def update_neighbors(c, n, w, r, B, cnt, delta):
    """cnt[y] += delta for every weight-w word y != c with |y & c| >= w - r  (r = d/2 - 1 <= 3)."""
    supp = np.zeros(64, dtype=np.int64)
    comp = np.zeros(64, dtype=np.int64)
    a = 0
    b = 0
    for p in range(n):
        if (c >> p) & 1:
            supp[a] = p
            a += 1
        else:
            comp[b] = p
            b += 1
    S = np.zeros(16384, dtype=np.int64)
    C = np.zeros(65536, dtype=np.int64)
    oS = _submasks(supp, a, r, S)
    oC = _submasks(comp, b, r, C)
    touched = 0
    for j in range(1, r + 1):
        s0 = oS[j - 1]
        s1 = oS[j]
        c0 = oC[j - 1]
        c1 = oC[j]
        for u in range(s0, s1):
            cu = c ^ S[u]
            for v in range(c0, c1):
                y = cu | C[v]
                cnt[rank_w(y, n, B)] += delta
                touched += 1
    return touched


@nb.njit(cache=True)
def init_counts(words, n, w, r, B, cnt, sent):
    for i in range(len(words)):
        cnt[rank_w(words[i], n, B)] = sent
    for i in range(len(words)):
        update_neighbors(words[i], n, w, r, B, cnt, 1)
    bad = 0
    for i in range(len(words)):
        if cnt[rank_w(words[i], n, B)] != sent:
            bad += 1
    return bad


@nb.njit(parallel=True, cache=True)
def low_blockers(ranks, n, w, r, B, owner, words, KB, cnt):
    L = len(ranks)
    outw = np.zeros(L, dtype=np.int64)
    outb = -np.ones((L, KB), dtype=np.int64)
    outn = np.zeros(L, dtype=np.int64)
    mism = np.zeros(L, dtype=np.int64)
    for i in nb.prange(L):
        x = _unrank_colex(ranks[i], w, B)
        outw[i] = x
        rk = np.zeros(B[w, r], dtype=np.int64)
        e = np.zeros(64, dtype=np.int64)
        S = np.zeros((r + 1, 65), dtype=np.int64)
        pos = np.zeros(r, dtype=np.int64)
        m = sub_ranks_g(x, n, w, r, B, rk, e, S, pos)
        nbk = 0
        for k in range(m):
            o = owner[rk[k]]
            if o != -1:
                dup = False
                for j in range(nbk):
                    if outb[i, j] == o:
                        dup = True
                        break
                if not dup:
                    if nbk < KB:
                        outb[i, nbk] = o
                    nbk += 1
        outn[i] = nbk
        if nbk != cnt[ranks[i]]:
            mism[i] = 1
    return outw, outb, outn, mism.sum()


def compatible(x, y, tthr):
    return bin(int(x) & int(y)).count("1") < tthr


class Walk:
    def __init__(self, words, n, d, w, KB, log):
        self.n, self.d, self.w, self.KB, self.log = n, d, w, KB, log
        self.r = d // 2 - 1
        assert 1 <= self.r <= 3
        need = lambda m: sum(comb(m, j) for j in range(1, self.r + 1))
        assert need(w) <= 16384 and need(n - w) <= 65536, "submask buffers too small"
        self.B = binom_table(63)
        self.words = np.unique(words.astype(np.int64))
        t0 = time.time()
        self.cnt = np.zeros(comb(n, w), dtype=np.int16)
        bad = init_counts(self.words, n, w, self.r, self.B, self.cnt, SENT)
        assert bad == 0, "a codeword was counted as a neighbour of another codeword: INVALID seed"
        log(f"  init counts: {comb(n, w)} words, {time.time()-t0:.1f}s")

    def full_recount_ok(self):
        c2 = np.zeros_like(self.cnt)
        init_counts(self.words, self.n, self.w, self.r, self.B, c2, SENT)
        return np.array_equal(c2, self.cnt)

    def analyse(self):
        n, w, r, B, KB = self.n, self.w, self.r, self.B, self.KB
        owner = -np.ones(comb(n, w - r), dtype=np.int32)
        bad = build_owner_g(self.words, len(self.words), n, w, r, B, owner)
        assert bad == 0, f"INVALID code: {bad} shared t-subsets"
        ranks = np.nonzero(self.cnt <= KB)[0].astype(np.int64)
        lw, lb, ln, mism = low_blockers(ranks, n, w, r, B, owner, self.words, KB, self.cnt)
        assert mism == 0, f"incremental counts inconsistent for {mism} words"
        return lw, lb, ln

    def apply(self, removed, inserted):
        n, w, r, B = self.n, self.w, self.r, self.B
        for c in removed:
            self.cnt[rank_w(np.int64(c), n, B)] = 0
            update_neighbors(np.int64(c), n, w, r, B, self.cnt, -1)
        for s in inserted:
            k = rank_w(np.int64(s), n, B)
            assert self.cnt[k] == 0, "inserted word still blocked"
            self.cnt[k] = SENT
            update_neighbors(np.int64(s), n, w, r, B, self.cnt, 1)


def run_round(W, rmax, rng, node_cap, ncluster, plateau_frac, max4, log):
    n, d, w, KB = W.n, W.d, W.w, W.KB
    words = W.words
    tthr = w - d // 2 + 1
    t0 = time.time()
    lw, lb, ln = W.analyse()
    t1 = time.time()
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
    log(f"  analyse(inc): {len(lw)} low-blocked words, by #blockers {hist.tolist()} ({t1-t0:.1f}s)")
    adj = defaultdict(set)
    for s in byset:
        if len(s) >= 2:
            for a in s:
                for b in s:
                    if a != b:
                        adj[a].add(b)
    Rs = set()
    big = []
    for s in byset:
        if 1 <= len(s) <= 3:
            Rs.add(s)
        elif len(s) >= 4:
            big.append(s)
    if len(big) > max4:
        big = rng.sample(big, max4)
    Rs.update(big)
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
        candl = np.array(cl + [int(words[c]) for c in R], dtype=np.int64)
        best, bestC, complete = mis_exact_g(candl, len(candl), tthr, node_cap)
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
    applied = []
    used, ins = set(), []

    def try_apply(R, S):
        if any(c in used for c in R):
            return False
        for x in S:
            for y in ins:
                if not compatible(x, y, tthr):
                    return False
        used.update(R)
        ins.extend(S)
        applied.append((R, S))
        return True

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
        return 0, 0
    rm = set(c for R, S in applied for c in R)
    removed = [int(words[i]) for i in rm]
    keep = np.array([int(words[i]) for i in range(len(words)) if i not in rm], dtype=np.int64)
    new = np.unique(np.concatenate([keep, np.array(ins, dtype=np.int64)]))
    assert len(new) == len(keep) + len(ins), "duplicate insertion"
    W.apply(removed, ins)
    W.words = new
    return len(new) - len(words), len(applied)


def main():
    seedfile, n, d, w, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    arg = lambda k, dflt: type(dflt)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else dflt
    rounds = arg("--rounds", 100000)
    seconds = arg("--seconds", 3600.0)
    rmax = arg("--rmax", 12)
    KB = arg("--kb", 4)
    rs = arg("--seed", 1)
    ncl = arg("--clusters", 6000)
    pf = arg("--plateau-frac", 0.3)
    node_cap = arg("--nodecap", 100000)
    max4 = arg("--max4", 20000)
    vev = arg("--verify-every", 25)
    rng = random.Random(rs)
    logf = open(outp + ".log", "a")

    def log(s):
        print(s, flush=True)
        logf.write(s + "\n"); logf.flush()

    words = np.load(seedfile).astype(np.int64)
    log(f"start(inc) {seedfile} M={len(np.unique(words))} n={n} d={d} w={w} rmax={rmax} KB={KB} seed={rs} "
        f"clusters={ncl} max4={max4} pf={pf}")
    t0 = time.time()
    W = Walk(words, n, d, w, KB, log)
    best = len(W.words)
    for r in range(rounds):
        if time.time() - t0 > seconds:
            break
        gain, napp = run_round(W, rmax, rng, node_cap, ncl, pf, max4, log)
        M = len(W.words)
        log(f"round {r}: M={M} gain={gain} applied={napp} best={max(best, M)} t={time.time()-t0:.0f}s")
        if vev and (r + 1) % vev == 0:
            ok = W.full_recount_ok()
            log(f"  full recount check: {'OK' if ok else 'MISMATCH'}")
            assert ok
        if M > best:
            best = M
            np.save(outp + "_best.npy", W.words)
            with open(outp + "_best.json", "w") as f:
                json.dump({"M": M, "n": n, "w": w, "d": d, "round": r, "t": time.time() - t0, "seed": seedfile}, f)
        np.save(outp + "_cur.npy", W.words)
    log(f"done best={best}")


if __name__ == "__main__":
    main()
