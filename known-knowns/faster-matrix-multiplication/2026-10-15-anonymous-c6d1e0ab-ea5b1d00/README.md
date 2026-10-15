# Fewer additions for <5,6,6> at rank 130: 502 against 562

## What

claim/object/5x6x6_m130_cr502_ZT_reduced.json (sha256 ea5b1d00e3702536a57a8598f0f09040f99b503e844d5018556128ac81d0a097) is a ternary straight-line program for 5x6 times 6x6 with the same 130 products as Perminov's cr562 file, verified exactly over Z with 502 additions under the reduced convention, below the sole live addition_reduced_ZT count of 562 and the COVERAGE.md naive count of 1716, with no operation count cited on the Lille 5x6x6 page.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/5x6x6_m130_cr502_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 5x6x6 rank 130 | 562 (minimum over his files for this format and rank; one file) | 502 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T12:10:59Z |
| Perminov, arXiv:2512.13365, Table 1 | 5x6x6 rank 130 | 562 | 502 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 5x6x6 | rank 130 | rank 130 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T12:10:59Z |
| Lille per-format page | 5x6x6 | rank 130; no complexity variant or operation count cited | 502 | https://fmm.univ-lille.fr/5x6x6.html | 2026-10-15T12:10:59Z |
| matmulcatalog COVERAGE.md, adds column | 5x6x6 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 502 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T12:10:59Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 5x6x6 rank 130 | 603 over Z (Table 3.4, comparable, above the reference) | 502 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 502 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T12:10:59Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 130, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-130 ternary scheme and its 562-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 130**, cited by the Lille catalogue (https://fmm.univ-lille.fr/5x6x6.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `anonymous-c6d1e0ab`.
