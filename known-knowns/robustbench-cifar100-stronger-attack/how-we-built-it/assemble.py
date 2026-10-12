#!/usr/bin/env python
"""
assemble.py -- stage 6 (merge): merge CPU-verified rows from multistart.py result dirs onto a base full-test-set tensor
(in the original run: the Addepalli2022Efficient_RN18 tensor written by assemble_final.py, implied count 2758), rule:
  * base row robust (CPU margin <= 0) and candidate row CPU margin > 0      -> NEW BREAK, replace
  * base row fooled and candidate CPU margin > base CPU margin               -> INSURANCE (safer margin), replace
Every candidate row is re-checked here: exact float64 feasibility vs the ToTensor x (|x_adv - x| <= 8/255, [0,1]) and a
CPU float32 forward (margin = best_wrong - true > 0 means fooled; ties are robust).  Writes <out>.npy + manifest.
The full 10k recount is done separately (verify-it-yourself/rbcheck.py).

  python assemble.py --base FINAL/x_adv.npy --base_margin FINAL/x_adv_row_cpu_margin.npy --cands DIR1,DIR2 --out OUT.npy
"""
import argparse, hashlib, json, os, sys, time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rb_common as rb  # noqa: E402
from feasibility import exact_feasible  # noqa: E402

EPS = 8.0 / 255.0


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for ch in iter(lambda: f.read(1 << 20), b''):
            h.update(ch)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='Addepalli2022Efficient_RN18')
    ap.add_argument('--base', required=True, help='base full-test-set tensor (.npy)')
    ap.add_argument('--base_margin', required=True, help='its row CPU margins (only used for the implied count)')
    ap.add_argument('--cands', required=True, help='comma list of result dirs, each with idx.npy + best_x.npy|best_rows.npy')
    ap.add_argument('--out', required=True)
    ap.add_argument('--threads', type=int, default=4)
    rb.add_common_args(ap)
    a = ap.parse_args()
    rb.configure(a.data_dir, a.model_dir, a.n_test)
    torch.set_num_threads(a.threads)
    t0 = time.time()
    x_all, y_all, hx = rb.load_cifar100_test()
    N = x_all.shape[0]
    base = np.load(a.base)[:N]
    bm = np.load(a.base_margin)[:N]
    model_cpu, _, wsha = rb.load_rb_model(a.model, 'cpu')
    # recompute base margins of every candidate index (do not trust files)
    cand = {}
    for d in a.cands.split(','):
        idx = np.load(os.path.join(d, 'idx.npy'))
        f = 'best_x.npy' if os.path.isfile(os.path.join(d, 'best_x.npy')) else 'best_rows.npy'
        rows = np.load(os.path.join(d, f))
        for k, i in enumerate(idx.tolist()[:len(rows)]):
            cand.setdefault(i, []).append((d, rows[k]))
    log = []
    out = base.copy()
    for i, lst in sorted(cand.items()):
        xi = x_all[i:i + 1]
        with torch.no_grad():
            m_base = float(rb.margin(rb.logits(model_cpu, torch.from_numpy(base[i:i + 1]), 1, 'cpu'), y_all[i:i + 1])[0])
        best = (None, m_base, None)
        for d, r in lst:
            r = exact_feasible(r[None].astype(np.float32), xi.numpy())
            with torch.no_grad():
                m = float(rb.margin(rb.logits(model_cpu, torch.from_numpy(r), 1, 'cpu'), y_all[i:i + 1])[0])
            if m > best[1]:
                best = (r[0], m, d)
        kind = None
        if best[0] is not None:
            if m_base <= 0 < best[1]:
                kind = 'NEW_BREAK'
            elif m_base > 0:
                kind = 'INSURANCE'
            if kind:
                out[i] = best[0]
        log.append(dict(idx=i, base_margin_cpu=m_base, base_margin_file=float(bm[i]), best_cand_margin_cpu=best[1],
                        source=best[2], action=kind))
        log[-1]['source'] = os.path.basename(os.path.normpath(best[2])) if best[2] else None
        print(f'idx {i}: base {m_base:+.5f} -> best cand {best[1]:+.5f} [{kind}] from {log[-1]["source"]}', flush=True)
    xn = x_all.numpy()
    d64 = np.concatenate([np.abs(out[k:k + 500].astype(np.float64) - xn[k:k + 500].astype(np.float64)).reshape(-1, 3072).max(1)
                          for k in range(0, N, 500)])
    assert (d64 <= EPS).all() and out.min() >= 0 and out.max() <= 1
    np.save(a.out, out)
    implied = int((bm <= 0).sum()) - sum(1 for r in log if r['action'] == 'NEW_BREAK')
    man = dict(time_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), model=a.model, weights_sha256=wsha,
               test_sha256=hx, base_sha256=sha(a.base), out_sha256=sha(a.out),
               base_implied_robust=int((bm <= 0).sum()), new_breaks=[r['idx'] for r in log if r['action'] == 'NEW_BREAK'],
               insurance=[r['idx'] for r in log if r['action'] == 'INSURANCE'], implied_robust=implied,
               max_linf_f64=float(d64.max()), rows=log, secs=round(time.time() - t0, 1))
    json.dump(man, open(a.out.replace('.npy', '') + '.manifest.json', 'w'), indent=1)
    print(json.dumps({k: man[k] for k in ('out_sha256', 'base_implied_robust', 'new_breaks', 'insurance', 'implied_robust',
                                          'max_linf_f64')}, indent=1))


if __name__ == '__main__':
    main()
