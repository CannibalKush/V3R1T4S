#!/usr/bin/env python3
"""build_and_cascade.py -- Iterated multi-round Matroid Max-Kill absorption + peel cascade.

Applies iterated exact nullspace absorption (across vw, uw, uv pairings until all three have nullity 0)
to existing schemes and their peels, saves all improved schemes, verifies each with verify_brent.py,
and cascades secondary peels + absorptions to discover all reachable record formats.
"""
import json, os, sys, time
from fractions import Fraction

sys.path.insert(0, os.path.abspath("repo/known-knowns/faster-matrix-multiplication/how-we-built-it"))
sys.path.insert(0, os.path.abspath("runs/2026-10-14-0004"))
sys.path.insert(0, os.path.abspath("runs/2026-10-14-0004/attempts/representation-absorber/code"))

import peel as PEEL
import screen_all as SA
import verify_brent as VB

OUT_DIR = "runs/2026-10-14-0004/attempts/representation-absorber/candidates"
os.makedirs(OUT_DIR, exist_ok=True)

BARS = {
    (11, 13, 13): 1204, (11, 13, 14): 1286, (11, 13, 15): 1362, (11, 14, 14): 1367,
    (11, 14, 15): 1432, (11, 15, 15): 1540, (11, 15, 16): 1605, (11, 16, 16): 1724,
    (12, 12, 13): 1144, (12, 12, 14): 1232, (12, 12, 15): 1280, (12, 13, 13): 1274,
    (12, 13, 14): 1370, (12, 13, 15): 1442, (12, 13, 16): 1509, (12, 14, 14): 1449,
    (12, 14, 15): 1538, (12, 14, 16): 1617, (12, 15, 15): 1600, (12, 15, 16): 1725,
    (12, 16, 16): 1815, (13, 13, 13): 1379, (13, 13, 14): 1511, (13, 13, 15): 1591,
    (13, 13, 16): 1704, (13, 14, 14): 1582, (13, 14, 15): 1681, (13, 14, 16): 1796,
    (13, 15, 15): 1776, (13, 15, 16): 1885, (13, 16, 16): 2022, (14, 14, 14): 1593,
    (14, 14, 15): 1789, (14, 14, 16): 1894, (14, 15, 15): 1848, (14, 15, 16): 2016,
    (14, 16, 16): 2128, (15, 15, 15): 1977, (15, 15, 16): 2132, (15, 16, 16): 2223,
}

TROPHY = {
    (14, 15, 15): 1842,
    (13, 14, 14): 1558,
    (15, 16, 16): 2180,
    (14, 14, 15): 1716,
    (13, 14, 15): 1677,
}

def canonicalize_dims(fmt, u, v, w):
    """If fmt = (n1, n2, n3) is not sorted, we can either keep fmt as-is (since parse_sources and fmmcheck
    sort fmt when comparing, and Perminov JSON stores actual n=[n1,n2,n3]) or transpose/cycle so n1 <= n2 <= n3.
    Let's check: cyclic shift (n1,n2,n3) -> (n2,n3,n1) maps (u,v,w) -> (v,w,u).
    Transpose of A*B=C: B^T * A^T = C^T maps (n1,n2,n3) -> (n3,n2,n1) and transposes each factor matrix:
      U (n1 x n2), V (n2 x n3), W (n3 x n1) -> U_new = V^T (n3 x n2), V_new = U^T (n2 x n1), W_new = W^T (n1 x n3).
    """
    n1, n2, n3 = fmt
    r = len(u)
    # Build 3D factor matrices for each term k
    U = [PEEL.mat_of(u[k], n1, n2) for k in range(r)]
    V = [PEEL.mat_of(v[k], n2, n3) for k in range(r)]
    W = [PEEL.mat_of(w[k], n3, n1) for k in range(r)]

    # Sort dimensions using cyclic shifts and transpose
    while not (n1 <= n2 <= n3):
        if n1 > n2:
            # Swap first two dims: first cycle (n1,n2,n3) -> (n3,n1,n2) then transpose -> (n2,n1,n3)
            # Under (n1,n2,n3) -> (n2,n1,n3):
            # New A is A^T (n2 x n1), New B is C^T (n1 x n3), New C is B^T (n2 x n3), wait:
            # In trilinear form Tr(A B C) where A is n1 x n2, B is n2 x n3, C is n3 x n1:
            # Taking transpose of the matrix product inside Tr(A B C) = Tr(C^T B^T A^T):
            # Let A' = U^T (n2 x n1), B' = W^T (n1 x n3), C' = V^T (n3 x n2).
            # Then Tr(A' B' C') = Tr(U^T W^T V^T) = Tr((V W U)^T) = Tr(U V W)!
            U, V, W = [PEEL.transpose(m) for m in U], [PEEL.transpose(m) for m in W], [PEEL.transpose(m) for m in V]
            n1, n2, n3 = n2, n1, n3
        elif n2 > n3:
            # Swap last two dims:
            # A' = W^T (n1 x n3), B' = V^T (n3 x n2), C' = U^T (n2 x n1)
            U, V, W = [PEEL.transpose(m) for m in W], [PEEL.transpose(m) for m in V], [PEEL.transpose(m) for m in U]
            n1, n2, n3 = n1, n3, n2

    u_flat = [[x for row in U[k] for x in row] for k in range(r)]
    v_flat = [[x for row in V[k] for x in row] for k in range(r)]
    w_flat = [[x for row in W[k] for x in row] for k in range(r)]
    return (n1, n2, n3), u_flat, v_flat, w_flat

