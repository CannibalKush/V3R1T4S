# RobustBench CIFAR-100: a stronger attack on Addepalli2022Efficient_RN18

[RobustBench](https://robustbench.github.io) ranks adversarially trained image classifiers by their *robust accuracy*:
the fraction of test images that stay correctly classified under every perturbation of at most ε per pixel. Robust
accuracy can only be measured from above (an attack that finds more adversarial images gives a lower, more accurate
value), and RobustBench's standard attack is AutoAttack. A lower count from a stronger attack shows that the listed
value overestimates the model's robustness.

**Claim (exact scope), as of 2026-10-12T03:36:53Z.** The tensor in `adversarial-examples/` (10,000 CIFAR-100 test images,
float32, shape (10000, 3, 32, 32), standard torchvision order, values in [0, 1]) satisfies max |x_adv − x| ≤ 8/255
for every pixel of every image (checked in float64, no tolerance; the maximum is exactly 8/255) and, against the
unmodified RobustBench model `Addepalli2022Efficient_RN18` (CIFAR-100, L∞) on CPU in float32:

| | clean accuracy | robust accuracy | robust images |
|---|---|---|---|
| RobustBench model_info / leaderboard (AutoAttack) | 65.45 % | **27.67 %** | 2,767 |
| this tensor | 65.45 % (6,545) | **27.57 %** | **2,757** |

That is **10 images fewer** than RobustBench's AutoAttack value, and 12 fewer than the value reported in the model's
paper (27.69 %). An image counts as robust when it is classified correctly both clean and on x_adv; exact ties count
as robust (in the model's favour; there are none). `adversarial-examples/robust_indices.txt` lists the 2,757 images.

**The record we beat.** `model_info/cifar100/Linf/Addepalli2022Efficient_RN18.json` in github.com/RobustBench/robustbench
(fetched 2026-10-12T03:36:53Z, sha256 `43eee2a7…105c`, unchanged since 11 Oct; repository HEAD 78fcc9e4 of
2025-03-31) lists `autoattack_acc` 27.67 and no `external` value; the leaderboard shows 27.67 as the best known robust
accuracy for this model. The stronger-attack papers that re-evaluate RobustBench CIFAR-100 models (A3, AutoAE, MALT,
PMA) do not evaluate this model, and the CR Attack README lists 27.67, no lower. A literature and code search found no
lower published value. Details: `the-record-we-beat/sources_2026-10-12T03-36-53Z.json`.

**Status.** Found by AI agents (see `READ_BEFORE_CITING.md` at the repository root) on 2026-10-11; verified internally
by three independent reviewers with their own code; **not yet reported to the maintainers** (RobustBench) at the time
of this release.

## How the tensor was made

The images were attacked with an ensemble of APGD-style attacks (Croce and Hein's AutoAttack components) using margin
losses (CW, DLR and targeted variants), a published constraint-relaxation attack (CR Attack) as a warm start, and
many random restarts concentrated on the images closest to the decision boundary; every replaced image was re-checked
on CPU before it went into the tensor. The image that took the count from 2,758 to 2,757 (index 2137) needed 250
restarts of 100 steps. Images that the model already misclassifies are left unchanged (3,455 images). The attack code
is not part of this release; the claim rests on the tensor and the checker.

## Storage (lossless)

The tensor is 122,880,128 bytes as a `.npy` file. It is stored with `numpy.savez_compressed` (zip + DEFLATE, lossless)
as `adversarial-examples/x_adv_Addepalli2022Efficient_RN18.npz` (45,517,304 bytes). The single member `x_adv.npy` of the
archive **is** the original file: its sha256 is `4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb`, the
hash of the tensor the reviewers checked. `verify-it-yourself/unpack.py` proves this three ways (the zip member streamed
out, the loaded array re-saved with `numpy.save`, and the raw float32 bytes, sha256 `aabc97bd…1ee0`) and can write the
`.npy` back out.

## Credits (please cite)

- **The model**: S. Addepalli, S. Jain, R. Venkatesh Babu, *Efficient and Effective Augmentation Strategy for
  Adversarial Training*, NeurIPS 2022, arXiv:2210.15318. The weights are theirs, distributed through RobustBench, and
  are not redistributed here.
- **RobustBench**: F. Croce, M. Andriushchenko, V. Sehwag, E. Debenedetti, N. Flammarion, M. Chiang, P. Mittal,
  M. Hein, *RobustBench: a standardized adversarial robustness benchmark*, NeurIPS 2021 Datasets and Benchmarks,
  arXiv:2010.09670.
- **AutoAttack / APGD**: F. Croce and M. Hein, *Reliable evaluation of adversarial robustness with an ensemble of
  diverse parameter-free attacks*, ICML 2020. **CR Attack**: Pan et al., AAAI 2025.
- **CIFAR-100**: A. Krizhevsky, *Learning Multiple Layers of Features from Tiny Images*, technical report, 2009.

## Limitations

- **The margin is the bare minimum.** 2,757 is exactly 10 images below 2,767. One more robust image voids the claim.
- **Near-ties.** Three of the fooled images (indices 4129, 2137, 9693) win by tiny logit margins (+1.4e-4, +3.7e-4,
  +4.2e-4 on CPU). Across CPU batch sizes 1/200/250, 1 and 4 threads, float64 and Apple MPS the margins moved by at
  most 4e-6, so the count was stable there, but other hardware (for example CUDA with TF32 or different convolution
  kernels) has not been tested and could flip a near-tie row.
- **What "8/255" is measured against.** RobustBench feeds the model `ToTensor` images, i.e. uint8/255 rounded to
  float32; against those the maximum perturbation is exactly 8/255 (float64 arithmetic). Against the exact rationals
  uint8/255 the maximum is 8/255 + 2.8e-8, an artefact of the float32 rounding of the clean images, not of the attack.
- The count is for this one model. It says nothing about other RobustBench entries, and it is an upper bound on the
  model's true robust accuracy, not its value.
- The tensor contains the CIFAR-100 test images (3,455 unchanged, the rest perturbed by at most 8/255); see
  `LICENSING.md` at the repository root.
- Internal verification only; RobustBench has not reviewed it.

## Files

```
README.md, RUN_IT_YOURSELF.md, INDEX.csv
adversarial-examples/  x_adv_Addepalli2022Efficient_RN18.npz (the tensor, lossless, 45.5 MB), robust_indices.txt (the 2,757 robust images)
verify-it-yourself/    unpack.py (restore + losslessness proof), rbcheck.py (standalone checker), run_checks.sh, RECEIPTS.md
the-record-we-beat/    sources_2026-10-12T03-36-53Z.json (fetch time, HTTP headers, sha256, extracted values)
```
