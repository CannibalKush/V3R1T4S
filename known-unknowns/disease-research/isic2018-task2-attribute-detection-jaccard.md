# ISIC 2018 Task 2 (dermoscopic attribute segmentation): beat the challenge-best mean Jaccard of 0.307 on the public test masks

🧬 **Disease research** · standard · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

ISIC 2018 Task 2 asked for pixel masks of five dermoscopic attributes that dermatologists use in melanoma assessment (pigment network, negative network, streaks, milia-like cysts, globules) on 1,000 test images, trained on 2,594 images. The metric is the Jaccard index per attribute, accumulated over the whole test set, averaged over the five attributes. The test masks are now a plain public download (ISIC2018_Task2_Test_GroundTruth.zip, 11.8 MB) and the official scorer is the isic-challenge-scoring package. The live leaderboard is topped by NMN_team at 0.307 (no external data), then Le-Health 0.276 and RECOD Titans 0.238. Unlike Task 1 (lesion boundary, about 0.80), this task is far from saturated: the attributes are thin, sparse and inconsistently annotated, and few groups have revisited it with modern segmentation models.

## What counts as a win

Binary masks for all five attributes on all 1,000 official Task 2 test images, from a model trained only on the official Task 2 training (and validation) data and frozen before any test scoring, whose leaderboard Jaccard computed by the skeptic with isic-challenge-scoring segmentation against ISIC2018_Task2_Test_GroundTruth is STRICTLY HIGHER (direction: max) than the Task 2 leader on the live leaderboard (re-fetched live immediately before claiming) and than any official-test value found by the NOVELTY check, by at least 0.01.

## Partial wins

- **p1:** Exceed 0.307 with a model trained on a laptop in under 12 hours, no external data.
- **p2:** Beat the leader's per-attribute Jaccard on at least three of the five attributes (from the leaderboard's per-category details), with the mean also above 0.307.

## How a win is checked

Skeptic downloads the public test masks, runs isic-challenge-scoring segmentation on the claimed mask folder (checks naming, image sizes, binary values and that all 5,000 masks exist), and compares with the live leaderboard. Audits that no test mask was read during training or tuning. Minutes.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://challenge.isic-archive.com/leaderboards/2018/?task=46&group_by=team>

## Sources

- <https://challenge.isic-archive.com/leaderboards/2018/>
- <https://challenge.isic-archive.com/data/>
- <https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task2_Test_GroundTruth.zip>
- <https://github.com/ImageMarkup/isic-challenge-scoring>
- <https://arxiv.org/abs/1902.03368>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Dataset-level Jaccard rewards getting the big positives right and not hallucinating on the many images with empty masks; train an image-level presence classifier per attribute and gate the segmenter with it.
- Use the Task 1 lesion mask (trained on Task 1 training data only) as an extra input channel or a hard crop: attributes only occur inside the lesion.
- Cross-domain import (retinal vessel and road-crack segmentation): thin-structure losses (clDice, topology-aware losses) and multi-scale line filters suit pigment network and streaks.
- Cross-domain import (astronomy source detection): milia-like cysts and globules are blob-like point sources; a Laplacian-of-Gaussian detector plus learned refinement may beat dense segmentation for them.
- Tune per-attribute probability thresholds on the validation set to maximise accumulated Jaccard, which is not the same threshold as per-pixel accuracy.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The metric accumulates intersection and union over all images; per-image mean Jaccard (common in papers) gives different numbers and cannot be compared.
- Test masks are public: threshold or epoch selection on test scores is leakage.
- Many papers on 'ISIC 2018 attributes' report on random splits of the training set; only the official 1,000-image test set compares with the leaderboard.
- Annotation is coarse (superpixel-based) and inconsistent; a model that exploits superpixel shapes may gain on the metric without detecting attributes better. Report that honestly.
- Attribute masks are a teaching and research aid; better scores do not make a diagnostic tool.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/isic2018-task2-attribute-detection-jaccard.md
```

Already set up? Say `run V3R1T4S on isic2018-task2-attribute-detection-jaccard`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `isic2018-task2-attribute-detection-jaccard`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
