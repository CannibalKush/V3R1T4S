# Novelty skeptic: 13x14x14 rank 1538 over Q

context: Claude Code subagent (Opus 5.5), fresh context

Claim: an exact bilinear scheme over Q for the format 13x14x14 with 1538 rank-one terms. Sorted format: (13,14,14). Rank does not change under axis permutation, so every source was checked for any order of 13, 14, 14.

## Live sources (one plain curl request each, User-Agent "V3R1T4S-research (honest client; curl)", no retries)

| # | Source | URL | UTC fetch time | HTTP | sha256 of saved page | Value read |
|---|---|---|---|---|---|---|
| 1 | Sedoglavic digest | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:20:50Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | entry `{"format": [13, 14, 14], "rank": 1582, "exponent": 2.817692}`; digest createdAt 2026-10-09T11:45:48; 5456 entries |
| 2 | Lille per-format page (template https://fmm.univ-lille.fr/{n}x{m}x{p}.html) | https://fmm.univ-lille.fr/13x14x14.html | 2026-10-15T09:20:50Z | 200 | f4f5d1067f4dea0882d6c15b04fa4399609c5cd695777824ce1a96c6d22330cd | title line: "Description of fast matrix multiplication algorithm: ⟨13×14×14:1614⟩" (rank 1614) |
| 3a | Perminov README | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:20:51Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | status row: "13x14x14 / 1614 (?) / 1614 (1625) / 1582 (1625) / 2.817691580", so ZT 1614 (?), Z 1614 (earlier 1625), Q 1582 (earlier 1625). Improvements table row: "13x14x14 / 1625 (Z) / 1582 (Q), file schemes/results/Q/13x14x14_m1582_Q.json". Minimum 1582 |
| 3b | Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T09:20:51Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | 28/09/2026: "13x14x14: found scheme with 1582 multiplications (Q)". Earlier entries: 1602 (Q), 1614 (ZT). Newest entry is 09/10/2026 (cloudroom-math schemes added); no 13x14x14 line below 1582 |
| 4 | MerlijnW70 fmm-schemes tree | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-15T09:20:52Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 paths, truncated=false; no file for 13x14x14, 14x13x14 or 14x14x13. Nearest: 13x13x15_m1591, 13x14x16_m1805, 11x14x14_m1367 |
| 5 | V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T09:20:52Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | row 45: "13,14,14 rank 1558 over Q", "below the minimum 1582 of the four criterion sources (-24)", "restriction of LITA squares (Khoruzhii, Serafin, Gelß, Pokutta)". Value 1558 |
| 6 | V3R1T4S open PRs | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T09:20:52Z | 200 | 7b69ba2e001ff158e1f3fb0fe924471fdac217f69257f01896d771c0351f197d | 40 open PRs. No title or body names 13x14x14 in any order, 1538 or 1558. Open matrix-multiplication PRs: #130 (13,15,15) rank 1763 and #149 (4,6,7) additions. Neither is this format |

### Lille construction text

The page has no separate "construction" column. Its "Algorithm definition" section reads, verbatim: "The algorithm ⟨13×14×14:1614⟩ is taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026. [ GitHub repository ]". The "Algorithm description" section offers only Maple tensor, LRP and evaluation-scheme downloads. The page (1614) lags the Lille digest (1582).

## Literature, web and repository search (last 24 months)

- Web and arXiv searches for 13x14x14 rank schemes (all axis orders), and for ranks 1538, 1558 and 1582: no paper or page gives any explicit rank for this format.
- Papers checked for scope: Perminov arXiv:2603.02398 and arXiv:2606.02480 (meta flip graph with serendipitous product, 680 formats up to 16x16x16; its results are carried in the README row above, 1582); Kauers and Wood arXiv:2505.05896 and arXiv:2510.19787; Moosbauer and Poole arXiv:2502.04514; Khoruzhii, Gelß and Pokutta arXiv:2511.10786 (structured square formats only). None gives a 13x14x14 rank below 1582.
- LITA repository (github.com/khoruzhii/lita; repo API and tree fetched 2026-10-15T09:21:50Z and 09:22:01Z, HTTP 200, tree sha256 d923a68888fc427aa8e9d216c6e54d45eb078afb8718ea55ae4990f443b89339; 31 paths): square schemes only, including 14x14x14_r1593 and 13x13x13 rank 1379. No rectangular files. Restricting the 14x14x14 scheme gives at most 1593 for 13x14x14. The trophy case's 1558 comes from further peeling of the LITA squares.
- AntoineTilloy/explicit-matmul-schemes (repo API and tree fetched 2026-10-15T09:21:53Z and 09:22:02Z, HTTP 200, tree sha256 09f95e50b050f925b7ccba2284262ed71d75ea385dec4cbf1c168d2838fb7673; 662 paths): square N=14 at 1593 (one search snippet suggested one fewer, which would still be 1592). No file for 13x14x14 in any order.
- Limits: a web search cannot rule out unpublished or unindexed work. The search covered the named live tables, the repositories they cite, arXiv through mid-October 2026 as indexed, and this repository's trophy case and open PRs.

## Comparison

Values found for the sorted format (13,14,14): fmm_sota.json 1582; Lille page 1614; Perminov min(ZT, Z, Q) = 1582; MerlijnW70 none; LITA 14x14x14 restriction at most 1593; V3R1T4S trophy case 1558; open PRs none. The minimum of everything found is 1558.

1538 < 1558, a strict improvement of 20. It is not a tie.

## Verdict

novelty: PASS. Rank 1538 strictly beats the lowest known rank for 13x14x14, the trophy-case rank 1558. Every live table read 1582 or higher, and nothing at or below 1538 was found in the literature or in open PRs. This check covers novelty only. The scheme's correctness is for the other skeptics.

pass: true
