# CRITERION skeptic report: code-2-175-25

Claim under test (CLAIM.md, verbatim): "object/code_q2_n175_k25_d61.json is a 25 x 175 generator
matrix over GF(2) of rank 25 whose linear code has minimum distance exactly 61, strictly above the
codetables.de lower bound of 60 for (q, n, k) = (2, 175, 25)." Target id `codetables-binary-linear`.

Inputs read: the claim folder only (CLAIM.md, INDEX.csv, REPRODUCE.md, object/, table-record/,
verify-it-yourself/) and claim.SHA256SUMS. All seven hashes in claim.SHA256SUMS verified OK
(`shasum -a 256 -c`). Object file: claim/object/code_q2_n175_k25_d61.json, sha256
5128a84caf064a0c4b0b6bd46d4c8d26e02cddac4bbc988437a72c947859e17c (same value in INDEX.csv).

Method: I did not rely on the author's checker. I wrote three checkers of my own in criterion_ws/
(check_pure.py: standard library, packed-int Gray-code walk; check_numpy.py: numpy meet-in-the-middle
enumeration with hardware popcount plus a MacWilliams cross-check; structure.py: polynomial check of
the author's stated construction) and ran them with `nice -n 19` on the object file. Outputs are kept
in criterion_ws/pure_out.txt, numpy_out.txt, structure_out.txt. Network: exactly one honest GET of the
live codetables.de cell and exactly one honest GET of the arXiv API, each with User-Agent
`V3R1T4S-research (honest client; curl)` and no retries; headers, bodies, times and hashes are kept in
criterion_ws/fetch/.

## Clause-by-clause

### Clause 1
> "(1) Rank is exactly k over GF(q), computed independently."

**Met.** The JSON key "G" holds 25 rows of 175 entries; all 4,375 entries are JSON integers 0 or 1
(my check rejects booleans with `type(x) is int`; the author's `x in (0, 1)` would have accepted
`true`/`false`, so this stretched-definition route was checked and is not used). Two independent rank
computations, (a) elimination keyed on the leading bit of packed Python ints and (b) explicit row
reduction of a uint8 matrix mod 2, both give rank 25 = k. No zero columns and no repeated columns, so
the length 175 is not padded.

### Clause 2
> "(2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords
> when feasible (2^k <= ~2^32), or, for large k ..., by two independent exact minimum-distance
> implementations that agree; never by sampling."

**Met.** 2^25 = 33,554,432 <= 2^32, so full enumeration is the required route and I did it twice,
with different methods:

- check_pure.py: Gray-code walk over all 33,554,431 nonzero codewords (one XOR of a packed 175-bit
  int per step, popcount via `bin().count`), 36.8 s. Result d = 61, A_61 = 95.
- check_numpy.py: all 2^13 combinations of rows 0..12 XOR-crossed with all 2^12 combinations of rows
  13..24 (8192 x 4096 = 2^25 codewords, zero word removed), `np.bitwise_count` on 3 x uint64 words,
  1.9 s. Result d = 61, A_61 = 95.

The two full weight distributions are identical, entry for entry (A_61 = 95, A_62 = 420,
A_63 = 1176, A_64 = 3036, ..., A_115 = 26, A_172 = 1; total 33,554,431). MacWilliams cross-check: the
dual weight distribution computed from this primal distribution is integral and non-negative and sums
to exactly 2^150, as it must for a genuine [175,25] code (dual distance 5). No sampling anywhere.
The author's own figures (d = 61, A_d = 95) agree, but my verdict rests on my runs.

### Clause 3
> "(3) d is STRICTLY GREATER (direction: max) than the lower bound in the live
> http://www.codetables.de/ cell for (q,n,k) at verification time, and at most the upper bound."

**Met.** One GET of `http://www.codetables.de/BKLC/BKLC.php?q=2&n=175&k=25` at
2026-10-14T19:15:17Z returned HTTP 200 (3,448 bytes, no redirect). Page text: "Bounds on linear codes
[175,25] over GF(2) / lower bound: 60 / upper bound: 72", construction of the tabulated [175,25,60]
code: subcode of a [175,27,60] shortening of a [176,28,60] Blokh-Zyablov concatenated code, "last
modified: 2001-01-30"; the upper bound 72 is Brouwer's (Berntzen-Kemper). The fetched page's sha256
is 248159ace5ed9e247b42b6e0690518c0a81e32fa2b2527d84c460f1bbe68307e, byte-identical to the hash the
author recorded in table-record/README.md for the fetch at 2026-10-14T19:00:20Z. 61 > 60 (strict,
direction max) and 61 <= 72. Hidden-quantifier check: "at verification time" is satisfied by my own
fetch today, not the author's. Null model: the cell's lower bound is the table's own propagated value
(the displayed derivation chain shows shortening and subcode propagation already applied), so a 61 at
this cell is not implied by any neighbouring cell; judged for this one cell only.

### Clause 4
> "(4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from
> them, and no newer arXiv claim already reaches that d."

**Met on the available evidence; the second half is a bounded negative search by nature.**

- Not a LinCodeEvolve code, not derived from one: one arXiv API GET (export.arxiv.org, query
  `all:LinCodeEvolve OR all:codetables OR abs:"best known linear codes"`, newest first, max 100;
  the http URL 301-redirected once to https inside the same request; totalResults 35, all 35
  returned) at 2026-10-14T19:15:18Z. The abstract of 2609.37056v1 (2026-09-29, "Evolving Towards
  Better Codes: LLM-Guided Search for High-Distance Binary Linear Codes") lists the seven codes:
  [172,21,66], [173,20,68], [176,21,68], [181,21,70], [184,21,72], [189,22,72], [200,21,77], "six of
  which have concise quasi-cyclic descriptions", improving 22 table entries "with standard code
  modification techniques". All seven have dimension 20, 21 or 22. The object has dimension 25.
  Puncturing, shortening, parity extension and Construction X never raise dimension, so no
  [175,25,*] code is a standard derivative of any of them. Independently, structure.py confirms the
  object is exactly the author's stated algebraic construction: h = 0x36a5431 =
  (x+1)(x^8+x^5+x^4+x^3+x^2+x+1)(x^8+x^6+x^5+x^4+x^2+x+1)(x^8+x^6+x^5+x^4+x^3+x+1) divides x^85 - 1,
  g = (x^85-1)/h has degree 60, row i of the first 170 columns equals (g x^i, g (x^i f mod h)) with
  f = 0xe600fc (quasi-cyclic index 2, m = 85; rows are successive cyclic shifts within each 85-block),
  and columns 170..174 are the five stated message functionals (bit i of each mask in row i). The
  170-column core alone has d = 60 with A_60 = 680, and every one of those 680 words picks up 1 to 5
  ones from the five appended columns (joint counts: 95, 221, 215, 119, 30), which is why d = 61 with
  A_61 = 95. This is Construction X with the trivial [5,5,1] auxiliary code on a quasi-cyclic chain;
  the criterion has no originality clause other than the LinCodeEvolve exclusion, which it clears.
- No newer arXiv claim reaching d = 61 at [175,25]: in the 35 results the newest is 2609.37056
  itself; no title or abstract contains "175"; the only other 2026 coding-theory hit (2608.18664,
  abelian codes) claims records over F_3 and F_4 only; the 2021 quasi-cyclic/quasi-twisted record
  papers (2108.06752, 2108.10316) predate the table state and the live cell still reads 60 today.
  I cannot prove a universal negative: a claim phrased without these terms, or listed only in a paper
  body, would be missed. confirmed_scope below is worded to this bound.

## Partial wins considered

- `p1` (quantum stabilizer record): not applicable; no stabilizer code is claimed.
- `p2` (improved upper bound certificate): not applicable; the upper bound 72 is untouched.
The claim is made against the full success criterion and needs no partial win.

## Verdict

PASS. All four clauses are met for the single cell (q, n, k) = (2, 175, 25): the object is a rank-25
generator matrix of a binary linear [175,25,61] code with exact minimum distance established by two
independent full enumerations of all 33,554,431 nonzero codewords (MacWilliams-consistent), 61 is
strictly above the live codetables.de lower bound 60 and at most the upper bound 72 at my
verification time, the code is neither one of nor derivable from the seven dimension-20..22
LinCodeEvolve codes, and a bounded arXiv search found no newer competing claim. The improvement is
one unit, the smallest possible, but it is genuine (no padding, exact count) and non-subsumed within
the table for this cell. Not judged: the author's neighbouring-length derivations, if any.

confirmed_scope: The 25 x 175 matrix in claim/object/code_q2_n175_k25_d61.json (sha256 5128a84caf064a0c4b0b6bd46d4c8d26e02cddac4bbc988437a72c947859e17c) has rank 25 over GF(2) and generates a binary linear [175,25,61] code with exactly 95 codewords of weight 61, established by two independent full enumerations of all 33,554,431 nonzero codewords, and 61 exceeds the lower bound 60 and is below the upper bound 72 shown in the live codetables.de cell for q=2, n=175, k=25 fetched once at 2026-10-14T19:15:17Z, while the code is not one of, and by dimension cannot be a standard derivative of, the seven LinCodeEvolve codes of arXiv:2609.37056 (all of dimension 20 to 22), and a single arXiv API query on 2026-10-14 found no newer claim of a binary [175,25] code with minimum distance 61 or more.

context: Claude Code subagent (Fable 5.1), fresh context

pass: true
