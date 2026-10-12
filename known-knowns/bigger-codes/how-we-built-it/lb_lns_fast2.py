#!/usr/bin/env python3
"""lb_lns_fast2.py: lb_lns_fast.py with the removal-set generation (co-blocking graph CSR,
random connected clusters, dedupe) also in numba / numpy.  Same neighbourhood definition as lb_lns_fast.

lb_lns_fast.py: lb_lns_inc.py (incremental blocker counts) + the move
phase compiled with numba and parallelised over removal sets.

Profiling one (28,6,10) round of lb_lns_inc showed 47 s in PURE PYTHON candidate gathering (all(... in Rset) over
~23M generator steps) and < 1 s in the exact MIS solver.  Here, for every removal set R (CSR array), a numba prange
loop gathers the candidates (low-blocked words whose blockers all lie in R, each counted once via its smallest
blocker in R), runs the SAME exact bitset MIS (lb_lns_gen.mis_exact_g, R listed last), and records improving /
plateau moves.  Removal-set generation (all 1..3-blocker sets, a random sample of 4-blocker sets, random connected
clusters of the co-blocking graph with |R| <= rmax) and move application (free words, then improving moves sorted
by gain, else a random fraction of disjoint plateau moves; inserted words pairwise compatibility-checked) are the
same as in lb_lns_gen.  Code validity is re-checked every round by the owner rebuild and the incremental-count
consistency assertions of lb_lns_inc, and by a full recount every --verify-every rounds.

usage: lb_lns_fast.py SEED.npy N D W OUT_PREFIX [--seconds S] [--rounds R] [--rmax 12] [--kb 4] [--max4 20000]
                      [--clusters 6000] [--seed X] [--plateau-frac 0.3] [--verify-every 25]
"""
import sys, os, time, json, random
import numpy as np
import numba as nb
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lns6 import KMAX, WMAX
from lb_lns_gen import mis_exact_g
from lb_lns_inc import Walk

CH = 64   # max words recorded per move


@nb.njit(parallel=True, cache=True)
def solve_all(Rflat, Rptr, bptr, bidx, lw, lb, ln, words, tthr, node_cap):
    NR = len(Rptr) - 1
    status = np.zeros(NR, dtype=np.int8)      # 0 none, 1 plateau, 2 improving
    nch = np.zeros(NR, dtype=np.int64)
    chosen = np.zeros((NR, CH), dtype=np.int64)
    for q in nb.prange(NR):
        r0 = Rptr[q]
        r1 = Rptr[q + 1]
        nr = r1 - r0
        cand = np.zeros(KMAX + 1, dtype=np.int64)
        K = 0
        over = False
        for a in range(r0, r1):
            c = Rflat[a]
            for z in range(bptr[c], bptr[c + 1]):
                i = bidx[z]
                k = ln[i]
                ok = True
                mn = 1 << 62
                for j in range(k):
                    b = lb[i, j]
                    if b < mn:
                        mn = b
                    inR = False
                    for e in range(r0, r1):
                        if Rflat[e] == b:
                            inR = True
                            break
                    if not inR:
                        ok = False
                        break
                if ok and mn == c:
                    if K + nr >= KMAX:
                        over = True
                        break
                    cand[K] = lw[i]
                    K += 1
            if over:
                break
        if over or K == 0:
            continue
        # R words last (prefer new words on ties); shuffle-free but candidate order is the bycw order
        for a in range(r0, r1):
            cand[K] = words[Rflat[a]]
            K += 1
        best, bestC, complete = mis_exact_g(cand, K, tthr, node_cap)
        if best < nr:
            continue
        m = 0
        newcount = 0
        for i in range(K):
            if (bestC[i >> 6] >> np.uint64(i & 63)) & np.uint64(1):
                if m < CH:
                    chosen[q, m] = cand[i]
                m += 1
                if i < K - nr:
                    newcount += 1
        if m > CH:
            continue
        nch[q] = m
        if best > nr:
            status[q] = 2
        elif newcount > 0:
            status[q] = 1
    return status, nch, chosen


BIGV = np.int64(1) << 40


@nb.njit(cache=True)
def build_adj(uniq, M):
    U, KBc = uniq.shape
    cnt = np.zeros(M + 1, dtype=np.int64)
    for u in range(U):
        k = 0
        for j in range(KBc):
            if uniq[u, j] < BIGV:
                k += 1
        if k >= 2:
            for a in range(k):
                cnt[uniq[u, a] + 1] += k - 1
    ptr = np.cumsum(cnt)
    nbr = np.empty(ptr[M], dtype=np.int64)
    fill = ptr[:-1].copy()
    for u in range(U):
        k = 0
        for j in range(KBc):
            if uniq[u, j] < BIGV:
                k += 1
        if k >= 2:
            for a in range(k):
                ua = uniq[u, a]
                for b in range(k):
                    if b != a:
                        nbr[fill[ua]] = uniq[u, b]
                        fill[ua] += 1
    # dedupe each segment
    ptr2 = np.zeros(M + 1, dtype=np.int64)
    nbr2 = np.empty(ptr[M], dtype=np.int64)
    k2 = 0
    for c in range(M):
        seg = np.sort(nbr[ptr[c]:ptr[c + 1]])
        last = -1
        for v in seg:
            if v != last:
                nbr2[k2] = v
                k2 += 1
                last = v
        ptr2[c + 1] = k2
    return ptr2, nbr2[:k2]


