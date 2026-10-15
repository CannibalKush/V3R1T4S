# Criterion skeptic report: add-6x8x8-cr993

Checker: criterion_ws/chk.py (written before reading the author's checker; the author's checker was not run or read). Raw output in criterion_ws/chk_out.txt. Hashes of all claim files verified OK with shasum -c against claim.SHA256SUMS.

## Own checker results on claim/object/6x8x8_m266_cr993_ZT_reduced.json
- Parse: n = [6, 8, 8], m = 266, z2 = false. 255 U-fresh, 274 V-fresh, 160 W-fresh variables; 266 u, 266 v, 48 w final forms.
- Straight-line order: every term references an input or an earlier fresh variable of the same map (a forward reference is rejected by the checker, see nulls). Every coefficient is +1 or -1.
- Ternary check: every fresh variable and every final form expanded exactly over the inputs; all expanded coefficients lie in {-1, 0, 1} (no non-ternary form in U, V or W).
- Tensor identity: all 48 outputs (output l*6+i is C[i][l], transposed layout) satisfy sum_k u_k[a] v_k[b] w_o[k] = [a=(i,j), b=(j,l)] exactly over Z (0 mismatches). Evaluated on 5 random integer 6x8 / 8x8 pairs: all 48 outputs equal A*B.
- Reduced count (sum of terms-1 over all fresh and final forms): U 255, V 274, W 464, total 993 (matches the object's complexity.reduced = 993).
- Self-reported naive count in the file: 3788. My recount nz(U)+nz(V)+nz(W)-2r-np = 4368-532-48 = 3788.

## Calibration on Perminov's live file 6x8x8_m266_cr1161_fv654_cn2780_ZT_reduced.json (fetched once)
- My counter gives U 296, V 366, W 499, total 1161. Ternary and tensor identity pass. Naive recount 2780. Calibration matches 1161.
- The brief expected the 266 products to be identical. They are NOT: after sign-normalising, the two files share 15 distinct u rows, 12 distinct v rows and 0 (u,v) product pairs. The claim's expanded U/V/W are much denser (total nonzeros 4368 vs 3360) and the row-weight histograms differ. So the claim file is a different rank-266 scheme, not Perminov's scheme with a better program. The CLAIM.md parenthesis "the scheme is the one in Perminov's repository at that rank" is false in the literal sense. The success criterion asks for a program for the format at the live best rank with a lower reduced count than the reference count for that format and rank; it does not require the same scheme, so this does not defeat the criterion. It does mean the count is not an addition-reduction of the reference scheme, and under the naive convention the claim (3788) is worse than Perminov's (2780).

## Clause by clause
1. "explicit straight-line program ... for a format with max(n,m,p) <= 8": met. Format <6,8,8>, max 8.
2. "rank r equal to the best rank listed in fmm_sota.json (re-fetched live)": met. Live fmm_sota.json (createdAt 2026-10-09) has format [6,8,8], rank 266. Claim rank 266.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": met (exact integer expansion and Brent identity, plus random integer evaluation; see above).
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository, counted under the 'reduced' convention; multiplication by -1 free, other scalars not allowed": met. The live git tree (321 paths under addition_reduced_ZT/ including a naive_addition_reduced_ZT/ subfolder and .m files; tree not truncated) holds exactly one file matching 6x8x8 or a permutation of the format: the cr1161 file, so the minimum cr is 1161. 993 < 1161. All expanded coefficients ternary, only +/- binary additions used. schemes/reduced_known.json (fetched once, 33 keys) has no 6x8x8 entry. Files named _cNNNN_ZT without "cr" are in the naive_addition_reduced_ZT folder and use the naive count nz(U)+nz(V)+nz(W)-2r-np (no sharing of subexpressions), a different convention, so they do not compare with reduced counts; none exists for 6x8x8 anyway. README and CHANGELOG were not fetched (not in the brief's list); the repo evidence used is the tree, the cr1161 file and reduced_known.json.
5. "AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant": met vacuously. The live page fmm.univ-lille.fr/6x8x8.html shows only the algorithm type polynomial and says the algorithm is the Kronecker product of <2x2x2:7> with <3x4x4:38>. It cites no complexity variant and no operation or addition count for rank 266. Nothing to be below.
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": met vacuously. The row for <6,8,8> reads R/Q/Z "266 Dronperminov-cr1161_fv654_cn2780_ZT_reduced" and the adds column is "-" (empty). Its convention is the naive count nz(U)+nz(V)+nz(W)-2r-np, shown for verified schemes only, so there is no published count to compare. (That convention would give 2780 for Perminov's scheme and 3788 for the claim, so the claim would not beat a naive number had one been listed; the criterion compares against published counts only, and none exists.)
7. Coefficient class clause (Lille rank only with non-ternary): not triggered. Lille/COVERAGE list rank 266 in R/Q/Z and the candidate is ternary integer.
8. "reference count is the MINIMUM cr value over all files for that format and rank": 1161 (only file).
9. "Each scheme is claimed once; a scheme that also lowers the rank is a rank target": rank 266 equals the live best, not lower. Not triggered.

## Null models (my checker)
- Flip one sign in a W fresh form: REJECTED (Brent mismatches in 6 of 48 outputs, random evaluation mismatch, non-ternary expanded W forms).
- Drop one term from a W fresh form: REJECTED (Brent mismatches in 12 of 48 outputs).
- Swap two v product factors (indices 10 and 11): REJECTED (5 of 48 outputs).
- Swap two final W outputs (7 and 8): REJECTED (2 of 48 outputs).
- Duplicate a term in a U fresh form (coefficient 2): REJECTED (non-ternary expanded forms).
- Forward reference in a U fresh form: REJECTED (order check).
The unmodified object passes all checks, so the checker discriminates.

## Verdicts
Full criterion: met as checkable from these sources, with the caveats that (a) the claim scheme differs from Perminov's rank-266 scheme, and (b) clauses 5 and 6 hold only because the Lille page and COVERAGE.md publish no count for this format and rank.
p1 (strictly fewer than Perminov's live 6x8x8 count, same reduced convention): met, 993 < 1161.

confirmed_scope: claim/object/6x8x8_m266_cr993_ZT_reduced.json (sha256 353b922983ecc35f13d03a9e7136407be941d5a3282630c9eb9c13af94c236ec) is a ternary straight-line program for a rank-266 scheme for <6,8,8>, exact over Z by my own tensor-identity and random-evaluation checks, with 993 reduced additions (U 255, V 274, W 464), against 1161 for the only live Perminov file for this format and rank, with no count for this format and rank on the Lille page or in COVERAGE.md to compare, and the scheme itself is not Perminov's scheme.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
