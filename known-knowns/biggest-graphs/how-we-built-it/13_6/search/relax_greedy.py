#!/usr/bin/env python3
"""Maximise the number of viol<=1 extras (each extra element shares a constraint with <= 1 cut element; <= 2 cut elements
per constraint) by randomized min-conflict greedy restarts. Writes the best extended set as JSON.

Elements are points (constraints = lines) for side 'points', and lines (constraints = points) for side 'lines', of the
H(9) incidence graph read from block 0 of Rajiv's (13,6) edge file. The random generator is numpy default_rng(7).

usage: relax_greedy.py points|lines BASE.json OUT.json RESTARTS [--rajiv graph_d13_k6_n534234.edges.xz]
"""
import argparse, os, sys, json, numpy as np, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from compound import read_all, block0  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('side', choices=['points', 'lines']); ap.add_argument('base_json'); ap.add_argument('out')
ap.add_argument('restarts', type=int)
ap.add_argument('--rajiv', default=os.path.join('rajiv', 'graph_d13_k6_n534234.edges.xz'),
                help="Rajiv's (13,6) edge file (Zenodo 10.5281/zenodo.23052995)")
a = ap.parse_args()
side, base_json, out, restarts = a.side, a.base_json, a.out, a.restarts
q = 9; P = (q ** 6 - 1) // (q - 1); B = 8 * P
n0, R = read_all(a.rajiv)
Cr = R[(R[:, 0] < B) & (R[:, 1] < B)]
_, pt_lines, _ = block0(Cr, P)
ln_pts = np.zeros((P, q + 1), np.int64); o = np.argsort(pt_lines.ravel(), kind='stable')
ln_pts[:] = (np.repeat(np.arange(P), q + 1)[o]).reshape(P, q + 1)
el_c, c_el = (pt_lines, ln_pts) if side == 'points' else (ln_pts, pt_lines)
S = np.array(json.load(open(base_json))['set'], np.int64)
cnt0 = np.bincount(el_c[S].ravel(), minlength=P)
inS0 = np.zeros(P, bool); inS0[S] = True
rng = np.random.default_rng(7); best = None; t0 = time.time()
for r in range(restarts):
    cnt = cnt0.copy(); inS = inS0.copy(); extra = []
    while True:
        nviol = (cnt[el_c] > 0).sum(axis=1); full = (cnt[el_c] >= 2).any(axis=1)
        cand = np.where((~inS) & (nviol <= 1) & (~full))[0]
        if not len(cand): break
        if r == 0:
            z = int(rng.choice(cand))
        else:
            # min-conflict: score = number of other candidates on z's constraints (sample for speed)
            sub = rng.choice(cand, size=min(len(cand), 64), replace=False)
            iscand = np.zeros(P, bool); iscand[cand] = True
            sc = np.array([iscand[c_el[el_c[z]].ravel()].sum() for z in sub]) + 0.5 * rng.random(len(sub))
            z = int(sub[np.argmin(sc)])
        extra.append(z); inS[z] = True; cnt[el_c[z]] += 1
    if best is None or len(extra) > len(best):
        best = list(extra)
    print(f"restart {r}: extras {len(extra)} (best {len(best)}) ({time.time()-t0:.0f}s)", flush=True)
Snew = np.r_[S, np.array(best, np.int64)]
mx = np.bincount(el_c[Snew].ravel(), minlength=P).max()
json.dump({'side': side, 'set': [int(x) for x in Snew], 'extra': [int(x) for x in best], 'base_file': base_json,
           'rule': 'each extra shares a constraint with <= 1 cut element; <= 2 cut elements per constraint', 'max_per_constraint': int(mx)}, open(out, 'w'))
print('wrote', out, len(Snew), 'max per constraint', mx)
