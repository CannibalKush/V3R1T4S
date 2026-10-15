# Novelty check: 15x15x16 rank 2105 over Q

context: Claude Code subagent (Opus 5.5), fresh context
role: novelty skeptic (fresh start; read only the claim folder and claim.SHA256SUMS)

Claim under test: object/15x16x15_r2105_Q.json, an exact scheme over Q of rank 2105. Its axes are stored as 15x16x15, a cyclic rotation of the sorted format 15x15x16. Rank does not change under axis permutation, so every source was read for the sorted format 15x15x16 and for every axis order.

## Live sources (one plain curl GET each, User-Agent 'V3R1T4S-research (honest client; curl)', no retries)

| Source | URL | UTC fetch time | HTTP | sha256 of saved page | Value read |
|---|---|---|---|---|---|
| Sedoglavic digest | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:30:33Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | entry {"format": [15, 15, 16], "rank": 2132, "exponent": 2.808074}; createdAt 2026-10-09T11:45:48; it is the only entry whose sorted format is 15,15,16 |
| Lille per-format page (template https://fmm.univ-lille.fr/{n}x{m}x{p}.html) | https://fmm.univ-lille.fr/15x15x16.html | 2026-10-15T09:30:33Z | 200 | 69f7757285fa5b71cff67e74cedef6f262f599c0858c6b251e67e5e427a6fc69 | title line "Description of fast matrix multiplication algorithm: 15x15x16:2132", so rank 2132 |
| Perminov README | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:30:35Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | status row (columns Format, ZT rank, Z rank, Q rank, omega): "15x15x16 / 2132 (?) / 2132 (?) / 2132 (2173) / 2.808074285". So ZT 2132, Z 2132, Q 2132; the bracketed previous ranks are "?", "?" and 2173. The rank-improvement table also lists 15x15x16: previous 2173 (Q), new 2132 (ZT/Z). Minimum over the three columns: 2132 |
| Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T09:30:35Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | three 15x15x16 lines: found 2155 (Q); found 2132 (Z); rediscovered 2132 (ZT). Nothing below 2132. Latest entry is dated 09/10/2026 (cloudroom-math schemes added) |
| MerlijnW70 fmm-schemes tree | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-15T09:30:36Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 paths, "truncated": false, 32 scheme files; none for 15x15x16, 15x16x15 or 16x15x15. No value |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T09:30:36Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | no 15x15x16 row in any axis order. Matrix-multiplication rows are 15,16,16:2180; 14,15,15:1842; 13,14,14:1558; 14,14,15:1716; 13,14,15:1677 (all from restricting the LITA square schemes) |
| V3R1T4S open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T09:30:37Z | 200 | 7b69ba2e001ff158e1f3fb0fe924471fdac217f69257f01896d771c0351f197d | 40 open PRs. A regex over every title and body for 15x15x16, 15x16x15 or 16x15x15 (separators x, the multiplication sign or a comma) and for the numbers 2105 and 2132 found nothing. FMM-related open PRs: #130 (13,15,15 rank 1763) and #149 (4,6,7 additive complexity). Neither covers this format |

All checks were done on the saved copies of the pages. Every first request returned 200, so no request was retried. Both the digest and the Lille page hashes match the author's table-record hashes from 2026-10-15T09:07Z, so neither source changed since the author fetched it.

## Lille construction text

The Lille page has no separate "construction" column for this format. Its "Algorithm definition" reads: "The algorithm 15x15x16:2132 is taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026. [GitHub repository]". Its "Algorithm type" is a polynomial summary of the term supports, starting "12*X^6*Y^4*Z^4+8*X*Y^12*Z+8*X*Y*Z^12+54*X^5*Y^4*Z^4+126*X^4*Y^4*Z^4+..." and ending "...+52*X^2*Y*Z+64*X*Y^2*Z+44*X*Y*Z^2+28*X*Y*Z". It names no Kronecker product or other composition. An older search-engine snapshot of the same page showed rank 2160 (a Kronecker product of 3x3x2:15 and 5x5x8:144), which the live page now replaces with 2132.

## Literature and web search (last 24 months)

- arXiv:2606.02480 (Perminov, meta flip graph, June 2026; 207 formats improved up to 16x16x16) and arXiv:2603.02398 (Perminov, open-source flip-graph framework, March 2026). Both papers' results are in Perminov's README, which lists 2132.
- LITA (Khoruzhii et al., github.com/khoruzhii/lita; manuscript "Local Improvements to Trilinear Aggregation", in preparation, 2026). It lists square formats only: 15x15x15:1977 and 16x16x16:2236. Restricting 16x16x16 gives at most 2236 for 15x15x16, and adding a 15x15x1 slab to 15x15x15 gives 1977 + 225 = 2202. Both are above 2105.
- matmulcatalog COVERAGE.md (solven-eu; arXiv:2606.13408): the 15,15,16 row reads "2132 Dronperminov-ZT" for F2 and for R/Q/Z, and best over any field is 2132.
- cloudroom-math (matyasstoch, added to Perminov's repository 09/10/2026): its README names only 4,6,15:261 among formats with a dimension of 15 or 16, and nothing for 15x15x16.
- Sedoglavic and Smirnov (2021): 15x15x15 at 2088, now superseded by 1977. Nothing for 15x15x16.
- Web searches for "15x15x16", "15x16x15", "16x15x15" and for recent flip-graph and trilinear-aggregation results up to October 2026 found no rank at or below 2105 for 15x15x16 in any axis order. Neighbouring trophy-case and table values (15x16x16: 2180 in the trophy case, 2223 in the tables) are for a larger format and do not bound 15x15x16 below 2105.

## Verdict

The minimum over everything found is 2132: digest 2132, Lille 2132, Perminov ZT/Z/Q 2132/2132/2132, MerlijnW70 has no scheme, the trophy case has no row, and no open PR covers this format. The literature shows nothing at or below 2105. 2105 is below 2132 by 27, so it strictly beats everything known. It is not a tie, and it is not a listed composition. This verdict covers novelty only. Whether the scheme is correct is for the panel's verification skeptic.

pass: true
