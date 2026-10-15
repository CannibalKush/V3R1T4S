# Open Problems label projection: beat the best listed accuracy/macro-F1 for transferring cell-type labels on the hardest datasets

🦠 **Biology** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

The Open Problems label-projection task trains a classifier on annotated single cells from some batches and predicts cell types for held-out batches. Most datasets are near-saturated (accuracy > 0.95), but in the latest public run (run_2026-09-21_17-18-30) two are not: cellxgene_census/tabula_sapiens, where the best accuracy is 0.377 (Seurat TransferData; next MLP 0.247) and best macro-F1 0.167; and cellxgene_census/gtex_v9, where accuracy reaches 0.893 (scANVI scArches) but macro-F1 is only 0.459. The tabula_sapiens result in particular suggests something structural (batch split by tissue or donor, label granularity) that a careful method could exploit.

## What counts as a win

For cellxgene_census/tabula_sapiens or cellxgene_census/gtex_v9, a frozen method that reads only train.h5ad and test.h5ad (never solution.h5ad) produces labels whose accuracy AND f1_macro, recomputed by the skeptic with the official metric components of github.com/openproblems-bio/task_label_projection, are STRICTLY HIGHER (direction: max) than every non-control method's values for that dataset in the newest score file and on the live page (re-fetched live immediately before claiming), by at least 0.02 absolute on f1_macro and not lower on accuracy.

## Partial wins

- **p1:** gtex_v9: macro-F1 above the listed best by >= 0.02 (rare cell types are where the headroom is).
- **p2:** A checkable explanation of the tabula_sapiens collapse (e.g. label sets that differ between train and test batches, read from train.h5ad/test.h5ad metadata only) plus a method that handles it.

## How a win is checked

Skeptic downloads train.h5ad and test.h5ad (gtex_v9 about 3 GB; tabula_sapiens about 20 GB, so gtex_v9 is the laptop-friendly target), runs the frozen method with solution.h5ad absent, scores with the official components, compares with the newest S3 score file and live page.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://openproblems.bio/benchmarks/label_projection/>

## Sources

- <https://openproblems.bio/benchmarks/label_projection/>
- <https://github.com/openproblems-bio/task_label_projection>
- <https://openproblems-data.s3.amazonaws.com/?list-type=2&prefix=resources/task_label_projection/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Inspect the split first: compare the label sets and batch covariates of train.h5ad and test.h5ad (metadata only); if test batches contain types absent from training or at different granularity, an open-set classifier with hierarchical (Cell Ontology) back-off is the fix.
- Cross-domain import (domain adaptation in vision): self-training with confidence thresholds and class-balanced pseudo-labels on the unlabeled test cells (transductive, allowed because test expression is an input), plus batch-statistic re-normalisation (AdaBN).
- Cross-domain import (optimal transport): label transfer by entropic OT between train and test cells in a shared embedding with unbalanced marginals, which handles cell-type proportion shift.
- Class-imbalance-aware training (logit adjustment, focal loss) directly targets macro-F1, which the listed methods do not optimise.
- Ensemble the strongest listed families (scANVI, Seurat TransferData, logistic regression) with weights chosen on a batch-held-out split of the training data.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- solution.h5ad (the test labels) sits in the same public folder; the skeptic must run the method without it.
- Original cellxgene census annotations of the test cells are public elsewhere; looking them up by cell barcode or donor is leakage.
- Transductive use of test expression is allowed, but using test-set label distributions estimated from the solution is not.
- Datasets are offered in several normalisations (log_cp10k, sqrt_cp10k, l1_sqrt); check which one the leaderboard entry used.
- Re-fetch the S3 results listing before claiming; runs are frequent.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/openproblems-label-projection-cross-dataset.md
```

Already set up? Say `run V3R1T4S on openproblems-label-projection-cross-dataset`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `openproblems-label-projection-cross-dataset`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
