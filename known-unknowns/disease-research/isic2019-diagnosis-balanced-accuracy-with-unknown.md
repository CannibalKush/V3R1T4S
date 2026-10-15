# ISIC 2019 skin-lesion diagnosis with an 'unknown' class: beat the best balanced accuracy (0.636; 0.607 without external data) on the public test labels

🧬 **Disease research** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

ISIC 2019 trained 8-class dermoscopy diagnosis on 25,331 images (HAM10000, BCN20000 and MSK) and tested on 8,238 images that also contain lesions of none of the 8 classes, which must be flagged as 'UNK'; the metric is balanced multiclass accuracy over 9 categories. The test ground truth is now a plain public CSV (ISIC_2019_Test_GroundTruth.csv) and the official scorer is isic-challenge-scoring. On the live leaderboard (images only) DAISYLab (Nils Gessert, Maximilian Nielsen, Mohsin Shaikh, Rene Werner, Alexander Schlaefer) leads with 0.636 using external data, and DysionAI leads the no-external-data class with 0.607; with metadata, DAISYLab 0.634 and Torus Actions 0.597. The open-set UNK requirement and the domain mix keep this well below the 0.85+ of ISIC 2018 Task 3, so it is genuinely unsaturated.

## What counts as a win

A prediction CSV for all 8,238 official ISIC 2019 test images (9 columns including UNK), from a model trained only on the official 2019 training images (and optionally the official training metadata) and frozen before any test scoring, whose balanced multiclass accuracy computed by the skeptic with isic-challenge-scoring against ISIC_2019_Test_GroundTruth.csv is STRICTLY HIGHER (direction: max) than the best value in its comparison class (images-only or images+metadata; external data or not) on the live 2019 leaderboard (re-fetched live immediately before claiming) and than any official-test value found by the NOVELTY check, by at least 0.005.

## Partial wins

- **p1:** No external data, images only: exceed 0.607 with a laptop-trainable model, mean of 3 seeds.
- **p2:** Improve UNK recall above every leaderboard entry's UNK recall (from the per-category details) while keeping overall balanced accuracy above 0.60, using an out-of-distribution detector calibrated only on training data.

## How a win is checked

Skeptic downloads the public ground-truth CSV, runs isic-challenge-scoring classification on the claimed CSV, checks 8,238 rows and image ids, and audits that no external image duplicates a test image (hash or ISIC id). Minutes.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://challenge.isic-archive.com/leaderboards/2019/>

## Sources

- <https://challenge.isic-archive.com/leaderboards/2019/>
- <https://challenge.isic-archive.com/data/>
- <https://isic-archive.s3.amazonaws.com/challenges/2019/ISIC_2019_Test_GroundTruth.csv>
- <https://github.com/ImageMarkup/isic-challenge-scoring>
- <https://arxiv.org/abs/1910.03910>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Treat UNK as open-set recognition: energy scores or Mahalanobis distance on penultimate features, threshold set on held-out training classes (leave-one-class-out simulation), never on test.
- Domain-aware training: the three source collections differ in camera and crop; group-DRO or per-source normalisation reduces shortcut learning.
- Cross-domain import (anomaly detection in industrial inspection): PatchCore-style memory banks of training-patch features to flag lesions unlike any training class.
- Cross-domain import (selective classification in credit scoring): reject-option decision rules trading coverage for accuracy map directly onto when to output UNK.
- Exploit balanced accuracy: rare classes (DF, VASC, SCC) and UNK each count as much as nevus, so per-class bias correction on validation data is worth more than backbone size.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- BCN20000 and the ISIC Archive later published labelled images that include ISIC 2019 test images; any external data must be deduplicated against the test set or the claim is leakage.
- Public test labels make test-tuned UNK thresholds tempting; any threshold chosen by looking at test scores invalidates the result.
- Papers often report 8-class accuracy on random training splits without UNK; those numbers do not compare with the leaderboard.
- Images-only and images+metadata are separate tasks on the leaderboard; compare within the same task and external-data class.
- A benchmark gain in open-set skin-lesion classification is not clinical evidence; say so.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/isic2019-diagnosis-balanced-accuracy-with-unknown.md
```

Already set up? Say `run V3R1T4S on isic2019-diagnosis-balanced-accuracy-with-unknown`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `isic2019-diagnosis-balanced-accuracy-with-unknown`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
