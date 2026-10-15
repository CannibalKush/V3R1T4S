# Dzugutov, modified-Dzugutov and Z1/Z2 clusters: lower a putative global minimum in the Doye-Wales polytetrahedral tables

⚪ **Packings and physics** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Jonathan Doye, David Wales and Sergei Simdyankin (Faraday Discuss. 2001) and Doye-Wales (PRL 2001) found putative global minima of clusters bound by the Dzugutov pair potential (N <= 100) and a modified Dzugutov potential (N <= 250); Doye, Wales, Fredrik Zetterling and Mikhail Dzugutov (JCP 2003) did the same for the Z1 and Z2 potentials (N <= 80). These glass-former potentials favour non-compact polytetrahedral structures with very rough, multi-funnel landscapes; the minima were found by seeded basin hopping in one campaign and the CCD invites improvements. No later systematic re-search was found (search 2026-10-13).

## What counts as a win

Success means coordinates for N particles such that E* under the exact pair potential of that table (Dzugutov 1992 form with the published constants, the modified form, or Z1/Z2; calibrated by reproducing ten posted point-file energies to 1e-6) is STRICTLY LOWER (direction: min) by at least 1e-4 than the live table energy for (potential, N) re-fetched immediately before claiming, AND than any value found by an arXiv/Google Scholar search for that potential's clusters; AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 in reduced units, then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue; AND polishing the posted point file gives an energy at least 1e-4 higher.

## Partial wins

- **p1:** A certified improvement for the modified-Dzugutov potential at N in 101..250 (the largest, least-revisited range) counts as the primary realistic win; report it with the structural motif (icosahedral network type).
- **p2:** Audit: any posted point file whose energy is not reproduced to 1e-6 or that polishes lower by > 1e-4.

## How a win is checked

Checker (< 10 min): curl the live table; parse; compute the pair energy with the smooth cutoff exactly as in the potential definition page; polish; Hessian; polish the posted structure; assert margins.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Dzugutov.html>

## Sources

- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Dzugutov.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Dzugutov/table.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/mDzugutov/table.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Dzugutov/potential.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Dzugutov/points/all.tar>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/table.html>
- <https://arxiv.org/abs/cond-mat/0011018>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Build structures as networks of interpenetrating 13-atom icosahedra (the motif Doye et al. identified) combinatorially: enumerate linear, ring and 3D network topologies of icosahedral units for each N and relax, instead of random starts.
- Import from quasicrystal and Frank-Kasper phase crystallography: carve clusters from the sigma, A15, C15 and dodecagonal approximant phases that Dzugutov's potential is known to stabilise in bulk.
- Import from graph theory: the disclination network of a polytetrahedral cluster is a graph; search over disclination graphs (as in the Nelson / Frank-Kasper description) as a discrete outer loop with continuous relaxation inside.
- Cross-potential seeding: relax every Z1/Z2 minimum under Dzugutov and vice versa, and every Dzugutov minimum under the modified form for N <= 100.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The Dzugutov potential has a smooth cutoff and a repulsive hump; implementing it without the exact cutoff function or constants gives slightly different energies that can masquerade as improvements. Calibrate first.
- Original and modified Dzugutov tables are different potentials; never compare across them.
- Very flat, rough landscapes: many near-degenerate minima differ by < 1e-4; the margin and distinct-basin rules are mandatory.
- Saddle points: L-BFGS can stop at index-1 saddles on these landscapes; the Hessian check is required.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/packings-physics/ccd-dzugutov-zetterling-polytetrahedral-clusters.md
```

Already set up? Say `run V3R1T4S on ccd-dzugutov-zetterling-polytetrahedral-clusters`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ccd-dzugutov-zetterling-polytetrahedral-clusters`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
