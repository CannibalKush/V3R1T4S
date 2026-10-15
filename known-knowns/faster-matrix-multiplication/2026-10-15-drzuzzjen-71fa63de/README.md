# <5,5,5> rank 93: a ternary straight-line program with 358 additions (record table: 383)

## What

The file 5x5x5_m93_cr358_ZT_reduced.json (sha256 71fa63de…129f5c) is a ternary straight-line program that computes the 5x5x5 matrix product exactly over Z with 93 multiplications and 358 binary additions/subtractions counted under Perminov's reduced convention (negations and single-term aliases free, every intermediate ternary); it is a re-reduction of the same bilinear scheme as Perminov's 5x5x5_m93_cr383 file and strictly below 383, which is the only and hence minimum reduced count for 5x5x5 rank 93 in the Perminov sources fetched 2026-10-15T15:20Z; no lower count for this format and rank appears in reduced_known.json, the README, the CHANGELOG, the Lille 5x5x5 page or matmulcatalog COVERAGE.md (+846).

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (standard-library Python 3; a few seconds on a laptop). The checker was written from the
definition in Perminov's README by an independent context; it checks the full tensor identity over Z, executes the
program on 24 random integer matrix pairs, enforces coefficients in {-1,0,1} after expansion and counts additions as the
sum over every form of (terms - 1).

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Perminov, FastMatrixMultiplication, addition_reduced_ZT | 5x5x5 rank 93 | 383 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T15:20:24Z (panel re-fetch 15:21:27Z) |
| Perminov, arXiv:2512.13365v2, results table | 5x5x5 rank 93 | 383 | https://arxiv.org/abs/2512.13365 | 2026-10-15T15:23:35Z |
| fmm_sota.json (best rank) | 5x5x5 | rank 93 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T15:20:26Z |
| Lille catalogue | 5x5x5 | rank 93, no complexity variant cited | https://fmm.univ-lille.fr/5x5x5.html | 2026-10-15T15:20:27Z |
| matmulcatalog COVERAGE 'adds' | <5,5,5> | naive count only | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T15:20:27Z |

Details and page hashes: the-record-we-beat/RECORD.md.

## Not claimed

- No new rank: the bilinear scheme is Perminov's own rank-93 ternary 5x5x5 scheme (identical rank-one terms); only the straight-line programs for the three maps are shorter (U 103 -> 98, V 105 -> 96, W 175 -> 164).
- No claim about total operations, practical speed or any other format.
- No optimality claim; the search was randomized and time-capped.
- A closed, unmerged V3R1T4S PR (#21, 2026-10-14) reported 378 for this cell; it is not a record table, and 358 is below it too.

## Credits

- A. I. Perminov: the rank-93 ternary scheme and its 383-addition reduced program, the reduced-scheme format and the counting convention (https://github.com/dronperminov/FastMatrixMultiplication, arXiv:2512.13365).
- J. Moosbauer and M. Poole: the rank-93 <5,5,5> scheme cited by the Lille catalogue (arXiv:2502.04514).
- A. Sedoglavic and the Lille FMM catalogue (https://fmm.univ-lille.fr/, fmm_digest).
- solven-eu/matmulcatalog (coverage table).
- J. Boyar and R. Peralta: the shortest-linear-program heuristic; its ternary-cancellation variant on U, V and W^T was described by calgulbenkian's team in elder-plinius/V3R1T4S PR #161 (our implementation is independent: how-we-built-it/bp.py).
- The transposition principle (Tellegen; Bordewijk), used for the W map.
