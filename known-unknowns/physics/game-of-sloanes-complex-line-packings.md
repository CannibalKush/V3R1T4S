# Game of Sloanes: a packing of n lines in C^d (d = 3..7) with lower coherence than the live leaderboard

⚛️ **Physics** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Packing n unit vectors in C^d so that the largest overlap |<phi_j,phi_k>| (the coherence) is as small as possible is the complex analogue of Sloane's line-packing tables; optimal packings include SICs (n = d^2) and mutually unbiased bases and are used in quantum state tomography. John Jasper, Emily J. King and Dustin G. Mixon run the 'Game of Sloanes' leaderboard (arXiv:1907.07848), now on GitHub (gnikylime/GameofSloanes, last commit 2026-04-28) with 291 rows for d = 2..7 (n up to 49) plus a few sporadic rows. Each row gives the best coherence (8 decimals), a lower bound, the creator and a downloadable packing; 75 rows are marked provably optimal and 7 conjectured optimal. Recent improvements came from several groups (creator codes hlc, jrr = Roman-Roche and Roca-Jerat via frameopt, bmem = Massion and Massart, oai = ChatGPT Pro prompted by Mixon), so the table is live and contested. Example rows on 2026-10-15: (d,n) = (3,13) 0.62214387 vs lower bound 0.59160798; (3,22) 0.70342497; (4,9) 0.40185012 vs 0.39528471; (4,10) 0.41077812. For d = 2 the problem is equivalent to point packing on the Bloch sphere (the Tammes problem), already covered by spherical-code tables.

## What counts as a win

Success means n unit vectors in C^d, 3 <= d <= 7, for a (d,n) row of the live leaderboard (https://github.com/gnikylime/GameofSloanes README table, re-fetched live immediately before claiming) whose coherence mu = max_{j<k} |<phi_j,phi_k>|, computed in mpmath at 40 digits after normalising each vector, is STRICTLY LOWER (direction: min) than the listed 'Best Coherence' by at least 1e-8 (the table's resolution and the maintainers' stated acceptance threshold), the row is not marked provably optimal, mu is at least the listed lower bound (a value below it means a bug), and the vectors are given to >= 16 significant digits in the repository's file format (real parts of all vectors vector-by-vector, then imaginary parts).

## Partial wins

- **p1:** A strict improvement (same rules) for a sporadic (d,n) outside the d <= 7, n <= 49 grid where the leaderboard lists an entry, or for a d = 3..7 row that matches a known lower bound to 1e-10 (a new putatively optimal packing, reported with the bound it meets).
- **p2:** A rigorous optimality certificate (e.g. an exact SDP/LP dual or a computer-assisted proof re-checkable in under an hour) for a row not yet marked provably optimal.

## How a win is checked

Download the claimed .txt (2dn numbers), reshape as vectors[j] = re[j*d:(j+1)*d] + i*im[j*d:(j+1)*d] (this layout reproduces the posted coherences, checked on 3x13_dgm and 4x9_hlc on 2026-10-15), normalise in mpmath, compute all n(n-1)/2 overlaps, take the max. Parse the live README table row for (d,n) and compare. Also recompute the posted file for that row to make sure the comparison uses the same convention. Under a minute for n <= 49.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/gnikylime/GameofSloanes>

## Sources

- <https://github.com/gnikylime/GameofSloanes>
- <https://arxiv.org/abs/1907.07848>
- <https://www.math.colostate.edu/~king/GameofSloanes.html>
- <https://github.com/chuan97/frameopt>
- <https://www.physics.usyd.edu.au/~sflammia/SIC/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Minimise a smooth surrogate (p-frame potential or log-sum-exp of overlaps with p rising to infinity) by Riemannian L-BFGS on the product of spheres, then polish the active set of near-maximal overlaps with Newton or an SQP that equalises them.
- Import from coding theory: build structured starts from difference sets, Weyl-Heisenberg or Clifford orbits, harmonic frames (rows of DFT matrices) and unions of mutually unbiased bases, then perturb; many optimal rows are group orbits.
- Import from physics: treat lines as particles with a repulsive potential on CP^{d-1} and anneal (as in Thomson-problem work), using the Fubini-Study metric; or use the frameopt suite by Roman-Roche as a baseline.
- Remove-one-vector trick: the README conjectures that deleting one vector from an ETF or SIC gives optimal (d, n-1) packings; test analogous deletions from good n+1 packings for nearby rows.
- Target rows where the gap between best coherence and the lower bound is largest relative to neighbours (e.g. d = 6, 7 with n around 30-49), where fewer methods have been run.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Unnormalised vectors: coherence must be computed after normalising each vector; posted files may carry rounding.
- Layout mistakes: reading the file as d-major instead of vector-by-vector gives wildly wrong coherences (0.97 instead of 0.62 for 3x13).
- Improvements below 1e-8 are numerical noise by the maintainers' own rule and are not wins.
- d = 2 rows are Bloch-sphere (Tammes) packings: an improvement there would contradict long-proven or long-studied spherical codes and is almost surely a bug; and d = 2 is outside this target.
- Submitting to the leaderboard is a pull request to someone else's repository; never open one without explicit permission from your human.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/game-of-sloanes-complex-line-packings.md
```

Already set up? Say `run V3R1T4S on game-of-sloanes-complex-line-packings`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `game-of-sloanes-complex-line-packings`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
