# Criterion skeptic report: add-6x6x7-cr695

Own checker: criterion_ws/chk.py (written before reading the author's). It parses the program, checks straight-line order and +/-1 coefficients, expands every fresh and final form to an integer vector over the inputs, requires every expanded coefficient in {-1,0,1}, checks the full Brent tensor identity for 6x6 times 6x7 (all 36*42*42 entries, C-transposed output layout: output k*6+i is C[i][k]), evaluates on 20 random integer matrix pairs, and counts sum(terms-1) over all fresh and final forms.

All 8 files match claim.SHA256SUMS (shasum -c: OK).

## Own checker output on the claim object
- Straight-line order and +/-1 coefficients: pass.
- Expanded ternary check on all 184+182+119 fresh forms and all final forms: every coefficient in {-1,0,1}, pass.
- Tensor identity (exact integers): pass. Random integer evaluation (20 trials): pass.
- Count: per map U=184, V=182, W=329, total 695.

## Calibration on Perminov's file (fetched once, curl, honest User-Agent)
6x6x7_m183_cr769_fv370_cn2502_ZT_reduced.json: same checker passes the tensor identity and ternary check and gives U=209, V=208, W=352, total 769, matching its name. The expanded U, V, W rows (183 products) are identical to the claim's, in the same order. Only the programs differ (695 vs 769).

## Clauses
1. "explicit straight-line program ... for a format <n,m,p> with max(n,m,p) <= 8": met (6,6,7).
2. "rank r equal to the best rank in fmm_sota.json (re-fetched live)": met. Live entry {format [6,6,7], rank 183}; claim rank 183.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": met (exact integer expansion, tensor identity, random evaluation). The ternary condition on every intermediate also holds.
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository, reduced convention": met. Live git tree (not truncated) holds exactly one addition_reduced_ZT file for 6x6x7: m183 cr769. Minimum cr is 769; 695 < 769. The other 6x6x7 files are in ZT/ (no counts) and naive_addition_reduced_ZT/6x6x7_m183_c2493_ZT (no "cr"). Files named _cNNNN_ZT without "cr" use the naive convention nz(U)+nz(V)+nz(W)-2r-np over the unreduced scheme, a different quantity from the reduced SLP count, so they do not compare. (I did not re-fetch reduced_known.json, README or CHANGELOG; the author's record lists no 6x6x7-183 reduced cell and no lower count. This is accepted from the author's record only.)
5. "below any lower count published on the live Lille per-format page's cited complexity variant": met. The live 6x6x7 page (fetched once) shows rank 183 from Kauers and Wood (arXiv 2505.05896) and an "Algorithm type" polynomial in X, Y, Z. It cites no complexity variant or operation count for this rank. Nothing to be below.
6. "and in matmulcatalog's live COVERAGE.md adds column": met. Row for <6,6,7> reads 183 (Dronperminov-ZT) with adds "+2493". That is the naive count (nz(U)+nz(V)+nz(W)-2r-np per the file's own legend), equal to the c2493 file; it is a different convention, and 695 < 2493 anyway. No lower count is published.
7. Coefficient class: Perminov's 183 is ZT (ternary, Z) and the claim is ternary; same class. Lille rank is not attained only with non-ternary coefficients here.
8. "reference count is the MINIMUM cr over all files for that format and rank": 769 (single file).
9. "scheme claimed once; a scheme that also lowers the rank is a rank target": met, the rank stays 183 (products identical to Perminov's).

## Null models (all rejected by the checker, output in criterion_ws/nulls.txt)
- flipped sign in w_fresh[0]: rejected (tensor identity fails).
- dropped term in u_fresh[5]: rejected (tensor identity fails).
- swapped v rows 3 and 4: rejected (tensor identity fails).
- shifted index in w[10]: rejected (non-ternary expanded final form).
- forward reference in u_fresh[0]: rejected (straight-line order).
- duplicated term in u_fresh[0] (coefficient 2): rejected (non-ternary).

## Hidden quantifier / stretch notes
- The 695 is the reduced count under the stated convention, counting every fresh and final form (including all 184 U and 182 V fresh entries). Calibration on Perminov's file with the same counter reproduces his stated 769, so the conventions are the same.
- The gain is entirely in the program (same 183 products). The improvement is 74 additions (about 9.6 percent) from 769.
- The comparison is only as live as the 2026-10-15 fetches; the Perminov reduced_known/README/CHANGELOG clause rests on the author's record.

## Verdicts
Full criterion: met on every clause checkable from these sources.
p1 (the 3x3x3 rank-23 partial win) concerns a different format and is not what this claim is; the claim does not meet it. The same-format "strictly fewer than Perminov's live 6x6x7 count, same convention" reading is met (695 < 769), but that is the full criterion itself, not the named p1.
p1: false

confirmed_scope: claim/object/6x6x7_m183_cr695_ZT_reduced.json (sha256 34a5c13ccfa01ac91606b8899c53be5f1facf7f62f1e06e9ddf5f9ec6bf82ea5) is a ternary straight-line program that, by exact integer expansion, computes the 6x6 by 6x7 product with the same 183 products as Perminov's cr769 file using 695 additions under the reduced convention (U 184, V 182, W 329), below the single live addition_reduced_ZT value of 769, with no lower count on the Lille page or in COVERAGE.md.

context: Claude Code subagent (Fable 5.1), fresh context

p1: false
pass: true
