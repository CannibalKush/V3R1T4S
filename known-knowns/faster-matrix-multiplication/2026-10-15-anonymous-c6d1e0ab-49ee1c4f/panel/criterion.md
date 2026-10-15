# CRITERION skeptic report: fmm-catalogue-small-format-rank, format 13x14x15, claimed rank 1645 over Q

Object: claim/object/13x14x15_r1645_Q.json
sha256 (from claim.SHA256SUMS): 49ee1c4f6642d1245e5af697eeb2f342024d04f06a0cc9113501ce8f45177144
All seven files in the claim folder were re-hashed and match claim.SHA256SUMS (shasum -a 256 -c: 7 x OK).

Notation note: the bank writes formats with angle brackets; this report writes them as 13x14x15 and the
generic format as (n,m,p) because the repository's checker rejects literal angle-bracket placeholders.

## 1. My own exact check (written before reading the author's checker code)

Method: decoded the vocab_rle_v1 rows to exact Fractions (1645 rows each of u, v, w; lengths 182, 210, 195);
scaled U, V, W globally by the LCM of their denominators (Du=40, Dv=40, Dw=5440, product 8704000) to integer
matrices; for each of the 182 A-indices a=(i,j) formed, with python-flint fmpz_mat exact integer arithmetic,
S_a = sum_k U[k,a] * V[k,:]^T W[k,:] (210 x 195) and required S_a == 8704000 * E_a, where E_a has 8704000 at
row (j,l), column index of C[i][l] for every l and 0 elsewhere. That is every one of the 182*210*195 = 7,452,900
Brent equations, in exact integers, no modular reduction, no sampling. The W index convention was detected on
slice 0 by trying both C row-major and C column-major; only column-major (w index = l*13 + i) matched, and the
author's checker docstring (read afterwards) states that same convention. Rank was counted as terms whose
u, v, w rows are all nonzero.

Real output (my_brent_check.py, run under nice -n 19 with the repository venv python):

    format n,m,p = 13,14,15; declared m (terms) = 1645; rows decoded = 1645
    terms with all three factors nonzero = 1645; terms with some zero factor = 0
    exact duplicate (u,v,w) triples = 0
    global denominators: Du=40 Dv=40 Dw=5440; product=8704000
    max |integer coefficient| after scaling = 14131200
    W index convention detected on slice 0: colmajor
    checked 182 A-slices x 210 x 195 = 7452900 Brent equations exactly; failing slices = 0; 3.2s
    RESULT: exact scheme for 13,14,15 over Q with rank 1645: PASS   [checker prints the format in angle brackets; rendered here without them]

Negative controls through my checker (null model: a pass must be falsifiable):
- one w coefficient changed from 1 to -1: "slice 0 matches NEITHER W convention, then FAIL"   [arrow in the original output rendered as a comma]
- last term dropped (1644 terms): "failing slices = 4 ... RESULT: FAIL"
- one u row zeroed: "failing slices = 42 ... RESULT: FAIL"

Author's checker, run from a copy of the claim folder (sh verify-it-yourself/run_checks.sh):
    exact integer check: D=8704000 (DU=40, DV=40, DW=5440), coefficient bound 40 bits, slot width 42 bits, 38220 blocks of 195 slots compared
    PASS format=13x14x15 rank=1645
    negative control rejected as expected (FAIL format=13x14x15 rank=1644: 840 of 38220 (a, b) blocks differ; first at A[3][4] x B[0][0])
    ALL CHECKS PASS
I read the author's checker after my own run: its packed-slot method is sound (slot width 42 bits exceeds the
stated 40-bit coefficient bound and D, so packed equality is slot-by-slot equality), and its D and rank agree with mine.

## 2. Live sources (one GET each, curl, User-Agent "V3R1T4S-research (honest client; curl)", no retries, 2026-10-15T09:13:47Z to 09:13:52Z)

| Source | HTTP | sha256 of body | Cell for 13x14x15 |
|---|---|---|---|
| fmm_sota.json (createdAt 2026-10-09T11:45:48, 5456 entries) | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | entries[3937] = {"format": [13, 14, 15], "rank": 1681} |
| Lille per-format page https://fmm.univ-lille.fr/13x14x15.html (template https://fmm.univ-lille.fr/{n}x{m}x{p}.html) | 200 | d2a562a11c213effc7df98468757cda923925f248fab408ed38c485039851158 | 13x14x15:1681, "taken from Andrew I. Perminov, FastMatrixMultiplication, GitHub, February 2026"; the only four-digit rank on the page is 1681 |
| Perminov README, section "Research Findings & Status", columns ZT / Z / Q | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | row: 13x14x15, ZT 1681 (?), Z 1681 (1714), Q 1681 (1714); min over ZT/Z/Q = 1681. "New best ranks" table also lists 13x14x15 at 1681 (ZT/Z), previous 1714 |
| MerlijnW70/fmm-schemes git tree (recursive, truncated=false, 39 paths) | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | no file for 13x14x15 (nearest: 13x13x15_m1591_ZT.json, 13x14x16_m1805_ZT.json) |
| V3R1T4S TROPHY_CASE.md | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | row 48: "13,14,15 rank 1677 over Q, below the minimum 1681 of the four criterion sources (-4)" |

All five body hashes equal the hashes in the author's table-record/README.md (author fetch 2026-10-15T09:07Z),
so the author compared against the same content I saw. Minimum over the four criterion sources: 1681.
Repository's own trophy entry for this format: 1677. Claimed rank: 1645 (36 below the sources, 32 below the trophy).

