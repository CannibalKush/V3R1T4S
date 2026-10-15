# Fewer additions for <4,6,8> at rank 140: 476 against 551

## What

claim/object/4x6x8_m140_cr476_ZT_reduced.json (sha256 45256d75a05660145a239129ba59524edf864bbda68bcf5297be8fdf7c38158e) is a ternary straight-line program that exactly computes the full 4x6 by 6x8 product over Z with 140 products (the best listed rank) using 476 reduced additions (U 108, V 136, W 232), strictly below the single live Perminov addition_reduced_ZT value of 551 for this format and rank, with no count published for it on the live Lille page or in the live COVERAGE.md adds column.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/4x6x8_m140_cr476_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 4x6x8 rank 140 | 551 (minimum over his files for this format and rank; one file) | 476 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T12:10:57Z |
| Perminov, arXiv:2512.13365, Table 1 | 4x6x8 rank 140 | 551 | 476 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 4x6x8 | rank 140 | rank 140 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T12:10:57Z |
| Lille per-format page | 4x6x8 | rank 140; no complexity variant or operation count cited | 476 | https://fmm.univ-lille.fr/4x6x8.html | 2026-10-15T12:10:57Z |
| matmulcatalog COVERAGE.md, adds column | 4x6x8 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 476 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T12:10:57Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 4x6x8 rank 140 | format absent | 476 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 476 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T12:10:57Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 140, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- The scheme is not claimed as new: the Lille catalogue lists the rank-140 4x6x8 algorithm as the Kronecker product of 2x2x2:7 and 2x3x4:20. Under the naive count (nonzeros of U, V, W) this scheme is worse than Perminov's file; the claim is the reduced count only.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-140 ternary scheme files whose Kronecker product is used here, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 140**, cited by the Lille catalogue (https://fmm.univ-lille.fr/4x6x8.html) for the rank.
- **V. Strassen** (1969) and **S. Winograd** (1971): the 2x2x2 rank-7 algorithm and its 15-addition variant, one factor of the scheme. **A. Sedoglavic**, the Lille catalogue, which lists this rank as the Kronecker product used here.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `anonymous-c6d1e0ab`.
