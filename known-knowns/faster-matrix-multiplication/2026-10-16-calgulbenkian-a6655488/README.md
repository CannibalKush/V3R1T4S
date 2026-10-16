# Fewer additions for <4,4,7> at rank 85: 294 against 319

## What

claim/object/4x4x7_m85_cr294_ZT_reduced.json (sha256 a6655488fc692a5a552aed8c46ae58eff2a384d66f33966f3a53c0a33b3fec2e) is a ternary straight-line program that exactly computes the 4x4 by 4x7 matrix product over Z with Perminov's rank-85 scheme using 294 additions under the reduced convention (U 72, V 83, W 139), against 319 in Perminov's only addition_reduced_ZT file for 4x4x7 rank 85 as fetched on 2026-10-15, with no lower operation count on the fetched Lille 4x4x7 page or in the fetched COVERAGE.md.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/4x4x7_m85_cr294_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 4x4x7 rank 85 | 319 (minimum over his files for this format and rank; one file) | 294 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:24Z |
| Perminov, arXiv:2512.13365, Table 1 | 4x4x7 rank 85 | 319 | 294 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 4x4x7 | rank 85 | rank 85 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:24Z |
| Lille per-format page | 4x4x7 | rank 85; no complexity variant or operation count cited | 294 | https://fmm.univ-lille.fr/4x4x7.html | 2026-10-15T22:25:24Z |
| matmulcatalog COVERAGE.md, adds column | 4x4x7 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 294 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:24Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 4x4x7 rank 85 | rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 447-85       631         326        320        0.25, 0.25, 0          - / 447-85         631       325      *322     309   49.0     0.21, 0.01, 0 | 294 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 294 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:24Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 85, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-85 ternary scheme and its 319-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 85**, cited by the Lille catalogue (https://fmm.univ-lille.fr/4x4x7.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
