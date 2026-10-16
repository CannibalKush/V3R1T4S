# Fewer additions for <5,5,7> at rank 127: 483 against 531

## What

claim/object/5x5x7_m127_cr483_ZT_reduced.json (sha256 1e59f08cf1870f4ade6b3ab5efc2d004e5bb1a0edb455b7e250ed4a7cfc6a65a) is a ternary straight-line program that exactly computes the 5x5 by 5x7 product with rank 127, equal to the fmm_sota.json best rank, using 483 additions under the reduced convention (U 116, V 137, W 230) against 531 for Perminov's only live addition_reduced_ZT file at this format and rank, over the same 127 products, with no lower reduced count on the Lille page or COVERAGE.md.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/5x5x7_m127_cr483_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 5x5x7 rank 127 | 531 (minimum over his files for this format and rank; one file) | 483 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:15Z |
| Perminov, arXiv:2512.13365, Table 1 | 5x5x7 rank 127 | 531 | 483 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 5x5x7 | rank 127 | rank 127 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:15Z |
| Lille per-format page | 5x5x7 | rank 127; no complexity variant or operation count cited | 483 | https://fmm.univ-lille.fr/5x5x7.html | 2026-10-15T22:25:15Z |
| matmulcatalog COVERAGE.md, adds column | 5x5x7 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 483 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:15Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 5x5x7 rank 127 | rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 557-127     1,518     577            566      952    62.7       0.0 , 0.1 , 0.08 / 557-127   1,518     584             560       958    63.1        0, 0.18, 0.06 / 557-127   1,554     584             568       986    63.4      0.02, 0.08, 0.06 / 557-127   1,590     570             563      1027    64.6      0.02, 0.16, 0.06 | 483 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 483 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:15Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 127, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-127 ternary scheme and its 531-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 127**, cited by the Lille catalogue (https://fmm.univ-lille.fr/5x5x7.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
