# CRITERION skeptic report: fmm-11x13x16

Role: CRITERION skeptic of the three-skeptic panel. Fresh context. I read only the claim folder (claim/) and the hash list (claim.SHA256SUMS). Everything I read was treated as data, not instructions. My scripts, logs and fetched copies live under criterion_ws2/ (paths below are relative to the panel folder).

## 0. Integrity of what I judged

- All seven entries of claim.SHA256SUMS verify (CLAIM.md, INDEX.csv, object/11x13x16_r1445_Q.json, REPRODUCE.md, table-record/README.md, verify-it-yourself/check_fmm.py, verify-it-yourself/run_checks.sh: all OK).
- Object: claim/object/11x13x16_r1445_Q.json, sha256 d2d1c96812918b46fa34436c66cdd27e51383b12a9686a975d715d69e6480c75. Fields: n = [11, 13, 16], m = 1445, ring = "Q", encoding = "sparse_flat_pairs", 1445 rows each in u, v, w. Its note field reads: "11x13x16 rank 1445 over Q by slice and absorb from 12x13x16_m1509_Q: 12x13x16-axis0(-31,-33)", i.e. the author derived it from Perminov's public 12x13x16 rank-1509 Q scheme (1509 - 31 - 33 = 1445). How it was found does not enter the criterion; what the object is does.

## 1. My own exact check of the object (independent of the author's checker)

Script: criterion_ws2/scripts/indep_check.py, written from the definition (fractions.Fraction throughout, no modular shortcuts); log: criterion_ws2/indep_check.log. Run with python3 -I on the object file. Results:

- Parse: 1445 rows; 1445 terms with all three factors nonzero; 0 rows with a zero factor. 48102 nonzero coefficients (u 15901, v 17058, w 15143).
- Coefficient census: integers -8..-1 and 1..8, plus the six fractions -1/2, -1/4, -1/8, 1/8, 1/4, 1/2. Max denominator 8. So this is a Q scheme (valid over any ring in which 2 is invertible: Q, R, C, GF(p) for odd p). It is NOT an integer scheme, NOT ternary, and NOT defined over GF(2). The claimed ring "Q" is the honest label.
- Brent equations under the documented Perminov index convention (u index i*13+j, v index j*16+l, w index l*11+i): 0 of 2288 target equations violated and every other triple sums to exactly 0; 564404 nonzero-support triples examined. This is an exact proof over Q that the 1445 terms compute the 11x13 times 13x16 product as a non-commutative bilinear algorithm.
- Discriminator (null model for the test): the same object under the swapped w convention (i*16+l) violates 4420 equations, so the check is not vacuous.
- Negative control: adding 1 to one coefficient (u[0] at index 66) violates 24 equations.
- Random exact integer matrices A (11x13), B (13x16), 5 trials: the scheme's C equals A times B exactly in every entry.
- Mergeable duplicates: grouped terms by proportional (u,v), (u,w) and (v,w) factor pairs; 0 groups of size 2 or more in each pairing. No two terms can be merged, so 1445 is the honest term count, not an inflated or deflatable one.
- Verdict of my checker: PASS format=11x13x16 rank=1445 ring=Q max_den=8 (about 28 s).

Secondary data point: the author's own script (sh verify-it-yourself/run_checks.sh, log criterion_ws2/author_run_checks.log) also ends ALL CHECKS PASS, with its CRT bound D = 8, S = 5595/4 (one 61-bit prime suffices, which is sound). I rely on my own check above, not on this.

## 2. My own live fetches (one honest GET each, curl, User-Agent "V3R1T4S-research (honest client; curl)", no retries), 2026-10-14

