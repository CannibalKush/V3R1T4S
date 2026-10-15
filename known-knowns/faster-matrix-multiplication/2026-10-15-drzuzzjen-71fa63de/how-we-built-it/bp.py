#!/usr/bin/env python3
"""Boyar-Peralta-style distance-guided linear straight-line program search with cancellation, ternary intermediates.

Method credit: Boyar and Peralta's shortest-linear-program heuristic; the ternary-cancellation variant applied to the
U, V and W^T maps of FMM schemes was described by calgulbenkian's team in elder-plinius/V3R1T4S PR #161
(how-we-built-it/README.md). This is an independent numba re-implementation (no code copied).

A map is a set of target rows over n <= 64 base variables, coefficients in {-1,0,1}; vectors are (pos, neg) bitmasks.
State: base set S (inputs, then computed vectors v = s_a +- s_b, always ternary), and for every target a current
representation as a signed sum of elements of S with cost len-1 (an upper bound on its distance).
Each step evaluates candidates v from
  (1) v = t -+ s with v in S+-S (completes t in two steps, allows cancellation),
  (2) v = t itself if t in S+-S,
  (3) v = r_i +- r_j for two elements of a target's representation (pair CSE),
and scores the total distance reduction; exact shallow distances use hash lookups in +-S and S+-S.
reduce_map_bp(M, seed, eps) -> (cost, fresh, final, defs) like cse.reduce_map (fresh: two-term forms; final: reps).
"""
import numpy as np
from numba import njit

MASK = np.uint64(0xFFFFFFFFFFFFFFFF)


@njit(cache=True)
def _add(ap, an, bp, bn):
    # a + b, ternary only (no same-sign overlap)
    if (ap & bp) != 0 or (an & bn) != 0:
        return False, np.uint64(0), np.uint64(0)
    rp = (ap & ~bn) | (bp & ~an)
    rn = (an & ~bp) | (bn & ~ap)
    return True, rp, rn


@njit(cache=True)
def _key(p, n):
    h = p * np.uint64(0x9E3779B97F4A7C15) ^ (n + np.uint64(0x632BE59BD9B4E019)) * np.uint64(0xC2B2AE3D27D4EB4F)
    return h ^ (h >> np.uint64(29))


@njit(cache=True)
def _popc(x):
    c = 0
    while x:
        x &= x - np.uint64(1)
        c += 1
    return c


