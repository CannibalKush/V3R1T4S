#!/usr/bin/env python3
"""Kronecker (tensor) product of two schemes in Perminov's layout -> naive scheme JSON (no fresh variables).
A index (i1*n2+i2)*(m1*m2) + (j1*m2+j2); B likewise; output C^T index k*n+i with k=k1*p2+k2, i=i1*n2+i2;
product q = q1*r2 + q2. usage: kron_scheme.py s1.json s2.json out.json"""
import json, sys
sys.path.insert(0, '[addcomp]/tools')
import graphs as G
from check_slp import check
d1, d2 = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
(n1, m1, p1), r1 = d1['n'], d1['m']; (n2, m2, p2), r2 = d2['n'], d2['m']
U1, V1, W1 = G.maps_of(d1); U2, V2, W2 = G.maps_of(d2)
n, m, p, r = n1 * n2, m1 * m2, p1 * p2, r1 * r2
def kron_in(X1, X2, R1, C1, R2, C2):
    C = C1 * C2; out = []
    for q1 in range(len(X1)):
        for q2 in range(len(X2)):
            row = []
            for a, va in enumerate(X1[q1]):
                if not va: continue
                i1, j1 = divmod(a, C1)
                for b, vb in enumerate(X2[q2]):
                    if not vb: continue
                    i2, j2 = divmod(b, C2)
                    row.append({"index": (i1 * R2 + i2) * C + (j1 * C2 + j2), "value": va * vb})
            out.append(sorted(row, key=lambda t: t['index']))
    return out
U = kron_in(U1, U2, n1, m1, n2, m2); V = kron_in(V1, V2, m1, p1, m2, p2)
# W: rows = outputs c = k*n + i over products
W = []
for k in range(p):
    k1, k2 = divmod(k, p2)
    for i in range(n):
        i1, i2 = divmod(i, n2)
        w1 = W1[k1 * n1 + i1]; w2 = W2[k2 * n2 + i2]
        row = [{"index": q1 * r2 + q2, "value": a * b} for q1, a in enumerate(w1) if a for q2, b in enumerate(w2) if b]
        W.append(row)
out = {"n": [n, m, p], "m": r, "z2": False, "u_fresh": [], "u": U, "v_fresh": [], "v": V, "w_fresh": [], "w": W}
c = check(out)
out["complexity"] = {"naive": c['naive_total'], "reduced": c['adds_total']}
json.dump(out, open(sys.argv[3], 'w'))
print(json.dumps(c))