@nb.njit(cache=True)
def gen_clusters(ptr, nbr, nodes, ncl, rmax, seed):
    np.random.seed(seed)
    out = np.full((ncl, rmax), BIGV, dtype=np.int64)
    front = np.empty(1 << 16, dtype=np.int64)
    if len(nodes) == 0:
        return out[:0]
    for q in range(ncl):
        c = nodes[np.random.randint(len(nodes))]
        out[q, 0] = c
        nr = 1
        target = np.random.randint(3, rmax + 1)
        nf = 0
        for z in range(ptr[c], ptr[c + 1]):
            if nf < len(front):
                front[nf] = nbr[z]
                nf += 1
        while nr < target and nf > 0:
            i = np.random.randint(nf)
            v = front[i]
            front[i] = front[nf - 1]
            nf -= 1
            inR = False
            for e in range(nr):
                if out[q, e] == v:
                    inR = True
                    break
            if inR:
                continue
            out[q, nr] = v
            nr += 1
            for z in range(ptr[v], ptr[v + 1]):
                u = nbr[z]
                inR2 = False
                for e in range(nr):
                    if out[q, e] == u:
                        inR2 = True
                        break
                if (not inR2) and nf < len(front):
                    front[nf] = u
                    nf += 1
        # insertion sort of out[q, :nr]
        for i in range(1, nr):
            x = out[q, i]
            j = i - 1
            while j >= 0 and out[q, j] > x:
                out[q, j + 1] = out[q, j]
                j -= 1
            out[q, j + 1] = x
    return out


def compatible(x, y, tthr):
    return (int(x) & int(y)).bit_count() < tthr


def run_round(W, rmax, rng, node_cap, ncluster, plateau_frac, max4, log):
    n, d, w, KB = W.n, W.d, W.w, W.KB
    words = W.words
    M = len(words)
    tthr = w - d // 2 + 1
    t0 = time.time()
    lw, lb, ln = W.analyse()
    t1 = time.time()
    L = len(lw)
    perm = np.random.default_rng(rng.randrange(1 << 30)).permutation(L)   # random tie-breaking in the MIS
    lw, lb, ln = lw[perm], lb[perm], ln[perm]
    hist = np.bincount(ln, minlength=KB + 1)
    # CSR codeword -> low words it blocks
    mask = np.arange(KB)[None, :] < ln[:, None]
    rows = lb[mask]
    cols = np.repeat(np.arange(L), ln)
    order = np.argsort(rows, kind="stable")
    bidx = cols[order].astype(np.int64)
    bptr = np.searchsorted(rows[order], np.arange(M + 1)).astype(np.int64)
    # distinct blocker sets (rows sorted, BIG-padded)
    lbs = np.sort(np.where(mask, lb, BIGV), axis=1)
    uniq = np.unique(lbs[ln > 0], axis=0)
    free0 = [int(x) for x in lw[ln == 0]]
    usize = (uniq < BIGV).sum(axis=1)
    small = uniq[usize <= 3]
    big = uniq[usize >= 4]
    if len(big) > max4:
        big = big[np.random.default_rng(rng.randrange(1 << 30)).choice(len(big), max4, replace=False)]
    aptr, anbr = build_adj(uniq, M)
    nodes = np.nonzero(np.diff(aptr) > 0)[0].astype(np.int64)
    cl = gen_clusters(aptr, anbr, nodes, ncluster, rmax, rng.randrange(1 << 30))
    width = max(rmax, KB)
    def pad(X):
        P = np.full((len(X), width), BIGV, dtype=np.int64)
        P[:, :X.shape[1]] = X[:, :min(X.shape[1], width)]
        return P
    allR = np.unique(np.concatenate([pad(small), pad(big), pad(cl)]), axis=0)
    allR = allR[np.random.default_rng(rng.randrange(1 << 30)).permutation(len(allR))]
    lens = (allR < BIGV).sum(axis=1)
    Rptr = np.zeros(len(allR) + 1, dtype=np.int64)
    Rptr[1:] = np.cumsum(lens)
    Rflat = allR[allR < BIGV].astype(np.int64)
    Rl = None
    t2 = time.time()
    status, nch, chosen = solve_all(Rflat, Rptr, bptr, bidx, lw, lb, ln, words, tthr, node_cap)
    t3 = time.time()
    imp = np.nonzero(status == 2)[0]
    pla = np.nonzero(status == 1)[0]
    log(f"  analyse(inc): {L} low-blocked words, by #blockers {hist.tolist()} ({t1-t0:.1f}s); "
        f"{len(Rptr)-1} removal sets ({t2-t1:.1f}s); solve {t3-t2:.1f}s: improving={len(imp)} plateau={len(pla)}")
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
    getR = lambda q: tuple(int(v) for v in Rflat[Rptr[q]:Rptr[q + 1]])
    impl = [(getR(q), [int(v) for v in chosen[q, :nch[q]]]) for q in imp]
    impl.sort(key=lambda t: -(len(t[1]) - len(t[0])))
    for R, S in impl:
        try_apply(R, S)
    gain = sum(len(S) - len(R) for R, S in applied)
    if gain == 0 and len(pla):
        pl = list(pla)
        rng.shuffle(pl)
        for q in pl[: max(1, int(len(pl) * plateau_frac))]:
            try_apply(getR(q), [int(v) for v in chosen[q, :nch[q]]])
    if not applied:
        return 0, 0
    rm = set(c for R, S in applied for c in R)
    removed = [int(words[i]) for i in rm]
    keep = np.array([int(words[i]) for i in range(M) if i not in rm], dtype=np.int64)
    new = np.unique(np.concatenate([keep, np.array(ins, dtype=np.int64)]))
    assert len(new) == len(keep) + len(ins), "duplicate insertion"
    W.apply(removed, ins)
    W.words = new
    return len(new) - M, len(applied)


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
    log(f"start(fast2) {seedfile} M={len(np.unique(words))} n={n} d={d} w={w} rmax={rmax} KB={KB} seed={rs} "
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
