# Fast matrix multiplication: format (13, 13, 15) in rank 1578 over Q

## What

The file claim/object/13x13x15_r1578_Q.json (sha256 9a8f254ed5b7e15b8f4157da632c5adc686e46c4f020659b924114c8b7c5a618) is an exact bilinear matrix multiplication scheme over Q for the format 13x13x15 with exactly 1578 rank-one terms, each with all three factors nonzero, verified by my own exact big-integer and multi-prime Brent-equation checks, and 1578 is strictly below the rank for the sorted format 13x13x15 in each of the four named sources as fetched live on 2026-10-15 (fmm_sota.json 1605, Lille page 1605, Perminov README ZT/Z/Q 1591/1591/1591, MerlijnW70 file 13x13x15_m1591_ZT.json), whose minimum is 1591.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/13x13x15_r1578_Q.json`.

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
| Sedoglavic `fmm_sota.json` | [13, 13, 15] | 1605 | **1578** | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:07:54Z |
| Lille per-format catalogue | 13x13x15 | 1605 | **1578** | https://fmm.univ-lille.fr/13x13x15.html | 2026-10-15T09:07:54Z |
| Perminov `README.md` (ZT / Z / Q) | 13x13x15 | 1591 / 1591 / 1739 | **1578** | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:07:54Z |
| MerlijnW70/fmm-schemes | 13x13x15 | see record | **1578** | https://github.com/MerlijnW70/fmm-schemes | 2026-10-15T09:07:54Z |
| V3R1T4S `TROPHY_CASE.md` and open pull requests | 13x13x15 | none | **1578** | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T09:07:54Z |

The panel's novelty skeptic re-fetched every source independently (first fetch 2026-10-15T09:20:50Z); its report is `panel/novelty.md`. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- The scheme is over the rationals. Nothing is claimed for the integer, ternary or GF(2) ranks of this format.
- The margin is 13 multiplications below the lowest listed value (1591). Records in this range move often; the comparison holds for the table versions recorded here.
- This is a rank bound for one format and does not improve the asymptotic exponent of matrix multiplication.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Khoruzhii, Serafin, Gelß and Pokutta**, *Local Improvements to Trilinear Aggregation* (LITA, https://github.com/khoruzhii/lita): this scheme is derived from LITA's published 15x15x15 scheme (rank 1977), cut to 14x15x15, 13x15x15 and 13x14x15 by the GPT builder's pinned recipe, then cut once more to 13x13x15 by the Opus builder (a direction the kill-count ranking never tries: it removes only 36 terms but opens a 25-dimensional kernel that absorbs 35 more), their published scheme, by restriction and exact absorption. Please credit them when using it.
- **A. I. Perminov**, *FastMatrixMultiplication* (https://github.com/dronperminov/FastMatrixMultiplication): the status table and the scheme file format this object uses.
- **A. Sedoglavic**, *Catalogue of fast matrix multiplication algorithms* (https://fmm.univ-lille.fr/ and https://github.com/sedoglavic/fmm_digest).
- **MerlijnW70**, *fmm-schemes* (https://github.com/MerlijnW70/fmm-schemes).
- **M. Kauers and I. Wood**, *Exploring the Meta Flip Graph for Matrix Multiplication*, arXiv:2510.19787: projection edges between formats, of which this slice is a non-coordinate version.
- **M. Kauers and J. Moosbauer**, *Flip Graphs for Matrix Multiplication*, arXiv:2212.01175: rank-lowering reductions, which the absorption step generalizes.
- Contributor credit: `anonymous-c6d1e0ab`.
