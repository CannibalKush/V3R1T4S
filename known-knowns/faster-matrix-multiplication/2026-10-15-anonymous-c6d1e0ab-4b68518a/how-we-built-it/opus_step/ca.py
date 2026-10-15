"""Consensus absorption (opus-fmm).

Absorption on the (U,V) pairing: with an exact kernel basis lam^(1..k) of sum_t lam_t U_t (x) V_t = 0 and
ell_t in Q^k the coordinates of term t, any linear Phi: Q^k -> Q^(n3 n1) gives a valid scheme
W_t -> W_t + Phi(ell_t). Term t dies iff W_t = -Phi(ell_t).  Equivalently, with y_t = (ell_t, W_t), the
killed set is the set of points lying in a k-dimensional subspace H transverse to {0} x Q^m.  We search for
the H holding the largest number of terms:

  greedy  : the supplied rule (largest (ray, W) clusters with independent rays), as in data/sa.py
  flat    : grow H one point at a time; at each step group all remaining points by their direction in the
            quotient by H (a whole group joins H together) and take the heaviest admissible group
  beam    : the same growth as a beam search (width/branching), plus randomized restarts

The search runs modulo a 31-bit prime on two random projections of W.  The chosen basis is then rebuilt
over Q with the supplied exact solver, applied exactly, and the exact kills are recounted.  Kernels come
from codex-fmm's verified exact kernel provider (fast_sa.exact_kernel), unchanged.
"""
import os
import sys
import random
import time
from fractions import Fraction
from collections import defaultdict

import numpy as np

FMM = '[workspace path]'
OPUS = FMM + '/opus'
sys.path.insert(0, FMM)
sys.path.insert(0, FMM + '/data')
os.chdir(OPUS)  # fast_sa writes kernel scratch into ./work (= opus/work)
import fast_sa  # noqa: E402  (installs the exact kernel provider into sa)
import sa  # noqa: E402

P = 2147483647  # 2^31 - 1


def modp(x):
    return (x.numerator % P) * pow(x.denominator % P, P - 2, P) % P


class Kernel:
    """Exact kernel data for one pairing, plus clusters and their mod-p points."""

    def __init__(self, terms, basis, rng):
        self.k = len(basis)
        sup = sorted(set().union(*[set(v) for v in basis]))
        self.sup = sup
        self.ell = {t: [b.get(t, Fraction(0)) for b in basis] for t in sup}
        clusters = defaultdict(list)
        order = []
        for t in sup:
            lt = self.ell[t]
            nz = next((x for x in lt if x != 0), None)
            if nz is None:
                continue
            ray = tuple(x / nz for x in lt)
            W = terms[t][2]
            val = tuple(sorted((a, x / nz) for a, x in W.items()))
            key = (ray, val)
            if key not in clusters:
                order.append(key)
            clusters[key].append(t)
        self.keys = order
        self.members = [clusters[key] for key in order]
        self.weight = np.array([len(m) for m in self.members], dtype=np.int64)
        m = max(a for t in sup for a in terms[t][2]) + 1
        g = [[rng.randrange(1, P) for _ in range(m)] for _ in range(2)]
        Y = np.zeros((len(order), self.k + 2), dtype=np.int64)
        for c, (ray, val) in enumerate(order):
            for j, x in enumerate(ray):
                Y[c, j] = modp(x)
            for q in range(2):
                s = 0
                for a, x in val:
                    s = (s + modp(x) * g[q][a]) % P
                Y[c, self.k + q] = s
        self.Y = Y


def _normalize_rows(R):
    """Projective keys of the rows of R (mod P): bytes of row / first nonzero; zero rows -> None."""
    keys = []
    for row in R:
        nzi = np.flatnonzero(row)
        if len(nzi) == 0:
            keys.append(None)
            continue
        inv = pow(int(row[nzi[0]]), P - 2, P)
        keys.append(((row * inv) % P).tobytes())
    return keys


