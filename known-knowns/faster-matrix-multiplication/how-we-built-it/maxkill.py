#!/usr/bin/env python3
"""maxkill.py -- max-kill absorption of the nullspace of one pairing (uv, uw or vw) of a scheme.

1. Exact left nullspace of the pairing matrix {y_k (x) z_k}: canonical RREF basis mod 3 primes
   (absorb_exact.left_null_canonical, Khatri-Rao projection), CRT + rational reconstruction, then EVERY row is checked
   exactly over Q (absorb_exact.exact_zero).  Rows c^(s), s = 1..d.
2. Shifts: T = sum_k y (x) z (x) (x_k - sum_s c^(s)_k zeta_s) for any zeta_s (x = free factor); term k dies iff
   x_k = sum_s c^(s)_k zeta_s.  Terms in exactly one block s (support of c_k = {s}) die iff zeta_s = x_k / c_sk, so per
   block we pick the normalized free factor with the largest multiplicity (the RREF pivot is always a one-block term,
   so this kills at least as many ONE-BLOCK terms as absorb_exact's RREF absorption).  Multi-block ("hub") terms die
   only if their equation holds exactly for the chosen shifts (checked, not optimised: if RREF happened to kill a hub,
   this could kill fewer in total).  One pairing per call; re-screen and iterate.
3. Writes CHILD.json and CERT.json (pairing, killed parent terms, null rows c^(s), shifts zeta_s).  The child must
   still be verified with ../verify-it-yourself/fmmcheck.py.  Deterministic (fixed seeds).
Usage: python3 maxkill.py SCHEME.json PAIRING CHILD.json CERT.json     (needs numpy and numba)"""
import json
import os
import sys
import time
from collections import defaultdict
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import absorb_exact as AE  # noqa: E402  (only its nullspace helpers are used)


def s_(x):
    return int(x) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


def main():
    src, pairing, childp, certp = sys.argv[1:5]
    t0 = time.time()
    n, T = AE.load(src)
    iy, iz = {"uv": (0, 1), "uw": (0, 2), "vw": (1, 2)}[pairing]
    ix = 3 - iy - iz
    Y = [t[iy] for t in T]
    Z = [t[iz] for t in T]
    res = [AE.left_null_canonical(Y, Z, p, seed=17) for p in AE.PRIMES]
    ranks = [x[0] for x in res]
    rep = {"src": src, "pairing": pairing, "r": len(T), "rank_modp": ranks}
    if all(x[1] is None for x in res):
        rep["nullity"] = 0
        print(json.dumps(rep))
        return
    pivs = [x[2] for x in res]
    assert all(pv == pivs[0] for pv in pivs) and all(x[1] is not None for x in res), "prime mismatch"
    C = AE.crt_ratrec([x[1] for x in res], AE.PRIMES)
    assert C is not None, "rational reconstruction failed"
    ok = [AE.exact_zero(c, Y, Z) for c in C]
    assert all(ok), "a null vector failed the exact check"
    d, r = len(C), len(T)
    rep["nullity"] = d
    rep["rref_pivots"] = pivs[0]
    blocks, hubs = defaultdict(list), []
    for k in range(r):
        sup = [s for s in range(d) if C[s][k] != 0]
        if len(sup) == 1:
            blocks[sup[0]].append(k)
        elif len(sup) > 1:
            hubs.append(k)
    zeta, chosen = [], {}
    for s in range(d):
        groups = defaultdict(list)
        for k in blocks[s]:
            groups[tuple(x / C[s][k] for x in T[k][ix])].append(k)
        z = max(groups, key=lambda g: (len(groups[g]), -groups[g][0]))
        zeta.append(list(z))
        chosen[s] = groups[z]
    newT, killed = [], []
    for k, t in enumerate(T):
        x = list(t[ix])
        for s in range(d):
            if C[s][k] != 0:
                x = [a - C[s][k] * b for a, b in zip(x, zeta[s])]
        if all(v == 0 for v in x):
            killed.append(k)
        else:
            nt = list(t)
            nt[ix] = x
            newT.append(nt)
    rep.update({"blocks": {s: len(blocks[s]) for s in range(d)}, "hubs": hubs,
                "chosen_per_block": chosen, "killed": killed, "n_killed": len(killed), "r_new": len(newT),
                "rref_would_kill": d, "sec": round(time.time() - t0, 1)})
    out = {"n": n, "m": len(newT), "ring": "Q",
           "note": "max-kill absorption of the %s nullspace of %s; killed %s" % (pairing, src.split("/")[-1], killed),
           "u": [[s_(x) for x in t[0]] for t in newT], "v": [[s_(x) for x in t[1]] for t in newT],
           "w": [[s_(x) for x in t[2]] for t in newT]}
    json.dump(out, open(childp, "w"))
    json.dump({"parent": src.split("/")[-1], "pairing": pairing, "killed_parent_terms": killed,
               "null_rows": [[str(x) for x in row] for row in C], "zeta": [[str(x) for x in z] for z in zeta]},
              open(certp, "w"))
    print(json.dumps(rep, default=str))


if __name__ == "__main__":
    main()
