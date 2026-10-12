#!/usr/bin/env python3
r"""
frame4.py -- D=4 frame lift with ONE translation per fibre ("Theorem 2"), q=3, fibre V=F_3^4.

Controller C: 4-regular, diameter <= 4.  Lift L: vertices C x V,
  (u,p) ~ (w, A_uw p + c_uw + lam*b_uw)  for each oriented controller edge u->w and lam in F_3  (b_uw = A_uw delta^u_w)
  (u,p) ~ (u, p + t_u)                    (translation; gives the 2 in-fibre neighbours p +- t_u)
so L is 14-regular on 81|C| vertices.

Local data (all fibres use the SAME plane Pi = <e1,e2>, which is WLOG after a change of coordinates per fibre):
  delta^u_w  : the 4 points of Pi, bijectively over w in N(u)                         (F1)
  K_{u->w}   : = <delta^u_w, eps^u_w>, eps^u_w with distinct classes mod Pi             (F3: pairwise complementary)
  A_uw       : A(Pi) = K_{w->u}, A(K_{u->w}) = Pi  (so A delta^u_w in <delta^w_u>)      (frame transport)
  t_u        : t_u notin Pi, t_u in Pi + K_{u->sigma(u)}, sigma(u) an out-neighbour in an Euler orientation
               (so sigma has no 2-cycles)                                               (T),(P3)
  U_u        : = <t_u, z_u>, U_u cap Pi = 0                                              (P0)
Per edge we enumerate all 3888 frame transports and keep those with
  A t_u      in (U_w + <delta^w_u>) \ <t_w, delta^w_u>      (P0 at w)
  A^-1 t_w   in (U_u + <delta^u_w>) \ <t_u, delta^u_w>      (P0 at u)
and then pick, by SAT, one transport per edge so that at every vertex v the 5 classes [A_yv t_y] mod Pi
(y in N[v], A_vv = I) cover the 4 points of PG(F^4/Pi)                                (P1).
Output: params JSON (everything needed to rebuild L) + optional edge list.

usage (the run that produced G_14_4_n8424.params.json; the controller file must be named adjD4_104c_d4D4.txt,
because its base name is stored in the params JSON):
  python -W ignore frame4.py adjD4_104c_d4D4.txt --seed 1 --tries 5 --out G14_4_104c_s1
"""
import argparse
import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gf3
from gf3 import ALL, code, codes, vec, rank, span, inv, proj_point

Q, S = 3, 4
E1, E2, E3, E4 = np.eye(4, dtype=np.int64)
PI_PTS = [E1, E2, (E1 + E2) % 3, (E1 + 2 * E2) % 3]           # the 4 points of Pi = <e1,e2>
QU_PTS = [E3, E4, (E3 + E4) % 3, (E3 + 2 * E4) % 3]           # 4 representatives of the points of F^4/Pi
PI_SET = span([E1, E2])


def qclass(v):
    """projective point (code of normalised vector in <e3,e4>) of v mod Pi; None if v in Pi."""
    v = np.asarray(v, dtype=np.int64) % 3
    w = np.array([0, 0, v[2], v[3]])
    return proj_point(w)


def read_controller(path):
    pairs = []
    for line in open(path):
        line = line.split('#')[0].strip()
        if not line:
            continue
        parts = line.replace(',', ' ').replace(':', ' ').split()
        try:
            a, b = int(parts[0]), int(parts[1])
        except (ValueError, IndexError):
            continue
        if len(parts) != 2:
            continue
        pairs.append((a, b))
    labels = sorted({x for e in pairs for x in e})
    idx = {x: i for i, x in enumerate(labels)}
    E = sorted({tuple(sorted((idx[a], idx[b]))) for a, b in pairs})
    n = len(labels)
    nbrs = [[] for _ in range(n)]
    for a, b in E:
        nbrs[a].append(b)
        nbrs[b].append(a)
    return n, E, nbrs


