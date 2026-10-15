# Pre-registration

target_id: fmm-catalogue-small-format-rank
frozen_utc: 2026-10-14T17:54:00Z
null_test: not needed because the claim is an explicit scheme checked by a deterministic exact checker against table values

**Timing note.** The success rule below was copied verbatim from the bank into the search team's brief at 2026-10-14T17:54Z, before the team's engine or sweep existed; this scheme was found later that day or the next. The rule was not chosen by us. The success rule was not chosen by us. It is the bank's criterion, quoted below, which was fixed before the search began.

## Success rule (bank criterion, verbatim except that the Lille URL template's angle brackets are written as braces, because the kit's checker reads an angle-bracketed n as an unfilled placeholder)

Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format <n,m,p> with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

## Statistic and threshold

- Statistic: the number of terms whose three factors are all nonzero, after an exact check of every Brent equation over Q.
- Threshold: strictly below the minimum, for the sorted format, over fmm_sota.json, the Lille per-format page, Perminov's README (ZT, Z and Q columns) and MerlijnW70's repository. In addition, no equal or better entry for the same cell may exist in the V3R1T4S trophy case.
