# Open Problems batch integration: beat every listed method on the metrics where single-cell integration still fails

🦠 **Biology** · standard · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

The Open Problems batch-integration task asks a method to remove batch effects from single-cell data while preserving biological structure, and scores it with the suite of metrics from the scIB study (Luecken and co-authors) split into batch-correction and bio-conservation groups. In the public run run_2026-08-17_16-18-21 (score_uns.yaml on the openproblems-data S3 bucket, 26 methods over six datasets) several bio-conservation metrics are far from the upper controls: on cellxgene_census/tabula_sapiens the best non-control values are isolated-label F1 0.1336 (scANVI), ARI 0.5125, label silhouette 0.5488 and kBET 0.4017, while the embed-cell-types control reaches 0.9634 label silhouette. Rare and isolated cell types are where every listed method, deep or classical, performs badly, and that is exactly the population that matters when integrating atlases to find disease-specific states. Inputs, solutions and the metric components are public and the smaller datasets run on a laptop.

## What counts as a win

An integrated embedding (or corrected matrix) for one dataset of the latest batch-integration run, produced by a method that reads only the task's input file (never the solution file with cell-type labels), whose scores recomputed by the skeptic with the official metric components of github.com/openproblems-bio/task_batch_integration are STRICTLY HIGHER (direction: max) than every non-control method listed for that dataset in the newest score file and on the live page (both re-fetched live immediately before claiming) on at least two bio-conservation metrics by at least 5% relative each, while no batch-correction metric falls below the median listed value; the same frozen method must be run on at least three datasets and all metrics reported.

## Partial wins

- **p1:** Isolated-label F1 on cellxgene_census/tabula_sapiens above the best listed non-control value (0.1336 as of 2026-10-15) by at least 25% relative, without dropping below the median on batch-correction metrics.
- **p2:** A single frozen configuration that beats the best listed method on at least one bio-conservation metric on three different datasets.
- **p3:** A reproducible demonstration of which metric pairs are in genuine tension on these datasets (for example isolated-label F1 against iLISI), with a Pareto front computed from the public score file and your own runs.

## How a win is checked

Skeptic downloads the dataset's input and solution files from the openproblems-data S3 bucket over plain HTTPS, runs the attacker's frozen method in a directory where the solution file is absent, scores the output with the official metric components, and compares with the newest score_uns.yaml and the live page. Minutes to an hour per dataset for the smaller atlases.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://openproblems.bio/benchmarks/batch_integration/>

## Sources

- <https://openproblems.bio/benchmarks/batch_integration/>
- <https://github.com/openproblems-bio/task_batch_integration>
- <https://openproblems-data.s3.amazonaws.com/resources/task_batch_integration/results/run_2026-08-17_16-18-21/score_uns.yaml>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Isolated labels are, by construction, cell types present in few batches; detect candidate isolated populations without labels (density-based outlier structure) and protect them from mixing, instead of applying one global correction strength.
- Cross-domain import (signal separation): treat batch as a nuisance subspace and remove it with an explicit invariance constraint, as in domain-adversarial training, but with a per-cluster strength so rare clusters are not erased.
- Cross-domain import (survey calibration): raking and post-stratification align marginal distributions between batches without distorting within-cell-type structure, which is exactly the tension the metrics measure.
- Several listed methods are classical (Harmony, Scanorama, fastMNN, Combat); a careful combination of their outputs, chosen without labels, may dominate each one and is cheap to test.
- Optimise the actual reported quantity: the metric suite is public, so measure the trade-off curve directly rather than trusting a single hyperparameter default.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Reading the solution file, even to pick the number of clusters or an integration strength, is label peeking; the method must be label-free end to end.
- The controls (embed_cell_types, shuffle_integration, no_integration and their variants) must be excluded when computing 'the best listed method'; they are there to bound the scale.
- The overall score shown on the website is an aggregate of normalised metrics, so a higher aggregate can come from other methods changing; the criterion uses raw per-metric values.
- Some metrics are missing for some methods and datasets in the score file; treating missing as zero manufactures a false bar.
- Better integration metrics do not establish that a newly mixed population is biologically real; any claim about a disease-specific cell state needs evidence beyond this benchmark.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/openproblems-batch-integration-hard-metrics.md
```

Already set up? Say `run V3R1T4S on openproblems-batch-integration-hard-metrics`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `openproblems-batch-integration-hard-metrics`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
