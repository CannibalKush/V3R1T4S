#!/usr/bin/env python3
"""Rebuild Rajiv's compound C(I;T,H) (Zenodo 23052995, Definition 3) from block 0 of his own edge file and the rules
in his witness, cut it at GIVEN cut sets (Lemma 5), attach t new vertices (one point + one line of every block, at
free slots) and join them by a random r-regular graph Y (relaxed Y: diameter of Y NOT required; the new-new pairs
are repaired afterwards and everything is confirmed by a full all-pairs BFS).

Self-test (always run): with Rajiv's own cut sets the rebuilt C' must equal his published C' edge set exactly.

Usage:
  compound.py --rajiv graph.edges.xz --witness cs.json [--sp SP.json] [--sl SL.json] --t T --seed s --out G.edges
SP/SL json: output of cutsets.py ('set' in Rajiv block-0 labels). Writes G.edges (plain 'u v', sorted) and
G.edges.meta.json (cut sets used, t, Y degree, slot usage, sha256).
"""
import argparse, json, lzma, hashlib, time, os
import numpy as np
import pandas as pd


def read_all(path):
    op = lzma.open if path.endswith('.xz') else open
    with op(path, 'rt') as f:
        first = f.readline().split()
        E = pd.read_csv(f, sep=r'\s+', header=None, dtype=np.int64, engine='c').values
    n, m = int(first[0]), int(first[1])
    assert len(E) == m, 'expected Rajiv header n m'
    return n, np.sort(E, 1)


def block0(C, P):
    B = C[(C[:, 1] < 2 * P)]
    assert (B[:, 0] < P).all() and (B[:, 1] >= P).all()
    u = B[:, 0]; v = B[:, 1] - P
    k = len(B) // P
    o = np.lexsort((v, u))
    return u[o].reshape(P, k)[:, 0], v[o].reshape(P, k), k   # (unused), pt_lines


def compound_edges(pt_lines, P, m, tour, H, SP, SL):
    q1 = pt_lines.shape[1]
    inc_u = np.repeat(np.arange(P, dtype=np.int64), q1)
    inc_v = pt_lines.ravel().astype(np.int64) + P
    parts = []
    for i in range(m):
        o = 2 * i * P
        parts.append(np.stack([inc_u + o, inc_v + o], 1))
    arcs = {(int(a), int(b)) for a, b in tour}
    Hs = {frozenset((int(a), int(b))) for a, b in H}
    x = np.arange(P, dtype=np.int64)
    keepP = np.ones(P, bool); keepP[np.asarray(SP, np.int64)] = False
    keepL = np.ones(P, bool); keepL[np.asarray(SL, np.int64)] = False
    for i in range(m):
        for j in range(i + 1, m):
            if (i, j) in arcs:
                parts.append(np.stack([2 * i * P + x, 2 * j * P + P + x], 1))
            elif (j, i) in arcs:
                parts.append(np.stack([2 * j * P + x, 2 * i * P + P + x], 1))
            else:
                raise ValueError(f'pair {i},{j} not in tournament')
            if frozenset((i, j)) in Hs:
                xs = x[keepP]
                parts.append(np.stack([2 * i * P + xs, 2 * j * P + xs], 1))
            else:
                xs = x[keepL]
                parts.append(np.stack([2 * i * P + P + xs, 2 * j * P + P + xs], 1))
    E = np.sort(np.concatenate(parts, 0), 1)
    return E


def keys(E, N):
    return E[:, 0] * N + E[:, 1]