## 3. Clause-by-clause

- "an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms)":
  MET. The JSON holds 1645 (u, v, w) rows; decoded lengths 182 = 13*14, 210 = 14*15, 195 = 13*15.
- "for a format (n,m,p) with max(n,m,p) at most 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}":
  MET. (13,14,15): max 15 is at most 16; sorted triple is (13,14,15).
- "whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of" the four sources:
  MET. r = 1645 (1645 terms with all three factors nonzero, none zero, none duplicate) vs fmm_sota.json 1681,
  Lille page 1681, Perminov min(ZT,Z,Q) = 1681, MerlijnW70 none listed. 1645 is strictly below 1681.
- "(every one re-fetched live immediately before claiming; the scheme beats the minimum over all four)":
  MET. Author's fetches 2026-10-15T09:07:43Z to 09:07:48Z with INDEX.csv at 09:07:48Z; my re-fetches six minutes later
  return byte-identical bodies.
- "The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims":
  MET. Ring claimed Q; coefficients are rationals with denominators dividing 40, 40 and 5440; verified in exact
  integer arithmetic after global scaling, by my checker and by the author's, with negative controls rejected.
- "a scheme valid only over GF(2) counts here ONLY if ...": NOT APPLICABLE. The scheme is over Q, not GF(2)-only
  (denominators are even, so it does not even reduce mod 2). Beating the min over ZT/Z/Q covers "ANY ring" as the
  criterion defines it through the four sources.
- "A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank
  equals a value already listed (the Lille table has a 'construction' column listing such derivations)":
  MET. The object's note says it was derived from a 13x15x15 rank-1762 parent by restricting one axis (a linear
  combination f of 15 slices to 14), i.e. a peeling/restriction, not a composition, padding or block split; and in
  any case 1645 equals no listed value (the Lille page's construction polynomial is for the 1681 algorithm; no
  source lists 1645 for this format). The clause is not triggered.
- "Ternary/integer re-derivations of a rank already attained over Q are NOT this target": NOT TRIGGERED. 1645 is a
  new rank, not a re-derivation of 1681 or 1677.
- "fewer additions at an existing rank is NOT this target": NOT TRIGGERED. The rank itself is lower.
- Repository-internal bar (panel instruction): strictly below the TROPHY_CASE.md entry for this format, 1677:
  MET. 1645 is strictly below 1677. The new scheme supersedes trophy row 48 (same format, same target) rather than opening a new format.

## 4. Hidden quantifiers and stretched definitions hunted

- "ALL of" the four sources: checked each, including all three Perminov columns and the Lille per-format page
  separately from the digest; all read 1681. No source lists a lower value for the sorted format.
- Rank counted as terms with all three factors nonzero, independently of the declared "m": 1645 = 1645.
- The scheme is for the full 13x14x15 tensor (all 7,452,900 Brent equations hold), not a padded smaller format.
- The "(?)" in Perminov's ZT column is "previous rank undocumented", not "open", per the bank statement; the
  minimum still is 1681.
- Context only, not a clause: the stated parent 13x15x15 rank 1762 is itself below the listed 13x15x15 rank 1776
  (fmm_sota.json / Perminov Q); that parent was not checked here and this report makes no claim about it.

## 5. Partial wins considered

- p1 (max dim from 17 to 32): not applicable, max dim is 15; the full criterion is the relevant bar and is met.
- p2 (GF(2)-only improvement): not applicable, the scheme is over Q and is a new rank overall.
No partial win is needed; the full success criterion is met literally.

## 6. Limits

- I verified the scheme and the five sources; I did not fetch MerlijnW70's README (the criterion names the
  repository; its scheme files live under schemes/ and the recursive tree, not truncated, has none for 13x14x15).
- Rank is a value over Q only; no claim is made about ZT or Z ranks for this format.
- The derivation note in the object ("Parent ... 13x15x15 r1762 ... axis=2") was not reproduced; it is irrelevant to
  the clauses since 1645 is not a listed value.

## Verdict

PASS. claim/object/13x14x15_r1645_Q.json is an exact rank-1645 bilinear scheme for 13x14x15 over Q (independently
verified, every Brent equation in exact integer arithmetic, negative controls rejected), and 1645 is strictly below
1681, the minimum over the four live criterion sources fetched 2026-10-15T09:13Z, and below the repository's own
trophy entry 1677. Genuine, non-subsumed win on the full success criterion (it supersedes the existing 1677 trophy
for the same format rather than being covered by it).

confirmed_scope: The file claim/object/13x14x15_r1645_Q.json (sha256 49ee1c4f6642d1245e5af697eeb2f342024d04f06a0cc9113501ce8f45177144) is an exact bilinear scheme over Q for the matrix multiplication format 13x14x15 with 1645 rank-one terms (all three factors nonzero, no duplicates), verified by an independent exact-integer check of all 7,452,900 Brent equations, and 1645 is strictly below 1681, the minimum rank for the sorted format 13x14x15 in fmm_sota.json (createdAt 2026-10-09T11:45:48), the Lille per-format page, Perminov's ZT/Z/Q columns and MerlijnW70's fmm-schemes tree as fetched live on 2026-10-15T09:13Z, and below the V3R1T4S TROPHY_CASE.md entry 1677 for this format; rank over Q only.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
