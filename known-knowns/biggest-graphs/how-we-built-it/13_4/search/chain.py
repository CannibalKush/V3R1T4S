#!/usr/bin/env python3
"""
Chained +1 insertions with edge pruning and near-miss saving (the (13,4) search engine).

One chain per spec entry (several chains can run in a process pool). Each chain:
  * loads its start graph (ddlib.load_graph, i.e. sorted edge list), checks it is valid, and prunes redundant edges
    (prune.py: delete an edge if the diameter stays <= D; edges tried in a random order from default_rng(seed0));
  * repeatedly: s += 1; insert one vertex with the 'slack' warm start (insert.py, rng default_rng(s)) and repair with
    the screened annealing sa2.sa2_run (seed s, `iters` iterations, temperature T0 -> T1, p_target 0.6, p_free 0.2);
      - if the cost reaches 0: re-verify with scipy, write OUT/valid_<tag>_<Delta>_<D>_N<n>.edges, prune again
        (order from default_rng(s)), write OUT/valid_..._pruned.edges and continue from the pruned graph;
      - otherwise write the best state as OUT/near_<tag>_N<n>_s<s>_c<cost>.edges (a "near-miss" with `cost` unordered
        pairs at distance > D; inputs for sa2_resume.py) and count a failure;
  * stops after `retries` consecutive failures.
The chain keeps the current graph in memory between steps; the pruned files are written in that in-memory order, so
chain_step.py can replay any single attempt from them. A checkpoint OUT/ckpt_<tag>.json makes the chain resumable;
delete OUT (or the checkpoint) for a fresh run, otherwise it continues from the checkpoint.

usage: chain.py --spec SPEC.json --out DIR [--procs P]
SPEC: list of {"seed": start graph path, "delta": int, "diam": int, "tag": str, "iters": float, "retries": int,
               "seed0": int, "T0": float (default 0.6), "T1": float (default 0.05), "prune": bool (default true)}
"""
import os, sys, time, json, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ddlib import load_graph, edges_to_adj, adj_to_edges, write_edges, exact_cost
from sa2 import sa2_run
from insert import initial_insert, verify_independent
from prune import prune


def chain(spec, out):
    tag = spec['tag']; Delta = spec['delta']; D = spec['diam']
    iters = spec.get('iters', 2e5); retries = spec.get('retries', 10); T0 = spec.get('T0', 0.6); T1 = spec.get('T1', 0.05)
    log = open(os.path.join(out, f'chain_{tag}.log'), 'a')
    ck = os.path.join(out, f'ckpt_{tag}.json')
    cur = spec['seed']; s = spec.get('seed0', 1000)
    if os.path.exists(ck):
        st = json.load(open(ck)); cur = st['current']; s = st.get('s', s)
    N, E = load_graph(cur)
    adj0, deg0 = edges_to_adj(N, E, Delta)
    c, _ = exact_cost(adj0, deg0, N, D)
    assert c == 0, f"start graph invalid ({c})"
    print(f"[{tag}] start N={N} free={Delta*N-int(deg0.sum())} from {cur}", file=log, flush=True)
    if spec.get('prune', True):
        perm = np.random.default_rng(s).permutation(len(E))
        rem = prune(adj0, deg0, N, D, E[perm, 0].astype(np.int64), E[perm, 1].astype(np.int64))
        E = adj_to_edges(adj0, deg0)
        print(f"[{tag}] pruned {rem} edges at start -> free={Delta*N-int(deg0.sum())}", file=log, flush=True)
    fails = 0
    while fails < retries:
        s += 1
        t0 = time.time()
        n, adj, deg = initial_insert(N, E, Delta, D, 1, 'slack', np.random.default_rng(s))
        c0, _ = exact_cost(adj, deg, n, D)
        best, badj, bdeg, acc, nfull, nscr = sa2_run(adj, deg, n, D, Delta, int(iters), T0, T1, s, 0.6, 0.0, 0.2, int(1e12), 0)
        print(f"[{tag}] N->{n} seed {s}: init {c0} best {best} acc {acc} full {nfull} screened {nscr} {time.time()-t0:.0f}s",
              file=log, flush=True)
        if best == 0:
            E2 = adj_to_edges(badj, bdeg)
            diam, dmax, dmin = verify_independent(n, E2, Delta, D)
            if diam <= D and dmax <= Delta:
                fn = os.path.join(out, f"valid_{tag}_{Delta}_{D}_N{n}.edges")
                write_edges(fn, E2, header=f"({Delta},{D}) graph N={n} diam={diam} maxdeg={dmax}; chain {tag} seed {s}")
                print(f"[{tag}] VALID N={n} diam={diam} maxdeg={dmax} free={Delta*n-int(bdeg.sum())} -> {fn}", file=log, flush=True)
                N, E = n, E2
                cur = fn
                if spec.get('prune', True):
                    a2, d2 = edges_to_adj(N, E, Delta)
                    perm = np.random.default_rng(s).permutation(len(E))
                    rem = prune(a2, d2, N, D, E[perm, 0].astype(np.int64), E[perm, 1].astype(np.int64))
                    E = adj_to_edges(a2, d2)
                    c2, _ = exact_cost(a2, d2, N, D)
                    assert c2 == 0
                    fnp = fn.replace('.edges', '_pruned.edges')
                    write_edges(fnp, E, header=f"({Delta},{D}) graph N={N}, pruned {rem} redundant edges; chain {tag}")
                    cur = fnp
                    print(f"[{tag}] pruned {rem} edges -> free={Delta*N-int(d2.sum())}", file=log, flush=True)
                json.dump({'current': cur, 'N': n, 's': s, 'time': time.strftime('%Y-%m-%dT%H:%M:%S')}, open(ck, 'w'))
                fails = 0
                continue
        # near-miss saving
        E2 = adj_to_edges(badj, bdeg)
        fn = os.path.join(out, f"near_{tag}_N{n}_s{s}_c{best}.edges")
        write_edges(fn, E2, header=f"near-miss ({Delta},{D}) N={n} cost={best} (unordered pairs at distance > D); chain {tag} seed {s}; parent {cur}")
        with open(os.path.join(out, 'near_index.jsonl'), 'a') as f:
            f.write(json.dumps({'tag': tag, 'N': n, 'Delta': Delta, 'D': D, 'cost': int(best), 'file': fn, 'parent': cur,
                                'seed': s, 'time': time.strftime('%Y-%m-%dT%H:%M:%S')}) + '\n')
        fails += 1
        json.dump({'current': cur, 'N': N, 's': s, 'time': time.strftime('%Y-%m-%dT%H:%M:%S')}, open(ck, 'w'))
    print(f"[{tag}] STUCK at N={N} after {retries} consecutive failures", file=log, flush=True)
    return tag, N


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--spec', required=True); ap.add_argument('--out', required=True); ap.add_argument('--procs', type=int, default=1)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    specs = json.load(open(a.spec))
    if a.procs > 1:
        import multiprocessing as mp
        with mp.get_context('fork').Pool(a.procs) as pool:
            for r in pool.starmap(chain, [(sp, a.out) for sp in specs]):
                print(r, flush=True)
    else:
        for sp in specs:
            print(chain(sp, a.out), flush=True)
