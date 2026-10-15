# Fast Matrix Multiplication: Format `(13, 15, 15)` in Rank 1763 over `Q`

## What

claim/13x15x15_r1763_Q.json (sha256 710c8ff6593f7c6e578a9ae83b4d7083ed5381db72fd734e614a3108d7c87465) is an exactly verified bilinear scheme over Q for the format <13,15,15> with 1763 non-zero rank-one terms, which is strictly less than the minimum rank 1776 across the four live criterion sources fetched 2026-10-14T13:54:59Z-13:55:00Z.

Path note: the confirmed-scope sentence above is quoted word for word from `panel/gate.md` and names the panel's `claim/` folder; in this package the same file (identical bytes) is `object/13x15x15_r1763_Q.json`.

## Check it yourself

From this package folder (`2026-10-14-anonymous-c6d1e0ab-710c8ff6/`), run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` (3.8+, standard library only) and a C compiler (`cc` / `clang` / `gcc`).
- **Rough laptop time**: ~2 seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

All criterion sources were fetched live on `2026-10-14` (`00:05:32Z`–`01:19:31Z`, one honest GET per source, no retries; see `the-record-we-beat/README.md` and `the-record-we-beat/sources_2026-10-14T01-19-25Z.json`):

| Source | Cell | Listed Rank | Our Rank (`Q`) | Margin | URL | UTC Fetch Time |
|---|---|---|---|---|---|---|
| Sedoglavic `fmm_sota.json` | `[13, 15, 15]` | `1776` | **`1763`** | **`-13`** | `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` | `2026-10-14T01:19:25Z` |
| Lille per-format catalogue | `13x15x15` | `1797` | **`1763`** | **`-34`** | `https://fmm.univ-lille.fr/13x15x15.html` | `2026-10-14T01:19:25Z` |
| Perminov `README.md` (`ZT / Z / Q`) | `13x15x15` | `1797 / 1797 / 1776` (min `1776`) | **`1763`** | **`-13`** | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md` | `2026-10-14T01:19:29Z` |
| `MerlijnW70/fmm-schemes` | `13x15x15` | none (`—`) | **`1763`** | — | `https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS` | `2026-10-14T01:19:29Z` |
| `solven-eu/matmulcatalog` `COVERAGE.md` | `13,15,15` | `1797` (`F2`) / `1797` (`R/Q/Z`) | **`1763`** | **`-34`** | `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` | `2026-10-14T01:19:30Z` |

## Not claimed

- This bound is over the rational numbers $\mathbb{Q}$ (`ring: "Q"`), with denominators dividing $L = 54,400 = 2^7 \cdot 5^2 \cdot 17$. Nothing is claimed for the ternary (`ZT`), integer (`Z`), or characteristic-2 (`GF(2)`) ranks of format `(13, 15, 15)`.
- This is a finite-format rank bound for `(13, 15, 15)` and does not improve the asymptotic exponent $\omega$ of matrix multiplication.
- Checked internally by three independent skeptic subagents (`panel/`) and the standalone checker shipped here; not peer reviewed.

## Credits

- **K. Khoruzhii, L. Serafin, P. Gelß, and S. Pokutta**, *Local Improvements to Trilinear Aggregation* (`https://github.com/khoruzhii/lita`, 2026): our `(13, 15, 15)` rank `1763` scheme descends from LITA's `(15, 15, 15)` rank `1977` square scheme via the V3R1T4S `(14, 15, 15)` rank `1842` scheme (`known-knowns/faster-matrix-multiplication/schemes/14x15x15_r1842_Q.json`). Please cite LITA when using this derived scheme.
- **A. Sedoglavic**, *Catalogue of Fast Matrix Multiplication Algorithms* (`https://fmm.univ-lille.fr/` and `https://github.com/sedoglavic/fmm_digest`).
- **A. I. Perminov**, *FastMatrixMultiplication* (`https://github.com/dronperminov/FastMatrixMultiplication`, arXiv:2606.02480).
- **MerlijnW70**, *fmm-schemes* (`https://github.com/MerlijnW70/fmm-schemes`).
- **solven-eu**, *matmulcatalog* (`https://github.com/solven-eu/matmulcatalog`).
- **M. Kauers and J. Wood**, arXiv:2510.19787 (slice restrictions), and **R. P. Brent**, STAN-CS-70-157 (1970) (the Brent equations).
- Contributor credit: `anonymous-c6d1e0ab`.
