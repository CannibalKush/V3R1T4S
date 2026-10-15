# Fewer additions for <6,6,6> at rank 153: 588 against 655

## What

claim/object/6x6x6_m153_cr588_ZT_reduced.json (sha256 4abbbac3ec7576e4a03ff6ab7110dd4c99e8c564724a8c2eba3b26c4e2231a47) is an exact ternary straight-line program for the rank-153 6x6x6 scheme with Perminov's own 153 products, using 588 additions under the reduced convention versus 655 in his only live 6x6x6 addition_reduced_ZT file, as checked on 2026-10-15.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/6x6x6_m153_cr588_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 6x6x6 rank 153 | 655 (minimum over his files for this format and rank; one file) | 588 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T12:10:58Z |
| Perminov, arXiv:2512.13365, Table 1 | 6x6x6 rank 153 | 655 | 588 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 6x6x6 | rank 153 | rank 153 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T12:10:58Z |
| Lille per-format page | 6x6x6 | rank 153; no complexity variant or operation count cited | 588 | https://fmm.univ-lille.fr/6x6x6.html | 2026-10-15T12:10:58Z |
| matmulcatalog COVERAGE.md, adds column | 6x6x6 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 588 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T12:10:58Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 6x6x6 rank 153 | no count over Z at rank 153; 679 over Z2 (Table 3.5, not comparable); 871 over Z at rank 164 (another scheme) | 588 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 588 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T12:10:58Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 153, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-153 ternary scheme and its 655-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 153**, cited by the Lille catalogue (https://fmm.univ-lille.fr/6x6x6.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `anonymous-c6d1e0ab`.
