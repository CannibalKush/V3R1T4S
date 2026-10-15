# Novelty check: 13x13x14, rank 1479 over Q

context: Claude Code subagent (Opus 5.5), fresh context

Claim read: the scheme in object/13x13x14_r1479_Q.json has 1479 terms for the format 13x13x14. Sorted format: (13,13,14). Rank does not change when the axes are permuted, so every source was checked for 13x13x14, 13x14x13 and 14x13x13.

## Sources (one plain request each, curl, User-Agent 'V3R1T4S-research (honest client; curl)', no retries)

| Source | URL | UTC fetch time | HTTP | sha256 of saved page | Value read |
|---|---|---|---|---|---|
| Sedoglavic digest (createdAt 2026-10-09T11:45:48) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:12:49Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | `{ "format": [13,13,14], "rank": 1511, "exponent": 2.826838 }` |
| Lille per-format page | https://fmm.univ-lille.fr/13x13x14.html | 2026-10-15T09:12:50Z | 200 | 60f9a6f7a1b36fb5c4e86c9111aee78abae17873544dcae7b98d0fff2ed70151 | title: "Description of fast matrix multiplication algorithm: ⟨13×13×14:1511⟩" |
| Perminov README status table | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:12:51Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | status row for 13x13x14: ZT "1511 (?)", Z "1511 (1524)", Q "1511 (1524)". So ZT is 1511, and Z and Q are 1511 (earlier 1524). The key-results row shows previous 1524 (Z), new 1511 (ZT). |
| Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T09:12:52Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | only entry: under "12.02.2026", "13x13x14: found scheme with 1511 multiplications (ZT)". No newer entry. The newest entry (09/10/2026) adds matyasstoch cloudroom-math schemes; none is for this format. |
| MerlijnW70 fmm-schemes tree | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-15T09:12:52Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 paths, truncated=false. No file for 13x13x14, 13x14x13 or 14x13x13. The nearest are 13x13x15_m1591_ZT.json and 13x13x16_m1709_ZT.json. |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T09:12:53Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | no row for 13x13x14 or a permutation of it, and no 1479 |
| V3R1T4S open PRs | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T09:12:53Z | 200 | 7b69ba2e001ff158e1f3fb0fe924471fdac217f69257f01896d771c0351f197d | 40 open PRs. None names 13x13x14 or a permutation in its title or body. FMM-related PRs: #130 (13,15,15 rank 1763) and #149 (4,6,7 additions). |

The page hashes for the digest, the Lille page, the README, the MerlijnW70 tree and the trophy case match the hashes the author recorded at 09:07Z. The content has not changed since the author's check.

## Lille construction

The page has no composition, padding or block-splitting derivation for this rank. Its "Algorithm definition" reads: "The algorithm ⟨13×13×14:1511⟩ is taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026. [GitHub repository]". It gives maple tensor, LRP and evaluation-scheme files. So 1511 is a directly found scheme, and the listed rank to beat is 1511. (Per-format URL template: https://fmm.univ-lille.fr/{n}x{m}x{p}.html.)

## Literature and web search (last 24 months)

- Web searches for "13x13x14" / "13×13×14" with 1511 or 1479, and for 2025-2026 flip-graph rank results. No page reports a rank below 1511 for this format in any axis order.
- arXiv:2606.02480 (Perminov, "Meta Flip Graph meets Serendipitous Product", v1 1 Jun 2026, v2 5 Jun 2026): covers all 680 formats up to 16x16x16 and is reflected in the README, whose value is 1511. Also seen: arXiv:2603.02398, arXiv:2510.19787 and arXiv:2505.05896 (Kauers-Wood), arXiv:2511.20317 (ternary meta flip graphs) and arXiv:2506.22113 (commutative). None reports a value below 1511 for (13,13,14).
- matyasstoch/cloudroom-math README, the newest source in Perminov's CHANGELOG: its claims with max dimension 16 or less are only 4x6x15 at 261 and 9x11x11 at 710. There is no 13x13x14 entry.
- Neighbouring formats for scale: Lille 13x13x13 is 1426 and the Perminov table has 1421 (Q). MerlijnW70 has 13x13x15 at 1591. A rank of 1479 lies between them and is not a listed value.

## Comparison

Minimum over all sources for sorted (13,13,14): min(1511 digest, 1511 Lille, 1511 Perminov ZT/Z/Q, none in MerlijnW70, none in trophy case or open PRs, nothing lower in the literature) = 1511. The claimed rank 1479 is strictly below 1511, by 32. It is not a tie. This verdict covers novelty only; checking that the scheme is correct is another panelist's job.

verdict: PASS (novelty)

pass: true
