# Fewer additions for <5,5,6> at rank 110: 413 against 460

## What

claim/object/5x5x6_m110_cr413_ZT_reduced.json (sha256 760a6fabaf3fef7778e29b48d9b96dca9ae9dc8686afa84060805ac3be723354) is a straight-line program with all expanded coefficients in {-1,0,1} that computes the 5x5 by 5x6 product exactly over Z with rank 110 (Perminov's own 110 products, equal to the best listed rank) using 413 reduced additions (U 108, V 114, W 191), strictly below the 460 of the only live 5x5x6 addition_reduced_ZT file, with no lower count on the Lille page or in COVERAGE.md.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/5x5x6_m110_cr413_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 5x5x6 rank 110 | 460 (minimum over his files for this format and rank; one file) | 413 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:16Z |
| Perminov, arXiv:2512.13365, Table 1 | 5x5x6 rank 110 | 460 | 413 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 5x5x6 | rank 110 | rank 110 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:16Z |
| Lille per-format page | 5x5x6 | rank 110; no complexity variant or operation count cited | 413 | https://fmm.univ-lille.fr/5x5x6.html | 2026-10-15T22:25:16Z |
| matmulcatalog COVERAGE.md, adds column | 5x5x6 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 413 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:16Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 5x5x6 rank 110 | rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 556-110     1,325     511            492      833    62.9      0.18 , 0.12 , 0.08 / 556-110   1,333     511             495       838    62.9       0.1, 0.12, 0.08 / 556-110   1,325     511             496       829    62.6      0.16, 0.16, 0.08 | 413 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 413 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:16Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 110, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-110 ternary scheme and its 460-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 110**, cited by the Lille catalogue (https://fmm.univ-lille.fr/5x5x6.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