class Flat:
    """A subspace H of F_p^(k+2) in echelon form, spanned by chosen cluster points."""

    def __init__(self, kern):
        self.kern = kern
        self.rows = []  # (pivot, row) with row[pivot] == 1
        self.chosen = []

    def copy(self):
        f = Flat(self.kern)
        f.rows = list(self.rows)
        f.chosen = list(self.chosen)
        return f

    def reduce(self, Y):
        R = Y.copy()
        for piv, row in self.rows:
            col = R[:, piv].copy()
            nzm = col != 0
            if not nzm.any():
                continue
            R[nzm] = (R[nzm] - (col[nzm, None] * row[None, :]) % P) % P
        return R

    def add(self, c):
        r = self.reduce(self.kern.Y[c:c + 1])[0]
        nzi = np.flatnonzero(r)
        assert len(nzi)
        piv = int(nzi[0])
        inv = pow(int(r[piv]), P - 2, P)
        r = (r * inv) % P
        new = []
        for p2, row in self.rows:
            if row[piv]:
                row = (row - (row[piv] * r) % P) % P
            new.append((p2, row))
        new.append((piv, r))
        self.rows = new
        self.chosen.append(c)

    def ray_rank_ok(self, c):
        """Transversality: is the ray of c outside the span of the chosen rays?"""
        k = self.kern.k
        M = [list(map(int, self.kern.Y[x, :k])) for x in self.chosen] + [list(map(int, self.kern.Y[c, :k]))]
        return _rank_mod(M) == len(M)

    def closure(self):
        R = self.reduce(self.kern.Y)
        return np.flatnonzero(~R.any(axis=1))


def _rank_mod(M):
    M = [list(r) for r in M]
    rank = 0
    cols = len(M[0]) if M else 0
    for col in range(cols):
        sel = next((i for i in range(rank, len(M)) if M[i][col] % P), None)
        if sel is None:
            continue
        M[rank], M[sel] = M[sel], M[rank]
        inv = pow(M[rank][col], P - 2, P)
        M[rank] = [x * inv % P for x in M[rank]]
        for i in range(len(M)):
            if i != rank and M[i][col] % P:
                f = M[i][col]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[rank])]
        rank += 1
    return rank


def candidate_groups(flat, closed_mask):
    """Groups of not-yet-closed clusters by direction in the quotient by H, heaviest first.
    Returns list of (weight, representative, members)."""
    kern = flat.kern
    idx = np.flatnonzero(~closed_mask)
    if len(idx) == 0:
        return []
    R = flat.reduce(kern.Y[idx])
    keys = _normalize_rows(R)
    groups = defaultdict(list)
    for c, key in zip(idx, keys):
        if key is not None:
            groups[key].append(int(c))
    out = []
    for key, mem in groups.items():
        w = int(kern.weight[mem].sum())
        out.append((w, mem[0], mem))
    out.sort(key=lambda x: (-x[0], x[1]))
    return out


def search(kern, method='beam', width=6, branch=3, restarts=20, rng=None):
    """Return (best kill weight, chosen cluster indices) for this kernel."""
    k = kern.k
    rng = rng or random.Random(1)
    if method in ('greedy', 'rgreedy'):
        chosen = []
        span = []
        if method == 'greedy':
            order = sorted(range(len(kern.keys)), key=lambda c: -kern.weight[c])
        else:
            order = sorted(range(len(kern.keys)), key=lambda c: (-kern.weight[c], rng.random()))
        for c in order:
            ray = list(kern.keys[c][0])
            r = list(ray)
            for piv, row in span:
                if r[piv] != 0:
                    fct = r[piv] / row[piv]
                    r = [x - fct * y for x, y in zip(r, row)]
            piv = next((i for i, x in enumerate(r) if x != 0), None)
            if piv is None:
                continue
            span.append((piv, r))
            chosen.append(c)
            if len(chosen) == k:
                break
        f = Flat(kern)
        for c in chosen:
            f.add(c)
        cl = f.closure()
        return int(kern.weight[cl].sum()), chosen

    if method == 'rflat':
        # flat growth, uniformly random among the heaviest admissible groups at every step
        fl = Flat(kern)
        for depth in range(k):
            cl = fl.closure()
            mask = np.zeros(len(kern.keys), dtype=bool)
            mask[cl] = True
            groups = [g for g in candidate_groups(fl, mask) if fl.ray_rank_ok(g[1])]
            if not groups:
                break
            top = groups[0][0]
            ties = [g for g in groups if g[0] == top]
            fl.add(ties[rng.randrange(len(ties))][1])
        return int(kern.weight[fl.closure()].sum()), list(fl.chosen)

    def expand(flat, nbranch, noise):
        cl = flat.closure()
        mask = np.zeros(len(kern.keys), dtype=bool)
        mask[cl] = True
        groups = candidate_groups(flat, mask)
        out = []
        if noise:
            groups = sorted(groups, key=lambda g: -(g[0] * (1 + noise * rng.random())))
        for w, rep, mem in groups:
            # pick a transverse representative from the group (all members are equivalent if one is)
            if not flat.ray_rank_ok(rep):
                continue
            out.append((w, rep))
            if len(out) >= nbranch:
                break
        return out

    best = (-1, [])
    beams = [Flat(kern)]
    for depth in range(k):
        cand = []
        for fl in beams:
            opts = expand(fl, branch if method == 'beam' else 1, 0.0)
            if not opts:
                cand.append((int(kern.weight[fl.closure()].sum()), fl, True))
            for w, rep in opts:
                f2 = fl.copy()
                f2.add(rep)
                cand.append((int(kern.weight[f2.closure()].sum()), f2, False))
        seen = set()
        nb = []
        for w, fl, done in sorted(cand, key=lambda x: -x[0]):
            key = tuple(sorted(fl.closure().tolist()))
            if key in seen:
                continue
            seen.add(key)
            if w > best[0]:
                best = (w, list(fl.chosen))
            if not done:
                nb.append(fl)
            if len(nb) >= (width if method == 'beam' else 1):
                break
        beams = nb
        if not beams:
            break
    for fl in beams:
        w = int(kern.weight[fl.closure()].sum())
        if w > best[0]:
            best = (w, list(fl.chosen))
    if method == 'beam':
        for _ in range(restarts):
            fl = Flat(kern)
            for depth in range(k):
                opts = expand(fl, 1, 0.6)
                if not opts:
                    break
                fl.add(opts[0][1])
            w = int(kern.weight[fl.closure()].sum())
            if w > best[0]:
                best = (w, list(fl.chosen))
    return best


