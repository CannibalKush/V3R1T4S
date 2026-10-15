# Criterion skeptic report: add-4x6x7-cr469

Source integrity: the hash list verifies for all 8 files in the claim folder (run from inside the claim folder, all OK).
Object sha256 (from the hash list): ade76c2eef28cca082e6f87f2ca0294f6a6e5bcdce1e1cb9356fe068bab0dd65.

## My own checker (criterion_ws/chk.py, pure Python, written before reading the author's)
Output on claim/object/4x6x7_m123_cr469_ZT_reduced.json:
{'n': (4, 6, 7), 'r': 123, 'adds': 469, 'U': 114, 'V': 140, 'W': 215, 'nonternary_forms': (0, 0, 0), 'tensor': True, 'random': True, 'fresh': (114, 140, 74)}

- Straight-line order: every term index refers to an input or an earlier fresh variable (asserted); every coefficient is +1 or -1 (asserted); no repeated index inside a form (asserted).
- Ternary condition: every fresh variable and every final form was expanded to an exact integer linear form over the inputs; zero forms have an expanded coefficient outside {-1,0,1} (nonternary_forms = (0,0,0) for U, V, W).
- Tensor identity: sum over the 123 products of U[t][a] V[t][b] W[c][t] equals exactly the 4x6x7 matrix-multiplication tensor, with the C-transposed output layout (output l*4+i is C[i][l]); 168 nonzero entries, no extras. True.
- Random evaluation: 20 random integer matrix pairs (entries -9..9), program output equals A*B. True.
- Count (sum of terms-1 over all fresh and final forms, negation free): 469 = U 114 + V 140 + W 215.

## Calibration
Perminov's 4x6x7_m123_cr517_cn1586_ZT_reduced.json (one fetch, HTTP 200): my counter gives 517 (U 128, V 164, W 225), tensor True, random True, nonternary (0,0,0). The expanded U, V and W rows (all 123 products and all 28 outputs) are identical between the claim and Perminov's file, so only the programs differ (fresh counts 114/140/74 versus 53/71/119). The file's own complexity field says reduced 517 (claim: 469), naive 1586 in both.

## Null models (all rejected by the same checker)
- flipped sign in w[5][0]: tensor False, random False.
- term added to a one-term v form (count 470): tensor False.
- term dropped from a fresh u form (count 468): tensor False.
- two u rows swapped: tensor False (count unchanged 469, so the count alone would not catch it).
- one w index shifted: tensor False.
- coefficient set to 2: assertion (non-ternary).
- forward reference to a later variable: assertion (order).
- form repeating an index: assertion (duplicate).

## Clauses
1. "an explicit straight-line program ... for a format <n,m,p> with max(n,m,p) <= 8": 4x6x7, max 7. Met.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": fetched once, HTTP 200; the entries list has exactly one entry for [4,6,7]: rank 123. The object has m=123. Met.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": exact integer expansion and tensor identity (above). Met.
4. "(2) strictly less than the smallest reduced addition count ... in Perminov's live repository, under the reduced convention; multiplication by any other scalar not allowed": tree fetched once (HTTP 200, not truncated). addition_reduced_ZT holds 195 files, none lacks a cr value; the only 4x6x7 file there is cr517 (no other permutation of the format appears). The minimum cr is 517; 469 < 517. The count follows the reduced convention (calibrated to 517 on Perminov's own file) and no non-ternary scalar appears, including in intermediates. The files named _cNNNN_ (c1562, c1586) are in the separate naive_addition_reduced_ZT directory, not in addition_reduced_ZT; they are naive nonzero-based counts (c1586 equals the cn1586 naive field), a different convention that does not compare with reduced counts. I did not independently fetch reduced_known.json, README or CHANGELOG (outside the named fetch list); the author's record says reduced_known has no entry for 4x6x7-123 and the other two state no lower count. Met on the sources I checked.
5. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant": Lille 4x6x7 page fetched once (HTTP 200). It lists rank 123 (Kauers-Wood, arXiv 2505.05896) and an "Algorithm type" polynomial in X,Y,Z (45 X^2Y^2Z^2 + ...), which is an algorithm-structure description, not an addition or operation count; no commentary or best-known-complexity variant is cited. No count to beat. Met (vacuously).
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": fetched once (HTTP 200). The 4x6x7 row shows +1586, and the header defines adds as nz(U)+nz(V)+nz(W) - 2r - n*p, a naive count. 469 < 1586 numerically, and the convention differs, so no lower reduced count is published there. Met.
7. "If the Lille rank is attained only with non-ternary coefficients, compare in the same class": the scheme is over Z with ternary coefficients and the program is ternary, so same class. Met.
8. "The reference count is the MINIMUM cr over all files for that format and rank": one file, 517. Met.
9. "Each scheme is claimed once; a scheme that also lowers the rank is a rank target": rank is 123, equal to the sota rank, not lower. Met.

Scope limits I note: the products are Perminov's (the claim only replaces the addition programs); the criterion does not require new products. Whether 469 is new in the literature beyond these sources is not judged here.

## Partial win p1
p1 as written concerns a rank-23 SLP for <3,3,3>, which this claim is not. The prompt's reading of p1 (strictly fewer than Perminov's live 4x6x7 count, same convention) is met: 469 < 517. It is subsumed by the full criterion here, which is also met.

p1: true
confirmed_scope: claim/object/4x6x7_m123_cr469_ZT_reduced.json (sha256 ade76c2eef28cca082e6f87f2ca0294f6a6e5bcdce1e1cb9356fe068bab0dd65) is a ternary straight-line program that, by my exact integer expansion, computes the 4x6x7 product with 123 products (the same products as Perminov's cr517 file, equal to the fmm_sota.json rank) using 469 reduced additions (U 114, V 140, W 215), below the sole live addition_reduced_ZT count of 517, with no Lille operation count and only a naive 1586 count in COVERAGE.md to beat.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
