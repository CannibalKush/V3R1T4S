#!/usr/bin/env python
"""
make_cr_attack.py -- builds cr_attack_vendored.py, the CR Attack implementation used by cr_residual.py (stage 3).

CR Attack (constraint-relaxation attack) is by Pan, Wu, Tang, Li, Yao, "Efficient Robustness Evaluation via Constraint
Relaxation", AAAI 2025; code at https://github.com/fzjcdt/constraint-relaxation-attack .  That repository has no licence
file, so its code is NOT redistributed here.  This script downloads the original file attacks/attacks/cr_attack.py,
checks that it is the exact version we used (sha256 below; fetched 2026-10-10 from the main branch, repository tree
31a17e63091ad71e3c6c5298c952785bf79aa74c), and applies the small adaptation we made, as line edits:
  * the torchattacks-style base class and the repository's Logger are dropped (self.model / self.device are set
    directly, logging goes to print);
  * the CUDA seeding call is guarded and the MPS generator is seeded as well;
  * every torch.arange(n) used as a row index is created on the model's device (needed on Apple MPS);
  * the potential threshold 0.05 becomes a parameter potential_thresh (default 0.05 = the published value).
With the defaults the attack arithmetic is the published one.  The result is checked against the sha256 of the file we
ran (df5357e0...176f).

  python make_cr_attack.py                      # download, patch, verify, write ./cr_attack_vendored.py
  python make_cr_attack.py --src cr_attack.py   # use an already downloaded copy instead
"""
import argparse, hashlib, os, urllib.request

URL = 'https://raw.githubusercontent.com/fzjcdt/constraint-relaxation-attack/main/attacks/attacks/cr_attack.py'
UPSTREAM_SHA256 = '91320622fee2d1221bd074fd73a1379e38da366bbe8cf94ca1bba61401f26254'
RESULT_SHA256 = 'df5357e045d86c5c3d0736ca5ad56ceae29ba382367f22bb4bcf3ec2481f176f'

# (first line, end line, replacement text) on the 0-based line list of the upstream file, applied bottom-up
EDITS = [
    (0, 0, '"""\ncr_attack_vendored.py -- CR Attack (Constraint Relaxation attack) of Pan, Wu, Tang, Li, Yao,\n"Efficient Robustness Evaluation via Constraint Relaxation", AAAI 2025.\n\nVendored from the public code https://github.com/fzjcdt/constraint-relaxation-attack (attacks/cr_attack.py), local copy\n<run dir>/data/live/cr_attack_code/cr_attack.py, sha256 91320622fee2d1221bd074fd73a1379e38da366bbe8cf94ca1bba61401f26254.\n\nModifications (ONLY these; the attack arithmetic is byte-for-byte the published one):\n  * dropped `from ..attack import Attack` (torchattacks-style base) and `from utils import Logger`: a minimal base sets\n    self.model / self.device from the model\'s parameters, logging goes to print;\n  * `torch.cuda.random.manual_seed` guarded (no CUDA on this host); the MPS generator is seeded as well;\n  * every `torch.arange(n)` used as a row index is created on the model\'s device (CUDA tolerates CPU index tensors, MPS may not);\n  * optional `potential_thresh` (published 0.05) and `restart_thresh_scale` (published 1.0) knobs for the EXTENDED variant;\n    with the defaults the algorithm is exactly the published one.\n"""\n'),
    (1, 1, '\n'),
    (4, 5, ''),
    (6, 10, 'class CRAttack:\n'),
    (15, 28, '                 max_iter=150, decay_steps=30, target_numbers=3, restart=5, random_start=True, seed=0, log_path=None,\n                 potential_thresh=0.05, verbose=False):\n        self.attack = "CR Attack"\n        self.model = model\n        self.device = next(model.parameters()).device\n'),
    (29, 30, "        if torch.cuda.is_available():\n            torch.cuda.random.manual_seed(seed)\n        if hasattr(torch, 'mps') and torch.backends.mps.is_available():\n            torch.mps.manual_seed(seed)\n"),
    (37, 41, '        self.potential_thresh = potential_thresh\n        self.verbose = verbose\n        self.logger = None\n'),
    (45, 46, '        u = torch.arange(x.shape[0], device=logits.device)\n'),
    (54, 55, '        u = torch.arange(x.shape[0], device=logits.device)\n'),
    (185, 186, '                u = torch.arange(cur_adv_images.shape[0], device=self.device)\n'),
    (194, 195, '                    potential_idx[target_index][idx_to_fool[(margin_min < self.potential_thresh).nonzero().flatten()]] = True\n'),
    (236, 237, '                    potential_idx[target_index][idx_to_fool[(margin_min < self.potential_thresh).nonzero().flatten()]] = True\n'),
    (313, 317, '            print(f"Batch {i // bs + 1}/{len(x_orig) // bs}: {success} out of {len(x_batch)} successfully perturbed, Forward: {f_num.sum().item()}, Backward: {b_num.sum().item()}, Total time: {round(time.time() - start_time, 1)} s", flush=True)\n'),
    (318, 322, ''),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=None, help='local copy of upstream attacks/attacks/cr_attack.py (else download)')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cr_attack_vendored.py'))
    a = ap.parse_args()
    if a.src:
        data = open(a.src, 'rb').read()
    else:
        req = urllib.request.Request(URL, headers={'User-Agent': 'cr-attack-fetch (one GET)'})
        data = urllib.request.urlopen(req, timeout=60).read()
    h = hashlib.sha256(data).hexdigest()
    if h != UPSTREAM_SHA256:
        raise SystemExit(f'upstream cr_attack.py has sha256 {h}, expected {UPSTREAM_SHA256} (the file changed upstream; '
                         'the line edits below apply to the 2026-10-10 version only)')
    lines = data.decode('utf-8').splitlines(keepends=True)
    for i1, i2, new in reversed(EDITS):
        lines[i1:i2] = new.splitlines(keepends=True)
    out = ''.join(lines).encode('utf-8')
    h2 = hashlib.sha256(out).hexdigest()
    if h2 != RESULT_SHA256:
        raise SystemExit(f'patched file sha256 {h2} != expected {RESULT_SHA256}')
    with open(a.out, 'wb') as f:
        f.write(out)
    print(f'wrote {a.out} (sha256 {h2}, identical to the file used in the original run)')


if __name__ == '__main__':
    main()
