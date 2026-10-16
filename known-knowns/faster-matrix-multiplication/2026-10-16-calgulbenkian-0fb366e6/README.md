# Fewer additions for <5,8,8> at rank 230: 929 against 974

## What

claim/object/5x8x8_m230_cr929_ZT_reduced.json (sha256 0fb366e6a2a5cc6bc6fd0b31334b1d859df86c180c0fc30759cbbd41c4867501) is a ternary straight-line program that exactly computes the <5,8,8> product over Z with the same 230 products as Perminov's cr974 scheme and 929 additions under the reduced convention (U 205, V 327, W 397), strictly below the 974 in his only addition_reduced_ZT file for this format and rank, with the Lille 5x8x8 page citing no operation count and COVERAGE.md listing only the naive +2638.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/5x8x8_m230_cr929_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 5x8x8 rank 230 | 974 (minimum over his files for this format and rank; one file) | 929 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:18Z |
| Perminov, arXiv:2512.13365, Table 1 | 5x8x8 rank 230 | 974 | 929 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 5x8x8 | rank 230 | rank 230 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:18Z |
| Lille per-format page | 5x8x8 | rank 230; no complexity variant or operation count cited | 929 | https://fmm.univ-lille.fr/5x8x8.html | 2026-10-15T22:25:18Z |
| matmulcatalog COVERAGE.md, adds column | 5x8x8 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 929 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:18Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 5x8x8 rank 230 | format absent at this rank | 929 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 929 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:18Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 230, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-230 ternary scheme and its 974-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 230**, cited by the Lille catalogue (https://fmm.univ-lille.fr/5x8x8.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
