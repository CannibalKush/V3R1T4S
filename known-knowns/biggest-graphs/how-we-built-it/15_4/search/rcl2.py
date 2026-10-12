"""rcl2: route-chart lifts over GENERIC finite groups (multiplication tables from groups.py).

G on V = H x F_q^s:  (h,x) ~ (h*t, A_t x + lam b_t), lam in Lambda_t, over the alphabet of generators t.
 paired label t, t' = t^-1:  A_t' = A_t^-1, b_t' = A_t^-1 b_t, Lambda_t' = -Lambda_t
 involution label t:         A_t^2 = I, A_t b_t = b_t, Lambda_t = -Lambda_t
Left multiplication by H is an automorphism, so BFS from the q^s sources (e,x) decides diameters.

Stage 1: choose generators so every non-identity element of H is the endpoint of a reduced word of length 4
         ("hard" miss = not reachable by reduced words of length 4 or 2; "soft" = only by length 2).
Stage 2: anneal the chart on the K2xG defect (pairs ((e,x),0) -> any vertex of K2xG not reached in D+1 steps).

Library module (imported by exh_bip.py and bip_proxy_search.py; its standalone command-line driver is omitted here).
Group strings: psl2:p, pgl2:p, sl2:p, gl2:p, A:n, S:n, C:k, meta:m,k,r ; products joined by 'x' e.g. 'sl2:3xC:6'
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import rcl, groups


def parse_group(sx):
    parts = sx.split('x')
    G = None
    for p in parts:
        kind, arg = p.split(':')
        if kind == 'psl2': H = groups.psl2(int(arg))
        elif kind == 'pgl2': H = groups.pgl2(int(arg))
        elif kind == 'sl2': H = groups.sl2(int(arg))
        elif kind == 'gl2': H = groups.gl2(int(arg))
        elif kind == 'A': H = groups.alternating(int(arg))
        elif kind == 'S': H = groups.symmetric(int(arg))
        elif kind == 'C': H = groups.cyclic(int(arg))
        elif kind == 'meta':
            m, k, r = map(int, arg.split(',')); H = groups.metacyclic(m, k, r)
        else:
            raise ValueError(kind)
        G = H if G is None else groups.direct_product(G, H)
    G['gstr'] = sx
    return G


def parse_spec(s):
    spec = []
    for tok in s.split(','):
        kind = 'pair' if tok.startswith('pair') else 'inv'
        spec.append((kind, int(tok[4:] if kind == 'pair' else tok[3:])))
    return spec


def sym_lams(p, q):
    if p == q: return list(range(q))
    if p == 1: return [0]
    if p == 2: return [1, q - 1]
    if p == 3: return [0, 1, q - 1]
    raise ValueError


# ------------------------------------------------------------------------------------------- stage 1
def alphabet(H, spec, gens):
    els, inv = [], []
    for (kind, p), g in zip(spec, gens):
        if kind == 'pair':
            i = len(els); els += [g, H['inv'](g)]; inv += [i + 1, i]
        else:
            i = len(els); els += [g]; inv += [i]
    return els, inv


def word_counts(H, els, inv, L):
    n = H['n']; nl = len(els)
    R = np.array([H['rmul'](g) for g in els])
    st = np.zeros((n, nl), dtype=np.int64)
    for t in range(nl):
        st[R[t][0], t] += 1
    for _ in range(L - 1):
        nxt = np.zeros_like(st)
        tot = st.sum(axis=1)
        for t2 in range(nl):
            np.add.at(nxt[:, t2], R[t2], tot - st[:, inv[t2]])
        st = nxt
    return st.sum(axis=1)


def stage1_score(H, spec, gens, L=4):
    els, inv = alphabet(H, spec, gens)
    if len(set(els)) != len(els) or 0 in els:
        return (10 ** 9, 0, 0)
    c4 = word_counts(H, els, inv, L)
    c2 = word_counts(H, els, inv, L - 2)
    hard = int(((c4[1:] == 0) & (c2[1:] == 0)).sum())
    soft = int(((c4[1:] == 0) & (c2[1:] > 0)).sum())
    ones = int((c4[1:] == 1).sum())
    return (hard, soft, ones)


def rand_gen(H, kind, rng):
    for _ in range(100000):
        g = H['sample'](rng)
        if (kind == 'inv') == H['is_inv'](g):
            return g
    return None


def stage1(H, spec, rng, iters=3000, T0=2.0):
    gens = [rand_gen(H, k, rng) for k, p in spec]
    if any(g is None for g in gens):
        return None, None
    cur = stage1_score(H, spec, gens); best = (cur, list(gens))
    T = T0
    for it in range(iters):
        i = int(rng.integers(len(spec)))
        old = gens[i]
        gens[i] = rand_gen(H, spec[i][0], rng)
        new = stage1_score(H, spec, gens)
        f = lambda s: s[0] * 1000 + s[1] * 10 + s[2] * 0.1
        if f(new) <= f(cur) or rng.random() < np.exp(-(f(new) - f(cur)) / max(T, 1e-9)):
            cur = new
            if f(cur) < f(best[0]):
                best = (cur, list(gens))
        else:
            gens[i] = old
        T *= 0.999
    return best


# ------------------------------------------------------------------------------------------- stage 2
class Lift:
    def __init__(self, H, spec, gens, q, s, D, rng):
        self.H, self.spec, self.gens, self.q, self.s, self.D, self.rng = H, spec, list(gens), q, s, D, rng
        self.Q = q ** s
        self.sources = np.arange(self.Q, dtype=np.int64)
        self.chart = [self.rand_chart(i) for i in range(len(spec))]

    def rand_chart(self, i):
        q, s = self.q, self.s
        kind, p = self.spec[i]
        if kind == 'pair':
            A = rcl.random_gl(q, s, self.rng)
            b = self.rng.integers(0, q, size=s)
            while not b.any():
                b = self.rng.integers(0, q, size=s)
            return (A, b)
        return rcl.random_involution(q, s, self.rng)

    def tweak(self, i):
        q, s = self.q, self.s
        kind, p = self.spec[i]
        if kind == 'inv' or self.rng.random() < 0.15:
            self.chart[i] = self.rand_chart(i); return
        A, b = self.chart[i]
        if self.rng.random() < 0.7:
            for _ in range(100):
                A2 = A.copy(); A2[self.rng.integers(s), self.rng.integers(s)] = self.rng.integers(q)
                if rcl.mat_inv_mod(A2, q) is not None:
                    self.chart[i] = (A2, b); return
        else:
            b2 = b.copy(); b2[self.rng.integers(s)] = self.rng.integers(q)
            if b2.any():
                self.chart[i] = (A, b2)

    def labels(self):
        out = []; q = self.q
        for (kind, p), g, (A, b) in zip(self.spec, self.gens, self.chart):
            lams = sym_lams(p, q)
            out.append((g, A, b, lams))
            if kind == 'pair':
                Ai = rcl.mat_inv_mod(A, q)
                out.append((self.H['inv'](g), Ai, (Ai @ b) % q, [(-l) % q for l in lams]))
        return out

    def build(self):
        Q = self.Q; n = self.H['n']
        cols = []
        for g, A, b, lams in self.labels():
            R = self.H['rmul'](g)
            T = rcl.affine_tables(A, b, self.q, self.s, lams)
            for j in range(T.shape[1]):
                cols.append((R[:, None] * Q + T[None, :, j]).reshape(-1))
        return np.stack(cols, axis=1).astype(np.int64)

    def defect(self, mode='k2'):
        nbr = self.build()
        if mode == 'k2':
            return int(rcl.k2_defect(nbr, self.sources, self.D + 1)[0])
        return int(rcl.g_defect(nbr, self.sources, self.D)[0])

    def state(self):
        return dict(group=self.H['gstr'], n=self.H['n'], spec=self.spec, q=self.q, s=self.s, D=self.D,
                    gens=[int(g) for g in self.gens], A=[c[0].tolist() for c in self.chart],
                    b=[c[1].tolist() for c in self.chart])


def stage2(lift, iters, T0, mode='k2', t_end=None, progress=0):
    cur = lift.defect(mode); best = (cur, lift.state())
    T = T0
    t0 = time.time()
    for it in range(iters):
        if progress and it % progress == 0 and it:
            print(json.dumps(dict(it=it, cur=cur, best=best[0], T=round(T, 2), sec=round(time.time() - t0))), flush=True)
        if t_end and time.time() > t_end:
            break
        i = int(lift.rng.integers(len(lift.spec)))
        old = lift.chart[i]
        lift.tweak(i)
        new = lift.defect(mode)
        if new <= cur or lift.rng.random() < np.exp(-(new - cur) / max(T, 1e-9)):
            cur = new
            if cur < best[0]:
                best = (cur, lift.state())
                if cur == 0:
                    break
        else:
            lift.chart[i] = old
        T = max(T * 0.9995, 0.5)
    return best, it + 1


def lift_from_state(st):
    H = parse_group(st['group'])
    spec = [tuple(x) for x in st['spec']]
    L = Lift(H, spec, st['gens'], st['q'], st['s'], st['D'], np.random.default_rng(0))
    L.chart = [(np.array(A, dtype=np.int64), np.array(b, dtype=np.int64)) for A, b in zip(st['A'], st['b'])]
    return L
