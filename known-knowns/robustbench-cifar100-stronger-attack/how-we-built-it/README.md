# How the tensor was built

This folder holds the code that produced `../adversarial-examples/x_adv_Addepalli2022Efficient_RN18.npz` (its single
member `x_adv.npy` has sha256 `4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb`). The tensor was not
made by one script but by a chain of six stages, each one starting from the tensor of the previous stage and attacking
only the images that were still robust ("the residual"), closest to the decision boundary first. Every stage is here,
cleaned (paths made configurable, internal labels removed); the attack code, constants and seeds are unchanged.

Lineage, confirmed by the sha256 of every intermediate tensor in the original run folders (implied robust count =
clean-correct images whose CPU margin best_wrong − true is ≤ 0):

| stage | script | what it does | output sha256 | robust |
|---|---|---|---|---|
| 1 | `stage1_apgdce.py` | APGD-CE, 100 steps, 1 random start, on all 6,545 clean-correct images | `53ec4fb0…4d6c` | 3,352 |
| 2 | `order_survivors.py`, `stage2_sh.py` | successive halving over 45 targeted/untargeted APGD arms per image (rounds 10/20/90 steps, keep 9 then 3) | `18939f4b…2e77` | 2,763 |
| 3 | `make_cr_attack.py`, `cr_residual.py` | CR Attack (published configuration) on the 771 residuals within 0.5 logits | `039b7bd8…1516` | 2,760 |
| 4 | `warm_residual.py` (3 runs) | warm relax/reset arms started at the incumbent points | `f7897547…a9be`, `f8f15b0a…3441`, `222d4a2a…949f` | 2,759, 2,758, 2,758 |
| 5 | `assemble_final.py` | safety polish of fooled rows with margin < 1e-3, float64 feasibility | `193c035e…7d8d` | 2,758 |
| 6 | `multistart.py` (3 runs), `assemble.py` | fresh multi-start APGD portfolio on the near-tie rows; merge | `4eea7cd6…decb` (published) | **2,757** |

Images broken after stage 2: 4129, 5091, 9718 (stage 3), 6582, 8075 (stage 4), 2137 (stage 6). Stage 6 also replaced
four already-fooled rows (557, 5091, 8141, 9693) by points with a larger margin ("insurance"); nothing else changed.

## Setup

```sh
pip install -r requirements.txt     # Python 3.11; torch 2.14.1, torchvision 0.29.1, numpy 2.4.6,
                                    # robustbench @ 78fcc9e4, autoattack @ a3922004 (exact environment of the run)
python make_cr_attack.py            # stage 3 only: fetches CR Attack's cr_attack.py (one GET) and adapts it, see below
```
Inputs (not redistributed here): the CIFAR-100 test set, https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz
(169,001,437 bytes, sha256 `85cd44d02ba6437773c5bbd22e183051d648de2e7d6b014e1ef29b855ba677a7`, md5 = torchvision's
`eb9058c3…8d85`; uint8 test images sha256 `4cb8e5d9…ee19`), fetched by torchvision into `--data_dir` on first use; and the
model weights `Addepalli2022Efficient_RN18.pt` (44,963,257 bytes, sha256 `aafda6c1…8587`), fetched by RobustBench's own
downloader into `--model_dir` on first use. Every script takes `--data_dir`, `--model_dir` (defaults `./data`,
`./models`) and `--n_test N` (use only the first N test images; for smoke tests).

**CR Attack** (Pan, Wu, Tang, Li, Yao, AAAI 2025, github.com/fzjcdt/constraint-relaxation-attack) is third-party code
in a repository without a licence file, so it is not included. `make_cr_attack.py` downloads
`attacks/attacks/cr_attack.py` (the 2026-10-10 version, sha256 `91320622…6254`), applies our adaptation as line edits
(standalone class instead of the torchattacks-style base class, MPS-safe indexing and seeding, the 0.05 potential
threshold as a parameter with the published default) and checks that the result is byte-identical to the file we ran
(`df5357e0…176f`). It writes `cr_attack_vendored.py` next to itself (or set `CR_ATTACK_DIR`).

## The commands of the original run

