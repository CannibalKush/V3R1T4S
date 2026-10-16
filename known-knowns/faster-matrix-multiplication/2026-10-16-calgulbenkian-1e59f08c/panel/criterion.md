# Criterion skeptic report: add-5x5x7-cr483

All evidence below is from my own checker (criterion_ws/chk.py, written before reading the author's) run in this session. Fetches were made once each, honest curl client, no retries, HTTP 200 on all. The claim folder files all matched claim.SHA256SUMS (8 of 8 OK).

## Own checker on claim/object/5x5x7_m127_cr483_ZT_reduced.json
- Straight-line order: every form references only inputs or earlier fresh variables (0 violations). Every coefficient is +1 or -1 (0 violations).
- Expansion over Z: all 116 + 137 + 82 fresh variables and all 127 + 127 + 35 final forms expanded to exact integer linear forms; max absolute expanded coefficient 1 (0 non-ternary intermediates, 0 non-ternary finals).
- Full tensor identity for 5x5 times 5x7 (Brent equations) with C-transposed output layout (output k*5+i is C[i][k]): 0 mismatches. Rank 127 (127 product factors, 35 outputs). 20 random integer matrix evaluations: 0 wrong entries.
- Reduced addition count, sum of (terms - 1) over all fresh and final forms: U 116, V 137, W 230, total 483.

## Calibration on Perminov's file
Fetched schemes/results/addition_reduced_ZT/5x5x7_m127_cr531_fv245_cn1607_ZT_reduced.json (sha256 9adf1d75...d064c, equals the author's record). My counter gives U 130, V 153, W 248, total 531, matching its cr531. It also passes my tensor and ternary checks. Its expanded U, V, W rows are identical to the claim's (same 127 products, same order). None of the three programs (u, v, w) is identical to his; all three differ, and each map has fewer additions in the claim (116 vs 130, 137 vs 153, 230 vs 248). So the claim recomputes the same scheme's linear maps with a shorter program.

## Clauses
1. "explicit straight-line program ... for a format with max(n,m,p) <= 8 and rank r equal to the best rank in fmm_sota.json": format 5x5x7, max 7 <= 8. Live fmm_sota.json entry: format [5,5,7], rank 127, the only entry for this format. Claim rank 127. MET.
2. "(1) verified symbolically to compute the full product A*B exactly over Z": exact integer Brent identity, 0 mismatches, plus random evaluation. MET.
3. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository": live tree (323 paths under addition_reduced_ZT, tree not truncated) holds exactly one 5x5x7 rank 127 file in addition_reduced_ZT, cr531. 483 < 531. MET. Files named c1606 in the separate naive_addition_reduced_ZT directory (5x5x7_m127_c1606_ZT) and cn1607 in the cr531 file name use the naive nonzero-count convention (nz-based, no shared subexpressions), not the reduced convention; they are a different count and not comparable, and the criterion names addition_reduced_ZT cr values. I did not re-fetch reduced_known.json, README or CHANGELOG (the brief limits my fetches); I rely on the author's table-record for those (reduced_known has no 5x5x7-127 entry, per that record), which is unverified by me.
4. Convention ("each binary +/- counts one; multiplication by -1 free; other scalars not allowed"): my count follows it, and the ternary condition holds on every expanded intermediate. MET.
5. "below any lower count published ... on the live Lille per-format page's cited complexity variant": the live 5x5x7 page cites the algorithm only as taken from Kauers and Wood (arXiv 2505.05896), with an "Algorithm type" polynomial and tensor/evaluation-scheme downloads; it cites no complexity variant and no operation or addition count. No lower count there. MET (vacuously).
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": the row for the 5x5x7 format shows +1606, defined as nz(U)+nz(V)+nz(W) - 2r - n*p, a naive count under another convention. 483 is below it numerically, and it is not a lower reduced count. MET.
7. "If the Lille rank is attained only with non-ternary coefficients ...": not triggered; the object is ternary and the rank is attained in ternary Z (Perminov's ZT file has the same products). MET.
8. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": rank is 127, equal to the best, not lower. MET.
9. Enumerated partial wins: p1 in the bank is the 3x3x3 rank 23 item, which this claim does not address. As reading the brief's own definition of p1 (strictly fewer than Perminov's live 5x5x7 count, same convention): 483 < 531 under the same counter calibrated on his file. True.

## Null models (my checker rejects each)
- Flipped sign in w_fresh[10]: 36 Brent mismatches, 36 wrong random outputs. Rejected.
- Dropped term in u_fresh[50] (form left with one term): form-length error, 116 Brent mismatches. Rejected.
- Dropped term in final w[7]: 13 Brent mismatches. Rejected.
- Swapped index in v[3]: 120 Brent mismatches. Rejected.
- Swapped outputs 0 and 1 (layout error): 20 mismatches. Rejected.
- Forward reference in u_fresh[0]: flagged as a straight-line order violation and 29 mismatches. Rejected.
- Coefficient 2 in v_fresh[5]: flagged, 18 mismatches. Rejected.
- Duplicate term giving expanded coefficient 2: flagged as non-ternary. Rejected.
Counter null: Perminov's file gives 531 (not 483), so the counter does not return the claimed number by default.

## Hidden quantifiers and stretched definitions
- "Strictly fewer than the live count" holds against the single reduced file; there is no second 5x5x7 rank 127 file in addition_reduced_ZT to hide a lower cr.
- The gain comes from the same products with a better program, which the criterion allows (counts SLPs for the scheme). No stretch of the convention was found: no non-ternary scalar, no reuse of an unrecorded quantity.
- Limits: I did not independently re-fetch reduced_known.json, README or CHANGELOG, and I judge no literature novelty.

p1 is also met as defined in the brief; the bank-listed p1 (3x3x3) is not addressed.

confirmed_scope: claim/object/5x5x7_m127_cr483_ZT_reduced.json (sha256 1e59f08cf1870f4ade6b3ab5efc2d004e5bb1a0edb455b7e250ed4a7cfc6a65a) is a ternary straight-line program that exactly computes the 5x5 by 5x7 product with rank 127, equal to the fmm_sota.json best rank, using 483 additions under the reduced convention (U 116, V 137, W 230) against 531 for Perminov's only live addition_reduced_ZT file at this format and rank, over the same 127 products, with no lower reduced count on the Lille page or COVERAGE.md.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
