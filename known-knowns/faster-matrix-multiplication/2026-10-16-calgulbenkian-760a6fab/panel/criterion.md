# Criterion skeptic report: add-5x5x6-cr413

Checker written independently in criterion_ws/chk.py (exact integer expansion of every fresh and final form; no use of the author's checker). Live fetches (each once, HTTP 200, UA 'V3R1T4S-research (honest client; curl)'): Perminov's 5x5x6 reduced file, fmm_sota.json, GitHub tree API (not truncated), Lille 5x5x6 page, matmulcatalog COVERAGE.md, and Perminov's reduced_known.json (one extra fetch, because the criterion names it). The claim folder hashes match claim.SHA256SUMS (all 8 OK).

## My checker on the claim object (claim/object/5x5x6_m110_cr413_ZT_reduced.json)
- Straight-line order: every form references only inputs or earlier fresh variables (asserted; a forward reference is rejected). Every coefficient is +1 or -1.
- Expanded coefficients: all 108 + 114 + 74 fresh forms and all 110 + 110 + 30 final forms expand to coefficients in {-1,0,1}; max |coef| = 1. Ternary condition holds.
- Tensor identity for 5x5 times 5x6 (25 x 30 x 30 entries, C-transposed output layout, output l*5+i = C[i][l]): 0 mismatches. 20 random integer matrix pairs: 0 wrong entries.
- 110 product factors (u, v), 30 outputs (w).
- Additions (sum over fresh and final forms of terms-1): total 413. Per map: U 108 (fresh 108, final 0), V 114 (fresh 114, final 0), W 191 (fresh 128, final 63). 108+114+191 = 413.

## Calibration on Perminov's file (5x5x6_m110_cr460_fv204_cn1215_ZT_reduced.json)
- My counter gives 460 (U 122, V 129, W 209), ternary, tensor identity exact, random evaluation exact. Matches its name.
- The expanded U, V, W rows (110 products, 30 outputs) of the claim equal his exactly (same order). So the scheme is his; the programs differ: all six lists (u, v, w and the three fresh lists) differ from his; no map's program is identical.

## Clauses
1. "explicit straight-line program ... format <n,m,p> with max(n,m,p) <= 8": 5,5,6, max 6. Met.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": fmm_sota.json entry for [5,5,6] has rank 110 (only entry; createdAt 2026-10-09). Claim rank 110. Met.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": tensor identity exact, 0 mismatches, plus random evaluation. Met.
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository": the tree lists exactly one addition_reduced_ZT file for 5x5x6 (cr460), so the minimum cr is 460. reduced_known.json has no 5x5x6 entry (grep for 5x5x6, 5x6x5, 6x5x5 finds nothing). 413 < 460. Same convention (calibrated). CHANGELOG.md and README not read (outside the named fetches); the criterion lists them as reference places, so this part is unchecked for them. Files naming `_cNNNN_ZT` without `cr` live in naive_addition_reduced_ZT (c1192, c1215) and the addition_reduced_ZT file carries cn1215; these are naive nonzero-based counts (nz(U)+nz(V)+nz(W)-2r-np style, no shared subexpressions), a different convention, not SLP addition counts, so they do not compare as references; 413 is below them numerically anyway. Met (for the files and checks I read).
5. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant": the Lille 5x5x6 page shows only a polynomial 'Algorithm type' (a multiplication-structure description: 40 X^2Y^2Z^2 + ...) and the source (Kauers and Wood, arXiv 2505.05896). It cites no complexity variant or operation count for this rank. No lower count exists there. Met vacuously.
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": row for <5,5,6> shows +1215 (naive formula nz(U)+nz(V)+nz(W)-2r-np, per its legend), cited from Dronperminov-ZT. 413 < 1215; no lower count. The conventions differ (naive vs SLP), so the comparison is weak but nothing lower is published. Met.
7. "If the Lille rank is attained only with non-ternary coefficients ...": not applicable; the rank is attained in Z with ternary coefficients (Perminov file, claim object).
8. "reference count is the MINIMUM cr value over all files for that format and rank": one file, 460. Met.
9. "Each scheme is claimed once; a scheme that also lowers the rank is a rank target": rank is 110, equal to the best; not lowered. Met.

## Null models and corruptions (all rejected by my checker)
- Flip sign of one term in w[3]: tensor mismatches 54, random eval wrong 20 -> rejected.
- Drop one term from u[10]: mismatches 18 -> rejected.
- Change one index in v_fresh[5]: mismatches 10, and ternary check fails -> rejected.
- Coefficient 2 in a u_fresh term: rejected by coefficient assertion.
- Permute the 30 outputs (wrong C layout): 300 mismatches -> rejected.
- Add a form that repeats an input (a0+a0): expanded coefficient 2, ternary check fails -> rejected.
- Forward reference in u_fresh[0]: straight-line order assertion fails -> rejected.
- Null model for the count: Perminov's own program for the same products scores 460 under the same counter, so 413 is not an artifact of the counter (the counter is unchanged between the two).

## Verdicts
Full criterion: met, as far as it is checkable from the named sources (the reduced-count win of 47 additions over the live 460, 10.2 percent, on a Perminov rank-110 scheme; the rank is not improved).
p1 as listed in the bank is the <3,3,3> rank-23 partial win, not this format. Read with the brief's meaning (strictly fewer than Perminov's live 5x5x6 count, same convention): met, 413 < 460, same counter, calibrated.
This is not subsumed by a published lower count in the sources I read; literature novelty beyond these sources is for another skeptic.

p1: true
confirmed_scope: claim/object/5x5x6_m110_cr413_ZT_reduced.json (sha256 760a6fabaf3fef7778e29b48d9b96dca9ae9dc8686afa84060805ac3be723354) is a straight-line program with all expanded coefficients in {-1,0,1} that computes the 5x5 by 5x6 product exactly over Z with rank 110 (Perminov's own 110 products, equal to the best listed rank) using 413 reduced additions (U 108, V 114, W 191), strictly below the 460 of the only live 5x5x6 addition_reduced_ZT file, with no lower count on the Lille page or in COVERAGE.md.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
