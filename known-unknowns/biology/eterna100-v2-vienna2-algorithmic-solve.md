# Eterna100-V2 under ViennaRNA 2: an automated RNA design algorithm that solves a puzzle no benchmarked algorithm has solved

🦠 **Biology** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

The Eterna100 is the standard benchmark for RNA inverse folding: for each of 100 target secondary structures, find a sequence whose minimum-free-energy fold is exactly that structure. Koodli, Rudolfs, Romano, Wayment-Steele, Dunlap, Eterna participants and Das redesigned it as Eterna100-V2 for the ViennaRNA 2 energy model, and the eternagame/eterna100-benchmarking repository (last pushed 2026-09-01) publishes per-trial results for RNAinverse, NEMO, DesiRNA, SentRNA, LEARNA and EternaBrain. In data/results.tsv, under Vienna 2 the best algorithm (DesiRNA) solves 92 of the 100 V2 targets, and seven V2 puzzles are solved by no benchmarked algorithm in any trial: #68 Taraxacum officinale, #71 Variation of a crop circle, #79 Shapes and Energy, #86 Methaqualone, #90 Gladius, #99 Shooting Star, #100 Teslagon (the puzzles file ships a Sample Solution (V2/Vienna2) for every V2 target, which a claimant should fold with stock RNAfold to confirm designability of that specific target before attacking it; Tianshuo Zhou, Wei Yu Tang, David Mathews and Liang Huang, arXiv:2402.17206, prove 18 Eterna100 puzzles undesignable under the Turner model in ViennaRNA, including #86, #90 and #99 - but for their V1 structures, and all three are among the 19 puzzles whose V2 structure differs from V1, so the V2 targets are not covered by that proof). A sequence for any one of them, produced de novo by an automated method, is a clean, instantly checkable result.

## What counts as a win

An automated design program (code released, deterministic given a logged seed) that, given only the dot-bracket target of an Eterna100-V2 puzzle that has no Success=1 row under folder vienna2 in data/results.tsv of github.com/eternagame/eterna100-benchmarking (re-fetched live immediately before claiming), outputs a sequence whose MFE structure from stock ViennaRNA 2.6.4 (or 2.1.9) RNAfold -T 37 with no other flags is EXACTLY the target, within 24 hours on a laptop. The program must not read the Eterna sample solutions, any human player solution, or any sequence database of Eterna designs, and the NOVELTY check must confirm no published algorithm (e.g. SAMFEO, Zhou et al.; Tang et al. arXiv:2412.08751; Gautam et al. arXiv:2602.12470) already reports solving that puzzle under Vienna 2.

## Partial wins

- **p1:** One of the seven listed puzzles solved de novo under the full criterion.
- **p2:** A single frozen algorithm that solves more Eterna100-V2 targets under Vienna 2 than DesiRNA's 92 (all solutions verified with stock RNAfold), even if it misses the seven hardest.
- **p3:** A machine-checkable undesignability certificate for one of the seven V2 targets under Vienna 2, produced with the released RNA-Undesign code (github.com/shanry/RNA-Undesign), would itself be a result - and would retire that target.

## How a win is checked

Skeptic installs ViennaRNA 2.6.4 (not preinstalled on a typical laptop), folds the claimed sequence with stock ViennaRNA 2.6.4 'RNAfold -T 37.0' (no other flags) and compares the dot-bracket string character by character with the target from data/eterna100_puzzles.tsv (seconds). Then re-runs the released program from the logged seed in a clean environment without network access or Eterna solution files and confirms it reproduces a valid design. Checks the NOVELTY literature for per-puzzle results.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/eternagame/eterna100-benchmarking>

## Sources

- <https://github.com/eternagame/eterna100-benchmarking>
- <https://raw.githubusercontent.com/eternagame/eterna100-benchmarking/master/data/results.tsv>
- <https://raw.githubusercontent.com/eternagame/eterna100-benchmarking/master/data/eterna100_puzzles.tsv>
- <https://daslab.stanford.edu/assets/pdfs/Koodli_et_al_Eterna100V2_bioRxiv_2025.pdf>
- <https://arxiv.org/abs/2402.17206>
- <https://arxiv.org/abs/2606.07562>
- <https://github.com/shanry/RNA-Undesign>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Decompose and conquer: split the target at multiloops into independent substructures, design each with local constraints, then repair junction conflicts with constrained RNAinverse or a CP-SAT model of base-pair compatibility.
- Ensemble-objective optimisation (SAMFEO-style): maximise the Boltzmann probability of the target or minimise ensemble defect with sampled coordinate moves, then polish for exact MFE; ViennaRNA's Python bindings make each evaluation milliseconds.
- Cross-domain import (VLSI routing / constraint satisfaction): encode 'target is MFE' lazily as cutting planes. Each time RNAfold returns a rival structure, add a constraint that the target beats that rival, and re-solve with a MaxSAT or ILP solver over sequence choices (counterexample-guided synthesis).
- Cross-domain import (protein design): negative design via explicit rival-structure enumeration (RNAsubopt) and boosting GC-closing pairs and loop mismatches that destabilise the specific rivals, as Eterna players do with 'boosts'.
- Study the human solutions' motif statistics WITHOUT copying them (e.g. which loop-closing pairs players favour) only from puzzles OUTSIDE the target set, and turn them into priors for the search.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Wrong energy model: loading Turner 1999 parameters into ViennaRNA 2.x leaves dangles=2 and is neither benchmark (the repository README warns this is more permissive). Use stock RNAfold 2.6.4 or 2.1.9 with no flags for Vienna 2.
- V1 vs V2 targets: several puzzles differ between Eterna100-V1 and -V2; solving the V1 structure under Vienna 2 does not count for V2. Use the 'Secondary Structure V2' column.
- Copying or seeding from the public 'Sample Solution' columns, Eterna player solutions or any database of Eterna designs is not an algorithmic solve.
- Degenerate MFE: if the target ties with another structure, RNAfold's traceback decides; the check is the exact string RNAfold returns, not an energy tie.
- Novelty: results.tsv covers only six algorithms. Huang-lab methods (SAMFEO and successors) report strong Eterna100 numbers; check their per-puzzle tables before claiming a first. Tristan Cazenave's Montparnasse (arXiv:2606.07562) reports solving all 100 Eterna100 V1 puzzles under Turner 1999 / Vienna 1 (#100 Teslagon in 9,383 s, #90 Gladius the hardest); that does not move this V2/Vienna 2 bar, but a claim must check whether Montparnasse or a successor has since been run on V2.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/eterna100-v2-vienna2-algorithmic-solve.md
```

Already set up? Say `run V3R1T4S on eterna100-v2-vienna2-algorithmic-solve`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `eterna100-v2-vienna2-algorithmic-solve`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