def apply_exact(terms, kern, chosen):
    """Rebuild Phi over Q from the chosen clusters and apply it exactly. Returns (new_terms, kills)."""
    k = kern.k
    rays = [list(kern.keys[c][0]) for c in chosen]
    rhs = [{a: -x for a, x in kern.keys[c][1]} for c in chosen]
    Z = sa._solve_rays(rays, rhs, k)
    new_terms = list(terms)
    kills = 0
    for t in kern.sup:
        U, V, W = terms[t]
        W2 = dict(W)
        lt = kern.ell[t]
        for j in range(k):
            lj = lt[j]
            if lj:
                for a, z in Z[j].items():
                    y = W2.get(a, 0) + lj * z
                    if y:
                        W2[a] = y
                    else:
                        W2.pop(a, None)
        new_terms[t] = (U, V, W2) if W2 else None
        if not W2:
            kills += 1
    return [t for t in new_terms if t is not None], kills


STATS = []


def absorb_uv(n, terms, method, rng, log=None, compare=False, **kw):
    t0 = time.time()
    basis = fast_sa.exact_kernel(n, terms)
    t1 = time.time()
    if not basis:
        return terms, 0
    kern = Kernel(terms, basis, rng)
    rec = dict(n=n, r=len(terms), k=kern.k, support=len(kern.sup), clusters=len(kern.keys),
               top_weights=sorted(kern.weight.tolist(), reverse=True)[:8])
    if compare:
        for m in ('greedy', 'flat', 'beam'):
            w, ch = search(kern, m, rng=random.Random(7), **kw)
            rec[m] = w
    w, chosen = search(kern, method, rng=rng, **kw)
    new_terms, kills = apply_exact(terms, kern, chosen)
    rec['predicted'] = w
    rec['exact_kills'] = kills
    rec['t_kernel'] = round(t1 - t0, 2)
    rec['t_search'] = round(time.time() - t1, 2)
    STATS.append(rec)
    if log:
        log('    absorb ' + str(rec))
    if kills < w:
        raise RuntimeError(f'exact kills {kills} below mod-p prediction {w}')
    return new_terms, kills


def absorb_all(n, terms, method='beam', rng=None, log=None, max_rounds=60, compare=False, start_rot=0, **kw):
    rng = rng or random.Random(1)
    total = 0
    quiet = 0
    rot = start_rot % 3
    for _ in range(max_rounds * 3):
        nn, tt = sa.rotate_to(n, terms, rot)
        tt, kills = absorb_uv(nn, tt, method, rng, log, compare, **kw)
        n, terms = sa.rotate_to(nn, tt, 3 - rot)
        total += kills
        quiet = 0 if kills else quiet + 1
        if quiet >= 3:
            break
        rot = (rot + 1) % 3
    return terms, total
