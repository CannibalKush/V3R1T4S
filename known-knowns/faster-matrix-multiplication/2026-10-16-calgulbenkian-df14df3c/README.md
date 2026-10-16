# Fewer additions for <4,4,5> at rank 61: 222 against 233

## What

The program claim/object/4x4x5_m61_cr222_ZT_reduced.json (sha256 df14df3c1a01189e540ab5a0eedebc331cd08e12714d795df0884481da292366) is a ternary straight-line program that, with its 61 products identical to those of Perminov's 4x4x5_m61_cr233 scheme (rank 61, the best rank in fmm_sota.json), computes the 4x4 by 4x5 product exactly over Z (full tensor identity and random integer evaluation, all expanded forms in {-1,0,1}) using 222 additions under Perminov's reduced convention (U 59, V 61, W 102), below his single live reduced file's 233 and below any count on the Lille 4x4x5 page (none cited) or in COVERAGE.md (+455 naive); it does not lower the rank and I judged no novelty beyond these sources.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/4x4x5_m61_cr222_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 4x4x5 rank 61 | 233 (minimum over his files for this format and rank; one file) | 222 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:30Z |
| Perminov, arXiv:2512.13365, Table 1 | 4x4x5 rank 61 | 233 | 222 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 4x4x5 | rank 61 | rank 61 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:30Z |
| Lille per-format page | 4x4x5 | rank 61; no complexity variant or operation count cited | 222 | https://fmm.univ-lille.fr/4x4x5.html | 2026-10-15T22:25:30Z |
| matmulcatalog COVERAGE.md, adds column | 4x4x5 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 222 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:30Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 4x4x5 rank 61 | rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 445-61       455         248        238        0, 0.01, 0.12          - / 445-61         455       248       238     217   47.7      0, 0.01, 0.1 | 222 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 222 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:30Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 61, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-61 ternary scheme and its 233-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 61**, cited by the Lille catalogue (https://fmm.univ-lille.fr/4x4x5.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
