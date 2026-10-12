#!/bin/sh
# Rebuild both published witness files from the saved CP-SAT solutions (checkpoints/) and compare their sha256 with
# the files in ../witnesses/. Deterministic: no solver involved, only bnn.pixel_map + onnxruntime replay.
# Needs the benchmark files at the pinned commit, e.g. from the family directory:
#   python3 verify-it-yourself/vnncheck.py --cache downloads
# Usage (from the family directory): sh how-we-built-it/regenerate_from_checkpoints.sh [DOWNLOADS_DIR] [OUT_DIR]
# Set PYTHON= to choose the interpreter. Exit 0 iff all four files are byte-identical to the published ones.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
FAM=$(cd "$HERE/.." && pwd)
DL=${1:-downloads}
OUT=${2:-regenerated}
PY=${PYTHON:-python3}
B="$DL/benchmarks/traffic_signs_recognition_2023/2.0"
ONNX="$B/onnx/3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.onnx.gz"
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
fail=0
# idx_1703: searched with pw = 10 (m = 1 - 2^-10); idx_178: pw = 9 (stored in the checkpoint)
$PY -I "$HERE/make_witness.py" --ckpt "$HERE/checkpoints/ckpt_idx_1703_cls22.json" --pw 10 \
    --vnnlib "$B/vnnlib/model_30_idx_1703_eps_1.00000.vnnlib.gz" --onnx "$ONNX" --out "$OUT/model_30_idx_1703_eps_1" || fail=1
$PY -I "$HERE/make_witness.py" --ckpt "$HERE/checkpoints/ckpt_idx_178_cls15.json" \
    --vnnlib "$B/vnnlib/model_30_idx_178_eps_1.00000.vnnlib.gz" --onnx "$ONNX" --out "$OUT/model_30_idx_178_eps_1" || fail=1
for i in 1703 178; do
  for f in witness_plain.txt witness_v2.txt; do
    new=$($SHA "$OUT/model_30_idx_${i}_eps_1/$f" | cut -d' ' -f1)
    pub=$($SHA "$FAM/witnesses/model_30_idx_${i}_eps_1/$f" | cut -d' ' -f1)
    if [ "$new" = "$pub" ]; then echo "idx_$i $f: identical to published ($new)"; else echo "idx_$i $f: DIFFERS ($new vs $pub)"; fail=1; fi
  done
done
[ $fail = 0 ] && echo "REGENERATED: all four witness files byte-identical" || echo "REGENERATION MISMATCH"
exit $fail
