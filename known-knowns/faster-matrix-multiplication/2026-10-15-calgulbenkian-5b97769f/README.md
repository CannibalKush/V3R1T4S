# Fast matrix multiplication: format (13, 15, 15) in rank 1762 over Q

## What

The object claim/object/13x15x15_r1762_Q.json (sha256 5b97769fb1c3115c7195f0c508e0cae9ded013ef2543a7f0d5aa4147410e1647) is, by my own exact rational check using Perminov's index convention (C stored transposed), a correct bilinear scheme over Q for the 13x15x15 matrix product with 1762 terms having all three factors nonzero, strictly below 1776 (fmm_sota.json and the Perminov table minimum), 1797 (Lille), the absent MerlijnW70 entry, and the repository's merged 1763, as fetched 2026-10-15.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/13x15x15_r1762_Q.json`.

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
| Sedoglavic `fmm_sota.json` | [13, 15, 15] | 1776 | **1762** | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T21:00:18Z |
| Lille per-format catalogue | 13x15x15 | 1797 | **1762** | https://fmm.univ-lille.fr/13x15x15.html | 2026-10-15T21:00:18Z |
| Perminov `README.md` (ZT / Z / Q) | 13x15x15 | 1776 | **1762** | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T21:00:18Z |
| MerlijnW70/fmm-schemes | 13x15x15 | none | **1762** | https://github.com/MerlijnW70/fmm-schemes | 2026-10-15T21:00:18Z |
| V3R1T4S `TROPHY_CASE.md` and open pull requests | 13x15x15 | none | **1762** | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T21:00:18Z |
| V3R1T4S `known-knowns/faster-matrix-multiplication/` (our merged pull request #130, 2026-10-15 16:33 UTC) | 13x15x15 | 1763 | **1762** | https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns/faster-matrix-multiplication/2026-10-14-anonymous-c6d1e0ab-710c8ff6 | 2026-10-15T21:00:00Z |

The panel's novelty skeptic re-fetched every source independently (first fetch 2026-10-15T18:41:19Z); its report is `panel/novelty.md`. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- The scheme is over the rationals. Nothing is claimed for the integer, ternary or GF(2) ranks of this format.
- The margin is 1 multiplication below the lowest known value, 1763, which is this repository's own merged scheme (pull request #130); the live catalogues still list 1776 and 1797. The maintainer's comment on pull request #164 invited this scheme as one below #130. Records in this range move often; the comparison holds for the table versions recorded here.
- This is a rank bound for one format and does not improve the asymptotic exponent of matrix multiplication.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Khoruzhii, Serafin, Gelß and Pokutta**, *Local Improvements to Trilinear Aggregation* (LITA, https://github.com/khoruzhii/lita): this scheme is derived from LITA's published 15x15x15 rank-1977 scheme (Khoruzhii and others), sliced to 14x15x15 rank 1842 and then to 13x15x15, with exact rational dependency absorption at each step, their published scheme, by restriction and exact absorption. Please credit them when using it.
- **A. I. Perminov**, *FastMatrixMultiplication* (https://github.com/dronperminov/FastMatrixMultiplication): the status table and the scheme file format this object uses.
- **A. Sedoglavic**, *Catalogue of fast matrix multiplication algorithms* (https://fmm.univ-lille.fr/ and https://github.com/sedoglavic/fmm_digest).
- **MerlijnW70**, *fmm-schemes* (https://github.com/MerlijnW70/fmm-schemes).
- **M. Kauers and I. Wood**, *Exploring the Meta Flip Graph for Matrix Multiplication*, arXiv:2510.19787: projection edges between formats, of which this slice is a non-coordinate version.
- **M. Kauers and J. Moosbauer**, *Flip Graphs for Matrix Multiplication*, arXiv:2212.01175: rank-lowering reductions, which the absorption step generalizes.
- Contributor credit: `calgulbenkian`.
