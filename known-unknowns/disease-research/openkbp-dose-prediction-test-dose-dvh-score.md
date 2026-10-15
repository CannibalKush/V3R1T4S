# OpenKBP radiotherapy dose prediction: beat the challenge winner's dose score 2.429 Gy or DVH score 1.478 Gy on the 100 released test patients

🧬 **Disease research** · standard · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

OpenKBP (AAPM 2020 grand challenge; Aaron Babier, Binghao Zhang, Rafid Mahmood, Kevin Moore, Thomas Purdie, Andrea McNiven and Timothy Chan, Medical Physics 2021) released CT, structure masks and clinical intensity-modulated radiotherapy dose for 340 head-and-neck cancer patients, split 200 train / 40 validation / 100 test, with the scoring class (EvaluateDose) in the open-kbp repository. Test doses were published after the challenge, so the two official metrics can be recomputed offline: dose score (mean absolute voxel dose error inside the feasible-dose mask, Gy) and DVH score (mean absolute error of the challenge's DVH metrics, Gy); lower is better. The final blinded test leaderboard (an image in the repository README) is topped by LSL AnHui University (Shuolin Liu, Jingjing Zhang, Teng Li, Hui Yan, Jianfei Liu) with dose score 2.4294 and DVH score 1.4776, ahead of SuperPod (2.5635) on dose and PTV - Prediction Team Vienna (1.5393) on DVH. Later papers report dose scores near the winner (for example TrDosePred, 2.426 Gy dose / 1.592 Gy DVH, and nnDoseNet, 2.579 / 1.540); at least one paper (DeepDoseNet, arXiv:2111.00077) reports about 2.0 Gy on the test split, which must be reproduced or explained before any claim.

## What counts as a win

Predicted dose files for all 100 OpenKBP test patients, from a model trained only on the 200 training patients (validation patients allowed for model selection) and frozen before any test scoring, whose dose score OR DVH score computed by the skeptic with the repository's EvaluateDose class is STRICTLY LOWER (direction: min) than the corresponding first-place value on the final test leaderboard shown in https://github.com/ababier/open-kbp (re-fetched live immediately before claiming) AND lower than every test-split value for that metric found by the NOVELTY check (including arXiv:2111.00077 if its protocol is the standard one), by at least 0.02 Gy, with the other score not worse than the winner's by more than 0.05 Gy.

## Partial wins

- **p1:** Dose score below 2.4294 with DVH score below 1.5393 (better than every challenge team on dose while staying in the top two on DVH), trained on a laptop (CPU or Apple GPU) in under 24 hours.
- **p2:** A reproduction audit of the strongest post-challenge claim (for example the about-2.0 Gy DeepDoseNet test result): rerun with the official evaluator and report whether it holds on the standard 100-patient test split.

## How a win is checked

Skeptic clones the open-kbp repository (data in provided-data/ with train-pats, valid-pats, test-pats), loads the claimed per-patient dose CSVs, runs EvaluateDose to compute dose and DVH scores over the 100 test patients, and compares with the leaderboard image. Re-runs inference from released weights on a subset to confirm the files. Audits training code for any read of test-pats dose. Under an hour.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/ababier/open-kbp>

## Sources

- <https://github.com/ababier/open-kbp>
- <https://raw.githubusercontent.com/ababier/open-kbp/master/README.md>
- <https://arxiv.org/abs/2011.14076>
- <https://arxiv.org/abs/2111.00077>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Cascaded 3D U-Nets with the winner's recipe (coarse then fine prediction, heavy flips and rotations, test-time augmentation) as the reproduction baseline; the winning code is public.
- Cross-domain import (physics-informed learning): add a differentiable pencil-beam or distance-to-target prior as an input channel, so the network learns a correction to physics rather than dose from scratch.
- Cross-domain import (geostatistics / kriging): model the residual dose field as a Gaussian process conditioned on structure distances, and blend with the network prediction where the network is uncertain.
- Optimise the metric directly: add a differentiable DVH loss (sorting-based) so the DVH score is trained for, not just voxel error.
- Small-data regime: 200 patients is tiny; ensembles of small 3D networks at reduced resolution with careful upsampling may beat one large network on a laptop.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Test doses are public: tuning epochs, ensembles or post-processing on test-pats scores is leakage. The README itself warns that post-challenge CodaLab results cannot be trusted for this reason.
- Scoring outside the feasible-dose mask, or on a subset of structures, changes the numbers; only the repository's EvaluateDose on all 100 test patients compares with the leaderboard.
- Several papers report on the validation split or on their own re-splits; values that look like 2.0-2.3 Gy are often not the standard test split.
- The repository's data loader and the original challenge data release must match (file versions changed when the repo was modernised); check patient counts and a sample patient's dose sums.
- A better dose prediction is an input to automated planning; it is not a treatment plan and says nothing about clinical outcomes.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/openkbp-dose-prediction-test-dose-dvh-score.md
```

Already set up? Say `run V3R1T4S on openkbp-dose-prediction-test-dose-dvh-score`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `openkbp-dose-prediction-test-dose-dvh-score`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
