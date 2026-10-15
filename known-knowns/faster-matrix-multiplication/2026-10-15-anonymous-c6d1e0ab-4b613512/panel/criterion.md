# CRITERION skeptic report: fmm-13x14x14-r1538

Object: claim/object/13x14x14_r1538_Q.json
sha256 (from claim.SHA256SUMS, re-verified with shasum -a 256 -c, all 7 files OK): 4b613512756bdb5c0303dc17236ad63b3b8a4e931d898e75e863d95d6dd9ab9e
Target: fmm-catalogue-small-format-rank. Claimed: rank 1538 over Q for the format 13x14x14.

Notation note: the bank writes formats with angle brackets; this file writes them as 13x14x14 or (n,m,p) and the Lille URL template as https://fmm.univ-lille.fr/{n}x{m}x{p}.html.

## My own exact check (written before reading the author's checker)

Encoding read from CLAIM.md: sparse_flat_pairs, rows of (index, value) pairs, values integers or "p/q" strings. Row lengths found: u 182 = 13*14 (A), v 196 = 14*14 (B), w 182 = 13*14 (C). 31,536 + 25,386 + 22,165 integer coefficients and 16,039 + 17,205 + 15,290 fractional ones (denominators 2, 4, 5, 8, 10, 40, ... and one factor 17 in u), so the ring Q is substantive, not a relabelled integer scheme.

Method: parse with fractions.Fraction; clear denominators with one global lcm per factor (Du = 5440, Dv = 40, Dw = 40, S = 8,704,000); compute S times the sum over terms of u_k (x) v_k (x) w_k as an integer tensor by numpy int64 matmul with an a-priori entry bound of 2,471,396,582,400 (42 bits, so no overflow is possible); compare entry by entry with S times the matrix multiplication tensor. I did not assume an index convention: all 8 row-major/transposed combinations for A, B, C were tried. A second method (python-flint fmpz_mat, arbitrary precision, no bound needed) was run on the passing convention. Rank counted as terms with all three factor rows nonzero.

Real output (my_brent_check.py):

    format n,m,p = 13,14,14; terms listed = 1538; terms with all three factors nonzero (rank) = 1538; zero terms = 0
    global denominators: Du=5440 Dv=40 Dw=40; scale S = 8704000
    max |U_int|=8913600 max |V_int|=22284 max |W_int|=22348; a-priori entry bound = 2471396582400 (42 bits) ; int64 safe: True
    method 1 (numpy int64): tensor computed in 14.4s; max |entry| = 8704000
      convention U   V   W  : FAIL (5040 of 6492304 entries differ)
      convention U   V   W^T: ALL BRENT EQUATIONS HOLD
      (the other six conventions FAIL)
    method 2 (python-flint fmpz, exact, no bound) convention (0, 0, 1): ALL BRENT EQUATIONS HOLD (25.2s)
    RESULT: VALID exact scheme over Q for 13x14x14, rank 1538

The passing convention is u[i*14+j] for A[i][j], v[j*14+l] for B[j][l], w[l*13+i] for C[i][l]; this is exactly the convention the author's checker docstring states (read afterwards). Every one of the 182*196*182 = 6,492,304 Brent equations holds exactly over Q.

Null models (my checker, same two methods): five corrupted copies were all rejected: drop the last term (rank 1537), drop term 700, add 1 to one w coefficient, swap two v rows, flip the sign of one u coefficient. Each printed "INVALID: no index convention satisfies the Brent equations".

Author's checker (read after mine; packed-integer slots with a stated bound, sound; run from a copy via run_checks.sh): "exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 42 bits, slot width 44 bits, 35672 blocks of 182 slots compared / PASS format=13x14x14 rank=1538", negative control rejected, "ALL CHECKS PASS", exit 0. Same D and bound as mine.

## Live sources (each fetched once, curl, User-Agent "V3R1T4S-research (honest client; curl)", no retries)

| Source | UTC | HTTP | sha256 | 13x14x14 cell |
|---|---|---|---|---|
| https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (createdAt 2026-10-09T11:45:48, 5456 entries) | 2026-10-15T09:23:01Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | {"format": [13, 14, 14], "rank": 1582} |
| https://fmm.univ-lille.fr/13x14x14.html | 2026-10-15T09:23:03Z | 200 | f4f5d1067f4dea0882d6c15b04fa4399609c5cd695777824ce1a96c6d22330cd | 1614 ("taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026", not a composition) |
| https://fmm.univ-lille.fr/ (main table, for the construction column) | 2026-10-15T09:30:41Z | 200 | d1580ec77377c36e3e21c66e51aa9b24c3c9a2544e0152395136bbee7816d627 | row 13x14x14: rank 1582, naive 2548, construction "Perminov 2026" (GitHub repository), not a composition |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:23:03Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | Research Findings and Status table (columns ZT rank, Z rank, Q rank): 13x14x14: 1614 (?), 1614 (1625), 1582 (1625); min = 1582 |
| https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-15T09:23:04Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 paths, truncated false; no 13x14x14, 14x13x14 or 14x14x13 file (README tables also list none) |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T09:23:05Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | row 45: 13x14x14 rank 1558 over Q |

