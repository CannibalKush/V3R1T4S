# CRITERION skeptic report: cell [213,26] over GF(2)

Object judged: `claim/object/code_q2_n213_k26_d77.json`, sha256
`924876aa988e3a9da62a776f88c297db6aa005b475fe3ad9e76291685851cd12` (matches claim.SHA256SUMS; all 7 listed files
verified OK with `shasum -a 256 -c`). The claim folder was the only input read. Only this cell is judged.

Own checks were written from scratch in `criterion_ws/mindist.py` (not the author's checker): rank by numpy GF(2)
Gaussian elimination; exact minimum distance by a numpy meet-in-the-middle (13+13 row split, 4 uint64 words per
codeword, `np.bitwise_count`) that counts every one of the 2^26 - 1 = 67,108,863 nonzero codewords into a weight
histogram, cross-checked by an independent packed-int Gray-code walk. Run under `nice -n 19`.

## Clause (1)
> "Rank is exactly k over GF(q), computed independently."

MEETS. Matrix parsed as 26 rows x 213 entries, all in {0,1}. Own Gaussian elimination over GF(2): rank 26.
(The MITM histogram independently confirms this: 0 nonzero messages map to the zero word.)

## Clause (2)
> "The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible
> (2^k <= ~2^32), ... never by sampling."

MEETS. 2^26 < 2^32, so full enumeration is the required method and was done. MITM counted exactly 67,108,863 nonzero
codewords (verified against 2^26 - 1), minimum weight 77 with A_77 = 1170; the Gray-code walk over all 2^26 - 1
codewords gives d = 77, A_77 = 1170; the two agree. No sampling. Full weight distribution recorded in
`criterion_ws/mindist.log` (sums to 2^26 - 1). Side check of the construction: the first 210 columns alone form a
[210,26,76] code (A_76 = 1995) and the 3-column tail cycles through powers of x mod x^3+x^2+1, as the object's
`construction` string says; rows 1..25 are cyclic shifts of row 0 in two 105-blocks (index-2 quasi-cyclic). This is
consistent with Construction X and is not itself a criterion clause.

## Clause (3)
> "d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/ cell for (q,n,k)
> at verification time, and at most the upper bound."

MEETS. One honest GET of `http://www.codetables.de/BKLC/BKLC.php?q=2&n=213&k=26` at 2026-10-15T00:14:28Z, HTTP 200,
User-Agent `V3R1T4S-research (honest client; curl)`, no retries. Page text: "[213,26] over GF(2) lower bound: 76
upper bound: 90"; the tabulated [213,26,76] is a subcode of a padded/extended Construction-X code, last modified
2001-01-30. sha256 of the fetched page `a0716470e57fc32f112482c5b8e3aabff76a7c1c055dd7d3e6a5b5fac18b5793`, identical
to the author's `table-record/README.md`. 77 > 76 and 77 <= 90. Null model: the trivial route of taking the
table's own [213,28,76] construction gives 76, not 77; the author's d is not reachable by lengthening a d=76 code
without the extra Construction-X structure, and the enumeration shows the +1 is real (A_77 = 1170, no weight-76 word).

## Clause (4)
> "The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and no newer
> arXiv claim already reaches that d."

MEETS, with one limit stated. One fetch each of the arXiv abstract and the HTML full text of 2609.37056 (dated
2026-09-29). Its seven codes are [172,21,66], [173,20,68], [176,21,68], [181,21,70], [184,21,72], [189,22,72],
[200,21,77]. Every [n,k,d] cell with n >= 100 named anywhere in the paper is:
(170,21,64) (172,21,66) (173,20,68) (176,21,68) (181,21,70) (184,21,72) (189,22,72) (200,21,77) (201,21,78)
(240,21,104). No cell has k = 26, none has n in 202..213, and the string "213" does not occur in the paper. Its
highest dimension is 22; no standard modification (puncture, shorten, extend, pad, subcode) raises k by 4 to
reach [213,26,77] from these, and the paper claims no such entry among its 22 improvements. The object is an
index-2 quasi-cyclic Construction-X code of its own description, not one of the seven.
Limit: my single arXiv API search for newer claims returned HTTP 301 and, under the no-retry rule, was not re-issued,
so "no newer arXiv claim" rests on the named primary source plus the live status source (codetables.de still
reads 76 at fetch time, and the paper states its results were checked by the table maintainer). That universal
negative is not fully verified by me.

## Partial wins considered
- `p1` (quantum stabilizer record): not applicable; this is a classical binary linear code.
- `p2` (improved upper bound): not applicable; nothing about the upper bound 90 is claimed or changed.
Neither is needed: the full success criterion is met for this one cell.

## Verdict
PASS. [213,26,77]_2, rank 26, d = 77 exact by full enumeration of all 2^26 - 1 codewords with two agreeing methods,
strictly above the live lower bound 76 and below the upper bound 90, not among or derived from the seven
LinCodeEvolve codes. Genuine, non-subsumed win for this cell, subject to the stated arXiv-search limit.

confirmed_scope: The generator matrix in claim/object/code_q2_n213_k26_d77.json (sha256 924876aa988e3a9da62a776f88c297db6aa005b475fe3ad9e76291685851cd12) has rank 26 over GF(2) and exact minimum distance 77 (A_77 = 1170) by full enumeration of all 67,108,863 nonzero codewords with two agreeing methods, which is strictly above the lower bound 76 and at most the upper bound 90 shown in the live codetables.de [213,26] cell fetched 2026-10-15T00:14:28Z, and it is not one of, nor by the paper's own text derived from, the seven LinCodeEvolve codes of arXiv:2609.37056; a live arXiv search for other newer claims was not completed.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
