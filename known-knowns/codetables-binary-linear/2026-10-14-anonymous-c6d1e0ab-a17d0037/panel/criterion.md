# CRITERION review: binary [173,17] code claim (target `codetables-binary-linear`)

Object under review: `claim/object/win_q2_n173_k17_d72.json`, sha256
`a17d00378317979d9fe0acb452d3cce805f55cb17595a8407acb9b56b7b51a76` (from claim.SHA256SUMS; all six
listed claim files re-hashed OK). Claim: a 17 x 173 generator matrix over GF(2) of rank 17 whose code has
minimum distance exactly 72, strictly above the codetables.de lower bound 70 for (q,n,k) = (2,173,17).

How I checked: I did not execute the author's checker. I wrote my own scripts in `criterion_ws/`
(`criterion_check.py`, `lce_derivation_check.py`, `lce_core_only_check.py`), ran them with `python -I`
from outside the claim folder with the object passed as an argument, and kept their outputs beside them.
Live sources were each fetched once with curl and the User-Agent `V3R1T4S-research (honest client; curl)`,
no retries: the codetables.de cell, the arXiv abstract page and HTML full text of 2609.37056, and one
arXiv API listing. Saved copies are under `criterion_ws/fetch/`.

## Clause 1

> (1) Rank is exactly k over GF(q), computed independently.

Met. Shape 17 x 173, every entry in {0,1}. Gaussian elimination over GF(2) (leading-bit reduction on
packed row integers, my own code) gives rank 17 = k. Cross-check: the numpy enumeration of all 2^17
messages yields 131072 distinct codewords with the zero word occurring exactly once.

## Clause 2

> (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when
> feasible (2^k <= ~2^32), or, for large k (or large k with small n-k, via the dual and MacWilliams
> identities), by two independent exact minimum-distance implementations that agree; never by sampling.

Met. k = 17 is feasible; all 2^17 - 1 = 131071 nonzero codewords were enumerated by two independent
methods (a Gray-code walk over packed integers, and a numpy doubling construction of the full codeword
array). Both give d = 72 and A_72 = 6341, matching the claimed d and A_d. Full weight distribution:
72:6341, 80:39440, 88:59586, 96:23885, 104:1785, 112:34 (all weights are multiples of 8). The MacWilliams
transform of this distribution is integral and nonnegative and sums to 2^156, as it must. The structure
explains the count: rows 0-15 are simultaneous cyclic shifts of row 0 in two length-85 blocks (a
double-circulant [170,16,72] core, A_72 = 4590, which is the full span of all 85 shifts), row 16 adds a
[170,17,69] code (A_69 = 1751), and columns 170-172 are the [3,1,3] repetition code on row 16
(Construction X), so d = min(72, 69+3) = 72 and A_72 = 4590 + 1751 = 6341. No sampling anywhere.

## Clause 3

> (3) d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/
> cell for (q,n,k) at verification time, and at most the upper bound.

Met. One fetch of `BKLC.php?q=2&n=173&k=17` at 2026-10-14T16:16:39Z returned HTTP/1.1 200 OK with the text
"Bounds on linear codes [173,17] over GF(2) lower bound: 70 upper bound: 77". The cell's recorded
construction is a subcode of a [173,18,70] Construction X code from a quasi-cyclic chain (Grassl-White,
ISIT 2005; cell last modified 2003-04-09; upper bound BK 1993). 72 > 70 and 72 <= 77. The Griesmer bound
for [173,17]_2 is d <= 80, so the tabulated 77 is the binding upper bound and 72 respects it. The author's
`table-record/table_snapshot.md` interval [70,77] agrees with the live cell.

## Clause 4

> (4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and
> no newer arXiv claim already reaches that d.

Met, to the extent checkable with single fetches. Evidence:

- arXiv:2609.37056 (submitted 2026-09-29, EPFL) lists its seven codes as [172,21,66], [173,20,68],
  [176,21,68], [181,21,70], [184,21,72], [189,22,72], [200,21,77]. Its Table 3 of all 22 improved entries
  contains only k = 20, 21, 22 (n = 171-189, 200, 201). There is no k = 17 entry anywhere in the paper.
- Parameter argument: shortening ([n-1,k-1,>=d]), puncturing ([n-1,k,>=d-1]), subcodes and zero-column
  padding applied to the seven codes give at (173,17) at best d >= 68 (subcodes of [173,20,68], or
  [176,21,68] shortened three times plus a subcode); every other route gives less. 68 is below even the
  table's 70, so the claimed 72 is not a consequence of LinCodeEvolve's results.
- Structural test: I rebuilt LinCodeEvolve's [173,20,68] from its Appendix A (m = 85, index 2,
  h = (x^4+x^3+x^2+x+1)(x^8+x^5+x^4+x^3+x^2+x+1)(x^8+x^7+x^6+x^5+x^4+x^3+1), f2 = x^15+x^11+x^6+x^3+x^2+1,
  tails 01001/10100/01010). Full enumeration of its 2^20 - 1 codewords gives d = 68, A_68 = 1156, exactly
  the paper's figures, so the reconstruction is right. The claimed code is not a subcode of it (with or
  without the tail columns). The claimed core's cyclic parent has check polynomial
  (x^8+x^5+x^4+x^3+x^2+x+1)(x^8+x^7+x^3+x+1), two octic cyclotomic cosets of x^85+1; no multiplier in
  Z_85^* maps that pair into the cosets of the [173,20,68], [172,21,66] or [176,21,68] parents, so no
  quasi-cyclic-structure-preserving permutation can embed it there. For [181,21,70] and [184,21,72] the
  coset condition admits 128 (u1,u2,swap) candidates, but explicit containment under all 85 x 85 block
  shifts fails for the claimed [170,17] part and even for the 16-dimensional core alone (0 hits). The
  claimed [170,17] part is also not itself quasi-cyclic (the shift of row 16 leaves its span), unlike the
  LinCodeEvolve parents. The code shares only the general design family (index-2 quasi-cyclic core of
  block length 85 plus a Construction X repetition tail), which the paper itself attributes to the
  classical Grassl-White approach.
