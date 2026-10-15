# CRITERION skeptic report: 14x16x16 rank 2117 over Q

Object: claim/object/14x16x16_r2117_Q.json
sha256 (from claim.SHA256SUMS, re-hashed locally, all 7 listed files OK): 9d6ef02f8162d9d5a53e56ecff6821459727c32d5a5fecb24283bd0c716fdf10

Notation: the bank writes formats with angle brackets; this file writes them as n,m,p triples or as 14x16x16
(the repo checker rejects angle-bracket placeholders). Quotes below are otherwise verbatim.

## My own verification (written before reading the author's checker body)

Script: criterion_ws/scripts/brent_check.py. Exact integer arithmetic with python-flint fmpz_mat: decode the
vocab_rle_v1 rows to Fractions, scale U, V, W by the LCM of their denominators (DU=25200, DV=720, DW=1440),
and for each of the 256 output slots c form U^T diag(W[:,c]) V exactly and compare every entry with
D*[target], D=DU*DV*DW. Index convention taken from the claim's description (u[i*n2+j] for A[i][j],
v[j*n3+l] for B[j][l], w[l*n1+i] for C[i][l]). No sampling, no floats, no modular reduction. Real output:

```
format n=[14, 16, 16] declared m=2117 terms=2117 rank(all three factors nonzero)=2117 zero_terms=0
declared ring=Q all_integer_coeffs=False DU=25200 DV=720 DW=1440
brent equations checked=12845056 (expected 12845056) mismatches=0 elapsed=36.3s
RESULT: PASS (rank 2117, expect 2117)
```

12,845,056 = 224*256*224 is every Brent equation for 14x16x16. Negative controls through the same checker:
dropping the last term gives `mismatches=107648 ... RESULT: FAIL (rank 2116)`; changing one coefficient in
the first W row gives `mismatches=60 ... RESULT: FAIL`. So the checker can fail and the object passes it.
The author's own script (run afterwards, for comparison) prints `PASS format=14x16x16 rank=2117` with the same
DU/DV/DW and `ALL CHECKS PASS`.

Rank: 2117 terms, every term has all three factors nonzero, so r = 2117.
Ring: coefficients are rationals (denominators up to 25200 appear; e.g. 7/48, 47767/288), so the scheme is
genuinely over Q and not over Z or a ternary set; it is verified exactly over Q, the ring it claims.

## Clause-by-clause

1. "a format n,m,p with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}"
   MET. Format 14x16x16, max side 16, sorted (14,16,16) is neither excluded triple.

2. "an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms)"
   MET. The JSON holds 2117 rows each of u (224 coefficients), v (256), w (256).

3. "whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of" the four sources,
   "every one re-fetched live immediately before claiming". I re-fetched each once (curl, User-Agent
   'V3R1T4S-research (honest client; curl)', no retries) at 2026-10-15T09:21:44Z to 09:21:47Z, all HTTP 200;
   all four sha256 values equal the author's table-record hashes (so the pages were unchanged since the
   author's 2026-10-14T18:44Z fetch).
   - fmm_sota.json (createdAt 2026-10-09T11:45:48, 5456 entries): entry {"format": [14, 16, 16], "rank": 2128}.
     2117 is less than 2128. MET.
   - Lille page https://fmm.univ-lille.fr/{n}x{m}x{p}.html for 14x16x16: title "14x16x16:2128";
     construction/source column: "is taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub,
     February 2026" (an imported scheme, not a composition). 2117 is less than 2128. MET.
   - Perminov README, 'Research Findings & Status' table row `14x16x16`: ZT 2170 (?), Z 2170 (?), Q 2128 (2142).
     Minimum over ZT/Z/Q = 2128. 2117 is less than 2128. MET. (The '(?)' cells are read as undocumented, not open.)
   - MerlijnW70 fmm-schemes git tree (39 paths, truncated=false): no 14x16x16 scheme (files containing 14 and
     16 are 10x14x16, 13x14x16, 9x14x16 only). Nothing to beat; vacuously MET, and the minimum over the
     four sources is 2128.
   The scheme beats the minimum over all four by 11.

4. "The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it
   claims"  MET, by my exact integer check above (scaled rationals, every equation).

5. "a scheme valid only over GF(2) counts here ONLY if ..."  NOT APPLICABLE: the scheme is over Q with
   characteristic-0 rational coefficients; the COVERAGE.md clause and partial win p2 do not arise.

6. "A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting
   rank equals a value already listed"  MET. 2117 is below every listed value, so it cannot equal one. Null
   model from fmm_sota.json (criterion_ws/out/composition_null_model.txt): the cheapest trivial composition
   is 7*306 = 2142 (2,2,2 tensor 7,8,8); the best axis split is 972+1230 = 2202; padding from 15x16x16 gives
   2223. No composition reaches 2117 or below. The object's own note says it was obtained by restricting a
   15x16x16 rank-2180 scheme along axis 0 (raw 2145) and absorbing 28 terms; that is a new scheme, and the
   2180 parent is itself a V3R1T4S trophy row, not a listed-table value.

7. "Ternary/integer re-derivations of a rank already attained over Q are NOT this target; fewer additions at
   an existing rank is NOT this target"  MET (not those cases): the rank is new over every ring listed, and
   the scheme is over Q, not a ring upgrade.

8. Scope splits: max side 16 keeps it inside the 16x16x16 Perminov table (so partial win p1, which is for
   17 to 32 max side, does not apply); not GF(2)-only (p2 does not apply); not the 3x3x3/4x4x4 moonshot.

## Subsumption / null-model notes

- V3R1T4S TROPHY_CASE.md (fetched once, 2026-10-15T09:25:18Z, sha256 b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412,
  same as the author's record): five fast-matrix-multiplication rows (14x15x15, 13x14x14, 15x16x16, 14x14x15,
  13x14x15); no 14x16x16 row. Not subsumed by an existing trophy.
- Hidden quantifiers checked: all 12,845,056 equations, not a sample; every term counted has three nonzero
  factors; the comparison is against the sorted format in all four sources; all four fetched live by me.
- Stretched definitions checked: the ring claimed (Q) matches the coefficients present; the Lille rank and
  fmm_sota rank are the same 2128 Perminov Q scheme, so there is one real record of 2128 and this beats it.

## Partial wins considered

p1 (max side 17 to 32): not applicable, max side is 16. p2 (GF(2)-only): not applicable, the scheme is over Q.
Neither is needed; the full criterion is met.

## Verdict

PASS on the full success criterion: an explicit, exactly verified rank-2117 bilinear scheme over Q for
14x16x16, strictly below the live minimum 2128 of all four named sources, not a composition of listed values,
not subsumed.

confirmed_scope: The file claim/object/14x16x16_r2117_Q.json (sha256 9d6ef02f8162d9d5a53e56ecff6821459727c32d5a5fecb24283bd0c716fdf10) is an exact bilinear scheme over Q for the 14x16x16 matrix multiplication format with 2117 rank-one terms, each with all three factors nonzero, verified by my own exact integer check of all 12,845,056 Brent equations, and 2117 is strictly below 2128, the minimum rank for the sorted format 14x16x16 in fmm_sota.json, the Lille 14x16x16 page, Perminov's README ZT/Z/Q columns and MerlijnW70's fmm-schemes tree as I fetched them on 2026-10-15.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
