# Fewer additions for <4,5,8> at rank 118: 470 against 513

## What

The program in claim/object/4x5x8_m118_cr470_ZT_reduced.json (sha256 8f63968828f21bb5d9ac3954a4424a742a68f22c641afbd4c507d26d3f7e3a2f) is a ternary straight-line program that computes the 4x5 by 5x8 integer matrix product exactly with Perminov's 118 products, using 470 additions under the reduced convention (U 102, V 146, W 222), against 513 for his only live addition_reduced_ZT file for that format and rank, with the Lille page citing no count and COVERAGE.md giving only a naive 1521.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/4x5x8_m118_cr470_ZT_reduced.json`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only (`sym_check.py`, optional, needs sympy).
- **Rough laptop time**: a few seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 4x5x8 rank 118 | 513 (minimum over his files for this format and rank; one file) | 470 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:20Z |
| Perminov, arXiv:2512.13365, Table 1 | 4x5x8 rank 118 | 513 | 470 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 4x5x8 | rank 118 | rank 118 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:20Z |
| Lille per-format page | 4x5x8 | rank 118; no complexity variant or operation count cited | 470 | https://fmm.univ-lille.fr/4x5x8.html | 2026-10-15T22:25:20Z |
| matmulcatalog COVERAGE.md, adds column | 4x5x8 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 470 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:20Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 4x5x8 rank 118 | format absent at this rank | 470 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 470 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:20Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 118, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-118 ternary scheme and its 513-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 118**, cited by the Lille catalogue (https://fmm.univ-lille.fr/4x5x8.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
