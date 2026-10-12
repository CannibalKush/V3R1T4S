"""
rb_common.py -- shared loading / verification helpers used by every stage of the pipeline.

Conventions:
  * x in [0,1], shape (N,3,32,32) float32, canonical torchvision CIFAR100(train=False) order, fine labels
    (N = 10000 for the real run; --n_test N restricts every stage to the first N test images for smoke tests).
  * The RobustBench model normalises internally; never normalise before calling it.
  * Official counts are CPU float32 with ties counted as NOT fooled (logit[y] >= max logit).  A GPU (Apple MPS in the
    original run) is used for the attack loops only; every success is re-verified on CPU.

Call configure(data_dir, model_dir, n_images) once at the start of a script (every stage exposes --data_dir,
--model_dir and --n_test).  The model weights are fetched by RobustBench's own downloader on first use if they are
not in model_dir; the CIFAR-100 test set is fetched by torchvision (md5-checked) if it is not in data_dir.
"""
import hashlib, json, os, time

import numpy as np
import torch

DATA_DIR = './data'
MODEL_DIR = './models'
N_IMAGES = 10000
EPS = 8.0 / 255.0


def configure(data_dir=None, model_dir=None, n_images=None):
    global DATA_DIR, MODEL_DIR, N_IMAGES
    if data_dir:
        DATA_DIR = data_dir
    if model_dir:
        MODEL_DIR = model_dir
    if n_images:
        N_IMAGES = int(n_images)


def add_common_args(ap):
    ap.add_argument('--data_dir', default='./data', help='torchvision CIFAR-100 root (contains cifar-100-python/)')
    ap.add_argument('--model_dir', default='./models', help='RobustBench model_dir (contains cifar100/Linf/<model>.pt)')
    ap.add_argument('--n_test', type=int, default=10000, help='use only the first N test images (smoke tests)')


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def pick_device(prefer='mps'):
    if prefer == 'mps' and torch.backends.mps.is_available():
        return torch.device('mps')
    if prefer == 'cuda' and torch.cuda.is_available():
        return torch.device('cuda')
    return torch.device('cpu')


def load_cifar100_test(data_dir=None):
    """Returns x float32 (N,3,32,32) in [0,1], y int64 (N,), sha256 of the raw uint8 images of the FULL test set."""
    import torchvision
    import torchvision.transforms as T
    ds = torchvision.datasets.CIFAR100(root=data_dir or DATA_DIR, train=False, download=True, transform=T.ToTensor())
    assert len(ds) == 10000
    raw = np.ascontiguousarray(ds.data)
    h = hashlib.sha256(raw.tobytes()).hexdigest()
    y = torch.from_numpy(np.asarray(ds.targets, dtype=np.int64))
    x = torch.from_numpy(raw).permute(0, 3, 1, 2).contiguous().to(torch.float32).div_(255.0)
    n = N_IMAGES
    return x[:n].contiguous(), y[:n].contiguous(), h


def load_rb_model(name, device='cpu', model_dir=None):
    """Unmodified robustbench loader; returns (model.eval() on device, weights path, weights sha256)."""
    from robustbench.utils import load_model
    model_dir = model_dir or MODEL_DIR
    m = load_model(name, model_dir=model_dir, dataset='cifar100', threat_model='Linf').eval()
    for p in m.parameters():
        p.requires_grad_(False)
    wpath = os.path.join(model_dir, 'cifar100', 'Linf', f'{name}.pt')
    return m.to(device), wpath, (sha256_file(wpath) if os.path.isfile(wpath) else None)


@torch.no_grad()
def logits(model, x, batch=250, device='cpu'):
    out = []
    for i in range(0, x.shape[0], batch):
        out.append(model(x[i:i + batch].to(device=device, dtype=torch.float32)).float().cpu())
    return torch.cat(out, 0)


def not_fooled_mask(lg, y):
    """True = still correct (ties count as NOT fooled)."""
    return lg.gather(1, y.view(-1, 1)).squeeze(1) >= lg.max(1).values


def margin(lg, y):
    """best_wrong_logit - true_logit; > 0 means fooled."""
    true = lg.gather(1, y.view(-1, 1)).squeeze(1)
    other = lg.clone()
    other.scatter_(1, y.view(-1, 1), float('-inf'))
    return other.max(1).values - true


def clean_gate(model, x, y, table_clean_acc, batch=250, device='cpu'):
    """Recompute clean accuracy on CPU and require |clean - clean_acc| <= 0.05 (only on the full test set).
    Returns (clean_acc, correct_mask)."""
    lg = logits(model, x, batch, device)
    correct = lg.argmax(1) == y
    n = x.shape[0]
    acc = 100.0 * correct.float().mean().item()
    if n != 10000:
        print(f'[clean gate] subset of {n} images: {int(correct.sum())}/{n} correct (gate applies to the full test set only)')
        return acc, correct
    ok = abs(acc - table_clean_acc) <= 0.05
    print(f'[clean gate] {int(correct.sum())}/10000 = {acc:.2f}%  table {table_clean_acc}  diff {abs(acc - table_clean_acc):.3f}  '
          f'-> {"OK" if ok else "FAIL"}')
    if not ok:
        raise SystemExit('clean accuracy gate failed: wrong model / data / labels')
    return acc, correct


def project(x_adv, x, eps=EPS):
    """Project onto the Linf ball and [0,1]; done in float32 like AutoAttack."""
    return torch.min(torch.max(x_adv, x - eps), x + eps).clamp_(0.0, 1.0)


def eps_check_float64(x_adv, x, eps=EPS, tol=1e-6):
    d = (x_adv.double() - x.double()).abs().flatten(1).max(1).values
    rng = ((x_adv.double() < 0) | (x_adv.double() > 1)).flatten(1).any(1)
    return d, int((d > eps + tol).sum()), int(rng.sum())


def cpu_verify(model_cpu, x_adv, y, batch=250):
    """Official count on CPU float32. Returns (not_fooled_mask, margins)."""
    lg = logits(model_cpu, x_adv, batch, 'cpu')
    return not_fooled_mask(lg, y), margin(lg, y)


def write_manifest(path, **kw):
    kw.setdefault('time_utc', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    kw.setdefault('torch', torch.__version__)
    with open(path, 'w') as f:
        json.dump(kw, f, indent=1, default=str)
    return path
