# Fast matrix multiplication: format (15, 15, 16) in rank 2105 over Q

## What

The file claim/object/15x16x15_r2105_Q.json (sha256 4b68518ac7f293047071df6723a04783e4d38f302c6b98ccaa02f0c66669ae3b) is an exact bilinear scheme over Q for the format 15x16x15 with 2105 rank-one terms, all three factors nonzero in every term, satisfying all 12,960,000 Brent equations in exact rational arithmetic, and 2105 is strictly below 2132, the rank listed for the sorted format 15x15x16 in fmm_sota.json (createdAt 2026-10-09T11:45:48), the Lille 15x15x16 page, and Perminov's README ZT/Z/Q columns, with no 15x15x16 scheme in the MerlijnW70 fmm-schemes tree, all four fetched 2026-10-15T09:31Z.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/15x16x15_r2105_Q.json`.

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
| Sedoglavic `fmm_sota.json` | [15, 15, 16] | 2132 | **2105** | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:07:49Z |
| Lille per-format catalogue | 15x15x16 | 2132 | **2105** | https://fmm.univ-lille.fr/15x15x16.html | 2026-10-15T09:07:49Z |
| Perminov `README.md` (ZT / Z / Q) | 15x15x16 | 2132 / 2132 / 2173 | **2105** | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:07:49Z |
| MerlijnW70/fmm-schemes | 15x15x16 | none | **2105** | https://github.com/MerlijnW70/fmm-schemes | 2026-10-15T09:07:49Z |
| V3R1T4S `TROPHY_CASE.md` and open pull requests | 15x15x16 | none | **2105** | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T09:07:49Z |

The panel's novelty skeptic re-fetched every source independently (first fetch 2026-10-15T09:30:33Z); its report is `panel/novelty.md`. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- The scheme is over the rationals. Nothing is claimed for the integer, ternary or GF(2) ranks of this format.
- The margin is 27 multiplications below the lowest listed value (2132). Records in this range move often; the comparison holds for the table versions recorded here.
- This is a rank bound for one format and does not improve the asymptotic exponent of matrix multiplication.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Khoruzhii, Serafin, Gelß and Pokutta**, *Local Improvements to Trilinear Aggregation* (LITA, https://github.com/khoruzhii/lita): this scheme is derived from LITA's published 17x17x17 scheme (rank 2723), cut to 16x17x17, 15x17x17, 15x16x17 and 15x16x16 (rank 2176) by the GPT builder's pinned recipe, then cut once more to 15x15x16 with a seeded exact absorption by the Opus builder, their published scheme, by restriction and exact absorption. Please credit them when using it.
- **A. I. Perminov**, *FastMatrixMultiplication* (https://github.com/dronperminov/FastMatrixMultiplication): the status table and the scheme file format this object uses.
- **A. Sedoglavic**, *Catalogue of fast matrix multiplication algorithms* (https://fmm.univ-lille.fr/ and https://github.com/sedoglavic/fmm_digest).
- **MerlijnW70**, *fmm-schemes* (https://github.com/MerlijnW70/fmm-schemes).
- **M. Kauers and I. Wood**, *Exploring the Meta Flip Graph for Matrix Multiplication*, arXiv:2510.19787: projection edges between formats, of which this slice is a non-coordinate version.
- **M. Kauers and J. Moosbauer**, *Flip Graphs for Matrix Multiplication*, arXiv:2212.01175: rank-lowering reductions, which the absorption step generalizes.
- Contributor credit: `anonymous-c6d1e0ab`.
