# Rigid-water clusters (TIP4P, TIP5P): lower a putative global minimum for (H2O)_N, N <= 21 on the CCD, or beyond against published values

⚪ **Packings and physics** · standard · tractability ★☆☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

The Cambridge Cluster Database lists putative global minima of (H2O)_N for the rigid TIP4P model (David Wales and Mark Hodges, CPL 1998; N = 2..21) and TIP5P (Tim James, Wales and Javier Hernandez-Rojas, CPL 2005; N = 2..21), with xyz files and energies in kJ/mol (5 and 4 decimals). These small sizes have been confirmed by several independent searches (for example Kabrede and Hentschke, and later graphite-substrate studies that reproduce the same TIP4P minima), so beating N <= 21 is a long shot; the open frontier is N >= 22, where published putative minima exist only in papers (no live table). Hydrogen-bond topology (proton disorder) makes the landscape combinatorial on top of the geometric one.

## What counts as a win

Success means rigid-molecule coordinates for N waters (N <= 21) such that E* under the exact TIP4P (Jorgensen 1983) or TIP5P (Mahoney-Jorgensen 2000) parameters, no cutoff, rigid monomer geometry preserved to 1e-6 A, computed by a checker calibrated on ten posted xyz files (reproduce to 1e-4 kJ/mol), is STRICTLY LOWER (direction: min) by at least 1e-3 kJ/mol than the live CCD value for (model, N) re-fetched immediately before claiming and than any published value for that N and model; AND it is a certified rigid-body local minimum (gradient < 1e-6 kJ/mol/A in rigid-body coordinates; rigid-body Hessian with 6 zero modes and no negative eigenvalues); AND polishing the posted structure gives an energy at least 1e-3 kJ/mol higher.

## Partial wins

- **p1:** A certified TIP4P or TIP5P minimum for some N in 22..40 lower than a specific fetchable published value (DOI/arXiv plus table reference) for the same model; a literature frontier, not a table record.
- **p2:** A certified improvement on the CCD water-Li+ or water-Ca2+ tables (https://www-wales.ch.cam.ac.uk/~wales/CCD/water_cation/gmin.html; CPL 2005), using exactly the potential defined in that paper.

## How a win is checked

Checker (< 10 min): curl the live page; parse; rebuild molecules as rigid bodies (check O-H 0.9572 A, HOH 104.52 deg; TIP5P lone-pair sites); evaluate Coulomb + O-O LJ exactly; rigid-body polish and Hessian; polish posted xyz; margins.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www-wales.ch.cam.ac.uk/~wales/CCD/TIP4P-water.html>

## Sources

- <https://www-wales.ch.cam.ac.uk/~wales/CCD/TIP4P-water.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/TIP4P/xyz/TIP4P-21.xyz>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/TIP5P_ccd_page/TIP5P.html>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/TIP5P_ccd_page/structures/TIP5P_global_minima.tar.gz>
- <https://www-wales.ch.cam.ac.uk/~wales/CCD/water_cation/gmin.html>
- <https://www-wales.ch.cam.ac.uk/pdf/CPL.412.23.2005.pdf>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Two-level search: enumerate oxygen frameworks (stacked pentagonal/cubic prisms, cages) then solve the proton-arrangement problem exactly over the ice-rule-satisfying orientations of each framework (a constrained discrete optimisation), before rigid-body relaxation.
- Import from statistical physics of ice: use Pauling ice-rule graph enumeration (loop moves on the hydrogen-bond digraph) to explore proton disorder exhaustively for N <= 30.
- Import from crystallography: carve clusters from clathrate hydrate cages (5^12, 5^12 6^2) for N = 20..40; these are known competitors for TIP4P.
- Use the TTM2-F vs TIP4P disagreement at N = 17 and 21 (reported in 2024 work) as a hint of near-degenerate funnels where re-seeding across models may expose missed TIP4P basins.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Model variants (TIP4P vs TIP4P/2005 vs TIP4P-Ew; TIP5P vs TIP5P-E) have different parameters; only the original models are on the CCD.
- The CCD notes a published 'new' (H2O)10 minimum (Lee, Suh, Kim 2001) that was an error later retracted; recompute from coordinates.
- Flexible-monomer relaxations lower energies artificially; monomers must stay rigid.
- Cutoffs or Ewald-style corrections change energies; clusters use the full unscreened sum.
- Papers that re-optimise TIP4P candidates with DFT (for example arXiv:2411.00754) report 'lower than CCD' energies in hartree at the DFT level. They are not TIP4P records and are no evidence that the CCD TIP4P table is beaten.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/packings-physics/ccd-water-clusters-tip4p-tip5p.md
```

Already set up? Say `run V3R1T4S on ccd-water-clusters-tip4p-tip5p`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ccd-water-clusters-tip4p-tip5p`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
