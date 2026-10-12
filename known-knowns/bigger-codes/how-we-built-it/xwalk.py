#!/usr/bin/env python3
"""xwalk.py -- multi-seed screen + plateau-walk driver around lb_lns_gen.py (used for the A(52..56,8,7) codes).

Engine: the low-blocker exact LNS of lb_lns_gen.py (analyse = one parallel pass over all C(n,w) words keeping words
with <= KB blockers; removal sets R from the blocker hypergraph; EXACT maximum independent set over {low-blocked
words whose blockers lie in R} + R).
This driver adds: seed loading/validation (archive `$BASE=16` files via convert_seed.load_hex, or .npy arrays),
a one-round SCREEN mode with machine-readable stats, a resumable multi-seed WALK mode with a time budget per seed,
checkpoints (_cur.npy every round, _best.npy on every gain), and a JSON status file.

Note: the per-seed random generator is seeded with `--seed` and Python's hash() of the tag string, which is
randomised per process unless PYTHONHASHSEED is set; the original runs did not set it.

usage:
  xwalk.py screen LIST OUTDIR [--kb 3] [--rmax 8]          LIST lines: archive_file n d w [tag]
  xwalk.py walk   LIST OUTDIR --per-seed SECONDS [--total SECONDS] [--kb 3] [--rmax 8] [--seed X] [--plateau-frac F]
"""
import sys, os, time, json, random
from collections import defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lb_lns_gen as G                                # noqa: E402
from lns6 import binom_table, KMAX                    # noqa: E402
from convert_seed import load_hex                     # noqa: E402


def load_seed(path, n, d, w):
    if path.endswith(".npy"):
        ws = np.unique(np.load(path).astype(np.int64))
    else:
        words = load_hex(path, n)
        ws = np.unique(np.array([int(x) for x in words], dtype=np.int64))
    assert n <= 63, "engine supports n <= 63"
    pc = np.array([bin(int(x)).count("1") for x in ws])
    assert (pc == w).all(), f"weight mismatch in {path}"
    assert int(ws.min()) >= 0 and int(ws.max()) < (1 << n)
    # validity: owner rebuild (no (w-r)-subset used twice  <=>  min distance >= d)
    r = d // 2 - 1
    from math import comb
    owner = -np.ones(comb(n, w - r), dtype=np.int32)
    bad = G.build_owner_g(ws, len(ws), n, w, r, binom_table(63), owner)
    assert bad == 0, f"seed {path} INVALID ({bad} shared subsets)"
    return ws


def run_round(words, n, d, w, KB, rmax, rng, node_cap, ncluster, plateau_frac, log):
    """Same move logic as lb_lns_gen.run_round, but returns statistics (for the screen)."""
    tthr = w - d // 2 + 1
    t0 = time.time()
    lw, lb, ln = G.analyse(words, n, d, w, KB)
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
    hist = np.bincount(ln, minlength=KB + 1).tolist() if len(ln) else [0] * (KB + 1)
    adj = defaultdict(set)
    for s in byset:
        if len(s) >= 2:
            for a in s:
                for b in s:
                    if a != b:
                        adj[a].add(b)
    Rs = set(s for s in byset if len(s) >= 1)
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
        best, bestC, complete = G.mis_exact_g(candl, len(candl), tthr, node_cap)
        nsolved += 1
        if best < len(R):
            continue
        chosen = [int(candl[i]) for i in range(len(candl)) if (int(bestC[i >> 6]) >> (i & 63)) & 1]
        if best > len(R):
            improving.append((R, chosen))
        elif set(chosen) != set(int(words[c]) for c in R):
            plateau.append((R, chosen))
    t2 = time.time()
    applied = []
    used, ins = set(), []

    def try_apply(R, S):
        if any(c in used for c in R):
            return False
        for x in S:
            for y in ins:
                if bin(x & y).count("1") >= tthr:
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
    stats = dict(hist=hist, nR=len(Rs), solved=nsolved, improving=len(improving), plateau=len(plateau),
                 t_analyse=round(t1 - t0, 1), t_moves=round(t2 - t1, 1))
    log(f"  hist={hist} R={len(Rs)} solved={nsolved} improving={len(improving)} plateau={len(plateau)} "
        f"(analyse {t1-t0:.0f}s, moves {t2-t1:.0f}s)")
    if not applied:
        return words, 0, 0, stats
    rm = set(c for R, S in applied for c in R)
    keep = np.array([int(words[i]) for i in range(len(words)) if i not in rm], dtype=np.int64)
    new = np.unique(np.concatenate([keep, np.array(ins, dtype=np.int64)]))
    assert len(new) == len(keep) + len(ins), "duplicate insertion"
    return new, len(new) - len(words), len(applied), stats


