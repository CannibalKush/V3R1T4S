# PEER fold classification: beat the leaderboard's 32.1% accuracy on held-out SCOP superfamilies

🦠 **Biology** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

PEER (Minghao Xu and co-authors, TorchProtein/TorchDrug) maintains public leaderboards for protein-sequence tasks at torchprotein.ai/benchmark, with fixed splits, published dataset statistics and per-entry parameter counts. The hardest board is fold classification: entire SCOP 1.75 superfamilies are held out, so the test proteins have similar structures but dissimilar sequences to anything in training, and the model must name one of 1195 folding topologies. The top listed accuracy is 32.10% (+/- 0.72) for a multi-task ESM-1b with contact prediction, then 29.95% for frozen ESM-1b; a plain CNN and LSTM are far lower. Two thirds of the test set is still misclassified, with 12,312 training and 718 test proteins, which is small enough to train on a laptop CPU in hours with a modest model on top of cached embeddings. Related boards on the same page are also unsaturated (solubility 70.63%, subcellular localization 79.82%).

## What counts as a win

Predicted fold labels for every protein in the PEER fold-classification test split, from a model trained only on the task's designated training set (plus publicly declared pretraining corpora that contain no SCOP 1.75 superfamily labels for the test superfamilies), whose test accuracy computed by the skeptic with the task's standard accuracy definition is STRICTLY HIGHER (direction: max) than the top accuracy listed on https://torchprotein.ai/benchmark for fold classification (re-fetched live immediately before claiming) by at least 1.5 percentage points, reported as mean and standard deviation over at least three seeds, and higher than any later published value found by the novelty check.

## Partial wins

- **p1:** Beat the top listed accuracy using a model of at most 150M parameters (the current leader uses about 659M), with the same seed protocol.
- **p2:** Beat the top listed accuracy on the solubility board (70.63% as of 2026-10-15) or the subcellular localization board (79.82%) under the same rules, with all boards you ran reported.
- **p3:** A published analysis, reproducible from the public split, of which of the 1195 folds account for the errors (for example singleton folds) and a method that fixes one named failure mode.

## How a win is checked

Skeptic obtains the PEER fold-classification split through the TorchProtein data loaders (public download, no registration), checks the prediction file covers each test protein exactly once, computes accuracy, reruns the attacker's training script from the released seed to reproduce the number within its stated standard deviation, and checks that no test superfamily appears in training. An hour or two.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://torchprotein.ai/benchmark>

## Sources

- <https://torchprotein.ai/benchmark>
- <https://github.com/DeepGraphLearning/PEER_Benchmark>
- <https://arxiv.org/abs/2206.02096>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Held-out superfamilies make this remote homology detection, so retrieval beats classification: embed training proteins, retrieve nearest neighbours and vote over their folds, which handles the 1195-way long tail better than a softmax head.
- Cross-domain import (few-shot vision): treat each fold as a class prototype and train with a metric-learning loss (ArcFace or supervised contrastive), standard for face recognition with thousands of rare classes.
- Cross-domain import (speech): fold topology is a global property of a long sequence; use attentive statistics pooling from speaker recognition rather than mean pooling of residue embeddings.
- Predict a cheap structural surrogate first (secondary-structure string, contact-map summary statistics) and classify on that, which is closer to what defines a fold than the raw sequence.
- Calibrate the long tail explicitly: with 1195 classes and 12,312 training proteins, many folds have a handful of examples, so class-balanced losses or logit adjustment may be worth more than a bigger encoder.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Any structure-based tool that queries a database containing the test proteins' own structures (or their superfamily members) breaks the held-out-superfamily design; declare every external database and check its contents.
- The leaderboard reports mean and standard deviation over seeds; a single lucky seed above the bar is not a win, hence the three-seed requirement.
- Multi-task entries on this board use extra supervision (contact prediction, secondary structure) that is listed in the 'external data' column; a comparison must respect what each entry was allowed to use.
- The page hosts several boards with different metrics; quoting a solubility accuracy against the fold-classification bar is a category error.
- Leaderboards hosted on a project site can go stale, so the novelty check must search the literature for higher published numbers on the same split before any claim.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/peer-fold-classification-superfamily-holdout.md
```

Already set up? Say `run V3R1T4S on peer-fold-classification-superfamily-holdout`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `peer-fold-classification-superfamily-holdout`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
