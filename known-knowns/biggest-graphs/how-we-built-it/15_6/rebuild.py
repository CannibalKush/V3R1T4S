#!/usr/bin/env python3
"""Deterministic rebuild of a relaxed-Y compound-surgery graph from its certificate:
   Rajiv's published graph (Zenodo 23052995; sha256 of the decompressed file checked against his witness)
   + cut sets (cutsets.py JSONs, or Rajiv's own) + t + seed  --compound.py-->  base graph
   + shortcut edges (assign_generic .shortcuts.npy, and optionally reattach moves already folded into an edge diff)
Writes OUT (plain 'u v', sorted) and prints its sha256.

Usage: rebuild.py --rajiv graph.edges.xz --witness cs.json [--sp SP.json] [--sl SL.json] --t T --seed s
                  --shortcuts SC.npy [--diff_add add.txt --diff_del del.txt] --out OUT.edges
"""
import argparse, hashlib, json, lzma, os, subprocess, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rajiv', required=True); ap.add_argument('--witness', required=True)
    ap.add_argument('--sp'); ap.add_argument('--sl'); ap.add_argument('--t', type=int, required=True)
    ap.add_argument('--seed', type=int, required=True); ap.add_argument('--shortcuts', required=True)
    ap.add_argument('--diff_add'); ap.add_argument('--diff_del')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    W = json.load(open(a.witness))
    raw = lzma.open(a.rajiv, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == W['edges_sha256'], f'Rajiv file sha {sha} != witness {W["edges_sha256"]}'
    print(f'Rajiv decompressed sha256 {sha} matches witness', flush=True)
    del raw
    base_out = a.out + '.base.edges'
    cmd = [sys.executable, os.path.join(HERE, 'compound.py'), '--rajiv', a.rajiv, '--witness', a.witness,
           '--t', str(a.t), '--seed', str(a.seed), '--out', base_out]
    if a.sp: cmd += ['--sp', a.sp]
    if a.sl: cmd += ['--sl', a.sl]
    subprocess.run(cmd, check=True)
    E = pd.read_csv(base_out, sep=r'\s+', header=None, dtype=np.int64).values
    S = np.load(a.shortcuts).astype(np.int64).reshape(-1, 2)
    E = np.concatenate([E, S], 0)
    N = int(E.max()) + 1
    E = np.sort(E, 1)
    if a.diff_del:
        Dl = np.sort(pd.read_csv(a.diff_del, sep=r'\s+', header=None, dtype=np.int64).values, 1)
        k = E[:, 0] * N + E[:, 1]; kd = Dl[:, 0] * N + Dl[:, 1]
        assert np.isin(kd, k).all(); E = E[~np.isin(k, kd)]
    if a.diff_add:
        Da = np.sort(pd.read_csv(a.diff_add, sep=r'\s+', header=None, dtype=np.int64).values, 1)
        E = np.concatenate([E, Da], 0)
    k = E[:, 0] * N + E[:, 1]
    assert len(np.unique(k)) == len(k) and (E[:, 0] != E[:, 1]).all()
    o = np.lexsort((E[:, 1], E[:, 0])); E = E[o]
    pd.DataFrame(E).to_csv(a.out, sep=' ', header=False, index=False)
    os.remove(base_out)
    print(f'rebuilt N={N} m={len(E)} maxdeg={np.bincount(E.ravel()).max()} sha256 '
          f'{hashlib.sha256(open(a.out, "rb").read()).hexdigest()}')


if __name__ == '__main__':
    main()