The five sources the author recorded in table-record/README.md have byte-identical sha256 to my fetches (the author fetched 09:07Z, I fetched 09:23Z). Minimum over the four criterion sources: 1582. Repository trophy: 1558. Note: the Lille per-format page (1614) lags the Lille main table (1582); both are above 1538.

## Success criterion, clause by clause

1. "an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms)": MET. 1538 explicit u, v, w rows; no empty, all-zero or duplicate-index rows.
2. "for a format (n,m,p) with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}": MET. (13,14,14), max 14, already sorted.
3. "whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in fmm_sota.json [1582], the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html [1614], the minimum over the ZT/Z/Q columns ... in Perminov's README [1582], and the lowest rank for that format in MerlijnW70/fmm-schemes [none listed] (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four)": MET. 1538 < 1582 = min over the four; the author's fetches were within 9 seconds of the fetch time written in INDEX.csv, and my refetch 16 minutes later is byte-identical.
4. "The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims": MET. Claimed Q; verified over Q in exact integer arithmetic (no floats, no modular reduction, no sampling) by two independent methods of mine plus the author's.
5. "a scheme valid only over GF(2) counts here ONLY if ...": NOT APPLICABLE. Scheme is over Q (rational coefficients), so the F2 column was not needed.
6. "A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed": MET (not triggered). 1538 equals no listed value (1582, 1614, 1558). The Lille construction column for 13x14x14 is "Perminov 2026", not a composition. As a null model I computed the best block-split and tensor-product bounds from the live fmm_sota.json: best is 1633 (4x14x14 + 9x14x14 = 532 + 1101); 1538 is below every such composition, so it is not reachable by plain composition of catalogue ranks. The object's own note says it was derived from a parent 13x14x15 scheme (rank 1645) by restricting one axis; a restriction is not a composition of listed schemes, and the resulting 1538 is new.
7. "Ternary/integer re-derivations of a rank already attained over Q are NOT this target": NOT TRIGGERED. 1538 is below the Q rank 1582, so it is a new rank, not a ring upgrade.
8. "fewer additions at an existing rank is NOT this target": NOT TRIGGERED. The rank itself is new.
9. Repository's own TROPHY_CASE.md entry for this format: 1558 (row 45, 13x14x14 rank 1558 over Q). 1538 < 1558 by 20, so the result is not subsumed by the existing trophy; it strictly supersedes it.

## Partial wins considered

- p1 (17 <= max side <= 32): not applicable, max side is 14.
- p2 (GF(2)-only improvement): not applicable, the scheme is over Q and is a new characteristic-0 rank.
Neither partial win is claimed or needed; the full criterion is met.

## Hidden quantifiers and stretched definitions checked

- "sorted format": 13x14x14 is sorted; the catalogues index by sorted format and MerlijnW70 was checked under all three axis orders.
- "rank" counted as terms with all three factors nonzero: 1538 of 1538, no padding terms, no zero terms inflating or deflating the count.
- "exact": no floating point anywhere; int64 use is covered by an explicit 42-bit bound and cross-checked with arbitrary precision.
- "ring it claims": Q claimed; coefficients are genuinely non-integer, and the check is over Q.
- "ALL of" four sources: all four fetched live by me, not only read from the author's record.
- "live immediately before claiming": author's hashes match mine 16 minutes later.
- Lille per-format page vs main table disagree (1614 vs 1582); the stricter number 1582 was used and is still beaten.

## Verdict

PASS. The object is an exact rank-1538 bilinear scheme over Q for 13x14x14, verified by my own exact check of every Brent equation, with rank strictly below all four live criterion sources (minimum 1582) and below the repository's own trophy entry (1558). It is a genuine, non-subsumed win on the full success criterion.

confirmed_scope: The file claim/object/13x14x14_r1538_Q.json (sha256 4b613512756bdb5c0303dc17236ad63b3b8a4e931d898e75e863d95d6dd9ab9e) is an exact bilinear scheme over Q for the matrix multiplication format 13x14x14 with 1538 rank-one terms, each with all three factors nonzero, satisfying every Brent equation in exact arithmetic by my own independent check, and 1538 is strictly below the 13x14x14 rank in each of the four criterion sources as fetched on 2026-10-15 (fmm_sota.json 1582, Lille per-format page 1614, Perminov README minimum over ZT/Z/Q 1582, MerlijnW70 repository none) and below the TROPHY_CASE.md entry of 1558.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
