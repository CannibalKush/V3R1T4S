# CRITERION skeptic report: fmm-15x15x16-r2105b

Object: claim/object/15x16x15_r2105_Q.json
sha256 (from claim.SHA256SUMS, re-hashed locally, matches): 4b68518ac7f293047071df6723a04783e4d38f302c6b98ccaa02f0c66669ae3b
All seven files in claim.SHA256SUMS verified OK with shasum -a 256 -c.

Target id: fmm-catalogue-small-format-rank. Stored format n=[15,16,15] (A is 15x16, B is 16x15); sorted format 15x15x16. Rank is invariant under axis permutation, so the comparison format is 15x15x16.

## My own exact check (written before reading the author's checker code)

Method: criterion_ws/my_brent_check.py, python3 standard library, fractions.Fraction only (no floats, no modular reduction, no sampling). Decoded the vocab_rle_v1 rows with the stated index convention (u[i*n2+j] for A[i][j], v[j*n3+l] for B[j][l], w[l*n1+i] for C[i][l]), enforced row lengths 240/240/225, accumulated the full tensor sum_t u_t[a] v_t[b] w_t[c] into a sparse dictionary, then compared every one of the (15*16)*(16*15)*(15*15) = 12,960,000 Brent equations against the exact target [i==i2][j==j2][l==l2], including entries no term touches. Rank counted as the number of terms with all three factors nonzero. Run with nice -n 19.

Real output:

```
n = (15, 16, 15) declared m = 2105 ring = Q encoding = vocab_rle_v1 terms listed = 2105
equations checked: 12960000 nonzero accumulated entries: 2932437 triple-product work: 72912151
mismatches: 0
rank (terms with all three factors nonzero): 2105
RESULT: PASS
```

Negative control (same checker, last term dropped): `mismatches: 1980 / rank 2104 / RESULT: FAIL`, so the checker does reject a broken scheme.

Second independent method (criterion_ws/my_random_eval.py): evaluated the scheme on random integer matrices with entries in [-10^6, 10^6] in exact Fraction arithmetic and compared to the classical product; seeds 1 and 2 both printed `scheme(A,B)==A@B exactly: True`.

Author's checker, run afterwards: `PASS format=15x16x15 rank=2105` (exit 0).

Conclusion: the object is an exact bilinear scheme over Q for the format 15x16x15 with 2105 rank-one terms, every term having all three factors nonzero. Coefficients are integers or rationals (W denominators up to 2100 after row scaling), so it is a Q scheme, not merely an integer or ternary one.

## Live sources (each fetched exactly once, curl, User-Agent 'V3R1T4S-research (honest client; curl)', no retries, 2026-10-15T09:31:39Z to 09:31:40Z, all HTTP 200)

Every fetched body has the same sha256 the author recorded in claim/table-record/README.md, so the tables did not change between the author's fetch (09:07Z) and mine.

| Source | My sha256 | Cell for 15x15x16 |
|---|---|---|
| fmm_sota.json (createdAt 2026-10-09T11:45:48, 5456 entries) | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | {"format": [15, 15, 16], "rank": 2132} |
| Lille per-format page https://fmm.univ-lille.fr/{n}x{m}x{p}.html with n,m,p = 15,15,16 | 69f7757285fa5b71cff67e74cedef6f262f599c0858c6b251e67e5e427a6fc69 | "15x15x16:2132", "taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026" (no composition construction shown) |
| Perminov README status table (header line 765: Format, ZT rank, Z rank, Q rank, omega; row at line 1444) | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | 15x15x16: ZT 2132 (?), Z 2132 (?), Q 2132 (2173); min = 2132 |
| MerlijnW70 fmm-schemes git tree (recursive, truncated: false, 39 paths) | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | no file for 15x15x16, 15x16x15 or 16x15x15 |

Minimum over the four sources: 2132. Claimed rank: 2105. 2105 < 2132.

## Clause-by-clause

