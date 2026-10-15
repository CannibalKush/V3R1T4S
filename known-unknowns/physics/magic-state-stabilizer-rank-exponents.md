# Stabilizer rank of magic states: an exact decomposition of |T>^{(x)m} or |F>^{(x)m} into fewer stabilizer states than the best published exponent allows

⚛️ **Physics** · standard · tractability ★★☆☆☆ · compute: laptop-days · open as of 2026-10-15

## The problem

The stabilizer rank chi(psi) is the fewest stabilizer states whose linear combination equals psi exactly; for m copies of a magic state it controls the runtime of stabilizer-rank simulators of Clifford+T circuits (Bravyi and Gosset 2016; Bravyi, Browne, Calpin, Campbell, Gosset, Howard 2019). Any exact decomposition of psi^{(x)m} into r stabilizer states gives an exponent alpha <= log2(r)/m. For the H-type state |T> = (|0> + e^{i pi/4}|1>)/sqrt2, Hammam Qassim, Hakop Pashayan and David Gosset (arXiv:2106.07740) proved alpha <= 0.3963; Farrokh Labib and Vincent Russo (arXiv:2605.28586, May 2026) gave new qutrit-orbit bounds and a closed-form four-copy decomposition matching log2(3)/4 ~ 0.3962 for what they call the qubit T-type orbit (state names differ between papers). For the face-centre magic state, Samuel Bevins (arXiv:2610.17500, 12 Oct 2026) built a 24-term decomposition of 12 copies from two 15-term identities and proved alpha_F <= 3/8. Small-m exact ranks remain open beyond a few copies, and the area is moving monthly.

## What counts as a win

Success means, for psi in {|T> (H-type, the state above), the face-centre state |F> as defined in arXiv:2610.17500}, an explicit list of r stabilizer states on m qubits (each as a stabilizer tableau plus phase, or a quadratic-form/affine-space description) and exact coefficients in an explicit number field (Q(zeta_8) suffices for |T>) whose sum equals psi^{(x)m} EXACTLY, with log2(r)/m STRICTLY LESS (direction: min) than the best published exponent for that orbit found by an arXiv search re-run immediately before claiming (0.3963 for |T> per arXiv:2106.07740 and 3/8 for |F> per arXiv:2610.17500 on 2026-10-15), by at least 0.001; OR, without beating the exponent, r STRICTLY LESS than the smallest published exact decomposition for that specific m (m <= 12), with the published value cited.

## Partial wins

- **p1:** A smaller exact decomposition for some fixed m <= 12 than any published for that m and orbit (even if log2(r)/m does not beat the asymptotic exponent).
- **p2:** A certified lower bound chi(psi^{(x)m}) >= r+1 for some small m where only weaker bounds are published, via exhaustive search with a re-checkable certificate.
- **p3:** A qutrit analogue: a decomposition beating the per-copy exponents of Labib and Russo (arXiv:2605.28586) for the Strange, Norrell or Hadamard-eigenstate qutrit orbits.

## How a win is checked

Expand each stabilizer state to its 2^m amplitude vector exactly (sympy over the cyclotomic field, or integer vectors over Z[zeta_8] scaled by powers of sqrt2), sum with the coefficients, and compare entrywise to the exact tensor power; m <= 16 takes seconds. Independently confirm each listed state is a stabilizer state (tableau generators commute and are independent, or the affine/quadratic form check). Recompute log2(r)/m and compare with the live papers.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://arxiv.org/abs/2610.17500>

## Sources

- <https://arxiv.org/abs/2610.17500>
- <https://arxiv.org/abs/2106.07740>
- <https://arxiv.org/abs/2605.28586>
- <https://arxiv.org/abs/1601.07601>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Symmetry-restricted search: psi^{(x)m} is permutation-symmetric, so search over orbits of stabilizer states under S_m and the single-qubit Clifford stabiliser of psi, solving for coefficients by exact linear algebra on the symmetric subspace (dimension m+1).
- Import from coding theory: stabilizer states with real amplitudes correspond to binary codes and quadratic forms; decompositions are sums of quadratic-phase functions over affine subspaces, so Reed-Muller and weight-enumerator tools find candidate supports.
- Import from tensor decomposition: treat chi as a constrained tensor rank and run alternating least squares over a dictionary of stabilizer states with sparsity (OMP) to find low-r numerical candidates, then recognise exact coefficients with PSLQ/LLL.
- Substitution/bootstrapping as in Bevins: look for balanced identities at small m that can be recursively substituted to yield a better asymptotic exponent.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Approximate decompositions (fidelity < 1) and stabilizer extent are different quantities; only exact equality counts.
- Orbit confusion: |T>, |H> and the face state |F> are named inconsistently across papers; fix the state vector explicitly and compare only to bounds for the same Clifford orbit.
- Coefficients recognised numerically must be verified exactly; PSLQ can return wrong algebraic numbers at low precision.
- This area moves monthly (2605.28586, 2610.06819, 2610.17500 all in 2026); re-search arXiv immediately before claiming.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/magic-state-stabilizer-rank-exponents.md
```

Already set up? Say `run V3R1T4S on magic-state-stabilizer-rank-exponents`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `magic-state-stabilizer-rank-exponents`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