def controller_diameter(n, nbrs):
    dmax = 0
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        fr = [s]
        while fr:
            nf = []
            for x in fr:
                for y in nbrs[x]:
                    if dist[y] < 0:
                        dist[y] = dist[x] + 1
                        nf.append(y)
            fr = nf
        if min(dist) < 0:
            return None
        dmax = max(dmax, max(dist))
    return dmax


def euler_orientation(n, E, nbrs, rng):
    """orient edges along an Euler circuit (every vertex out=in=2 for a connected 4-regular graph)."""
    adj = {v: [] for v in range(n)}
    for i, (a, b) in enumerate(E):
        adj[a].append((b, i))
        adj[b].append((a, i))
    for v in adj:
        rng.shuffle(adj[v])
    used = [False] * len(E)
    ptr = {v: 0 for v in range(n)}
    stack = [(int(rng.integers(n)), None)]
    circuit = []
    while stack:
        v, ei = stack[-1]
        while ptr[v] < len(adj[v]) and used[adj[v][ptr[v]][1]]:
            ptr[v] += 1
        if ptr[v] == len(adj[v]):
            circuit.append((v, ei))
            stack.pop()
        else:
            w, j = adj[v][ptr[v]]
            used[j] = True
            stack.append((w, j))
    # circuit is reversed list of (vertex, edge used to arrive)
    circuit.reverse()
    arcs = []
    for k in range(1, len(circuit)):
        prev_v = circuit[k - 1][0]
        v, ei = circuit[k]
        arcs.append((prev_v, v))
    assert len(arcs) == len(E), (len(arcs), len(E))
    return arcs


def per_vertex_data(n, nbrs, sigma, rng):
    L = []
    for u in range(n):
        pi = rng.permutation(4)
        rho = rng.permutation(4)
        d = {}
        eps = {}
        for i, w in enumerate(nbrs[u]):
            d[w] = PI_PTS[pi[i]].copy()
            eps[w] = (QU_PTS[rho[i]] * int(rng.integers(1, 3)) + int(rng.integers(0, 3)) * E1 + int(rng.integers(0, 3)) * E2) % 3
        s = sigma[u]
        while True:
            pc = (int(rng.integers(0, 3)) * E1 + int(rng.integers(0, 3)) * E2) % 3
            if rank([pc, d[s]]) == 2:            # Pi-part of t_u nonzero and not parallel to delta^u_sigma(u)
                break
        t = (eps[s] * int(rng.integers(1, 3)) + pc) % 3
        # make sure t in Pi + K_{u->sigma(u)}: eps[s] already has class of K_{u->s}; pc in Pi -> ok
        # Lemma (arc solvability): U_u = <t_u, z_u> must be complementary to Pi AND to every K_{u->w}.
        good = []
        for zc in range(81):
            z = ALL[zc]
            if rank([E1, E2, t, z]) != 4:
                continue
            if all(rank([d[w], eps[w], t, z]) == 4 for w in nbrs[u]):
                good.append(zc)
        if not good:
            raise RuntimeError(f'no complementary U at vertex {u}')
        z = ALL[good[int(rng.integers(len(good)))]]
        L.append({'delta': d, 'eps': eps, 't': t, 'z': z.copy(), 'nU': len(good)})
    return L


def p0_allowed(Lw, wnb):
    """codes y with y in (U_w + <delta^w_wnb>) minus <t_w, delta^w_wnb>."""
    big = span([Lw['t'], Lw['z'], Lw['delta'][wnb]])
    small = span([Lw['t'], Lw['delta'][wnb]])
    ok = np.zeros(81, dtype=bool)
    for c in big - small:
        ok[c] = True
    return ok