All stages ran on one Apple M5 (10 cores, 32 GB, macOS 27) with the attack loops on the Apple MPS GPU and every
success re-verified on the CPU in float32 (4 threads), on a machine shared with other jobs (load often 70-400). Seeds
are given; MPS kernels and random streams are not bit-reproducible across machines or torch builds, so a re-run of
stages 1-6 gives a tensor of the same kind (robust count near 2,757), not the same bytes. Stage 6's merge step is
exactly reproducible on CPU (below). `S1` … `S6` stand for any output directories; flags not shown are the defaults.

```sh
M=Addepalli2022Efficient_RN18; COMMON="--data_dir DATA --model_dir MODELS"
# stage 1 (2026-10-09, 2,031 s; 3,352 robust)
python stage1_apgdce.py --model $M $COMMON --ckpt S1/ckpt --out S1/out            # steps 100, batch 500, seed 0, mps
python order_survivors.py --stage1 S1/out --out S1/order.npy                      # the 3,352 survivors, closest first
# stage 2 (2026-10-09, 21,577 s; 589 more fooled -> 2,763)
python stage2_sh.py --model $M $COMMON --stage1 S1/out --indices S1/order.npy --mode sh --K 27 --L1 9 \
  --losses_top dlr-t,cw-t,pm-t --losses_wide cw-t --r 10,20,90 --keep 9,3 --super 64 --sub 500 --seed 2 \
  --ckpt S2/ckpt --out S2/out --tag full_sh
python mask_from_margin.py S2/out/full_sh_cpu_margin.npy S2/mask.npy
# stage 3 (2026-10-11, 6,095 s; 3 breaks -> 2,760)
python cr_residual.py --model $M $COMMON --x_adv_in S2/out/x_adv_full_sh.npy --margin_in S2/out/full_sh_cpu_margin.npy \
  --mask_in S2/mask.npy --ckpt S3 --max_dist 0.5 --batch 100 --seed 0  # targets 3, restart 5, max_iter 150, decay 30
python mask_from_margin.py S3/m_cpu.npy S3/mask.npy
# stage 4 (2026-10-11): 4a 117 s (1 break), 4b 435 s (1 break), 4c 1,075 s (0 breaks, 36 robust rows moved closer)
python warm_residual.py --model $M $COMMON --x_adv_in S3/x_adv.npy --margin_in S3/m_cpu.npy --mask_in S3/mask.npy \
  --ckpt S4a --arms crwarm --max_dist 0.05 --limit 8 --batch 8 --seed 0
python mask_from_margin.py S4a/m_cpu.npy S4a/mask.npy
python warm_residual.py --model $M $COMMON --x_adv_in S4a/x_adv.npy --margin_in S4a/m_cpu.npy --mask_in S4a/mask.npy \
  --ckpt S4b --arms crwarm --max_dist 0.1 --batch 100 --seed 0
python mask_from_margin.py S4b/m_cpu.npy S4b/mask.npy
python warm_residual.py --model $M $COMMON --x_adv_in S4b/x_adv.npy --margin_in S4b/m_cpu.npy --mask_in S4b/mask.npy \
  --ckpt S4c --arms crwarm_t,tempering,crhop --max_dist 0.03 --batch 50 --seed 2
# stage 5 (240 s)
python assemble_final.py --model $M $COMMON --ckpt S4c --out S5/x_adv.npy
# stage 6 (multi-start runs 172 s, 314 s, 366 s; merges 268 s and 121 s)
python multistart.py --model $M $COMMON --x_ref S5/x_adv.npy --m_ref S5/x_adv_row_cpu_margin.npy \
  --idx 557,4129,9693,5091,8141 --restarts 32 --n_iter 100 --batch 160 --seed 11 --out S6/run_a_seed11
python multistart.py --model $M $COMMON --x_ref S5/x_adv.npy --m_ref S5/x_adv_row_cpu_margin.npy \
  --idx 2137,1972 --restarts 250 --arms cwv,dlr,dlrt1,cwt1,cw --n_iter 100 --batch 250 --seed 1 --out S6/run_b_seed1
python assemble.py --model $M $COMMON --base S5/x_adv.npy --base_margin S5/x_adv_row_cpu_margin.npy \
  --cands S6/run_a_seed11,S6/run_b_seed1 --out S6/x_adv_v1.npy          # first 2,757 tensor, sha256 a72dfaf0…8242
python multistart.py --model $M $COMMON --x_ref S6/x_adv_v1.npy --m_ref S5/x_adv_row_cpu_margin.npy \
  --idx 2137,4129,9693,5091 --restarts 100 --arms cwv,dlr,dlrt1,cwt1,cw --n_iter 100 --batch 200 --seed 3 --out S6/run_c_seed3
python assemble.py --model $M $COMMON --base S5/x_adv.npy --base_margin S5/x_adv_row_cpu_margin.npy \
  --cands S6/run_c_seed3,S6/run_b_seed1,S6/run_a_seed11 --out S6/x_adv.npy   # the published tensor
```
With `--idx`, `--m_ref` is only logged; `--x_ref` matters (the targeted arms aim at the incumbent row's top wrong
classes), which is why run_c used the first 2,757 tensor. Total attack wall time about 9 hours of the shared GPU.

