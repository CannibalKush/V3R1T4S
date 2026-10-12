# Reproduce: RobustBench CIFAR-100, Addepalli2022Efficient_RN18

All commands are relative to the `known-knowns/robustbench-cifar100-stronger-attack/` directory. Requirements:
`python3` with `numpy`, `torch`, `torchvision` and RobustBench at the commit we compared against:
```sh
pip install numpy torch torchvision git+https://github.com/RobustBench/robustbench@78fcc9e48a07a861268f295a777b975f25155964
```
On first use the CIFAR-100 test set (about 160 MB, via torchvision) and the model weights (about 45 MB, via
RobustBench's own downloader) go into `./data` and `./models`.

## 1. Integrity and lossless restore

```sh
sha256sum adversarial-examples/*                  # macOS: shasum -a 256; expected values in INDEX.csv
python3 verify-it-yourself/unpack.py x_adv.npy    # optional argument: write the original .npy file
```
Expected: the zip member `x_adv.npy`, the loaded array re-saved with `numpy.save`, and the written file all have sha256
`4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb`; last line `LOSSLESS: yes, bit-identical to the
original tensor`. In your own code: `x_adv = numpy.load('adversarial-examples/x_adv_Addepalli2022Efficient_RN18.npz')['x_adv']`.

## 2. The full check (the claim)

```sh
python3 verify-it-yourself/rbcheck.py --data_dir data --model_dir models
```
Checks the sha256 of the tensor, test images, labels and weights; the threat model on all 10,000 images in float64
(max |x_adv − x| ≤ 8/255 with no tolerance, values in [0, 1]); then runs the unmodified model in eval mode on CPU on
the clean and the adversarial images. Expected:
```
FULL TEST SET: clean 6545/10000 (RobustBench clean_acc 65.45 % = 6545), robust 2757/10000 vs RobustBench AutoAttack 27.67 % = 2767: 10 images below
RBCHECK PASS model=Addepalli2022Efficient_RN18 n=10000 clean=6545 robust=2757 ...
```
Runtime: 2 × 10,000 ResNet-18 forward passes; about 50 s per 500 images on 4 CPU threads of a busy machine, so
roughly 10–20 minutes. `--n 500` checks the first 500 images only (expected: clean 321, robust 146, and the robust set
equal to `robust_indices.txt` on those images). `sh verify-it-yourself/run_checks.sh` runs sections 1 and 2
(`N=500` for the quick version; `PYTHON`, `DATA_DIR`, `MODEL_DIR` to choose interpreter and directories).

The count is per image, so a GPU or another library version can be compared image by image with
`adversarial-examples/robust_indices.txt`. Three fooled images are near-ties (indices 4129, 2137, 9693; CPU logit
margins +1.4e-4 to +4.2e-4); if your hardware disagrees, it will be on those rows first.

## 3. Compare with today's table

One GET, with a User-Agent that says who you are:
```sh
curl -sS -A "your-name-or-project (single GET)" \
  https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar100/Linf/Addepalli2022Efficient_RN18.json
```
On 2026-10-12T03:36:53Z: `"clean_acc": "65.45"`, `"autoattack_acc": "27.67"`, `"reported": "27.69"`, no `external`
field. If an `external` value of 27.57 or lower has since appeared, the result is no longer an improvement (see
Corrections in `READ_BEFORE_CITING.md` at the repository root).

## 4. Regenerate

The generating code and the exact commands of every stage are in `how-we-built-it/README.md`. The last step (merging
the three multi-start results onto the stage-5 tensor) can be redone exactly, on CPU in about a minute, from the
small inputs stored in `how-we-built-it/stage6-inputs/`:
```sh
DATA_DIR=data MODEL_DIR=models sh how-we-built-it/regenerate_final_step.sh regenerated
```
Expected last line: `regenerated/x_adv.npy sha256 4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb:
BIT-IDENTICAL to the published tensor`. The full pipeline from the clean images (`stage1_apgdce.py` ... `assemble.py`,
about 9 hours on an Apple M5 GPU) gives a tensor of the same kind but not the same bytes, because GPU kernels and random
streams differ between machines; `sh how-we-built-it/smoke_pipeline.sh OUT` runs every stage on 100 images with tiny
budgets.
