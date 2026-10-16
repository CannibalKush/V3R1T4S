# Criterion skeptic report: 2x4x8 rank 51, 181 reduced additions

Method: I wrote my own checker (criterion_ws/chk.py) from the criterion before reading the author's. It parses the program, enforces straight-line order (a reference to a not-yet-computed index raises), accepts only +1/-1 term values, expands every fresh variable and every final form to an exact integer vector over the inputs, tests the ternary condition on all expanded vectors, tests the full tensor identity for 2x4 times 4x8 (output index l*2+i is C[i][l], the transposed layout), evaluates 50 random integer matrix pairs, and counts additions as the sum of (terms - 1) over all fresh and final forms. The claim folder hashes all verified OK against claim.SHA256SUMS.

## My checker on the claimed object

- Straight-line order and +/-1 term values: pass (no exception).
- Expanded coefficients: maximum absolute value over all 37+67+21 fresh variables and all 51+51+16 final forms is 1, so every expanded intermediate and final form is ternary. Pass.
- Tensor identity (all 8 x 32 x 16 index triples): exact, tensor = True. Random integer evaluation: True.
- Additions per map: U 37, V 67, W 77, total 181. Matches the declared 181.
- The file's key `n: 3` is unused by my checker; the format comes from the 8 / 32 / 16 sizes, and the identity holds for 2x4x8.

## Calibration on Perminov's file

I fetched 2x4x8_m51_cr188_cn354_ZT_reduced.json once (sha256 b68445935df00311217280a30d628395594619584691d8264723045b2b62131a, same as the author's record). My counter gives U 38, V 72, W 78, total 188, equal to its declared 188; it is also ternary, and satisfies the tensor identity and random evaluation. The expanded U, V and W rows (the 51 products) are identical to the claim's, row for row. All six program lists (u_fresh, u, v_fresh, v, w_fresh, w) differ from his, so no map's program is identical to his: the claim re-optimises all three maps on his scheme. Naive count from the expanded rows is 472 - 102 - 16 = 354, equal to his cn354 and to the COVERAGE value.

## Clauses

1. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)", max dim <= 8: fmm_sota.json (createdAt 2026-10-09T11:45:48) lists format [2,4,8] rank 51. Claim rank 51, max dim 8. MET.
2. "(1) verified symbolically to compute the full product A*B exactly over Z": exact integer tensor identity and 50 random integer evaluations pass; the program is ternary so it is valid over Z. MET.
3. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository ... re-fetched live": the recursive tree (not truncated, 321 files under addition_reduced_ZT) holds exactly one file for 2x4x8, and no permutation of the format: cr188. Its reduced_known.json has no 2x4x8 key, and the README (line with 2x4x8, ranks 51) and CHANGELOG give no lower addition count. 181 < 188. MET. Files in that directory named _cNNN_ZT without cr (126 of them, for example 2x4x11_m71_c430_ZT.json) are naive counts under another convention (nonzeros minus 2r minus np, ignoring shared subexpressions), not the reduced convention, so they do not compare. No such file exists for 2x4x8 anyway (the naive 354 appears only as cn354 in the cr188 file name and in COVERAGE).
4. "counted under Perminov's 'reduced' convention (each binary +/- ... one; multiplication by -1 free; other scalars not allowed)": my sum of (terms - 1) gives 181, and the same counter gives 188 on his file. Every expanded form is in {-1,0,1}. MET.
5. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant": the page https://fmm.univ-lille.fr/2x4x8.html shows rank 51, attributed to AlphaEvolve (Novikov et al., 2025), and an "algorithm type" polynomial (monomial coefficients, a shape descriptor). It cites no addition count or operation count and no best-known-complexity variant for this rank. Nothing lower exists to beat. MET (vacuous).
6. matmulcatalog COVERAGE.md "adds" column: the row for the format <2,4,8> reads "+354". Its legend defines adds as nz(U)+nz(V)+nz(W) - 2r - n*p, a naive count with no shared subexpressions, a different convention. 354 is not lower than 181 anyway. MET.
7. "If the Lille rank is attained only with non-ternary coefficients, compare in the same class": the scheme is ternary and Perminov's reference is in the same class (ZT). MET.
8. "The reference count is the MINIMUM cr value over all files for that format and rank": only one file, cr188, so the minimum is 188. MET.
9. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": the rank is 51, equal to the live best, not lower. MET.

## Null models and corruptions (all rejected)

- Flip one sign in a final U form: tensor False, random False.
- Drop one term from a W form: tensor False, random False.
- Swap two W outputs: tensor False, random False.
- Flip one sign in a V fresh variable: tensor False, random False, and an expanded coefficient leaves {-1,0,1} (ternary False).
- Duplicate a term in a fresh form (coefficient 2): ternary False, tensor False.
- Forward reference to a later fresh index: rejected by the straight-line check.

The checker accepts the real object and rejects every corruption.

## Verdicts

Full criterion: met on every clause checkable from these sources. The enumerated partial win p1 is about <3,3,3> rank 23 (58 additions). The claim is for 2x4x8, so the stated p1 is not met in its enumerated form. Read as the lead's definition (strictly fewer than Perminov's live 2x4x8 count under the same convention), it is true: 181 < 188.

p1 (as defined by the lead): the claim is strictly fewer than Perminov's live 2x4x8 count, 181 against 188, same convention: true. The full criterion is also met, so p1 is subsumed by the full win rather than separate.

Limits: the checks cover this rank-51 scheme (his products, taken from AlphaEvolve via Lille) only. The claim does not lower the rank and I did not judge literature novelty. Counts are in the reduced convention only.

confirmed_scope: claim/object/2x4x8_m51_cr181_ZT_reduced.json (sha256 e5f0f3807baaa5f00a76f606bd33199db83dfd83ef82c21abbcb0fbc79c02d95) is a ternary straight-line program that exactly computes the full 2x4 times 4x8 product over Z with Perminov's own 51 products, using 181 additions under the reduced convention (U 37, V 67, W 77), against 188 for his only live 2x4x8 file, with no lower addition count on the Lille page, in reduced_known.json, or in COVERAGE.md, as fetched on 2026-10-15.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
