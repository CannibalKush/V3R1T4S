# Criterion skeptic report: add-3x4x5-cr156

Checker: my own script (criterion_ws/chk.py, more.py), written before reading the author's. Object: claim/object/3x4x5_m47_cr156_ZT_reduced.json. All 8 claim files matched claim.SHA256SUMS (shasum -c, run from inside the claim folder).

## Clause 1: explicit straight-line program, format <n,m,p> with max dim <= 8
Quote: "an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format <n,m,p> with max(n,m,p) <= 8".
Met. Format 3x4x5 (max 5). U map: 12 inputs (A), 38 fresh forms, 47 factor forms. V map: 20 inputs (B), 44 fresh, 47 factor forms. W map: 47 product inputs, 23 fresh, 15 output forms (transposed C layout: output index k*3+i is C[i][k]).
Straight-line order: every term index refers only to an input or an earlier fresh variable (True for U, V and W). Every coefficient is +1 or -1. No form repeats an index.

## Clause 2: rank equals the live best rank in fmm_sota.json
Quote: "rank r equal to the best rank listed for that format in .../fmm_sota.json (re-fetched live)".
Met. Fetched once (HTTP 200, createdAt 2026-10-09T11:45:48). The only entry for [3,4,5] is rank 47 (exponent 2.821072). The object has m = 47.

## Clause 3: (1) verified symbolically to compute A*B exactly over Z
Met. My checker expanded every fresh variable and every final form to an integer linear form over the inputs. Expanded-coefficient check: every expanded coefficient of every fresh and final form in U, V and W lies in {-1,0,1} (ternary = True, True, True), so no non-ternary intermediate occurs. Full tensor identity (Brent equations, exact integers, every A[i][j]*B[l][q] coefficient slot of every output, with the transposed C layout): 0 violations. Evaluation on 50 random integer matrix pairs (entries -9..9), all 15 outputs: 0 mismatches.

## Clause 4: strictly fewer additions than Perminov's minimum reduced count
Quote: "STRICTLY LESS than the smallest reduced addition count ... counted under Perminov's 'reduced' convention ... The reference count is the MINIMUM cr value over all files for that format and rank in the live directory".
My count (one per binary +/-, negation free, sum over all fresh and final forms of terms-1): U = 38, V = 44, W = 74, total 156. The file's declared complexity (reduced 156, naive 277) agrees.
Calibration: I fetched Perminov's 3x4x5_m47_cr161_cn277_ZT_reduced.json once (HTTP 200, sha256 d1248a3a32dd03bf5d9216edfdaf6b01be95987d7cefee03f5f9f9645271319a, same as the author's record). My counter gives U = 39, V = 48, W = 74, total 161, equal to his cr161. His scheme also passes my ternary, order, Brent (0 violations) and random-evaluation (0 mismatches) checks, so the counter and checker are sound on a known object.
Same products: the expanded U rows, V rows and W matrix of the claim equal his exactly, row by row and in the same order. The 47 products are his. The W program (fresh and final lists) is identical to his (74 additions). Only the U and V programs differ: U saves 1 (39 to 38), V saves 4 (48 to 44), total saving 5.
Live directory: fetched the git tree once (HTTP 200, not truncated). Under schemes/results/addition_reduced_ZT/ there are 195 files and exactly one for 3x4x5 (or any permutation): 3x4x5_m47_cr161_cn277_ZT_reduced.json. Minimum cr = 161. The tree also has schemes/results/naive_addition_reduced_ZT/3x4x5_m47_c277_ZT.json (and .m). Those names carry c277 with no "cr", live in a different directory, and equal the "naive": 277 field of his own reduced file: a naive nonzero-based count without subexpression sharing, a different convention, so not comparable to reduced counts. 156 < 161. Met.
Not re-fetched by me: reduced_known.json, README, CHANGELOG (my brief named only the tree and the one file). The author's table-record lists reduced_known.json 3x4x5-47 as Z 276 / Z2 242 and no lower count in README/CHANGELOG; I did not confirm this independently. 276 is far above 156 in any case. This is a residual unchecked limit.

## Clause 5: below any count on the live Lille page and in COVERAGE.md
Lille: fetched https://fmm.univ-lille.fr/3x4x5.html once (HTTP 200). It lists <3x4x5:47>, the algorithm-type polynomial, and the AlphaTensor (Fawzi et al., Nature 2022) source. It cites no complexity variant and no operation or addition count for this rank (no commentaries section). Nothing there is lower than 156. Met (vacuously).
COVERAGE.md: fetched once (HTTP 200). Row for <3,4,5>: R/Q/Z column "47 Alphatensor-Z", adds column "+287". Its stated convention is naive nz(U)+nz(V)+nz(W) - 2r - n*p, not an SLP count. 287 > 156, and a different convention; no cell below 156. Met.
Coefficient class: the claim is ternary (Z); Lille/COVERAGE rank 47 has a Z entry, so the same-class comparison applies and is satisfied.

## Clause 6: scheme claimed once, not a rank target
Rank is the live best rank (47), not lower. Met as far as checkable from these sources (other claims of this scheme are outside my sources).

## Null models and corruptions (my checker, real output)
- Flipped one sign in u_fresh[3]: 11 Brent violations, 320 random mismatches, ternary check also fails. Rejected.
- Dropped one term from w[4]: 3 Brent violations, 43 random mismatches. Rejected.
- Swapped v rows 10 and 11: 36 Brent violations, 235 random mismatches. Rejected.
- Swapped output forms 0 and 1 (wrong C layout): 16 Brent violations, 98 random mismatches. Rejected.
- Doubled a term in u[0] (coefficient 2): ternary check fails, 5 Brent violations, 47 mismatches. Rejected.
- Perminov's reference file is accepted by the same checker with count 161.

## Verdicts
Full criterion: met on every clause I could check from the named sources. The win is real but narrow: a reduced-count improvement of 5 additions (161 to 156) on Perminov's own rank-47 products, with his W program reused unchanged and only the U and V programs improved. Not subsumed by any source fetched: the live directory minimum is 161, Lille cites no count, COVERAGE.md uses a naive convention.
Partial win p1: the bank's enumerated p1 is a rank-23 <3,3,3> SLP, which this claim is not. Under the brief's reading of p1 (strictly fewer than Perminov's live 3x4x5 count, same convention) it holds: 156 < 161. That is the same fact as clause 4, not a separate win. The claim meets the full criterion, not only p1.

confirmed_scope: The program claim/object/3x4x5_m47_cr156_ZT_reduced.json (sha256 e5731a01ecf58de14b5fc4a6e9a0de880b11146aeeeef4df6844dd83bfbb83a8) is a ternary straight-line program (all expanded forms in {-1,0,1}) computing the exact 3x4 by 4x5 integer matrix product with the same 47 products as Perminov's 3x4x5_m47_cr161 file (rank 47 equals the fmm_sota.json best), using 156 additions under his reduced convention (U 38, V 44, W 74, W program unchanged from his), against his live-directory minimum of 161 and no lower count on the Lille 3x4x5 page or in COVERAGE.md (naive +287), as fetched on 2026-10-15.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