@njit(cache=True)
def _find(keys, kp, kn, sp, sn, q_p, q_n):
    """binary search for vector (q_p,q_n) in sorted key array; returns position or -1."""
    k = _key(q_p, q_n)
    lo, hi = 0, keys.shape[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if keys[mid] < k:
            lo = mid + 1
        else:
            hi = mid
    while lo < keys.shape[0] and keys[lo] == k:
        if kp[lo] == q_p and kn[lo] == q_n:
            return lo
        lo += 1
    return -1


@njit(cache=True)
def _bp(Tp, Tn, n, seed, eps, max_steps, deep):
    np.random.seed(seed)
    T = Tp.shape[0]
    MAXS = n + max_steps + 1
    Sp = np.zeros(MAXS, np.uint64)
    Sn = np.zeros(MAXS, np.uint64)
    defs = np.zeros((max_steps, 3), np.int64)
    for i in range(n):
        Sp[i] = np.uint64(1) << np.uint64(i)
    ns = n
    # representations: rep[t, k] = signed index (s+1)*sign, length replen[t]
    MAXR = 70
    rep = np.zeros((T, MAXR), np.int64)
    replen = np.zeros(T, np.int64)
    for t in range(T):
        L = 0
        for i in range(n):
            b = np.uint64(1) << np.uint64(i)
            if Tp[t] & b:
                rep[t, L] = i + 1
                L += 1
            elif Tn[t] & b:
                rep[t, L] = -(i + 1)
                L += 1
        replen[t] = L
    steps = 0
    while steps < max_steps:
        D = replen - 1
        if D.sum() == 0:
            break
        # +-S index: sorted keys of S and -S
        m1 = 2 * ns
        k1 = np.empty(m1, np.uint64); p1 = np.empty(m1, np.uint64); n1 = np.empty(m1, np.uint64); i1 = np.empty(m1, np.int64)
        for s in range(ns):
            k1[2 * s] = _key(Sp[s], Sn[s]); p1[2 * s] = Sp[s]; n1[2 * s] = Sn[s]; i1[2 * s] = s + 1
            k1[2 * s + 1] = _key(Sn[s], Sp[s]); p1[2 * s + 1] = Sn[s]; n1[2 * s + 1] = Sp[s]; i1[2 * s + 1] = -(s + 1)
        o = np.argsort(k1)
        k1 = k1[o]; p1 = p1[o]; n1 = n1[o]; i1 = i1[o]
        # S+-S index (both orientations of sign), with the defining pair
        cap = ns * (ns - 1) * 2 + 1
        k2 = np.empty(cap, np.uint64); p2 = np.empty(cap, np.uint64); n2 = np.empty(cap, np.uint64)
        a2 = np.empty(cap, np.int64); b2 = np.empty(cap, np.int64)
        m2 = 0
        for a in range(ns):
            for b in range(a + 1, ns):
                for sg in range(2):
                    if sg == 0:
                        ok, rp, rn = _add(Sp[a], Sn[a], Sp[b], Sn[b])
                    else:
                        ok, rp, rn = _add(Sp[a], Sn[a], Sn[b], Sp[b])
                    if ok and (rp | rn) != 0:
                        # store v and -v
                        k2[m2] = _key(rp, rn); p2[m2] = rp; n2[m2] = rn; a2[m2] = a + 1; b2[m2] = (b + 1) if sg == 0 else -(b + 1); m2 += 1
                        k2[m2] = _key(rn, rp); p2[m2] = rn; n2[m2] = rp; a2[m2] = -(a + 1); b2[m2] = -(b + 1) if sg == 0 else (b + 1); m2 += 1
        o = np.argsort(k2[:m2])
        k2 = k2[:m2][o]; p2 = p2[:m2][o]; n2 = n2[:m2][o]; a2 = a2[:m2][o]; b2 = b2[:m2][o]
        # candidate list: (a, b) signed indices defining v = sgn(a) S[|a|-1] + sgn(b) S[|b|-1]
        CMAX = 200000
        ca = np.empty(CMAX, np.int64); cb = np.empty(CMAX, np.int64); nc = 0
        for t in range(T):
            if D[t] == 0:
                continue
            # (2) t itself in S+-S
            j = _find(k2, p2, n2, Sp, Sn, Tp[t], Tn[t])
            if j >= 0 and nc < CMAX:
                ca[nc] = a2[j]; cb[nc] = b2[j]; nc += 1
            # (1) v = t - (+-s), v in S+-S
            if D[t] >= 2:
                for s in range(ns):
                    for sg in range(2):
                        if sg == 0:
                            ok, vp, vn = _add(Tp[t], Tn[t], Sn[s], Sp[s])
                        else:
                            ok, vp, vn = _add(Tp[t], Tn[t], Sp[s], Sn[s])
                        if ok and (vp | vn) != 0:
                            j = _find(k2, p2, n2, Sp, Sn, vp, vn)
                            if j >= 0 and nc < CMAX:
                                ca[nc] = a2[j]; cb[nc] = b2[j]; nc += 1
            # (3) pairs within the representation
            L = replen[t]
            for x in range(L):
                for y in range(x + 1, L):
                    if nc < CMAX:
                        ca[nc] = rep[t, x]; cb[nc] = rep[t, y]; nc += 1
        if nc == 0:
            break
        # evaluate candidates
        best = -1
        bscore = 0
        bnorm = -1
        seen = 0
        for c in range(nc):
            a = ca[c]; b = cb[c]
            ia = abs(a) - 1; ib = abs(b) - 1
            if ia == ib:
                continue
            ap = Sp[ia] if a > 0 else Sn[ia]; an = Sn[ia] if a > 0 else Sp[ia]
            bp_ = Sp[ib] if b > 0 else Sn[ib]; bn = Sn[ib] if b > 0 else Sp[ib]
            ok, vp, vn = _add(ap, an, bp_, bn)
            if not ok or (vp | vn) == 0:
                continue
            if _find(k1, p1, n1, Sp, Sn, vp, vn) >= 0:
                continue
            score = 0
            norm = 0
            for t in range(T):
                d = D[t]
                if d == 0:
                    norm += 0
                    continue
                nd = d
                if (vp == Tp[t] and vn == Tn[t]) or (vp == Tn[t] and vn == Tp[t]):
                    nd = 0
                else:
                    for sg in range(2):
                        if sg == 0:
                            ok2, up, un = _add(Tp[t], Tn[t], vn, vp)
                        else:
                            ok2, up, un = _add(Tp[t], Tn[t], vp, vn)
                        if ok2 and (up | un) != 0:
                            if nd > 1 and _find(k1, p1, n1, Sp, Sn, up, un) >= 0:
                                nd = 1
                            elif nd > 2 and _find(k2, p2, n2, Sp, Sn, up, un) >= 0:
                                nd = 2
                            elif nd > 3 and deep:
                                for s3 in range(ns):
                                    for g3 in range(2):
                                        if g3 == 0:
                                            ok3, wp, wn = _add(up, un, Sn[s3], Sp[s3])
                                        else:
                                            ok3, wp, wn = _add(up, un, Sp[s3], Sn[s3])
                                        if ok3 and (wp | wn) != 0 and _find(k2, p2, n2, Sp, Sn, wp, wn) >= 0:
                                            nd = 3
                                            break
                                    if nd == 3:
                                        break
                    if nd == d and d >= 2:
                        # pair inside the representation
                        L = replen[t]
                        hit = False
                        for x in range(L):
                            if hit:
                                break
                            for y in range(x + 1, L):
                                if (rep[t, x] == a and rep[t, y] == b) or (rep[t, x] == b and rep[t, y] == a) or \
                                   (rep[t, x] == -a and rep[t, y] == -b) or (rep[t, x] == -b and rep[t, y] == -a):
                                    hit = True
                                    break
                        if hit:
                            nd = d - 1
                score += d - nd
                norm += nd * nd
            if score <= 0:
                continue
            # BP tie-break: larger score, then larger sum of squared distances; random among equals
            better = False
            if score > bscore:
                better = True
                seen = 1
            elif score == bscore:
                if eps > 0 and np.random.random() < eps:
                    norm = bnorm  # randomized variant: ignore the norm tie-break for this candidate
                if norm > bnorm:
                    better = True
                    seen = 1
                elif norm == bnorm:
                    seen += 1
                    if np.random.randint(0, seen) == 0:
                        better = True
            if better:
                best = c
                bscore = score
                bnorm = norm
        if best < 0:
            break
        a = ca[best]; b = cb[best]
        ia = abs(a) - 1; ib = abs(b) - 1
        ap = Sp[ia] if a > 0 else Sn[ia]; an = Sn[ia] if a > 0 else Sp[ia]
        bp_ = Sp[ib] if b > 0 else Sn[ib]; bn = Sn[ib] if b > 0 else Sp[ib]
        ok, vp, vn = _add(ap, an, bp_, bn)
        v = ns
        Sp[v] = vp; Sn[v] = vn
        defs[steps, 0] = a; defs[steps, 1] = b; defs[steps, 2] = 0
        ns += 1
        steps += 1
        # update representations
        for t in range(T):
            d = replen[t] - 1
            if d == 0:
                continue
            if vp == Tp[t] and vn == Tn[t]:
                rep[t, 0] = v + 1; replen[t] = 1
                continue
            if vp == Tn[t] and vn == Tp[t]:
                rep[t, 0] = -(v + 1); replen[t] = 1
                continue
            done = False
            for sg in range(2):
                if done:
                    break
                sv = 1 if sg == 0 else -1
                if sg == 0:
                    ok2, up, un = _add(Tp[t], Tn[t], vn, vp)
                else:
                    ok2, up, un = _add(Tp[t], Tn[t], vp, vn)
                if not ok2 or (up | un) == 0:
                    continue
                if d > 1:
                    j = _find(k1, p1, n1, Sp, Sn, up, un)
                    if j >= 0:
                        rep[t, 0] = sv * (v + 1); rep[t, 1] = i1[j]; replen[t] = 2
                        done = True
                        continue
                if d > 2:
                    j = _find(k2, p2, n2, Sp, Sn, up, un)
                    if j >= 0:
                        rep[t, 0] = sv * (v + 1); rep[t, 1] = a2[j]; rep[t, 2] = b2[j]; replen[t] = 3
                        done = True
                        continue
                if d > 3 and deep:
                    for s3 in range(ns - 1):
                        if done:
                            break
                        for g3 in range(2):
                            if g3 == 0:
                                ok3, wp, wn = _add(up, un, Sn[s3], Sp[s3])
                            else:
                                ok3, wp, wn = _add(up, un, Sp[s3], Sn[s3])
                            if ok3 and (wp | wn) != 0:
                                j = _find(k2, p2, n2, Sp, Sn, wp, wn)
                                if j >= 0:
                                    rep[t, 0] = sv * (v + 1); rep[t, 1] = (s3 + 1) if g3 == 0 else -(s3 + 1)
                                    rep[t, 2] = a2[j]; rep[t, 3] = b2[j]; replen[t] = 4
                                    done = True
                                    break
            if done:
                continue
            L = replen[t]
            for x in range(L):
                if done:
                    break
                for y in range(x + 1, L):
                    sgn = 0
                    if (rep[t, x] == a and rep[t, y] == b) or (rep[t, x] == b and rep[t, y] == a):
                        sgn = 1
                    elif (rep[t, x] == -a and rep[t, y] == -b) or (rep[t, x] == -b and rep[t, y] == -a):
                        sgn = -1
                    if sgn != 0:
                        rep[t, x] = sgn * (v + 1)
                        for z in range(y, L - 1):
                            rep[t, z] = rep[t, z + 1]
                        replen[t] = L - 1
                        done = True
                        break
    return defs[:steps], rep, replen, ns


def _bits(M):
    n = M.shape[1]
    assert n <= 64
    P = np.zeros(M.shape[0], np.uint64)
    N = np.zeros(M.shape[0], np.uint64)
    for i in range(M.shape[0]):
        for j in range(n):
            if M[i, j] > 0:
                P[i] |= np.uint64(1) << np.uint64(j)
            elif M[i, j] < 0:
                N[i] |= np.uint64(1) << np.uint64(j)
    return P, N


def reduce_map_bp(M, seed=0, eps=0.0, max_steps=None, deep=True):
    """Same contract as cse.reduce_map: returns (cost, fresh, final, defs)."""
    import cse
    M = np.asarray(M, np.int8)
    U, inv, sgn = cse.dedupe(M)
    n = M.shape[1]
    P, N = _bits(U)
    if max_steps is None:
        max_steps = int(np.count_nonzero(U))
    defs, rep, replen, ns = _bp(P, N, n, seed, eps, max_steps, deep)
    # prune unused fresh vars (transitively), renumber
    nf = defs.shape[0]
    used = np.zeros(n + nf, bool)
    for t in range(U.shape[0]):
        for k in range(replen[t]):
            used[abs(rep[t, k]) - 1] = True
    for f in range(nf - 1, -1, -1):
        if used[n + f]:
            used[abs(defs[f, 0]) - 1] = True
            used[abs(defs[f, 1]) - 1] = True
    newid = {}
    for i in range(n):
        newid[i] = i
    fresh = []
    for f in range(nf):
        if used[n + f]:
            newid[n + f] = n + len(fresh)
            a, b = int(defs[f, 0]), int(defs[f, 1])
            fresh.append([{"index": newid[abs(a) - 1], "value": 1 if a > 0 else -1},
                          {"index": newid[abs(b) - 1], "value": 1 if b > 0 else -1}])
    urow = []
    for t in range(U.shape[0]):
        urow.append([{"index": newid[abs(int(rep[t, k])) - 1], "value": 1 if rep[t, k] > 0 else -1} for k in range(replen[t])])
    # duplicate rows: a multi-term rep used more than once becomes one extra fresh var
    count = {}
    for u in inv:
        if u >= 0:
            count[u] = count.get(u, 0) + 1
    final, extra, uid = [], [], {}
    base = n + len(fresh)
    for u, s in zip(inv, sgn):
        f = urow[u]
        if len(f) >= 2 and count[u] > 1:
            if u not in uid:
                uid[u] = base + len(extra)
                extra.append(f)
            final.append([{"index": uid[u], "value": s}])
        else:
            final.append([{"index": x["index"], "value": x["value"] * s} for x in f])
    fresh_all = fresh + extra
    cost = sum(len(f) - 1 for f in fresh_all) + sum(max(len(f) - 1, 0) for f in final)
    return cost, fresh_all, final, defs
