# Criterion skeptic report: add-4x6x6-cr373

Object: claim/object/4x6x6_m105_cr373_ZT_reduced.json (sha256 0daeb11814025acb716cc2cb7432d358a83e8bff7985faec2ef73e5efad21bda; claim.SHA256SUMS verifies OK for all 8 files when run inside the claim folder).
My own checker is in criterion_ws/chk.py (written before reading the author's checker, which I did not run).

## Clause by clause

1. "explicit straight-line program ... for a format <n,m,p> with max(n,m,p) <= 8": MET. Format 4x6x6, max dim 6. Every form references only inputs or earlier fresh variables (a forward reference makes my checker reject); every coefficient is +1 or -1.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": MET. Live fmm_sota.json entry: format [4,6,6], rank 105. Object m = 105 (105 u/v factors, 24 w outputs).
3. "(1) verified symbolically to compute the full product A*B exactly over Z": MET. Checker output: every fresh variable and final form expanded to an exact integer linear form over the inputs; all expanded coefficients lie in {-1,0,1} (ternary condition, intermediates included). Full Brent tensor identity for 4x6 times 6x6 checked over all 24 x 36 x 24 index triples (output k*4+i is C[i][k], transposed layout): exact match. 50 random integer matrix pairs (entries -9..9): all 24 outputs equal A*B.
4. "(2) STRICTLY LESS than the smallest reduced addition count ... counted under Perminov's reduced convention": MET. My counter (sum over all fresh and final forms of terms - 1, negation free) gives 373 = U 95 + V 106 + W 172, equal to the declared reduced 373. Calibration: I fetched Perminov's 4x6x6_m105_cr430_fv243_cn894_ZT_reduced.json once (HTTP 200, sha256 9427b13b5509d45df8c56294f2abe6bc4e478f2aa079a1925e600ca2183739b5); my counter gives 430 = U 112 + V 131 + W 187, and that file also passes the ternary and Brent checks. So the counter matches his convention.
5. "The reference count is the MINIMUM cr value over all files for that format and rank in the live directory": MET. The live git tree (one fetch, not truncated, 6637 entries) has exactly one addition_reduced_ZT file for 4x6x6: cr430, rank 105. Minimum 430; 373 < 430. Other 4x6x6 files are in other directories (ZT, serendipitous_base, known tensor), not addition_reduced_ZT. Files named _cNNNN_ZT without "cr" do not exist for this format; in general they would be naive counts (nz-based, the cn-style convention), not the reduced convention, so they would not compare. reduced_known.json (fetched once) has no 4x6x6-105 key (only 4x6x6-116 with a Z2 value, a different rank), so it supplies no lower count.
6. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant": MET. Live https://fmm.univ-lille.fr/4x6x6.html lists 4x6x6:105 as the Kronecker tensor product of 2x2x2:7 with 2x3x3:15 and cites no complexity variant or operation count; no commentary section. Nothing to be below.
7. "and in matmulcatalog's live COVERAGE.md 'adds' column": MET. The 4x6x6 row shows rank 105 and adds +965. That column is a naive count (nz(U)+nz(V)+nz(W) - 2r - n*p), a different convention; literally 373 < 965, so no lower published count there.
8. "If the Lille rank ... non-ternary ... same coefficient class": not triggered; the scheme is ternary and so is the reference.
9. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": MET. Rank 105 equals the best known; no rank lowering.

## Is it the same scheme as Perminov's?

No. The 105 products (expanded u and v rows, compared up to overall sign) share 0 rows with Perminov's 4x6x6 file. This agrees with CLAIM.md (Kronecker product of two of his smaller schemes) and with Lille's own definition of 4x6x6:105. The criterion compares format and rank, not scheme, so this is allowed. The win lies in the straight-line programs over a different rank-105 decomposition.

## Null models (all rejected by my checker)

- Flipped one sign in w[3]: REJECT (Brent mismatch).
- Dropped a term from u_fresh[10]: REJECT (Brent mismatch).
- Changed one index in v_fresh[20]: REJECT (expanded coefficient leaves {-1,0,1}).
- Swapped two output rows of w: REJECT (Brent mismatch).
- Coefficient 2 in a fresh form: REJECT.
- Forward reference in u_fresh[0]: REJECT.
- Unmodified object: accepted.

## Verdicts

Full criterion: met on every checkable clause. Limit: the Lille and COVERAGE clauses are vacuous or cross-convention (no comparable published count exists), so the binding comparison is the single Perminov file, 430 vs 373.
p1 (as defined in my brief: strictly fewer than Perminov's live 4x6x6 count, same convention): met. The bank's own text defines p1 as a 3x3x3 result, p2 as 4x4x4 and p3 as three formats; the claim meets none of those, only the full criterion for 4x6x6.

p1: true
confirmed_scope: The program claim/object/4x6x6_m105_cr373_ZT_reduced.json (sha256 0daeb11814025acb716cc2cb7432d358a83e8bff7985faec2ef73e5efad21bda) is a ternary straight-line program that exactly computes the 4x6 by 6x6 product at rank 105 (the live best rank) with 373 additions under Perminov's reduced convention (U 95, V 106, W 172), strictly below the single live addition_reduced_ZT file for 4x6x6 at rank 105 (cr 430, recounted as 430 by the same counter), with no comparable lower count on the Lille page or in COVERAGE.md.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
