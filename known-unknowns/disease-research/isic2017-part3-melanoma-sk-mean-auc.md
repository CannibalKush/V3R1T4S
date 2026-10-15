# ISIC 2017 Part 3 (melanoma and seborrheic keratosis): beat the challenge-best mean AUC of 0.911 on the public 600-image test labels

🧬 **Disease research** · standard · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

ISIC 2017 Part 3 (Codella et al., ISBI 2018) scored two binary tasks on 600 dermoscopy test images: melanoma vs all and seborrheic keratosis vs all, ranked by the mean of the two ROC AUCs, with only 2,000 training and 150 validation images. The test ground truth is a plain public CSV (ISIC-2017_Test_v2_Part3_GroundTruth.csv) and the official scorer is isic-challenge-scoring. The live leaderboard is led by the Casio and Shinshu University joint team (Kazuhisa Matsunaga and colleagues) at 0.911, then Universidad Carlos III de Madrid (Ivan Gonzalez-Diaz) 0.910 and RECOD Titans 0.908, none flagged as using external data on the board. The small training set makes this a sharp test of data efficiency.

## What counts as a win

Probability scores for all 600 official test images for both tasks, from a model trained only on the 2,000 official training images (validation images allowed for selection) and frozen before any test scoring, whose mean of melanoma AUC and seborrheic-keratosis AUC computed by the skeptic with isic-challenge-scoring against the public Part 3 test ground truth is STRICTLY HIGHER (direction: max) than the Part 3 leader on the live 2017 leaderboard (re-fetched live immediately before claiming) and than any official-test value without external data found by the NOVELTY check, by at least 0.005. Claims using external dermoscopy data are reported separately and must be deduplicated against the test images.

## Partial wins

- **p1:** Melanoma AUC alone above the best melanoma AUC on the leaderboard's per-category details, no external data.
- **p2:** Mean AUC above 0.911 with an ImageNet-pretrained model fine-tuned on a laptop in under 6 hours, mean over 3 seeds.

## How a win is checked

Skeptic downloads the public Part 3 test ground truth CSV, runs isic-challenge-scoring classification on the claim, checks 600 ids, and audits external data for overlap with test images. Minutes.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://challenge.isic-archive.com/leaderboards/2017/?task=44&group_by=team>

## Sources

- <https://challenge.isic-archive.com/leaderboards/2017/>
- <https://isic-archive.s3.amazonaws.com/challenges/2017/ISIC-2017_Test_v2_Part3_GroundTruth.csv>
- <https://github.com/ImageMarkup/isic-challenge-scoring>
- <https://arxiv.org/abs/1710.05006>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Strong pretrained backbones plus heavy augmentation and multi-crop test-time averaging; most 2017 entries used ResNet-50-era models.
- Self-supervised pretraining on the 2,000 training images only (DINO-style) before fine-tuning, which keeps the no-external-data class.
- Cross-domain import (few-shot learning): prototype-based heads and episodic training suit a 2,000-image, two-task problem.
- Cross-domain import (radiology reader studies): AUC-optimising pairwise losses (as used for screening CAD) target the metric directly.
- Multi-task training of the two binary heads with the Part 1 lesion masks as an auxiliary task (masks are part of the official training data).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Later ISIC releases (2018, 2019 training sets and the ISIC Archive) contain many 2017 test images with labels; any external data must be deduplicated by hash against the 600 test images.
- Test labels are public; selecting checkpoints or ensembles by test AUC is leakage.
- Some papers report melanoma AUC only, or a 3-class accuracy; only the mean of the two AUCs compares with the primary leaderboard metric.
- 600 images and roughly 117 melanomas mean AUC differences below about 0.01 are within noise; report bootstrap intervals.
- Research benchmark only; no diagnostic claim.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/isic2017-part3-melanoma-sk-mean-auc.md
```

Already set up? Say `run V3R1T4S on isic2017-part3-melanoma-sk-mean-auc`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `isic2017-part3-melanoma-sk-mean-auc`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
