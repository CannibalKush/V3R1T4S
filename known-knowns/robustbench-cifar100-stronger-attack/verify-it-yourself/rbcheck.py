#!/usr/bin/env python3
"""
rbcheck.py -- standalone checker for the adversarial CIFAR-100 tensor against RobustBench's Addepalli2022Efficient_RN18.

  1. loads the tensor from ../adversarial-examples/x_adv_Addepalli2022Efficient_RN18.npz and checks that it is
     bit-identical to the original (sha256, see unpack.py);
  2. loads the CIFAR-100 test set exactly as RobustBench does (robustbench.data.load_cifar100: torchvision CIFAR100,
     train=False, ToTensor only, standard order, fine labels) and checks its sha256;
  3. checks the threat model on ALL 10,000 images in float64: max |x_adv - x| <= 8/255 (no tolerance), 0 <= x_adv <= 1,
     all values finite;
  4. loads the unmodified model with robustbench.utils.load_model('Addepalli2022Efficient_RN18', dataset='cifar100',
     threat_model='Linf') in eval mode (downloads the weights on first use, about 45 MB) and checks the weights' sha256;
  5. counts clean-correct images and robust images on CPU in float32. An image counts as robust when it is
     clean-correct and, on x_adv, the true-class logit is >= every other logit (a tie counts as robust, in the model's
     favour). RobustBench's AutoAttack value for this model is 27.67 % = 2,767 images.

Requirements: python3, numpy, torch, torchvision, robustbench (pip install git+https://github.com/RobustBench/robustbench@78fcc9e48a07a861268f295a777b975f25155964).

  python3 rbcheck.py --data_dir DATA --model_dir MODELS                 # full check (2 x 10,000 forward passes)
  python3 rbcheck.py --data_dir DATA --model_dir MODELS --n 500         # quick check on images 0..499
Runtime: about 50 s for --n 500 on 4 CPU threads of a busy machine, so roughly 10-20 minutes for the full check.
Exit 0 iff every check passes (with --n < 10000 the counts are compared with robust_indices.txt for those images).
"""
import argparse, hashlib, os, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import unpack  # noqa: E402

