#!/usr/bin/env python
"""
warm_residual.py -- stage 4: pushes the RESIDUAL set of a verified x_adv tensor (clean-correct images still correctly
classified) with WARM leave-the-ball-and-come-back arms started at the saved incumbent endpoints, closest-to-boundary
first:

  crwarm    CR Attack's periodic relax/reset schedule (Pan et al., AAAI 2025: per 30-step cycle, 10 steps in radius
            eps + eps*scale, 10 at eps, a shrink to eps - eps*scale + uniform noise of +-eps*scale, then eps; scale halves
            every 30 steps, floor 0.05) WARM-STARTED at the incumbent with the untargeted CW margin (an independent
            re-implementation of the schedule, first written by another AI agent of the same project).
  crhop     basin hopping from the incumbent with CR's reset/relax/eps moves (same origin as crwarm).
  crwarm_t  crwarm on the TARGETED margin z_t - z_y for each of the top-K wrong classes at the incumbent (best tracked on
            the untargeted margin, i.e. any wrong class counts).
  tempering replica exchange over relaxation radii: R replicas run the relax phase at radii eps*(1+r_k), swap
            neighbouring replicas by Metropolis on the projected margin; best projected point kept.

Every device-claimed success (device margin > -0.02 after an arm) is re-verified on the CPU float32 model (argmax ties =
NOT fooled), borderline CPU margins get a 3-round small-step CW polish, and only CPU-verified successes (margin > 0) are
committed, via a float64 projection onto the eps-box and [0,1].  Optionally (--commit_improved) robust rows whose CPU
margin improved are also committed so later invocations start from the better incumbent (count unchanged).
Per-unit checkpoints (x_adv.npy, m_cpu.npy, state.json) make it resumable.  --write_out writes a tensor with the one-ulp
nudge toward x (not used in the original pipeline: assemble_final.py does this step).

  python warm_residual.py --model Addepalli2022Efficient_RN18 --x_adv_in X --margin_in M --mask_in K --ckpt DIR \
        --arms crwarm --max_dist 0.1 --batch 100 --seed 0
"""
import argparse, hashlib, json, math, os, sys, time

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rb_common as rb  # noqa: E402

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


def proj(xa, lo, hi):
    return torch.min(torch.max(xa, lo), hi).clamp(0.0, 1.0)


@torch.no_grad()
def dev_margin(model, xa, y, bs=250):
    out = []
    for i in range(0, xa.shape[0], bs):
        out.append(cw_margin(model(xa[i:i + bs]), y[i:i + bs]))
    return torch.cat(out, 0)


def grad_obj(model, xa, y, t=None):
    """returns (untargeted CW margin, gradient of the objective): objective = CW margin, or z_t - z_y if t is given."""
    xa = xa.detach().requires_grad_(True)
    z = model(xa)
    m = cw_margin(z, y)
    if t is None:
        obj = m
    else:
        obj = z.gather(1, t.view(-1, 1)).squeeze(1) - z.gather(1, y.view(-1, 1)).squeeze(1)
    g, = torch.autograd.grad(obj.sum(), xa)
    return m.detach(), g.detach()


class Best:
    def __init__(self, x0, m0):
        self.x = x0.clone(); self.m = m0.clone()

    def update(self, xc, mc):
        upd = mc > self.m
        if upd.any():
            self.x[upd] = xc[upd]; self.m[upd] = mc[upd]
        return int(upd.sum())


