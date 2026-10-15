# Monomer-dimer constant of the square lattice: more than the 11-12 decimals published by Kong (2006)

⚛️ **Physics** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

The monomer-dimer entropy h2 of the square lattice (log of the number of matchings per site of the n x n grid as n grows; Hosoya index growth, OEIS A028420 counts the finite boards) has no closed form. Baxter's 1968 heuristic gave e^h2 = 1.940215351; Shmuel Friedland and Uri Peled (Adv. Appl. Math. 2005, arXiv math/0402009) certified 8 decimals; Yong Kong (Phys. Rev. E 74 (2006) 061102, arXiv cond-mat/0610690) maximised fixed-density entropies to get h2 = 0.662798972834 with bracket 0.662798972831 < h2 < 0.662798972845 ('11 correct digits'); Paolo Butera, Paul Federbush and Marco Pernici (arXiv 1305.7028, 2013) give 0.662798972(1) from series. No OEIS entry holds the digits of h2 (search checked 2026-10-15) and Steven Finch's 2020-2024 errata quote only 0.66279897.... At unit monomer activity the model has no phase transition (Heilmann-Lieb) and correlations decay exponentially, so high-precision CTM or boundary-MPS methods should give many more digits on a laptop.

## What counts as a win

Success means a decimal value of h2 (natural log, per site) with at least 20 decimals such that (a) two independent methods agree on all claimed decimals (for example CTM or VUMPS on the monomer-dimer transfer operator, and exact strip transfer matrices of width up to about 24 with extrapolation), (b) the value lies inside Kong's bracket [0.662798972831, 0.662798972845] and agrees with 0.662798972834 to its 12 decimals up to final-digit rounding, (c) the digits are stable over at least three truncation increases, and (d) an arXiv/Google Scholar/OEIS search, re-run immediately before claiming, finds no published value with as many decimals. Direction: more digits.

## Partial wins

- **p1:** A rigorous enclosure of h2 certifying at least 12 decimals (improving Friedland-Peled's 8 certified decimals and making Kong's bracket rigorous or not), via Friedland-Peled transfer-matrix inequalities evaluated in exact or interval arithmetic with published certificate vectors.
- **p2:** At least 15 decimals, by two independent methods, of the square-lattice monomer-dimer free energy at another standard monomer activity reported in the literature with fewer digits (for example Kong's fixed-density values f2(1/2) = 0.633195588930), stating the published comparator with its source.

## How a win is checked

Skeptic (< 1 hour): rerun both programs at the two largest truncations in multiprecision; check digit agreement, check the value against Kong's bracket, and reproduce OEIS A028420 terms n <= 14 with the strip transfer code as a correctness test of the state space.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://arxiv.org/abs/cond-mat/0610690>

## Sources

- <https://arxiv.org/abs/cond-mat/0610690>
- <https://arxiv.org/abs/math/0402009>
- <https://arxiv.org/abs/1305.7028>
- <https://arxiv.org/abs/2001.00578>
- <https://oeis.org/A028420>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Baxter's own 1968 route was a variational CTM-like approximation; rerun a modern CTM (Nishino-Okunishi CTMRG) on the monomer-dimer vertex model in arbitrary precision.
- From quantum many-body physics: the monomer-dimer transfer matrix maps to a hard-core boson chain; a VUMPS fixed point in high precision is an independent second method.
- From combinatorics: Kong's fixed-density maximisation and the Friedland-Peled pressure inequalities give two-sided checks; use them as a sanity frame around the high-precision estimate.
- Exact strip free energies f_L via sparse power iteration on 2^L-state transfer matrices (L <= 26 fits in RAM) plus exponential-correction fits.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Normalisation traps: per site vs per dimer, natural log vs e^h2 (1.9402...), and the pure-dimer constant (Catalan/pi = 0.2915...) are all different numbers that circulate under the same name.
- Kong's '0.662798972834' is quoted with 12 decimals but he states 11 correct digits; the comparator is the bracket, not the last printed digit.
- Agreement of successive truncations of one method is not two methods; the criterion needs genuinely different algorithms.
- Float64 limits agreement to about 15 digits; a 20-digit claim needs multiprecision linear algebra end to end.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/monomer-dimer-square-lattice-constant-digits.md
```

Already set up? Say `run V3R1T4S on monomer-dimer-square-lattice-constant-digits`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `monomer-dimer-square-lattice-constant-digits`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
