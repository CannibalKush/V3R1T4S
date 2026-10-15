# Novelty check: 15x16x16, rank 2176 over Q

context: Claude Code subagent (Opus 5.5), fresh context

Claim read: claim/CLAIM.md, claim/INDEX.csv, claim/table-record/README.md and the object file name (object/15x16x16_r2176_Q.json). All four files match claim.SHA256SUMS. The claimed rank is 2176 for the format 15x16x16 over Q. Sorted format: (15,16,16).

## Live sources (one plain curl GET each, User-Agent 'V3R1T4S-research (honest client; curl)', no retries)

| # | URL | UTC fetch time | HTTP | sha256 of saved page | Value read |
|---|---|---|---|---|---|
| 1 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:20:52Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | entry {"format": [15, 16, 16], "rank": 2223, "exponent": 2.801309}; digest createdAt 2026-10-09T11:45:48, 5456 entries |
| 2 | https://fmm.univ-lille.fr/15x16x16.html | 2026-10-15T09:20:52Z | 200 | ec9909c16f784fb8dd22e470b9bb2770603927f85c83c5be118acbedb139f0b2 | title line "Description of fast matrix multiplication algorithm: ⟨15×16×16:2262⟩", so rank 2262 |
| 3a | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:20:54Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | status row `15x16x16` : ZT "2302 (?)", Z "2302 (?)", Q "2223 (2262)"; minimum 2223 (bracketed 2262 is the previous best). New-ranks table: 2262 (Q) to 2223 (Q) |
| 3b | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T09:20:54Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | 28/09/2026 "Rank improvement": `15x16x16` scheme with 2223 multiplications (Q); an earlier entry lists 2246 (Q). Newest entry 09/10/2026 (cloudroom-math schemes added) has no 15x16x16 line. Nothing below 2223 |
| 4 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-15T09:20:54Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 paths, truncated=false; no file for 15x16x16, 16x15x16 or 16x16x15 |
| 5 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T09:20:55Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | row 46: "<15,16,16> rank 2180 over Q (supersedes our 2196 of 2026-10-10)"; summary row also lists <15,16,16> 2180 |
| 6 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T09:20:55Z | 200 | 7b69ba2e001ff158e1f3fb0fe924471fdac217f69257f01896d771c0351f197d | 40 open PRs (under the page limit, so the list is complete); none mentions 15x16x16, any permutation, 2176 or 2180 |
| 7 (extra) | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T09:22:06Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | row ⟨15,16,16⟩: F2 2302, R/Q/Z 2302, best (any field) 2302 |

The sha256 values for sources 1, 2, 3a, 4 and 5 are the same as in the author's table-record (fetched 2026-10-14T18:44Z). Those pages have not changed since the author checked them.

Lille URL template: https://fmm.univ-lille.fr/{n}x{m}x{p}.html

## Lille construction text (verbatim from the 15x16x16 page)

"The algorithm ⟨15×16×16:2262⟩ could be constructed using the following decomposition: ⟨15×16×16:2262⟩ = ⟨8×8×8:336⟩ + ⟨7×8×8:306⟩ + ⟨8×8×8:336⟩ + ⟨7×8×8:306⟩ + ⟨7×8×8:306⟩ + ⟨8×8×8:336⟩ + ⟨8×8×8:336⟩ ."

This is a block split, and the parts add up to 2262. The construction is not 2176.

## Nearby formats checked (restriction bounds)

A scheme for a larger format restricts to 15x16x16 at the same rank, so I checked the formats that contain it. fmm_sota.json lists [16,16,16] at 2236, [15,16,17] at 2448 and [16,16,17] at 2492. Perminov's README lists 16x16x16 at Q 2237. All of these are above 2176, so none of them gives an already-known rank at or below 2176.

## Literature and PR search (last 24 months)

Searches run on 2026-10-15 (web and arXiv): "15x16x16 matrix multiplication scheme rank 2176 OR 2180 OR 2223"; "15x16x16 / 15×16×16 / <15,16,16> matrix multiplication rank new scheme 2026"; "arXiv 2026 new upper bounds tensor rank rectangular matrix multiplication 16x16x16 flip graph LITA"; "LITA Khoruzhii Serafin Gelß Pokutta trilinear aggregation"; "matyasstoch cloudroom-math"; "github matrix multiplication scheme 15x16x16 rank Q json new record October 2026"; "restriction of square scheme peeling new ranks 15 16 16 rational"; "V3R1T4S fast matrix multiplication 15,16,16 rank".

What turned up:
- arXiv:2603.02398 and arXiv:2606.02480 (Perminov, flip graph and meta flip graph): their results feed the live README and CHANGELOG, whose best is 2223.
- arXiv:2511.20317 (ternary meta flip graphs), arXiv:2510.19787 (meta flip graph), arXiv:2506.22113 (commutative flip graphs), arXiv:2505.09824, arXiv:2602.13171 (complex to rational), arXiv:2511.10786 (structured flip graphs): none reports a rank for 15x16x16 below 2223.
- arXiv:2606.13408 (matmulcatalog article): lists ⟨15,16,16⟩ at 2262 (non-commutative), against 2302 from Perminov.
- The GitHub fork MerlijnW70/FastMatrixMultiplication lists 15x16x16 as 2262 to 2223 (Q). MerlijnW70/fmm-schemes releases v1.1 and v1.3 have no 15x16x16 entry.
- 3x3 addition-count papers (2604.27645, 2609.06588, 2607.28676, 2512.21980, 2508.03857, 2601.05272) are not relevant to this format.
- No paper, repository or web page reports a rank at or below 2176 for 15x16x16 in any axis order.

V3R1T4S: TROPHY_CASE.md holds the repository's own 2180 (row 46, from LITA squares by restriction and absorption). None of the 40 open PRs touches this format.

## Verdict

Minimum over everything found: 2180 (V3R1T4S TROPHY_CASE.md, row 46). The public tables give 2223 (fmm_sota.json, Perminov Q), 2262 (Lille page) and 2302 (Perminov ZT and Z, matmulcatalog). MerlijnW70 has no scheme for this format. The claim's 2176 is strictly below 2180, by 4. This is a strict improvement, not a tie.

This check covers novelty only. It does not verify that the scheme is correct.

novelty: PASS (2176 < 2180)

pass: true
