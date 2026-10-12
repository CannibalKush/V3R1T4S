"""
apgd_lib.py -- stateful, continuable APGD (Linf) with per-row loss selection, for budget-allocation search.

Re-implementation of Croce & Hein's APGD (arXiv:2003.01690; reference: fra31/auto-attack autopgd_base.py @ a3922004):
momentum 0.75, initial step 2*eps, checkpoint schedule p_0=0, p_1=0.22, p_{j+1}=p_j+max(p_j-p_{j-1}-0.03,0.06),
step halving when < rho=0.75 of the steps since the last checkpoint increased the loss or when neither the step nor the
best loss changed, restart from the best point.  Differences (all deliberate, all documented):
  * an ArmBatch keeps its whole optimiser state (x_adv, momentum term, grad, step size, best point, counters) so that a
    scheduler can run it for n steps, prune rows, and CONTINUE the survivors without wasting steps;
  * every row may use a different loss ('ce','cw','dlr','pm' untargeted; 'cw-t','dlr-t','pm-t','ce-t' targeted at
    row.target), selected with torch.where over the candidate losses (the forward/backward is shared);
  * the best-MARGIN iterate (max_{j!=y} z_j - z_y, over all classes) is tracked separately from the best-LOSS iterate;
    the margin is what the official count uses (ties = not fooled), so it is the scheduling reward and the returned point;
  * starts: 'rand' (uniform in the eps ball, like AA), 'zero' (x itself), 'corner' (x + eps*sign(grad_x loss)), or a
    given tensor (transfer / warm start).
Everything is float32 on the attack device; the final projection to the eps ball is done in float64 by the caller
(see project64) and successes are re-verified on CPU.
"""
import math
import torch
import torch.nn.functional as F

EPS = 8.0 / 255.0
LOSS_IDS = {'ce': 0, 'cw': 1, 'dlr': 2, 'pm': 3, 'cw-t': 4, 'dlr-t': 5, 'pm-t': 6, 'ce-t': 7}
TARGETED = {4, 5, 6, 7}


def margin_from_logits(z, y):
    """best_wrong_logit - true_logit  (> 0 means fooled; ties -> 0 -> NOT fooled)."""
    zy = z.gather(1, y.view(-1, 1)).squeeze(1)
    other = z.clone()
    other.scatter_(1, y.view(-1, 1), float('-inf'))
    return other.max(1).values - zy


def all_losses(z, y, t):
    """Return (R, 8) tensor of candidate per-row losses to MAXIMISE. t = target class (any int where untargeted)."""
    R = z.shape[0]
    u = torch.arange(R, device=z.device)
    zs, _ = z.sort(dim=1)
    zy = z[u, y]
    zt = z[u, t]
    # untargeted
    ce = F.cross_entropy(z, y, reduction='none')
    other = z.clone()
    other[u, y] = float('-inf')
    zmax_other = other.max(1).values
    cw = zmax_other - zy
    ind = (zs[:, -1] == zy).float()
    dlr = -(zy - zs[:, -2] * ind - zs[:, -1] * (1. - ind)) / (zs[:, -1] - zs[:, -3] + 1e-12)
    p = F.softmax(z, dim=1)
    py = p[u, y]
    pother = p.clone()
    pother[u, y] = -1.0
    pm = pother.max(1).values - py
    # targeted
    cw_t = zt - zy
    dlr_t = -(zy - zt) / (zs[:, -1] - 0.5 * (zs[:, -3] + zs[:, -4]) + 1e-12)
    pm_t = p[u, t] - py
    ce_t = -F.cross_entropy(z, t, reduction='none')
    return torch.stack([ce, cw, dlr, pm, cw_t, dlr_t, pm_t, ce_t], dim=1)