Notes on fidelity: (1) stage 2 ranks target classes by clean logits; the original run read them from an MPS forward
of the clean test set saved by a setup script that is not preserved (file sha256 `1e0a9465…3d01`); `stage2_sh.py`
recomputes them on `--device` unless `--clean_logits` is given. (2) In the original run, stages 4a and 4b and the first
multi-start run (run_a) used slightly earlier copies of `warm_residual.py` and `multistart.py`; the later edits added
checkpointing after every arm and extra output files (`x_end.npy`, `rows_img.npy`), not attack changes, as far as the
logs show. (3) The masks fed to stages 3 and 4 came from a checker or from `m <= 0`; all six were checked to equal
`mask_from_margin.py`'s output. (4) Exploratory stage-6 runs that contributed no row (64 restarts on the 10 closest
residuals, 30 restarts on the next 33, an exhaustive coordinate search on 5 images) were candidates in the original
merge commands (the exact list of the first merge was not recorded); leaving them out gives the same bytes for both
merges (checked), so their code is not included. Stage 3 also ran a
second CR draw (seed 7, 22 closest residuals) later, which found nothing and is not part of the lineage.

## Exact regeneration of the last step

`stage6-inputs/` holds the small original arrays needed to redo the final merge bit for bit: the five stage-5 rows
that stage 6 replaced (`base_rows*.npy`), the stage-5 row margins, and the `idx.npy` / `best_x.npy` / `best_cpu_margin.npy`
of the three multi-start runs (276 KB in all). With `--cands run_a_seed11,run_b_seed1` the same base also
regenerates the first 2,757 tensor (`a72dfaf0…8242`) that run_c used as `--x_ref`.

```sh
DATA_DIR=DATA MODEL_DIR=MODELS sh regenerate_final_step.sh OUT_DIR   # under a minute on 2 CPU threads
```
`rebuild_base.py` rebuilds the stage-5 tensor from the published one (expected sha256 `193c035e…7d8d`), then
`assemble.py` re-verifies every candidate row on the CPU and writes the final tensor. Expected last line:
`... sha256 4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb: BIT-IDENTICAL to the published tensor`.
See `SMOKE.md` for our run of this and of `smoke_pipeline.sh` (every stage on 100 images with tiny budgets).

## Credits and licences

APGD / AutoAttack: F. Croce and M. Hein (ICML 2020); `apgd_lib.py` and the `apgd_rows` function of `multistart.py`
re-implement APGD following fra31/auto-attack (MIT licence, Copyright (c) 2020 Francesco Croce) at commit a3922004.
CR Attack: Pan, Wu, Tang, Li, Yao (AAAI 2025); its code is fetched, not included, and the `crwarm`/`crhop` arms of
`warm_residual.py` are our own implementation of its relax/reset schedule. RobustBench (MIT) is used unmodified as a
library. The model weights are the authors' (Addepalli, Jain, Venkatesh Babu, NeurIPS 2022) via RobustBench.
