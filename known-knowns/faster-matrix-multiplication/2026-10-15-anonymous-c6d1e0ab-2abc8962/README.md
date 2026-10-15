# Fewer additions for <5,7,7> at rank 176: 699 against 788

## What

The program in claim/object/5x7x7_m176_cr699_ZT_reduced.json (sha256 2abc89623e051336de20440c1e68300d56656b98733b8df7e66808bbd60174be) is an exact ternary straight-line program for the same 176 products as Perminov's cr788 5x7x7 file, verified over Z by my own Brent and random-matrix checks, and costs 699 reduced additions (U 179, V 206, W 314) against his sole 5x7x7 addition_reduced_ZT file at 788, with the Lille page citing no operation count and matmulcatalog's naive +2745 not on the reduced convention, as of my fetches.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/5x7x7_m176_cr699_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 5x7x7 rank 176 | 788 (minimum over his files for this format and rank; one file) | 699 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T11:28:40Z |
| Perminov, arXiv:2512.13365, Table 1 | 5x7x7 rank 176 | 788 | 699 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 5x7x7 | rank 176 | rank 176 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T11:28:40Z |
| Lille per-format page | 5x7x7 | rank 176; no complexity variant or operation count cited | 699 | https://fmm.univ-lille.fr/5x7x7.html | 2026-10-15T11:28:40Z |
| matmulcatalog COVERAGE.md, adds column | 5x7x7 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 699 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T11:28:40Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 5x7x7 rank 176 | no count over Z; 817 to 826 over Z2 (Table 3.5, not comparable) | 699 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 699 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T11:28:40Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 176, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-176 ternary scheme and its 788-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **Kauers and Wood, arXiv:2505.05896 (rank 176)**, cited by the Lille catalogue (https://fmm.univ-lille.fr/5x7x7.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `anonymous-c6d1e0ab`.
