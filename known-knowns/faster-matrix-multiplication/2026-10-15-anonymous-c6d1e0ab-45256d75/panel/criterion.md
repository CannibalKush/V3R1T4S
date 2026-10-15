# Criterion skeptic report: add-4x6x8-cr476

Sources read: the claim folder and claim.SHA256SUMS only (all 8 hashes verified OK with shasum -a 256 -c), plus the live fetches named in the brief (one each, UA 'V3R1T4S-research (honest client; curl)', all HTTP 200): Perminov's 4x6x8 cr551 file, fmm_sota.json (createdAt 2026-10-09T11:45:48), the GitHub tree API for Perminov's repo (not truncated, 6637 entries), the Lille 4x6x8 page, matmulcatalog COVERAGE.md. I also fetched Perminov's README.md and CHANGELOG.md (200) and schemes/reduced_known.json (200; the root-level path 404s) because the criterion names them. Own checker: criterion_ws/chk.py (written before reading the author's checker; the author's scripts were not opened).

## My checker, run on the object (claim/object/4x6x8_m140_cr476_ZT_reduced.json)
Real output:
`errs=[] nerr=0 tensor_bad=0 random_bad=0 adds_U=108 adds_V=136 adds_W=232 total=476 max_abs_expanded=1 claimed={naive:1620, reduced:476}`
- (1) Straight-line order: every form references only inputs or strictly earlier fresh variables of its own map (a forward reference is flagged; none found). Every coefficient is +1 or -1 (none else).
- (2) Every fresh variable and every final form expanded to an exact integer linear form over the inputs: all expanded coefficients lie in {-1,0,1} (max abs 1), including all intermediates.
- (3) Format n=[4,6,8], 140 products, 32 outputs (C transposed layout: output l*4+i = C[i][l]). Full tensor identity sum_q U[q][A_ij] V[q][B_kl] W[l*4+i][q] = [j==k][o==l*4+i] checked on all 24*48*32 entries: 0 violations. 20 random integer 4x6 / 6x8 matrix pairs (entries -9..9), all 32 outputs each: 0 mismatches.
- (4) Reduced count = sum over all fresh and final forms of (terms - 1): U 108 + V 136 + W 232 = 476. Matches the file's own complexity.reduced=476. Product-factor forms in u and v are single-term (0 additions); the W outputs carry the output sums.

## Calibration on Perminov's file (4x6x8_m140_cr551_cn1248_ZT_reduced.json)
My counter, same code: `adds_U=119 adds_V=172 adds_W=260 total=551`, expansion ternary, tensor identity exact, random evaluation exact, stored reduced=551, naive=1248. So the counter reproduces his 551 and the convention is the same. His 140 products (expanded U,V,W rows, signed) versus the claim's: 0 rows in common, so the products are different, as CLAIM.md says (claim is the Kronecker product of his 2x2x2_m7_cr15 and 2x3x4_m20_cr54 schemes; I did not re-derive that Kronecker structure, only that the rows differ). The claim's naive field (1620) is higher than his (1248); that is irrelevant to the reduced-convention criterion.

## Null models and corruptions (criterion_ws/nulls.py), all rejected
- Flip sign of one W fresh term: tensor violations 24, random mismatches 90. REJECTED.
- Drop last term of output 3: 6 violations, 20 mismatches. REJECTED.
- Swap V factors 10 and 11: 60 violations, 73 mismatches. REJECTED.
- Duplicate an index inside a U fresh form (coefficient 2): nonternary flagged (and identity fails). REJECTED.
- Forward reference in a U fresh form: order error flagged. REJECTED.
- Change the index of one W term: nonternary 2 flagged, 40 violations. REJECTED.
Calibration also doubles as a positive control (accepted, 551).

## Clauses
1. "an explicit straight-line program ... for a format <n,m,p> with max(n,m,p) <= 8": 4x6x8, max 8. MET.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": entry `{ "format": [4,6,8], "rank": 140, "exponent": 2.819770 }`; the object has m=140. MET.
3. "(1) is verified symbolically to compute the full product A*B exactly over Z": exact integer expansion plus exact tensor identity plus random evaluation, as above (no sympy run by me; exact integer symbolic expansion is equivalent). MET.
4. "(2) STRICTLY LESS than the smallest reduced addition count for that format and rank in Perminov's live repository ... counted under Perminov's 'reduced' convention": the tree has exactly one file for 4x6x8 (any axis permutation): addition_reduced_ZT/4x6x8_m140_cr551_cn1248_ZT_reduced.json, so min cr = 551; 476 < 551. No file named _cNNNN_ZT (no 'cr') exists for 4x6x8 in the tree, so the naive-count-convention question does not arise here (such files, where they exist for other formats, count nz-style totals and would not compare to cr). reduced_known.json (schemes/) has no 4x6x8 key; README lists 4x6x8 only in the rank table (140); CHANGELOG has no 4x6x8 line. MET.
5. "AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant": the Lille 4x6x8 page cites no complexity variant and no operation count; it gives the algorithm type polynomial and says the algorithm is the (Kronecker) tensor product of <2x2x2:7> with <2x3x4:20>. Nothing lower is published there, so the clause is vacuously satisfied. MET (vacuous).
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": the row for <4,6,8> reads `**140** in R/Q/Z | — | —`: the adds cell is `—` (shown for verified schemes only; this entry is not verified there; it credits 'Dronperminov-cr551_cn1248_ZT_reduced' rank 140). Its convention is naive nz(U)+nz(V)+nz(W) - 2r - n*p, a different count, not comparable to reduced. No lower count published. MET (vacuous).
7. "If the Lille rank ... only with non-ternary coefficients": not applicable; the Lille/Perminov rank 140 is attained with ternary coefficients and the candidate is ternary.
8. "The reference count is the MINIMUM cr value over all files for that format and rank": 551 (single file). MET.
9. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": rank is equal to the best known, not lower. MET. (Novelty beyond the named sources, including whether the Kronecker construction with reduced SLPs is already published, is left to another skeptic.)

## Verdicts
Full criterion: met on every clause checkable from the named sources; the comparison is to the single 551 reference and 476 < 551 with a different product set at the same rank. Caveats on width: the Lille and COVERAGE clauses hold because those sources publish no count for this format and rank; the evidence is for the format-and-rank comparison only, not for the optimality of 476.
Partial win p1 concerns <3,3,3> rank 23 only; the claim is a 4x6x8 result, so p1 is not met as written (a 3x3x3 SLP is required). The alternative reading in the brief (strictly fewer than Perminov's live 4x6x8 count, same convention) is met: 476 < 551. I report the brief's reading on the p1 line below. p2 and p3 are not claimed (p3 needs three formats).

p1 as defined in the brief (strictly fewer than Perminov's live 4x6x8 count, same convention): true. (The bank's own p1, a rank-23 <3,3,3> SLP, is not what the claim contains.)

confirmed_scope: claim/object/4x6x8_m140_cr476_ZT_reduced.json (sha256 45256d75a05660145a239129ba59524edf864bbda68bcf5297be8fdf7c38158e) is a ternary straight-line program that exactly computes the full 4x6 by 6x8 product over Z with 140 products (the best listed rank) using 476 reduced additions (U 108, V 136, W 232), strictly below the single live Perminov addition_reduced_ZT value of 551 for this format and rank, with no count published for it on the live Lille page or in the live COVERAGE.md adds column.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