def edge_candidates(u, w, L):
    """all frame transports A (u->w) satisfying P0 at both ends; returns list of (A, tau_w(u), tau_u(w))."""
    Lu, Lw = L[u], L[w]
    f1 = Lu['delta'][w]
    f2 = next(P for P in PI_PTS if rank([P, f1]) == 2)
    f3 = Lu['eps'][w]
    f4 = next(Qv for Qv in QU_PTS if rank([f1, f2, f3, Qv]) == 4)
    F = np.stack([f1, f2, f3, f4], axis=1) % 3
    Finv = inv(F)
    dw = Lw['delta'][u]
    Kw = span([dw, Lw['eps'][u]])                  # K_{w->u}
    line_dw = span([dw])
    g1s = [dw, (2 * dw) % 3]
    g2s = [vec(c) for c in sorted(Kw - line_dw)]
    g3s = [vec(c) for c in sorted(PI_SET - line_dw)]
    PK = span([E1, E2, Lw['eps'][u]])              # Pi + K_{w->u}
    g4s = [vec(c) for c in range(81) if c not in PK]
    okY = p0_allowed(Lw, u)
    okX = p0_allowed(Lu, w)
    tu, tw = Lu['t'], Lw['t']
    tw_code = code(tw)
    out = []
    G = np.array([np.stack([g1, g2, g3, g4], axis=1) for g1, g2, g3, g4 in itertools.product(g1s, g2s, g3s, g4s)])
    A = np.einsum('nij,jk->nik', G, Finv) % 3
    Atu = np.einsum('nij,j->ni', A, tu) % 3
    yc = codes(Atu)
    sel = okY[yc]
    if not sel.any():
        return out
    A = A[sel]
    yv = Atu[sel]
    img = np.einsum('nij,kj->nki', A, ALL) % 3       # (n, 81, 4): A x for every x
    ic = codes(img)                                   # (n, 81)
    xs = np.argmax(ic == tw_code, axis=1)             # x with A x = t_w
    selx = okX[xs]
    for k in np.nonzero(selx)[0]:
        out.append((A[k], qclass(yv[k]), qclass(ALL[xs[k]])))
    return out


def solve_p1(n, nbrs, arcs, L, cands):
    """SAT: choose one (tau_w(u), tau_u(w)) pair per arc so that P1 holds at every vertex."""
    from pysat.solvers import Cadical153
    from pysat.card import CardEnc, EncType
    var = 0
    pairvars = []
    clauses = []
    cover = {}   # (v, point) -> list of vars
    for ai, (u, w) in enumerate(arcs):
        pairs = sorted({(a, b) for (_, a, b) in cands[ai]})
        vs = []
        for (a, b) in pairs:
            var += 1
            vs.append((var, a, b))
            cover.setdefault((w, a), []).append(var)
            cover.setdefault((u, b), []).append(var)
        pairvars.append(vs)
    top = var
    for vs in pairvars:
        lits = [x[0] for x in vs]
        enc = CardEnc.equals(lits=lits, bound=1, top_id=top, encoding=EncType.pairwise)
        clauses.extend(enc.clauses)
    for v in range(n):
        tq = qclass(L[v]['t'])
        for P in [proj_point(x) for x in QU_PTS]:
            if P == tq:
                continue
            lits = cover.get((v, P), [])
            if not lits:
                return None
            clauses.append(lits)
    s = Cadical153(bootstrap_with=clauses)
    if not s.solve():
        return None
    model = set(x for x in s.get_model() if x > 0)
    choice = []
    for vs in pairvars:
        ch = [(a, b) for (x, a, b) in vs if x in model]
        choice.append(ch[0])
    return choice


