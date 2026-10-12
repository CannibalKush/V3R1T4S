"""Exact CP-SAT (OR-Tools) encoding of the VNN-COMP traffic_signs 3_30_30 BNN robustness query.

Search space (strictly inside the box, float32-exact): x_i = v_i + off_i + m * d_i with
  v_i = floor((lo_i+hi_i)/2) (integer), d_i integer in [lo_i - v_i, hi_i - v_i], m = 1 - 2^-PW,
  off_i = +2^-(PW+1) if v_i == lo_i, -2^-(PW+1) if v_i == hi_i, else 0   (PW = 9 by default).
Layer 1 preact a_j = t_j + rho_j with t_j = c_j + K_j integer (c_j = sum w v, K_j = sum w d) and
  |rho_j| <= 27 * (2^-(PW+1) + eps * 2^-PW) < 1.  So t_j >= 1 -> +1, t_j <= -1 -> -1.
  If no pixel of the receptive field has an offset, rho_j = -2^-PW K_j and the t_j = 0 case is decided by sign(c_j)
  (c_j >= 0 -> +1): s_j = [t_j >= 0] if c_j >= 0 else [t_j >= 1].  Otherwise t_j = 0 is forbidden.
Layer 2: s2_k = [u_k >= 0], u_k integer sum of +-1 over 2x2x16 inputs.  Logits exact integer.
Objective: maximize D = L_c - L_t for a chosen class c.  Stops when D >= 2 and the softmax margin >= 1e-5.

Usage: python -I cpsat_bnn30.py --vnnlib F --cls C [--onnx NET.onnx.gz] [--time 600] [--workers 4] [--out best.json]
                                [--hint best.json] [--pw 9] [--argmax] [--log]
The solver's random seed is OR-Tools' default (random_seed = 1); CP-SAT with several workers is not deterministic
across machines or thread timings, so a rerun may find a different solution (or none within the time limit).
"""
import argparse, json, os, sys, time
import numpy as np
from ortools.sat.python import cp_model
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bnn import BNN30, parse_box, softmax64, pixel_map

# default location of the benchmark ONNX after `python3 verify-it-yourself/vnncheck.py --cache downloads`
# (run from the family directory); override with --onnx
ONNX = 'downloads/benchmarks/traffic_signs_recognition_2023/2.0/onnx/3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.onnx.gz'


def build(net, pm, tgt, cls, argmax=False, hint=None):
    v, off, m, dmin, dmax = pm
    w1, w2, w3 = net.w1, net.w2, net.w3
    a1, h1, a2, h2, L = net.forward_int(v)
    # per-neuron max |K| given the pixel domains
    unst1 = {}
    for o in range(16):
        for y in range(28):
            for x in range(28):
                c = int(a1[o, y, x])
                kmin = kmax = 0
                has_off = False
                for ch in range(3):
                    for i in range(3):
                        for j in range(3):
                            wv = int(w1[o, ch, i, j]); lo_, hi_ = int(dmin[y + i, x + j, ch]), int(dmax[y + i, x + j, ch])
                            kmin += min(wv * lo_, wv * hi_); kmax += max(wv * lo_, wv * hi_)
                            has_off |= off[y + i, x + j, ch] != 0
                if c >= 0 and c + kmin >= (1 if has_off else 0): continue   # stays +1 for every d (t>=1 needed when offsets present)
                if c < 0 and c + kmax <= (-1 if has_off else 0): continue   # stays -1 for every d
                unst1[(o, y, x)] = (c, has_off)
    model = cp_model.CpModel()
    pix = {}
    def pixvar(h, w, ch):
        key = (h, w, ch)
        if key not in pix:
            pix[key] = model.NewIntVar(int(dmin[h, w, ch]), int(dmax[h, w, ch]), f'd_{h}_{w}_{ch}')
        return pix[key]
    s1 = {}
    n_strict = 0
    for (o, y, x), (c, has_off) in unst1.items():
        terms = []
        for ch in range(3):
            for i in range(3):
                for j in range(3):
                    terms.append(int(w1[o, ch, i, j]) * pixvar(y + i, x + j, ch))
        K = sum(terms)
        s = model.NewBoolVar(f's1_{o}_{y}_{x}')
        if has_off:
            n_strict += 1
            model.Add(K >= 1 - c).OnlyEnforceIf(s)            # t >= 1
            model.Add(K <= -1 - c).OnlyEnforceIf(s.Not())     # t <= -1
        else:
            theta = -c if c >= 0 else -c + 1                   # s <=> t >= 0 (c>=0) / t >= 1 (c<0)
            model.Add(K >= theta).OnlyEnforceIf(s)
            model.Add(K <= theta - 1).OnlyEnforceIf(s.Not())
        s1[(o, y, x)] = s
    # ---- layer 2
    s2 = {}; fixed2 = {}; n2_unst = 0
    for p in range(32):
        for y in range(27):
            for x in range(27):
                const = 0; terms = []
                for o in range(16):
                    for i in range(2):
                        for j in range(2):
                            wv = int(w2[p, o, i, j]); key = (o, y + i, x + j)
                            if key in s1:
                                terms.append(wv * s1[key]); const -= wv
                            else:
                                const += wv * int(h1[o, y + i, x + j])
                k = (y * 27 + x) * 32 + p
                if not terms:
                    fixed2[k] = 1 if const >= 0 else -1; continue
                nt = len(terms)
                if const - 2 * nt >= 0: fixed2[k] = 1; continue
                if const + 2 * nt <= -1: fixed2[k] = -1; continue
                u = const + 2 * sum(terms)
                s = model.NewBoolVar(f's2_{k}')
                model.Add(u >= 0).OnlyEnforceIf(s)
                model.Add(u <= -1).OnlyEnforceIf(s.Not())
                s2[k] = s; n2_unst += 1
    def logit_diff(cc, tt):
        const = 0; terms = []
        for k in range(23328):
            dw = int(w3[k, cc] - w3[k, tt])
            if dw == 0: continue
            if k in s2: terms.append(2 * dw * s2[k]); const -= dw
            else: const += dw * fixed2[k]
        return const, terms
    const, terms = logit_diff(cls, tgt)
    model.Maximize(const + sum(terms))
    if argmax:
        for b in range(43):
            if b in (cls, tgt): continue
            cb, tb = logit_diff(cls, b); model.Add(cb + sum(tb) >= 0)
    if hint is not None:
        for key, var in pix.items(): model.AddHint(var, int(hint[key]))
    info = dict(n_unst1=len(unst1), n_strict_rule=n_strict, n_pix=len(pix), n_unst2=n2_unst, centre_D=int(L[cls] - L[tgt]), obj_const=const, n_obj_terms=len(terms))
    return model, pix, s1, s2, info


