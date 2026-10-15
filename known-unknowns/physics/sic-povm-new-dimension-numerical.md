# SIC-POVMs: the first publicly posted numerical Weyl-Heisenberg SIC fiducial in a dimension d >= 194 (outside known families)

⚛️ **Physics** · standard · tractability ★★☆☆☆ · compute: laptop-days · open as of 2026-10-15

## The problem

A SIC-POVM in dimension d is d^2 unit vectors in C^d with |<psi_j|psi_k>|^2 = 1/(d+1) for j != k; Zauner's conjecture says they exist for every d, as Weyl-Heisenberg orbits of a fiducial vector. Numerical fiducials: Andrew Scott and Markus Grassl (JMP 2010) for all d <= 67; Scott (arXiv:1703.03993) a putatively complete list of known-symmetry solutions for d <= 90, one Zauner-symmetric solution for every d <= 121, and higher-symmetry solutions for d = 124, 143, 147, 168, 172, 195, 199, 228, 259, 323; Grassl reports numerical solutions for all d <= 193 (CodEx talk abstract, 2021, which also mentions exact solutions in d = 844 and 1299). Families beyond that: Fibonacci-Lucas dimensions (Grassl-Scott 2017: 4, 8, 19, 48, 124, 323, 844, ...), Stark-unit constructions for prime d = n^2+3 (Appleby, Bengtsson, Grassl, Harrison, McConnell 2022; up to d = 19603) and for d = n^2+3 = 4p (Bengtsson, Grassl, McConnell, arXiv:2403.02872; up to d = 39604), all tabulated on Grassl's SIC page (last updated 2022-11-08). Crucially, Marcus Appleby, Steven Flammia and Gene Kopp (arXiv:2501.03970, Jan 2025) give an explicit conditional construction of a putatively complete set of Weyl-Heisenberg SICs in EVERY dimension d > 3 (ghost SICs from Shintani-Faddeev modular cocycle values, Galois-conjugate to SICs assuming the order-1 abelian Stark conjecture and a special-value identity), released as the Julia package Zauner.jl, and computed four inequivalent numerical SICs in d = 100 (three new). So for d >= 194 outside the families above, no numerical fiducial appears to be publicly posted (checked 2026-10-15), but a public recipe exists; a new-dimension numerical fiducial is a data contribution and a test of the Appleby-Flammia-Kopp conjectures, not new existence mathematics.

## What counts as a win

Success means a fiducial vector psi in C^d for some d >= 194 such that (a) after Newton refinement in mpmath at 60 digits, max_{p != 0} | |<psi|D_p psi>|^2 - 1/(d+1) | < 1e-40 over all d^2 - 1 Weyl-Heisenberg displacement operators D_p (Appleby convention), with |psi| = 1; (b) d does not appear (re-fetched live immediately before claiming) on Grassl's SIC page (http://s208785153.online.de/SICPOVM/), on Flammia's exact-SIC page, in Scott 2017's list, in the Fibonacci-Lucas and Stark-unit papers (arXiv:1707.02944, 2112.05552, 2403.02872), in Appleby-Flammia-Kopp (arXiv:2501.03970) or the Zauner.jl documentation, and an arXiv/Google Scholar search for 'SIC' with 'd = <value>' finds no published fiducial for that d; and (c) the claim states which method produced it (independent numerical search vs the Zauner.jl ghost construction), since only the former is independent evidence for the conjectures behind the latter.

## Partial wins

- **p1:** The first PUBLICLY posted numerical fiducial (60-digit refined, same tolerance) for some d in 152..193 not in any posted list; Grassl reports solutions exist there, so this is a public-data contribution only.
- **p2:** A numerical SIC for some d >= 101 found by an independent method (not Zauner.jl) whose overlap phases match (or provably fail to match) the Appleby-Flammia-Kopp ghost prediction for that d: either outcome is an independent test of the 2025 conjectures. A mismatch must be confirmed by two independent computations.
- **p3:** A new Clifford-orbit class of SIC in some d <= 90 missing from both Scott's putative complete list and the Appleby-Flammia-Kopp admissible-tuple tables (shown inequivalent under the extended Clifford group via overlap-phase multisets); this would contradict two completeness conjectures and needs exceptional scrutiny.

## How a win is checked

Checker (< 30 min for d <= 400): load psi (complex, >= 60 digits), normalise; compute all overlaps <psi|D_{p} psi> via the FFT identity in double, then for the max-deviation check repeat in mpmath at 60 digits (d^2 overlaps x O(d) each; ~10^7 multiprecision operations at d = 200); assert deviation < 1e-40; confirm d is not in the known-dimension list compiled from the cited sources.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <http://s208785153.online.de/SICPOVM/>

## Sources

- <http://s208785153.online.de/SICPOVM/>
- <https://www.physics.usyd.edu.au/~sflammia/SIC/>
- <https://arxiv.org/abs/1703.03993>
- <https://arxiv.org/abs/0910.5784>
- <https://arxiv.org/abs/2112.05552>
- <https://arxiv.org/abs/2403.02872>
- <https://arxiv.org/abs/1707.02944>
- <https://arxiv.org/abs/2501.03970>
- <https://github.com/sflammia/Zauner.jl>
- <https://sflammia.github.io/Zauner.jl/tables/>
- <https://www.math.colostate.edu/~king/codex/abstracts/grassl2021.html>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Ghost-first route: use Zauner.jl to compute the ghost fiducial for a chosen d >= 194 at high precision, then Galois-conjugate (sign switch of sqrt(Delta_0)) by recognising overlaps as algebraic numbers, and Newton-refine; a successful run is a data point for the Appleby-Flammia-Kopp conjectures beyond d = 100.
- Independent numerical route: impose Zauner (order-3) or Scott's F_a/F_b symmetry and minimise sum_p |<psi|D_p psi>|^4 with FFT-based O(d^2 log d) evaluations and many L-BFGS restarts; seed with Stark-unit or ghost phases to cut restarts.
- Import from signal processing: SIC fiducials are flat-ambiguity Gabor windows; Gerchberg-Saxton-style alternating projections between fiducial and ambiguity-function constraints are a fast alternative to gradient descent.
- Dimension choice: favour d with many small factors (e.g. 196, 198, 200, 210) where extra Clifford symmetries reduce the search, or d whose admissible tuple has a short word length l in the Zauner.jl tables (cheaper ghost evaluation).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Near-misses: L-BFGS converges to vectors with deviation ~1e-6 that are not SICs; only the 60-digit Newton refinement to < 1e-40 counts.
- Known dimensions are scattered across sources: Scott 2017 (195, 199, 228, 259, 323), Fibonacci-Lucas (844, and 1299 per Grassl's 2021 talk), the Stark-unit tables (e.g. 199, 292, 487, 628, 787, ... 39604) and the d = 100 examples of arXiv:2501.03970; check all of them.
- A Zauner.jl-generated SIC is the output of a public recipe; it must be labelled as such and is not independent confirmation of the Appleby-Flammia-Kopp conjectures.
- A numerical fiducial, however precise, is not a proof of existence (the SIC equations are overdetermined, so interval Newton does not apply directly); say 'numerical'.
- Convention mismatches (phase factor tau = -e^{i pi/d}, index ordering) change individual overlaps but not their moduli; the checker uses moduli.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/sic-povm-new-dimension-numerical.md
```

Already set up? Say `run V3R1T4S on sic-povm-new-dimension-numerical`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `sic-povm-new-dimension-numerical`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