1. "a format n x m x p with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}" (quoted with the bank's angle-bracket format notation spelled out): max side is 16; sorted format is (15,15,16). MET.

2. "an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms)": the JSON holds u, v, w lists of 2105 rows each, fully decodable. MET.

3. "whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of" the four live sources: 2105 < 2132 = fmm_sota.json = Lille page = min(ZT, Z, Q) in Perminov's README; MerlijnW70 lists nothing for the format (so it imposes no lower value). MET against every one of the four, each re-fetched by me.

4. "The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims": ring claimed is Q; my Fraction check of all 12,960,000 Brent equations passes. MET. The GF(2)-only sub-clause does not apply (the scheme is over Q, so COVERAGE.md is not needed).

5. "A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed": 2105 is not listed anywhere for 15x15x16. Null model from fmm_sota.json: best one-cut split of 15x15x16 into two listed formats is 2193 (15x15x14 + 15x15x2); best padding is 16x16x16 at 2236; no listed format dominating 15x15x16 has rank <= 2132 other than 15x15x16 itself. So 2105 is not reachable by plain composition of listed values, and the Lille page shows no construction entry for this format (its 2132 is Perminov's scheme). The object's own note says it was derived from an unpublished parent 15x16x16 scheme of rank 2176 by removing one axis slice (raw 2144) and then absorbing 39 terms; that is a reduction search, not a composition that lands on a listed value. MET.

6. "Ternary/integer re-derivations of a rank already attained over Q are NOT this target": 2105 was not attained over any ring in the four sources; the object is itself a Q scheme. Not that split. MET.

7. "fewer additions at an existing rank is NOT this target": the rank is new, not an existing one. MET.

8. "every one re-fetched live immediately before claiming": the author's table-record shows fetch times 09:07:43Z to 09:07:49Z on 2026-10-15 with hashes identical to my 09:31Z fetches. MET.

## Hidden quantifiers and stretched definitions hunted

- Format naming: the file says 15x16x15; INDEX.csv and table-record compare the sorted 15x15x16. Rank is permutation-invariant, so this is legitimate; I checked all three tables under 15x15x16 and MerlijnW70 under all three spellings.
- Rank counting: all 2105 listed terms have all three factors nonzero; no zero or empty terms inflate or deflate the count. The declared "m": 2105 matches the list length and the nonzero count.
- Ring: coefficients include denominators 2, 3, 4, 6, 7, 8, 12, 15, 20, 24, 30, 35, 60, 70, so the scheme is genuinely over Q (not Z or ZT); the criterion allows any ring and the record over ANY ring is 2132, so Q is fine.
- Perminov's "(?)" cells: read as "undocumented previous rank", not "open", as the bank instructs; the ZT and Z values are 2132 either way.
- Composition null model: computed above; 2105 is below every trivial composition/padding bound derivable from fmm_sota.json.
- Scope of the parent: the note's parent 15x16x16 rank 2176 would itself be below the listed 2223 for 15x16x16, but that parent is not in this claim folder and is not part of this claim; it is not counted here.

## Partial wins considered

- p1 (17 <= max side <= 32): not applicable, max side is 16; the full criterion applies instead.
- p2 (GF(2)-only improvement): not applicable, the scheme is over Q and beats the characteristic-0 record.

Neither partial win is claimed or needed; the full criterion is met.

## Verdict

The object meets every clause of the full success criterion literally: an exactly verified Q scheme for 15x16x15 with 2105 rank-one terms, strictly below the 2132 listed for the sorted format 15x15x16 in all four live sources at my own fetch time, not a composition landing on a listed value, and not one of the excluded scope splits. Genuine, non-subsumed win. PASS.

confirmed_scope: The file claim/object/15x16x15_r2105_Q.json (sha256 4b68518ac7f293047071df6723a04783e4d38f302c6b98ccaa02f0c66669ae3b) is an exact bilinear scheme over Q for the format 15x16x15 with 2105 rank-one terms, all three factors nonzero in every term, satisfying all 12,960,000 Brent equations in exact rational arithmetic, and 2105 is strictly below 2132, the rank listed for the sorted format 15x15x16 in fmm_sota.json (createdAt 2026-10-09T11:45:48), the Lille 15x15x16 page, and Perminov's README ZT/Z/Q columns, with no 15x15x16 scheme in the MerlijnW70 fmm-schemes tree, all four fetched 2026-10-15T09:31Z.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
