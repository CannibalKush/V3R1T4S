# Fewer additions for <4,6,7> at rank 123: 469 against 517

## What

claim/object/4x6x7_m123_cr469_ZT_reduced.json (sha256 ade76c2eef28cca082e6f87f2ca0294f6a6e5bcdce1e1cb9356fe068bab0dd65) is a ternary straight-line program that, by my exact integer expansion, computes the 4x6x7 product with 123 products (the same products as Perminov's cr517 file, equal to the fmm_sota.json rank) using 469 reduced additions (U 114, V 140, W 215), below the sole live addition_reduced_ZT count of 517, with no Lille operation count and only a naive 1586 count in COVERAGE.md to beat.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/4x6x7_m123_cr469_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 4x6x7 rank 123 | 517 (minimum over his files for this format and rank; one file) | 469 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T11:28:43Z |
| Perminov, arXiv:2512.13365, Table 1 | 4x6x7 rank 123 | 517 | 469 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 4x6x7 | rank 123 | rank 123 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T11:28:43Z |
| Lille per-format page | 4x6x7 | rank 123; no complexity variant or operation count cited | 469 | https://fmm.univ-lille.fr/4x6x7.html | 2026-10-15T11:28:43Z |
| matmulcatalog COVERAGE.md, adds column | 4x6x7 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 469 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T11:28:43Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 4x6x7 rank 123 | no count over Z; 575 over Z2 (Table 3.5, not comparable) | 469 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | PR #149 (DrZuzzjen, open draft): 503 under the same convention; closed PR #10: 505 | 469 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T11:28:43Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 123, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- The open pull request on this cell (PR #149 (DrZuzzjen, open draft)) is not ours; its 503 is above 469 and is listed in the table above.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-123 ternary scheme and its 517-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **Kauers and Wood, arXiv:2505.05896 (rank 123)**, cited by the Lille catalogue (https://fmm.univ-lille.fr/4x6x7.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `anonymous-c6d1e0ab`.
