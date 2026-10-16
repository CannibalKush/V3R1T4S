# Novelty check: 13x15x15 rank 1762 over Q

context: Claude Code subagent (Opus 5.5), fresh context

Role: NOVELTY skeptic. Claim checked: an exact scheme over Q for format 13x15x15 (sorted 13,15,15) with 1762 rank-one terms. The bar is 1763, the merged V3R1T4S package (pull request #130).

Every page below was fetched once with curl, User-Agent 'V3R1T4S-research (honest client; curl)'. There were no retries. The time is from `date -u`, the status is from curl's `%{http_code}`, and the sha256 is of the saved page.

## Live sources

| # | Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|---|
| 1 | Sedoglavic digest | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T21:02:19Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | `{ "format": [13,15,15], "rank": 1776, "exponent": 2.812457 }` (createdAt 2026-10-09T11:45:48) |
| 2 | Lille per-format page (template https://fmm.univ-lille.fr/{n}x{m}x{p}.html) | https://fmm.univ-lille.fr/13x15x15.html | 2026-10-15T21:02:19Z | 200 | ce3fdb838b44413ff5b4b6d7a94ae09b6581254148141ddae788c7aa2cd68ee7 | Title: "Description of fast matrix multiplication algorithm: 13 x 15 x 15"; heading rank ⟨13×15×15:1797⟩ |
| 3a | Perminov README | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T21:02:21Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | Status row: `13x15x15 / ZT 1797 (?) / Z 1797 (1803) / Q 1776 (1803) / 2.812456688`. New-best-ranks row: `13x15x15 / prev 1803 (Z) / new 1776 (Q)`. Minimum over ZT/Z/Q, brackets included: 1776 |
| 3b | Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T21:02:21Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | Lowest entry for 13x15x15: 26/09/2026 "found scheme with 1776 multiplications (Q)". Earlier entries are 1797 (ZT, Z) and 1803. The newest entry (09/10/2026, cloudroom-math schemes) has no 13x15x15 line |
| 4 | MerlijnW70 fmm-schemes tree | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-15T21:02:21Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | truncated=false, 39 paths. No file for sorted format 13,15,15 in any axis order |
| 5 | V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T21:02:22Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | No 13x15x15 row, and no 1763 or 1762. The matrix-multiplication rows are 14x15x15, 13x14x14, 15x16x16, 14x14x15 and 13x14x15. The file had not yet been regenerated after #130 |
| 6 | V3R1T4S open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T21:02:22Z | 200 | 70096953df06d2cebcf7483fe05152290fa32919027f4ce31d440ab4e8dfe25a | 10 open pull requests: #195, #194, #193, #192, #191, #190, #154, #153, #30 and #9. None names 13x15x15 (in any order), 1762 or 1763 in its title or body. None is a matrix-multiplication claim |
| 7 | V3R1T4S merged FMM packages | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-15T21:02:23Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 29 entries. They include package 2026-10-14-anonymous-c6d1e0ab-710c8ff6 (#130), 19 further c6d1e0ab packages dated 2026-10-15, and one drzuzzjen package |
| 7b | Family INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-15T21:03:28Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | Project rows cover only 14x15x15, 13x14x14, 15x16x16, 14x14x15 and 13x14x15. There is no 13x15x15 row |
| 7c | V3R1T4S full repository tree | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-10-15T21:03:28Z | 200 | c819b82d816f07c1a3fbc4476607bf0b7225e00cd836a3fd2a72c845d28f8eb4 | truncated=false, 2497 paths. The only paths for sorted format 13,15,15 are in the #130 package: `object/13x15x15_r1763_Q.json` and `how-we-built-it/make_result_13x15x15.py`. Merged minimum: 1763 |
| 8 | Comments on issue/PR #164 | https://api.github.com/repos/elder-plinius/V3R1T4S/issues/164/comments | 2026-10-15T21:02:23Z | 200 | 5fe60089c10f79dc73e4cb2b8d8133c6be9b6be3664172528fc1326a710a9460 | One comment, quoted below |

Rows 7b and 7c were extra single fetches. They were needed to read the formats inside the merged packages, because the directory listing gives only folder names.

### Lille construction text (verbatim)

"Algorithm definition The algorithm ⟨13×15×15:1797⟩ is taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026. [ GitHub repository ]"

The page has no composition, padding or block-splitting decomposition for this format. It lists only the algorithm-type polynomial and the Maple downloads.

### Maintainer comment on #164 (verbatim)

By elder-plinius (OWNER), 2026-10-15T18:41:19Z:

> Merged, thank you! Two independent exact checkers (rational and big-integer, no modular shortcuts, none of the package's code run) confirm all Brent equations for ⟨13,13,14⟩ at rank 1479. The live catalogues give 1511, so the gain is 32.
>
> Also worth knowing: the build log for #164 shows an unpublished ⟨13,15,15⟩ rank-1762 scheme, one below the merged #130. Feel free to submit it.
>
> _Reviewed with Claude on the maintainer's behalf._

## Literature search (last 24 months, October 2024 to October 2026)

I ran web and arXiv searches for: "13x15x15 matrix multiplication rank scheme"; "13x15x15" / "⟨13,15,15⟩" / "13×15×15" with 1776, 1763 or 1762; 2026 flip-graph and LITA papers on rectangular formats up to 16; LITA (Khoruzhii, Serafin, Gelß, Pokutta); arXiv 2606.13408; and cloudroom-math. Papers and pages surfaced:

- arXiv:2603.02398 (Perminov, open-source flip-graph framework)
- arXiv:2606.02480 (meta flip graph meets serendipitous product)
- arXiv:2510.19787 (Kauers and Wood, meta flip graph)
- arXiv:2511.10786 (Khoruzhii, Gelß, Pokutta, structured matrix multiplication)
- arXiv:2602.11041
- arXiv:2606.13408 (a machine-checkable catalogue up to 32x32x32, submitted 14 Aug 2026)
- arXiv:2505.05896
- neighbouring Lille pages (13x13x15, 14x15x15, 15x15x15, 13x15x18)

None of them reports a rank at or below 1762 for 13x15x15 in any axis order. The public results for this format all feed the catalogues above: 1803 and 1797 (Perminov), then 1776 (Perminov, from the LITA schemes, 26 Sep 2026).

The open-PR search covered all 10 open pull requests: none is for this format. The repository search covered TROPHY_CASE.md (no row), the merged known-knowns family (only #130 at 1763) and the full main tree (no other 13x15x15 file).

## Verdict

Everything found, as minima for sorted format 13,15,15:

- fmm_sota.json: 1776
- Lille page: 1797
- Perminov ZT/Z/Q: 1797 / 1797 / 1776
- MerlijnW70: none
- TROPHY_CASE.md: none
- open PRs: none
- merged V3R1T4S package #130: 1763
- literature: nothing below 1776

The minimum is 1763. The claim's 1762 is strictly below 1763, by 1. This is a strict improvement, not a tie. No source holds a rank of 1762 or lower.

The maintainer's own comment on #164 calls this scheme unpublished and one below #130. That fits with it being new, but it is not evidence that the scheme is correct. Correctness is for the other skeptics to check.

novelty: PASS (1762 is below 1763, the minimum of all live sources and merged packages)

pass: true
