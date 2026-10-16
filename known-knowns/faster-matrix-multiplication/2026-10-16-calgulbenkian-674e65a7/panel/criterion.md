# Criterion skeptic report: add-2x8x8-cr418

My own checker (criterion_ws/chk.py, written before reading the author's) and one fetch of each named source, 2026-10-15. Claim file hashes verified against claim.SHA256SUMS (all OK).

## Checker evidence (claim/object/2x8x8_m100_cr418_ZT_reduced.json)
- Format n = [2,8,8], m = 100. Parsed; every form references only inputs or earlier fresh variables; every coefficient is +1 or -1. 
- Every fresh variable and every final form expanded to an integer linear form over the inputs: all expanded coefficients lie in {-1,0,1} (no non-ternary intermediate).
- Full tensor identity for 2x8 times 8x8 (C transposed: output k*2+i is C[i][k]) holds exactly: ok = True (the set of nonzero Brent terms equals exactly the 128 matrix-multiplication triples, no extras, no cancellation errors). 20 random integer matrix pairs: all 16 outputs equal A*B.
- Reduced additions (sum of terms-1 over all fresh and final forms): U 90, V 154, W 174, total 418. Matches the file's own complexity field (reduced 418, naive 608). Naive recount nz(U)+nz(V)+nz(W)-2r-np = 824-200-16 = 608.

## Calibration against Perminov's file
Fetched 2x8x8_m100_cr424_cn608_ZT_reduced.json. My counter gives 424 (U 93, V 154, W 177), ok = True. Expanded U, V, W rows (the 100 products and the output maps) are identical to the claim's. So the scheme is the same; only programs differ: V program is byte-identical to his (154); U program differs (90 vs 93, saves 3); W program differs (174 vs 177, saves 3). Total saving 6.

## Null models (all rejected by my checker)
- flip sign of one w term: tensor identity fails (ok False, random eval wrong).
- replace single-term u[10] by another input: fails.
- shift one index in v_fresh[5]: fails.
- swap outputs 0 and 1: fails.
- coefficient set to 2: rejected (non-ternary).
- forward reference in u_fresh[0]: rejected (order).

## Clauses
1. "format with max(n,m,p) <= 8 and rank r equal to the best rank listed in fmm_sota.json (re-fetched live)": format [2,8,8], max 8. Live fmm_sota.json (createdAt 2026-10-09T11:45:48) lists exactly one entry for [2,8,8], rank 100. Met.
2. "(1) verified symbolically to compute the full product A*B exactly over Z": exact integer expansion plus tensor identity plus random evaluation. Met.
3. "(2) strictly less than the smallest reduced addition count ... in Perminov's live repository (addition_reduced_ZT file, reduced_known.json, README, CHANGELOG)": live tree (6637 entries, not truncated) has exactly one 2x8x8 file in addition_reduced_ZT (and none named 8x2x8 or 8x8x2): cr424. That is the minimum cr for this format and rank. 418 < 424. reduced_known.json has no 2x8x8 key. The README lists 2x8x8 only in a rank table (100), and the CHANGELOG has no 2x8x8 entry. Of the 321 ZT files, 195 carry cr; the others are named _cNNN_ZT (for example 2x3x10_m50_c198) and are naive counts, nz-based, a different convention (no common-subexpression elimination); none is for 2x8x8, so no comparison arises. Met.
4. "counted under the reduced convention (binary +/- one, -1 free, no other scalars)": my counter does exactly this and gives 424 on his file, matching his name. Met.
5. "AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant": the 2x8x8 page cites no complexity variant or operation count; it gives only the rank-100 polynomial 28X2Y2Z2+..., a Hopcroft-Kerr 1971 citation, and links to tensor/LRP/evaluation-scheme files. No count to be below. Vacuously met (the page's attached evaluation-scheme file was not fetched; I only checked the page text).
6. "and matmulcatalog's live COVERAGE.md adds column": the row for 2,8,8 shows rank 100 (Dronperminov-cr424_cn608_ZT_reduced) and adds = "—" (none). Its convention is naive nz(U)+nz(V)+nz(W)-2r-np; the claim's naive count is 608, and the file's naive field is also 608 (vs 418 reduced). No published lower count. Met.
7. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": rank 100 equals the sota rank; no rank lowering. Met.
8. Ternary coefficient-class clause: the Lille rank is attained by a ternary/Z scheme (Perminov's), same class as the candidate. Met.

## Verdicts
Full criterion: met on every clause checkable from these sources. The win is real but narrow: same scheme, same V program, U and W programs shortened by 3 additions each. It is not subsumed by any source named here (Perminov's only 2x8x8 file is 424).
Partial win p1 (as the brief defines it: strictly fewer than Perminov's live 2x8x8 count, same convention): true, 418 < 424. Note the bank text enumerates a different p1 (rank-23 3x3x3), which this claim does not address; I judged the brief's definition.

confirmed_scope: The program in claim/object/2x8x8_m100_cr418_ZT_reduced.json (sha256 674e65a792736a9bf4930d7e529fb901990cafa22ddf52baaf6c2ed0d256a87f) exactly computes the 2x8 by 8x8 product over Z with 100 products, the same 100 products as Perminov's 2x8x8_m100_cr424_cn608_ZT_reduced.json, using 418 reduced additions (U 90, V 154, W 174) with all expanded intermediates ternary, which is below 424, the only and minimum reduced count for this format and rank in his live addition_reduced_ZT directory on 2026-10-15, with no Lille-page complexity variant and no matmulcatalog adds value for 2x8x8 found.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
