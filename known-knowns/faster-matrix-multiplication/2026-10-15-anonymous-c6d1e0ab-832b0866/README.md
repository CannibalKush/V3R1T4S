# Fewer additions for <5,6,7> at rank 150: 582 against 664

## What

The file claim/object/5x6x7_m150_cr582_ZT_reduced.json (sha256 832b08667df7d72d5c12f78f7073168f43dd50e323aaaf547290f0533d2585f3) is a ternary straight-line program for the rank-150 scheme of <5,6,7> (same 150 products as Perminov's cr664 file) that exactly computes A*B over Z with 582 additions under Perminov's reduced convention (U 147, V 171, W 264), against 664 for the only live addition_reduced_ZT file at that rank, with no lower count cited on the Lille page or in COVERAGE.md.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/5x6x7_m150_cr582_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 5x6x7 rank 150 | 664 (minimum over his files for this format and rank; one file) | 582 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T11:28:40Z |
| Perminov, arXiv:2512.13365, Table 1 | 5x6x7 rank 150 | 664 | 582 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 5x6x7 | rank 150 | rank 150 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T11:28:40Z |
| Lille per-format page | 5x6x7 | rank 150; no complexity variant or operation count cited | 582 | https://fmm.univ-lille.fr/5x6x7.html | 2026-10-15T11:28:40Z |
| matmulcatalog COVERAGE.md, adds column | 5x6x7 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 582 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T11:28:40Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 5x6x7 rank 150 | 684 to 688 over Z (Table 3.4, comparable, above the reference) | 582 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | PR #159 (DrZuzzjen, open draft, 2026-10-15): 652 under the same convention | 582 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T11:28:40Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 150, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- The open pull request on this cell (PR #159 (DrZuzzjen, open draft, 2026-10-15)) is not ours; its 652 is above 582 and is listed in the table above.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-150 ternary scheme and its 664-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **Kauers and Wood, arXiv:2505.05896 (rank 150)**, cited by the Lille catalogue (https://fmm.univ-lille.fr/5x6x7.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search. Pull request #159 (<5,6,7> at 652) by the same author is compared against above.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `anonymous-c6d1e0ab`.
