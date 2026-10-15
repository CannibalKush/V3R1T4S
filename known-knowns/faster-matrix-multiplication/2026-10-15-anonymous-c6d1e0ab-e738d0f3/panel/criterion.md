# CRITERION skeptic report: fmm-13x13x14-r1479

Object: claim/object/13x13x14_r1479_Q.json
sha256 (from claim.SHA256SUMS, re-verified with shasum -a 256 -c, all 7 files OK): e738d0f367b67ba740109db2687b58811da516ee74f67c42ccb934eab382548d
Target id: fmm-catalogue-small-format-rank. Claimed: rank 1479 over Q for format 13x13x14, versus a listed minimum of 1511.

Quoting rule: the bank writes formats in angle-bracket notation; every quote below rewrites them as nxmxp (e.g. 13x13x14) and the Lille URL template as https://fmm.univ-lille.fr/{n}x{m}x{p}.html. Nothing else in the quotes is changed.

## My own exact check (written from the encoding description before reading the author's checker code)

Method: decode vocab_rle_v1 rows to Fractions; scale each row to integers by its own denominator lcm; remove the per-term scale D_t by multiplying U'_t by L/D_t with L = lcm_t D_t (L = 54400), so sum_t U'_t x V'_t x W'_t = L * target exactly over Z; for each of the 169 A-slots a, form M_a = V'^T diag(U'[:,a]) W' with python-flint fmpz_mat (arbitrary-precision integers, no modular reduction, no sampling) and compare all 182 x 182 entries to L*[i==i2][j==j2][l==l2] under the stated convention u[i*n2+j], v[j*n3+l], w[l*n1+i]. Rank counted on the raw rationals as terms with all three rows nonzero.

Real output:

    format n1,n2,n3 = 13,13,14; declared m = 1479; rows = 1479
    terms with all three factors nonzero: 1479; zero terms: 0
    global integer scale L = 54400 (16 bits)
    Brent equations checked: 5597956 (expected 5597956); mismatches: 0
    MY-CHECK PASS rank=1479

Negative controls on MY checker (both must fail, both did):

    neg_drop_last (last term removed): mismatches: 49980; RANK MISMATCH: counted 1478; MY-CHECK FAIL
    neg_perturb (one W coefficient of term 0 changed): first MISMATCH a=0 b=71 c=4 got 272 want 0; mismatches: 1976; MY-CHECK FAIL

Second independent exact method: evaluate the scheme on 3 random integer matrices A (13x13), B (13x14) with entries in [-10^6, 10^6] using Python Fractions and compare to A@B entrywise: "exact match of all 182 entries of A@B: True" for all 3 trials.

Informational: 1479 terms, 1479 distinct up to scaling (no duplicate/proportional terms); denominators present 1,2,4,5,8,10,17,20,40,136,272,1088 (so the scheme is genuinely over Q, not Z); max |coefficient| 44160/17.

Author's checker (run only after mine): `sh verify-it-yourself/run_checks.sh` printed "PASS format=13x13x14 rank=1479", rejected its own negative control, and ended "ALL CHECKS PASS". Its method (per-matrix integer scaling, packed W slots of 43 bits above a 41-bit coefficient bound) is sound and independent of mine.

## Clause-by-clause

1. "a format nxmxp with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}" -- MET. Format is 13x13x14, max side 14; sorted (13,13,14).

2. "an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms)" -- MET. The JSON holds 1479 u/v/w rows of lengths 169/182/182 decoding to explicit rational coefficient matrices.

3. "whose number of rank-one terms r ... Count r after dropping zero terms" -- MET: r = 1479; no zero terms (every term has all three factors nonzero), so no inflated or hidden count.

