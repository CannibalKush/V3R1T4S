# Fast matrix multiplication: format (13, 13, 14) in rank 1479 over Q

## What

The file claim/object/13x13x14_r1479_Q.json (sha256 e738d0f367b67ba740109db2687b58811da516ee74f67c42ccb934eab382548d) is a bilinear scheme with exactly 1479 rank-one terms, all three factors nonzero in every term, whose coefficients are rationals with denominators dividing 1088 and which satisfies all 5597956 Brent equations for the format 13x13x14 exactly over Q, and 1479 is strictly below 1511, the rank listed for the sorted format 13x13x14 in each of fmm_sota.json (createdAt 2026-10-09T11:45:48), the Lille page https://fmm.univ-lille.fr/13x13x14.html, and Perminov's README ZT/Z/Q columns, while MerlijnW70's fmm-schemes held no 13x13x14 scheme, all as fetched by me once on 2026-10-15 between 09:13:40Z and 09:13:43Z.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/13x13x14_r1479_Q.json`.

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
| Sedoglavic `fmm_sota.json` | [13, 13, 14] | 1511 | **1479** | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:07:46Z |
| Lille per-format catalogue | 13x13x14 | 1511 | **1479** | https://fmm.univ-lille.fr/13x13x14.html | 2026-10-15T09:07:46Z |
| Perminov `README.md` (ZT / Z / Q) | 13x13x14 | 1511 / 1524 / 1511 | **1479** | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:07:46Z |
| MerlijnW70/fmm-schemes | 13x13x14 | none | **1479** | https://github.com/MerlijnW70/fmm-schemes | 2026-10-15T09:07:46Z |
| V3R1T4S `TROPHY_CASE.md` and open pull requests | 13x13x14 | none | **1479** | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T09:07:46Z |

The panel's novelty skeptic re-fetched every source independently (first fetch 2026-10-15T09:12:49Z); its report is `panel/novelty.md`. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- The scheme is over the rationals. Nothing is claimed for the integer, ternary or GF(2) ranks of this format.
- The margin is 32 multiplications below the lowest listed value (1511). Records in this range move often; the comparison holds for the table versions recorded here.
- This is a rank bound for one format and does not improve the asymptotic exponent of matrix multiplication.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Khoruzhii, Serafin, Gelß and Pokutta**, *Local Improvements to Trilinear Aggregation* (LITA, https://github.com/khoruzhii/lita): this scheme is derived from LITA's published 15x15x15 scheme (rank 1977), cut to 14x15x15, 13x15x15, 13x14x15, 13x14x14 and then 13x13x14, their published scheme, by restriction and exact absorption. Please credit them when using it.
- **A. I. Perminov**, *FastMatrixMultiplication* (https://github.com/dronperminov/FastMatrixMultiplication): the status table and the scheme file format this object uses.
- **A. Sedoglavic**, *Catalogue of fast matrix multiplication algorithms* (https://fmm.univ-lille.fr/ and https://github.com/sedoglavic/fmm_digest).
- **MerlijnW70**, *fmm-schemes* (https://github.com/MerlijnW70/fmm-schemes).
- **M. Kauers and I. Wood**, *Exploring the Meta Flip Graph for Matrix Multiplication*, arXiv:2510.19787: projection edges between formats, of which this slice is a non-coordinate version.
- **M. Kauers and J. Moosbauer**, *Flip Graphs for Matrix Multiplication*, arXiv:2212.01175: rank-lowering reductions, which the absorption step generalizes.
- Contributor credit: `anonymous-c6d1e0ab`.
