#!/usr/bin/env python
"""
stage1_apgdce.py -- stage 1: APGD-CE (100 steps, random start, 1 restart) on every clean-correct CIFAR-100 test image of
a RobustBench model, with per-batch checkpoints (resumable), float64 projection, CPU re-verification and a survivors list.

Deviation from AutoAttack's APGD-CE: every 10 steps the rows whose on-device margin already exceeds 1e-2 are frozen
(their best-margin iterate is kept) and dropped from the batch, which saves ~40% of the gradient budget without changing
the outcome for any image that AutoAttack would have fooled at that point.  The best-MARGIN iterate is returned (not the
first misclassified one), which can only help under the ties-are-robust rule.

  python stage1_apgdce.py --model Addepalli2022Efficient_RN18 --data_dir DATA --model_dir MODELS --ckpt S1/ckpt --out S1/out
Outputs in --out: x_adv_stage1.npy, stage1_cpu_margin.npy, stage1_survivors.npy, clean_correct.npy, manifest.
"""
import argparse, json, os, sys, time

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rb_common as rb  # noqa: E402
import apgd_lib as A  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='Addepalli2022Efficient_RN18')
    ap.add_argument('--clean_acc', type=float, default=65.45, help='RobustBench model_info clean_acc (gate on the full set)')
    ap.add_argument('--steps', type=int, default=100)
    ap.add_argument('--batch', type=int, default=500)
    ap.add_argument('--drop_every', type=int, default=10)
    ap.add_argument('--drop_margin', type=float, default=1e-2)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--device', default='mps')
    ap.add_argument('--threads', type=int, default=4)
    ap.add_argument('--n', type=int, default=10000, help='debug: only first n test images are attacked')
    ap.add_argument('--ckpt', required=True)
    ap.add_argument('--out', required=True)
    rb.add_common_args(ap)
    a = ap.parse_args()
    rb.configure(a.data_dir, a.model_dir, a.n_test)
    torch.set_num_threads(a.threads)
    os.makedirs(a.ckpt, exist_ok=True); os.makedirs(a.out, exist_ok=True)
    dev = rb.pick_device(a.device)
    T0 = time.time()

    x, y, hx = rb.load_cifar100_test()
    N = x.shape[0]
    model_cpu, wpath, wsha = rb.load_rb_model(a.model, 'cpu')
    print(f'[stage1] model {a.model} weights sha256 {wsha} test-set sha256 {hx} device {dev}', flush=True)
    clean_acc, correct = rb.clean_gate(model_cpu, x, y, a.clean_acc)
    model = rb.load_rb_model(a.model, dev)[0] if dev.type != 'cpu' else model_cpu

    idx_all = torch.nonzero(correct[:a.n]).squeeze(1)
    state_p = os.path.join(a.ckpt, 'state.json')
    state = json.load(open(state_p)) if os.path.exists(state_p) else {'done_batches': [], 'batch_secs': {}}
    nb = (idx_all.numel() + a.batch - 1) // a.batch
    t_attack = 0.0
    for b in range(nb):
        bp = os.path.join(a.ckpt, f'batch_{b:03d}.npy')
        if b in state['done_batches'] and os.path.exists(bp):
            continue
        bi = idx_all[b * a.batch:(b + 1) * a.batch]
        t0 = time.time()
        arm = A.ArmBatch(model, x[bi], y[bi], y[bi], torch.full((bi.numel(),), A.LOSS_IDS['ce']), horizon=a.steps,
                         start='rand', seed=a.seed * 100000 + b, device=dev)
        out = torch.empty_like(x[bi])
        out_margin = torch.full((bi.numel(),), float('nan'))
        alive = torch.arange(bi.numel())  # positions within the batch
        steps_done = 0
        while steps_done < a.steps and alive.numel() > 0:
            arm.step(a.drop_every)
            steps_done += a.drop_every
            mb = arm.margin_best.cpu()
            fooled = mb > a.drop_margin
            if steps_done >= a.steps:
                fooled = torch.ones_like(fooled)
            if fooled.any():
                pos = alive[fooled]
                out[pos] = arm.x_best_margin[fooled].cpu()
                out_margin[pos] = mb[fooled]
            keep = ~fooled
            alive = alive[keep]
            if alive.numel() > 0 and steps_done < a.steps:
                arm = arm.select(torch.nonzero(keep).squeeze(1))
        dt = time.time() - t0
        t_attack += dt
        np.save(bp, out.numpy().astype(np.float32))
        np.save(os.path.join(a.ckpt, f'batch_{b:03d}_idx.npy'), bi.numpy())
        np.save(os.path.join(a.ckpt, f'batch_{b:03d}_devmargin.npy'), out_margin.numpy().astype(np.float32))
        state['done_batches'].append(b); state['batch_secs'][str(b)] = round(dt, 1)
        json.dump(state, open(state_p, 'w'))
        print(f'[stage1] batch {b+1}/{nb}: device-fooled {(out_margin > 0).sum().item()}/{bi.numel()}  {dt:.0f}s  '
              f'(total {time.time()-T0:.0f}s)', flush=True)

    # ---- assemble, project in float64, CPU verify
    x_adv = x.clone()
    for b in range(nb):
        bi = torch.from_numpy(np.load(os.path.join(a.ckpt, f'batch_{b:03d}_idx.npy')))
        xb = torch.from_numpy(np.load(os.path.join(a.ckpt, f'batch_{b:03d}.npy')))
        x_adv[bi] = A.project64(xb, x[bi])
    d, ev, rv = rb.eps_check_float64(x_adv, x)
    t0 = time.time()
    mg = A.cpu_margins(model_cpu, x_adv, y)
    not_fooled = mg <= 0
    n_robust = int(not_fooled.sum())
    # survivors for stage 2: clean-correct images not fooled on CPU, plus weakly fooled ones (margin < 1e-3) to polish
    surv = torch.nonzero(correct & (mg < 1e-3)).squeeze(1)
    print(f'[stage1] CPU verify {time.time()-t0:.0f}s: robust {n_robust}/{N} = {100.0 * n_robust / N:.2f}%  '
          f'(clean {int(correct.sum())})  weak(0<m<1e-3) {int(((mg > 0) & (mg < 1e-3)).sum())}  '
          f'survivors-for-stage2 {surv.numel()}  max Linf {d.max():.9f} eps_viol {ev} range_viol {rv}', flush=True)
    xp = os.path.join(a.out, 'x_adv_stage1.npy')
    np.save(xp, x_adv.numpy().astype(np.float32))
    np.save(os.path.join(a.out, 'stage1_cpu_margin.npy'), mg.numpy().astype(np.float32))
    np.save(os.path.join(a.out, 'stage1_survivors.npy'), surv.numpy())
    np.save(os.path.join(a.out, 'clean_correct.npy'), correct.numpy())
    rb.write_manifest(os.path.join(a.out, 'x_adv_stage1.manifest.json'), model=a.model,
                      weights_sha256=wsha, test_images_sha256=hx, x_adv_sha256=rb.sha256_file(xp), n_images=N,
                      method=f'APGD-CE {a.steps} steps, 1 random start (seed {a.seed}), momentum 0.75, step 2eps with '
                             f'APGD checkpoint halving; rows frozen when device margin > {a.drop_margin} (checked every '
                             f'{a.drop_every} steps); best-margin iterate kept; float64 final projection',
                      device=str(dev), attack_seconds=round(t_attack, 1), total_seconds=round(time.time() - T0, 1),
                      robust_count_cpu=n_robust, clean_acc=clean_acc, max_linf=float(d.max()),
                      eps_violations=ev, range_violations=rv, n_survivors_stage2=int(surv.numel()))
    print('[stage1] DONE wrote', xp, flush=True)


if __name__ == '__main__':
    main()
