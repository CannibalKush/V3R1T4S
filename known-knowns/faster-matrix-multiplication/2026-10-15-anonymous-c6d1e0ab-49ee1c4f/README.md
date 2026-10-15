# Fast matrix multiplication: format (13, 14, 15) in rank 1645 over Q

## What

The file claim/object/13x14x15_r1645_Q.json (sha256 49ee1c4f6642d1245e5af697eeb2f342024d04f06a0cc9113501ce8f45177144) is an exact bilinear scheme over Q for the matrix multiplication format 13x14x15 with 1645 rank-one terms (all three factors nonzero, no duplicates), verified by an independent exact-integer check of all 7,452,900 Brent equations, and 1645 is strictly below 1681, the minimum rank for the sorted format 13x14x15 in fmm_sota.json (createdAt 2026-10-09T11:45:48), the Lille per-format page, Perminov's ZT/Z/Q columns and MerlijnW70's fmm-schemes tree as fetched live on 2026-10-15T09:13Z, and below the V3R1T4S TROPHY_CASE.md entry 1677 for this format; rank over Q only.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/13x14x15_r1645_Q.json`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: under two minutes.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed rank | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Sedoglavic `fmm_sota.json` | [13, 14, 15] | 1681 | **1645** | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:07:48Z |
| Lille per-format catalogue | 13x14x15 | 1681 | **1645** | https://fmm.univ-lille.fr/13x14x15.html | 2026-10-15T09:07:48Z |
| Perminov `README.md` (ZT / Z / Q) | 13x14x15 | 1681 / 1714 / 1681 | **1645** | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:07:48Z |
| MerlijnW70/fmm-schemes | 13x14x15 | none | **1645** | https://github.com/MerlijnW70/fmm-schemes | 2026-10-15T09:07:48Z |
| V3R1T4S `TROPHY_CASE.md` | 13x14x15 | 1677 (the repository's own project) | **1645** | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T09:07:48Z |

The panel's novelty skeptic re-fetched every source independently (first fetch 2026-10-15T09:12:49Z); its report is `panel/novelty.md`. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- The scheme is over the rationals. Nothing is claimed for the integer, ternary or GF(2) ranks of this format.
- The margin is 32 multiplications below the lowest listed value (1677). Records in this range move often; the comparison holds for the table versions recorded here.
- This is a rank bound for one format and does not improve the asymptotic exponent of matrix multiplication.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Khoruzhii, Serafin, Gelß and Pokutta**, *Local Improvements to Trilinear Aggregation* (LITA, https://github.com/khoruzhii/lita): this scheme is derived from LITA's published 15x15x15 scheme (rank 1977), cut to 14x15x15, 13x15x15 and then 13x14x15, their published scheme, by restriction and exact absorption. Please credit them when using it.
- **A. I. Perminov**, *FastMatrixMultiplication* (https://github.com/dronperminov/FastMatrixMultiplication): the status table and the scheme file format this object uses.
- **A. Sedoglavic**, *Catalogue of fast matrix multiplication algorithms* (https://fmm.univ-lille.fr/ and https://github.com/sedoglavic/fmm_digest).
- **MerlijnW70**, *fmm-schemes* (https://github.com/MerlijnW70/fmm-schemes).
- **M. Kauers and I. Wood**, *Exploring the Meta Flip Graph for Matrix Multiplication*, arXiv:2510.19787: projection edges between formats, of which this slice is a non-coordinate version.
- **M. Kauers and J. Moosbauer**, *Flip Graphs for Matrix Multiplication*, arXiv:2212.01175: rank-lowering reductions, which the absorption step generalizes.
- Contributor credit: `anonymous-c6d1e0ab`.
