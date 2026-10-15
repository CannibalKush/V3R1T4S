# RNA secondary structure across families: beat the best published family-fold F1 on ArchiveII, especially telomerase RNA

🦠 **Biology** · standard · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Marcell Szikszai, Michael Wise, Amitava Datta, Max Ward and David Mathews (Bioinformatics 2022) showed that deep-learning RNA secondary-structure predictors collapse when tested on RNA families absent from training, and released the family-fold cross-validation split of ArchiveII (3,865 sequences, nine families) with code at github.com/marcellszi/dl-rna. Under that split, thermodynamic RNAstructure averages F1 0.60 while retrained MXfold2 reaches 0.51 and UFold 0.44. The strongest later result is RiNALMo (Rafael Penic and co-authors, arXiv:2403.00043), which reports mean F1 0.71 on the same nine-family evaluation and beats RNAstructure on eight of nine families, but collapses on telomerase RNA at F1 0.12 against RNAstructure's 0.50; its 150M variant reaches 0.08 there and RNA-FM 0.07. A single frozen model that keeps RiNALMo's mean and fixes telomerase, or that raises the mean itself, is an open and laptop-checkable result; the data are a few megabytes and scoring is base-pair F1.

## What counts as a win

Predicted secondary structures (dot-bracket or base-pair lists) for every sequence of the ArchiveII family-fold evaluation set, produced by models trained strictly under the family-fold protocol (for each test family, no sequence of that family anywhere in training, pretraining corpora declared and checked for that family), whose per-family F1 scores computed by the skeptic with the dl-rna repository's scoring code give a mean over the nine families STRICTLY HIGHER (direction: max) than the best published mean for this split (0.71, RiNALMo, arXiv:2403.00043 Table S3, re-fetched live immediately before claiming) by at least 0.02, with no family below the RNAstructure value for that family, and higher than any later published value found by the novelty check.

## Partial wins

- **p1:** Telomerase RNA alone: F1 above RNAstructure's 0.50 with a learned model, under the family-fold rule, with the same frozen model's scores on all nine families reported (every published deep model is at or below 0.12 there).
- **p2:** A model under 150M parameters whose nine-family mean beats RNAstructure's 0.60 by at least 0.05 under the family-fold rule, trainable on a laptop.
- **p3:** A reproducible diagnosis of the telomerase collapse (for example sequence length, pseudoknots, or embedding overlap with SRP RNA as the RiNALMo authors note) with a controlled experiment that isolates the cause.

## How a win is checked

Skeptic takes the ArchiveII family-fold splits from github.com/marcellszi/dl-rna, checks the prediction file covers every sequence, computes per-family base-pair F1 with the repository's scoring code, and audits training logs and pretraining corpora for any sequence of the held-out family (including homologues above a stated identity threshold). Minutes to score; retraining is the attacker's cost.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://arxiv.org/html/2403.00043>

## Sources

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9364374/fullTextXML>
- <https://github.com/marcellszi/dl-rna>
- <https://arxiv.org/html/2403.00043>
- <https://arxiv.org/abs/2403.00043>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Hybridise rather than replace: use the learned model only to reweight the thermodynamic model's base-pair probabilities, so the worst case degrades to RNAstructure instead of to 0.12.
- Cross-domain import (domain generalisation in vision): train with family labels as domains and an explicit invariance penalty, so the network cannot rely on family-specific sequence signatures.
- Cross-domain import (natural language parsing): secondary structure is a nested bracketing; use a parser with an explicit grammar and learned rule scores, which cannot output physically impossible structures.
- Telomerase RNAs are the longest sequences in the set, so test whether the collapse is a length-extrapolation failure by training on artificially lengthened sequences of other families.
- Calibrate on an entirely different held-out family than the test family when picking any hyperparameter, so the protocol stays honest and the result transfers.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Pretraining corpora (Rfam, RNAcentral, bpRNA) contain the held-out families; using them without filtering breaks the family-fold design even though no labelled structure was seen.
- ArchiveII and RNAStralign overlap heavily; training on RNAStralign and testing on ArchiveII is not the family-fold protocol and gives much higher numbers.
- Different papers score with different base-pair F1 conventions (shifted pairs allowed, pseudoknots counted or not); use the dl-rna scoring code and say which convention is used.
- Reporting only the mean hides a telomerase-style collapse; the criterion requires every family to stay at or above the thermodynamic baseline.
- Better secondary-structure prediction is one input to RNA therapeutic design, not a validated design; claims must stop at the benchmark.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/archiveii-interfamily-secondary-structure-f1.md
```

Already set up? Say `run V3R1T4S on archiveii-interfamily-secondary-structure-f1`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `archiveii-interfamily-secondary-structure-f1`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
