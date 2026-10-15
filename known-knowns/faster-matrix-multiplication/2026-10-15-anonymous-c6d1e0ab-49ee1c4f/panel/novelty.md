# Novelty skeptic: fmm-catalogue-small-format-rank, 13x14x15 rank 1645 over Q

context: Claude Code subagent (Opus 5.5), fresh context

Claim read: CLAIM.md, INDEX.csv, table-record/README.md, and the object file name (object/13x14x15_r1645_Q.json). Claimed rank 1645 for <13,14,15> over Q. Sorted format: (13,14,15).

## Live sources (one plain curl GET each, User-Agent 'V3R1T4S-research (honest client; curl)', no retries)

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| fmm_sota.json digest | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:12:49Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48, 5456 entries; `{"format": [13, 14, 15], "rank": 1681, "exponent": 2.816137}` |
| Lille per-format page (template https://fmm.univ-lille.fr/{n}x{m}x{p}.html) | https://fmm.univ-lille.fr/13x14x15.html | 2026-10-15T09:12:50Z | 200 | d2a562a11c213effc7df98468757cda923925f248fab408ed38c485039851158 | title line: "Description of fast matrix multiplication algorithm: ⟨13×14×15:1681⟩" |
| Perminov README | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:12:51Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | Research Findings & Status row: `` | `13x14x15` |  1681 (?)   | 1681 (1714)  | 1681 (1714)  |   2.816136526   | `` (ZT 1681, Z 1681, Q 1681; bracketed previous 1714). New-best-ranks row: prev 1714 (Z), new 1681 (ZT/Z). Minimum: 1681 |
| Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T09:12:52Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | latest entry 09/10/2026; 13x14x15 entries: 1698 (ZT), then 1681 (Z), then "rediscovered" 1681 (ZT). Nothing below 1681 |
| MerlijnW70 fmm-schemes tree | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-15T09:12:52Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 paths, truncated false; no file for 13x14x15 or any permutation (nearest: 13x13x15_m1591, 13x14x16_m1805) |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T09:12:53Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | entry 48: "<13,14,15> rank 1677 over Q", below 1681 by 4 |
| V3R1T4S open PRs | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T09:12:53Z | 200 | 7b69ba2e001ff158e1f3fb0fe924471fdac217f69257f01896d771c0351f197d | 40 open PRs; titles, bodies and branch names scanned for any axis order of 13,14,15: no match. FMM PRs present: #130 (13,15,15) rank 1763, #149 (4,6,7) additions. None for this format |

The hashes for fmm_sota.json, the Lille page, Perminov's README, the MerlijnW70 tree and TROPHY_CASE.md match those in the author's table-record, so those pages had not changed since the author's fetch at about 09:07Z.

### Lille construction text (verbatim, tags stripped)

"Algorithm definition. The algorithm ⟨13×14×15:1681⟩ is taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026. [GitHub repository]". The page has no composition, padding or block-split line for this format. The "Algorithm type" field is a polynomial of term-support counts (it starts 7·X^4·Y^4·Z^6 + 2·X^4·Y^6·Z^3 + ...), not a construction.

## Extra checks

- matmulcatalog COVERAGE.md, https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md, fetched 2026-10-15T09:14:12Z, HTTP 200, sha256 c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7: row `⟨13,14,15⟩`, F2 1681 and R/Q/Z 1681 (Dronperminov-ZT), best over any field 1681.
- arXiv 2606.13408 ("A catalog of fast matrix multiplication algorithms with exhaustive derivations", dated 2026-06-11), https://arxiv.org/abs/2606.13408, fetched 2026-10-15T09:14:13Z, HTTP 200, sha256 0f660efe3eabbecea23372f4559dba04acdebb6153fd4b51477b35ad45c1f88c: abstract page only. Its live catalogue (the matmulcatalog row above) reports 1681.
- Composition sanity check: I took one split along any axis, using fmm_sota.json ranks (and n·m for a format with a 1). The best is 1732 = R(4,14,15) + R(9,14,15). No simple split comes near 1645.

## Literature search (last 24 months, any axis order)

I ran web searches for "13x14x15", "<13,14,15>" and "13×14×15" with rank or tensor rank, plus searches for flip-graph and meta-flip-graph papers from 2025 and 2026. These covered arXiv 2502.04514, 2510.19787 (Kauers and Wood meta flip graph), 2511.10786 and 2511.20317 (ternary meta flip graphs), 2603.02398 (Perminov framework), 2606.02480 (meta flip graph with serendipitous product), 2606.13408 (catalog), 2609.17533 (GPU search over F2), AlphaEvolve, and the Khoruzhii/Serafin/Gelß/Pokutta (LITA) line. The only rank I found for this format outside the repository is 1681 (Perminov, Feb 2026; Lille). The lowest rank known anywhere is the repository's own trophy, 1677. I found no published or posted rank at or below 1645 for any permutation of 13x14x15.

## Verdict

Minimum over everything found: 1677 (TROPHY_CASE.md entry 48). Without the trophy, the minimum of the four public sources and matmulcatalog is 1681. The claimed 1645 is strictly below 1677, by 32, and so it is new as a rank. This verdict covers novelty only. It does not check that the scheme is exactly correct.

novelty: PASS (1645 < 1677)
pass: true
