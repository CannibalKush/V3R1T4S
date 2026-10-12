#!/usr/bin/env python3
"""Standalone generator (numpy only) of the (15,4) graph on 13365 vertices, directly from the 381-byte state JSON.

Construction (route-chart lift over a Schreier coset graph):
  Gamma = Z_11 x|_2 Z_30, (i,j)*(i',j') = (i + 2^j i' mod 11, j + j' mod 30), element index h = 30 i + j.
  Letters (from the state): a, a^-1, b, b^-1 (pairs) and c (involution), with charts (A_t, b_t) over F_3^4.
  Lift L: vertices (h, x), h in Gamma, x in F_3^4 (base-3 code); edges (h,x) ~ (h t, A_t x + lam b_t), lam in F_3.
  c0 = (0,15) is an involution of Gamma; rho(h,x) = (c0 h, x) is an automorphism of L (left and right
  multiplication commute) and it swaps the parity of the Z_30 coordinate.
  The graph G = L / <rho>: vertices are the 13365 rho-orbits, labelled by the rank of min(v, rho v) with
  v = 81 h + x; [u] ~ [w] iff u ~ w or u ~ rho(w); loops (u ~ rho u) dropped.
  Equivalently: the route-chart lift over the Schreier coset graph <c0>\\Cay(Gamma, {a,a^-1,b,b^-1,c}).
Usage: gen_G_15_4_direct.py STATE.json OUT.edges
"""
import sys, json, itertools
import numpy as np
st = json.load(open(sys.argv[1])); st = st.get('state', st)
m, k, r = map(int, st['group'].split(':')[1].split(','))
assert (m, k, r) == (11, 30, 2) and st['q'] == 3 and st['s'] == 4
n = m * k
rp = [pow(r, j, m) for j in range(k)]
def mul(g, h):
    i1, j1 = divmod(g, k); i2, j2 = divmod(h, k)
    return ((i1 + rp[j1] * i2) % m) * k + (j1 + j2) % k
def inv(g):
    i, j = divmod(g, k); jj = (-j) % k
    return ((-rp[jj] * i) % m) * k + jj
def minv3(A):
    M = np.concatenate([np.array(A) % 3, np.eye(4, dtype=int)], axis=1)
    for c in range(4):
        p = next(i for i in range(c, 4) if M[i, c] % 3)
        M[[c, p]] = M[[p, c]]
        M[c] = (M[c] * (1 if M[c, c] == 1 else 2)) % 3
        for i in range(4):
            if i != c and M[i, c]:
                M[i] = (M[i] - M[i, c] * M[c]) % 3
    return M[:, 4:] % 3
ga, gb, gc = st['gens']
Aa, Ab, Ac = [np.array(x) for x in st['A']]
ba, bb, bc = [np.array(x) for x in st['b']]
assert np.array_equal((Ac @ Ac) % 3, np.eye(4, dtype=int)) and np.array_equal((Ac @ bc) % 3, bc % 3)
Aai, Abi = minv3(Aa), minv3(Ab)
letters = [(ga, Aa, ba), (inv(ga), Aai, (Aai @ ba) % 3), (gb, Ab, bb), (inv(gb), Abi, (Abi @ bb) % 3), (gc, Ac, bc)]
X = np.array(list(itertools.product(range(3), repeat=4)))[:, ::-1]
X = X[np.argsort(X @ np.array([1, 3, 9, 27]))]
pw = np.array([1, 3, 9, 27])
c0 = 0 * k + 15
assert mul(c0, c0) == 0 and all((mul(c0, h) % k) % 2 != (h % k) % 2 for h in range(n))
NL = n * 81
rho = np.array([mul(c0, v // 81) * 81 + v % 81 for v in range(NL)])
rep = np.minimum(np.arange(NL), rho)
lab = -np.ones(NL, dtype=np.int64); u = np.unique(rep); lab[u] = np.arange(len(u))
edges = set()
for h in range(n):
    for g, A, b in letters:
        h2 = mul(h, g)
        Y = (X @ A.T) % 3
        for lam in range(3):
            tgt = ((Y + lam * b) % 3) @ pw
            for x in range(81):
                p, q = lab[rep[h * 81 + x]], lab[rep[h2 * 81 + int(tgt[x])]]
                if p != q:
                    edges.add((min(p, q), max(p, q)))
with open(sys.argv[2], 'w') as f:
    for a_, b_ in sorted(edges):
        f.write(f'{a_} {b_}\n')
print(f'N={len(u)} edges={len(edges)}')
