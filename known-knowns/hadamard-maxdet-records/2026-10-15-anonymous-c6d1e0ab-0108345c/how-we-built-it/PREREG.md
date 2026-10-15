# Run Preregistration: `hadamard-maxdet-records`

- **UTC Timestamp**: `2026-10-14T07:49:06Z`
- **Target**: `hadamard-maxdet-records` (`tractability = 3.0`)

## 1. Preregistered Attack Plan

1. **Standalone Exact Verifier (`verify_maxdet.py`)**:
   - Pure Python stdlib verifier implementing two independent exact integer determinant algorithms:
     - **Method A**: Fraction-free Bareiss integer elimination (`det_bareiss`).
     - **Method B**: Multi-prime Chinese Remainder Theorem modular determinant across distinct 62-bit primes (`det_crt`) until $\prod p_i > 2 B(n)^2$.
   - Verifies $X_{ij} \in \{\pm 1\}$, $|\det X| \pmod{2^{n-1}} = 0$, $D(X) = |\det X| / 2^{n-1} > D_{\text{rec}}(n)$, and $|\det X| \le B(n)$.
   - Also implements `--gram` mode for `p2` (Frozen Gram Targets), verifying symmetry, $G_{ii} = n$, mod-4 Gram congruences, Sylvester positive definiteness (all $n$ leading principal minors $> 0$ via Bareiss), $\det G > (\det R_{\text{rec}}(n))^2$, $M_0 M_0^T = G[:k, :k]$ for $k \ge n - 2$, constructive rational equivalence $Q Q^T = G$ (and $P (n I_n) P^T = G$ when $\sqrt{n} \in \mathbb{Q}$), and exact Hasse–Minkowski local Hilbert symbol invariants at all primes $p \mid 2 n \det G$.
2. **Lens 1 (`attempts/c-evaluator-optimizer/`)**:
   - Build and run `maxdet_search.c` + `run_maxdet_campaign.py` on $n = 105, 109, 117$ and open orders in $29 \le n \le 101$.
3. **Lens 2 (`attempts/representation-absorber/`)**:
   - Build and run `frozen_gram_builder.py` to generate exact `p2` Frozen Gram Targets and constructive rational congruence certificates on $n = 49, 81$ and open $n \equiv 1 \pmod 4$ orders, plus two-circulant PAF spectrum audits on $55 \le n \le 99$.
null_test: not needed because hadamard-maxdet-records is an exact deterministic integer determinant problem
