# Novelty check: <13,13,15> rank 1578 over Q

context: Claude Code subagent (Opus 5.5), fresh context

Role: novelty skeptic. Claim: object/13x13x15_r1578_Q.json, an exact scheme over Q for <13,13,15> with 1578 rank-one terms. Sorted format compared: (13,13,15). I did not run the scheme here. Exactness is the reproduce skeptic's job; this file covers novelty only.

Method: one plain curl GET per page, User-Agent "V3R1T4S-research (honest client; curl)", no retries. Every fetch returned HTTP 200 with no challenge page. Pages were saved in the panel's novelty_ws/ folder.

## Live sources

| # | Source | URL | UTC fetch time | HTTP | sha256 | Value read for sorted (13,13,15) |
|---|---|---|---|---|---|---|
| 1 | Lille digest fmm_sota.json (createdAt 2026-10-09T11:45:48, 5456 entries) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:20:50Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | `{"format": [13, 13, 15], "rank": 1605, "exponent": 2.825055}` |
| 2 | Lille per-format page (template https://fmm.univ-lille.fr/{n}x{m}x{p}.html) | https://fmm.univ-lille.fr/13x13x15.html | 2026-10-15T09:20:50Z | 200 | 3f01c282cb2debee57eb71774249022076cbb880bc7442be6ab40ac4225e8d44 | title line "Description of fast matrix multiplication algorithm: ⟨13×13×15:1605⟩", so rank 1605 |
| 3a | Perminov README status table | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:20:52Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | row `` | `13x13x15` |    1591     |     1591     |     1591     |   2.821701739   | ``, so ZT 1591, Z 1591, Q 1591, with no bracketed earlier values and no "(?)" marks. No row exists for 13x15x13 or 15x13x13. |
| 3b | Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T09:20:53Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | Only one entry names the format: "`13x13x15`: found scheme with `1605` multiplications;" in the 13.02.2026 section. The file never mentions 1591 or anything lower for this format. The 1591 most likely came in through the MerlijnW70 merges of 29/09/2026 and 02/10/2026; the CHANGELOG names those merges but not the formats. The only "1578" in the file is for `10x16x16`, a different format. Newest section: 09/10/2026. |
| 4 | MerlijnW70 fmm-schemes tree (39 paths, truncated=false) | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-15T09:20:53Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | Only one path is any permutation of (13,13,15): `schemes/13x13x15_m1591_ZT.json`. Rank 1591, read from the file name. |
| 5 | V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T09:20:53Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | No row for 13x13x15 in any axis order. The matrix-multiplication rows cover <15,16,16>, <14,15,15>, <13,14,14>, <14,14,15> and <13,14,15>. |
| 6 | V3R1T4S open pull requests (40 open) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T09:20:53Z | 200 | 7b69ba2e001ff158e1f3fb0fe924471fdac217f69257f01896d771c0351f197d | No PR title, body or branch names 13x13x15 in any axis order. The two FMM PRs are #130 (<13,15,15> rank 1763) and #149 (<4,6,7> additive complexity). Both are other formats. |

The hashes of sources 1, 2, 3a, 4 and 5 match the author's table-record exactly. Those pages have not changed since the author fetched them at 09:07 to 09:08Z.

## Lille construction text

The Lille page's "Algorithm definition" reads:

"The algorithm ⟨13×13×15:1605⟩ could be constructed using the following decomposition: ⟨13×13×15:1605⟩ = ⟨7×5×5:127⟩ + ⟨7×5×5:127⟩ + ⟨6×4×5:90⟩ + ⟨6×5×5:110⟩ + ⟨6×5×5:110⟩ + ⟨6×4×5:90⟩ + ⟨7×5×5:127⟩ + ⟨7×4×5:104⟩ + ⟨7×4×5:104⟩ + ⟨7×4×5:104⟩ + ⟨6×5×5:110⟩ + ⟨7×4×5:104⟩ + ⟨6×4×5:90⟩ + ⟨7×4×5:104⟩ + ⟨7×4×5:104⟩ ."

The Lille value is a block composition of 15 smaller schemes: 3×127 + 3×90 + 3×110 + 6×104 = 1605. The claim at 1578 is not this composition.

## Literature and web search (last 24 months, to 2026-10-15)

I ran four web searches: the exact format string in each axis order with "rank" and "scheme"; flip-graph arXiv papers from 2026 together with 13x13x15 and 1591; an extended search for the format with "2026 new scheme"; and the format with the candidate ranks 1578, 1580, 1585 and 1590.

What the searches covered:
- arXiv 2603.02398 (Perminov's open-source flip-graph framework)
- arXiv 2606.02480 (meta flip graph, named by the bank)
- arXiv 2510.19787 (Kauers and Wood, meta flip graph)
- arXiv 2502.04514 (flip graphs with symmetry)
- arXiv 2505.05896 (consequences of the Moosbauer-Poole schemes)
- arXiv 2506.22113 (commutative schemes via flip graphs)
- arXiv 2606.13408 (catalogue of FMM algorithms with exhaustive derivations)
- the 3x3 addition papers 2512.21980, 2604.27645 and 2609.06588
- the MerlijnW70 fmm-schemes release notes v1.0, v1.1 and v1.3
- Lille per-format pages that turned up in results

What I found: the lowest published rank for 13x13x15 is 1591, a ternary scheme. The fmm-schemes v1.3 release notes list it as "was 1605", and Perminov's table now carries it in all three columns. No search turned up any rank at or below 1590 for 13x13x15, 13x15x13 or 15x13x13. Nothing I saw lists 1578.

Limit: web search can miss a very recent preprint or an unindexed repository. The sources the bank names were all fetched live above.

## Verdict

Minimum over everything found: min(1605 sota, 1605 Lille, 1591 ZT, 1591 Z, 1591 Q, 1591 MerlijnW70, none in the trophy case, none in open PRs, none in the literature) = 1591. The claimed 1578 is 13 below that minimum, a strict improvement, not a tie. The Lille 1605 entry is a block composition, so it raises no composition objection to 1578.

novelty: PASS (1578 < 1591)
pass: true
