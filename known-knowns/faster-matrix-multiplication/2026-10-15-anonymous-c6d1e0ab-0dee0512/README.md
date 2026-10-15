# Fast matrix multiplication: format (15, 16, 16) in rank 2176 over Q

## What

claim/object/15x16x16_r2176_Q.json (sha256 0dee0512255d74595673fd8bfa0df20b0ab0a87785b2d11cbb2a94f6dbd5d57c) is an exact bilinear scheme over Q for the 15x16x16 matrix multiplication format with 2176 rank-one terms, all nonzero, satisfying all 14,745,600 Brent equations in exact integer arithmetic, and 2176 is strictly below 2223, the minimum rank for 15x16x16 in the four live sources fetched 2026-10-15 (fmm_sota.json 2223, Lille page 2262, Perminov README ZT 2302 / Z 2302 / Q 2223, MerlijnW70 tree no entry), and below the V3R1T4S trophy case entry of 2180.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/15x16x16_r2176_Q.json`.

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
| Sedoglavic `fmm_sota.json` | [15, 16, 16] | 2223 | **2176** | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:08:07Z |
| Lille per-format catalogue | 15x16x16 | 2262 | **2176** | https://fmm.univ-lille.fr/15x16x16.html | 2026-10-15T09:08:07Z |
| Perminov `README.md` (ZT / Z / Q) | 15x16x16 | 2302 / 2223 / 2262 | **2176** | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:08:07Z |
| MerlijnW70/fmm-schemes | 15x16x16 | none | **2176** | https://github.com/MerlijnW70/fmm-schemes | 2026-10-15T09:08:07Z |
| V3R1T4S `TROPHY_CASE.md` | 15x16x16 | 2180 (the repository's own project) | **2176** | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T09:08:07Z |

The panel's novelty skeptic re-fetched every source independently (first fetch 2026-10-15T09:20:52Z); its report is `panel/novelty.md`. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- The scheme is over the rationals. Nothing is claimed for the integer, ternary or GF(2) ranks of this format.
- The margin is 4 multiplications below the lowest listed value (2180). Records in this range move often; the comparison holds for the table versions recorded here.
- This is a rank bound for one format and does not improve the asymptotic exponent of matrix multiplication.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Khoruzhii, Serafin, Gelß and Pokutta**, *Local Improvements to Trilinear Aggregation* (LITA, https://github.com/khoruzhii/lita): this scheme is derived from LITA's published 17x17x17 scheme (rank 2723), cut to 16x17x17, 15x17x17, 15x16x17 and then 15x16x16, their published scheme, by restriction and exact absorption. Please credit them when using it.
- **A. I. Perminov**, *FastMatrixMultiplication* (https://github.com/dronperminov/FastMatrixMultiplication): the status table and the scheme file format this object uses.
- **A. Sedoglavic**, *Catalogue of fast matrix multiplication algorithms* (https://fmm.univ-lille.fr/ and https://github.com/sedoglavic/fmm_digest).
- **MerlijnW70**, *fmm-schemes* (https://github.com/MerlijnW70/fmm-schemes).
- **M. Kauers and I. Wood**, *Exploring the Meta Flip Graph for Matrix Multiplication*, arXiv:2510.19787: projection edges between formats, of which this slice is a non-coordinate version.
- **M. Kauers and J. Moosbauer**, *Flip Graphs for Matrix Multiplication*, arXiv:2212.01175: rank-lowering reductions, which the absorption step generalizes.
- Contributor credit: `anonymous-c6d1e0ab`.
