# The record we beat

Cell: <5,5,5>, rank 93, reduced additions (Perminov 'reduced' convention), ternary coefficients.
Value in the table: 383, file schemes/results/addition_reduced_ZT/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json (sha256 808285b8fb393d2e950ecff4ffe9881a209b6d3eff0d787e34d801a3f22293da), the only addition_reduced_ZT file for 5x5x5.
Also 383 in arXiv:2512.13365v2 (Perminov), results table, row 5x5x5 (NOVELTY panel fetch 2026-10-15T15:23:35Z).

Fetch log (one honest GET each, curl, User-Agent naming V3R1T4S; time | HTTP | sha256 of the page | URL | saved name):

2026-10-15T15:20:24Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | perminov_tree.json
2026-10-15T15:20:25Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | perminov_README.md
2026-10-15T15:20:25Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | perminov_CHANGELOG.md
2026-10-15T15:20:26Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | reduced_known.json
2026-10-15T15:20:26Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | fmm_sota.json
2026-10-15T15:20:27Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | matmul_COVERAGE.md
2026-10-15T15:20:27Z | 200 | 3daec22adb7e0efa20ebc2f2e9847b32951da7c57dc0980fbd00bc476645b593 | https://fmm.univ-lille.fr/5x5x5.html | lille_5x5x5.html
2026-10-15T15:20:28Z | 200 | 48c623ce3a79aaba234d4ce2137c013a3aa8385426a61d6e53054d64384ee511 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | v3r1t4s_open_prs.json

Extracted values: tree truncated=false; 5x5x5 addition_reduced_ZT min cr 383; reduced_known.json has no 5x5x5 key; README lists 5x5x5
rank 93 with no addition count; CHANGELOG has no 5x5x5 entry; fmm_sota.json 5x5x5 rank 93; Lille 5x5x5 page cites the Moosbauer-Poole scheme and no complexity variant; matmulcatalog COVERAGE naive adds only.
