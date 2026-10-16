# Fewer additions for <2,8,8> at rank 100: 418 against 424

## What

The program in claim/object/2x8x8_m100_cr418_ZT_reduced.json (sha256 674e65a792736a9bf4930d7e529fb901990cafa22ddf52baaf6c2ed0d256a87f) exactly computes the 2x8 by 8x8 product over Z with 100 products, the same 100 products as Perminov's 2x8x8_m100_cr424_cn608_ZT_reduced.json, using 418 reduced additions (U 90, V 154, W 174) with all expanded intermediates ternary, which is below 424, the only and minimum reduced count for this format and rank in his live addition_reduced_ZT directory on 2026-10-15, with no Lille-page complexity variant and no matmulcatalog adds value for 2x8x8 found.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/2x8x8_m100_cr418_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 2x8x8 rank 100 | 424 (minimum over his files for this format and rank; one file) | 418 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:35Z |
| Perminov, arXiv:2512.13365, Table 1 | 2x8x8 rank 100 | 424 | 418 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 2x8x8 | rank 100 | rank 100 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:35Z |
| Lille per-format page | 2x8x8 | rank 100; no complexity variant or operation count cited | 418 | https://fmm.univ-lille.fr/2x8x8.html | 2026-10-15T22:25:35Z |
| matmulcatalog COVERAGE.md, adds column | 2x8x8 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 418 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:35Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 2x8x8 rank 100 | format absent at this rank | 418 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 418 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:35Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 100, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-100 ternary scheme and its 424-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 100**, cited by the Lille catalogue (https://fmm.univ-lille.fr/2x8x8.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
