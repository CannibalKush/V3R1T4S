# Criterion skeptic report: 13x15x15 at rank 1762

## Own checker (written before reading the author's checker)
My script (criterion_ws/mycheck.py) parses the sparse_flat_pairs rows into exact Fractions, and for every one of the 195 output indices c accumulates the sum over terms of U[a]*V[b]*W[c] and compares it with the matrix-multiplication tensor, in exact rational arithmetic (no modular shortcut). Real output:

    dims 13 15 15 rows 1762 1762 1762 encoding sparse_flat_pairs ring Q
    fractional entries 21727 17487 21250
    rank (all three nonzero) 1762 total rows 1762
    denominator lcms 5440 40 40
    C=i*p+l bad output entries: 192
    C=l*n+i bad output entries: 0

U indexes A as i*15+j, V indexes B as j*15+l, and W indexes C transposed as l*13+i (the stated Perminov convention). Under that indexing all 195 Brent equation blocks hold exactly; under row-major C indexing they fail, so the convention is not optional. Output transposition is a relabeling of the output index and does not change the tensor rank. Rank counted as terms with all three factors nonzero: 1762. The coefficients are genuinely rational (denominators up to 5440), so the ring is Q, not Z or a finite field. I did not run the author's checker.

## Live sources (each fetched once, UA 'V3R1T4S-research (honest client; curl)', 2026-10-15)
- fmm_sota.json: entry for format [13, 15, 15] rank 1776 (file createdAt 2026-10-09T11:45:48).
- Lille per-format page https://fmm.univ-lille.fr/{n}x{m}x{p}.html at 13x15x15: rank 1797, "taken from: Andrew I. Perminov, FastMatrixMultiplication, February 2026". No composition or padding derivation is listed for this format.
- Perminov README: table rows ZT/Z/Q: 1803 (Z) and 1776 (Q) in the new-best table; 1797 (?) / 1797 (1803) / 1776 (1803) in the full table. Minimum 1776.
- MerlijnW70 fmm-schemes tree (39 entries, not truncated): no scheme for 13x15x15 (only 2x13x15, 10x13x14, 11x13x15, 12x12x15, 12x13x15, 13x13x15).
- TROPHY_CASE.md: no 13x15x15 row (zero matches for the format, 1762 or 1763).
- Repository known-knowns/faster-matrix-multiplication (contents listing of 21 dated packages, plus a recursive git tree): the only file for this format is the merged package 2026-10-14-anonymous-c6d1e0ab-710c8ff6, object 13x15x15_r1763_Q.json. No other merged package holds a 13x15x15 scheme in any axis order.
- Maintainer comment on pull request #164 (elder-plinius, 2026-10-15T18:41:19Z), quoted: "Also worth knowing: the build log for #164 shows an unpublished (13,15,15) rank-1762 scheme, one below the merged #130. Feel free to submit it."

Bar to beat: min(1776, 1797, 1776, none) = 1776 externally, and 1763 internally (merged pull request #130). 1762 is strictly below every one of them.

## Clauses
1. "an explicit bilinear scheme (U, V, W ...) for a format with max(n,m,p) at most 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}": explicit U, V, W given; max side 15; sorted (13,15,15) is neither excluded format. Met.
2. "number of rank-one terms r is STRICTLY LESS than ALL of" the four sources: 1762 is below 1776 (sota), below 1797 (Lille), below 1776 (Perminov minimum of ZT/Z/Q), and MerlijnW70 has no entry, so nothing to tie. Met. The claim sentence says "strictly fewer than 1763, the lowest rank listed ... in the four live record tables and the V3R1T4S trophy case"; that is imprecise (the four tables list 1776 or worse, the trophy case lists nothing for this format, and 1763 is the repository's merged package), but 1762 is below every one of those values, so the imprecision does not change the verdict.
3. "verified in exact arithmetic ... over the ring it claims": ring Q claimed; I verified in exact Fractions. Met. The scheme is not GF(2)-only, so the p2 caveat does not apply.
4. "composing, padding or block-splitting ... does not count if the resulting rank equals a value already listed": the object's note says it comes from a rank-1842 14x15x15 scheme by an axis-0 peel with absorption (raw 1796, 34 absorbed). The result 1762 equals no listed value (1776, 1797, 1763). Met. The Lille page lists no construction for this format.
5. Not a ternary re-derivation of a Q rank, nor an additions-only result: rank 1762 is below the best Q rank. Met.
6. Scope splits: one format, one ring (Q); nothing wider is asserted than I could check.

## Null models and hidden quantifiers
"ANY ring" is satisfied by Q. The rank equals the row count, so there are no padded zero terms. Null model: the same cell is already improved by this contributor's own merged 1763, which I treated as the bar; 1762 is one below, a strict improvement, not a tie and not a re-submission of 1763. I did not independently scan open pull requests for a duplicate; the maintainer comment explicitly invites this scheme.

## Partial wins considered
p1 (max side from 17 to 32) does not apply (max side 15). p2 (GF(2)-only) does not apply (coefficients are rational, ring Q). The full criterion is met, so no partial win is needed.

## Verdict
Pass: the object meets the full success criterion.

confirmed_scope: The object claim/object/13x15x15_r1762_Q.json (sha256 5b97769fb1c3115c7195f0c508e0cae9ded013ef2543a7f0d5aa4147410e1647) is, by my own exact rational check using Perminov's index convention (C stored transposed), a correct bilinear scheme over Q for the 13x15x15 matrix product with 1762 terms having all three factors nonzero, strictly below 1776 (fmm_sota.json and the Perminov table minimum), 1797 (Lille), the absent MerlijnW70 entry, and the repository's merged 1763, as fetched 2026-10-15.

context: Claude Code subagent (Fable 5.1), fresh context

pass: true
