#!/usr/bin/env python
"""
cr_residual.py -- stage 3: CR Attack (Pan et al., AAAI 2025; the published code adapted by make_cr_attack.py into
cr_attack_vendored.py) on the RESIDUAL set of a verified x_adv tensor -- the clean-correct images that the previous
stages still leave correctly classified -- closest-to-boundary first, as a sequential stage appended to the pipeline:
  * CR is run from the CLEAN image (its own PGD-10 target ranking, fresh uniform starts, relaxed/reset eps schedule),
    i.e. from different start points than the first-order arms that already saturated on this residual set;
  * every device-claimed success is re-verified on the CPU float32 model (ties = not fooled);
    borderline CPU margins get a short small-step CW polish on the device and are re-verified;
  * only CPU-verified successes are committed into the x_adv tensor (float64 projection onto the eps-box);
  * per-unit checkpoints (x_adv.npy + m_cpu.npy + state.json) make the run resumable; --final writes a deliverable
    tensor after a one-ulp nudge so max|x_adv - x| <= 8/255 holds in float64 against the torchvision ToTensor
    reference, and recounts the whole test set on CPU (not used in the original pipeline).

  python make_cr_attack.py      # once: builds cr_attack_vendored.py next to this file
  python cr_residual.py --x_adv_in X --margin_in M --mask_in K --ckpt DIR --max_dist 0.5 --batch 100 --seed 0
"""
import argparse, hashlib, json, os, sys, time

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rb_common as rb                     # noqa: E402  (loaders, CPU verify, float64 checks)
sys.path.insert(0, os.environ.get('CR_ATTACK_DIR', HERE))   # where make_cr_attack.py wrote cr_attack_vendored.py
try:
    from cr_attack_vendored import CRAttack    # noqa: E402
except ImportError:
    raise SystemExit('cr_attack_vendored.py not found: run `python make_cr_attack.py` first (see README.md), or set '
                     'CR_ATTACK_DIR to the directory that holds it')

EPS = 8.0 / 255.0
STOP = 1e-3


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def cw_margin(z, y):
    """best wrong logit - true logit; > 0 means fooled (ties = 0 = not fooled)."""
    true = z.gather(1, y.view(-1, 1)).squeeze(1)
    other = z.clone()
    other.scatter_(1, y.view(-1, 1), float('-inf'))
    return other.max(1).values - true


@torch.no_grad()
def dev_margin(model, xa, y, bs=250):
    out = []
    for i in range(0, xa.shape[0], bs):
        out.append(cw_margin(model(xa[i:i + bs]), y[i:i + bs]))
    return torch.cat(out, 0)


def polish_cw(model, x, y, lo, hi, x0, n_steps=20, step=EPS / 16):
    """small-step signed-gradient ascent on the CW margin inside the box, keeping the best device-margin iterate."""
    xa = x0.clone()
    with torch.no_grad():
        m_best = cw_margin(model(xa), y)
    x_best = xa.clone()
    for _ in range(n_steps):
        xa = xa.detach().requires_grad_(True)
        z = model(xa)
        m = cw_margin(z, y)
        g, = torch.autograd.grad(m.sum(), xa)
        with torch.no_grad():
            xa = torch.min(torch.max(xa + step * g.sign(), lo), hi)
            m = cw_margin(model(xa), y)
            upd = m > m_best
            x_best[upd] = xa[upd]
            m_best[upd] = m[upd]
    return x_best.detach(), m_best.detach()


