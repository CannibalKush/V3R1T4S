#!/bin/sh
# (13,6) parameter search, end to end, with the parameters and seeds that produced G_13_6_n535495.
#   1. cutsets.py       : strict cut sets of H(9), 1M iterations, seed 77, warm-started from inputs/H9_points_r2.json
#                         (3924) and inputs/H9_lines_r1.json (3940); original results 3928 points / 3949 lines
#   2. relax_greedy.py  : add 'mild' extra cut elements (127 points, 118 lines in the original run), default_rng(7)
#   3. relaxed13.py     : Rajiv's compound cut at the relaxed sets + t = 4055 new vertices + random 5-regular Y (seed 1)
#   4. xchk (C)         : all-pairs check; XCHK_DUMP lists the far pairs (3179 in the original run, all new-new)
#   5. exact_sc.py      : one shortcut per far pair that is not already fixed (2643 in the original run)
#   6. xchk             : final all-pairs check (expect VALID)
#
# Environment (all optional):
#   PYTHON     python interpreter (default python3)
#   CC         C compiler (default cc)
#   RAJIV_DIR  directory with Rajiv's unzipped Zenodo data (default ./rajiv): needs
#              graph_d13_k6_n534234.edges.xz and witnesses/cs_d13_k6_n534234.json
#   OUT        output directory (default ./out_13_6)
#   THREADS    threads for xchk / exact_sc (default 6, as in the original run)
#   FROM_X1=1           skip step 1 and start from the shipped strict sets inputs/H9_points_x1.json, H9_lines_x1.json
#   USE_SHIPPED_PAIRS=1 give exact_sc the far-pair list of the original run (inputs/far_pairs_t4055.txt) instead of
#                       the fresh XCHK_DUMP list. The dump's line order depends on thread scheduling and exact_sc
#                       processes the pairs in a seeded shuffle of that order, so only the shipped list reproduces
#                       the original 2643 shortcuts exactly.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PYTHON:-python3}
CC=${CC:-cc}
Z=${RAJIV_DIR:-rajiv}
OUT=${OUT:-out_13_6}
TH=${THREADS:-6}
R="$Z/graph_d13_k6_n534234.edges.xz"
W="$Z/witnesses/cs_d13_k6_n534234.json"
mkdir -p "$OUT"

if [ "${FROM_X1:-0}" = "1" ]; then
  SPX="$HERE/inputs/H9_points_x1.json"
  SLX="$HERE/inputs/H9_lines_x1.json"
else
  SPX="$OUT/H9_points_x1.json"
  SLX="$OUT/H9_lines_x1.json"
  # --stall was not recorded for the original run; the script default (200000) is used here.
  "$PY" "$HERE/cutsets.py" --rajiv "$R" --witness "$W" --side points --iters 1000000 --seed 77 \
      --init "$HERE/inputs/H9_points_r2.json" --out "$SPX" --cache "$OUT/H9_block0.npz"
  "$PY" "$HERE/cutsets.py" --rajiv "$R" --witness "$W" --side lines --iters 1000000 --seed 77 \
      --init "$HERE/inputs/H9_lines_r1.json" --out "$SLX" --cache "$OUT/H9_block0.npz"
fi

"$PY" "$HERE/relax_greedy.py" points "$SPX" "$OUT/SP_relaxed_v1.json" 12 --rajiv "$R"
"$PY" "$HERE/relax_greedy.py" lines "$SLX" "$OUT/SL_relaxed_v1.json" 12 --rajiv "$R"

G="$OUT/G13_relax_t4055_s1"
"$PY" "$HERE/relaxed13.py" --rajiv "$R" --witness "$W" --sp "$OUT/SP_relaxed_v1.json" --sl "$OUT/SL_relaxed_v1.json" \
    --kp 0 --kl 0 --seed 1 --t 4055 --out "$G.edges"

"$CC" -O3 -march=native -o "$OUT/xchk" "$HERE/xchk.c" -lpthread
XCHK_DUMP="$G.bad.txt" "$OUT/xchk" "$G.edges" 13 6 "$TH" || true     # INVALID expected here: it lists the far pairs
PAIRS="$G.bad.txt"
[ "${USE_SHIPPED_PAIRS:-0}" = "1" ] && PAIRS="$HERE/inputs/far_pairs_t4055.txt"

"$PY" "$HERE/exact_sc.py" "$G.edges" 13 531440 "$G.esc.edges" --threads "$TH" --quiet --rebuild-every 100 \
    --pairs "$PAIRS"

XCHK_DUMP="$G.esc.bad.txt" "$OUT/xchk" "$G.esc.edges" 13 6 "$TH"
shasum -a 256 "$G.esc.edges" 2>/dev/null || sha256sum "$G.esc.edges"
