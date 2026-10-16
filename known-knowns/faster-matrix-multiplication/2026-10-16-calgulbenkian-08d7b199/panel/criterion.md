# Criterion skeptic report: add-4x5x5-cr281

Sources read: the claim folder and claim.SHA256SUMS (all eight hashes verified OK with shasum -a 256 -c), plus one fetch each of the five named live sources (stored under criterion_ws/). My checker is criterion_ws/chk.py (own code, written before reading the author's checker, which I did not run or use); the comparison and corruption driver is criterion_ws/cmp.py.

## Own checker output (object: claim/object/4x5x5_m76_cr281_ZT_reduced.json)

- Layout: n = [4,5,5], m = 76 products, U inputs = 20 (A row-major), V inputs = 25 (B row-major), W inputs = 76 products, 20 outputs; output k*4+i is C[i][k] (transposed layout).
- Straight-line order: every term in every form references an input or an earlier fresh variable only; every coefficient is +1 or -1. No violations.
- Ternary condition: every fresh variable and every final form was expanded to an exact integer linear form over the inputs; every expanded coefficient lies in {-1,0,1}. No violations (errors: 0).
- Full tensor identity: the 76 product factors and 20 outputs were expanded into the tensor T[a][b][c] = sum over products of U*V*W and compared at all 20*25*20 = 10000 positions with the 4x5 times 5x5 Brent target (with the C-transposed output index). Brent violations: 0.
- Random integer evaluation: the SLP itself (not the expansion) run on 20 random integer matrix pairs in [-9,9], all 20 output entries equal A*B each time. No mismatch.
- Count (one per binary +/-, negation free, sum of terms-1 over all fresh and final forms): U 75, V 84, W 122, total 281. Fresh variables: 75 / 84 / 31. Matches the file's own complexity field (reduced 281, naive 530).

## Calibration on Perminov's file (4x5x5_m76_cr299_fv112_cn530_ZT_reduced.json, fetched once)

- My checker passes it with 0 errors (straight-line, ternary, Brent, random evaluation) and my counter gives U 76, V 93, W 130, total 299. Calibration holds.
- Expanded U rows, V rows and W rows of the claim equal Perminov's exactly, row by row in the same order (U equal True, V equal True, W equal True). So the 76 products are his scheme.
- The programs differ in all three maps: claim u/u_fresh, v/v_fresh and w/w_fresh are each not identical to his (his fresh counts 40/34/38 against the claim's 75/84/31). No map's program is identical to his. Per-map counts claim vs his: U 75 vs 76, V 84 vs 93, W 122 vs 130.

## Null models and corruptions (all run through my checker)

- Flipped sign of one W term: rejected (non-ternary expansion, 23 Brent violations).
- Dropped one W term: rejected (3 Brent violations, random evaluation mismatch).
- Swapped two U output indices: rejected (24 Brent violations, mismatch).
- Coefficient 2 inserted in a V fresh form: rejected (coef 2 and non-ternary).
- Forward reference in a U fresh form: rejected (out-of-order reference).
- Two W outputs swapped (wrong transposed layout): rejected (20 Brent violations).
- Fresh form summing the same input twice (non-ternary expansion): rejected.
Seven of seven corruptions rejected; the uncorrupted object accepted.

## Clauses

1. "explicit straight-line program ... for a format <n,m,p> with max(n,m,p) <= 8": 4x5x5, max 5. MET.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": fmm_sota.json fetched (createdAt 2026-10-09T11:45:48) lists format [4,5,5] rank 76 (exponent 2.82122); the claim has rank 76. MET. (It does not lower rank, so it is not a rank target.)
3. "(1) verified symbolically to compute the full product A*B exactly over Z": exact integer expansion, full tensor identity and random evaluation all pass; ternary on every intermediate. MET.
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository ... MINIMUM cr value over all files for that format and rank": the live git tree (recursive listing, not truncated) has exactly one 4x5x5 file in addition_reduced_ZT, with cr299; so the minimum cr is 299 and 281 < 299. The tree also has naive_addition_reduced_ZT/4x5x5_m76_c528_ZT and c532 files; these carry NNN counts without "cr" and are naive counts (non-zero entry style count over the whole scheme with its own convention, no common-subexpression reuse), a different convention and magnitude (528 vs 530/299), so they do not compare to a reduced count. Not lower under the reduced convention either way. Limit: I did not fetch reduced_known.json, README or CHANGELOG (the brief names only the file listing and the cr299 file); the 4x5x5 reduced figure there was not checked by me. MET on the evidence fetched.
5. "AND below any lower count ... on the live Lille per-format page's cited complexity variant": fmm.univ-lille.fr/4x5x5.html (fetched once) cites only the Nature 2022 AlphaTensor source for 4x5x5:76 and an "Algorithm type" polynomial (a shape signature of the tensor decomposition), no complexity variant and no operation count for this rank. There is no cited count to beat. MET (vacuously).
6. "matmulcatalog's live COVERAGE.md 'adds' column": the 4x5x5 row shows R/Q/Z 76 and adds +549. Its convention is naive nz(U)+nz(V)+nz(W)-2r-n*p, not reduced. 281 < 549, and the naive-convention count of the claim itself (530 in its own field, a different formula) is not what is compared. Not a lower count. MET.
7. "If the Lille rank is attained only with non-ternary coefficients, compare in the same class": the scheme is ternary (Z), comparison is in-class. MET.
8. "Each scheme is claimed once": the scheme is not a rank improvement and is Perminov's own scheme with a better program. No evidence of earlier claim in my sources. MET as far as I can tell.

## Verdicts

Full criterion (as checkable from these sources): met. The win is an addition count only; the claim's products are Perminov's own, so nothing about the scheme itself is new, and novelty beyond the sources named here is not judged.

p1: the brief defines p1 as strictly fewer than Perminov's live 4x5x5 count under the same convention: 281 < 299, met. Note the bank's enumerated p1 text is the 3x3x3:23 target (58 additions), which this claim does not address; p3 (three formats) is also not met. The full criterion is met on its own terms, so the claim is not merely a partial win.

confirmed_scope: claim/object/4x5x5_m76_cr281_ZT_reduced.json (sha256 08d7b199e9ecc9f7254dc46c23ecf2128e83444277b19eac6bbcb678a107f819) is a ternary straight-line program that, by my own exact checker, computes the full 4x5 by 5x5 product over Z with Perminov's 76 products (expanded U, V, W rows identical to his) using 281 additions under the reduced convention (U 75, V 84, W 122), against 299 in the only 4x5x5 file of his live addition_reduced_ZT directory, with no cited count on the Lille 4x5x5 page and COVERAGE.md giving only a naive +549.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
