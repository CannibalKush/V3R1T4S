"""Exhaustive stage-1 for BIPARTITE controllers: triples (a, b, c), all of odd parity, c an involution; alphabet
{a,a^-1,b,b^-1,c}. hard = #even elements (!= e) not reached by reduced words of length 2 or 4
                         + #odd elements not reached by reduced words of length 3 or 5 (length 1 too).
Usage: exh_bip.py --group meta:43,6,7 [--maxhard 0] [--out file]
"""
import sys, os, json, time, argparse
import numpy as np
import numba as nb
sys.path.insert(0, os.path.dirname(__file__))
import rcl2, rcl_bip


@nb.njit(cache=True)
def score_triple(mul, inv, par, a, b, c, n, st, nx, reach_e, reach_o):
    letters = np.array([a, inv[a], b, inv[b], c])
    linv = np.array([1, 0, 3, 2, 4])
    for i in range(n):
        reach_e[i] = 0; reach_o[i] = 0
        for t in range(5):
            st[i, t] = 0
    for t in range(5):
        st[letters[t], t] += 1
        reach_o[letters[t]] = 1
    for step in range(2, 6):
        for i in range(n):
            for t in range(5):
                nx[i, t] = 0
        for h in range(n):
            tot = 0
            for t in range(5):
                tot += st[h, t]
            if tot == 0:
                continue
            for t2 in range(5):
                v = tot - st[h, linv[t2]]
                if v > 0:
                    nx[mul[h, letters[t2]], t2] += v
        for i in range(n):
            s = 0
            for t in range(5):
                st[i, t] = nx[i, t]; s += nx[i, t]
            if s > 0:
                if step % 2 == 0:
                    reach_e[i] = 1
                else:
                    reach_o[i] = 1
    hard = 0
    for i in range(1, n):
        if par[i] == 0:
            if reach_e[i] == 0:
                hard += 1
        else:
            if reach_o[i] == 0:
                hard += 1
    return hard


@nb.njit(parallel=True, cache=True)
def scan(mul, inv, par, odd_non, odd_inv):
    n = mul.shape[0]
    na = odd_non.shape[0]
    res = np.full((na, na, odd_inv.shape[0]), 10 ** 6, dtype=np.int64)
    for ia in nb.prange(na):
        st = np.zeros((n, 5), dtype=np.int64); nx = np.zeros((n, 5), dtype=np.int64)
        re = np.zeros(n, dtype=np.int64); ro = np.zeros(n, dtype=np.int64)
        a = odd_non[ia]
        if inv[a] < a:
            continue
        for ib in range(na):
            b = odd_non[ib]
            if b == a or b == inv[a] or inv[b] < b or b < a:
                continue
            for ic in range(odd_inv.shape[0]):
                res[ia, ib, ic] = score_triple(mul, inv, par, a, b, odd_inv[ic], n, st, nx, re, ro)
    return res


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--group', required=True); ap.add_argument('--maxhard', type=int, default=0)
    ap.add_argument('--top', type=int, default=10); ap.add_argument('--out')
    a = ap.parse_args()
    t0 = time.time()
    H = rcl2.parse_group(a.group); n = H['n']
    par = rcl_bip.parity_vec(H, a.group).astype(np.int64)
    assert rcl_bip.check_parity_hom(H, par)
    mul = H['mul'].astype(np.int64); inv = H['inverse'].astype(np.int64)
    odd_inv = np.array([g for g in range(1, n) if par[g] == 1 and mul[g, g] == 0], dtype=np.int64)
    odd_non = np.array([g for g in range(1, n) if par[g] == 1 and mul[g, g] != 0], dtype=np.int64)
    if len(odd_inv) == 0 or len(odd_non) < 2:
        rec = dict(group=a.group, n=n, error='no odd involution / generators')
    else:
        res = scan(mul, inv, par, odd_non, odd_inv)
        mh = int(res.min())
        flat = np.argwhere(res <= max(a.maxhard, mh))
        best = sorted((int(res[i, j, k]), int(odd_non[i]), int(odd_non[j]), int(odd_inv[k])) for i, j, k in flat)[:a.top]
        rec = dict(group=a.group, n=n, min_hard=mh, n_ok=int((res <= a.maxhard).sum()), best=best, sec=round(time.time() - t0, 1))
    print(json.dumps(rec), flush=True)
    if a.out:
        with open(a.out, 'a') as f:
            f.write(json.dumps(rec) + '\n')