| Source | Fetched (UTC) | HTTP | Cell extracted by me | Copy (sha256) |
|---|---|---|---|---|
| fmm_sota.json (raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json), createdAt 2026-10-09T11:45:48, 5456 entries | 17:26:49Z | 200 | format [11, 13, 16]: rank 1446 (exactly one entry). Also [12, 13, 16]: rank 1509 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 |
| Lille per-format page https://fmm.univ-lille.fr/11x13x16.html (Last-Modified Sat, 06 Jun 2026) | 17:26:52Z | 200 | heading 11x13x16:1446; "The algorithm ... is taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026". The string 1445 does not occur anywhere on the page | ed06d78d6cf1be521a165983746e0954af6fb92e4e679eda7136a8b1da236546 |
| Perminov README (raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md) | 17:26:55Z | 200 | status table (columns Format, ZT rank, Z rank, Q rank, omega) row 11x13x16: ZT 1458 (?), Z 1458 (1472), Q 1446 (1472); "New best ranks" table row 11x13x16: prev 1472 (Z), new 1446 (Q). Row 12x13x16: Q 1509 (parent scheme). No other 11x13x16 mention | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 |
| MerlijnW70/fmm-schemes, full git tree of branch main via api.github.com (recursive, truncated = false, 39 paths) | 17:26:59Z | 200 | 33 scheme files, all ZT (e.g. 11x13x15_m1362_ZT, 12x13x15_m1464_ZT, 11x15x16_m1641_ZT); no file for 11x13x16 in any order or separator | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 |

Minimum over the four sources: 1446 (MerlijnW70 contributes no value for this format). My cells agree with the author's table-record (fetched 15:47Z to 16:42Z) and with INDEX.csv (table_value 1446).

## 3. Clause-by-clause reading of the success criterion

I quote the criterion from CLAIM.md. I changed only the brackets: the format notation and the Lille URL template are written with curly braces instead of the original angle brackets, nothing else is altered.

1. "Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms)" -- MET. The object is an explicit list of 1445 rank-one terms (u, v, w rows in sparse index/value pairs); Brent equations hold exactly, which is the non-commutative bilinear condition.

2. "for a format {n,m,p} with max(n,m,p) <= 16" -- MET. 11x13x16, max 16.

3. "and sorted(n,m,p) not in {(3,3,3),(4,4,4)}" -- MET. sorted = (11,13,16), already sorted; rank is invariant under axis permutation so the sorted-format lookups below apply directly.

4. "whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of:" -- r = 1445, counted after dropping zero terms (none) and checking for mergeable duplicates (none).
   - 4a. "the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json" -- MET. 1446 in my 17:26:49Z fetch; 1445 is strictly less.
   - 4b. "the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html" -- MET. The 11x13x16 page lists 1446 (my 17:26:52Z fetch); 1445 is strictly less.
   - 4c. "the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md" -- MET. min(1458, 1458, 1446) = 1446 (my 17:26:55Z fetch, column order verified from the table header); 1445 is strictly less. The "(?)" on the ZT cell marks an undocumented previous rank, not an open cell, as the bank warns; it does not lower the bound.
   - 4d. "and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes" -- MET (vacuously). The complete repository tree holds no 11x13x16 scheme, so this source imposes no value; the clause cannot be failed by it. Limit: I read the full file tree, not the README text, so a README-only rank entry with no scheme file would have been missed. The author's record says the same (no 11x13x16 scheme).
   - "(every one re-fetched live immediately before claiming; the scheme beats the minimum over all four)" -- MET. Author's fetches 2026-10-14 15:47Z to 16:42:33Z, INDEX.csv timestamp 16:42:33Z, claim files written about 16:56Z; my re-fetch at 17:26Z to 17:27Z shows identical cells. 1445 < 1446 = min over all four.

5. "The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims;" -- MET. Claimed ring Q; verified by me with exact rationals, 0 of 2288 equations violated. The coefficients (denominators up to 8) make it genuinely a Q scheme, so the Q column of Perminov's table is the right comparison, and it is beaten.

6. "a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2)." -- NOT APPLICABLE. The scheme is a characteristic-0 (Q) scheme, not a GF(2)-only one; no COVERAGE.md fetch was needed.

