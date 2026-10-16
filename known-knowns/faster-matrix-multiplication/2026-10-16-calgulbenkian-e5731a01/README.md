# Fewer additions for <3,4,5> at rank 47: 156 against 161

## What

The program claim/object/3x4x5_m47_cr156_ZT_reduced.json (sha256 e5731a01ecf58de14b5fc4a6e9a0de880b11146aeeeef4df6844dd83bfbb83a8) is a ternary straight-line program (all expanded forms in {-1,0,1}) computing the exact 3x4 by 4x5 integer matrix product with the same 47 products as Perminov's 3x4x5_m47_cr161 file (rank 47 equals the fmm_sota.json best), using 156 additions under his reduced convention (U 38, V 44, W 74, W program unchanged from his), against his live-directory minimum of 161 and no lower count on the Lille 3x4x5 page or in COVERAGE.md (naive +287), as fetched on 2026-10-15.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/3x4x5_m47_cr156_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 3x4x5 rank 47 | 161 (minimum over his files for this format and rank; one file) | 156 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:38Z |
| Perminov, arXiv:2512.13365, Table 1 | 3x4x5 rank 47 | 161 | 156 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 3x4x5 | rank 47 | rank 47 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:38Z |
| Lille per-format page | 3x4x5 | rank 47; no complexity variant or operation count cited | 156 | https://fmm.univ-lille.fr/3x4x5.html | 2026-10-15T22:25:38Z |
| matmulcatalog COVERAGE.md, adds column | 3x4x5 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 156 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:38Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 3x4x5 rank 47 | rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 345-47         714       284         276      438    61.3         0, 0.11, 0.08 / 345-47      668           254       242      426     63.8       0, 0.005, 0.07 / 345-47          287      171       161     126   43.9   0.23, 0.01, 0.01 / 345-47          288    176         165     123   42.7   0.21, 0.01, 0.08 | 156 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 156 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:38Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 47, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-47 ternary scheme and its 161-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 47**, cited by the Lille catalogue (https://fmm.univ-lille.fr/3x4x5.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
