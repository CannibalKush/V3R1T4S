# Fewer additions for <4,4,6> at rank 73: 256 against 280

## What

For format 4x4x6 at rank 73 (the live best rank in fmm_sota.json), claim/object/4x4x6_m73_cr256_ZT_reduced.json (sha256 feea5fbcfd07fd3416d280a9a3d8af5e49c916171b9771d614e51e7a43f98b85) is a ternary straight-line program that exactly computes A*B over Z (Brent identity and random-integer evaluation verified, all expanded coefficients in {-1,0,1}) with 256 reduced additions, strictly below the live minimum of 280 in Perminov's addition_reduced_ZT for the same 73 products, with no lower count cited on the live Lille 4x4x6 page and only a non-comparable naive count in COVERAGE.md.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/4x4x6_m73_cr256_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 4x4x6 rank 73 | 280 (minimum over his files for this format and rank; one file) | 256 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:27Z |
| Perminov, arXiv:2512.13365, Table 1 | 4x4x6 rank 73 | 280 | 256 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 4x4x6 | rank 73 | rank 73 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:27Z |
| Lille per-format page | 4x4x6 | rank 73; no complexity variant or operation count cited | 256 | https://fmm.univ-lille.fr/4x4x6.html | 2026-10-15T22:25:27Z |
| matmulcatalog COVERAGE.md, adds column | 4x4x6 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 256 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:27Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 4x4x6 rank 73 | format absent at this rank | 256 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 256 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:27Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 73, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-73 ternary scheme and its 280-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 73**, cited by the Lille catalogue (https://fmm.univ-lille.fr/4x4x6.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
