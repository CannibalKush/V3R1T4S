# Ground-state entropy of Potts antiferromagnets (proper colourings): tighten the certified bounds of Lundow and Markstrom (2008) for 4- and 5-colourings of the square grid or 3- and 4-colourings of the cubic lattice

⚛️ **Physics** · standard · tractability ★★★☆☆ · compute: laptop-days · open as of 2026-10-15

## The problem

The zero-temperature entropy of the q-state Potts antiferromagnet is the growth rate W per site of proper q-colourings. Lieb solved q = 3 on the square lattice ((4/3)^(3/2)); q = 4 and 5 on the square lattice and q = 3, 4 on the cubic lattice have no closed form. Per Hakan Lundow and Klas Markstrom (LMS J. Comput. Math. (2008), 'Exact and approximate compression of transfer matrices for graph homomorphisms', open access) give the best rigorous bounds known to us: 2.336056640723116 <= W_sq(4) <= 2.33606820555777; 3.2504049231640764 <= W_sq(5) <= 3.250407145038276; 1.4460096817417 <= W_c(3) <= 1.4470681274660; 2.0343787307189 <= W_c(4) <= 2.0652128520667. A large-q series quoted there gives W_sq(4) = 2.336056641 +- 1e-9 (heuristic). The Monte Carlo value W_sq(4) = 2.3370(7) of Robert Shrock and Shan-Ho Tsai (1997), still cited in later papers, sits about 1.4 standard errors above the rigorous bracket and is roughly 1e5 times less precise. Since q = 4, 5 on the square lattice are non-critical, both tighter rigorous bounds (larger transfer matrices with symmetry compression; their cubic bounds used only 4x4 to 6x6 cross-sections) and many more non-rigorous digits are laptop-reachable. No later improvement was found (search 2026-10-15).

## What counts as a win

Success means a rigorous bound strictly improving one of the eight published bounds above (upper smaller or lower larger), by at least 1e-9 for W_sq(4) or W_sq(5) and at least 1e-6 for W_c(3) or W_c(4), with the transfer-matrix definition and a nonnegative test vector whose Collatz-Wielandt ratios (or the exact eigenvalue inequality used by Lundow and Markstrom, cited by equation) a skeptic recomputes in exact or outward-rounded arithmetic, AND an arXiv/Google Scholar search re-run immediately before claiming that finds no published bound at least as good.

## Partial wins

- **p1:** At least 15 decimals of W_sq(4) (or W_sq(5)) by two independent non-rigorous methods (corner transfer matrix or VUMPS, and strip transfer matrices with extrapolation), lying inside the Lundow-Markstrom bracket and agreeing with the series value 2.336056641 within 1e-9.
- **p2:** An independent reproduction of Lundow and Markstrom's eigenvalue table for 4-colourings of the square grid up to their largest width, with exact or multiprecision eigenvalues released as data.

## How a win is checked

Skeptic (< 1 hour per certificate at moderate width): rebuild the colour-compressed transfer matrix for the stated width and boundary type, check the claimed vector is nonnegative, compute the ratios exactly or with interval arithmetic, and apply the stated inequality; reproduce two smaller published widths first.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.cambridge.org/core/journals/lms-journal-of-computation-and-mathematics/article/exact-and-approximate-compression-of-transfer-matrices-for-graph-homomorphisms/DF3F31D5871C39FDAD818685EDA617B3>

## Sources

- <https://www.cambridge.org/core/journals/lms-journal-of-computation-and-mathematics/article/exact-and-approximate-compression-of-transfer-matrices-for-graph-homomorphisms/DF3F31D5871C39FDAD818685EDA617B3>
- <https://arxiv.org/abs/cond-mat/9706162>
- <https://arxiv.org/abs/1502.07254>
- <https://arxiv.org/abs/1806.06751>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Colour-permutation compression: count colourings up to the action of S_q on colours (set partitions of the boundary) so the state space for q = 4 grows like Bell-type numbers, not q^width; Lundow and Markstrom used this only up to modest widths on 2006 hardware.
- From quantum many-body physics: for the non-critical square-lattice cases, VUMPS/CTMRG in high precision gives the p1 digits quickly and suggests which boundary type converges fastest for rigorous use.
- For the cubic lattice, increase the cross-section (6x6, 6x8 tori) with the same compression and a matrix-free power iteration; the 3-colouring bracket is still about 1e-3 wide.
- From representation theory: block-diagonalise by translation momentum and reflection symmetry of the cross-section; the leading eigenvector lives in the trivial sector, which shrinks the problem further.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The widely quoted Monte Carlo value 2.3370(7) for W_sq(4) is far less precise than (and sits above) the rigorous bracket; using it as the bar produces false 'improvements'.
- Vertex colourings vs edge colourings: the Kondev-Henley four-colouring model is an edge-colouring model with a different entropy.
- Open, cylinder and torus transfer matrices bound W in specific directions only for the right parities and boundary choices; check the inequality's hypotheses for each matrix.
- Per-site vs per-row normalisation and natural log vs W: report W per site as in Lundow-Markstrom.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/potts-antiferromagnet-colouring-entropy-bounds.md
```

Already set up? Say `run V3R1T4S on potts-antiferromagnet-colouring-entropy-bounds`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `potts-antiferromagnet-colouring-entropy-bounds`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
