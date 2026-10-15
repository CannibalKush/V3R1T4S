# (NaCl)_N Cl- cluster anions (N <= 35, Tosi-Fumi Coulomb plus Born-Mayer and Welch potentials): lower a putative global minimum in the Doye-Wales table

⚪ **Packings and physics** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Jonathan Doye and David Wales (Phys. Rev. B 59, 2292, 1999) tabulated putative global minima of (NaCl)_N Cl- for N = 1..35 under two potentials: a rigid-ion Coulomb plus Born-Mayer (Tosi-Fumi) model and the polarizable Welch potential. The Cambridge Cluster Database table (dated 1997) gives energies in eV to 3 decimals with point files in bohr (all.tar). Ionic clusters have rock-salt cuboid minima with competing column and sheet structures, so the landscape has many near-degenerate funnels. No later paper reporting lower energies for these exact potentials was found (searches 2026-10-15). Because the table rounds to 1 meV, a new minimum must be recomputed from coordinates and differ by a real margin. Checked live 2026-10-15: table page HTTP 200.

## What counts as a win

Success means Cartesian coordinates of N Na+ and N+1 Cl- ions (N in 1..35) such that E* under the Coulomb plus Born-Meyer potential exactly as in Doye-Wales 1999 (calibrated first: the checker reproduces the 3-decimal posted energies of every C+BM point file and agrees to 1e-8 eV with its own evaluation of the posted coordinates) is STRICTLY LOWER (direction: min) by at least 2e-3 eV than the checker's own evaluation of the posted C+BM structure for that N, polished, AND than the table value re-fetched live immediately before claiming, AND than any published value for the same potential found by an arXiv / Google Scholar search for '(NaCl)nCl- global minima'; AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 (reduced units of the table), then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue.

## Partial wins

- **p1:** The same certified improvement (margin 2e-3 eV, same checks) for the Welch polarizable potential column, using a checker that solves the induced dipoles self-consistently and reproduces every posted Welch point file to 1e-3 eV.
- **p2:** A certified C+BM putative global minimum for N in 36..60, with the structure type (cuboid, column, sheet) and the full lowest-10 list, against a fetchable published comparator if any exists; a literature frontier, not a table record.

## How a win is checked

Checker (< 5 min): curl the live table; parse the C+BM and Welch columns; download all.tar (coordinates in bohr); evaluate E = sum_{i<j} [ q_i q_j / r_ij + A_ij exp(-r_ij / rho) ] with the Tosi-Fumi parameters of Doye-Wales 1999 (arXiv cond-mat/9801152) in float64 and mpmath; calibration on all posted files; polish; Hessian (6 zero modes, none negative); polish the posted structure; assert margins.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/NaCl/table.html>

## Sources

- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/NaCl.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/NaCl/table.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/NaCl/points/all.tar>
- <https://arxiv.org/abs/cond-mat/9801152>
- <https://arxiv.org/abs/cond-mat/9905407>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Crystallographic enumeration: generate every rock-salt cuboid, cuboid-with-adatom and cuboid-with-vacancy arrangement with 2N+1 ions and charge -1 exhaustively (a finite lattice-animal enumeration), relax all, then basin-hop only from the best few.
- Mineralogy import: include hexagonal (wurtzite-like and h-BN-like sheet) and stacked-ring motifs known from (NaCl)_n DFT studies; the ionic model can favour them at small N.
- Charge-ordering moves: swap a Na+/Cl- pair or move the excess Cl- to a corner, edge or face site; the extra-anion position drives many of the near-degenerate funnels.
- Electrostatics import: use Ewald-free fast multipole or exact pair sums with compensated summation so 1e-8 eV comparisons are reliable.
- Graph-theory import: canonicalise relaxed structures by their nearest-neighbour graph to avoid re-exploring isomorphic minima.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Table energies are rounded to 1 meV; any claim within 2 meV of the table is indistinguishable from rounding and must be judged against the checker's own evaluation of the posted coordinates.
- Units: coordinates are in bohr and energies in eV; mixing bohr and angstrom in the Born-Mayer exponent produces huge fake 'improvements'.
- The Welch potential includes polarization; evaluating Welch structures with the rigid-ion C+BM model (or vice versa) is not comparable.
- Wrong total charge: a claim must have exactly N Na+ and N+1 Cl-; a neutral or doubly charged cluster is a different problem.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/packings-physics/ccd-nacl-cluster-anions-born-mayer.md
```

Already set up? Say `run V3R1T4S on ccd-nacl-cluster-anions-born-mayer`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ccd-nacl-cluster-anions-born-mayer`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
