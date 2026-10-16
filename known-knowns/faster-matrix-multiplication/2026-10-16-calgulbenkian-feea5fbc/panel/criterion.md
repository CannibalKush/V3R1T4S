# Criterion skeptic report: add-4x4x6-cr256

All checks below were run by my own checker (criterion_ws/chk.py and criterion_ws/nulls.py), written before reading the author's. Claim hashes verified with shasum -c against claim.SHA256SUMS, run from inside the claim folder: all 8 files OK.

## Clause 1: explicit straight-line program, max dimension <= 8, rank equal to live best rank
Quote: "an explicit straight-line program ... for a format with max(n,m,p) <= 8 and rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)".
Met. Format 4x4x6 (max 6), r = 73. The live fmm_sota.json (sha256 d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1) has exactly one 4x4x6 entry: rank 73. The program is straight-line: every form references only inputs or earlier fresh variables (no forward reference, no duplicate index in a form), and every coefficient is +1 or -1 (checked on all U, V, W forms).

## Clause 2: symbolic verification of the full product
Quote: "(1) is verified symbolically to compute the full product A*B exactly over Z".
Met. Real checker output:
  claim: ternary_ok=True brent_violations=0 random_eval_ok=True counts {u: 66, v: 71, w: 119} total 256
Every fresh variable and final form was expanded to an exact integer linear form over the inputs; all expanded coefficients lie in {-1,0,1} (no non-ternary intermediate). The Brent identity sum_t U[t][a] V[t][b] W[k*4+i][t] = [a=(i,j) and b=(j,k)] was tested for all 16*24*24 index triples with the transposed output layout (output k*n+i is C[i][k]): 0 violations. 20 random integer matrix evaluations of the program (products formed as ua*vb) matched A*B exactly.

## Clause 3: addition count strictly below Perminov's live minimum reduced count
Quote: "STRICTLY LESS than the smallest reduced addition count ... counted under Perminov's 'reduced' convention ... The reference count is the MINIMUM cr value over all files for that format and rank in the live directory".
Met. My count (sum over all fresh and final forms of terms-1) is 256: U 66, V 71, W 119. The live tree (GitHub git trees API, truncated=false, sha256 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610) lists in addition_reduced_ZT exactly one 4x4x6 file: 4x4x6_m73_cr280_cn540_ZT_reduced.json, so the minimum cr is 280. 256 < 280.
Calibration: I fetched that file once (sha256 cbc252aaf1694aa0cb565cf4a4c3e9d418697afad253af77e25611dc66852222, matches the author's record). My counter gives 280 (U 73, V 81, W 126), ternary_ok, 0 Brent violations. Its expanded U, V, W rows (73 products, same order) are identical to the claim's for all three maps, so it is the same scheme and only the programs differ. No map's program is identical to his: each map's count is lower (U 66 vs 73, V 71 vs 81, W 119 vs 126).
Files named c534 and c540 without "cr" are in a different directory (naive_addition_reduced_ZT) and use the naive nonzero-based count with no shared subexpressions, not the reduced convention; they are outside the criterion's reference set and do not compare. (Even by value, 534 and 540 exceed 256.) I did not refetch reduced_known.json, README or CHANGELOG; for those I rely on the author's record (no 4x4x6-73 entry, no lower count). The minimum comes from the tree and the file names, which I fetched myself.

## Clause 4: below counts on the Lille per-format page
Quote: "AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant".
Met vacuously. The live 4x4x6 Lille page (sha256 f30768b4561049c721e286835986e541845a62f27b39ac16bef0a002bd17809e) lists rank 73 (Smirnov, January 2023), an algorithm-type polynomial, and encodings. It cites no complexity variant and no operation or addition count for this rank, so nothing lower exists to beat. The coefficient-class clause is not triggered.

## Clause 5: below matmulcatalog COVERAGE.md adds column
Quote: "and in matmulcatalog's live COVERAGE.md 'adds' column".
Met. The live COVERAGE.md (sha256 c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7) row for 4,4,6 shows rank 73 with adds "+565". The column is defined as the naive count nz(U)+nz(V)+nz(W) - 2r - n*p, a different convention, not comparable to a reduced count; in any case 565 > 256.

## Null models (my checker rejects each)
- flipped sign in v_fresh[5] term 0: 8 Brent violations, random eval fails: rejected.
- dropped a term from w[3]: 2 violations, eval fails: rejected.
- swapped an index in u[10]: 20 violations: rejected.
- swapped two outputs: 16 violations: rejected.
- forward reference in u_fresh[0]: structural reject.
- coefficient 2 in v[0]: structural reject (non-ternary).
The checker accepts the unmodified claim and Perminov's file (280), so it is not trivially rejecting.

## Other clauses
"Each scheme is claimed once: a scheme that also lowers the rank is a rank target": the rank stays 73, equal to the live best, so this is not a rank target. Coefficients are ternary over Z, the same class as Perminov's. No hidden quantifier found: the compared cell is exactly one file and rank.

## Verdicts
Full criterion: met (4x4x6 at rank 73, 256 < 280; the Lille and COVERAGE clauses are non-binding). The bank's enumerated partial wins (3x3x3, 4x4x4, three-format shift) concern other formats and are not what is claimed. The task's p1 (strictly fewer than Perminov's live 4x4x6 count, same convention) is met, as a weaker consequence: 256 < 280.

p1: true
confirmed_scope: For format 4x4x6 at rank 73 (the live best rank in fmm_sota.json), claim/object/4x4x6_m73_cr256_ZT_reduced.json (sha256 feea5fbcfd07fd3416d280a9a3d8af5e49c916171b9771d614e51e7a43f98b85) is a ternary straight-line program that exactly computes A*B over Z (Brent identity and random-integer evaluation verified, all expanded coefficients in {-1,0,1}) with 256 reduced additions, strictly below the live minimum of 280 in Perminov's addition_reduced_ZT for the same 73 products, with no lower count cited on the live Lille 4x4x6 page and only a non-comparable naive count in COVERAGE.md.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
