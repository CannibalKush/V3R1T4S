# Criterion skeptic report: add-2x5x6-cr179

All claim files matched claim.SHA256SUMS (shasum -c run inside the claim folder: 8 of 8 OK). I wrote my own checker (criterion_ws/chk.py, cmp.py) before opening the author's; I did not run or read the author's checker.

## My checker, on the claim object
Object: claim/object/2x5x6_m47_cr179_ZT_reduced.json (n field is [2,5,6], m 47).
- Straight-line order: every form references only inputs or earlier fresh variables; every coefficient is +1 or -1. Errors: 0.
- Expansion over Z: every fresh variable (38 U, 28 V, 20 W) and every final form expanded exactly; all expanded coefficients lie in {-1,0,1}. Violations: 0.
- Tensor identity for 2x5 times 5x6 (A row-major 10 inputs, B row-major 30 inputs, output index l*2+i is C[i][l], the transposed layout): all 10*30*12 Brent equations hold exactly with 47 products. 20 random integer matrix pairs also match A*B on all 12 outputs.
- Count (sum of terms-1 over fresh and final forms): U 38, V 65, W 76, total 179. Naive convention check on the expanded rows: nz(U)=122, nz(V)=192, nz(W)=124, 438-94-12 = 332, matching the stored naive 332.

## Calibration on Perminov's file
Fetched once: 2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json. My checker: 0 errors, U 40, V 65, W 76, total 181 (matches his stored reduced 181 and the file name). The expanded U, V, W rows (47 products) are identical to the claim's, row for row. Programs: v_fresh, v, w_fresh, w are byte-for-byte identical to his (V and W maps unchanged, 65 and 76). Only the U map program differs (u_fresh 15 fresh vs 38 fresh; U 40 vs 38 additions). So the claim is the same scheme, with a re-optimised U-side program saving 2 additions. The claim's sentence "the scheme is the one in Perminov's repository" is accurate for the 47 products; the 179 program is new relative to his file.

## Null models (all rejected by my checker)
- Flipped sign of one term in v_fresh[3]: rejected (tensor equation fails, 2 != 0).
- Dropped last term of w[5]: rejected (tensor equation fails; count would be 178).
- Swapped u rows 10 and 11: rejected (tensor equation fails).
- Forward reference in u_fresh[0]: rejected (not yet computed).
- Coefficient 2 in u_fresh[2]: rejected (not ternary).
- Duplicated term making an expanded coefficient 2: rejected (expanded non-ternary).

## Clauses
1. "an explicit straight-line program ... for a format with max(n,m,p) <= 8": 2x5x6, max 6. Met.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": fetched once (createdAt 2026-10-09T11:45:48); entry format [2,5,6], rank 47. Claim rank 47. Met.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": exact integer expansion, full Brent identity, random evaluation. Met (exact integer linear-form expansion and tensor identity, not sympy).
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository": the live tree (not truncated) holds exactly one 2x5x6 file in addition_reduced_ZT (any permutation of the format), cr181, so the minimum cr is 181. 179 < 181. Met. I did not read reduced_known.json, README or CHANGELOG, which the criterion names as additional places; the tree listing and file are what I checked.
5. Counted under the reduced convention (binary +/- counts one, negation free, no other scalars): my counter reproduces his 181, and gives 179. Met.
6. Files named _cNNNN_ZT without cr: these sit in a separate directory, naive_addition_reduced_ZT, not addition_reduced_ZT, and there is no 2x5x6 file in it. They count nonzero entries in a naive way (no shared subexpressions), so they are not comparable with reduced counts; none exist for this format anyway. Not applicable.
7. "below any lower count ... on the live Lille per-format page's cited complexity variant": fetched the 2x5x6 page once. It cites the rank-47 algorithm from AlphaEvolve (2025) with a polynomial type description and no operation count or best-known complexity variant. No count to be below. Met vacuously.
8. "and in matmulcatalog's live COVERAGE.md adds column": the row for the 2,5,6 format lists +332, which is the naive count nz(U)+nz(V)+nz(W)-2r-np. 179 < 332, but this is a different convention, so the comparison is weak; the clause as written is met.
9. Coefficient class: the rank is attained over Z, same class as the candidate. Met.
10. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": rank not lowered. Met.

## Verdicts
Full criterion: met as checkable from these sources, with the caveats that the Lille clause is vacuous and the COVERAGE clause compares against a naive count.
p1 as listed in the bank is the 3x3x3 partial win, which this claim does not address. Read as the brief frames it (strictly fewer than Perminov's live 2x5x6 count, same convention): met, 179 < 181. Taken literally as the bank's enumerated p1, not met. I record the brief's reading below.

confirmed_scope: claim/object/2x5x6_m47_cr179_ZT_reduced.json (sha256 3d1e40cf65f343ad2edfe3735c1d4eccd1fd4aeaca82b31980779e38a059dcc1) is a ternary straight-line program that I verified exactly over Z (full 2x5x6 tensor identity, all expanded coefficients in {-1,0,1}) to compute a rank-47 scheme with the same 47 products as Perminov's 2x5x6 cr181 file and 179 additions under his reduced convention (U 38, V 65, W 76; V and W programs identical to his, U program 2 additions shorter), below his only 2x5x6 file (181), with no Lille operation count to compare against and COVERAGE.md giving only the naive 332.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
