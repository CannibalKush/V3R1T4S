"""symsearch.py: SYMMETRIC Z_n-voltage search (voltages constant on orbits of the cyclic group <omega> acting on the
flags of W(q), GF(q^4) model in gq4.py).  Constraint (C4) is checked on orbit representatives only (pairs (u,w)
with u a representative of its <omega>-orbit), which is exact because the constraint is <omega>-invariant.
After a solution is found it is expanded to all flags and re-checked on ALL opposite pairs (vsearch.count_bad).

usage (the run that produced the published (9,4) voltages; it stops at the first restart with 0 violations):
  python symsearch.py --q 7 --n 2 --seed 1 --steps 100000 --restarts 10 --out sym_q7_n2_s1.npz
then: python lam.py sym_q7_n2_s1.npz G_9_4_n1700.edges   (and export_txt.py for the plain-text files)
"""
import argparse
import os
import sys
import time
import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vsearch as vs
import gq4


def prepare_from_adj(q, P, adj):
    adj = adj.astype(np.int64)
    eid, ends = vs.edge_index(adj, P)
    G = vs._count_geod(adj, P)
    V = adj.shape[0]
    pid = -np.ones((V, V), np.int32)
    ge, gsign, gpair, npair = vs._enum_geod(adj, eid, P, G, pid)
    E = ends.shape[0]
    eptr, erows, epos = vs._csr(ge, E, 4)
    pptr, prows, _ = vs._csr(gpair.reshape(-1, 1), npair, 1)
    return dict(q=q, P=P, adj=adj, eid=eid, ends=ends, G=G, ge=ge, gsign=gsign, gpair=gpair, npair=npair,
                eptr=eptr, erows=erows, epos=epos, pptr=pptr, prows=prows, pid=pid)


def edge_orbits(g, ends):
    P, shift, line_img = g['P'], g['shift'], g['line_img']
    look = {(int(p), int(L)): e for e, (p, L) in enumerate(ends)}
    orb = -np.ones(len(ends), np.int64)
    no = 0
    for e in range(len(ends)):
        if orb[e] >= 0:
            continue
        p, L = int(ends[e, 0]), int(ends[e, 1]) - P
        while True:
            f = look[(p, P + L)]
            if orb[f] >= 0:
                break
            orb[f] = no
            p = (p + shift) % P
            L = int(line_img[L])
        no += 1
    return orb, no


@njit(cache=True)
def _walksat(terms, tsign, nterm, nc, nv, n, x, steps, noise, seed, v_ptr, v_c, v_k, v_coef):
    """terms[c, k, j]: variable ids (or -1) of the j-th edge of the k-th geodesic of constraint c;
    tsign[c, k, j]: +-1.  Constraint c is satisfied iff the values sum(tsign*x) mod n over k cover Z_n.
    v_ptr/v_c/v_k/v_coef: for each variable v, the (constraint, term, coefficient) triples, sorted by constraint."""
    np.random.seed(seed)
    K = terms.shape[1]
    val = np.zeros((nc, K), np.int64)
    cnt = np.zeros((nc, n), np.int64)
    for c in range(nc):
        for k in range(nterm[c]):
            s = 0
            for j in range(4):
                v = terms[c, k, j]
                if v >= 0:
                    s += tsign[c, k, j] * x[v]
            s %= n
            if s < 0:
                s += n
            val[c, k] = s
            cnt[c, s] += 1
    bad = np.zeros(nc, np.bool_)
    nbad = 0
    for c in range(nc):
        for r in range(n):
            if cnt[c, r] == 0:
                bad[c] = True
        if bad[c]:
            nbad += 1
    best = nbad
    bestx = x.copy()
    tmpcnt = np.zeros(n, np.int64)
    for it in range(steps):
        if nbad == 0:
            break
        c0 = np.random.randint(nc)
        while not bad[c0]:
            c0 = np.random.randint(nc)
        bestsc = 1 << 30
        bv = -1
        bd = 0
        if np.random.rand() < noise:
            k = np.random.randint(nterm[c0])
            j = np.random.randint(4)
            while terms[c0, k, j] < 0:
                j = np.random.randint(4)
            bv = terms[c0, k, j]
            bd = 1 + np.random.randint(n - 1)
        else:
            for k in range(nterm[c0]):
                for j in range(4):
                    v = terms[c0, k, j]
                    if v < 0:
                        continue
                    for d in range(1, n):
                        brk = 0
                        mk = 0
                        t = v_ptr[v]
                        while t < v_ptr[v + 1]:
                            c = v_c[t]
                            for r in range(n):
                                tmpcnt[r] = cnt[c, r]
                            while t < v_ptr[v + 1] and v_c[t] == c:
                                kk = v_k[t]
                                s0 = val[c, kk]
                                s1 = (s0 + v_coef[t] * d) % n
                                if s1 < 0:
                                    s1 += n
                                tmpcnt[s0] -= 1
                                tmpcnt[s1] += 1
                                t += 1
                            nb = False
                            for r in range(n):
                                if tmpcnt[r] == 0:
                                    nb = True
                            if nb and not bad[c]:
                                brk += 1
                            elif (not nb) and bad[c]:
                                mk += 1
                        sc = brk - mk
                        if sc < bestsc or (sc == bestsc and np.random.rand() < 0.5):
                            bestsc = sc
                            bv = v
                            bd = d
        v = bv
        d = bd
        x[v] = (x[v] + d) % n
        t = v_ptr[v]
        while t < v_ptr[v + 1]:
            c = v_c[t]
            while t < v_ptr[v + 1] and v_c[t] == c:
                kk = v_k[t]
                s0 = val[c, kk]
                s1 = (s0 + v_coef[t] * d) % n
                if s1 < 0:
                    s1 += n
                cnt[c, s0] -= 1
                cnt[c, s1] += 1
                val[c, kk] = s1
                t += 1
            nb = False
            for r in range(n):
                if cnt[c, r] == 0:
                    nb = True
            if nb and not bad[c]:
                bad[c] = True
                nbad += 1
            elif (not nb) and bad[c]:
                bad[c] = False
                nbad -= 1
        if nbad < best:
            best = nbad
            bestx[:] = x
    return bestx, best


