#!/usr/bin/env python3
"""relaxed13.py: (13,6) compound surgery with RELAXED cut sets.
Rajiv's Lemma 5 asks the point cut set S_P to be pairwise non-collinear and S_L pairwise non-concurrent. That is
sufficient, not necessary: the base compound cut at S_P + 1 point collinear with a cut point still has diameter 6
(xchk, all pairs). Here: S_P' = S_P + extra points such that every line holds <= maxper cut points and the extra point is
collinear with <= viol cut points (greedy, random order); S_L' dually. Then C''(S_P', S_L') + t = min(|S_P'|,|S_L'|) new
vertices (one point + one line of every block at free slots, random 5-regular Y), exactly as compound.py does. Nothing is
assumed: the final graph is repaired by exact_sc.py (new-new pairs; base pairs if xchk lists any) and checked all-pairs.
usage: relaxed13.py --sp SP.json --sl SL.json --kp K --kl K [--maxper 2] [--viol 1] --seed s [--t T] --out G.edges
                    [--rajiv graph_d13_k6_n534234.edges.xz] [--witness witnesses/cs_d13_k6_n534234.json]
Inputs: Rishabh Rajiv, Zenodo 10.5281/zenodo.23052995 (graph file + witness); compound.py one directory up.
Writes G.edges, G.edges.SP.json and G.edges.SL.json (the cut sets actually used).
"""
import argparse, json, hashlib, os, sys, time
import numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from compound import read_all, block0, compound_edges, random_regular, keys  # noqa: E402


def extend(S, el_c, c_el, P, k, maxper, viol, rng):
    """S: elements (points or lines); el_c[e] = constraints through e; c_el[c] = elements on constraint c."""
    cnt = np.bincount(el_c[S].ravel(), minlength=P)
    inS = np.zeros(P, bool); inS[S] = True
    extra = []
    for z in rng.permutation(P):
        if len(extra) >= k:
            break
        if inS[z]:
            continue
        cs = el_c[z]
        if (cnt[cs] >= maxper).any():
            continue
        if int((cnt[cs] > 0).sum()) > viol:
            continue
        extra.append(int(z)); inS[z] = True; cnt[cs] += 1
    return np.r_[S, np.array(extra, np.int64)], extra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sp', required=True); ap.add_argument('--sl', required=True)
    ap.add_argument('--kp', type=int, default=0); ap.add_argument('--kl', type=int, default=0)
    ap.add_argument('--maxper', type=int, default=2); ap.add_argument('--viol', type=int, default=1)
    ap.add_argument('--t', type=int, default=0); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--out', required=True); ap.add_argument('--base-only', action='store_true')
    ap.add_argument('--rajiv', default=os.path.join('rajiv', 'graph_d13_k6_n534234.edges.xz'))
    ap.add_argument('--witness', default=os.path.join('rajiv', 'witnesses', 'cs_d13_k6_n534234.json'))
    a = ap.parse_args(); t0 = time.time()
    W = json.load(open(a.witness))
    q, m = W['q'], W['m']; P = (q ** 6 - 1) // (q - 1); base = 2 * m * P; Delta = W['d']; r = Delta - 2 * m
    n0, R = read_all(a.rajiv)
    Cr = R[(R[:, 0] < base) & (R[:, 1] < base)]
    _, pt_lines, _ = block0(Cr, P)
    ln_pts = np.zeros((P, q + 1), np.int64); o = np.argsort(pt_lines.ravel(), kind='stable')
    ln_pts[:] = (np.repeat(np.arange(P), q + 1)[o]).reshape(P, q + 1)
    SP = np.array(json.load(open(a.sp))['set'], np.int64); SL = np.array(json.load(open(a.sl))['set'], np.int64)
    rng = np.random.default_rng(a.seed)
    SP2, xp = extend(SP, pt_lines, ln_pts, P, a.kp, a.maxper, a.viol, rng)
    SL2, xl = extend(SL, ln_pts, pt_lines, P, a.kl, a.maxper, a.viol, rng)
    mp = np.bincount(pt_lines[SP2].ravel(), minlength=P).max(); ml = np.bincount(ln_pts[SL2].ravel(), minlength=P).max()
    print(f"S_P {len(SP)} + {len(xp)} = {len(SP2)} (max per line {mp}); S_L {len(SL)} + {len(xl)} = {len(SL2)} (max per point {ml}) ({time.time()-t0:.0f}s)", flush=True)
    json.dump({'side': 'points', 'set': [int(x) for x in SP2], 'extra': xp, 'base_file': a.sp}, open(a.out + '.SP.json', 'w'))
    json.dump({'side': 'lines', 'set': [int(x) for x in SL2], 'extra': xl, 'base_file': a.sl}, open(a.out + '.SL.json', 'w'))
    C = compound_edges(pt_lines, P, m, W['tournament'], W['H'], SP2, SL2)
    if a.base_only:
        C = C[np.lexsort((C[:, 1], C[:, 0]))]
        pd.DataFrame(C).to_csv(a.out, sep=' ', header=False, index=False); print('wrote base', a.out); return
    deg = np.bincount(C.ravel(), minlength=base); defi = Delta - deg
    t = a.t or min(len(SP2), len(SL2))
    newE = []
    for i in range(m):
        for kind, lo in (('P', 2 * i * P), ('L', 2 * i * P + P)):
            idx = np.arange(lo, lo + P); slots = np.repeat(idx, defi[lo:lo + P])
            assert len(slots) >= t, (kind, i, len(slots), t)
            sel = rng.permutation(slots)[:t]
            newE.append(np.stack([base + np.arange(t), sel], 1))
    Y = random_regular(t, r, rng) + base
    E = np.sort(np.concatenate([C] + newE + [Y], 0), 1)
    N = base + t; kk = keys(E, N)
    assert len(np.unique(kk)) == len(kk) and (E[:, 0] != E[:, 1]).all()
    d2 = np.bincount(E.ravel(), minlength=N); assert d2.max() <= Delta
    E = E[np.lexsort((E[:, 1], E[:, 0]))]
    pd.DataFrame(E).to_csv(a.out, sep=' ', header=False, index=False)
    print(f"wrote {a.out} N={N} t={t} M={len(E)} free slots left {int((Delta - d2[:base]).sum())} sha256 {hashlib.sha256(open(a.out,'rb').read()).hexdigest()} ({time.time()-t0:.0f}s)", flush=True)


if __name__ == '__main__':
    main()