class Driver:
    def __init__(self, a):
        self.a = a
        torch.set_num_threads(a.threads)
        self.dev = rb.pick_device(a.device)
        os.makedirs(a.ckpt, exist_ok=True)
        self.logf = open(os.path.join(a.ckpt, 'log.txt'), 'a')
        self.log(f'== start {now()} args {vars(a)}')
        self.x, self.y, self.hx = rb.load_cifar100_test()
        self.N = self.x.shape[0]
        self.model_cpu, self.wpath, self.wsha = rb.load_rb_model(a.model, 'cpu')
        self.model = rb.load_rb_model(a.model, self.dev)[0] if self.dev.type != 'cpu' else self.model_cpu
        self.log(f'model {a.model} weights sha256 {self.wsha} device {self.dev} test-set sha256 {self.hx}')
        # inputs: the incumbent tensor, its CPU margins and its not-fooled mask
        self.state_path = os.path.join(a.ckpt, 'state.json')
        self.xadv_path = os.path.join(a.ckpt, 'x_adv.npy')
        self.mcpu_path = os.path.join(a.ckpt, 'm_cpu.npy')
        x_in = torch.from_numpy(np.load(a.x_adv_in))
        m_in = torch.from_numpy(np.load(a.margin_in)).float()
        mask_in = torch.from_numpy(np.load(a.mask_in)).bool()
        self.log(f'x_adv_in {a.x_adv_in} sha256 {rb.sha256_file(a.x_adv_in)}; residual (not fooled) {int(mask_in.sum())}; '
                 f'margin_in {a.margin_in}; mask_in {a.mask_in}')
        x_in = x_in[:self.N]; m_in = m_in[:self.N]; mask_in = mask_in[:self.N]   # --n_test subset (smoke tests)
        assert x_in.shape == (self.N, 3, 32, 32)
        assert int((m_in[mask_in] > 0).sum()) == 0, 'mask/margin disagree: a not-fooled image has margin > 0'
        if os.path.isfile(self.state_path) and os.path.isfile(self.xadv_path):
            self.state = json.load(open(self.state_path))
            self.x_adv = torch.from_numpy(np.load(self.xadv_path))
            self.m_cpu = torch.from_numpy(np.load(self.mcpu_path))
            self.log(f'RESUMED: units done {self.state["unit_done"]}/{len(self.state["units"])}, '
                     f'successes so far {len(self.state["successes"])}')
        else:
            self.x_adv = x_in.clone()
            self.m_cpu = m_in.clone()
            # residual ordering: closest to the boundary first (margin <= 0, larger = closer)
            res = torch.nonzero(mask_in).squeeze(1)
            band = res[m_in[res] > -a.max_dist] if a.max_dist is not None else res
            order = band[m_in[band].argsort(descending=True)] if a.order == 'closest' else band
            if a.limit:
                order = order[:a.limit]
            units = [order[i:i + a.batch].tolist() for i in range(0, order.numel(), a.batch)]
            self.state = {'created': now(), 'args': vars(a), 'x_adv_in_sha256': rb.sha256_file(a.x_adv_in),
                          'n_residual_total': int(mask_in.sum()), 'n_selected': int(order.numel()),
                          'units': units, 'unit_done': 0, 'successes': {}, 'borderline': {}, 'unit_stats': [],
                          'fwd_total': 0.0, 'bwd_total': 0.0, 'wall_total': 0.0}
            self.log(f'selected {order.numel()} residual images with CPU margin > -{a.max_dist} (of {int(mask_in.sum())}), '
                     f'{len(units)} units of <= {a.batch}')
            self.save()

    def log(self, s):
        line = f'[{time.strftime("%H:%M:%S")}] {s}'
        print(line, flush=True)
        self.logf.write(line + '\n'); self.logf.flush()

    def save(self):
        np.save(self.xadv_path, self.x_adv.numpy().astype(np.float32))
        np.save(self.mcpu_path, self.m_cpu.numpy().astype(np.float32))
        tmp = self.state_path + '.tmp'
        json.dump(self.state, open(tmp, 'w'))
        os.replace(tmp, self.state_path)

    def box(self, idx):
        xb = self.x[idx].to(self.dev)
        return xb, self.y[idx].to(self.dev), (xb - EPS).clamp(0, 1), (xb + EPS).clamp(0, 1)

    def cpu_margin(self, xa_cpu, idx):
        lg = rb.logits(self.model_cpu, xa_cpu, 250, 'cpu')
        return rb.margin(lg, self.y[idx])

    def commit(self, idx, xa_cpu, m_cpu):
        """commit CPU-verified successes (exact rule m_cpu > 0); float64 projection onto the eps-box and [0,1]."""
        for j in range(idx.numel()):
            i = int(idx[j])
            xi = torch.min(torch.max(xa_cpu[j].double(), self.x[i].double() - EPS), self.x[i].double() + EPS).clamp(0, 1).float()
            self.x_adv[i] = xi
            self.m_cpu[i] = float(m_cpu[j])

    def run(self):
        a = self.a
        attacker = CRAttack(self.model, eps=EPS, max_iter=a.max_iter, decay_steps=a.decay_steps,
                            target_numbers=a.targets, restart=a.restart, random_start=True, seed=a.seed,
                            potential_thresh=a.potential_thresh)
        units = self.state['units']
        for k in range(self.state['unit_done'], len(units)):
            bi = torch.tensor(units[k], dtype=torch.long)
            xb, yb, lo, hi = self.box(bi)
            h = int(hashlib.sha256(f'{a.seed}|cr|{k}'.encode()).hexdigest()[:8], 16)
            torch.manual_seed(h)
            if self.dev.type == 'mps':
                torch.mps.manual_seed(h)
            t0 = time.time()
            adv, fnum, bnum = attacker.forward(xb, yb)
            with torch.no_grad():
                adv = torch.min(torch.max(adv, lo), hi)
                md = dev_margin(self.model, adv, yb)
            t_attack = time.time() - t0
            cand = torch.nonzero(md > -0.02).squeeze(1)           # device-claimed successes + near misses
            n_dev = int((md > 0).sum())
            n_cpu_exact = n_cpu_safe = n_polished = 0
            if cand.numel():
                adv_c = adv[cand].cpu()
                idx_c = bi[cand.cpu()]
                mc = self.cpu_margin(adv_c, idx_c)
                # polish borderline CPU margins (-0.02, 1e-3) with small CW steps on the device (3 rounds, shrinking
                # step), re-verify on CPU after every round; keep a point only if its CPU margin improved
                for rd, stp in enumerate((EPS / 16, EPS / 32, EPS / 64)):
                    bord = torch.nonzero((mc > -0.02) & (mc < STOP)).squeeze(1)
                    if not bord.numel():
                        break
                    xb2, yb2, lo2, hi2 = self.box(idx_c[bord])
                    xp, mp = polish_cw(self.model, xb2, yb2, lo2, hi2, adv_c[bord].to(self.dev), n_steps=20, step=stp)
                    xp = xp.cpu()
                    mcp = self.cpu_margin(xp, idx_c[bord])
                    better = mcp > mc[bord]
                    for q in range(bord.numel()):
                        if bool(better[q]):
                            adv_c[bord[q]] = xp[q]
                            mc[bord[q]] = mcp[q]
                    n_polished += int(better.sum())
                ok = mc > 0
                n_cpu_exact = int(ok.sum()); n_cpu_safe = int((mc >= STOP).sum())
                if ok.any():
                    self.commit(idx_c[ok], adv_c[ok], mc[ok])
                    for q in torch.nonzero(ok).squeeze(1).tolist():
                        self.state['successes'][str(int(idx_c[q]))] = {
                            'unit': k, 'm_cpu': float(mc[q]), 'm_dev': float(md[cand[q]]),
                            'm_before': float(self.m_cpu_in(int(idx_c[q])))}
                for q in torch.nonzero((mc > -0.02) & ~ok).squeeze(1).tolist():
                    self.state['borderline'][str(int(idx_c[q]))] = {'unit': k, 'm_cpu': float(mc[q]), 'm_dev': float(md[cand[q]])}
            fsum, bsum = float(fnum.sum()), float(bnum.sum())
            st = {'unit': k, 'n': int(bi.numel()), 'dev_fooled': n_dev, 'cpu_fooled_exact': n_cpu_exact,
                  'cpu_fooled_safe': n_cpu_safe, 'polished': n_polished, 'fwd_per_img': round(fsum / bi.numel(), 1),
                  'bwd_per_img': round(bsum / bi.numel(), 1), 'attack_s': round(t_attack, 1),
                  'unit_s': round(time.time() - t0, 1), 'finished': now(),
                  'margin_range': [float(self.m_cpu_in_min(bi)), float(self.m_cpu_in_max(bi))]}
            self.state['unit_stats'].append(st)
            self.state['fwd_total'] += fsum; self.state['bwd_total'] += bsum; self.state['wall_total'] += time.time() - t0
            self.state['unit_done'] = k + 1
            self.save()
            if self.dev.type == 'mps':
                torch.mps.empty_cache()
            tot = len(self.state['successes'])
            self.log(f'  unit {k + 1}/{len(units)} n={bi.numel()} margins [{st["margin_range"][0]:.3f},{st["margin_range"][1]:.3f}] '
                     f'dev-fooled {n_dev} cpu-fooled exact {n_cpu_exact} (safe {n_cpu_safe}, polished {n_polished}) '
                     f'fwd/img {st["fwd_per_img"]} bwd/img {st["bwd_per_img"]} {t_attack:.0f}s  TOTAL new breaks {tot}')
        self.log(f'== attack done: {len(self.state["successes"])} CPU-verified new breaks on {self.state["n_selected"]} selected residuals; '
                 f'fwd total {self.state["fwd_total"]:.0f} bwd total {self.state["bwd_total"]:.0f} wall {self.state["wall_total"]:.0f}s')

    # margins of the INPUT tensor (before this run) for reporting
    def m_cpu_in(self, i):
        if not hasattr(self, '_m_in'):
            self._m_in = torch.from_numpy(np.load(self.a.margin_in)).float()
        return self._m_in[i]

    def m_cpu_in_min(self, bi):
        return self.m_cpu_in(bi).min()

    def m_cpu_in_max(self, bi):
        return self.m_cpu_in(bi).max()

    def final(self):
        """ulp nudge for strict float64 feasibility, float64 checks, full CPU recount, write the deliverable."""
        a = self.a
        t0 = time.time()
        xa = self.x_adv.numpy().astype(np.float32); x0 = self.x.numpy()
        over = np.abs(xa.astype(np.float64) - x0.astype(np.float64)) > EPS
        n_nudged = int(over.sum())
        if n_nudged:
            xa[over] = np.nextafter(xa[over], x0[over]).astype(np.float32)
        xa = np.clip(xa, 0.0, 1.0)
        self.x_adv = torch.from_numpy(xa)
        self.log(f'  final: nudged {n_nudged} coordinates by one float32 ulp toward x')
        nf, mg = rb.cpu_verify(self.model_cpu, self.x_adv, self.y)
        d, ev, rv = rb.eps_check_float64(self.x_adv, self.x)
        n_robust = int(nf.sum())
        out = a.out or os.path.join(a.ckpt, 'x_adv_final.npy')
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        np.save(out, xa)
        np.save(out.replace('.npy', '_cpu_margin.npy'), mg.numpy().astype(np.float32))
        np.save(out.replace('.npy', '_not_fooled_mask.npy'), nf.numpy())
        res = {'model': a.model, 'time_utc': now(), 'weights_sha256': self.wsha, 'test_images_sha256': self.hx,
               'x_adv_in_sha256': self.state['x_adv_in_sha256'],
               'robust_total_cpu_ties_robust': n_robust, 'max_linf_float64': float(d.max()),
               'eps_violations': ev, 'range_violations': rv, 'n_unchanged_images': int((d == 0).sum()),
               'new_breaks_committed': len(self.state['successes']), 'n_selected': self.state['n_selected'],
               'n_residual_total': self.state['n_residual_total'], 'fwd_total': self.state['fwd_total'],
               'bwd_total': self.state['bwd_total'], 'wall_total_s': round(self.state['wall_total'], 1),
               'cr_config': {k: vars(a)[k] for k in ('targets', 'restart', 'max_iter', 'decay_steps', 'potential_thresh', 'seed')},
               'x_adv_sha256': rb.sha256_file(out), 'final_s': round(time.time() - t0, 1)}
        json.dump(res, open(out + '.summary.json', 'w'), indent=1)
        self.state['final'] = res
        self.save()
        self.log(f'[FINAL] robust (CPU, ties=robust) {n_robust}/{self.N} = {100.0 * n_robust / self.N:.2f}%  max Linf {d.max():.10f} '
                 f'eps_viol {ev} range_viol {rv} new breaks {len(self.state["successes"])}  wrote {out}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='Addepalli2022Efficient_RN18')
    ap.add_argument('--x_adv_in', required=True, help='incumbent full-test-set tensor (.npy, float32)')
    ap.add_argument('--margin_in', required=True, help='its CPU margins (best_wrong - true), float32 (N,)')
    ap.add_argument('--mask_in', required=True, help='its not-fooled mask (== margin <= 0; see mask_from_margin.py)')
    ap.add_argument('--ckpt', required=True)
    ap.add_argument('--max_dist', type=float, default=None, help='only residuals with CPU margin > -max_dist (logits)')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--order', default='closest', choices=['closest', 'index'])
    ap.add_argument('--batch', type=int, default=200)
    ap.add_argument('--targets', type=int, default=3)
    ap.add_argument('--restart', type=int, default=5)
    ap.add_argument('--max_iter', type=int, default=150)
    ap.add_argument('--decay_steps', type=int, default=30)
    ap.add_argument('--potential_thresh', type=float, default=0.05)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--device', default='mps')
    ap.add_argument('--threads', type=int, default=4)
    ap.add_argument('--final', action='store_true')
    ap.add_argument('--out', default=None)
    rb.add_common_args(ap)
    a = ap.parse_args()
    rb.configure(a.data_dir, a.model_dir, a.n_test)
    d = Driver(a)
    d.run()
    if a.final:
        d.final()
    d.log(f'== end {now()}')


if __name__ == '__main__':
    main()
