#!/usr/bin/env python3
"""One insertion step: add k vertices to a valid (Delta, D) graph ('slack' warm start, insert.py) and repair it with
the screened simulated annealing sa2.sa2_run. On success writes OUT/sa2hit_<tag>_<Delta>_<D>_N<n>_s<seed>.edges
(re-verified independently with scipy all-pairs BFS); otherwise the best state OUT/sa2best_..._c<cost>.edges.
Prints one JSON line.

(13,4) step 6611 -> 6612 (seed 1, 1e5 iterations):
  insert_step.py G_13_4_n6611_rajiv.edges --delta 13 --diam 4 --k 1 --iters 100000 --T0 0.6 --T1 0.05 --seed 1 \
                 --out OUT --tag t6611
"""
import os, sys, time, json, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ddlib import load_graph, adj_to_edges, write_edges, exact_cost
from sa2 import sa2_run
from insert import initial_insert, verify_independent


def run(fn, Delta, D, k, iters, T0, T1, seed, pt=0.6, pfree=0.2, outdir=None, tag='s2', strategy='slack'):
    N, E = load_graph(fn)
    n, adj, deg = initial_insert(N, E, Delta, D, k, strategy, np.random.default_rng(seed))
    c0, _ = exact_cost(adj, deg, n, D)
    t0 = time.time()
    best, badj, bdeg, acc, nfull, nscreen = sa2_run(adj, deg, n, D, Delta, int(iters), T0, T1, seed, pt, 0.0, pfree, int(1e12), 0)
    dt = time.time() - t0
    cb, _ = exact_cost(badj, bdeg, n, D)
    res = dict(seedfile=os.path.basename(fn), Delta=Delta, D=D, k=k, n=n, seed=seed, init=int(c0), best=int(best),
               best_recheck=int(cb), acc=int(acc), nfull=int(nfull), nscreen=int(nscreen), secs=round(dt, 1),
               free_after=int(Delta * n - bdeg.sum()), iters=iters, T0=T0)
    assert cb == best, f"bookkeeping mismatch {cb} vs {best}"
    if best == 0 and outdir:
        E2 = adj_to_edges(badj, bdeg)
        diam, dmax, dmin = verify_independent(n, E2, Delta, D)
        res.update(verified_diam=diam, maxdeg=dmax)
        f = os.path.join(outdir, f"sa2hit_{tag}_{Delta}_{D}_N{n}_s{seed}.edges")
        write_edges(f, E2, header=f"({Delta},{D}) graph N={n} diam={diam} maxdeg={dmax}; from {os.path.basename(fn)} + {k} inserted (SA2 seed {seed})")
        res['file'] = f
    elif outdir:
        E2 = adj_to_edges(badj, bdeg)
        write_edges(os.path.join(outdir, f"sa2best_{tag}_{Delta}_{D}_N{n}_s{seed}_c{best}.edges"), E2)
    return res


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('graph', help='valid (Delta,D) graph, edge list')
    ap.add_argument('--delta', type=int, required=True); ap.add_argument('--diam', type=int, required=True)
    ap.add_argument('--k', type=int, default=1, help='number of vertices to insert')
    ap.add_argument('--iters', type=float, default=1e5); ap.add_argument('--T0', type=float, default=0.6)
    ap.add_argument('--T1', type=float, default=0.05); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--p-target', type=float, default=0.6); ap.add_argument('--p-free', type=float, default=0.2)
    ap.add_argument('--out', default='.'); ap.add_argument('--tag', default='s2')
    ap.add_argument('--strategy', default='slack', choices=['slack', 'subdiv'])
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    print(json.dumps(run(a.graph, a.delta, a.diam, a.k, a.iters, a.T0, a.T1, a.seed, a.p_target, a.p_free, a.out, a.tag,
                         a.strategy)), flush=True)
