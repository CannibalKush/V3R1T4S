# Criterion skeptic report: add-4x5x7-cr379

I wrote my own checker (criterion_ws/chk.py) from the criterion before using the author's. It checks straight-line order, that every coefficient is +1 or -1, exact integer expansion of every fresh and final form with a ternary test on every expanded form, the full Brent identity for 4x5 times 5x7 (C-transposed output index k*4+i for C[i][k]), 20 random integer matrix evaluations, and the reduced count (sum of terms minus 1 over all fresh and final forms).

## Evidence from my checker (real output)

- Claim object: `OK {'u': 91, 'v': 113, 'w': 175} 379`; 104 U rows, 104 V rows, 28 W rows. Per map: U 91, V 113, W 175, total 379. Straight-line order, +-1 coefficients, ternary expansion of every intermediate and output, full tensor identity, and random evaluation all pass. Forms never repeat an index within a form.
- Calibration on Perminov's file 4x5x7_m104_cr400_fv163_cn931_ZT_reduced.json (fetched once): `OK {'u': 97, 'v': 120, 'w': 183} 400`. My counter gives 400, matching the file name and its stored reduced field.
- Expanded U, V and W rows (all 104 products and 28 outputs, in order) are identical between the claim and Perminov's file. The fresh/final programs differ in all three maps (U 91 vs 97, V 113 vs 120, W 175 vs 183). So no map's program is identical to his; the claim is the same scheme with a shorter program in each map. The claim's own stored complexity field says reduced 379 and naive 931, equal to his naive 931.
- Null models, each rejected by my checker: flipped sign in a fresh U form (non-ternary expansion); dropped term in a W fresh form (tensor identity fails); changed index in a V factor (tensor fails); forward reference (order check); coefficient 2 (coefficient check); dropped term in an output (tensor fails); swapped two outputs, a layout error (tensor fails); duplicate index within a form (rejected). Baseline unchanged passes.

## Clauses

1. "explicit straight-line program ... for a format with max(n,m,p) at most 8": met. The format is 4x5x7, max 7, in Perminov's JSON layout.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": met. The live file has one entry for 4x5x7 with rank 104; the claim has m = 104.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": met by exact integer expansion and the full tensor identity, checked on every (a, b, c) triple, plus random integer evaluation. (I did not run a sympy pass; exact integer expansion of all linear forms plus the complete tensor identity is a symbolic verification.)
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository ... the MINIMUM cr value over all files for that format and rank": met. The live tree listing (not truncated) has exactly one file in addition_reduced_ZT for 4x5x7 rank 104, with cr400, and none for any permutation of the format. 379 below 400. The two other 4x5x7 m104 files are in naive_addition_reduced_ZT and are named c924 and c927 with no "cr"; they are naive counts (nonzero-based, as the COVERAGE and naive field convention) and do not compare to the reduced convention, where shared subexpressions cost one addition. I did not fetch reduced_known.json, README or CHANGELOG myself (outside the named fetches); the author's record says they hold no lower count, and the live directory minimum is the stated reference.
5. "counted under Perminov's reduced convention ... multiplication by any other scalar is not allowed": met. My counter is calibrated to 400 on his file, all coefficients are +-1, and every expanded intermediate is in {-1,0,1}.
6. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant": met. The live page https://fmm.univ-lille.fr/4x5x7.html lists rank 104 (Kauers and Wood, arXiv 2505.05896) and a bivariate complexity polynomial in X, Y, Z (36 X^2 Y^2 Z^2 + ... ), which is a count-by-structure variant, not an addition count for a ternary SLP. It cites no addition or operation count that can sit below 379, so nothing is lower than the claim. The page does not say whether its rank-104 algorithm is ternary; the claim is ternary and the comparison class is Z/ternary.
7. "and in matmulcatalog's live COVERAGE.md 'adds' column": met. The row for 4x5x7 shows 104 in F2 and R/Q/Z with adds +927. This is the naive count nz(U)+nz(V)+nz(W) - 2r - n*p, not a reduced SLP count, so 927 is not a lower count; and 379 below 927 anyway.
8. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": met. The rank is 104, equal to the best, not lower.

## Verdicts

p1 is the 3x3x3 rank-23 partial win; it does not apply to a 4x5x7 object. The brief's "p1" here is the same-format condition (strictly fewer than Perminov's live 4x5x7 count of 400, same convention): met, 379 below 400. The enumerated p1 of the bank text (3x3x3) is not what this claim shows.

The claim meets the full success criterion as checkable from these sources, under the stated caveats (Lille page gives no addition count; reduced_known.json, README and CHANGELOG not independently fetched by me).

Margin note: the win is on the program only; the 104 products are Perminov's. It is a single format at one rank.

confirmed_scope: claim/object/4x5x7_m104_cr379_ZT_reduced.json (sha256 b3b9b009a9de20414ff66a9309bc4092c31b6ad74a3aec0e235e470cd5d07335) is a ternary straight-line program that exactly computes the 4x5 by 5x7 product over Z with Perminov's own 104 rank products, and counts 379 reduced additions (U 91, V 113, W 175) against his live 400 for this format and rank, as of 2026-10-15.

context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