# ------------------------------------------------------------------------------------------------------------------------
# arms (all return points inside [lo, hi]; best tracked on the untargeted CW margin of eps-feasible points only)
# ------------------------------------------------------------------------------------------------------------------------
def arm_crwarm(model, x, y, lo, hi, xb, mb, gen, max_iter=150, decay=30, relax_mult=1.0, noise_mult=1.0, target=None):
    alpha = EPS
    best = Best(xb, mb)
    xa = xb.clone()
    scale = 1.0
    nfwd = 0
    for i in range(max_iter):
        if i % decay == 0:
            scale = max(scale * 0.5, 0.05)
        ph = i % decay
        if ph < decay // 3:
            cur_eps = EPS + relax_mult * alpha * scale
        elif ph < 2 * (decay // 3):
            cur_eps = EPS
        elif ph == 2 * (decay // 3):
            cur_eps = EPS - alpha * scale
            xa = (x + (xa - x).clamp(-cur_eps, cur_eps)).clamp(0, 1)
            xa = (xa + (2 * torch.rand(xa.shape, generator=gen) - 1).to(xa.device) * noise_mult * alpha * scale).clamp(0, 1)
            cur_eps = EPS
        else:
            cur_eps = EPS
        m, g = grad_obj(model, xa, y, target); nfwd += 1
        inside = ((xa - x).abs().flatten(1).max(1).values <= EPS + 1e-7)
        if inside.any():
            best.update(torch.where(inside.view(-1, 1, 1, 1), xa, best.x), torch.where(inside, m, best.m - 1))
        xa = xa + alpha * scale * g.sign()
        xa = (x + (xa - x).clamp(-cur_eps, cur_eps)).clamp(0, 1)
        if cur_eps > EPS:
            xp = proj(xa, lo, hi)
            best.update(xp, dev_margin(model, xp, y)); nfwd += 1
    xp = proj(xa, lo, hi)
    best.update(xp, dev_margin(model, xp, y)); nfwd += 1
    return best.x, best.m, {'image_steps': nfwd}


def arm_crhop(model, x, y, lo, hi, xb, mb, gen, hops=12, scales=(0.5, 0.5, 0.25, 0.25, 0.125, 0.0625), relax_steps=10,
              eps_steps=10, relax_mult=1.0, noise_mult=1.0, target=None):
    alpha = EPS
    best = Best(xb, mb)
    nfwd = 0
    for h in range(hops):
        scale = scales[h % len(scales)]
        cur_eps = EPS - alpha * scale
        xa = (x + (best.x - x).clamp(-cur_eps, cur_eps)).clamp(0, 1)
        xa = (xa + (2 * torch.rand(xa.shape, generator=gen) - 1).to(xa.device) * noise_mult * alpha * scale).clamp(0, 1)
        r_eps = EPS + relax_mult * alpha * scale
        for i in range(relax_steps):
            m, g = grad_obj(model, xa, y, target); nfwd += 1
            xa = (x + (xa + alpha * scale * g.sign() - x).clamp(-r_eps, r_eps)).clamp(0, 1)
            xp = proj(xa, lo, hi)
            best.update(xp, dev_margin(model, xp, y)); nfwd += 1
        xa = proj(xa, lo, hi)
        for i in range(eps_steps):
            m, g = grad_obj(model, xa, y, target); nfwd += 1
            best.update(xa, m)
            xa = proj(xa + alpha * scale * g.sign(), lo, hi)
        best.update(xa, dev_margin(model, xa, y)); nfwd += 1
    return best.x, best.m, {'image_steps': nfwd}


def topk_wrong(model, xb, y, k):
    with torch.no_grad():
        z = model(xb)
    z = z.clone()
    z.scatter_(1, y.view(-1, 1), float('-inf'))
    return z.topk(k, 1).indices


def arm_crwarm_t(model, x, y, lo, hi, xb, mb, gen, k=3, **kw):
    best = Best(xb, mb)
    tops = topk_wrong(model, xb, y, k)
    nfwd = 1
    for j in range(k):
        xr, mr, st = arm_crwarm(model, x, y, lo, hi, best.x, best.m, gen, target=tops[:, j], **kw)
        best.update(xr, mr); nfwd += st['image_steps']
    return best.x, best.m, {'image_steps': nfwd}


def arm_crhop_t(model, x, y, lo, hi, xb, mb, gen, k=3, **kw):
    best = Best(xb, mb)
    tops = topk_wrong(model, xb, y, k)
    nfwd = 1
    for j in range(k):
        xr, mr, st = arm_crhop(model, x, y, lo, hi, best.x, best.m, gen, target=tops[:, j], **kw)
        best.update(xr, mr); nfwd += st['image_steps']
    return best.x, best.m, {'image_steps': nfwd}


def arm_tempering(model, x, y, lo, hi, xb, mb, gen, radii=(0.25, 0.5, 1.0, 2.0), rounds=10, relax_steps=8, eps_steps=6,
                  step_frac=0.25, T=0.01):
    """replica exchange over relaxation radii: replica k ascends (sign steps of step_frac*eps) inside radius eps*(1+r_k)
    for relax_steps, then its projection is polished eps_steps at eps (scored); neighbouring replicas swap their relaxed
    states with prob min(1, exp((m_a - m_b)(1/T_a - 1/T_b))) using the projected margins, T_k = T*(1+r_k)."""
    R = len(radii)
    best = Best(xb, mb)
    reps = [xb.clone() for _ in range(R)]
    scores = [mb.clone() for _ in range(R)]
    nfwd = 0
    step = step_frac * EPS
    for rd in range(rounds):
        for k, r in enumerate(radii):
            xa = reps[k]
            r_eps = EPS * (1 + r)
            for i in range(relax_steps):
                m, g = grad_obj(model, xa, y); nfwd += 1
                xa = (x + (xa + step * g.sign() - x).clamp(-r_eps, r_eps)).clamp(0, 1)
            reps[k] = xa
            xp = proj(xa, lo, hi)
            for i in range(eps_steps):
                m, g = grad_obj(model, xp, y); nfwd += 1
                best.update(xp, m)
                xp = proj(xp + (step / 2) * g.sign(), lo, hi)
            mp = dev_margin(model, xp, y); nfwd += 1
            best.update(xp, mp)
            scores[k] = mp
        # swap neighbours (even/odd alternation)
        for k in range(rd % 2, R - 1, 2):
            Ta, Tb = T * (1 + radii[k]), T * (1 + radii[k + 1])
            d = (scores[k + 1] - scores[k]) * (1.0 / Ta - 1.0 / Tb)
            u = torch.rand(d.shape, generator=gen).to(d.device)
            sw = u < torch.exp(d.clamp(max=0.0))
            sw = sw | (d > 0)
            if sw.any():
                a_, b_ = reps[k].clone(), reps[k + 1].clone()
                reps[k][sw] = b_[sw]; reps[k + 1][sw] = a_[sw]
                sa_, sb_ = scores[k].clone(), scores[k + 1].clone()
                scores[k][sw] = sb_[sw]; scores[k + 1][sw] = sa_[sw]
    return best.x, best.m, {'image_steps': nfwd}


ARMS = {'crwarm': arm_crwarm, 'crhop': arm_crhop, 'crwarm_t': arm_crwarm_t, 'crhop_t': arm_crhop_t,
        'tempering': arm_tempering}


def polish_cw(model, x, y, lo, hi, x0, n_steps=20, step=EPS / 16):
    """small-step signed-gradient ascent on the CW margin inside the box, keeping the best device-margin iterate."""
    xa = x0.clone()
    with torch.no_grad():
        m_best = cw_margin(model(xa), y)
    x_best = xa.clone()
    for _ in range(n_steps):
        xa = xa.detach().requires_grad_(True)
        m = cw_margin(model(xa), y)
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
        self.log(f'== start {now()} pid {os.getpid()} args {vars(a)}')
        self.x, self.y, self.hx = rb.load_cifar100_test()
        self.N = self.x.shape[0]
        self.model_cpu, self.wpath, self.wsha = rb.load_rb_model(a.model, 'cpu')
        self.model = rb.load_rb_model(a.model, self.dev)[0] if self.dev.type != 'cpu' else self.model_cpu
        self.log(f'model {a.model} weights sha256 {self.wsha} device {self.dev} test-set sha256 {self.hx}')
        self.state_path = os.path.join(a.ckpt, 'state.json')
        self.xadv_path = os.path.join(a.ckpt, 'x_adv.npy')
        self.mcpu_path = os.path.join(a.ckpt, 'm_cpu.npy')
        x_in = torch.from_numpy(np.load(a.x_adv_in))
        m_in = torch.from_numpy(np.load(a.margin_in)).float()
        mask_in = torch.from_numpy(np.load(a.mask_in)).bool()
        self.m_in = m_in
        self.log(f'x_adv_in {a.x_adv_in} sha256 {rb.sha256_file(a.x_adv_in)}; residual (not fooled) {int(mask_in.sum())}')
        x_in = x_in[:self.N]; m_in = m_in[:self.N]; mask_in = mask_in[:self.N]   # --n_test subset (smoke tests)
        self.m_in = m_in
        assert x_in.shape == (self.N, 3, 32, 32)
        assert bool((mask_in == (m_in <= 0)).all()), 'mask/margin disagree'
        if os.path.isfile(self.state_path) and os.path.isfile(self.xadv_path):
            self.state = json.load(open(self.state_path))
            self.x_adv = torch.from_numpy(np.load(self.xadv_path))
            self.m_cpu = torch.from_numpy(np.load(self.mcpu_path))
            self.log(f'RESUMED: units done {self.state["unit_done"]}/{len(self.state["units"])}, '
                     f'successes so far {len(self.state["successes"])}')
        else:
            self.x_adv = x_in                      # no copy (host memory is tight)
            self.m_cpu = m_in.clone()
            res = torch.nonzero(mask_in).squeeze(1)
            band = res[m_in[res] > -a.max_dist] if a.max_dist is not None else res
            order = band[m_in[band].argsort(descending=True)]
            order = order[a.skip:]
            if a.limit:
                order = order[:a.limit]
            units = [order[i:i + a.batch].tolist() for i in range(0, order.numel(), a.batch)]
            self.state = {'created': now(), 'args': vars(a), 'x_adv_in_sha256': rb.sha256_file(a.x_adv_in),
                          'n_residual_total': int(mask_in.sum()), 'n_selected': int(order.numel()),
                          'units': units, 'unit_done': 0, 'successes': {}, 'improved_committed': 0,
                          'unit_stats': [], 'image_steps_total': 0.0, 'wall_total': 0.0}
            self.log(f'selected {order.numel()} residual images with CPU margin > -{a.max_dist} (skip {a.skip}) of '
                     f'{int(mask_in.sum())}, {len(units)} units of <= {a.batch}')
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

    def f64_proj(self, i, xi):
        return torch.min(torch.max(xi.double(), self.x[i].double() - EPS), self.x[i].double() + EPS).clamp(0, 1).float()

    def verify_and_commit(self, k, arm, idx, xa_dev, md):
        """CPU-verify rows with device margin > -0.02 (polish borderline), commit CPU-verified successes; optionally commit
        CPU-improved robust rows.  Returns (n_cpu_exact, n_cpu_safe, n_polished, fooled_mask_in_unit)."""
        a = self.a
        n_exact = n_safe = n_pol = n_imp = 0
        fooled_in_unit = torch.zeros(idx.numel(), dtype=torch.bool)
        xa_cpu = xa_dev.cpu()
        if a.commit_improved:
            check = torch.arange(idx.numel())
        else:
            check = torch.nonzero(md.cpu() > -0.02).squeeze(1)
        if not check.numel():
            return 0, 0, 0, 0, fooled_in_unit
        adv_c = torch.stack([self.f64_proj(int(idx[q]), xa_cpu[q]) for q in check.tolist()])
        idx_c = idx[check]
        mc = self.cpu_margin(adv_c, idx_c)
        for rd, stp in enumerate((EPS / 16, EPS / 32, EPS / 64)):
            bord = torch.nonzero((mc > -0.02) & (mc < STOP)).squeeze(1)
            if not bord.numel():
                break
            xb2, yb2, lo2, hi2 = self.box(idx_c[bord])
            xp, mp = polish_cw(self.model, xb2, yb2, lo2, hi2, adv_c[bord].to(self.dev), n_steps=20, step=stp)
            xp = xp.cpu()
            xp = torch.stack([self.f64_proj(int(idx_c[bord[q]]), xp[q]) for q in range(bord.numel())])
            mcp = self.cpu_margin(xp, idx_c[bord])
            better = mcp > mc[bord]
            for q in range(bord.numel()):
                if bool(better[q]):
                    adv_c[bord[q]] = xp[q]
                    mc[bord[q]] = mcp[q]
            n_pol += int(better.sum())
        for q in range(idx_c.numel()):
            i = int(idx_c[q])
            if float(mc[q]) > 0:
                self.x_adv[i] = adv_c[q]
                before = float(self.m_cpu[i])
                self.m_cpu[i] = float(mc[q])
                self.state['successes'][str(i)] = {'unit': k, 'arm': arm, 'm_cpu': float(mc[q]),
                                                   'm_before_run': float(self.m_in[i]), 'm_before_arm': before}
                n_exact += 1; n_safe += int(float(mc[q]) >= STOP)
                fooled_in_unit[int(check[q])] = True
            elif a.commit_improved and float(mc[q]) > float(self.m_cpu[i]):
                self.x_adv[i] = adv_c[q]
                self.m_cpu[i] = float(mc[q])
                n_imp += 1
        self.state['improved_committed'] += n_imp
        return n_exact, n_safe, n_pol, n_imp, fooled_in_unit

    def run(self):
        a = self.a
        arms = a.arms.split(',')
        params = json.loads(a.params)
        units = self.state['units']
        for k in range(self.state['unit_done'], len(units)):
            bi = torch.tensor(units[k], dtype=torch.long)
            t0 = time.time()
            stats = {'unit': k, 'n': int(bi.numel()), 'margin_range': [float(self.m_in[bi].min()), float(self.m_in[bi].max())],
                     'arms': []}
            active = torch.ones(bi.numel(), dtype=torch.bool)
            for arm in arms:
                act = torch.nonzero(active).squeeze(1)
                if not act.numel():
                    break
                idx = bi[act]
                xb, yb, lo, hi = self.box(idx)
                inc = self.x_adv[idx].to(self.dev)
                inc = proj(inc, lo, hi)
                with torch.no_grad():
                    m0 = dev_margin(self.model, inc, yb)
                h = int(hashlib.sha256(f'{a.seed}|{arm}|{k}'.encode()).hexdigest()[:8], 16)
                gen = torch.Generator().manual_seed(h)
                torch.manual_seed(h)
                ta = time.time()
                xr, mr, st = ARMS[arm](self.model, xb, yb, lo, hi, inc, m0, gen, **params.get(arm, {}))
                xr = proj(xr, lo, hi)
                with torch.no_grad():
                    mr = dev_margin(self.model, xr, yb)
                t_arm = time.time() - ta
                ne, ns, npol, nimp, fl = self.verify_and_commit(k, arm, idx, xr, mr)
                active[act[fl]] = False
                gain = (mr - m0).cpu()
                rec = {'arm': arm, 'n': int(idx.numel()), 'dev_fooled': int((mr > 0).sum()), 'cpu_fooled_exact': ne,
                       'cpu_fooled_safe': ns, 'polished': npol, 'improved_committed': nimp,
                       'dev_gain_mean': float(gain.mean()), 'dev_gain_max': float(gain.max()),
                       'dev_improved': int((gain > 0).sum()), 'image_steps_per_img': st.get('image_steps', 0),
                       'arm_s': round(t_arm, 1)}
                stats['arms'].append(rec)
                self.state['image_steps_total'] += float(st.get('image_steps', 0)) * idx.numel()
                self.state.setdefault('arm_log', []).append(dict(rec, unit=k, finished=now()))
                self.save()                          # commits survive an alarm in the middle of a unit
                if self.dev.type == 'mps':
                    torch.mps.empty_cache()
                self.log(f'  unit {k + 1}/{len(units)} arm {arm}: n={idx.numel()} dev-fooled {rec["dev_fooled"]} '
                         f'cpu-fooled {ne} (safe {ns}, polished {npol}) improved-committed {nimp} '
                         f'dev gain mean {rec["dev_gain_mean"]:+.4f} max {rec["dev_gain_max"]:+.4f} {t_arm:.0f}s')
            stats['unit_s'] = round(time.time() - t0, 1)
            stats['finished'] = now()
            self.state['unit_stats'].append(stats)
            self.state['wall_total'] += time.time() - t0
            self.state['unit_done'] = k + 1
            self.save()
            tot = len(self.state['successes'])
            self.log(f'  unit {k + 1}/{len(units)} done margins [{stats["margin_range"][0]:.4f},{stats["margin_range"][1]:.4f}] '
                     f'{stats["unit_s"]:.0f}s  TOTAL new breaks {tot}  -> implied robust {int((self.m_cpu <= 0).sum())}')
        self.log(f'== attack done: {len(self.state["successes"])} CPU-verified new breaks on {self.state["n_selected"]} selected; '
                 f'image-steps {self.state["image_steps_total"]:.0f}; wall {self.state["wall_total"]:.0f}s')

    def write_out(self, out):
        """one-ulp nudge toward x until max|x_adv - x| <= 8/255 in float64 (ToTensor reference), chunked to save memory."""
        xa = self.x_adv.numpy().astype(np.float32)
        x0 = self.x.numpy()
        n_nudged = 0
        dmax = np.zeros(self.N); rng = np.zeros(self.N, dtype=bool)
        for s0 in range(0, self.N, 500):
            sl = slice(s0, s0 + 500)
            xs, x0s = xa[sl], x0[sl]
            for _ in range(4):
                over = np.abs(xs.astype(np.float64) - x0s.astype(np.float64)) > EPS
                if not over.any():
                    break
                n_nudged += int(over.sum())
                xs[over] = np.nextafter(xs[over], x0s[over]).astype(np.float32)
            np.clip(xs, 0.0, 1.0, out=xs)
            dmax[sl] = np.abs(xs.astype(np.float64) - x0s.astype(np.float64)).reshape(xs.shape[0], -1).max(1)
            rng[sl] = ((xs < 0) | (xs > 1)).reshape(xs.shape[0], -1).any(1)
        ev = int((dmax > EPS).sum()); ev6 = int((dmax > EPS + 1e-6).sum()); rv = int(rng.sum())
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        np.save(out, xa)
        np.save(out.replace('.npy', '_cpu_margin_rows.npy'), self.m_cpu.numpy().astype(np.float32))
        res = {'model': self.a.model, 'time_utc': now(), 'x_adv_sha256': rb.sha256_file(out),
               'x_adv_in_sha256': self.state['x_adv_in_sha256'],
               'n_nudged_ulp': n_nudged, 'max_linf_float64': float(dmax.max()), 'eps_violations_strict': ev,
               'eps_violations_tol1e-6': ev6, 'range_violations': rv,
               'implied_robust_from_row_margins': int((self.m_cpu <= 0).sum()),
               'new_breaks': self.state['successes'], 'note': 'implied count = CPU margins of the input tensor for unchanged rows '
               '+ CPU-verified margins of committed rows; run a full checker for the official count'}
        json.dump(res, open(out + '.manifest.json', 'w'), indent=1)
        self.log(f'[WRITE] {out} sha256 {res["x_adv_sha256"]} nudged {n_nudged} max Linf {dmax.max():.10f} viol {ev}/{ev6} '
                 f'range {rv} implied robust {res["implied_robust_from_row_margins"]}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True)
    ap.add_argument('--x_adv_in', required=True)
    ap.add_argument('--margin_in', required=True)
    ap.add_argument('--mask_in', required=True)
    ap.add_argument('--ckpt', required=True)
    ap.add_argument('--arms', default='crwarm')
    ap.add_argument('--params', default='{}', help='JSON dict arm -> kwargs')
    ap.add_argument('--max_dist', type=float, default=None)
    ap.add_argument('--skip', type=int, default=0)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--batch', type=int, default=100)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--device', default='mps')
    ap.add_argument('--threads', type=int, default=4)
    ap.add_argument('--commit_improved', type=int, default=1)
    ap.add_argument('--write_out', default=None)
    rb.add_common_args(ap)
    a = ap.parse_args()
    rb.configure(a.data_dir, a.model_dir, a.n_test)
    d = Driver(a)
    d.run()
    if a.write_out:
        d.write_out(a.write_out)
    d.log(f'== end {now()}')


if __name__ == '__main__':
    main()
