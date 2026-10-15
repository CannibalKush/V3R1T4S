# Protein Engineering Tournament pilot (zero-shot track): beat the best team score on an unseen enzyme

🦠 **Biology** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

In the zero-shot in-silico track of the pilot Protein Engineering Tournament (Armer, Kane, Cortade, Redestig, Estell, Yusuf, Rollins, Spinner, Marks, Brunette, Kelly, DeBenedictis; Proteins 2025), teams received only sequences and had to rank variants of three enzymes with no training data. The published board (doc/zero-shot-board.csv) shows how hard this is: on alpha-amylase the best average Spearman is 0.401 (marks-lab) and one team is at -0.261; on aminotransferase the best is 0.163 (marks-lab) with another team at -0.283; on the xylanase classification event the best weighted F1 is 0.641 with accuracy 0.567 (marks-lab), against five submissions. Evaluation data with measured values and the scoring notebook are public in the repository, so the bar is reproducible offline. Ranking variants of an enzyme nobody has assayed is the core capability claimed for protein language models, and on this release they are close to useless on two of three events.

## What counts as a win

Scores for every variant in a zero-shot event's evaluation file, produced by a method that reads none of that event's measured values at any stage (no threshold, sign or hyperparameter fitted on them), whose average Spearman (or weighted F1 and accuracy for the xylanase event), recomputed by the skeptic with the repository's evaluation.ipynb, is STRICTLY HIGHER (direction: max) than the best team value for that event in doc/zero-shot-board.csv (re-fetched live immediately before claiming) by at least 0.05, with the same frozen method applied to all three zero-shot events and all results reported.

## Partial wins

- **p1:** Aminotransferase: average Spearman above 0.30 (best team value 0.163 as of 2026-10-15) with a frozen zero-shot method, on an event where two of four teams scored at or below zero.
- **p2:** One frozen method that is above zero on all three events and beats the best team on at least one, which no participant achieved.
- **p3:** A reproducible comparison of scoring conventions for multi-mutant variants (masked marginals, wild-type marginals, whole-sequence likelihood) on these events, showing how much of the published spread between teams is convention rather than model.

## How a win is checked

Skeptic clones the repository, checks the score file covers every evaluation row, runs the event's cells in in_silico_zero-shot/evaluation.ipynb, confirms from the code that the measured-value columns were never read, and compares with doc/zero-shot-board.csv. Minutes.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://raw.githubusercontent.com/the-protein-engineering-tournament/pet-pilot-2023/main/doc/zero-shot-board.csv>

## Sources

- <https://github.com/the-protein-engineering-tournament/pet-pilot-2023>
- <https://raw.githubusercontent.com/the-protein-engineering-tournament/pet-pilot-2023/main/doc/zero-shot-board.csv>
- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12517241/fullTextXML>
- <https://arxiv.org/abs/2309.09955>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Negative Spearman for several teams suggests sign and convention errors rather than no signal; fix the convention first, using an unrelated public deep mutational scan to choose it, and see how much of the gap closes.
- Cross-domain import (ensemble forecasting): average the ranks of several independent weak predictors (alignment conservation, a small language model, a biophysical stability estimate) rather than trusting one model, which is standard practice where individual skill is low.
- Cross-domain import (structural engineering): score mutations by predicted change in packing and electrostatics around the catalytic residues, which is mechanistic and needs no training data.
- These are industrial enzymes with large natural families; build a family alignment from public sequence databases and use covariation, which is often stronger than a general-purpose model for one protein.
- The xylanase event is classification rather than correlation; calibrating a continuous score into classes without peeking at labels is itself the hard part and can be done on an unrelated assay.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Using the supervised track's training data for the same or a homologous enzyme makes the method not zero-shot; the tracks share organisms and must be kept separate.
- Fitting the sign of the correlation on the event's own values is the most common invisible leak here and would explain large apparent gains.
- The three events use two different metrics; a claim must use the metric the board uses for that event.
- Test sets are small (roughly a hundred to a few thousand variants), so differences below 0.05 Spearman are not meaningful.
- Winning a ranking event does not mean the top-ranked designs work: in the tournament's in-vitro round, many submitted designs failed expression or stability screens.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/protein-engineering-tournament-zeroshot-spearman.md
```

Already set up? Say `run V3R1T4S on protein-engineering-tournament-zeroshot-spearman`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `protein-engineering-tournament-zeroshot-spearman`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
