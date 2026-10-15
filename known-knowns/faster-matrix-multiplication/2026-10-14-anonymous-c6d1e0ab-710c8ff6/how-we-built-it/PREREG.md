# Pre-Registration (`PREREG.md`)

frozen_utc: 2026-10-14T00:09:40Z
target_id: fmm-catalogue-small-format-rank
null_test: not needed because claims are explicit bilinear matrix multiplication schemes verified deterministically in exact arithmetic against the Brent equations and compared against deterministic catalogue integers.

## Success Criterion (Verbatim from Bank)
Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format (n,m,p) with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/(n)x(m)x(p).html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

## Partial Wins (Verbatim from Bank)
- **p1**: A new rank for a format with 17 <= max(n,m,p) <= 32 (outside Perminov's 16x16x16 table but inside the Lille catalogue): an exactly verified scheme whose rank is strictly below the live fmm_sota.json entry and the live Lille per-format page for that format, and not a plain composition already listed in the Lille 'construction' column.
- **p2**: A GF(2)-only improvement: an exactly verified (mod 2) scheme whose rank is strictly below the F2 column for its format in the live matmulcatalog COVERAGE.md AND below every GF(2)-valid scheme for that format in Perminov's live repository and MerlijnW70's repository, for a format where the characteristic-0 best rank is already <= the new GF(2) rank (so it is not a new rank overall).

## Exact Verification Protocol and Thresholds
1. **Checker**: Both `python3 runs/2026-10-14-0004/verify_brent.py scheme.json` and `python3 repo/known-knowns/faster-matrix-multiplication/verify-it-yourself/fmmcheck.py scheme.json` (or standard-library exact rational CRT checker) must pass with `0` failed Brent equations over $\mathbb{Q}$.
2. **Novelty & Threshold**: For a full win (`max(n,m,p) <= 16`), the verified rank $r$ over $\mathbb{Q}$ must be strictly smaller than:
   - `fmm_sota.json` rank for `sorted(n,m,p)`,
   - `https://fmm.univ-lille.fr/(n)x(m)x(p).html` rank (fetched live before claiming),
   - `min(ZT, Z, Q)` in Perminov's `README.md`,
   - lowest rank in `MerlijnW70/fmm-schemes`,
   - `R/Q/Z` column in `solven-eu/matmulcatalog` `COVERAGE.md`, AND
   - any existing record for `sorted(n,m,p)` in V3R1T4S `TROPHY_CASE.md`.
