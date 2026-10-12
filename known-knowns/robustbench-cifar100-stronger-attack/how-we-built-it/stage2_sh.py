#!/usr/bin/env python
"""
stage2_sh.py -- budget-allocation search over targeted-APGD arms for the images that survive APGD-CE.

Arms per image: (target class among the top-K wrong classes by clean logit) x (loss).  Ranks 1..L1 get all losses in
--losses_top (default dlr-t,cw-t,pm-t), ranks L1+1..K get --losses_wide (default cw-t); --corner_top c adds a
corner-start (x + eps*sign(grad)) cw-t arm for the top c targets.  Successive halving: every arm runs r_1 steps, the
top n_2 arms of each image (by best margin achieved so far) CONTINUE (state kept) for r_2 more steps, the top n_3 for
r_3 more.  An image is done as soon as any arm's device margin exceeds --drop_margin (checked every 10 steps); its
remaining arms are dropped.  Max budget per image = A*r_1 + n_2*r_2 + n_3*r_3 gradient steps
(default 45*10 + 9*20 + 3*90 = 900 = AutoAttack's APGD-T budget of 9 targets x 100 steps).

--mode uniform runs AutoAttack's APGD-T configuration through the same code (9 targets x 100 steps, dlr-t, random
start, no pruning) for the equal-budget ablation.

Resumable: per super-chunk .npz checkpoints in --ckpt.  Outputs x_adv_<tag>.npy (stage-1 tensor with improved rows),
CPU margins, residual list, and an auditable per-image arm log (margin of every arm after every round, kept flags,
breaking arm).
"""
import argparse, json, os, sys, time

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rb_common as rb  # noqa: E402
import apgd_lib as A  # noqa: E402


def cat_arms(batches):
    """Concatenate ArmBatch objects that have taken the same number of steps."""
    b0 = batches[0]
    nb = A.ArmBatch.__new__(A.ArmBatch)
    nb.model, nb.eps, nb.rho, nb.dev = b0.model, b0.eps, b0.rho, b0.dev
    for name in ('x', 'y', 't', 'loss_id', 'x_adv', 'x_adv_old', 'grad', 'grad_best', 'loss_best', 'x_best',
                 'margin_best', 'x_best_margin', 'step_size', 'loss_best_last_check', 'reduced_last_check'):
        setattr(nb, name, torch.cat([getattr(b, name) for b in batches], 0))
    nb.loss_steps = torch.cat([b.loss_steps for b in batches], 1)
    nb.R = nb.x.shape[0]
    for name in ('horizon', 'n_iter_2', 'n_iter_min', 'size_decr', 'k', 'counter3', 'i'):
        assert all(getattr(b, name) == getattr(b0, name) for b in batches), name
        setattr(nb, name, getattr(b0, name))
    nb.traj = [torch.cat([b.traj[j] for b in batches], 0) for j in range(len(b0.traj))]
    return nb