def build(controller, seed, max_tries=200, verbose=True):
    n, E, nbrs = read_controller(controller)
    assert all(len(x) == 4 for x in nbrs), 'controller not 4-regular'
    diam = controller_diameter(n, nbrs)
    assert diam is not None and diam <= 4, f'controller diameter {diam}'
    rng = np.random.default_rng(seed)
    arcs = euler_orientation(n, E, nbrs, rng)
    out_nb = {u: [w for (a, w) in arcs if a == u] for u in range(n)}
    sigma = {u: out_nb[u][int(rng.integers(len(out_nb[u])))] for u in range(n)}
    for u in range(n):
        assert sigma[sigma[u]] != u
    for attempt in range(max_tries):
        L = per_vertex_data(n, nbrs, sigma, rng)
        cands = []
        bad = 0
        for (u, w) in arcs:
            cs = edge_candidates(u, w, L)
            cands.append(cs)
            if not cs:
                bad += 1
        if verbose:
            print(f'attempt {attempt}: arcs without P0-candidates: {bad}/{len(arcs)}; '
                  f'min/avg #cands {min(len(c) for c in cands)}/{np.mean([len(c) for c in cands]):.1f}', flush=True)
        if bad:
            continue
        choice = solve_p1(n, nbrs, arcs, L, cands)
        if choice is None:
            if verbose:
                print('  P1 SAT: UNSAT', flush=True)
            continue
        A = {}
        for ai, (u, w) in enumerate(arcs):
            ok = [c for c in cands[ai] if (c[1], c[2]) == choice[ai]]
            A[(u, w)] = ok[int(rng.integers(len(ok)))][0]
        P = {'controller_file': os.path.basename(controller), 'n': n, 'q': 3, 's': 4, 'seed': seed,
             'arcs': [[int(u), int(w)] for (u, w) in arcs],
             'A': [A[(u, w)].astype(int).tolist() for (u, w) in arcs],
             'b': [((A[(u, w)] @ L[u]['delta'][w]) % 3).astype(int).tolist() for (u, w) in arcs],
             'c': [ALL[int(rng.integers(81))].astype(int).tolist() for _ in arcs],
             't': [L[u]['t'].astype(int).tolist() for u in range(n)],
             'z': [L[u]['z'].astype(int).tolist() for u in range(n)],
             'sigma': [int(sigma[u]) for u in range(n)],
             'controller_edges': [[int(a), int(b)] for (a, b) in E]}
        return P
    return None


def lift_edges(P):
    n = P['n']
    m = 81
    edges = []
    for (u, w), A, b, c in zip(P['arcs'], P['A'], P['b'], P['c']):
        A = np.array(A); b = np.array(b); c = np.array(c)
        img = (ALL @ A.T + c) % 3
        for lam in range(3):
            ci = codes((img + lam * b) % 3)
            edges.append(np.stack([u * m + np.arange(m), w * m + ci], axis=1))
    for u in range(n):
        t = np.array(P['t'][u])
        ci = codes((ALL + t) % 3)
        edges.append(np.stack([u * m + np.arange(m), u * m + ci], axis=1))
    Ed = np.concatenate(edges)
    Ed = np.sort(Ed, axis=1)
    return Ed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('controller', help='4-regular diameter-4 controller edge list (one "a b" pair per line)')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--out', default=None, help='prefix for params.json / edges.txt')
    ap.add_argument('--tries', type=int, default=200)
    a = ap.parse_args()
    t0 = time.time()
    P = build(a.controller, a.seed, a.tries)
    if P is None:
        print('FAILED to find parameters')
        sys.exit(1)
    Ed = lift_edges(P)
    u = np.unique(Ed, axis=0)
    N = P['n'] * 81
    deg = np.bincount(Ed.ravel(), minlength=N)
    print(f'params found in {time.time() - t0:.1f}s; lift N={N}, edges={len(Ed)} unique={len(u)}, '
          f'loops={(Ed[:, 0] == Ed[:, 1]).sum()}, deg min/max={deg.min()}/{deg.max()}', flush=True)
    if a.out:
        with open(a.out + '.params.json', 'w') as f:
            json.dump(P, f)
        np.savetxt(a.out + '.edges.txt', u, fmt='%d')
        print('wrote', a.out + '.params.json', a.out + '.edges.txt')


if __name__ == '__main__':
    main()
