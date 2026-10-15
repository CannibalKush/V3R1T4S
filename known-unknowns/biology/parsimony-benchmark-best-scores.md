# Maximum parsimony: a tree with fewer steps than the best-known score on a classic benchmark alignment

🦠 **Biology** · standard · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Large classic phylogenetic alignments (Zilla 500-taxon rbcL, RDPII, ARB, PROTO) and the MPBoot TreeBASE/PANDIT benchmark collection have published best-known Fitch parsimony scores from PTM, TNT, PAUP* and MPBoot (e.g. Zilla best known 16218 steps (PTM), PAUP* 16221, TNT 16219, per Table 2 of Kevin Sundberg, Mark Clement, Quinn Snell, Dan Ventura, Michael Whiting and Keith Crandall, BMC Bioinformatics 13(S13):S8; in that table the PROTO row's two scores, 162,438 and 810,231, belong to different datasets, so read the column alignment carefully). Find an unrooted binary tree with strictly fewer parsimony steps than the best published score for any such public alignment.

## What counts as a win

A Newick tree over exactly the taxa of a public benchmark alignment (from the MPBoot zenodo data or the dataset cited in https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3426809/fullTextXML (Table 2)) whose Fitch (unordered, equal-weight, gaps treated as the publication specifies) parsimony score, computed by two independent implementations (our checker and TNT or PAUP*-free equivalent such as MPBoot/RAxML-NG --evaluate parsimony), is strictly lower than the best published score for that dataset, both tables re-fetched live immediately before claiming, and lower than any post-2012 score found by a novelty search.

## Partial wins

- **zilla-16218-tie:** Reach 16218 on Zilla from random starting trees with open tools within laptop-hours (TNT reportedly stopped at 16219).
- **mpboot-dataset-improvement:** Strictly beat the MPBoot-reported best score on any one TreeBASE dataset from the zenodo supplementary data.

## How a win is checked

Fitch algorithm checker in Python (O(taxa x sites)), cross-checked with a second implementation; must first reproduce a published score from a published tree. Minutes.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3426809/fullTextXML>

## Sources

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3426809/fullTextXML>
- <https://zenodo.org/records/1156452>
- <https://arxiv.org/abs/1306.1339>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- TNT 'new technology' search (sectorial search, ratchet, drift, tree fusing) with many replicates on 10 cores.
- MPBoot / IQ-TREE-style stochastic NNI+SPR with perturbation, then TBR polish.
- Cross-domain import (TSP/VRP metaheuristics): treat SPR/TBR as large-neighbourhood ruin-and-recreate (as in HGS-CVRP) with genetic crossover of trees by subtree-prune-and-graft fusion.
- Cross-domain import (Steiner tree / VLSI): parsimony is the Steiner tree in Hamming space; use Steiner-point heuristics (Lin-Kernighan style edge swaps) and ILP on small sectors.
- Exact sector solving: extract 15-25 taxon sectors and solve them optimally with branch and bound, reinsert.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Gap/missing-data treatment and character weighting change the score; reproduce a published score first with the same convention.
- The PTM 16218 vs 16234 discrepancy across two tables shows settings differ; compare like with like.
- Static 2012-2018 tables: newer TNT runs may already have beaten them; novelty search required.
- Datasets must be the exact published alignment (taxon count, site count); downloading a different version of 'Zilla' invalidates the comparison.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/parsimony-benchmark-best-scores.md
```

Already set up? Say `run V3R1T4S on parsimony-benchmark-best-scores`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `parsimony-benchmark-best-scores`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
