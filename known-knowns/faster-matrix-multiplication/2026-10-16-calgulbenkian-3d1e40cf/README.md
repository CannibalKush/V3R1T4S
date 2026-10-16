# Fewer additions for <2,5,6> at rank 47: 179 against 181

## What

claim/object/2x5x6_m47_cr179_ZT_reduced.json (sha256 3d1e40cf65f343ad2edfe3735c1d4eccd1fd4aeaca82b31980779e38a059dcc1) is a ternary straight-line program that I verified exactly over Z (full 2x5x6 tensor identity, all expanded coefficients in {-1,0,1}) to compute a rank-47 scheme with the same 47 products as Perminov's 2x5x6 cr181 file and 179 additions under his reduced convention (U 38, V 65, W 76; V and W programs identical to his, U program 2 additions shorter), below his only 2x5x6 file (181), with no Lille operation count to compare against and COVERAGE.md giving only the naive 332.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/2x5x6_m47_cr179_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 2x5x6 rank 47 | 181 (minimum over his files for this format and rank; one file) | 179 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:43Z |
| Perminov, arXiv:2512.13365, Table 1 | 2x5x6 rank 47 | 181 | 179 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 2x5x6 | rank 47 | rank 47 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:43Z |
| Lille per-format page | 2x5x6 | rank 47; no complexity variant or operation count cited | 179 | https://fmm.univ-lille.fr/2x5x6.html | 2026-10-15T22:25:43Z |
| matmulcatalog COVERAGE.md, adds column | 2x5x6 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 179 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:43Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 2x5x6 rank 47 | rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 256-47       332         189        184        0.43, 0.01, 0          - / 256-47         332       188       184     148   44.6     0.31, 0.01, 0 | 179 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 179 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:43Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 47, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-47 ternary scheme and its 181-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 47**, cited by the Lille catalogue (https://fmm.univ-lille.fr/2x5x6.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