- Newer arXiv claims: one API listing (200 most recent matches for "codetables", "best known linear
  codes", "new binary linear codes" and similar phrases) returned 82 entries. The 2026 entries are
  2610.15535 (symplectic hull theory), 2609.39081 (edit-distance DNA barcodes), 2609.37056 (LinCodeEvolve),
  2608.18664 (abelian codes; records over F_3 and F_4), 2608.12414 and 2606.08750 (Z_4 codes), and
  2607.02170 (entanglement-assisted quantum codes). None claims a binary [173,17] code with d >= 72.
- Limits: the arXiv search is a keyword search over abstracts, so a paper not using those phrases would be
  missed; and equivalence to a subcode of a LinCodeEvolve code under an arbitrary coordinate permutation
  (beyond the structure-preserving maps tested) is not computationally excluded. Neither the paper nor the
  listing claims any such derivation, and the parameter argument makes the result new regardless.

## Hidden quantifiers, stretched definitions, null models

- The bank's binary tables cover n <= 256; n = 173 is in range. The claim states d exactly 72, and the
  enumeration confirms exactness rather than a lower bound.
- Columns 170-172 are three identical columns (dual distance 2). That is inherent to Construction X with
  the [3,1,3] repetition code and does not change the [173,17,72] parameters. Per the kit I judge only this
  cell and assert nothing about [172,17], [174,17] or other neighbours.
- Null model: a random [173,17] binary code has d near 55 (Gilbert-Varshamov); the table's 70 already comes
  from a structured quasi-cyclic chain; 72 is a +2 gain inside the Griesmer (80) and tabulated (77) upper
  bounds. The claimed count A_72 = 6341 matches the independently computed value, so no weight data was
  tuned.
- codetables.de lower bounds are closed under the standard derivations, and the fetched cell shows 70 with
  its derivation, so a 72 at (173,17) is not already implied by a neighbouring cell. I relied on that
  closure rather than fetching neighbour cells (single-fetch rule).
- The author's checker and its exclusion rule (q = 2, 19 <= k <= 22, 170 <= n <= 240) were read but not
  relied on; all numbers above come from my own code and my own fetches.

## Partial wins considered

- `p1` (quantum stabilizer record): not applicable; the object is a classical binary linear code.
- `p2` (improved upper bound): not applicable; no non-existence certificate is offered and the upper bound
  77 is untouched.

The claim is judged against the full success criterion only.

## Verdict

All four clauses are met with my own evidence: rank 17; exact d = 72 (A_72 = 6341) by two full
enumerations; strictly above the live lower bound 70 and at most the upper bound 77 at verification time;
not one of, not a standard derivative of, and not structurally contained in the LinCodeEvolve codes, with
no newer arXiv claim found at this cell. Genuine, non-subsumed +2 win at (2,173,17). PASS.

confirmed_scope: The matrix in claim/object/win_q2_n173_k17_d72.json (sha256 a17d00378317979d9fe0acb452d3cce805f55cb17595a8407acb9b56b7b51a76) is a 17 x 173 GF(2) generator matrix of rank 17 whose code has, by two independent full enumerations of all 131071 nonzero codewords, minimum distance exactly 72 with 6341 minimum-weight words, which strictly exceeds the lower bound 70 and does not exceed the upper bound 77 shown in the live codetables.de cell for q=2, n=173, k=17 fetched once at 2026-10-14T16:16:39Z, and which is neither one of nor a subcode or standard derivative (under the quasi-cyclic-structure-preserving maps tested) of the seven arXiv:2609.37056 LinCodeEvolve codes, whose published improvements are all at k in {20,21,22}.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