def read_list(path):
    out = []
    for ln in open(path):
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        p = ln.split()
        f, n, d, w = p[0], int(p[1]), int(p[2]), int(p[3])
        tag = p[4] if len(p) > 4 else f"A{n}_{d}_{w}_{os.path.basename(f).replace('.npy','')}"
        out.append((f, n, d, w, tag))
    return out


def main():
    mode, lst, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    arg = lambda k, dv: type(dv)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else dv
    KB = arg("--kb", 3)
    rmax = arg("--rmax", 8)
    rs = arg("--seed", 1)
    pf = arg("--plateau-frac", 0.3)
    ncl = arg("--clusters", 3000)
    node_cap = arg("--nodecap", 100000)
    per_seed = arg("--per-seed", 600.0)
    total = arg("--total", 1e9)
    os.makedirs(outdir, exist_ok=True)
    logf = open(os.path.join(outdir, f"{mode}.log"), "a")

    def log(s):
        s = time.strftime("%H:%M:%S ") + s
        print(s, flush=True)
        logf.write(s + "\n"); logf.flush()

    T0 = time.time()
    for (f, n, d, w, tag) in read_list(lst):
        if time.time() - T0 > total:
            log("total budget exhausted"); break
        statf = os.path.join(outdir, tag + f".{mode}.json")
        if mode == "screen" and os.path.exists(statf):
            log(f"skip {tag} (screened)"); continue
        cur = os.path.join(outdir, tag + "_cur.npy")
        bestf = os.path.join(outdir, tag + "_best.npy")
        try:
            if mode == "walk" and os.path.exists(cur):
                words = load_seed(cur, n, d, w)
                st = json.load(open(statf)) if os.path.exists(statf) else {}
                M0 = st.get("M0", len(words)); best = st.get("best", len(words)); r0 = st.get("rounds", 0)
                spent = st.get("spent", 0.0)
            else:
                words = load_seed(f, n, d, w)
                M0 = len(words); best = M0; r0 = 0; spent = 0.0
                np.save(os.path.join(outdir, tag + "_seed.npy"), words)
        except Exception as e:  # noqa
            log(f"LOAD FAIL {tag}: {e!r}"); continue
        if mode == "walk" and spent >= per_seed:
            log(f"skip {tag} (budget spent {spent:.0f}s)"); continue
        rng = random.Random(rs * 1000003 + hash(tag) % 1000003)
        log(f"== {mode} {tag} file={f} n={n} d={d} w={w} M={len(words)} (seed M0={M0}, best={best}) KB={KB} rmax={rmax}")
        t0 = time.time()
        r = r0
        while True:
            words, gain, napp, stats = run_round(words, n, d, w, KB, rmax, rng, node_cap, ncl, pf, log)
            M = len(words)
            log(f"  round {r}: M={M} gain={gain} applied={napp} best={max(best, M)} t={time.time()-t0:.0f}s")
            if M > best:
                best = M
                np.save(bestf, words)
            np.save(cur, words)
            r += 1
            rec = dict(tag=tag, file=f, n=n, d=d, w=w, M0=M0, M=M, best=best, rounds=r,
                       spent=spent + time.time() - t0, last=stats)
            json.dump(rec, open(statf, "w"))
            if mode == "screen":
                break
            if time.time() - t0 + spent > per_seed or time.time() - T0 > total:
                break
            if stats["improving"] == 0 and stats["plateau"] == 0 and gain == 0:
                log("  frozen (no improving and no plateau move): stop this seed")
                break
        log(f"== end {tag}: M0={M0} best={best} rounds={r}")
    log("done")


if __name__ == "__main__":
    main()