def iterated_absorb(fmt, u, v, w, label, pair_order=("uv", "uw", "vw")):
    T = [[list(u[k]), list(v[k]), list(w[k])] for k in range(len(u))]
    PAIR_MAP = {"vw": (1, 2, 0), "uw": (0, 2, 1), "uv": (0, 1, 2)}
    steps = []
    for rnd in range(10):
        changed = False
        for pname in pair_order:
            iy, iz, ix = PAIR_MAP[pname]
            r = len(T)
            Y = [t[iy] for t in T]
            Z = [t[iz] for t in T]
            X = [t[ix] for t in T]
            rk, d, pivs, C = SA.compute_exact_nullspace(Y, Z)
            if d <= 0 or C is None:
                continue
            mk = SA.matroid_maxkill(C, X)
            killed_set = set(mk["killed_terms"])
            new_X = mk["new_X"]
            newT = []
            for k, t in enumerate(T):
                if k in killed_set:
                    continue
                nt = list(t)
                nt[ix] = new_X[k]
                if any(val != 0 for val in nt[ix]):
                    newT.append(nt)
            print(f"  [{label}] round {rnd} {pname}: r={r} -> {len(newT)} (nullity={d}, killed={len(killed_set)})", flush=True)
            steps.append(f"{pname}:-{len(killed_set)}")
            T = newT
            changed = True
        if not changed:
            break
    u2 = [t[0] for t in T]
    v2 = [t[1] for t in T]
    w2 = [t[2] for t in T]
    return u2, v2, w2, steps

def save_and_verify(fmt, u, v, w, note, tag):
    F = PEEL.Field(None)
    fmt_s, u_s, v_s, w_s = canonicalize_dims(fmt, u, v, w)
    r = len(u_s)
    s_str = f"{fmt_s[0]}x{fmt_s[1]}x{fmt_s[2]}"
    fname = f"{s_str}_r{r}_Q_{tag}.json"
    path = os.path.join(OUT_DIR, fname)
    js = PEEL.to_json(fmt_s, u_s, v_s, w_s, F, note=note)
    with open(path, "w") as f:
        json.dump(js, f)
    ok, msg = VB.verify_file(path)
    bar = BARS.get(fmt_s)
    tr = TROPHY.get(fmt_s)
    eff_bar = min(bar, tr) if (bar and tr) else (bar or tr)
    status = "RECORD!" if (ok and eff_bar and r < eff_bar) else ("PASS" if ok else "FAIL")
    print(f"  -> {status} {fname}: {msg} | 4-source bar={bar}, trophy={tr}, margin_vs_bar={r - bar if bar else None}, margin_vs_all={r - eff_bar if eff_bar else None}", flush=True)
    return fmt_s, u_s, v_s, w_s, path, ok