class Chunk:
    """All arms of one super-chunk of S images.  Global row space: R = S * n_arms rows."""

    def __init__(self, model, dev, x, y, imgs, ranked, arm_rank, arm_loss, arm_corner, horizon, sub, seed, drop_margin):
        self.model, self.dev, self.sub, self.drop = model, dev, sub, drop_margin
        self.S = imgs.numel(); self.n_arms = arm_rank.numel()
        self.x = x[imgs]; self.y = y[imgs]
        R = self.S * self.n_arms
        self.row_img = torch.arange(self.S).repeat_interleave(self.n_arms)
        self.row_arm = torch.arange(self.n_arms).repeat(self.S)
        rk = arm_rank[self.row_arm]
        self.row_t = torch.where(rk > 0, ranked[self.row_img, (rk - 1).clamp(min=0)], self.y[self.row_img])
        self.row_loss = arm_loss[self.row_arm]
        self.row_corner = arm_corner[self.row_arm]
        self.mb = torch.full((R,), float('-inf'))          # best margin per row (ever)
        self.xbm = None                                    # best point per row, filled lazily (CPU, R x 3x32x32)
        self.img_done = torch.zeros(self.S, dtype=torch.bool)
        self.img_best_m = torch.full((self.S,), float('-inf'))
        self.img_best_x = self.x.clone()
        self.img_best_arm = torch.full((self.S,), -1, dtype=torch.long)
        self.horizon, self.seed = horizon, seed
        self.live = []  # list of (ArmBatch, global row ids)
        self.log_rounds = []  # (S, n_arms) margins after each round
        self.log_kept = []
        self.log_traj = []    # (R,) best-margin snapshot of every row after every 10-step chunk (pruning audit)
        self.log_traj_steps = []

    def start(self):
        for corner in (False, True):
            rows = torch.nonzero(self.row_corner == corner).squeeze(1)
            for s in range(0, rows.numel(), self.sub):
                rid = rows[s:s + self.sub]
                bi = self.row_img[rid]
                b = A.ArmBatch(self.model, self.x[bi], self.y[bi], self.row_t[rid], self.row_loss[rid],
                               horizon=self.horizon, start='corner' if corner else 'rand',
                               seed=self.seed + int(rid[0]), device=self.dev)
                self.live.append((b, rid))
        self._harvest()

    def _harvest(self):
        """Pull margins/points of live rows into the global arrays, update per-image bests."""
        for b, rid in self.live:
            if b.R == 0:
                continue
            m = b.margin_best.cpu()
            self.mb[rid] = m
            # per-image best
            for i_img in torch.unique(self.row_img[rid]):
                sel = (self.row_img[rid] == i_img)
                j = torch.argmax(torch.where(sel, m, torch.full_like(m, float('-inf'))))
                if m[j] > self.img_best_m[i_img]:
                    self.img_best_m[i_img] = m[j]
                    self.img_best_x[i_img] = b.x_best_margin[j].cpu()
                    self.img_best_arm[i_img] = self.row_arm[rid[j]]

    def run_steps(self, steps, chunk=10):
        done = 0
        while done < steps and any(b.R > 0 for b, _ in self.live):
            n = min(chunk, steps - done)
            for b, _ in self.live:
                if b.R > 0:
                    b.step(n)
            done += n
            self._harvest()
            self.log_traj.append(self.mb.clone()); self.log_traj_steps.append(len(self.log_traj_steps) * 0 + self._steps_total(n))
            self.img_done |= self.img_best_m > self.drop
            # drop rows of done images
            new_live = []
            for b, rid in self.live:
                if b.R == 0:
                    continue
                keep = ~self.img_done[self.row_img[rid]]
                if keep.all():
                    new_live.append((b, rid))
                elif keep.any():
                    new_live.append((b.select(torch.nonzero(keep).squeeze(1)), rid[keep]))
            self.live = new_live

    def _steps_total(self, n):
        self._st = getattr(self, '_st', 0) + n
        return self._st

    def prune(self, kkeep):
        """Keep the top kkeep arms per (undone) image, by best margin so far; re-batch the survivors."""
        if self.dev.type == 'mps':
            torch.mps.empty_cache()
        M = torch.full((self.S, self.n_arms), float('-inf'))
        M[self.row_img, self.row_arm] = self.mb
        self.log_rounds.append(M.clone())
        live_rows = torch.cat([rid for _, rid in self.live]) if self.live else torch.zeros(0, dtype=torch.long)
        Ml = torch.full((self.S, self.n_arms), float('-inf'))
        Ml[self.row_img[live_rows], self.row_arm[live_rows]] = self.mb[live_rows]  # only live rows are candidates
        order = Ml.argsort(dim=1, descending=True)[:, :kkeep]
        keep = torch.zeros(self.S, self.n_arms, dtype=torch.bool)
        keep[torch.arange(self.S).repeat_interleave(kkeep), order.flatten()] = True
        keep &= torch.isfinite(Ml) & ~self.img_done.view(-1, 1)
        self.log_kept.append(keep.clone())
        parts, rids = [], []
        for b, rid in self.live:
            if b.R == 0:
                continue
            k = keep[self.row_img[rid], self.row_arm[rid]]
            if k.any():
                parts.append(b.select(torch.nonzero(k).squeeze(1))); rids.append(rid[k])
        self.live = []
        if parts:
            big = cat_arms(parts); brid = torch.cat(rids)
            for s in range(0, big.R, self.sub):
                sl = torch.arange(s, min(s + self.sub, big.R))
                self.live.append((big.select(sl), brid[sl]))

    def finish(self):
        M = torch.full((self.S, self.n_arms), float('-inf'))
        M[self.row_img, self.row_arm] = self.mb
        self.log_rounds.append(M.clone())
        self.live = []

    def polish(self, drop):
        """Images with 0 < margin <= drop: 20 cw-t steps (step eps/4) toward the current best wrong class."""
        weak = torch.nonzero((self.img_best_m > 0) & (self.img_best_m <= drop)).squeeze(1)
        if weak.numel() == 0:
            return 0
        with torch.no_grad():
            z = self.model(self.img_best_x[weak].to(self.dev)).cpu()
        z[torch.arange(weak.numel()), self.y[weak]] = float('-inf')
        tgt = z.argmax(1)
        pb = A.ArmBatch(self.model, self.x[weak], self.y[weak], tgt, torch.full((weak.numel(),), A.LOSS_IDS['cw-t']),
                        horizon=20, x_init=self.img_best_x[weak], device=self.dev)
        pb.step_size[:] = A.EPS / 4
        pb.step(20)
        mbp = pb.margin_best.cpu(); better = mbp > self.img_best_m[weak]
        self.img_best_x[weak[better]] = pb.x_best_margin.cpu()[better]
        self.img_best_m[weak[better]] = mbp[better]
        return int(weak.numel())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='Addepalli2022Efficient_RN18')
    ap.add_argument('--stage1', required=True, help='dir with x_adv_stage1.npy, stage1_cpu_margin.npy, stage1_survivors.npy')
    ap.add_argument('--indices', default=None, help='.npy of test indices to attack (default: all stage-1 survivors)')
    ap.add_argument('--mode', default='sh', choices=['sh', 'uniform'])
    ap.add_argument('--K', type=int, default=27)
    ap.add_argument('--L1', type=int, default=9)
    ap.add_argument('--losses_top', default='dlr-t,cw-t,pm-t')
    ap.add_argument('--losses_wide', default='cw-t')
    ap.add_argument('--corner_top', type=int, default=0)
    ap.add_argument('--untargeted', default='pm,cw', help='untargeted loss arms (rank 0), each REPLACES one lowest wide-rank '
                    'target arm so the arm count and budget stay fixed; "" disables')
    ap.add_argument('--r', default='10,20,90', help='steps per round')
    ap.add_argument('--keep', default='9,3', help='arms kept per image after round 1, 2')
    ap.add_argument('--horizon', type=int, default=None, help='APGD checkpoint-schedule horizon (default sum(r))')
    ap.add_argument('--drop_margin', type=float, default=2e-3)
    ap.add_argument('--super', type=int, default=64, help='images per super-chunk (checkpoint granularity)')
    ap.add_argument('--sub', type=int, default=500, help='rows per GPU sub-batch')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--device', default='mps')
    ap.add_argument('--ckpt', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tag', default='stage2')
    ap.add_argument('--no_cpu_verify', action='store_true')
    ap.add_argument('--clean_logits', default=None,
                    help='(N,100) float32 .npy of clean logits used to rank the target classes; the original run used an '
                         'MPS forward of the clean test set (sha256 1e0a9465...3d01).  If omitted, the clean logits are '
                         'computed here on --device and saved to <out>/clean_logits_<model>.npy')
    ap.add_argument('--threads', type=int, default=4)
    rb.add_common_args(ap)
    a = ap.parse_args()
    rb.configure(a.data_dir, a.model_dir, a.n_test)
    torch.set_num_threads(a.threads)
    os.makedirs(a.ckpt, exist_ok=True); os.makedirs(a.out, exist_ok=True)
    dev = rb.pick_device(a.device)
    T0 = time.time()

    x, y, hx = rb.load_cifar100_test()
    model_cpu, wpath, wsha = rb.load_rb_model(a.model, 'cpu')
    model = rb.load_rb_model(a.model, dev)[0] if dev.type != 'cpu' else model_cpu
    if a.clean_logits:
        clean_logits = torch.from_numpy(np.load(a.clean_logits))[:x.shape[0]]
    else:   # reconstruction of the original input (an on-device forward of the clean test set; see README)
        clean_logits = rb.logits(model, x, 250, dev)
        np.save(os.path.join(a.out, f'clean_logits_{a.model}.npy'), clean_logits.numpy().astype(np.float32))
    x_adv1 = torch.from_numpy(np.load(os.path.join(a.stage1, 'x_adv_stage1.npy')))
    m1 = torch.from_numpy(np.load(os.path.join(a.stage1, 'stage1_cpu_margin.npy')))
    surv = torch.from_numpy(np.load(a.indices if a.indices else os.path.join(a.stage1, 'stage1_survivors.npy'))).long()
    print(f'[{a.tag}] model {a.model} mode {a.mode} images {surv.numel()} device {dev}', flush=True)

    # ---- arm design
    if a.mode == 'uniform':
        K, L1, losses_top, losses_wide, rs, keeps, corner_top = 9, 9, ['dlr-t'], [], [100], [], 0
    else:
        K, L1 = a.K, a.L1
        losses_top = a.losses_top.split(','); losses_wide = [s for s in a.losses_wide.split(',') if s]
        rs = [int(v) for v in a.r.split(',')]; keeps = [int(v) for v in a.keep.split(',')]
        corner_top = a.corner_top
    horizon = a.horizon or sum(rs)
    untargeted = [u for u in (a.untargeted.split(',') if a.mode == 'sh' else []) if u]
    K_eff = K - len(untargeted) if losses_wide else K
    arm_defs = []  # (rank, loss_name, start); rank 0 = untargeted
    for rk in range(1, K_eff + 1):
        for ln in (losses_top if rk <= L1 else losses_wide):
            arm_defs.append((rk, ln, 'rand'))
    for ln in untargeted:
        arm_defs.append((0, ln, 'rand'))
    for rk in range(1, corner_top + 1):
        arm_defs.append((rk, 'cw-t', 'corner'))
    n_arms = len(arm_defs)
    budget = n_arms * rs[0] + sum(k * r for k, r in zip(keeps, rs[1:]))
    print(f'[{a.tag}] arms/image {n_arms}  rounds {rs}  keep {keeps}  max budget/image {budget} steps  horizon {horizon}',
          flush=True)
    arm_rank = torch.tensor([d[0] for d in arm_defs]); arm_loss = torch.tensor([A.LOSS_IDS[d[1]] for d in arm_defs])
    arm_corner = torch.tensor([d[2] == 'corner' for d in arm_defs])

    state_p = os.path.join(a.ckpt, 'state.json')
    state = json.load(open(state_p)) if os.path.exists(state_p) else {'done': [], 'secs': {}}
    chunks = [surv[s:s + a.super] for s in range(0, surv.numel(), a.super)]
    for ci, imgs in enumerate(chunks):
        cp = os.path.join(a.ckpt, f'chunk_{ci:03d}.npz')
        if ci in state['done'] and os.path.exists(cp):
            continue
        t0 = time.time()
        S = imgs.numel()
        cl = clean_logits[imgs].clone()
        cl[torch.arange(S), y[imgs]] = float('-inf')
        ranked = cl.argsort(dim=1, descending=True)[:, :K]  # ranked[i, r-1] = wrong class of rank r
        ch = Chunk(model, dev, x, y, imgs, ranked, arm_rank, arm_loss, arm_corner, horizon, a.sub,
                   a.seed * 1000003 + ci * 1009, a.drop_margin)
        ch.start()
        for rnd, r in enumerate(rs):
            ch.run_steps(r)
            if rnd < len(rs) - 1:
                ch.prune(keeps[rnd])
        ch.finish()
        n_pol = ch.polish(a.drop_margin)
        dt = time.time() - t0
        n_fooled_dev = int((ch.img_best_m > 0).sum())
        np.savez(cp, imgs=imgs.numpy(), x_best=ch.img_best_x.numpy().astype(np.float32),
                 margin_dev=ch.img_best_m.numpy().astype(np.float32), best_arm=ch.img_best_arm.numpy(),
                 margin_rounds=np.stack([m.numpy() for m in ch.log_rounds], 0),
                 kept_rounds=(np.stack([k.numpy() for k in ch.log_kept], 0) if ch.log_kept else np.zeros((0, S, n_arms), bool)),
                 ranked=ranked.numpy(), arm_rank=arm_rank.numpy(), arm_loss=arm_loss.numpy(), arm_corner=arm_corner.numpy(),
                 traj=np.stack([t.numpy() for t in ch.log_traj], 0).astype(np.float32), traj_steps=np.array(ch.log_traj_steps),
                 row_img=ch.row_img.numpy(), row_arm=ch.row_arm.numpy())
        state['done'].append(ci); state['secs'][str(ci)] = round(dt, 1)
        json.dump(state, open(state_p, 'w'))
        print(f'[{a.tag}] chunk {ci+1}/{len(chunks)} ({S} imgs): device-fooled {n_fooled_dev}  polished {n_pol}  '
              f'{dt:.0f}s  total {time.time()-T0:.0f}s', flush=True)
        del ch
        if dev.type == 'mps':
            torch.mps.empty_cache()

    # ---- assemble on top of stage 1
    x_adv = x_adv1.clone()
    best_arm_all = {}
    for ci, imgs in enumerate(chunks):
        z = np.load(os.path.join(a.ckpt, f'chunk_{ci:03d}.npz'), allow_pickle=False)
        xb = torch.from_numpy(z['x_best']); md = torch.from_numpy(z['margin_dev'])
        improve = md > m1[imgs]
        if improve.any():
            x_adv[imgs[improve]] = A.project64(xb[improve], x[imgs[improve]])
        for i_, ba in zip(imgs.numpy(), z['best_arm']):
            best_arm_all[int(i_)] = int(ba)
    mg_s = None
    if not a.no_cpu_verify:
        t0 = time.time()
        mg_s = A.cpu_margins(model_cpu, x_adv[surv], y[surv])
        n_fooled = int((mg_s > 0).sum()); n_weak = int(((mg_s > 0) & (mg_s < 1e-3)).sum())
        print(f'[{a.tag}] CPU verify ({time.time()-t0:.0f}s) on {surv.numel()} images: fooled {n_fooled}  '
              f'(weak <1e-3: {n_weak})  residual {surv.numel()-n_fooled}', flush=True)
    d, ev, rv = rb.eps_check_float64(x_adv, x)
    xp = os.path.join(a.out, f'x_adv_{a.tag}.npy')
    np.save(xp, x_adv.numpy().astype(np.float32))
    if mg_s is not None:
        mg_all = m1.clone(); mg_all[surv] = mg_s
        np.save(os.path.join(a.out, f'{a.tag}_cpu_margin.npy'), mg_all.numpy().astype(np.float32))
        np.save(os.path.join(a.out, f'{a.tag}_residual.npy'), surv[mg_s <= 0].numpy())
        np.save(os.path.join(a.out, f'{a.tag}_attacked.npy'), surv.numpy())
    json.dump({'best_arm': best_arm_all, 'arm_defs': arm_defs, 'rounds': rs, 'keep': keeps, 'K': K, 'L1': L1,
               'mode': a.mode, 'budget_per_image_max': budget}, open(os.path.join(a.out, f'{a.tag}_arms.json'), 'w'))
    rb.write_manifest(os.path.join(a.out, f'x_adv_{a.tag}.manifest.json'), model=a.model,
                      weights_sha256=wsha, test_images_sha256=hx, x_adv_sha256=rb.sha256_file(xp),
                      method=f'{a.mode}: {n_arms} arms {arm_defs} rounds {rs} keep {keeps} drop_margin {a.drop_margin} '
                             f'seed {a.seed} horizon {horizon}; on top of the stage-1 tensor',
                      device=str(dev), total_seconds=round(time.time() - T0, 1), max_linf=float(d.max()),
                      eps_violations=ev, range_violations=rv, n_attacked=int(surv.numel()),
                      n_fooled_cpu=(int((mg_s > 0).sum()) if mg_s is not None else None))
    print(f'[{a.tag}] DONE wrote {xp}  max Linf {d.max():.10f} eps_viol {ev} range_viol {rv}', flush=True)


if __name__ == '__main__':
    main()
