# LUNA16 lung-nodule detection and false-positive reduction: beat the best CPM (0.951 detection, 0.968 false-positive reduction) under the official 10-fold protocol

🧬 **Disease research** · standard · tractability ★★☆☆☆ · compute: laptop-days · open as of 2026-10-15

## The problem

LUNA16 (Arnaud Setio, Colin Jacobs and co-authors, Medical Image Analysis 2017) is the standard benchmark for lung-cancer screening CT computer-aided detection: 888 LIDC-IDRI CT scans in 10 fixed subsets, 1,186 reference nodules (>= 3 mm, accepted by at least 3 of 4 radiologists), an official evaluation script, and the Competition Performance Metric (CPM: mean sensitivity at 1/8, 1/4, 1/2, 1, 2, 4 and 8 false positives per scan). Methods are evaluated by 10-fold cross-validation over the fixed subsets. The results page lists PAtech at 0.951 for full detection and PATech at 0.968 for the false-positive-reduction track (classifying the 754,975 supplied candidates in candidates_V2). Data, annotations, candidates and the evaluation script are on Zenodo under CC BY 4.0 (about 120 GB of scans).

## What counts as a win

Per-subset prediction CSVs for all 888 scans, each subset predicted by a model that never saw that subset's scans or labels in training or selection (strict 10-fold over the official subsets), whose CPM computed by the skeptic with the official LUNA16 evaluation script (with annotations_excluded handling) is STRICTLY HIGHER (direction: max) than the top score of the same track on https://luna16.grand-challenge.org/Results/ (re-fetched live immediately before claiming) and than any strict-10-fold value for that track found by the NOVELTY check, by at least 0.005.

## Partial wins

- **p1:** False-positive-reduction track: CPM above 0.968 on candidates_V2 with a model small enough to train all 10 folds on a laptop in under 3 days.
- **p2:** Detection track: CPM above 0.951 with all 10 folds released, or a documented reproduction showing that a published claim above 0.951 does or does not hold under the strict protocol.

## How a win is checked

Skeptic downloads annotations.csv, annotations_excluded and the evaluation script from Zenodo, runs the script on the merged predictions, and spot-checks 1-2 folds by retraining or by running released weights on that subset. Audits fold assignment (subset id per scan) and that no fold's model was tuned on its own test subset. Hours for scoring and audit; days for a full retrain.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://luna16.grand-challenge.org/Results/>

## Sources

- <https://luna16.grand-challenge.org/Results/>
- <https://luna16.grand-challenge.org/Evaluation/>
- <https://zenodo.org/records/3723295>
- <https://zenodo.org/records/4121926>
- <https://arxiv.org/abs/1612.08012>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- False-positive reduction is laptop-friendly: extract 3D patches at candidate locations once (small disk footprint), then train compact 3D CNNs or 2.5D multi-view networks per fold.
- Cross-domain import (particle physics triggers): cascaded classifiers with increasing cost, as used in detector triggers, cut most easy negatives with a cheap model before an expensive one.
- Cross-domain import (astronomy point-source detection): matched filters and scale-space blob detectors on lung-masked CT give a strong, interpretable candidate generator.
- Ensembles across folds of different architectures and input scales, combined by rank averaging, typically add the last 0.005-0.01 CPM.
- Hard-negative mining focused on vessels and fissures, which dominate false positives at 1/8 and 1/4 FPs per scan where the CPM is weakest.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- All labels are public and evaluation is self-run cross-validation, so leakage is easy: any use of a fold's scans for training, early stopping or threshold choice for that fold's predictions invalidates the claim.
- Many papers re-split LIDC-IDRI or use different nodule definitions (all nodules, >= 1 radiologist); only the official 1,186-nodule reference and script compare with the results page.
- Detection and false-positive-reduction tracks are different tasks with different bars; do not compare a candidate classifier with the detection board.
- Pretraining on LIDC-IDRI-derived data (including public nodule datasets built from it) leaks test scans; declare and exclude.
- The results page closed to new entries years ago, so later literature claims must be checked; CPM gains do not imply screening benefit.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/luna16-nodule-detection-cpm-10fold.md
```

Already set up? Say `run V3R1T4S on luna16-nodule-detection-cpm-10fold`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `luna16-nodule-detection-cpm-10fold`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
