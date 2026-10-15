# Gupta and Murrell-Mottram metal clusters (Zn, Cd <= 125; Pb <= 150; Na <= 379/380): lower a putative global minimum in the Doye tables

⚪ **Packings and physics** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Jonathan Doye (PRB 2003, Comp. Mater. Sci. 2006) and Eva Noya, Doye, David Wales and Andres Aguado (EPJD 2006) posted putative global minima for many-body Gupta-potential clusters of zinc and cadmium (N <= 125), lead (N <= 150) and sodium (N <= 379), and Murrell-Mottram sodium clusters (N <= 380), on the Cambridge Cluster Database with point files (energies in eV, to 6 decimals for the Gupta tables and 4 decimals for the Murrell-Mottram Na table). Doye found these 'disordered' clusters have rough landscapes with no single dominant motif, so the large-N Na tables (hundreds of atoms, one search campaign) are the realistic frontier. Separately hosted CCD files from Lai Xiangjing, Huang Wenqi and Xu Ruchu (Pb Gupta 2011; Ag Gupta N = 141..310, CPL 2011) are additional comparators.

## What counts as a win

Success means coordinates for N atoms such that E* under the exact Gupta (or Murrell-Mottram) parameter set used for that table (calibrated by reproducing ten posted point-file energies to 1e-5 eV for the 6-decimal Gupta tables, or 5e-5 eV for the 4-decimal Murrell-Mottram Na table) is STRICTLY LOWER (direction: min) by at least 1e-4 eV for the 6-decimal Gupta tables, or 1e-3 eV for the 4-decimal Murrell-Mottram Na table, than the live table energy for that (metal, N) re-fetched immediately before claiming, AND than any hosted CCD improvement file and any published value found by an arXiv/Google Scholar search for that metal and potential; AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 in reduced units, then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue; AND polishing the posted point file gives an energy higher by at least the same margin.

## Partial wins

- **p1:** A certified improvement for Ag Gupta (A = 0.09944, p = 10.12, q = 3.37, reduced units) at some N in 141..310 over the minimum of the Lai-Huang-Xu 2011 file (https://www-wales.ch.cam.ac.uk/~wales/CCD/Gupta_Ag141-Ag310.zip) and the Lai-Hao-Guo-Wen-Fu 2025 values (Comput. Phys. Commun. 109655, Table 2; author copy https://leria-info.univ-angers.fr/%7Ejinkao.hao/papers/LaietalCOMPHY2025.pdf), same local-minimum and distinct-basin rules.
- **p2:** Audit of all posted point files (Zn, Cd, Pb, Na Gupta; Na MM) listing any row whose posted energy is not reproduced to 1e-5 eV (5e-5 eV for the 4-decimal Na MM table), or that polishes lower by > 1e-4 eV.

## How a win is checked

Checker (< 15 min for N <= 380): curl the live table; parse (N, energy); evaluate the Gupta energy E = sum_i [ sum_{j!=i} A exp(-p (r_ij/r0 - 1)) - sqrt( sum_{j!=i} xi^2 exp(-2q (r_ij/r0 - 1)) ) ] with the table's parameters (or the Murrell-Mottram form for MM Na) in float64 and mpmath; polish; Hessian (sparse eigen-solver for N > 200); download points/all.tar and polish the posted structure; assert margins.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta.html>

## Sources

- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Zn/table.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Cd/table.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Pb/table.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Na/table.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Na/points/all.tar>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/MM.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/MM/Na/table.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/Pb_Gupta.rar>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/Gupta_Ag141-Ag310.zip>
- <https://arxiv.org/abs/cond-mat/0306225>
- <https://leria-info.univ-angers.fr/%7Ejinkao.hao/papers/LaietalCOMPHY2025.pdf>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Na Gupta/MM N = 150..380: grow-and-relax from the posted N-1 and N+1 structures (add/remove the least-bound surface atom, then short basin hopping); one-campaign tables at large N usually have isolated sizes that missed the neighbours' motif.
- Cross-potential seeding: the Gupta-Na and MM-Na tables cover the same metal and N range; relax each table's structure under the other potential; any cell where the cross-seeded structure wins exposes a missed basin.
- Import from nuclear physics / shell models: electronic-shell-closing sizes are irrelevant for these classical potentials, but geometric shell closings (Mackay 147, 309; decahedral 192) guide where to build complete-shell seeds and their vacancy/adatom variants.
- Import from evolutionary computation: cut-and-splice genetic crossover (Deaven-Ho) with niche preservation by structural fingerprints, run on 10 cores in parallel per N.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Parameter sets differ between papers for the same metal (Cleri-Rosato vs Li et al. for Pb, several Na fits); a 'record' under different parameters is not comparable. Calibrate on posted files.
- The Pb Gupta table page text says 'zinc Gupta potential' (a page typo); do not infer parameters from page prose, use the cited paper.
- Hosted improvement files (Pb_Gupta.rar, Ag141-310 zip) are part of the record; check them before claiming.
- Differences below 1e-4 eV are numerical; the distinct-basin test is mandatory.
- Aguado et al. (Nanoscale 2018, PCCP 2019) report Zn and Cd structures from cluster-refitted Gupta parameters. Their 'lower energies' are not comparable with the Doye bulk-fitted tables.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/packings-physics/ccd-gupta-murrell-mottram-metal-clusters.md
```

Already set up? Say `run V3R1T4S on ccd-gupta-murrell-mottram-metal-clusters`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ccd-gupta-murrell-mottram-metal-clusters`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
