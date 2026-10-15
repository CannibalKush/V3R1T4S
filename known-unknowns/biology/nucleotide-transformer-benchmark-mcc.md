# Nucleotide Transformer benchmark: beat the best published MCC on a genomic regulatory task

🦠 **Biology** · standard · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

The Nucleotide Transformer downstream benchmark (Hugo Dalla-Torre and co-authors, InstaDeep; Nature Methods 2024) fixes 18 genomic classification tasks (histone marks such as H3K9me3 and H3K4me2, promoter and enhancer types, splice sites) with published train/test splits and ten-fold results. The public leaderboard space hosts benchmark.csv with 273 rows of per-fold Matthews correlation coefficients, F1 and accuracy for every model and task, so the exact distribution behind each bar is visible rather than a single number. Splice-site tasks are saturated (best ten-fold mean MCC 0.966-0.971) but the chromatin tasks are not: computed from that file, the best ten-fold mean MCC is 0.4807 on H3K9me3 (NT-1000G 2.5B), 0.4991 on H3K4me1 (Enformer), 0.5169 on H3K27ac (Enformer), 0.5186 on H2AFZ and 0.5694 on enhancer types, across 15-16 models per task. The data load from the Hugging Face hub without registration, and sequences are short enough (a few hundred to a few thousand bases) for a small convolutional model or a cached-embedding probe to be trained on a laptop.

## What counts as a win

Predictions for every sequence of a benchmark task's test split, from a model trained only on that task's training split (pretrained weights allowed if their corpus is declared and contains no test-split labels), whose mean MCC over the benchmark's ten folds, recomputed by the skeptic with the standard MCC definition on the released splits, is STRICTLY HIGHER (direction: max) than the best mean MCC for that task in the leaderboard's benchmark.csv (re-fetched live immediately before claiming) by at least 0.02 absolute, with the fold-wise values published and a paired comparison over folds favouring the new method.

## Partial wins

- **p1:** Beat the best listed mean MCC on H3K9me3 (0.4807 as of 2026-10-15) by at least 0.02 with a model under 100M parameters.
- **p2:** Beat the best listed mean MCC on any three of the 18 tasks at once with a single frozen architecture and training recipe.
- **p3:** A reproducible audit of fold-to-fold variance on the histone tasks, showing which published ranking differences are inside the noise, with the per-fold numbers from benchmark.csv.

## How a win is checked

Skeptic loads the task's released splits from the Hugging Face hub, checks the prediction file covers each test sequence per fold exactly once, computes MCC per fold, compares with the per-fold arrays in benchmark.csv, reruns the attacker's training from the released seed for at least one fold, and checks for overlap between training and test sequences. An hour or two.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://huggingface.co/spaces/InstaDeepAI/nucleotide_transformer_benchmark/blob/main/data/benchmark.csv>

## Sources

- <https://huggingface.co/spaces/InstaDeepAI/nucleotide_transformer_benchmark>
- <https://huggingface.co/spaces/InstaDeepAI/nucleotide_transformer_benchmark/blob/main/data/benchmark.csv>
- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11810778/fullTextXML>
- <https://github.com/instadeepai/nucleotide-transformer>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Histone-mark tasks are about nucleosome positioning and sequence composition; engineered k-mer and periodicity features with a gradient-boosted tree are a serious baseline and run in minutes.
- Cross-domain import (audio): dinucleotide periodicity around 10 base pairs is a helical-phasing signal, so a filterbank or spectral front end may capture what a token-level transformer dilutes.
- Cross-domain import (clinical trials): with ten folds and small effects, use paired tests across folds rather than comparing means, and design the experiment to detect a stated effect size.
- Reverse-complement equivalence is a free symmetry; averaging over both strands at inference costs nothing and is not standard in all published entries.
- Probe cached embeddings from several released genomic models and ensemble them, which separates the value of pretraining from the value of fine-tuning compute.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Genomic regions can be near-duplicated between train and test splits; verify the split as released rather than assuming it is clean, and report any overlap found.
- Reporting the best fold instead of the mean over folds is a common inflation; the criterion requires the ten-fold mean and the per-fold values.
- MCC, F1 and accuracy rank models differently on imbalanced histone tasks; compare against the same metric the leaderboard lists.
- Large pretrained genomic models saw most of the human genome, so they may have seen the test regions unlabelled; this is allowed but must be declared, and a claim of 'no leakage' needs the label check, not a corpus claim.
- A gain on a histone-mark classifier is a step in regulatory genomics, not evidence about any disease mechanism.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/nucleotide-transformer-benchmark-mcc.md
```

Already set up? Say `run V3R1T4S on nucleotide-transformer-benchmark-mcc`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `nucleotide-transformer-benchmark-mcc`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
