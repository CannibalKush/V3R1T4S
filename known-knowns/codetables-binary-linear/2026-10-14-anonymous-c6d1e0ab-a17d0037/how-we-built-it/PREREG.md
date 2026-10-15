# Pre-Registration (`PREREG.md`)

target_id: codetables-binary-linear
frozen_utc: 2026-10-14T08:41:00Z
null_test: not needed because codetables-binary-linear is an exact deterministic finite-field linear code minimum-distance verification problem

## 1. Exact Claim Criterion & Primary Metric
- **Full Win (`solution_claim`)**: An explicit $k \times n$ generator matrix $G$ over $\mathbb{F}_q$ ($q \in \{2, 3, 4, 5, 7, 8, 9\}$) such that:
  1. $\operatorname{rank}_{\mathbb{F}_q}(G) = k$, computed independently by exact Gaussian elimination over $\mathbb{F}_q$.
  2. Exact minimum Hamming distance $d = \min_{x \in \mathbb{F}_q^k \setminus \{0\}} \operatorname{wt}(x G)$ computed by full enumeration of all $q^k - 1$ nonzero codewords via two independent exact algorithms (e.g., Gray-code stepping and recursive/coset enumeration or dual MacWilliams polynomial when $n - k$ is small; never by sampling).
  3. $d > d_{\text{lower}}(q, n, k)$ (strictly greater than the live `http://www.codetables.de/BKLC/` lower bound for $(q, n, k)$) and $d \le d_{\text{upper}}(q, n, k)$.
  4. Not one of the 7 LinCodeEvolve codes (`arXiv:2609.37056`) or derived from them, and not superseded by any newer arXiv or GitHub claim.
- **Partial Win `p1` (`partial_win_claim` — Quantum Stabilizer Code `[[n, k, d]]`)**:
  1. An explicit $(n - k) \times 2n$ binary stabilizer generator matrix $S = (X \mid Z)$ over $\mathbb{F}_2$ (or $\mathbb{F}_4$-additive generator matrix) of exact rank $n - k$.
  2. Exact symplectic self-orthogonality $X Z^\top + Z X^\top \equiv 0 \pmod 2$.
  3. Exact quantum minimum distance $d = \min_{v \in C^\perp \setminus C} \operatorname{wt}_{\text{symp}}(v)$ (or $d = \min_{v \in C^\perp \setminus \{0\}} \operatorname{wt}_{\text{symp}}(v)$ for pure codes) strictly greater than the live `http://www.codetables.de/QECC/` lower bound for `[[n, k]]`.
- **Partial Win `p2` (`partial_win_claim` — Improved Upper Bound)**:
  1. An exact rational Delsarte LP dual certificate or exhaustive non-existence certificate proving no $[n, k, d_{\text{upper}}]_q$ linear code exists, lowering $d_{\text{upper}}(q, n, k)$.

## 2. Two Independent Attack Lenses
1. **Lens 1 (`attempts/symmetry-orbit-join/`)**:
   - Quasi-cyclic (`QC`), double-circulant, and bordered/twisted group-ring searches over $\mathbb{F}_q$ ($q \in \{2, 3, 4, 5, 7, 8, 9\}$) and symplectic circulant / metacirculant searches for quantum stabilizer codes `[[n, k, d]]` (`p1`), plus Construction X / puncturing / shortening / extension waterfalls.
2. **Lens 2 (`attempts/c-evaluator-optimizer/`)**:
   - Native C (`clang -O3 -march=native -pthread`) bitwise / 64-bit SIMD Gray-code minimum-weight evaluator coupled with simulated annealing / tabu search over systematic tail blocks $[I_k \mid A]$ and symplectic stabilizer completions, plus exact rational Delsarte / MacWilliams LP upper-bound dual certificate checks (`p2`).

## 3. Verification Gate
- Standalone `verify_bklc.py` implementing two independent exact minimum-distance and rank/symplectic evaluators, plus `--self-test` checking a positive known code and rejecting a rank-deficient / lower-weight negative test case.
