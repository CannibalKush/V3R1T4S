# Criterion skeptic report: add-2x5x5-cr147

All numbers below come from my own checker (criterion_ws/chk.py, written before reading the author's checker, which I did not read) run on the claim object and on live fetches made once each with the honest User-Agent, no retries.

## Own checker output
Claim object, claim/object/2x5x5_m40_cr147_ZT_reduced.json:
- Straight-line order: every form references only inputs or strictly earlier fresh variables; all coefficients are +1 or -1; no duplicate terms in a form. PASS.
- Expanded over the inputs with exact integers, every fresh variable and every final form: max |coefficient| = 1 (ternary at every intermediate). PASS.
- Full Brent tensor identity for 2x5 times 5x5 over all 10*25*10 index triples, 40 products, output k*n+i = C[i][k] (transposed layout): exact, PASS. Direct SLP evaluation on 200 random integer matrices: all outputs equal A*B, PASS.
- Reduced count (sum of terms-1 over fresh and final forms, negation free): U 31, V 54, W 62, total 147. Matches the declared 147.

## Calibration on Perminov's file
Fetched 2x5x5_m40_cr153_cn283_ZT_reduced.json (sha256 89296c6d...1bab, matches the author's record). My counter: U 34, V 55, W 64, total 153 = declared 153. It also passes the ternary, tensor and random checks.
The expanded U, V and W product rows of the claim equal Perminov's exactly (U, V, W all identical). The programs differ in every map (no map's program is identical to his). So the scheme is his; only the addition programs are new, and each map is cheaper (31<34, 54<55, 62<64).

## Clauses
1. "format <n,m,p> with max <= 8": 2x5x5, max 5. Met.
2. "rank r equal to the best rank in fmm_sota.json (re-fetched live)": entry for [2,5,5] rank 40 (file sha d0da2c36...); claim rank 40. Met.
3. "(1) verified symbolically to compute A*B exactly over Z": exact integer expansion and tensor identity above. Met.
4. "(2) STRICTLY LESS than the smallest reduced addition count ... counted under Perminov's reduced convention ... reference is the MINIMUM cr over all files": live tree (not truncated) has exactly one addition_reduced_ZT file for 2x5x5: ..._m40_cr153_cn283_ZT_reduced.json, so the minimum cr is 153; 147 < 153. Met. Convention check: my counter reproduces 153 on his file. Files named _cNNNN_ZT without "cr" are naive counts (nonzeros-based, not the sum of terms-1 over a CSE program), a different convention, so they do not compare; none exist for 2x5x5 rank 40 in this tree anyway. I did not re-fetch reduced_known.json, README or CHANGELOG (outside my allowed sources); the author's table record lists reduced_known 2x5x5-40 Z 313 (a different, larger convention number) and no lower stated count. That part rests on the author's record.
5. "AND below any lower count published on the live Lille per-format page's cited complexity variant": the live page fmm.univ-lille.fr/2x5x5.html (sha b1284cd1...) gives rank 40 from Hopcroft-Kerr style citation text and links to tensor, LRP, raw and symmetry files; it cites no complexity variant and no operation count. Nothing lower to beat. Met (vacuously).
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": the row for <2,5,5> shows "+256". The column is defined there as nz(U)+nz(V)+nz(W) - 2r - n*p (naive count). Different convention, not comparable with a reduced count; it is not a lower published reduced count. 147 < 256 numerically anyway. Met.
7. "If the Lille rank is attained only with non-ternary coefficients, compare in the same class": the claim and Perminov's reference are both ternary Z, same class. Met.
8. "Each scheme is claimed once; a scheme that also lowers the rank is a rank target": rank is unchanged at 40. Met.
9. Hidden quantifier check: the criterion asks "strictly less than the minimum", which is the weakest-looking clause; I found no stretched definition. The one soft point is that "scheme is Perminov's" means the win is purely an SLP improvement (CSE) on his product set, which the criterion permits.

## Null models and corruptions (all rejected)
- Flipped one sign in a W output term: tensor identity fails, random evaluation fails.
- Dropped a term from a U final form (count falls to 146): tensor identity fails, random fails.
- Swapped one index in a V fresh form: tensor identity fails, random fails.
- Forward reference in a U fresh form: rejected structurally.
- Coefficient 2 in a W form: rejected structurally (non-ternary).
- Swapped two output rows (wrong layout): tensor identity fails, random fails.

## Verdicts
Full criterion: met. A genuine, strict improvement of Perminov's only 2x5x5 rank-40 reduced count (153 to 147, exact, ternary throughout), on the same product set. Nothing on the Lille page or in COVERAGE.md is a lower comparable count.
Partial win p1, as the brief defines it (strictly fewer than Perminov's live 2x5x5 count, same convention): met, 147 < 153. The bank's own enumerated p1 is about <3,3,3> and is not addressed by this claim; the full criterion is the operative test.

p1: true
confirmed_scope: claim/object/2x5x5_m40_cr147_ZT_reduced.json (sha256 62737a117df29bc9dc6194509ed47f95a6f763ea3ca21fca84f79a78c44e6e1a) is an exact ternary straight-line program for the rank-40 <2,5,5> scheme with Perminov's product set using 147 reduced additions (U 31, V 54, W 62), strictly below the 153 of his only live addition_reduced_ZT file for that format and rank, with Lille's page citing no operation count and COVERAGE.md's adds column being a naive count under another convention.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
