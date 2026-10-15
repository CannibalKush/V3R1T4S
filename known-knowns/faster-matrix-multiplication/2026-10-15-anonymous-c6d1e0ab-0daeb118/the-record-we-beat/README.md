# The record we beat (metadata only)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the author. No page is copied here.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| tree.json | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T11:55:16Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | addition_reduced_ZT files for 4x6x6 rank 105: cr [430]; minimum 430 |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T09:46:09Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | 4x6x6-105: None |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:44:30Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | no lower count for this format and rank stated |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T09:44:31Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | no lower count for this format and rank stated |
| lille_4x6x6.html | https://fmm.univ-lille.fr/4x6x6.html | 2026-10-15T12:10:59Z | 200 | 32bd27b99d224bba878517615f3d04b31d8102d0f9a616c47b111c88b5af6e44 | rank 105; Commentaries section present: False |
| COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T09:44:32Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | adds column is a naive count (nz(U)+nz(V)+nz(W)-2r-np), not comparable; no cell below the reduced counts |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T11:55:17Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | [4, 6, 6]: rank 105 |

Compared cell: 4x6x6 at rank 105, reduced additions. Reference (minimum over Perminov's files for this format and rank): 430. This object: 373.

## Reference scheme file (not shipped: third-party data)

The reference count comes from Perminov's file https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x6x6_m105_cr430_fv243_cn894_ZT_reduced.json (sha256 of the copy the author fetched on 2026-10-15: 9427b13b5509d45df8c56294f2abe6bc4e478f2aa079a1925e600ca2183739b5). This object uses a different rank-equal scheme (a Kronecker product of two of Perminov's schemes, see CLAIM.md), so only the format, rank and count compare. To recount the reference, download it and run verify-it-yourself/check_slp.py on it; the author's counter reproduces its cr value.

## Other sources compared (read by the author, not copied here)

| Source | What it says for 4x6x6 at rank 105 | Our value |
|---|---|---|
| Perminov, arXiv:2512.13365 Table 1 | 430 (same convention) | 373 |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 (PDF sha256 c095482d4bc6a410171092bc6b37ef4e2a1d07808c076149f0f183704fbff3d6, downloaded by hand after an automated fetch met a challenge page) | no count at rank 105; 464 over Z at rank 106 (another scheme, Table 3.4) | 373 |
| V3R1T4S open pull requests on this target | none | 373 |
| V3R1T4S TROPHY_CASE.md | no row for this target | 373 |

The panel's novelty skeptic fetched every primary page again on 2026-10-15 (times and sha256 in panel/novelty.md); all pages
matched the author's record.

## Re-fetched by the author before filing

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| Perminov repository tree, re-fetched by the author before filing | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T11:55:16Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | addition_reduced_ZT files for 4x6x6 rank 105: 1 file(s), minimum cr 430; unchanged |
| fmm_sota.json, re-fetched by the author before filing | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T11:55:17Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | 4x6x6: rank 105, unchanged |
