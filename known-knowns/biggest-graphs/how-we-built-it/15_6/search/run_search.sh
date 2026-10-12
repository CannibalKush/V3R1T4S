#!/bin/sh
# (15,6) parameter search, end to end, with the parameters and seeds that produced G_15_6_n1424896.
#   1. cutsets.py      : larger Lemma-5 cut sets of H(11) (points 7679, lines 7648 in the original run)
#   2. ../compound.py  : Rajiv's compound cut at those sets + t = 7648 new vertices + random 7-regular Y (seed 1)
#   3. assign_generic.py: exact far new-new pairs (9 in the original run) + one shortcut edge per pair (seed 1)
#
# Environment (all optional):
#   PYTHON     python interpreter (default python3)
#   RAJIV_DIR  directory with Rajiv's unzipped Zenodo data (default ./rajiv): needs
#              graph_d15_k6_n1424472.edges.xz and witnesses/cs_d15_k6_n1424472.json
#   OUT        output directory (default ./out_15_6)
#   USE_SHIPPED_CUTSETS=1  skip step 1 and use the cut sets shipped in ../ (H11_points_s5.json, H11_lines_s1.json)
#
# Runtime of the original run (Apple-silicon laptop, heavily shared machine): step 1 points 586 s, lines 2048 s
# (single-threaded numba); step 2 about 4.5 min; step 3 about 6 min (numba, multi-threaded).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PYTHON:-python3}
Z=${RAJIV_DIR:-rajiv}
OUT=${OUT:-out_15_6}
R="$Z/graph_d15_k6_n1424472.edges.xz"
W="$Z/witnesses/cs_d15_k6_n1424472.json"
mkdir -p "$OUT"

if [ "${USE_SHIPPED_CUTSETS:-0}" = "1" ]; then
  SP="$HERE/../H11_points_s5.json"
  SL="$HERE/../H11_lines_s1.json"
else
  SP="$OUT/H11_points_s5.json"
  SL="$OUT/H11_lines_s1.json"
  "$PY" "$HERE/cutsets.py" --rajiv "$R" --witness "$W" --side points --iters 100000 --rounds 1 --stall 40000 \
      --seed 5 --out "$SP" --cache "$OUT/H11_block0.npz"
  "$PY" "$HERE/cutsets.py" --rajiv "$R" --witness "$W" --side lines --iters 300000 --rounds 1 --stall 60000 \
      --seed 1 --out "$SL" --cache "$OUT/H11_block0.npz"
fi

"$PY" "$HERE/../compound.py" --rajiv "$R" --witness "$W" --sp "$SP" --sl "$SL" --t 7648 --seed 1 \
    --out "$OUT/G_15_6_base.edges"

"$PY" "$HERE/assign_generic.py" --graph "$OUT/G_15_6_base.edges" --delta 15 --off 1417248 --t 7648 --D 6 \
    --out "$OUT/G_15_6_n1424896.edges" --seed 1 --iters 3000000 --hours 0.5 --write_partial

shasum -a 256 "$OUT/G_15_6_n1424896.edges" 2>/dev/null || sha256sum "$OUT/G_15_6_n1424896.edges"
