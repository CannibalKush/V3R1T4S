#!/usr/bin/env python
"""
multistart.py -- stage 6: restart-distribution analysis + massive diverse multi-start portfolio on chosen images of a
full-test-set tensor (in the original run: the near-boundary residuals and the near-tie fooled rows of the
Addepalli2022Efficient_RN18 tensor written by assemble_final.py, implied count 2758).

Why: the warm relax/reset variants of stage 4 were exhausted on these residuals.  The open
question for a FRESH-START multi-start attack is the spread of local-maximum margins across random restarts: if the upper
tail of the restart distribution reaches the incumbent, enough restarts cross the boundary; if every restart ends far below
the incumbent, multi-start is dead.  This script measures that distribution per image (extreme-value view) and keeps the
best feasible point per image; every claimed break is re-verified on CPU float32 (ties = not fooled).

Attack core = APGD (Croce & Hein 2020, arXiv:2003.01690; MIT-licensed reference code fra31/auto-attack) re-implemented
from the autoattack a3922004 attack_single_run
(Linf, momentum 0.75, step 2*eps, checkpoints 0.22N / -0.03N / min 0.06N, oscillation rule rho=0.75, restart-from-best on
step halving), per row, with a per-row loss/target from a disclosed portfolio.  Separately from APGD's own best-loss
bookkeeping we track, for every row, the feasible iterate with the highest untargeted CW margin (best_wrong - true).

Portfolio (round-robin over restarts so every image gets every arm equally):
  cw      untargeted CW margin, uniform start          ce      cross-entropy, uniform start
  dlr     untargeted DLR, uniform start                 dlrt1   targeted DLR on the incumbent's best wrong class
  cwt1    targeted CW margin on incumbent rank 1        cwt2    targeted CW margin on incumbent rank 2
  cwt3    targeted CW margin on incumbent rank 3        cwv     untargeted CW from a random VERTEX start
"""
import argparse, json, os, sys, time

import numpy as np
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rb_common as rb  # noqa: E402
from feasibility import exact_feasible  # noqa: E402

EPS = 8.0 / 255.0
PORTFOLIO = ['cw', 'ce', 'dlr', 'dlrt1', 'cwt1', 'cwt2', 'cwt3', 'cwv']


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def cw_margin(z, y):
    true = z.gather(1, y.view(-1, 1)).squeeze(1)
    other = z.clone()
    other.scatter_(1, y.view(-1, 1), float('-inf'))
    return other.max(1).values - true


def loss_rows(kind, z, y, t):
    """kind: LongTensor code per row: 0 cw, 1 ce, 2 dlr, 3 dlr-t, 4 cw-t (higher = worse for the model)."""
    u = torch.arange(z.shape[0], device=z.device)
    zs, _ = z.sort(dim=1)
    zy = z[u, y]
    out = torch.zeros(z.shape[0], device=z.device, dtype=z.dtype)
    m = kind == 0
    if m.any():
        out = torch.where(m, cw_margin(z, y), out)
    m = kind == 1
    if m.any():
        out = torch.where(m, F.cross_entropy(z, y, reduction='none'), out)
    m = kind == 2
    if m.any():
        top = zs[:, -1]
        second = zs[:, -2]
        is_top = (z.argmax(1) == y).to(z.dtype)
        dlr = -(zy - second * is_top - top * (1. - is_top)) / (zs[:, -1] - zs[:, -3] + 1e-12)
        out = torch.where(m, dlr, out)
    m = kind == 3
    if m.any():
        dlrt = -(zy - z[u, t]) / (zs[:, -1] - .5 * (zs[:, -3] + zs[:, -4]) + 1e-12)
        out = torch.where(m, dlrt, out)
    m = kind == 4
    if m.any():
        out = torch.where(m, z[u, t] - zy, out)
    return out


