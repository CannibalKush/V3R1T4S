#!/usr/bin/env python3
"""make_result_13x15x15.py -- Deterministic builder for <13, 15, 15> rank 1763 over Q.

Derives 13x15x15_r1763_Q.json from 14x15x15_r1842_Q.json in two exact steps:
1. Generalised one-slice peel along axis n (axis=0) with e = e_1 + e_13, f = e_1,
   which annihilates 46 rank-one terms (1842 -> 1796).
2. Exact 20-dimensional left nullspace extraction of the (v (x) w) pairing over Q
   (via 3-prime CRT + rational reconstruction, certified by exact Fraction dot products),
   followed by Rado-Edmonds matroid max-kill u-factor shifting, which annihilates 33 terms
   simultaneously (1796 -> 1763).
3. Normalizes each rank-one product u_k (x) v_k (x) w_k over Q so u_k, v_k are primitive
   integer vectors (first non-zero entry > 0, gcd = 1) and w_k carries the exact rational
   multiplier, and serializes in compact sparse_flat_pairs JSON (< 1 MB).
"""
import hashlib, json, math, os, subprocess, sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath("repo/known-knowns/faster-matrix-multiplication/how-we-built-it"))
import peel as PEEL
import screen_all as SA

def primitive_int_vec(vec):
    """Scale rational vector vec != 0 so entries are integers with gcd=1 and first non-zero > 0.
    Returns (int_vec, scale_factor) such that vec = scale_factor * int_vec."""
    lcm_d = 1
    for x in vec:
        if x != 0:
            lcm_d = math.lcm(lcm_d, x.denominator)
    iv = [int(x * lcm_d) for x in vec]
    g = 0
    for x in iv:
        if x != 0:
            g = math.gcd(g, abs(x))
    first_nz = next(x for x in iv if x != 0)
    if first_nz < 0:
        g = -g
    iv = [x // g for x in iv]
    scale = Fraction(g, lcm_d)
    return iv, scale

def to_sparse_flat(vec):
    out = []
    for idx, val in enumerate(vec):
        if val != 0:
            out.append(idx)
            if isinstance(val, int) or val.denominator == 1:
                out.append(int(val))
            else:
                out.append(f"{val.numerator}/{val.denominator}")
    return out

def main():
    F = PEEL.Field(None)
    src_path = "repo/known-knowns/faster-matrix-multiplication/schemes/14x15x15_r1842_Q.json"
    fmt, u, v, w, _ = PEEL.load_scheme(src_path)
    cen = PEEL.peel_census(fmt, u, v, w, F, 0)
    print(f"Step 1 (peel axis=0): best_z={cen['best_z']}, e={cen['best_e']}, f={cen['best_f']}")
    fmt2, u2, v2, w2 = PEEL.project(fmt, u, v, w, F, 0, cen["best_e"], cen["best_f"])
    print(f"Peeled format: {fmt2}, rank: {len(u2)}")

    rk, d, pivs, C = SA.compute_exact_nullspace(v2, w2)
    print(f"Step 2 (vw nullspace): rank={rk}/{len(u2)}, nullity={d}")
    mk = SA.matroid_maxkill(C, u2)
    killed = set(mk["killed_terms"])
    new_u = mk["new_X"]

    u_out, v_out, w_out = [], [], []
    for k in range(len(u2)):
        if k in killed:
            continue
        uk, vk, wk = new_u[k], v2[k], w2[k]
        if all(x == 0 for x in uk):
            continue
        ui, su = primitive_int_vec(uk)
        vi, sv = primitive_int_vec(vk)
        ws = [x * su * sv for x in wk]
        u_out.append(to_sparse_flat(ui))
        v_out.append(to_sparse_flat(vi))
        w_out.append(to_sparse_flat(ws))

    r_final = len(u_out)
    print(f"Step 3 (absorbed & normalized): final rank = {r_final} (killed {len(killed)} terms)")

    out_dir = os.path.join(os.path.dirname(HERE), "result")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "13x15x15_r1763_Q.json")
    obj = {
        "n": list(fmt2),
        "m": r_final,
        "ring": "Q",
        "encoding": "sparse_flat_pairs",
        "note": (
            "13x15x15 rank 1763 over Q: axis-0 generalised slice peel (e=e_1+e_7, f=e_7, -46 terms) "
            "of 14x15x15_r1842_Q.json followed by exact 20-dimensional vw-pairing nullspace matroid max-kill (-33 terms)."
        ),
        "u": u_out,
        "v": v_out,
        "w": w_out,
    }
    raw = json.dumps(obj, separators=(",", ":")) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(raw)
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    print(f"Wrote result/13x15x15_r1763_Q.json ({len(raw)} bytes, sha256={h})")

    chk = subprocess.run([sys.executable, "runs/2026-10-14-0004/verify_brent.py", out_path],
                         capture_output=True, text=True, check=True)
    print(chk.stdout.strip())

if __name__ == "__main__":
    main()
