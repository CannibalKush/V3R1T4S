#!/usr/bin/env python3
"""Replay ONE attempt of chain.py: from the chain's current graph as it held it in memory (a *_pruned.edges file
written by chain.py, read in FILE order) insert one vertex with seed s and anneal exactly as chain.py does
(insert.initial_insert 'slack' with default_rng(s), then sa2.sa2_run with seed s, iters, T0, T1, p_target 0.6,
p_free 0.2). Writes OUT (same header style as chain.py's near-miss / valid files) and prints the cost.

Example, the (13,4) near-miss (attempt 13064 of chain c134 from the pruned 6629-vertex graph):
  chain_step.py valid_c134_13_4_N6629_pruned.edges --delta 13 --diam 4 --seed 13064 --iters 2e5 --T0 0.6 \
                --out near_c134_N6630_s13064.edges        # cost 2 (init 126)
"""
import os, sys, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ddlib import load_edges_file_order, adj_to_edges, write_edges, exact_cost
from sa2 import sa2_run
from insert import initial_insert

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('graph'); ap.add_argument('--delta', type=int, required=True); ap.add_argument('--diam', type=int, required=True)
ap.add_argument('--seed', type=int, required=True); ap.add_argument('--iters', type=float, default=2e5)
ap.add_argument('--T0', type=float, default=0.6); ap.add_argument('--T1', type=float, default=0.05)
ap.add_argument('--out', required=True)
a = ap.parse_args()
Delta, D, s = a.delta, a.diam, a.seed
N, E = load_edges_file_order(a.graph)
t0 = time.time()
n, adj, deg = initial_insert(N, E, Delta, D, 1, 'slack', np.random.default_rng(s))
c0, _ = exact_cost(adj, deg, n, D)
best, badj, bdeg, acc, nfull, nscr = sa2_run(adj, deg, n, D, Delta, int(a.iters), a.T0, a.T1, s, 0.6, 0.0, 0.2, int(1e12), 0)
print(f"N->{n} seed {s}: init {c0} best {best} acc {acc} full {nfull} screened {nscr} {time.time()-t0:.0f}s", flush=True)
E2 = adj_to_edges(badj, bdeg)
write_edges(a.out, E2, header=f"({Delta},{D}) N={n} cost={best} (unordered pairs at distance > D); seed {s}; parent {os.path.basename(a.graph)}")
print(f"wrote {a.out}")