class ArmBatch:
    """R rows = (image, target, loss) arms.  All rows in a batch have taken the same number of steps."""

    def __init__(self, model, x, y, t, loss_id, horizon, eps=EPS, start='rand', x_init=None, seed=0, rho=0.75,
                 device=None):
        self.model = model
        self.eps = eps
        self.rho = rho
        dev = device or x.device
        self.dev = dev
        self.x = x.to(dev)
        self.y = y.to(dev)
        self.t = t.to(dev)
        self.loss_id = loss_id.to(dev)
        self.R = x.shape[0]
        self.horizon = horizon  # planned total steps (sets the checkpoint schedule, as n_iter does in APGD)
        self.n_iter_2 = max(int(0.22 * horizon), 1)
        self.n_iter_min = max(int(0.06 * horizon), 1)
        self.size_decr = max(int(0.03 * horizon), 1)
        self.k = self.n_iter_2
        self.counter3 = 0
        self.i = 0
        # ---- start point
        g = torch.Generator(device='cpu').manual_seed(int(seed))
        if x_init is not None:
            x_adv = x_init.to(dev).clone()
        elif start == 'rand':
            tt = (2 * torch.rand(x.shape, generator=g) - 1).to(dev)
            tt = tt / (tt.abs().flatten(1).max(1).values.view(-1, 1, 1, 1) + 1e-12)
            x_adv = self.x + eps * tt
        elif start == 'zero':
            x_adv = self.x.clone()
        elif start == 'corner':
            xg = self.x.clone().requires_grad_(True)
            with torch.enable_grad():
                L = self._loss(self.model(xg))
                gr, = torch.autograd.grad(L.sum(), xg)
            x_adv = self.x + eps * gr.sign()
        else:
            raise ValueError(start)
        x_adv = torch.min(torch.max(x_adv, self.x - eps), self.x + eps).clamp(0., 1.)
        self.x_adv = x_adv
        self.x_adv_old = x_adv.clone()
        # ---- first gradient
        logits, loss_indiv, grad = self._fwd_bwd(self.x_adv)
        self.grad = grad
        self.grad_best = grad.clone()
        self.loss_best = loss_indiv.clone()
        self.x_best = self.x_adv.clone()
        m = margin_from_logits(logits, self.y)
        self.margin_best = m.clone()
        self.x_best_margin = self.x_adv.clone()
        self.step_size = 2.0 * eps * torch.ones(self.R, 1, 1, 1, device=dev)
        self.loss_steps = torch.zeros(horizon + 1, self.R, device=dev)  # loss history (for the oscillation check)
        self.loss_best_last_check = self.loss_best.clone()
        self.reduced_last_check = torch.ones(self.R, device=dev)
        self.traj = [m.detach().cpu()]  # margin trajectory, one entry per step (auditable)

    # -- losses
    def _loss(self, z):
        allL = all_losses(z, self.y, self.t)
        return allL.gather(1, self.loss_id.view(-1, 1)).squeeze(1)

    def _fwd_bwd(self, x_adv):
        x_adv = x_adv.detach().requires_grad_(True)
        with torch.enable_grad():
            logits = self.model(x_adv)
            loss_indiv = self._loss(logits)
            grad, = torch.autograd.grad(loss_indiv.sum(), x_adv)
        return logits.detach(), loss_indiv.detach(), grad.detach()

    @torch.no_grad()
    def _check_oscillation(self, k):
        # fraction of the last k steps in which the loss increased, per row
        j = self.i  # loss_steps[j] is the current loss
        cnt = torch.zeros(self.R, device=self.dev)
        for c in range(k):
            cnt += (self.loss_steps[j - c] > self.loss_steps[j - c - 1]).float()
        return (cnt <= k * self.rho).float()

    def step(self, n):
        """Run n APGD iterations on all rows.  Returns nothing; read margin_best / x_best_margin."""
        eps = self.eps
        for _ in range(n):
            if self.i >= self.horizon:
                break
            with torch.no_grad():
                grad2 = self.x_adv - self.x_adv_old
                self.x_adv_old = self.x_adv.clone()
                a = 0.75 if self.i > 0 else 1.0
                x1 = self.x_adv + self.step_size * self.grad.sign()
                x1 = torch.min(torch.max(x1, self.x - eps), self.x + eps).clamp(0., 1.)
                x1 = torch.min(torch.max(self.x_adv + (x1 - self.x_adv) * a + grad2 * (1 - a), self.x - eps),
                               self.x + eps).clamp(0., 1.)
                self.x_adv = x1
            logits, loss_indiv, grad = self._fwd_bwd(self.x_adv)
            self.grad = grad
            with torch.no_grad():
                m = margin_from_logits(logits, self.y)
                upd = m > self.margin_best
                self.margin_best = torch.where(upd, m, self.margin_best)
                self.x_best_margin[upd] = self.x_adv[upd]
                self.traj.append(m.detach().cpu())
                self.i += 1
                self.loss_steps[self.i] = loss_indiv
                ind = loss_indiv > self.loss_best
                self.x_best[ind] = self.x_adv[ind]
                self.grad_best[ind] = grad[ind]
                self.loss_best = torch.where(ind, loss_indiv, self.loss_best)
                self.counter3 += 1
                if self.counter3 == self.k:
                    fl_osc = self._check_oscillation(self.k)
                    fl_no_impr = (1. - self.reduced_last_check) * (self.loss_best_last_check >= self.loss_best).float()
                    fl_osc = torch.max(fl_osc, fl_no_impr)
                    self.reduced_last_check = fl_osc.clone()
                    self.loss_best_last_check = self.loss_best.clone()
                    red = fl_osc > 0
                    if red.any():
                        self.step_size[red] /= 2.0
                        self.x_adv[red] = self.x_best[red]
                        self.grad[red] = self.grad_best[red]
                    self.k = max(self.k - self.size_decr, self.n_iter_min)
                    self.counter3 = 0

    def select(self, idx):
        """Return a new ArmBatch holding only rows idx (LongTensor on any device), state preserved."""
        idx = idx.to(self.dev)
        nb = ArmBatch.__new__(ArmBatch)
        nb.model, nb.eps, nb.rho, nb.dev = self.model, self.eps, self.rho, self.dev
        for name in ('x', 'y', 't', 'loss_id', 'x_adv', 'x_adv_old', 'grad', 'grad_best', 'loss_best', 'x_best',
                     'margin_best', 'x_best_margin', 'step_size', 'loss_best_last_check', 'reduced_last_check'):
            setattr(nb, name, getattr(self, name)[idx])
        nb.loss_steps = self.loss_steps[:, idx]
        nb.R = idx.numel()
        for name in ('horizon', 'n_iter_2', 'n_iter_min', 'size_decr', 'k', 'counter3', 'i'):
            setattr(nb, name, getattr(self, name))
        nb.traj = [tr[idx.cpu()] for tr in self.traj]
        return nb

    def trajectory(self):
        """(steps+1, R) CPU tensor of per-step margins."""
        return torch.stack(self.traj, 0)


