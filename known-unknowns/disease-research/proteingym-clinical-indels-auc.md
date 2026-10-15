# ProteinGym clinical indels: beat the leaderboard's best average AUC on insertion/deletion clinical variants

🧬 **Disease research** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

ProteinGym (Pascal Notin, Aaron Kollasch, Debora Marks and colleagues) keeps a separate, much thinner leaderboard for CLINICAL INDELS - benign versus pathogenic insertion/deletion variants in human proteins - alongside its well-known substitution tables. The live summary CSV fetched 2026-10-15 lists only 18 baselines and is led by PoET (200M) at average AUC 0.935, then Provean 0.927, RITA L 0.922, RITA XL 0.916, down to a profile hidden Markov model at 0.663, ProtGPT2 0.649 and Unirep 0.599. Unlike the substitution tables, this file carries no bootstrap standard error column, and almost every strong substitution-benchmark method (GEMME, EVE, ESM-1b/1v, SaProt, ProSST, ESCOTT, VenusREM, RSALOR) is absent because it cannot score length changes. A 0.26 AUC gap between the leader and the plain HMM, in a category where indels dominate unsolved rare-disease exomes, is unusually open ground for alignment machinery that runs on a CPU.

## What counts as a win

Success means a saved score file with one real-valued score per variant covering EVERY protein and EVERY variant of the ProteinGym clinical indel benchmark (v1.3 release; no protein dropped, mutant identifiers matched exactly, sha256 of the file published), produced by a released method that uses no clinical label source for any benchmark protein (no ClinVar, HGMD, dbNSFP pathogenicity column, gnomAD-derived pathogenicity score and no supervised pathogenicity predictor) and no per-protein tuning, such that the repository's own scoring scripts, run by the skeptic with the repository's aggregation (AUC per protein, then the repository's UniProt/category aggregation), give an Average_AUC STRICTLY GREATER (direction: max) than the best Average_AUC in https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/clinical_zero_shot/indels/AUC/Summary_performance_clinical_indels_AUC.csv , re-fetched live immediately before claiming (0.935 for PoET (200M) as fetched 2026-10-15), by at least 0.010 absolute AND outside a 95% bootstrap interval the skeptic computes by resampling proteins (the live CSV publishes no standard error, so the interval must be computed, not quoted).

## Partial wins

- **p1:** Beat the best alignment-only baseline on the live clinical indel table (Provean, 0.927 as fetched 2026-10-15) by >= 0.010 with a method that uses no neural network at all and runs the whole benchmark on a laptop in under 4 hours, with timings.
- **p2:** Add a genuinely new model class to this table: full-benchmark clinical indel scores from a structure-aware or MSA-based method the table currently lacks, reaching Average_AUC >= 0.92 with code, logs and a reproducible environment.
- **p3:** A per-protein audit: a list of >= 20 clinical proteins where the live leader's released scores give AUC < 0.6, plus a method exceeding AUC 0.8 on those proteins without dropping overall Average_AUC more than 0.005 below the live leader.

## How a win is checked

Skeptic clones OATML-Markslab/ProteinGym at a pinned commit, downloads the v1.3 clinical indel benchmark files as the README documents, checks the submitted score file covers exactly the benchmark variant set (per-protein row counts and mutant identifiers), runs the repository's performance scripts to recompute per-protein AUC and the aggregation, resamples proteins for an interval, re-fetches the live CSV for the bar, and greps the attacker's code and model manifest for ClinVar/HGMD/dbNSFP/gnomAD-derived inputs. Reproducing the attacker's scores for 20 random proteins on the skeptic's machine closes the loop. CPU-only, well under an hour of compute.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/clinical_zero_shot/indels/AUC/Summary_performance_clinical_indels_AUC.csv>

## Sources

- <https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/clinical_zero_shot/indels/AUC/Summary_performance_clinical_indels_AUC.csv>
- <https://github.com/OATML-Markslab/ProteinGym>
- <https://github.com/OATML-Markslab/ProteinGym/tree/main/benchmarks>
- <https://proteingym.org/benchmarks>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Profile HMMs done properly: the listed HMM scores 0.663 because it is a plain hmmer profile. Deep, taxonomically reweighted MSAs, full forward-algorithm log-odds instead of Viterbi, family-fitted insert/delete priors and length-aware normalisation plausibly close most of the gap to the language models.
- CROSS-DOMAIN (string algorithms): score an indel as the cost of the cheapest alignment of the mutant to the family profile under affine gap penalties learned from the family's own gap statistics, with repeat-aware penalties from tandem-repeat detection - in-frame indels in repeats are the classic benign class.
- CROSS-DOMAIN (compression / MDL): normalised compression distance between the mutant sequence and the family corpus handles length changes natively, unlike substitution scorers, and costs nothing on CPU.
- CROSS-DOMAIN (statistical physics): free-energy difference in a Potts model of the family, with the deletion treated as a column removal and the insertion as an added site sampled from the family's background, gives a principled length-change energy rather than a heuristic.
- Structure-informed tolerance: AlphaFold DB models are free for these human proteins, so loop-versus-core location, predicted disorder and local packing give an indel-tolerance prior that no listed baseline uses.
- Frame and domain logic: an in-frame indel inside a disordered linker and a frame-preserving deletion of a catalytic loop are different problems; conditioning on Pfam domain boundaries and secondary-structure context is cheap and unexploited.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Label leakage: most human variant-effect tooling is trained on ClinVar, and this benchmark's labels are clinical. Any supervised pathogenicity component, or a language model fine-tuned on clinical labels, inflates AUC without advancing anything.
- Partial coverage: scoring only proteins with many variants, or only in-frame indels, then comparing to an average over the whole benchmark. The repository's aggregation must be rerun on the full set.
- No published error bar: because this CSV has no bootstrap standard-error column, differences of 0.003-0.008 can be noise; the claimant must compute and report a resampling interval over proteins, not quote the table.
- Table drift: the summary CSV is regenerated as baselines land, and the clinical substitution and clinical indel tables share model names; comparing to a cached number or to the substitutions table is a false positive.
- Frequency circularity: benign labels are partly frequency-derived, so any allele-frequency feature re-derives the label definition and must be treated as leakage.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/proteingym-clinical-indels-auc.md
```

Already set up? Say `run V3R1T4S on proteingym-clinical-indels-auc`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `proteingym-clinical-indels-auc`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