def apgd_rows(model, x, y, kind, t, start, n_iter, gen):
    """Per-row APGD (Linf). Returns (x_cwbest, m_cwbest) = feasible iterate with the best untargeted CW margin."""
    B = x.shape[0]
    lo = (x - EPS).clamp(0, 1)
    hi = (x + EPS).clamp(0, 1)
    nd = x.dim() - 1

    def proj(v):
        return torch.min(torch.max(v, lo), hi)

    tt = torch.rand(x.shape, generator=gen, device=x.device) * 2 - 1
    is_vertex = (start == 1).view(-1, *([1] * nd))
    unif = x + EPS * tt / tt.abs().flatten(1).max(1).values.view(-1, *([1] * nd))
    vert = x + EPS * torch.sign(tt)
    xa = proj(torch.where(is_vertex, vert, unif))

    n2 = max(int(0.22 * n_iter), 1)
    nmin = max(int(0.06 * n_iter), 1)
    sdec = max(int(0.03 * n_iter), 1)

    xa.requires_grad_(True)
    z = model(xa)
    li = loss_rows(kind, z, y, t)
    g, = torch.autograd.grad(li.sum(), xa)
    xa = xa.detach()
    with torch.no_grad():
        m = cw_margin(z.detach(), y)
    x_cw = xa.clone(); m_cw = m.clone()
    x_best = xa.clone(); g_best = g.clone(); l_best = li.detach().clone()
    step = 2.0 * EPS * torch.ones(B, *([1] * nd), device=x.device)
    x_old = xa.clone()
    k = n2; counter3 = 0
    l_best_last = l_best.clone()
    reduced_last = torch.ones_like(l_best)
    loss_steps = torch.zeros(n_iter, B, device=x.device)
    for i in range(n_iter):
        with torch.no_grad():
            g2 = xa - x_old
            x_old = xa.clone()
            a = 0.75 if i > 0 else 1.0
            x1 = proj(xa + step * torch.sign(g))
            x1 = proj(xa + (x1 - xa) * a + g2 * (1 - a))
            xa = x1
        xa.requires_grad_(True)
        z = model(xa)
        li = loss_rows(kind, z, y, t)
        g, = torch.autograd.grad(li.sum(), xa)
        xa = xa.detach()
        with torch.no_grad():
            zd = z.detach()
            m = cw_margin(zd, y)
            upd = m > m_cw
            if upd.any():
                x_cw[upd] = xa[upd]
                m_cw[upd] = m[upd]
            y1 = li.detach()
            loss_steps[i] = y1
            ind = y1 > l_best
            x_best[ind] = xa[ind]; g_best[ind] = g[ind]; l_best[ind] = y1[ind]
            counter3 += 1
            if counter3 == k:
                tcount = torch.zeros(B, device=x.device)
                for c5 in range(k):
                    if i - c5 - 1 >= 0:
                        tcount += (loss_steps[i - c5] > loss_steps[i - c5 - 1]).float()
                fl_osc = (tcount <= k * 0.75).float()
                fl_noimpr = (1. - reduced_last) * (l_best_last >= l_best).float()
                fl_osc = torch.max(fl_osc, fl_noimpr)
                reduced_last = fl_osc.clone()
                l_best_last = l_best.clone()
                if fl_osc.sum() > 0:
                    ii = fl_osc > 0
                    step[ii] /= 2.0
                    xa[ii] = x_best[ii]
                    g[ii] = g_best[ii]
                k = max(k - sdec, nmin)
                counter3 = 0
    return x_cw, m_cw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='Addepalli2022Efficient_RN18')
    ap.add_argument('--x_ref', required=True, help='incumbent full-test-set tensor (the targets of the targeted arms are '
                    'the incumbent rows\' top wrong classes)')
    ap.add_argument('--m_ref', required=True, help='its row CPU margins (selects images when --idx is not given; '
                    'otherwise only logged)')
    ap.add_argument('--n_images', type=int, default=10, help='closest residuals (CPU margin <= 0, nearest first)')
    ap.add_argument('--skip', type=int, default=0, help='skip the first N closest residuals')
    ap.add_argument('--idx', default='', help='explicit comma-separated test indices (overrides n_images/skip)')
    ap.add_argument('--restarts', type=int, default=64)
    ap.add_argument('--arms', default=','.join(PORTFOLIO))
    ap.add_argument('--n_iter', type=int, default=100)
    ap.add_argument('--batch', type=int, default=160)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--device', default='mps')
    ap.add_argument('--threads', type=int, default=4)
    ap.add_argument('--out', required=True)
    rb.add_common_args(ap)
    a = ap.parse_args()
    rb.configure(a.data_dir, a.model_dir, a.n_test)

    torch.set_num_threads(a.threads)
    os.makedirs(a.out, exist_ok=True)
    logf = open(os.path.join(a.out, 'log.txt'), 'a')

    def log(s):
        s = f'[{now()}] {s}'
        print(s, flush=True); logf.write(s + '\n'); logf.flush()

    dev = rb.pick_device(a.device)
    x_all, y_all, hx = rb.load_cifar100_test()
    xr = np.load(a.x_ref, mmap_mode='r')
    mr = np.load(a.m_ref)[:x_all.shape[0]]
    if a.idx:
        idx = np.array([int(v) for v in a.idx.split(',')], dtype=np.int64)
    else:
        res = np.where(mr <= 0)[0]
        res = res[np.argsort(-mr[res], kind='stable')]   # closest to the boundary first
        idx = res[a.skip:a.skip + a.n_images]
    log(f'start model {a.model} device {dev} test sha {hx[:16]} images {idx.tolist()} '
        f'ref margins {[round(float(mr[i]), 5) for i in idx]} restarts {a.restarts} arms {a.arms} n_iter {a.n_iter}')
    model, wpath, wsha = rb.load_rb_model(a.model, dev)
    model_cpu, _, _ = rb.load_rb_model(a.model, 'cpu')
    log(f'weights sha256 {wsha}')

    x_img = x_all[idx]; y_img = y_all[idx]
    x_inc = torch.from_numpy(np.ascontiguousarray(xr[idx]))
    with torch.no_grad():
        z_inc = rb.logits(model_cpu, x_inc, 250, 'cpu')
    m_inc = rb.margin(z_inc, y_img)
    zz = z_inc.clone(); zz.scatter_(1, y_img.view(-1, 1), float('-inf'))
    ranks = zz.argsort(1, descending=True)[:, :3]          # incumbent's wrong classes by logit
    log(f'incumbent CPU margins {[round(float(v), 5) for v in m_inc]} (ref file {[round(float(mr[i]), 5) for i in idx]}); '
        f'incumbent top-3 wrong classes {ranks.tolist()}')

    arms = a.arms.split(',')
    assert a.restarts >= len(arms), '--restarts must be >= the number of arms (restarts are dealt round-robin to the arms)'
    code = {'cw': (0, 0, 0), 'ce': (1, 0, 0), 'dlr': (2, 0, 0), 'dlrt1': (3, 0, 0), 'cwt1': (4, 0, 0),
            'cwt2': (4, 1, 0), 'cwt3': (4, 2, 0), 'cwv': (0, 0, 1)}
    rows = []   # (image j, restart r, arm)
    for r in range(a.restarts):
        arm = arms[r % len(arms)]
        for j in range(len(idx)):
            rows.append((j, r, arm))
    n = len(rows)
    J = torch.tensor([rw[0] for rw in rows])
    kind = torch.tensor([code[rw[2]][0] for rw in rows])
    trank = torch.tensor([code[rw[2]][1] for rw in rows])
    start = torch.tensor([code[rw[2]][2] for rw in rows])
    tgt = ranks[J, trank]
    m_end = np.full(n, np.nan, dtype=np.float32)
    x_end = np.zeros((n,) + tuple(x_img.shape[1:]), dtype=np.float32)   # every restart's best-CW feasible point
    best_m = np.full(len(idx), -np.inf, dtype=np.float32)
    best_x = x_inc.numpy().copy()
    gen = torch.Generator(device=dev); gen.manual_seed(a.seed)
    t0 = time.time()
    for s in range(0, n, a.batch):
        sl = slice(s, min(s + a.batch, n))
        jj = J[sl]
        xd = x_img[jj].to(dev); yd = y_img[jj].to(dev)
        xc, mc = apgd_rows(model, xd, yd, kind[sl].to(dev), tgt[sl].to(dev), start[sl].to(dev), a.n_iter, gen)
        mc = mc.cpu().numpy(); xc = xc.cpu().numpy()
        m_end[sl] = mc
        x_end[sl] = xc
        for q, j in enumerate(jj.tolist()):
            if mc[q] > best_m[j]:
                best_m[j] = mc[q]; best_x[j] = xc[q]
        if dev.type == 'mps':
            torch.mps.empty_cache()
        done = sl.stop
        log(f'  rows {s}-{done}/{n}: device max end-margin {np.nanmax(mc):+.4f}  ({time.time() - t0:.0f}s, '
            f'{done * a.n_iter / (time.time() - t0):.0f} image-steps/s)')
        np.save(os.path.join(a.out, 'm_end.npy'), m_end)
    # CPU verification of the per-image best points (float64 feasibility after a one-ulp nudge loop)
    x64 = x_img.numpy().astype(np.float64)
    xb = exact_feasible(best_x.astype(np.float32), x_img.numpy())   # exact float64 feasibility (feasibility.py)
    linf = np.abs(xb.astype(np.float64) - x64).reshape(len(idx), -1).max(1)
    with torch.no_grad():
        zc = rb.logits(model_cpu, torch.from_numpy(xb), 250, 'cpu')
    mc_cpu = rb.margin(zc, y_img).numpy()
    summary = {'time_utc': now(), 'model': a.model, 'weights_sha256': wsha, 'idx': idx.tolist(),
               'restarts': a.restarts, 'arms': arms, 'n_iter': a.n_iter, 'seed': a.seed,
               'image_steps': int(n * a.n_iter), 'wall_s': round(time.time() - t0, 1), 'per_image': []}
    for j, i in enumerate(idx.tolist()):
        me = m_end[J.numpy() == j]
        per_arm = {}
        for arm in arms:
            sel = np.array([(rw[0] == j and rw[2] == arm) for rw in rows])
            v = m_end[sel]
            per_arm[arm] = {'n': int(len(v)), 'max': float(np.max(v)), 'mean': float(np.mean(v))}
        summary['per_image'].append({
            'idx': i, 'y': int(y_img[j]), 'inc_margin_cpu': float(m_inc[j]),
            'restart_max_dev': float(np.max(me)), 'restart_mean_dev': float(np.mean(me)), 'restart_sd_dev': float(np.std(me)),
            'restart_q90_dev': float(np.quantile(me, 0.9)),
            'gap_best_minus_inc': float(np.max(me) - float(m_inc[j])),
            'n_within_0.01_of_inc': int((me >= float(m_inc[j]) - 0.01).sum()),
            'best_cpu_margin': float(mc_cpu[j]), 'best_linf_f64': float(linf[j]), 'fooled_cpu': bool(mc_cpu[j] > 0),
            'per_arm': per_arm})
        log(f'IMG {i}: inc {float(m_inc[j]):+.5f} | restarts max {np.max(me):+.5f} mean {np.mean(me):+.4f} sd {np.std(me):.4f} '
            f'q90 {np.quantile(me, 0.9):+.4f} | best CPU {mc_cpu[j]:+.5f} linf {linf[j]:.10f} '
            f'| arms max: ' + ' '.join(f'{k}:{v["max"]:+.4f}' for k, v in per_arm.items()))
    fooled = [i for j, i in enumerate(idx.tolist()) if mc_cpu[j] > 0]
    summary['fooled_cpu_idx'] = fooled
    json.dump(summary, open(os.path.join(a.out, 'summary.json'), 'w'), indent=1)
    np.save(os.path.join(a.out, 'best_x.npy'), xb)
    np.save(os.path.join(a.out, 'best_cpu_margin.npy'), mc_cpu)
    np.save(os.path.join(a.out, 'idx.npy'), idx)
    np.save(os.path.join(a.out, 'x_end.npy'), x_end)
    np.save(os.path.join(a.out, 'rows_img.npy'), J.numpy())
    log(f'DONE: CPU-fooled {len(fooled)}/{len(idx)} {fooled}; wall {time.time() - t0:.0f}s')


if __name__ == '__main__':
    main()
