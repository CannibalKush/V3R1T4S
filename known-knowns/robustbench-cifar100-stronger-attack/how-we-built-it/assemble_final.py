#!/usr/bin/env python
"""
assemble_final.py -- stage 5: turn the latest warm_residual.py checkpoint into a full tensor (the base of stage 6).

  1. load <ckpt>/x_adv.npy + m_cpu.npy (row CPU margins maintained by the driver);
  2. SAFETY POLISH: every perturbed (= clean-correct) row that is fooled with a small CPU margin (0 < m < --safe, default 1e-3) gets up to
     3 rounds of 20 small CW sign steps (eps/16, eps/32, eps/64) inside the float32 box on the device; the result is
     projected in float64, re-verified on the CPU float32 model and kept only if its CPU margin increased;
  3. one-ulp nudge toward x until max|x_adv - x| <= 8/255 in float64 against the ToTensor reference; [0,1] clip;
  4. writes OUT (float32 .npy) + OUT.manifest.json (sha256, nudges, feasibility, the polished rows).
The official count is a full CPU checker run (verify-it-yourself/rbcheck.py on the final tensor).

  python assemble_final.py --model Addepalli2022Efficient_RN18 --ckpt C2 --out FINAL/x_adv.npy
"""
import argparse, hashlib, json, os, sys, time

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rb_common as rb  # noqa: E402
from warm_residual import polish_cw  # noqa: E402

EPS = 8.0 / 255.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True)
    ap.add_argument('--ckpt', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--safe', type=float, default=1e-3)
    ap.add_argument('--device', default='mps')
    ap.add_argument('--threads', type=int, default=4)
    rb.add_common_args(ap)
    a = ap.parse_args()
    rb.configure(a.data_dir, a.model_dir, a.n_test)
    torch.set_num_threads(a.threads)
    t0 = time.time()
    dev = rb.pick_device(a.device)
    x, y, hx = rb.load_cifar100_test()
    xa = torch.from_numpy(np.load(os.path.join(a.ckpt, 'x_adv.npy')))
    m = torch.from_numpy(np.load(os.path.join(a.ckpt, 'm_cpu.npy'))).float()
    model_cpu, _, wsha = rb.load_rb_model(a.model, 'cpu')
    model = rb.load_rb_model(a.model, dev)[0] if dev.type != 'cpu' else model_cpu
    N = x.shape[0]
    # perturbed rows (clean-wrong rows carry x_adv = x exactly in every tensor of the pipeline and must stay untouched)
    perturbed = (xa != x).flatten(1).any(1)
    rows = torch.nonzero(perturbed & (m > 0) & (m < a.safe)).squeeze(1)
    pol = []
    if rows.numel():
        xb = x[rows].to(dev); yb = y[rows].to(dev)
        lo, hi = (xb - EPS).clamp(0, 1), (xb + EPS).clamp(0, 1)
        cur = xa[rows].clone()
        mc = rb.margin(rb.logits(model_cpu, cur, 250, 'cpu'), y[rows])
        for stp in (EPS / 16, EPS / 32, EPS / 64):
            xp, _ = polish_cw(model, xb, yb, lo, hi, cur.to(dev), n_steps=20, step=stp)
            xp = xp.cpu().double()
            xp = torch.min(torch.max(xp, x[rows].double() - EPS), x[rows].double() + EPS).clamp(0, 1).float()
            mp = rb.margin(rb.logits(model_cpu, xp, 250, 'cpu'), y[rows])
            better = mp > mc
            cur[better] = xp[better]; mc[better] = mp[better]
        for j, i in enumerate(rows.tolist()):
            pol.append({'idx': int(i), 'm_before': float(m[i]), 'm_after': float(mc[j])})
            if float(mc[j]) > float(m[i]):
                xa[i] = cur[j]; m[i] = mc[j]
    xn = xa.numpy().astype(np.float32)
    x0 = x.numpy()
    n_nudged = 0
    dmax = np.zeros(N)
    for s in range(0, N, 500):
        sl = slice(s, s + 500)
        xs, x0s = xn[sl], x0[sl]
        for _ in range(4):
            over = np.abs(xs.astype(np.float64) - x0s.astype(np.float64)) > EPS
            if not over.any():
                break
            n_nudged += int(over.sum())
            xs[over] = np.nextafter(xs[over], x0s[over]).astype(np.float32)
        np.clip(xs, 0.0, 1.0, out=xs)
        dmax[sl] = np.abs(xs.astype(np.float64) - x0s.astype(np.float64)).reshape(-1, 3072).max(1)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    np.save(a.out, xn)
    np.save(a.out.replace('.npy', '_row_cpu_margin.npy'), m.numpy().astype(np.float32))
    sha = hashlib.sha256(open(a.out, 'rb').read()).hexdigest()
    res = {'time_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'model': a.model, 'weights_sha256': wsha,
           'test_images_sha256': hx, 'sha256': sha,
           'perturbed_rows': int(perturbed.sum()), 'implied_robust_row_margins': int((m <= 0).sum()),
           'safety_polished_rows': pol, 'n_nudged_ulp': n_nudged, 'max_linf_float64': float(dmax.max()),
           'n_over_eps_strict': int((dmax > EPS).sum()), 'n_over_eps_1e-6': int((dmax > EPS + 1e-6).sum()),
           'secs': round(time.time() - t0, 1)}
    json.dump(res, open(a.out + '.manifest.json', 'w'), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