4. "STRICTLY LESS (direction: min) than ALL of" the four live sources, "every one re-fetched live immediately before claiming" -- MET. My own single fetches (curl, User-Agent "V3R1T4S-research (honest client; curl)", no retries, 2026-10-15T09:13:40Z to 09:13:43Z, all HTTP 200):
   - fmm_sota.json (createdAt 2026-10-09T11:45:48, 5456 entries; sha256 d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1): entry {"format": [13, 13, 14], "rank": 1511}. No other permutation key exists (formats are stored sorted).
   - Lille page https://fmm.univ-lille.fr/13x13x14.html (sha256 60f9a6f7a1b36fb5c4e86c9111aee78abae17873544dcae7b98d0fff2ed70151): title "13x13x14:1511"; "Algorithm definition: The algorithm 13x13x14:1511 is taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026." No construction/composition derivation is given on the page.
   - Perminov README (sha256 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341), "Research Findings & Status" table line: | `13x13x14` | 1511 (?) | 1511 (1524) | 1511 (1524) | 2.826838093 |, so ZT = Z = Q = 1511, minimum 1511; the earlier results table also lists 13x13x14 at 1511 (ZT), previous 1524 (Z).
   - MerlijnW70 fmm-schemes tree (API, truncated=false, 39 paths; sha256 f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37): no scheme for 13x13x14, 13x14x13 or 14x13x13 (nearest: 13x13x15_m1591_ZT, 13x13x16_m1709_ZT).
   Minimum over the four = 1511; 1479 < 1511 by 32. My four content hashes equal the author's table-record hashes byte for byte, so the author's "re-fetched live" record is corroborated and nothing moved between 09:07Z and 09:13Z.

5. "verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims" -- MET. Claimed ring Q; my check is exact over Z after rational scaling, equivalent to exact over Q; the random-matrix check is exact Fractions. GF(2)-only clause does not apply (the scheme is characteristic-0; its rational denominators include 2, so it is not even a GF(2) scheme).

6. "A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed" -- MET (clause not triggered). 1479 equals no listed value for 13x13x14 (all four list 1511, Perminov's bracketed previous 1524). Composition null models from the live fmm_sota.json all exceed 1479: 13x13x13 (1379) + 13x13x1 (169) = 1548; 2 x 7x13x13 (794) = 1588. The author's embedded note says the object was derived from a 13x14x14 rank-1539 parent by a dimension reduction and term absorption (raw 1515, absorbed 36); that is a derivation, but the clause only excludes derivations whose rank equals a listed value, and none does. Note the Lille per-format page states the listed 1511 is Perminov's scheme, not a construction, so there is no listed composition at or below 1479 either.

7. Scope splits: "Ternary/integer re-derivations of a rank already attained over Q are NOT this target" -- not applicable: 1479 is below the Q column itself (1511), so this is a new rank, not a ring upgrade. "fewer additions at an existing rank is NOT this target" -- not applicable: the rank is new.

8. Hidden quantifiers hunted: "over ANY ring" is satisfied by beating min(ZT, Z, Q) = 1511; "sorted format" invariance was respected (I searched all three axis permutations in every source); "ALL of" the four sources was checked individually, not just the author's summary; "count r after dropping zero terms" was checked (none to drop). The "(?)" cells in Perminov's ZT column were read as "undocumented", not "open", as the bank instructs; the ZT value is 1511 anyway.

## Partial wins considered

- p1 (17 <= max side <= 32): not applicable, max side is 14; the full criterion is the right target and is met.
- p2 (GF(2)-only improvement): not applicable, the scheme is over Q and is a new characteristic-0 rank.
Neither partial win subsumes this: the result is a full win, not a partial.

## Limits

- The Lille main table (with its construction column) was not separately fetched; the per-format page named by the criterion was, and it attributes the listed 1511 to Perminov's scheme with no construction derivation.
- The TROPHY_CASE.md line in the author's table-record was not re-fetched by me; it is not one of the four sources named in the success criterion.
- I did not search beyond the four named sources for any unlisted lower rank; the criterion is defined against those four.

## Verdict

PASS. The object is an exactly verified rank-1479 bilinear scheme over Q for 13x13x14, strictly below the live minimum 1511 of all four named sources, with every clause of the full success criterion met literally and no scope split or composition exclusion triggered.

confirmed_scope: The file claim/object/13x13x14_r1479_Q.json (sha256 e738d0f367b67ba740109db2687b58811da516ee74f67c42ccb934eab382548d) is a bilinear scheme with exactly 1479 rank-one terms, all three factors nonzero in every term, whose coefficients are rationals with denominators dividing 1088 and which satisfies all 5597956 Brent equations for the format 13x13x14 exactly over Q, and 1479 is strictly below 1511, the rank listed for the sorted format 13x13x14 in each of fmm_sota.json (createdAt 2026-10-09T11:45:48), the Lille page https://fmm.univ-lille.fr/13x13x14.html, and Perminov's README ZT/Z/Q columns, while MerlijnW70's fmm-schemes held no 13x13x14 scheme, all as fetched by me once on 2026-10-15 between 09:13:40Z and 09:13:43Z.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
