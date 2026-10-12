"""Bipartite route-chart lifts: controller Cay(H, S) with every generator OUTSIDE an index-2 subgroup H0, so the lift
G (vertex set H x F_q^s, edges (h,x)~(h t, A_t x + lam b_t)) is itself bipartite (colour = parity of h).
Target: diam(G) <= Db (odd, e.g. 5): even walks <= Db-1 must reach every (h0, y) with h0 in H0 and odd walks <= Db
every (h1, y) with h1 outside H0.  N = |H| q^s.
Parity: H = meta:m,k,r with k even (parity = j mod 2 for element (i,j) = i*k+j), or any 'GxC:2' (parity = index%2).
Stage 1: generators of odd parity; hard = #H0 elements (!= e) unreachable by reduced words of length 2 or Db-1,
         + #odd elements unreachable by reduced words of length Db or Db-2.
Stage 2: chart SA on the G-defect (pairs ((e,x), v) with dist > Db).
Library module: exh_bip.py and bip_proxy_search.py use parity_vec / check_parity_hom (standalone driver omitted).
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import rcl, rcl2


def parity_vec(H, gstr):
    n = H['n']
    if gstr.endswith('xC:2'):
        return np.arange(n) % 2
    if gstr.startswith('meta:') and 'x' not in gstr:
        m, k, r = map(int, gstr.split(':')[1].split(','))
        assert k % 2 == 0
        return (np.arange(n) % k) % 2
    raise ValueError('need meta:m,k,r with k even or ...xC:2')


def check_parity_hom(H, par):
    mul = H['mul']
    return bool(np.all((par[:, None] + par[None, :]) % 2 == par[mul]))


def rand_odd(H, kind, par, rng):
    n = H['n']
    for _ in range(100000):
        g = int(rng.integers(1, n))
        if par[g] != 1:
            continue
        if (kind == 'inv') == H['is_inv'](g):
            return g
    return None


def stage1_score(H, spec, gens, par, Db):
    els, inv = rcl2.alphabet(H, spec, gens)
    if len(set(els)) != len(els) or 0 in els:
        return (10 ** 9, 0)
    ce = rcl2.word_counts(H, els, inv, Db - 1)
    ce2 = rcl2.word_counts(H, els, inv, Db - 3) if Db >= 4 else np.zeros_like(ce)
    co = rcl2.word_counts(H, els, inv, Db)
    co2 = rcl2.word_counts(H, els, inv, Db - 2)
    ev = (par == 0); ev[0] = False
    od = (par == 1)
    hard = int((ev & (ce == 0) & (ce2 == 0)).sum()) + int((od & (co == 0) & (co2 == 0)).sum())
    soft = int((ev & (ce == 0)).sum()) + int((od & (co == 0)).sum())
    return (hard, soft)


def stage1(H, spec, par, Db, rng, iters):
    gens = [rand_odd(H, k, par, rng) for k, p in spec]
    if any(g is None for g in gens):
        return None, None
    f = lambda s: s[0] * 1000 + s[1]
    cur = stage1_score(H, spec, gens, par, Db); best = (cur, list(gens)); T = 2.0
    for it in range(iters):
        i = int(rng.integers(len(spec))); old = gens[i]
        gens[i] = rand_odd(H, spec[i][0], par, rng)
        new = stage1_score(H, spec, gens, par, Db)
        if f(new) <= f(cur) or rng.random() < np.exp(-(f(new) - f(cur)) / max(T, 1e-9)):
            cur = new
            if f(cur) < f(best[0]):
                best = (cur, list(gens))
        else:
            gens[i] = old
        T *= 0.999
    return best