def reduced_instance(D, orb, P, nrep_pts, nrep_lines, reps):
    """constraints = ordered pairs (u,w), u in reps, w opposite u. terms = orbit ids of geodesic edges + signs."""
    adj = D['adj']
    eid = D['eid']
    k = adj.shape[1]
    cons = []
    for u in reps:
        s = 1 if u < P else -1
        # enumerate NB 4-walks from u, group by endpoint w
        by_w = {}
        for ia in range(k):
            a = adj[u, ia]
            e1 = eid[u, ia]
            for ib in range(k):
                b = adj[a, ib]
                if b == u:
                    continue
                e2 = eid[a, ib]
                for ic in range(k):
                    c = adj[b, ic]
                    if c == a:
                        continue
                    e3 = eid[b, ic]
                    for iw in range(k):
                        w = adj[c, iw]
                        if w == b:
                            continue
                        e4 = eid[c, iw]
                        by_w.setdefault(int(w), []).append((orb[e1], orb[e2], orb[e3], orb[e4]))
        for w, geos in by_w.items():
            cons.append(geos)
    nc = len(cons)
    K = k
    terms = -np.ones((nc, K, 4), np.int64)
    tsign = np.zeros((nc, K, 4), np.int64)
    nterm = np.zeros(nc, np.int64)
    for c, geos in enumerate(cons):
        nterm[c] = len(geos)
        for kk, (o1, o2, o3, o4) in enumerate(geos):
            # sign pattern: walk from u: (+,-,+,-) if u point else (-,+,-,+); the per-constraint global sign does
            # not matter for coverage, so use (+,-,+,-) for all
            terms[c, kk] = (o1, o2, o3, o4)
            tsign[c, kk] = (1, -1, 1, -1)
    return terms, tsign, nterm


def var_index(terms, tsign, nterm, nv, n):
    trip = [[] for _ in range(nv)]
    for c in range(terms.shape[0]):
        for k in range(nterm[c]):
            coef = {}
            for j in range(4):
                v = int(terms[c, k, j])
                if v >= 0:
                    coef[v] = coef.get(v, 0) + int(tsign[c, k, j])
            for v, cf in coef.items():
                if cf % n != 0:
                    trip[v].append((c, k, cf))
    ptr = np.zeros(nv + 1, np.int64)
    for v in range(nv):
        trip[v].sort()
        ptr[v + 1] = ptr[v] + len(trip[v])
    vc = np.zeros(ptr[-1], np.int64); vk = np.zeros(ptr[-1], np.int64); vf = np.zeros(ptr[-1], np.int64)
    for v in range(nv):
        for i, (c, k, cf) in enumerate(trip[v]):
            vc[ptr[v] + i] = c; vk[ptr[v] + i] = k; vf[ptr[v] + i] = cf
    return ptr, vc, vk, vf


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--q', type=int, required=True)
    ap.add_argument('--n', type=int, default=2)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--steps', type=int, default=200000)
    ap.add_argument('--noise', type=float, default=0.1)
    ap.add_argument('--restarts', type=int, default=20)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    t0 = time.time()
    g = gq4.build(a.q)
    P = g['P']
    D = prepare_from_adj(a.q, P, g['adj'])
    orb, no = edge_orbits(g, D['ends'])
    # orbit representatives of points and lines
    reps = []
    seen = np.zeros(2 * P, bool)
    for v in range(P):
        if not seen[v]:
            j = v
            while not seen[j]:
                seen[j] = True
                j = (j + g['shift']) % P
            reps.append(v)
    for l in range(P):
        if not seen[P + l]:
            j = l
            while not seen[P + j]:
                seen[P + j] = True
                j = int(g['line_img'][j])
            reps.append(P + l)
    terms, tsign, nterm = reduced_instance(D, orb, P, 0, 0, reps)
    vptr, vc, vk, vf = var_index(terms, tsign, nterm, no, a.n)
    print('q=%d n=%d flag orbits %d, reps %d, reduced constraints %d (%.1fs)' % (a.q, a.n, no, len(reps),
          terms.shape[0], time.time() - t0), flush=True)
    rng = np.random.default_rng(a.seed)
    gbest = 10 ** 9
    for r in range(a.restarts):
        x = rng.integers(0, a.n, no).astype(np.int64)
        bx, b = _walksat(terms, tsign, nterm, terms.shape[0], no, a.n, x, a.steps, a.noise, a.seed * 1000 + r,
                         vptr, vc, vk, vf)
        print('restart', r, 'reduced bad', b, '%.1fs' % (time.time() - t0), flush=True)
        if b < gbest:
            gbest = b
            alpha = bx[orb]
            full = vs.count_bad(alpha, a.n, D)
            print('   full check: violated opposite pairs =', full, flush=True)
            np.savez_compressed(a.out, alpha=alpha, xorb=bx, orb=orb, q=a.q, n=a.n, bad=full, ends=D['ends'],
                                adj=g['adj'], lines=g['lines'], spread=g['spread'], P=P)
        if gbest == 0:
            break
    print('done best', gbest)
