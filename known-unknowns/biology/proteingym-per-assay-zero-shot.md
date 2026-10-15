# ProteinGym zero-shot substitutions: beat every listed model's Spearman on a single DMS assay

🦠 **Biology** · standard · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

ProteinGym (OATML-Markslab) publishes, for 217 deep-mutational-scanning assays, the Spearman correlation of every benchmarked zero-shot fitness predictor (~100 models) in DMS_substitutions_Spearman_DMS_level.csv; the overall leaders (AIDO Protein-RAG 16B, VenusREM, ~0.518 average) are listed in the Summary CSV. Restricted to non-disease assays (stability, activity, binding, expression of non-pathogen proteins). Produce zero-shot scores (no use of the assay's own labels) that achieve a Spearman strictly higher than the maximum over all listed models for at least one assay.

## What counts as a win

For one non-disease assay in the live DMS-level CSV at https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv (re-fetched immediately before claiming), a saved score file (mutant, score) produced by a frozen, pre-registered method whose code never reads the assay's DMS_score column, such that ProteinGym's own Spearman routine yields a value strictly greater than the row maximum over all listed models; the method's hyperparameters must be fixed before scoring the target assay (pre-registration hash), and the same method must be run on all assays in the same function category with results reported.

## Partial wins

- **category-top10:** A frozen laptop-runnable method (<= 650M params) whose average Spearman over all Stability assays exceeds the 10th-ranked model's Stability column in the Summary CSV.
- **low-msa-assay-win:** Beat the row max on a Low_MSA_depth assay with a method using no MSA.

## How a win is checked

Download the assay CSV from the ProteinGym data release, run the official Spearman computation on the submitted score file, compare to the live DMS-level row max; skeptic re-runs the frozen method on the assay from the pre-registered commit to reproduce the score file byte-for-byte (or within float tolerance). Under an hour per assay for small models.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv>

## Sources

- <https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv>
- <https://proteingym.org/benchmarks>
- <https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/Summary_performance_DMS_substitutions_Spearman.csv>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Rank-average ensemble of precomputed ProteinGym model scores (released in the repo) plus ESM-2 650M masked-marginals, with ensemble weights fixed from OTHER assays only.
- Structure-aware thermodynamic proxy: ESM-IF / ProteinMPNN log-likelihoods on the AlphaFold DB structure for stability assays.
- Evolutionary model: EVmutation/Potts model trained on a fresh jackhmmer MSA with tuned reweighting, combined with site-conservation priors.
- Cross-domain import (recommender systems): low-rank matrix factorisation across assays x models to learn which model families transfer to which protein families, then pick per-assay without using its labels.
- Cross-domain import (econometrics/forecast combination): Bates-Granger optimal forecast combination with shrinkage, fit leave-one-assay-out.
- Cross-domain import (NLP calibration): temperature/position-specific calibration of PLM logits using unlabeled mutational spectra (entropy normalization per site).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Label leakage: any tuning, ensembling weight or model selection that touches the target assay's DMS_score is supervised, not zero-shot. Freeze before scoring.
- Cherry-picking: beating the row max on one of 217 assays by chance is likely for a noisy small assay; require the frozen method be reported on the whole category and pre-registered.
- Several assay rows have very few mutants; Spearman bootstrap SE can exceed the margin. Require margin > bootstrap SE.
- Disease-relevant assays (human disease genes, viral proteins) belong to another lane; restrict to non-disease assays.
- The CSVs on main changed in Jan/Mar 2026; always compare to the live file, not a cached copy.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/proteingym-per-assay-zero-shot.md
```

Already set up? Say `run V3R1T4S on proteingym-per-assay-zero-shot`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `proteingym-per-assay-zero-shot`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
