# Fewer additions for <5,6,8> at rank 170: 667 against 720

## What

The file claim/object/5x6x8_m170_cr667_ZT_reduced.json (sha256 efb7f10c7e3a5dcd2481aacbd72ae5e308550dd825927d1c1114574354447c80) is a ternary straight-line program that exactly computes the full 5x6 times 6x8 product over Z at rank 170 (Brent identity verified, every expanded coefficient in {-1,0,1}) using 667 reduced additions (U 159, V 196, W 312), strictly below the 720 of the only addition_reduced_ZT file for 5x6x8 rank 170, on the same products as that file, and no source checked (the live Lille page, COVERAGE.md) gives a comparable lower count.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/5x6x8_m170_cr667_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 5x6x8 rank 170 | 720 (minimum over his files for this format and rank; one file) | 667 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:12Z |
| Perminov, arXiv:2512.13365, Table 1 | 5x6x8 rank 170 | 720 | 667 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 5x6x8 | rank 170 | rank 170 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:12Z |
| Lille per-format page | 5x6x8 | rank 170; no complexity variant or operation count cited | 667 | https://fmm.univ-lille.fr/5x6x8.html | 2026-10-15T22:25:12Z |
| matmulcatalog COVERAGE.md, adds column | 5x6x8 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 667 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:12Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 5x6x8 rank 170 | format absent at this rank | 667 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 667 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:12Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 170, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-170 ternary scheme and its 720-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 170**, cited by the Lille catalogue (https://fmm.univ-lille.fr/5x6x8.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
