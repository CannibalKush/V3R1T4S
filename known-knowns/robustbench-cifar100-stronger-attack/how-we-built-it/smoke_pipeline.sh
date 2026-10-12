#!/bin/sh
# smoke_pipeline.sh -- runs every stage of the pipeline on the first N_IMAGES test images (default 100) on the CPU with
# tiny budgets (a few attack steps per stage), to check that the code runs end to end.  It does NOT reproduce the
# published numbers (those used the full budgets in README.md on 10,000 images).
#   sh smoke_pipeline.sh OUT_DIR          (env: PYTHON, DATA_DIR, MODEL_DIR, THREADS, N_IMAGES, DEVICE,
#                                           CR_SRC = local copy of upstream cr_attack.py, else it is downloaded once)
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=${1:?usage: sh smoke_pipeline.sh OUT_DIR}
PYTHON=${PYTHON:-python3}
DATA_DIR=${DATA_DIR:-./data}
MODEL_DIR=${MODEL_DIR:-./models}
THREADS=${THREADS:-2}
N=${N_IMAGES:-100}
DEV=${DEVICE:-cpu}
M=Addepalli2022Efficient_RN18
C="--data_dir $DATA_DIR --model_dir $MODEL_DIR --n_test $N"
export OMP_NUM_THREADS="$THREADS" MKL_NUM_THREADS="$THREADS" PYTHONDONTWRITEBYTECODE=1
mkdir -p "$OUT"
say() { echo "== $(date -u +%H:%M:%SZ) $*"; }

say "stage 1: APGD-CE (10 steps instead of 100)"
"$PYTHON" "$HERE/stage1_apgdce.py" --model $M $C --steps 10 --batch 100 --device "$DEV" --threads "$THREADS" \
  --ckpt "$OUT/s1/ckpt" --out "$OUT/s1/out"
"$PYTHON" "$HERE/order_survivors.py" --stage1 "$OUT/s1/out" --out "$OUT/s1/order.npy"

say "stage 2: successive halving over targeted APGD arms (12 arms, rounds 2/2/4 instead of 45 arms, 10/20/90)"
"$PYTHON" "$HERE/stage2_sh.py" --model $M $C --stage1 "$OUT/s1/out" --indices "$OUT/s1/order.npy" --mode sh \
  --K 6 --L1 3 --losses_top dlr-t,cw-t,pm-t --losses_wide cw-t --r 2,2,4 --keep 3,1 --super 64 --sub 500 --seed 2 \
  --device "$DEV" --threads "$THREADS" --ckpt "$OUT/s2/ckpt" --out "$OUT/s2/out" --tag full_sh
"$PYTHON" "$HERE/mask_from_margin.py" "$OUT/s2/out/full_sh_cpu_margin.npy" "$OUT/s2/out/mask.npy"

say "stage 3: CR Attack on the residual (1 target, 1 restart, 30 iterations instead of 3, 5, 150)"
if [ -n "${CR_SRC:-}" ]; then "$PYTHON" "$HERE/make_cr_attack.py" --src "$CR_SRC" --out "$OUT/cr_attack_vendored.py"
else "$PYTHON" "$HERE/make_cr_attack.py" --out "$OUT/cr_attack_vendored.py"; fi
CR_ATTACK_DIR="$OUT" "$PYTHON" "$HERE/cr_residual.py" --model $M $C --x_adv_in "$OUT/s2/out/x_adv_full_sh.npy" \
  --margin_in "$OUT/s2/out/full_sh_cpu_margin.npy" --mask_in "$OUT/s2/out/mask.npy" --ckpt "$OUT/s3" \
  --max_dist 0.5 --batch 50 --targets 1 --restart 1 --max_iter 30 --decay_steps 30 --seed 0 --device "$DEV" --threads "$THREADS"
"$PYTHON" "$HERE/mask_from_margin.py" "$OUT/s3/m_cpu.npy" "$OUT/s3/mask.npy"

say "stage 4: warm relax/reset (crwarm, 30 iterations instead of 150)"
"$PYTHON" "$HERE/warm_residual.py" --model $M $C --x_adv_in "$OUT/s3/x_adv.npy" --margin_in "$OUT/s3/m_cpu.npy" \
  --mask_in "$OUT/s3/mask.npy" --ckpt "$OUT/s4" --arms crwarm --params '{"crwarm": {"max_iter": 30}}' --max_dist 0.5 \
  --batch 50 --seed 0 --device "$DEV" --threads "$THREADS"

say "stage 5: safety polish + float64 feasibility"
"$PYTHON" "$HERE/assemble_final.py" --model $M $C --ckpt "$OUT/s4" --out "$OUT/s5/x_adv.npy" --device "$DEV" --threads "$THREADS"

say "stage 6: multi-start APGD portfolio on the 3 closest residuals (5 restarts x 10 steps) + merge"
"$PYTHON" "$HERE/multistart.py" --model $M $C --x_ref "$OUT/s5/x_adv.npy" --m_ref "$OUT/s5/x_adv_row_cpu_margin.npy" \
  --n_images 3 --restarts 5 --arms cwv,dlr,dlrt1,cwt1,cw --n_iter 10 --batch 20 --seed 0 --device "$DEV" \
  --threads "$THREADS" --out "$OUT/s6/ms"
"$PYTHON" "$HERE/assemble.py" --model $M $C --base "$OUT/s5/x_adv.npy" --base_margin "$OUT/s5/x_adv_row_cpu_margin.npy" \
  --cands "$OUT/s6/ms" --out "$OUT/s6/x_adv.npy" --threads "$THREADS"
say "done"
