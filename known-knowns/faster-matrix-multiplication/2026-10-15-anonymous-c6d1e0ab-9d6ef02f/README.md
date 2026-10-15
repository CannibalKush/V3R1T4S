# Fast matrix multiplication: format (14, 16, 16) in rank 2117 over Q

## What

The file claim/object/14x16x16_r2117_Q.json (sha256 9d6ef02f8162d9d5a53e56ecff6821459727c32d5a5fecb24283bd0c716fdf10) is an exact bilinear scheme over Q for the 14x16x16 matrix multiplication format with 2117 rank-one terms, each with all three factors nonzero, verified by my own exact integer check of all 12,845,056 Brent equations, and 2117 is strictly below 2128, the minimum rank for the sorted format 14x16x16 in fmm_sota.json, the Lille 14x16x16 page, Perminov's README ZT/Z/Q columns and MerlijnW70's fmm-schemes tree as I fetched them on 2026-10-15.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/14x16x16_r2117_Q.json`.

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
| Sedoglavic `fmm_sota.json` | [14, 16, 16] | 2128 | **2117** | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:08:01Z |
| Lille per-format catalogue | 14x16x16 | 2128 | **2117** | https://fmm.univ-lille.fr/14x16x16.html | 2026-10-15T09:08:01Z |
| Perminov `README.md` (ZT / Z / Q) | 14x16x16 | 2170 / 2128 / 2142 | **2117** | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:08:01Z |
| MerlijnW70/fmm-schemes | 14x16x16 | none | **2117** | https://github.com/MerlijnW70/fmm-schemes | 2026-10-15T09:08:01Z |
| V3R1T4S `TROPHY_CASE.md` and open pull requests | 14x16x16 | none | **2117** | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T09:08:01Z |

The panel's novelty skeptic re-fetched every source independently (first fetch 2026-10-15T09:20:51Z); its report is `panel/novelty.md`. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- The scheme is over the rationals. Nothing is claimed for the integer, ternary or GF(2) ranks of this format.
- The margin is 11 multiplications below the lowest listed value (2128). Records in this range move often; the comparison holds for the table versions recorded here.
- This is a rank bound for one format and does not improve the asymptotic exponent of matrix multiplication.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Khoruzhii, Serafin, Gelß and Pokutta**, *Local Improvements to Trilinear Aggregation* (LITA, https://github.com/khoruzhii/lita): this scheme is derived from the V3R1T4S repository's own published 15x16x16 rank-2180 scheme (itself a restriction of LITA's square schemes), cut once along its 15-axis, their published scheme, by restriction and exact absorption. Please credit them when using it.
- **A. I. Perminov**, *FastMatrixMultiplication* (https://github.com/dronperminov/FastMatrixMultiplication): the status table and the scheme file format this object uses.
- **A. Sedoglavic**, *Catalogue of fast matrix multiplication algorithms* (https://fmm.univ-lille.fr/ and https://github.com/sedoglavic/fmm_digest).
- **MerlijnW70**, *fmm-schemes* (https://github.com/MerlijnW70/fmm-schemes).
- **M. Kauers and I. Wood**, *Exploring the Meta Flip Graph for Matrix Multiplication*, arXiv:2510.19787: projection edges between formats, of which this slice is a non-coordinate version.
- **M. Kauers and J. Moosbauer**, *Flip Graphs for Matrix Multiplication*, arXiv:2212.01175: rank-lowering reductions, which the absorption step generalizes.
- Contributor credit: `anonymous-c6d1e0ab`.
