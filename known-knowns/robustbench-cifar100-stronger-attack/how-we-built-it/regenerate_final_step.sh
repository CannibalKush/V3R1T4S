#!/bin/sh
# regenerate_final_step.sh -- re-runs the last step of the pipeline (stage 6 merge, assemble.py) from the stage-5 tensor
# and the three multi-start results that contributed rows, and checks that the output is bit-identical to the published
# tensor (.npy sha256 4eea7cd6...decb).  CPU only, under a minute; needs the CIFAR-100 test set and the model weights
# (fetched on first use into DATA_DIR / MODEL_DIR).
#   sh regenerate_final_step.sh [OUT_DIR]        (env: PYTHON, DATA_DIR, MODEL_DIR, THREADS)
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=${1:-./regenerated}
PYTHON=${PYTHON:-python3}
DATA_DIR=${DATA_DIR:-./data}
MODEL_DIR=${MODEL_DIR:-./models}
THREADS=${THREADS:-2}
I="$HERE/stage6-inputs"
mkdir -p "$OUT"
export OMP_NUM_THREADS="$THREADS" MKL_NUM_THREADS="$THREADS" PYTHONDONTWRITEBYTECODE=1
"$PYTHON" "$HERE/rebuild_base.py" --out "$OUT/stage5_x_adv.npy"
"$PYTHON" "$HERE/assemble.py" --base "$OUT/stage5_x_adv.npy" --base_margin "$I/base_row_cpu_margin.npy" \
  --cands "$I/run_c_seed3,$I/run_b_seed1,$I/run_a_seed11" --out "$OUT/x_adv.npy" --threads "$THREADS" \
  --data_dir "$DATA_DIR" --model_dir "$MODEL_DIR" > "$OUT/assemble.log" 2>&1
grep '^idx' "$OUT/assemble.log"
"$PYTHON" - "$OUT/x_adv.npy" <<'EOF'
import hashlib, sys
h = hashlib.sha256(open(sys.argv[1], 'rb').read()).hexdigest()
ok = h == '4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb'
print(f'{sys.argv[1]} sha256 {h}: {"BIT-IDENTICAL to the published tensor" if ok else "DIFFERENT from the published tensor"}')
sys.exit(0 if ok else 1)
EOF
