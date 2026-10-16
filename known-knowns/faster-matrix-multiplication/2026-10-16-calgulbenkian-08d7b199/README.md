# Fewer additions for <4,5,5> at rank 76: 281 against 299

## What

claim/object/4x5x5_m76_cr281_ZT_reduced.json (sha256 08d7b199e9ecc9f7254dc46c23ecf2128e83444277b19eac6bbcb678a107f819) is a ternary straight-line program that, by my own exact checker, computes the full 4x5 by 5x5 product over Z with Perminov's 76 products (expanded U, V, W rows identical to his) using 281 additions under the reduced convention (U 75, V 84, W 122), against 299 in the only 4x5x5 file of his live addition_reduced_ZT directory, with no cited count on the Lille 4x5x5 page and COVERAGE.md giving only a naive +549.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/4x5x5_m76_cr281_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 4x5x5 rank 76 | 299 (minimum over his files for this format and rank; one file) | 281 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:29Z |
| Perminov, arXiv:2512.13365, Table 1 | 4x5x5 rank 76 | 299 | 281 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 4x5x5 | rank 76 | rank 76 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:29Z |
| Lille per-format page | 4x5x5 | rank 76; no complexity variant or operation count cited | 281 | https://fmm.univ-lille.fr/4x5x5.html | 2026-10-15T22:25:29Z |
| matmulcatalog COVERAGE.md, adds column | 4x5x5 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 281 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:29Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 4x5x5 rank 76 | rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 455-76       549         322        310      0.26, 0.01, 0.11       437 / 455-76        1,107      469         451      656    59.2       0.17, 0.1, 0.104 / 455-76     1,015          388       372      643     63.3     0.145, 0.11, 0.005 / 455-76          549      325       310     239   43.5    0.19, 0.1, 0.1 | 281 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 281 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:29Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 76, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-76 ternary scheme and its 299-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 76**, cited by the Lille catalogue (https://fmm.univ-lille.fr/4x5x5.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