def project64(x_adv, x, eps=EPS):
    """Final projection in float64, returned as float32.  The float32 cast can move a value by half an ulp (~3e-8)
    outside the ball; those elements are nudged one float32 ulp toward x so that max|x_adv-x| <= eps holds exactly in
    float64 (x itself is a float32 multiple of 1/255, so x +- eps is representable only approximately)."""
    xx = x.float().cpu()
    xa = torch.minimum(torch.maximum(x_adv.double().cpu(), xx.double() - eps), xx.double() + eps).clamp(0., 1.)
    xa = xa.float()
    for _ in range(3):
        d = xa.double() - xx.double()
        over = d.abs() > eps
        if not over.any():
            break
        toward = torch.nextafter(xa, xx)
        xa = torch.where(over, toward, xa)
    return xa.clamp(0., 1.)


@torch.no_grad()
def cpu_margins(model_cpu, x_adv, y, batch=250):
    out = []
    for i in range(0, x_adv.shape[0], batch):
        z = model_cpu(x_adv[i:i + batch].float()).float()
        out.append(margin_from_logits(z, y[i:i + batch]))
    return torch.cat(out, 0)


@torch.no_grad()
def device_margins(model, x_adv, y, device, batch=500):
    out = []
    for i in range(0, x_adv.shape[0], batch):
        z = model(x_adv[i:i + batch].to(device).float()).float()
        out.append(margin_from_logits(z, y[i:i + batch].to(device)).cpu())
    return torch.cat(out, 0)