def random_regular(t, r, rng):
    """Configuration model with repair of loops / multi-edges by random 2-switches. If t*r is odd, vertex t-1 gets
    degree r-1 (max degree stays r)."""
    degs = np.full(t, r)
    if (t * r) % 2:
        degs[-1] -= 1
    stubs = rng.permutation(np.repeat(np.arange(t), degs))
    E = stubs.reshape(-1, 2)
    E = np.sort(E, 1)
    for _ in range(200):
        k = E[:, 0] * t + E[:, 1]
        _, first = np.unique(k, return_index=True)
        bad = np.ones(len(E), bool); bad[first] = False
        bad |= E[:, 0] == E[:, 1]
        nb = int(bad.sum())
        if nb == 0:
            return E
        for i in np.flatnonzero(bad):
            j = int(rng.integers(len(E)))
            a, b = E[i]; c, d = E[j]
            if rng.random() < 0.5:
                E[i] = sorted((a, c)); E[j] = sorted((b, d))
            else:
                E[i] = sorted((a, d)); E[j] = sorted((b, c))
    raise RuntimeError('could not make Y simple')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rajiv', required=True); ap.add_argument('--witness', required=True)
    ap.add_argument('--sp'); ap.add_argument('--sl')
    ap.add_argument('--t', type=int, required=True)
    ap.add_argument('--ydeg', type=int, default=None)
    ap.add_argument('--delta', type=int, default=None)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    t0 = time.time()
    W = json.load(open(a.witness))
    q, k6, m = W['q'], W['k'], W['m']
    P = (q ** k6 - 1) // (q - 1)
    base = 2 * m * P
    Delta = a.delta or W['d']
    r = a.ydeg if a.ydeg is not None else Delta - 2 * m
    n0, R = read_all(a.rajiv)
    Cr = R[(R[:, 0] < base) & (R[:, 1] < base)]
    print(f'Rajiv: n={n0} m={len(R)}; C\' {len(Cr)} edges ({time.time()-t0:.0f}s)', flush=True)
    _, pt_lines, q1 = block0(Cr, P)
    assert q1 == q + 1
    SPr = np.array(W['deleted_points'], np.int64); SLr = np.array(W['deleted_lines'], np.int64)
    if SLr.max() >= P:
        SLr = SLr - P
    E0 = compound_edges(pt_lines, P, m, W['tournament'], W['H'], SPr, SLr)
    same = len(E0) == len(Cr) and np.array_equal(np.sort(keys(E0, base)), np.sort(keys(Cr, base)))
    print(f'self-test: rebuilt C\' with Rajiv cut sets == published C\': {same} ({len(E0)} vs {len(Cr)})', flush=True)
    assert same, 'compound rules misunderstood'
    SP = np.array(json.load(open(a.sp))['set'], np.int64) if a.sp else SPr
    SL = np.array(json.load(open(a.sl))['set'], np.int64) if a.sl else SLr
    # Lemma 5 hypotheses, re-checked here independently of cutsets.py
    cP = np.bincount(pt_lines[SP].ravel(), minlength=P).max()          # points of SP per line
    ln_pts = np.zeros((P, q + 1), np.int64)
    o = np.argsort(pt_lines.ravel(), kind='stable')
    ln_pts[:] = (np.repeat(np.arange(P), q + 1)[o]).reshape(P, q + 1)
    cL = np.bincount(ln_pts[SL].ravel(), minlength=P).max()            # lines of SL per point
    print(f'cut sets: |S_P|={len(SP)} (max per line {cP}), |S_L|={len(SL)} (max per point {cL})', flush=True)
    assert cP <= 1 and cL <= 1, 'cut set violates Lemma 5 hypotheses'
    C = compound_edges(pt_lines, P, m, W['tournament'], W['H'], SP, SL)
    deg = np.bincount(C.ravel(), minlength=base)
    defi = Delta - deg
    assert defi.min() >= 0
    rng = np.random.default_rng(a.seed)
    t = a.t
    newE = []
    slot_info = {}
    for i in range(m):
        for kind, lo in (('P', 2 * i * P), ('L', 2 * i * P + P)):
            idx = np.arange(lo, lo + P)
            slots = np.repeat(idx, defi[lo:lo + P])
            slot_info[f'{kind}{i}'] = int(len(slots))
            assert len(slots) >= t, f'not enough {kind} slots in block {i}: {len(slots)} < {t}'
            sel = rng.permutation(slots)[:t]
            newE.append(np.stack([base + np.arange(t), sel], 1))
    Y = random_regular(t, r, rng) + base if r > 0 else np.zeros((0, 2), np.int64)
    E = np.concatenate([C] + newE + [Y], 0)
    E = np.sort(E, 1)
    N = base + t
    kk = keys(E, N)
    assert len(np.unique(kk)) == len(kk), 'multi-edge'
    assert (E[:, 0] != E[:, 1]).all()
    d2 = np.bincount(E.ravel(), minlength=N)
    assert d2.max() <= Delta
    o = np.lexsort((E[:, 1], E[:, 0])); E = E[o]
    pd.DataFrame(E).to_csv(a.out, sep=' ', header=False, index=False)
    sha = hashlib.sha256(open(a.out, 'rb').read()).hexdigest()
    free_left = int((Delta - d2[:base]).sum())
    meta = dict(N=int(N), m=int(len(E)), base=int(base), t=int(t), ydeg=int(r), Delta=int(Delta), q=q, m_blocks=m,
                SP_size=int(len(SP)), SL_size=int(len(SL)), sp_file=a.sp, sl_file=a.sl, seed=a.seed,
                slots=slot_info, free_slots_left=free_left, sha256=sha,
                deg_hist={int(k): int(v) for k, v in zip(*np.unique(d2, return_counts=True))})
    json.dump(meta, open(a.out + '.meta.json', 'w'), indent=1)
    print(json.dumps(meta), flush=True)
    print(f'done {time.time()-t0:.0f}s')


if __name__ == '__main__':
    main()