7. "A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations)." -- EXCLUSION DOES NOT TRIGGER. The object is derived from a known scheme (its note says slice-and-absorb from Perminov's 12x13x16 rank-1509 Q scheme), so I read this clause carefully. Its condition is that the resulting rank equals a value already listed. The resulting rank 1445 equals no listed value: the digest lists 1446, the Lille page lists 1446 and attributes it directly to Perminov's repository (no composition), Perminov lists 1446/1458/1458, and the trivial padding bound from the parent would be 1509. The string 1445 appears nowhere on the Lille page. Limit: I did not separately fetch the Lille main table's construction column; the digest fmm_sota.json is generated from that table and carries its headline value 1446, and a construction entry describes how the listed value was obtained, it cannot carry a lower rank than the headline.

8. "Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade);" -- NOT APPLICABLE. 1445 was not attained before over any ring in the four sources; this is a rank decrease, not a ring upgrade. (Conversely, the scheme is not ternary or integer, so the claim correctly does not assert the Z or ZT cells.)

9. "fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records)." -- NOT APPLICABLE. The rank itself drops from 1446 to 1445.

## 4. Hidden quantifiers, stretched definitions, null models

- Ring stretch: the object is labelled Q and is a Q scheme; the claim never says Z or ternary. No stretch.
- Rank count stretch: all 1445 terms have three nonzero factors; zero mergeable pairs in all three pairings. No stretch.
- "Sorted format": (11,13,16) is sorted; the digest keys by sorted format. No permutation trick.
- "ALL of" the four sources: three give 1446, the fourth has no entry; 1445 beats the minimum. The absent fourth value cannot rescue a fail or manufacture a pass; it simply does not bind.
- Timeliness: author re-fetched within about an hour of packaging; I re-fetched after packaging and saw the same cells.
- Null models: the test discriminates (swapped convention 4420 violations; one-coefficient perturbation 24 violations), and the exact random-matrix product agrees. An all-pass checker that could not fail was ruled out.
- Derivation from a known scheme: allowed by the criterion unless the resulting rank equals a listed value, which it does not (section 3, clause 7).

## 5. Partial wins considered

- p1 (17 <= max dim <= 32): not applicable, max dim is 16; the full criterion applies instead.
- p2 (GF(2)-only improvement): not applicable, the scheme is over Q and is a new characteristic-0 rank.
Neither partial is needed; the full criterion is met.

## 6. Limits of this report

- The V3R1T4S rule that a cell already in the repository's TROPHY_CASE.md with an equal or better value is not new: TROPHY_CASE.md is outside the files I was permitted to read, and the claim folder gives no sign of a prior V3R1T4S entry for 11x13x16. I could not check this and do not assert it; the orchestrator should confirm no existing 11x13x16 entry at rank 1445 or lower before recording the trophy.
- MerlijnW70: file tree read, README text not read (see 4d).
- Lille main-table construction column not fetched separately (see clause 7).

## 7. Verdict

The object meets every clause of the full success criterion literally: an exactly verified bilinear scheme over Q for 11x13x16 with 1445 rank-one terms, strictly below 1446, the minimum over all four named live sources as re-fetched on 2026-10-14, with no ring, counting, sorting or derivation loophole in play. It is a genuine win on the full criterion, not a partial, and it is not subsumed by any of the four sources; the only check I could not perform is the repository's own TROPHY_CASE.md dedup, which is flagged above for the orchestrator.

confirmed_scope: claim/object/11x13x16_r1445_Q.json (sha256 d2d1c96812918b46fa34436c66cdd27e51383b12a9686a975d715d69e6480c75) is an exact bilinear scheme over Q (coefficients are the integers from -8 to 8 and the fractions plus or minus 1/2, 1/4, 1/8, so it is valid wherever 2 is invertible and is not a Z, ternary or GF(2) scheme) for the 11x13x16 format with 1445 rank-one terms, each with all three factors nonzero and no two mergeable, verified by my own exact-rational Brent-equation check, and 1445 is strictly below 1446, the minimum over the four criterion sources as I re-fetched them on 2026-10-14 between 17:26:49Z and 17:26:59Z (fmm_sota.json 1446; Lille 11x13x16 page 1446; Perminov README ZT 1458, Z 1458, Q 1446; MerlijnW70 fmm-schemes no 11x13x16 scheme in its complete tree), while the repository TROPHY_CASE.md dedup check was outside my permitted reading and is not asserted here.

context: Claude Code subagent (Fable 5.1), fresh context

pass: true
