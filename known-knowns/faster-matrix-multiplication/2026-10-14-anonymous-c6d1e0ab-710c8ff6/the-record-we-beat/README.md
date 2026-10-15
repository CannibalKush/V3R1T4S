# The Record We Beat: Format `(13, 15, 15)` (`fmm-catalogue-small-format-rank`)

All four criterion sources (plus `solven-eu/matmulcatalog` and the repository open pull requests endpoint) were fetched live with a single honest GET (`curl -sS`) on `2026-10-14` during scouting (`00:05:32Z`–`01:11:09Z`) and re-fetched by the independent `NOVELTY` panelist (`01:19:25Z`–`01:19:31Z`).

| Source | URL | UTC Fetch Time | HTTP Status | SHA-256 of Fetched Page | Extracted Cell for `(13, 15, 15)` |
|---|---|---|---|---|---|
| Sedoglavic `fmm_sota.json` | `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` | `2026-10-14T01:19:25Z` | `200` | `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1` | `{"format": [13, 15, 15], "rank": 1776, "exponent": 2.812457}` (`createdAt: 2026-10-09T11:45:48`) |
| Lille per-format catalogue page | `https://fmm.univ-lille.fr/13x15x15.html` | `2026-10-14T01:19:25Z` | `200` | `ce3fdb838b44413ff5b4b6d7a94ae09b6581254148141ddae788c7aa2cd68ee7` | `13x15x15:1797` (Andrew I. Perminov, Feb 2026; no lower-rank construction derivation listed) |
| Perminov `README.md` (`ZT / Z / Q`) | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md` | `2026-10-14T01:19:29Z` | `200` | `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341` | `1797 (?) / 1797 (1803) / 1776 (1803)` (minimum `1776` over `Q`) |
| `MerlijnW70/fmm-schemes` (`SHA256SUMS`) | `https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS` | `2026-10-14T01:19:29Z` | `200` | `de848328881cf69cbe2a8d8309e04d94826cf1431b5b39e81db63f95af58a3fd` | none (`32` entries; `13x15x15` absent) |
| `solven-eu/matmulcatalog` `COVERAGE.md` | `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` | `2026-10-14T01:19:30Z` | `200` | `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7` | `1797` (`F2`) / `1797` (`R/Q/Z`) |
| V3R1T4S Open Pull Requests | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` | `2026-10-14T01:19:31Z` | `200` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `0` open PRs (`[]`) |

- **Minimum across all sources**: `1776`
- **Our verified rank over `Q` (`object/13x15x15_r1763_Q.json`)**: `1763` (`margin = -13`).