def main():
    F = PEEL.Field(None)
    sdir = "repo/known-knowns/faster-matrix-multiplication/schemes"

    # 1. Direct absorption on 13x14x14_r1558_Q.json
    print("\n--- 1. Absorbing 13x14x14_r1558_Q.json ---", flush=True)
    fmt, u, v, w, _ = PEEL.load_scheme(os.path.join(sdir, "13x14x14_r1558_Q.json"))
    u2, v2, w2, st = iterated_absorb(fmt, u, v, w, "13x14x14_r1558")
    f_13_14_14, u_1544, v_1544, w_1544, _, _ = save_and_verify(
        fmt, u2, v2, w2, "iterated matroid absorption of 13x14x14_r1558_Q.json (" + ",".join(st) + ")", "abs"
    )

    # 2. Direct absorption on 14x14x15_r1716_Q.json
    print("\n--- 2. Absorbing 14x14x15_r1716_Q.json ---", flush=True)
    fmt, u, v, w, _ = PEEL.load_scheme(os.path.join(sdir, "14x14x15_r1716_Q.json"))
    u2, v2, w2, st = iterated_absorb(fmt, u, v, w, "14x14x15_r1716")
    f_14_14_15, u_1715, v_1715, w_1715, _, _ = save_and_verify(
        fmt, u2, v2, w2, "iterated matroid absorption of 14x14x15_r1716_Q.json (" + ",".join(st) + ")", "abs"
    )

    # 3. Direct absorption on 13x14x15_r1677_Q.json (try both uv-first and uw-first)
    print("\n--- 3. Absorbing 13x14x15_r1677_Q.json ---", flush=True)
    fmt, u, v, w, _ = PEEL.load_scheme(os.path.join(sdir, "13x14x15_r1677_Q.json"))
    for order in [("uv", "uw", "vw"), ("uw", "uv", "vw")]:
        u2, v2, w2, st = iterated_absorb(fmt, u, v, w, "13x14x15_r1677_" + "".join(order), pair_order=order)
        save_and_verify(fmt, u2, v2, w2, "iterated matroid absorption of 13x14x15_r1677_Q.json (" + ",".join(st) + ")", "".join(order))

    # 4. Peel 14x14x15_r1715 along all axes + absorb (especially axis=1 -> 13x14x15!)
    print("\n--- 4. Peeling 14x14x15_r1715 + absorbing ---", flush=True)
    best_13_14_15 = None
    for ax in (0, 1, 2):
        cen = PEEL.peel_census(f_14_14_15, u_1715, v_1715, w_1715, F, ax)
        fmt_p, up, vp, wp = PEEL.project(f_14_14_15, u_1715, v_1715, w_1715, F, ax, cen["best_e"], cen["best_f"])
        u2, v2, w2, st = iterated_absorb(fmt_p, up, vp, wp, f"peel(14x14x15_r1715,ax={ax})")
        fs, us, vs, ws, _, _ = save_and_verify(
            fmt_p, u2, v2, w2,
            f"peel of 14x14x15_r1715 axis {ax} e={cen['best_e']} f={cen['best_f']} + absorb ({','.join(st)})",
            f"from1715_ax{ax}"
        )
        if fs == (13, 14, 15) and (best_13_14_15 is None or len(us) < len(best_13_14_15[1])):
            best_13_14_15 = (fs, us, vs, ws)

    # 5. Peel 14x15x15_r1842_Q.json along axis=0 -> 13x15x15 + absorb
    print("\n--- 5. Peeling 14x15x15_r1842_Q.json along axis=0 -> 13x15x15 + absorbing ---", flush=True)
    fmt, u, v, w, _ = PEEL.load_scheme(os.path.join(sdir, "14x15x15_r1842_Q.json"))
    cen = PEEL.peel_census(fmt, u, v, w, F, 0)
    fmt_p, up, vp, wp = PEEL.project(fmt, u, v, w, F, 0, cen["best_e"], cen["best_f"])
    u2, v2, w2, st = iterated_absorb(fmt_p, up, vp, wp, "peel(14x15x15_r1842,ax=0)")
    f_13_15_15, u_1763, v_1763, w_1763, _, _ = save_and_verify(
        fmt_p, u2, v2, w2,
        f"peel of 14x15x15_r1842_Q.json axis 0 e={cen['best_e']} f={cen['best_f']} + absorb ({','.join(st)})",
        "from1842_ax0"
    )

    # 6. Peel 15x16x16_r2180_Q.json along all axes + absorb (axis=0 -> 14x16x16, axis=1,2 -> 15x15x16)
    print("\n--- 6. Peeling 15x16x16_r2180_Q.json + absorbing ---", flush=True)
    fmt, u, v, w, _ = PEEL.load_scheme(os.path.join(sdir, "15x16x16_r2180_Q.json"))
    best_14_16_16 = None
    for ax in (0, 1, 2):
        cen = PEEL.peel_census(fmt, u, v, w, F, ax)
        fmt_p, up, vp, wp = PEEL.project(fmt, u, v, w, F, ax, cen["best_e"], cen["best_f"])
        u2, v2, w2, st = iterated_absorb(fmt_p, up, vp, wp, f"peel(15x16x16_r2180,ax={ax})")
        fs, us, vs, ws, _, _ = save_and_verify(
            fmt_p, u2, v2, w2,
            f"peel of 15x16x16_r2180_Q.json axis {ax} e={cen['best_e']} f={cen['best_f']} + absorb ({','.join(st)})",
            f"from2180_ax{ax}"
        )
        if fs == (14, 16, 16):
            best_14_16_16 = (fs, us, vs, ws)

    # 7. Peel 13x14x14_r1544 along all axes + absorb (axis=0 -> 12x14x14, axis=1,2 -> 13x13x14)
    print("\n--- 7. Peeling 13x14x14_r1544 + absorbing ---", flush=True)
    best_13_13_14 = None
    for ax in (0, 1, 2):
        cen = PEEL.peel_census(f_13_14_14, u_1544, v_1544, w_1544, F, ax)
        fmt_p, up, vp, wp = PEEL.project(f_13_14_14, u_1544, v_1544, w_1544, F, ax, cen["best_e"], cen["best_f"])
        u2, v2, w2, st = iterated_absorb(fmt_p, up, vp, wp, f"peel(13x14x14_r1544,ax={ax})")
        fs, us, vs, ws, _, _ = save_and_verify(
            fmt_p, u2, v2, w2,
            f"peel of 13x14x14_r1544 axis {ax} e={cen['best_e']} f={cen['best_f']} + absorb ({','.join(st)})",
            f"from1544_ax{ax}"
        )
        if fs == (13, 13, 14) and (best_13_13_14 is None or len(us) < len(best_13_13_14[1])):
            best_13_13_14 = (fs, us, vs, ws)

    # 8. Cascade peels from our new 14x16x16, 13x15x15, and 13x14x15!
    for parent_name, parent in [("14x16x16", best_14_16_16), ("13x15x15", (f_13_15_15, u_1763, v_1763, w_1763)), ("13x14x15", best_13_14_15), ("13x13x14", best_13_13_14)]:
        if parent is None:
            continue
        pf, pu, pv, pw = parent
        print(f"\n--- 8. Cascading peel from {parent_name} (rank {len(pu)}) ---", flush=True)
        for ax in (0, 1, 2):
            cen = PEEL.peel_census(pf, pu, pv, pw, F, ax)
            fmt_p, up, vp, wp = PEEL.project(pf, pu, pv, pw, F, ax, cen["best_e"], cen["best_f"])
            u2, v2, w2, st = iterated_absorb(fmt_p, up, vp, wp, f"peel({parent_name}_r{len(pu)},ax={ax})")
            save_and_verify(
                fmt_p, u2, v2, w2,
                f"peel of {parent_name}_r{len(pu)} axis {ax} e={cen['best_e']} f={cen['best_f']} + absorb ({','.join(st)})",
                f"from_{parent_name}_r{len(pu)}_ax{ax}"
            )

if __name__ == "__main__":
    main()
