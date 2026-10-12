#!/usr/bin/env python3
"""sweep.py -- generalised-peel sweep over scheme files.

For every scheme file and each axis (n, m, p): find the best coordinate peel and the best generalised (e,f) peel
(peel.peel_census), estimate the projected rank r - z, and whenever that is within --margin of the bar of the
smaller (sorted) format, BUILD the projected scheme (peel.project).  If the built scheme has fewer terms than the
bar it is written to --candidates as
    <n>x<m>x<p>_r<rank>_from_<source file>_<axis>.json
with the same `note` field as the published files.  One CSV row per (file, axis) is appended to --out
(resumable: (file, axis) pairs already present are skipped unless --force).

With --verify, every written candidate is checked by ../verify-it-yourself/fmmcheck.py (exact, CRT-bounded).

Example (the sweep that found the three LITA-derived schemes; LITA files from fetch_lita.sh):
    python3 sweep.py --bars bars_2026-10-08.csv --out out/peel_lita.csv --candidates out/candidates \\
        lita/13x13x13_r1379.npz lita/15x15x15_r1977.npz lita/14x14x14_r1593.npz lita/16x16x16_r2236.npz
"""
import argparse
import csv
import json
import os
import subprocess
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import peel  # noqa: E402

DEF_BARS = os.path.join(HERE, "bars_2026-10-08.csv")
DEF_CHECKER = os.path.join(HERE, "..", "verify-it-yourself", "fmmcheck.py")


def load_bars(path):
    """CSV with columns format (sorted, e.g. 13x14x14) and bar (smallest listed rank)."""
    bar = {}
    for r in csv.DictReader(open(path)):
        bar[tuple(int(x) for x in r["format"].split("x"))] = int(r["bar"])
    return bar


def ring_of(u, v, w):
    allc = [c for mat in (u, v, w) for row in mat for c in row if c]
    if all(c in (1, -1) for c in allc):
        return "ZT"
    if all(Fraction(c).denominator == 1 for c in allc):
        return "Z"
    return "Q"


def fmt_str(f):
    return "x".join(map(str, f))


def run_checker(checker, path):
    out = subprocess.run([sys.executable, checker, path], capture_output=True, text=True)
    last = (out.stdout.strip().splitlines() or [""])[-1]
    return out.returncode == 0, last


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="scheme files (.npz from LITA or Perminov-style .json)")
    ap.add_argument("--bars", default=DEF_BARS, help="CSV format,bar (default: %(default)s)")
    ap.add_argument("--out", default="peel_sweep.csv", help="CSV of results (appended; resumable)")
    ap.add_argument("--candidates", default="candidates", help="directory for schemes below the bar")
    ap.add_argument("--margin", type=int, default=2, help="build the projection when r-z <= bar+margin")
    ap.add_argument("--axes", default="nmp", help="subset of the axes n, m, p to peel (default: all three)")
    ap.add_argument("--verify", action="store_true", help="run fmmcheck.py on every written candidate")
    ap.add_argument("--checker", default=DEF_CHECKER)
    ap.add_argument("--force", action="store_true", help="overwrite --out instead of resuming")
    args = ap.parse_args()

    bar = load_bars(args.bars)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    os.makedirs(args.candidates, exist_ok=True)
    done = set()
    fields = ["file", "fmt", "ring", "r", "axis", "fmt2_sorted", "bar2", "coord_best_z", "coord_best_idx",
              "gen_best_z", "e", "f", "n_e_rank1", "n_f_rank1", "est_rank", "built", "built_rank", "beats_bar",
              "verified", "seconds"]
    if os.path.exists(args.out) and not args.force:
        for row in csv.DictReader(open(args.out)):
            done.add((row["file"], row["axis"]))
    new = not os.path.exists(args.out) or args.force
    fh = open(args.out, "w" if args.force else "a", newline="")
    wr = csv.DictWriter(fh, fieldnames=fields)
    if new:
        wr.writeheader()
        fh.flush()

    axes = [ax for ax in range(3) if "nmp"[ax] in args.axes]
    for path in args.files:
        base = os.path.basename(path)
        if all((base, "nmp"[ax]) in done for ax in axes) and not args.force:
            continue
        t0 = time.time()
        fmt, u, v, w, meta = peel.load_scheme(path)
        if meta.get("z2"):
            print(f"[skip] {base}: GF(2) scheme (only rational schemes are handled here)", flush=True)
            continue
        r = len(u)
        F = peel.Field(None)
        ring = ring_of(u, v, w)
        for axis in axes:
            if (base, "nmp"[axis]) in done and not args.force:
                continue
            if fmt[axis] <= 2:
                continue  # projecting to a dimension-1 format is pointless
            ta = time.time()
            cen = peel.peel_census(fmt, u, v, w, F, axis)
            fmt2 = list(fmt); fmt2[axis] -= 1
            fmt2s = tuple(sorted(fmt2))
            bar2 = bar.get(fmt2s)
            coord_best_idx = max(cen["coord"], key=lambda l: cen["coord"][l])
            coord_best_z = cen["coord"][coord_best_idx]
            z = cen["best_z"]
            est = r - z
            row = dict(file=base, fmt=fmt_str(fmt), ring=ring, r=r, axis="nmp"[axis], fmt2_sorted=fmt_str(fmt2s),
                       bar2=bar2, coord_best_z=coord_best_z, coord_best_idx=coord_best_idx, gen_best_z=z, e="", f="",
                       n_e_rank1=cen["n_e_rank1"], n_f_rank1=cen["n_f_rank1"], est_rank=est, built=False,
                       built_rank="", beats_bar=False, verified="", seconds=0)
            if cen["best_e"] is not None:
                row["e"] = " ".join(str(x) for x in cen["best_e"])
                row["f"] = " ".join(str(x) for x in cen["best_f"])
            if bar2 is not None and est <= bar2 + args.margin and z > 0:
                fmt2b, u2, v2, w2 = peel.project(fmt, u, v, w, F, axis, cen["best_e"], cen["best_f"])
                rk = len(u2)
                row.update(built=True, built_rank=rk)
                if rk < bar2:
                    row["beats_bar"] = True
                    out = os.path.join(args.candidates, f"{fmt_str(fmt2b)}_r{rk}_from_{base}_{'nmp'[axis]}.json")
                    note = peel.note_for(base, "nmp"[axis], cen["best_e"], cen["best_f"])
                    json.dump(peel.to_json(fmt2b, u2, v2, w2, F, note=note), open(out, "w"))
                    print(f"[CANDIDATE] {out}: {rk} terms < bar {bar2} for {fmt_str(fmt2s)} (ring {ring})", flush=True)
                    if args.verify:
                        ok, last = run_checker(args.checker, out)
                        row["verified"] = ok
                        print(f"  {last}", flush=True)
                else:
                    print(f"  near miss {base} axis {'nmp'[axis]} -> {fmt_str(fmt2s)} {rk} terms vs bar {bar2}", flush=True)
            row["seconds"] = round(time.time() - ta, 2)
            wr.writerow(row)
            fh.flush()
        print(f"{base}: fmt {fmt_str(fmt)} ring {ring} r={r} {time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
