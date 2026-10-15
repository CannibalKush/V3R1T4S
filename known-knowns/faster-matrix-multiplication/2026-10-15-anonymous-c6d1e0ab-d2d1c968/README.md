# Fast matrix multiplication: format (11, 13, 16) in rank 1445 over Q

## What

claim/object/11x13x16_r1445_Q.json (sha256 d2d1c96812918b46fa34436c66cdd27e51383b12a9686a975d715d69e6480c75) is an exact bilinear scheme over Q (coefficients are the integers from -8 to 8 and the fractions plus or minus 1/2, 1/4, 1/8, so it is valid wherever 2 is invertible and is not a Z, ternary or GF(2) scheme) for the 11x13x16 format with 1445 rank-one terms, each with all three factors nonzero and no two mergeable, verified by my own exact-rational Brent-equation check, and 1445 is strictly below 1446, the minimum over the four criterion sources as I re-fetched them on 2026-10-14 between 17:26:49Z and 17:26:59Z (fmm_sota.json 1446; Lille 11x13x16 page 1446; Perminov README ZT 1458, Z 1458, Q 1446; MerlijnW70 fmm-schemes no 11x13x16 scheme in its complete tree), while the repository TROPHY_CASE.md dedup check was outside my permitted reading and is not asserted here.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/11x13x16_r1445_Q.json`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 10 seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed rank | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Sedoglavic `fmm_sota.json` | [11, 13, 16] | 1446 | **1445** | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-14T16:58:44Z |
| Lille per-format catalogue | 11x13x16 | 1446 (taken from Perminov, 2026) | **1445** | https://fmm.univ-lille.fr/11x13x16.html | 2026-10-14T16:58:45Z |
| Perminov `README.md` (ZT / Z / Q) | 11x13x16 | 1458 / 1458 / 1446 (min 1446) | **1445** | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-14T16:58:46Z |
| Perminov `CHANGELOG.md` | 11x13x16 | 1446 since 03.04.2026 | **1445** | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-14T16:58:47Z |
| MerlijnW70/fmm-schemes | 11x13x16 | none | **1445** | https://github.com/MerlijnW70/fmm-schemes | 2026-10-14T16:58:47Z |
| V3R1T4S `TROPHY_CASE.md` and open pull requests | 11x13x16 | none | **1445** | https://github.com/elder-plinius/V3R1T4S | 2026-10-14T16:58:48Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- The scheme is over the rationals: its coefficients have denominators up to 8. Nothing is claimed for the integer, ternary or GF(2) ranks of this format.
- The margin is one multiplication. Records in this range move often; the comparison holds for the table versions recorded here.
- This is a rank bound for one format and does not improve the asymptotic exponent of matrix multiplication.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, *FastMatrixMultiplication* (https://github.com/dronperminov/FastMatrixMultiplication). This scheme is derived from his published 12x13x16 rank-1509 scheme (`schemes/results/Q/12x13x16_m1509_Q.json`), and his 1446 is the record it is compared against. Please credit him when using it.
- **A. Sedoglavic**, *Catalogue of fast matrix multiplication algorithms* (https://fmm.univ-lille.fr/ and https://github.com/sedoglavic/fmm_digest).
- **MerlijnW70**, *fmm-schemes* (https://github.com/MerlijnW70/fmm-schemes).
- **M. Kauers and I. Wood**, *Exploring the Meta Flip Graph for Matrix Multiplication*, arXiv:2510.19787: projection edges between formats, of which this slice is a non-coordinate version.
- **M. Kauers and J. Moosbauer**, *Flip Graphs for Matrix Multiplication*, arXiv:2212.01175: rank-lowering reductions, which the absorption step generalizes.
- Contributor credit: `anonymous-c6d1e0ab`.
