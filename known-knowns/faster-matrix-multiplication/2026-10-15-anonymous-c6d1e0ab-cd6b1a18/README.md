# Fewer additions for <5,5,8> at rank 144: 556 against 620

## What

claim/object/5x5x8_m144_cr556_ZT_reduced.json (sha256 cd6b1a181d857f3e993cc6c15338a7f709bd1119c2745a399cfc02eae9b52f03) is a ternary straight-line program for the Perminov rank-144 scheme of the 5x5x8 format that computes A*B exactly over Z with 556 additions under the reduced convention, versus 620 for the only 5x5x8 file in Perminov's live addition_reduced_ZT, with no operation count for this rank on the Lille page and only a different naive count in COVERAGE.md; it shows no rank improvement and no evidence for any other format.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/5x5x8_m144_cr556_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 5x5x8 rank 144 | 620 (minimum over his files for this format and rank; one file) | 556 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T12:10:58Z |
| Perminov, arXiv:2512.13365, Table 1 | 5x5x8 rank 144 | 620 | 556 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 5x5x8 | rank 144 | rank 144 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T12:10:58Z |
| Lille per-format page | 5x5x8 | rank 144; no complexity variant or operation count cited | 556 | https://fmm.univ-lille.fr/5x5x8.html | 2026-10-15T12:10:58Z |
| matmulcatalog COVERAGE.md, adds column | 5x5x8 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 556 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T12:10:58Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 5x5x8 rank 144 | format absent | 556 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 556 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T12:10:58Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 144, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-144 ternary scheme and its 620-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 144**, cited by the Lille catalogue (https://fmm.univ-lille.fr/5x5x8.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `anonymous-c6d1e0ab`.
