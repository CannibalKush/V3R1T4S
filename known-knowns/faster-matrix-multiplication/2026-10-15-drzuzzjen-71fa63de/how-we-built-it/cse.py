#!/usr/bin/env python3
"""Randomized pair-greedy common-subexpression elimination for ternary linear maps.

A map is a set of target rows over base variables x_0..x_{n-1}, coefficients in {-1,0,1}.
An SLP introduces t = ±a ± b (one addition each); a target row is then a signed sum of
available variables (len-1 additions). Rows equal up to sign are computed once.
cost = (#introduced vars) + sum_rows (nnz(row)-1)   [Perminov 'reduced' convention]

reduce_map(M, seed, eps, forced=None) returns (cost, fresh, final, defs) in Perminov JSON-like form, so the
result can be re-verified by tools/fmm_check.py independently of this module. M must be a 2-D ternary
matrix with no all-zero row (a zero linear form is never part of a legitimate scheme).
"""
import numpy as np
from numba import njit


@njit(cache=True)
def _greedy(R0, seed, eps, max_new, forced):
    np.random.seed(seed)
    nrows, n = R0.shape
    V = n + max_new
    R = np.zeros((nrows, V), np.int8)
    R[:, :n] = R0
    defs = np.zeros((max_new, 3), np.int64)  # a, b, sign: t = x_a + sign*x_b
    nv = n
    cnt = np.zeros((V, V, 2), np.int32)
    idx = np.empty(V, np.int64)
    nf = 0
    while nv < V:
        # forced prefix (iterated greedy / ruin-and-recreate): apply recorded pairs first
        if nf < forced.shape[0]:
            a = forced[nf, 0]; b = forced[nf, 1]; sg = forced[nf, 2]; nf += 1
            if a >= nv or b >= nv or a == b or (sg != 1 and sg != -1):
                continue
            hits = 0
            for r in range(nrows):
                if R[r, a] != 0 and R[r, b] == sg * R[r, a]:
                    hits += 1
            if hits < 2:
                continue
            t = nv
            defs[t - n, 0] = a; defs[t - n, 1] = b; defs[t - n, 2] = sg
            for r in range(nrows):
                if R[r, a] != 0 and R[r, b] == sg * R[r, a]:
                    R[r, t] = R[r, a]; R[r, a] = 0; R[r, b] = 0
            nv += 1
            continue
        # count signed pairs
        best = 1
        for r in range(nrows):
            k = 0
            for j in range(nv):
                if R[r, j] != 0:
                    idx[k] = j
                    k += 1
            for p in range(k):
                a = idx[p]
                for q in range(p + 1, k):
                    b = idx[q]
                    s = 0 if R[r, a] == R[r, b] else 1
                    cnt[a, b, s] += 1
                    if cnt[a, b, s] > best:
                        best = cnt[a, b, s]
        if best < 2:
            # reset touched counters
            for a in range(nv):
                for b in range(nv):
                    cnt[a, b, 0] = 0
                    cnt[a, b, 1] = 0
            break
        # threshold: occasionally accept pairs one below the max (exploration)
        thr = best
        if best > 2 and np.random.random() < eps:
            thr = best - 1
        # reservoir-sample uniformly among pairs with count >= thr
        chosen_a = -1
        chosen_b = -1
        chosen_s = 0
        seen = 0
        for a in range(nv):
            for b in range(a + 1, nv):
                for s in range(2):
                    c = cnt[a, b, s]
                    if c >= thr:
                        seen += 1
                        if np.random.randint(0, seen) == 0:
                            chosen_a = a
                            chosen_b = b
                            chosen_s = s
                    cnt[a, b, s] = 0
        a = chosen_a
        b = chosen_b
        sg = 1 if chosen_s == 0 else -1
        t = nv
        defs[t - n, 0] = a
        defs[t - n, 1] = b
        defs[t - n, 2] = sg
        for r in range(nrows):
            if R[r, a] != 0 and R[r, b] == sg * R[r, a]:
                R[r, t] = R[r, a]
                R[r, a] = 0
                R[r, b] = 0
        nv += 1
    return R[:, :nv], defs[: nv - n], nv - n


def dedupe(M):
    """Unique nonzero rows up to sign; returns (U, inverse index, sign per original row)."""
    keys = {}
    rows, inv, sgn = [], [], []
    for row in M:
        nz = np.nonzero(row)[0]
        if len(nz) == 0:
            inv.append(-1); sgn.append(1); continue
        s = 1 if row[nz[0]] > 0 else -1
        k = tuple((row * s).tolist())
        if k not in keys:
            keys[k] = len(rows); rows.append(np.array(k, np.int8))
        inv.append(keys[k]); sgn.append(s)
    return np.array(rows, np.int8).reshape(len(rows), M.shape[1]), inv, sgn


def reduce_map(M, seed=0, eps=0.0, forced=None):
    M = np.asarray(M, np.int8)
    if M.ndim != 2:
        raise ValueError("M must be 2-D")
    if M.size and int(np.abs(M).max()) > 1:
        raise ValueError("M must be ternary")
    if M.shape[0] and not np.any(M, axis=1).all():
        raise ValueError("M has an all-zero row")
    U, inv, sgn = dedupe(M)
    nnz = int(np.count_nonzero(U))
    if forced is None:
        forced = np.zeros((0, 3), np.int64)
    Rf, defs, k = _greedy(U, seed, eps, max(1, nnz), np.asarray(forced, np.int64).reshape(-1, 3))
    n = M.shape[1]
    # each fresh var: one addition. Rows: unique rows with >=2 terms after substitution.
    fresh = [[{"index": int(a), "value": 1}, {"index": int(b), "value": int(s)}] for a, b, s in defs]
    # a fresh var that is itself exactly a unique row is fine; rows reference it with len 1 (cost 0)
    urow_forms = []
    for r in range(Rf.shape[0]):
        nz = np.nonzero(Rf[r])[0]
        urow_forms.append([{"index": int(j), "value": int(Rf[r, j])} for j in nz])
    # Perminov layout: a unique row with >=2 terms is materialised as a fresh var only if it is used
    # more than once in the original map; otherwise written inline. Both cost len-1.
    final = []
    extra = []
    uid_var = {}
    count = {}
    for u in inv:
        if u >= 0:
            count[u] = count.get(u, 0) + 1
    for o, (u, s) in enumerate(zip(inv, sgn)):
        if u < 0:
            final.append([]); continue
        f = urow_forms[u]
        if len(f) >= 2 and count[u] > 1:
            if u not in uid_var:
                uid_var[u] = n + len(fresh) + len(extra)
                extra.append(f)
            final.append([{"index": uid_var[u], "value": s}])
        else:
            final.append([{"index": t["index"], "value": t["value"] * s} for t in f])
    fresh_all = fresh + extra
    cost = sum(len(f) - 1 for f in fresh_all) + sum(max(len(f) - 1, 0) for f in final)
    return cost, fresh_all, final, defs