MODEL = 'Addepalli2022Efficient_RN18'
WEIGHTS_SHA256 = 'aafda6c19381b62fdb09aa6905331bcaa0341eac76c5080d2a99a95f8ac18587'
TEST_UINT8_SHA256 = '4cb8e5d9309da489bf6b19cc10cd96c3ae6f8daf225380b605aaee4c0d6aee19'   # dataset.data, (10000,32,32,3) uint8
LABELS_INT64_SHA256 = '80031c23f8300724c6fbc588e4bccbe41c6392041782148727bb497b0132c4ad'
EPS = 8.0 / 255.0
CLEAN_EXPECTED, ROBUST_EXPECTED, BAR_IMAGES = 6545, 2757, 2767


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data_dir', default='./data')
    ap.add_argument('--model_dir', default='./models')
    ap.add_argument('--n', type=int, default=10000, help='evaluate the model on images 0..n-1 (feasibility is always checked on all)')
    ap.add_argument('--batch', type=int, default=200)
    ap.add_argument('--threads', type=int, default=4)
    a = ap.parse_args()
    import torch
    import robustbench
    from robustbench.data import load_cifar100
    from robustbench.utils import load_model
    torch.set_num_threads(a.threads)
    ok = True
    t0 = time.time()

    xa = unpack.load()                                       # asserts bit-identity with the original tensor
    print(f'x_adv: {xa.dtype} {xa.shape}, bit-identical to the original (.npy sha256 {unpack.ORIGINAL_NPY_SHA256})')
    ok &= xa.shape == (10000, 3, 32, 32) and xa.dtype == np.float32

    x, y = load_cifar100(n_examples=10000, data_dir=a.data_dir)
    import torchvision
    raw = torchvision.datasets.CIFAR100(root=a.data_dir, train=False, download=False)
    ts = hashlib.sha256(np.ascontiguousarray(raw.data).tobytes()).hexdigest()
    ls = hashlib.sha256(y.numpy().astype(np.int64).tobytes()).hexdigest()
    print(f'CIFAR-100 test set: images sha256 {ts} {"ok" if ts == TEST_UINT8_SHA256 else "MISMATCH"}; '
          f'labels sha256 {ls} {"ok" if ls == LABELS_INT64_SHA256 else "MISMATCH"}')
    ok &= ts == TEST_UINT8_SHA256 and ls == LABELS_INT64_SHA256
    xc = x.numpy()

    d = np.abs(xa.astype(np.float64) - xc.astype(np.float64))
    linf = float(d.max())
    n_over = int((d > EPS).sum())
    n_range = int(((xa < 0) | (xa > 1)).sum())
    finite = bool(np.isfinite(xa).all())
    unchanged = int((d.reshape(10000, -1) == 0).all(1).sum())
    print(f'threat model (float64, all 10000 images): max Linf {linf!r} (8/255 = {EPS!r}); coordinates above 8/255: {n_over}; '
          f'outside [0,1]: {n_range}; all finite: {finite}; images left unchanged: {unchanged}')
    ok &= n_over == 0 and n_range == 0 and finite

    model = load_model(MODEL, model_dir=a.model_dir, dataset='cifar100', threat_model='Linf').eval()
    wpath = os.path.join(a.model_dir, 'cifar100', 'Linf', MODEL + '.pt')
    ws = hashlib.sha256(open(wpath, 'rb').read()).hexdigest()
    try:
        from importlib.metadata import version
        rbv = version('robustbench')
    except Exception:
        rbv = '?'
    print(f'model {MODEL} (robustbench {rbv}, torch {torch.__version__}): '
          f'weights sha256 {ws} {"ok" if ws == WEIGHTS_SHA256 else "MISMATCH"}')
    ok &= ws == WEIGHTS_SHA256

    n = a.n
    def margins(arr):
        out = []
        with torch.no_grad():
            for i in range(0, n, a.batch):
                lo = model(torch.from_numpy(np.ascontiguousarray(arr[i:min(i + a.batch, n)]))).double()
                yy = y[i:min(i + a.batch, n)]
                true = lo.gather(1, yy[:, None]).squeeze(1)
                lo2 = lo.clone(); lo2[torch.arange(len(yy)), yy] = -float('inf')
                out.append((lo2.max(1).values - true).numpy())   # > 0: another class wins (misclassified)
        return np.concatenate(out)
    t1 = time.time(); mc = margins(xc); tc = time.time() - t1
    t1 = time.time(); ma = margins(xa); tr = time.time() - t1
    clean_ok = mc <= 0
    robust = clean_ok & (ma <= 0)
    ties = int(((mc == 0) | (ma == 0)).sum())
    fooled_close = np.sort(ma[clean_ok & (ma > 0)])[:3]
    print(f'images 0..{n - 1}: clean-correct {int(clean_ok.sum())}, robust {int(robust.sum())}, exact ties {ties} '
          f'({tc:.0f} s clean, {tr:.0f} s adversarial on {a.threads} CPU threads)')
    print(f'  smallest positive margins among fooled images: {fooled_close.tolist()}')
    exp_idx = np.loadtxt(os.path.join(os.path.dirname(HERE), 'adversarial-examples', 'robust_indices.txt'), dtype=np.int64)
    exp_mask = np.zeros(10000, bool); exp_mask[exp_idx] = True
    same = bool((robust == exp_mask[:n]).all())
    print(f'  robust set equals robust_indices.txt on these images: {same} ({int(exp_mask[:n].sum())} expected)')
    ok &= same
    if n == 10000:
        print(f'FULL TEST SET: clean {int(clean_ok.sum())}/10000 (RobustBench clean_acc 65.45 % = 6545), '
              f'robust {int(robust.sum())}/10000 vs RobustBench AutoAttack 27.67 % = {BAR_IMAGES}: '
              f'{BAR_IMAGES - int(robust.sum())} images below')
        ok &= int(clean_ok.sum()) == CLEAN_EXPECTED and int(robust.sum()) == ROBUST_EXPECTED
    print(f"RBCHECK {'PASS' if ok else 'FAIL'} model={MODEL} n={n} clean={int(clean_ok.sum())} robust={int(robust.sum())} "
          f"max_linf={linf!r} runtime={time.time() - t0:.0f}s")
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
