# Criterion skeptic report: add-4x4x7-cr294

Own checker: criterion_ws/chk.py (written before reading the author's checker, which I did not run). Nulls: criterion_ws/nulls.py. Fetched copies are in criterion_ws/.

## Checker output on claim/object/4x4x7_m85_cr294_ZT_reduced.json
- Hashes: all files match claim.SHA256SUMS.
- Straight-line order: every form references only inputs (U: 16, V: 28, W: 85) or earlier fresh variables of its own map. Asserted for all 72 + 83 + 50 fresh forms and all 85 + 85 + 28 final forms. Every coefficient is +1 or -1.
- Ternary check: every fresh variable and final form expanded over the inputs with exact integers. All expanded coefficients lie in {-1, 0, 1}. No non-ternary intermediate.
- Tensor identity for 4x4 times 4x7: 85 products, 28 outputs, output index k*4+i is C[i][k] (transposed layout). Full Brent equations hold exactly (the sum of U*V*W triples equals the matrix multiplication tensor, no extra terms). Also 20 random integer matrix pairs evaluated: all 28 outputs equal A*B.
- Count (sum of terms - 1 over all fresh and final forms): U 72, V 83, W 139, total 294. The file's own complexity.reduced field says 294.

## Calibration on Perminov's file
Fetched once (HTTP 200): 4x4x7_m85_cr319_fv119_cn631_ZT_reduced.json, sha256 dc7b4ef436d90acd4d6de6f3b913a7f6f2f9b8c33ccadd119b7f95e1179e05f1. My counter gives U 81, V 93, W 145, total 319, matching its name. It also passes Brent and the random evaluation. Expanded U, V, W rows of the claim and of his file are identical, row for row and in the same order. So the scheme is his, and no map's program is identical to his: all three differ (72 vs 81, 83 vs 93, 139 vs 145).

## Clauses
1. "explicit straight-line program ... format <n,m,p> with max(n,m,p) <= 8": met. Format 4x4x7, max dimension 7.
2. "rank r equal to the best rank listed in fmm_sota.json (re-fetched live)": met. Fetched once (HTTP 200); entry is format [4,4,7], rank 85. The claim's rank is 85.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": met (Brent identity exact, plus random evaluation).
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository ... reference is the MINIMUM cr over all files for that format and rank in the live directory": met. The live tree (HTTP 200, not truncated) holds exactly one addition_reduced_ZT file for 4x4x7, the cr319 file above, so the minimum is 319 and 294 < 319. There is no permuted-format file such as 4x7x4. Files named _cNNN_ZT without "cr" live in schemes/results/naive_addition_reduced_ZT, a separate directory, and there is no 4x4x7 file there. They use a naive count (nonzeros minus 2r minus outputs), which is not the reduced SLP convention, so they do not compare. I did not fetch reduced_known.json, README or CHANGELOG (outside my brief); the table-record metadata says they give no lower 4x4x7 count. I did not verify that.
5. "counted under Perminov's reduced convention (+/- counts one; -1 free; no other scalar)": met. My counter reproduces 319 on his file and 294 here, and the ternary check rejects any other scalar.
6. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant": met, vacuously. The fetched Lille 4x4x7 page (HTTP 200) lists rank 85 (AlphaEvolve source) and an algorithm-type polynomial (27 X^2Y^2Z^2 + 5 X^2YZ + ...), which is a tensor-type description, not an operation count. It cites no complexity variant or operation count for this rank.
7. "and in matmulcatalog's live COVERAGE.md 'adds' column": met, vacuously. The 4x4x7 row shows +631 under the naive convention nz(U)+nz(V)+nz(W)-2r-n*p, which equals Perminov's cn631. It is not comparable with a reduced SLP count, and nothing in it is below 294 anyway.
8. "If the Lille rank is attained only with non-ternary coefficients, compare in the same class": the candidate is ternary, and Perminov's ZT file is the same class, so the comparison is like for like.
9. "Each scheme is claimed once; a scheme that also lowers the rank is a rank target": met. Rank 85 equals the best known rank, so it is not a rank improvement.

## Null models (all rejected by my checker)
- Flipped sign in w_fresh[3]: Brent false, random false.
- Dropped term in v_fresh[10]: Brent false, random false.
- Swapped product indices u[5] and u[6]: Brent false, random false.
- Swapped output forms 0 and 1: Brent false, random false.
- Coefficient 2 in u_fresh[0]: rejected (non-ternary coefficient).
- Forward reference in u_fresh[0]: rejected (straight-line order).
- Appended fresh form 16+16 (expands to coefficient 2): rejected (non-ternary intermediate).

## Verdicts
Full criterion: met. A genuine, non-subsumed win over the one live file of Perminov's (319 down to 294, 25 fewer additions, all three maps improved), with no competing lower count on the Lille page or in COVERAGE.md. Limit: reduced_known.json, README and CHANGELOG were not re-fetched by me.

Partial win p1 as written (a rank-23 3x3x3 SLP) does not apply to this object. Read as "strictly fewer than Perminov's live count for this format, same convention", the claim also meets it (294 < 319), but that is subsumed by the full criterion.

p1: true
confirmed_scope: claim/object/4x4x7_m85_cr294_ZT_reduced.json (sha256 a6655488fc692a5a552aed8c46ae58eff2a384d66f33966f3a53c0a33b3fec2e) is a ternary straight-line program that exactly computes the 4x4 by 4x7 matrix product over Z with Perminov's rank-85 scheme using 294 additions under the reduced convention (U 72, V 83, W 139), against 319 in Perminov's only addition_reduced_ZT file for 4x4x7 rank 85 as fetched on 2026-10-15, with no lower operation count on the fetched Lille 4x4x7 page or in the fetched COVERAGE.md.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