class CB(cp_model.CpSolverSolutionCallback):
    def __init__(self, pix, pm, tgt, cls, net, out, t0, pw):
        super().__init__(); self.pix, self.pm, self.tgt, self.cls, self.net, self.out, self.t0, self.pw = pix, pm, tgt, cls, net, out, t0, pw
        self.best = None
    def on_solution_callback(self):
        v, off, m, dmin, dmax = self.pm
        d = np.zeros((30, 30, 3), dtype=np.int64)
        for (h, w, ch), var in self.pix.items(): d[h, w, ch] = self.Value(var)
        x = v.astype(np.float64) + off + m * d
        a1, h1, a2, h2, L = self.net.forward_int(x)
        D = int(L[self.cls] - L[self.tgt]); obj = self.ObjectiveValue()
        Y = softmax64(L); ymargin = float(Y[self.cls] - Y[self.tgt])
        print(f'[{time.time()-self.t0:7.1f}s] solution obj={obj:.0f} surrogate D={D} argmax={int(L.argmax())} L_cls={L[self.cls]} L_t={L[self.tgt]} '
              f'n_pix_changed={int((d != 0).sum())} min|a1|={float(np.abs(a1).min()):.4f} ymargin={ymargin:.4g}', flush=True)
        assert D == int(obj), 'model/surrogate mismatch'
        self.best = dict(obj=D, d=d.reshape(-1).tolist(), argmax=int(L.argmax()), L=L.tolist(), t=time.time() - self.t0, ymargin=ymargin, pw=self.pw)
        json.dump(self.best, open(self.out, 'w'))
        if D >= 2 and ymargin >= 1e-5:
            print(f'*** PROPERTY-SATISFYING SOLUTION FOUND (surrogate): D={D} softmax margin {ymargin:.4g} ***', flush=True)
            self.StopSearch()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vnnlib', required=True); ap.add_argument('--cls', type=int, required=True)
    ap.add_argument('--onnx', default=ONNX)
    ap.add_argument('--time', type=float, default=600); ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--argmax', action='store_true'); ap.add_argument('--out', default='best.json')
    ap.add_argument('--hint', default=None); ap.add_argument('--pw', type=int, default=9); ap.add_argument('--log', action='store_true')
    args = ap.parse_args()
    net = BNN30(args.onnx)
    lo, hi, tgt = parse_box(args.vnnlib)
    pm = pixel_map(lo, hi, args.pw)
    hint = np.array(json.load(open(args.hint))['d']).reshape(30, 30, 3) if args.hint else None
    t0 = time.time()
    model, pix, s1, s2, info = build(net, pm, tgt, args.cls, argmax=args.argmax, hint=hint)
    print('model built in %.1fs:' % (time.time() - t0), info, 'target', tgt, 'pw', args.pw, flush=True)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time; solver.parameters.num_workers = args.workers
    solver.parameters.log_search_progress = args.log
    cb = CB(pix, pm, tgt, args.cls, net, args.out, t0, args.pw)
    st = solver.Solve(model, cb)
    print('status', solver.StatusName(st), 'obj', solver.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
          'bound', solver.BestObjectiveBound(), 'wall %.1fs' % (time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
