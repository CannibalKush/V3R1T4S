# Smoke runs of the cleaned code (2026-10-12)

Run from this folder of the repository (not from the original run folders), on the build machine: Apple M5, macOS 27,
Python 3.11.15 with the packages of `requirements.txt` (torch 2.14.1, numpy 2.4.6, robustbench @ 78fcc9e4), CPU only,
2 threads (`OMP_NUM_THREADS=2`, `nice -n 10`), machine shared with other jobs (load average 20-60). The CIFAR-100 test
set and the model weights were already on disk (sha256 checked by the scripts, nothing downloaded); the upstream CR
Attack file was given as a local copy of the 2026-10-10 download (`CR_SRC`), so `make_cr_attack.py` ran offline.
Outputs went to a scratch directory outside the repository (`OUT` below).

## 1. Exact regeneration of the last step (matches: yes)

```sh
PYTHON=python3 DATA_DIR=DATA MODEL_DIR=MODELS THREADS=2 sh regenerate_final_step.sh OUT
```
11 s wall. Output (paths shortened):
```
wrote OUT/stage5_x_adv.npy sha256 193c035e004b4932e9e4aa6127877883bd2dbc1580b00333b03f92f3523a7d8d (== stage-5 tensor)
idx 557: base +0.00023 -> best cand +0.00162 [INSURANCE] from run_a_seed11
idx 1972: base -0.00276 -> best cand -0.00186 [None] from run_b_seed1
idx 2137: base -0.00121 -> best cand +0.00037 [NEW_BREAK] from run_c_seed3
idx 4129: base +0.00014 -> best cand +0.00014 [None] from None
idx 5091: base +0.00066 -> best cand +0.00125 [INSURANCE] from run_c_seed3
idx 8141: base +0.00085 -> best cand +0.00105 [INSURANCE] from run_a_seed11
idx 9693: base +0.00015 -> best cand +0.00042 [INSURANCE] from run_c_seed3
OUT/x_adv.npy sha256 4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb: BIT-IDENTICAL to the published tensor
```
Also checked: (a) `assemble.py` with `--cands run_a_seed11,run_b_seed1` on the same base gives the first 2,757
tensor of the original run bit for bit (sha256 `a72dfaf09b14b6f3a3c106cbededa367961984e64b75f38f6cb72120378c8242`),
the `--x_ref` of the third multi-start run; (b) before the small inputs were extracted, the cleaned `assemble.py` was
run on the original stage-5 tensor with the original six-candidate list (including the three exploratory runs) and
with only the three contributing runs: both gave `4eea7cd6…decb` (about 50 s each).

## 2. Every stage on 100 images with tiny budgets (runs: yes; not meant to reproduce the published numbers)

```sh
PYTHON=python3 DATA_DIR=DATA MODEL_DIR=MODELS THREADS=2 N_IMAGES=100 CR_SRC=cr_attack.py sh smoke_pipeline.sh OUT
```
243 s wall, exit 0. Budgets: stage 1 10 APGD steps; stage 2 12 arms, rounds 2/2/4; stage 3 CR with 1 target, 1
restart, 30 iterations; stage 4 crwarm 30 iterations; stage 6 5 restarts × 10 steps on the 3 closest residuals.
Trimmed output:
```
[clean gate] subset of 100 images: 70/100 correct (gate applies to the full test set only)
[stage1] CPU verify 2s: robust 39/100 = 39.00%  (clean 70)  ...  max Linf 0.031372549 eps_viol 0 range_viol 0
[full_sh] arms/image 12  rounds [2, 2, 4]  keep [3, 1]  max budget/image 34 steps  horizon 8
[full_sh] CPU verify (2s) on 39 images: fooled 4  (weak <1e-3: 0)  residual 35
wrote OUT/cr_attack_vendored.py (sha256 df5357e045d86c5c3d0736ca5ad56ceae29ba382367f22bb4bcf3ec2481f176f, identical to the file used in the original run)
  unit 1/1 n=11 margins [-0.488,-0.065] dev-fooled 0 cpu-fooled exact 0 (safe 0, polished 0) fwd/img 54.0 bwd/img 40.0 23s  TOTAL new breaks 0
  unit 1/1 arm crwarm: n=11 dev-fooled 0 cpu-fooled 0 (safe 0, polished 0) improved-committed 11 dev gain mean +0.0213 max +0.1016 19s
 "implied_robust_row_margins": 35, "n_nudged_ulp": 2855, "max_linf_float64": 0.03137254901960784, "n_over_eps_strict": 0
IMG 17: inc -0.04474 | restarts max -0.05027 ... | best CPU -0.05027 linf 0.0313725490 | arms max: cwv:-0.0503 dlr:-0.0877 ...
DONE: CPU-fooled 0/3 []; wall 9s
 "out_sha256": "fdf5f1449a85a43c0e02987aa2b52eca82f268c70aba71e086883eedb76c6720", "implied_robust": 35
```
So on the first 100 images: 70 clean-correct, 39 left after 10 APGD-CE steps, 35 after the small successive-halving
stage; the tiny CR/warm/multi-start budgets broke nothing more (they only moved 11 robust rows closer to the boundary),
and every tensor kept max |x_adv − x| = 8/255 exactly. On CPU the pipeline is deterministic: a second run gave the
same tensors (stage 1 `fe0f635f…`, stage 2 `9e19f704…`, stage 5 `fdf5f144…`).

A first attempt of this smoke run used 4 restarts for 5 arms in stage 6 and crashed in the summary statistics (an arm
with no restart); `multistart.py` now rejects `--restarts` smaller than the number of arms up front (the original runs
all used more restarts than arms) and the smoke script uses 5.

Stage 2's target ranking: the clean logits recomputed on CPU differ from the original MPS file by at most 9.7e-6 on
these 100 images, and the top-27 wrong-class ranking is identical on all 100.
