"""Sweep slice-and-absorb from one parent scheme: shrink any axis, up to `depth` steps, keep the best scheme
per child format, compare with the live bars (fmm_sota.json and Perminov's status table).

Usage: python -I sweep.py PARENT.json --depth 2 --top 4 --out DIR [--seed 1]
Writes DIR/<parent stem>.csv (one row per child format reached) and DIR/<format>_r<rank>_Q.json for every child
whose rank is at most bar + 2, each re-checked with the exact Brent equations before saving.
"""
import argparse
import csv
import json
import os
import random
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa  # noqa: E402

DATA = os.path.expanduser("~/v3r1t4s/fmm/data")


def load_bars():
    bars = {}
    if not os.path.exists(os.path.join(DATA, "raw.githubusercontent.com_sedoglavic_fmm_digest_master_fmm_sota.json")):
        return bars  # no local table copies: run without bars (use --save-all to keep the children)
    d = json.load(open(os.path.join(DATA, "raw.githubusercontent.com_sedoglavic_fmm_digest_master_fmm_sota.json")))
    for e in d["entries"]:
        bars[tuple(sorted(e["format"]))] = (e["rank"], "fmm_sota")
    txt = open(os.path.join(DATA, "raw.githubusercontent.com_dronperminov_FastMatrixMultiplication_master_README.md")).read()
    status = txt[txt.find("## Research Findings & Status"):]
    for m in re.finditer(r"^\| `(\d+)x(\d+)x(\d+)` \|([^|]*)\|([^|]*)\|([^|]*)\|", status, re.M):
        fmt = tuple(sorted(int(x) for x in m.group(1, 2, 3)))
        vals = []
        for col in m.group(4, 5, 6):
            mm = re.search(r"\d+", col)
            if mm:
                vals.append(int(mm.group()))
        if vals:
            v = min(vals)
            if fmt not in bars or v < bars[fmt][0]:
                bars[fmt] = (v, "perminov")
    return bars


def best_child(n, terms, axis, top, seed):
    nr, tr = sa.rotate_to(n, terms, axis)
    best = None
    for idx, (kills, f, e) in enumerate(sa.slice_candidates(nr, tr, top=top)):
        ns, ts = sa.slice_dim1(nr, tr, f, e)
        ts2, ab = sa.absorb_all(ns, ts, random.Random(seed * 1000 + idx))
        cn, ct = sa.rotate_to(ns, ts2, 3 - axis)
        info = dict(f=dict(f), e=dict(e), slice_kills=len(tr) - len(ts), absorb_kills=ab)
        if best is None or len(ct) < len(best[1]):
            best = (cn, ct, info)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("parent")
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--top", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", required=True)
    ap.add_argument("--save-all", action="store_true", help="save every child, not only those near a bar")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    bars = load_bars()
    t0 = time.time()
    n, terms = sa.load(a.parent)
    stem = os.path.basename(a.parent).replace(".json", "")
    print(f"parent {sa.fmt(n)} rank {len(terms)} from {stem}", flush=True)
    frontier = {tuple(n): (n, terms, [])}
    rows = []
    seen_best = {}
    for depth in range(1, a.depth + 1):
        nxt = {}
        for _, (pn, pt, path) in frontier.items():
            for axis in range(3):
                if pn[axis] <= 2:
                    continue
                cn, ct, info = best_child(pn, pt, axis, a.top, a.seed + depth)
                key = tuple(sorted(cn))
                bar, src = bars.get(key, (None, None))
                step = path + [f"{sa.fmt(pn)}-axis{axis}(-{info['slice_kills']},-{info['absorb_kills']})"]
                margin = None if bar is None else len(ct) - bar
                print(f"  depth {depth}: {sa.fmt(pn)} axis {axis} -> {sa.fmt(cn)} rank {len(ct)} bar {bar} ({src}) "
                      f"margin {margin}  [{time.time() - t0:.0f}s]", flush=True)
                if key not in seen_best or len(ct) < seen_best[key][0]:
                    seen_best[key] = (len(ct), cn, ct, step, bar, src)
                if tuple(cn) not in nxt or len(ct) < len(nxt[tuple(cn)][1]):
                    nxt[tuple(cn)] = (cn, ct, step)
        frontier = nxt
    with open(os.path.join(a.out, f"{stem}.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["parent", "child_sorted", "rank", "bar", "bar_source", "margin", "path", "saved"])
        for key, (rank, cn, ct, step, bar, src) in sorted(seen_best.items()):
            saved = ""
            if a.save_all or (bar is not None and rank <= bar + 2):
                ok = sa.brent_ok(cn, ct)
                if ok:
                    saved = f"{sa.fmt(cn)}_r{rank}_Q.json"
                    sa.save(os.path.join(a.out, saved), cn, ct,
                            note=f"{sa.fmt(cn)} rank {rank} over Q by slice and absorb from {stem}: " + " | ".join(step))
                else:
                    saved = "BRENT_FAIL"
            w.writerow([stem, "x".join(map(str, key)), rank, bar, src, None if bar is None else rank - bar,
                        " | ".join(step), saved])
            print(f"RESULT {stem} -> {'x'.join(map(str, key))}: rank {rank} vs bar {bar} ({src}) "
                  f"margin {None if bar is None else rank - bar} {saved}", flush=True)
    print(f"done in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
