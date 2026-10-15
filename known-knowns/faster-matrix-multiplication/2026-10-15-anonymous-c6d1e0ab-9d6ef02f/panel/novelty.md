# Novelty review: 14x16x16, rank 2117 over Q

context: Claude Code subagent (Opus 5.5), fresh context

Role: novelty skeptic. I read only the claim folder (CLAIM.md, INDEX.csv, table-record/README.md, the object file name) and claim.SHA256SUMS. The claim is a rank-2117 exact scheme over Q for the format 14x16x16 (already in sorted order). The table value it says it beats is 2128.

Fetch method: one plain curl GET per page, User-Agent "V3R1T4S-research (honest client; curl)", no retries. Time from `date -u`, status from curl's http_code, sha256 of the saved body. Pages saved under the panel's novelty_ws/ folder. Every request returned 200. None was blocked or served a challenge page.

## Live sources

| # | Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|---|
| 1 | Sedoglavic digest | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T09:20:51Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | `{"format": [14, 16, 16], "rank": 2128, "exponent": 2.808914}`; this is the only entry whose sorted format is 14x16x16; digest createdAt 2026-10-09T11:45:48 |
| 2 | Lille per-format page (template https://fmm.univ-lille.fr/{n}x{m}x{p}.html) | https://fmm.univ-lille.fr/14x16x16.html | 2026-10-15T09:20:51Z | 200 | c8a6c116b6746ef25ca4eef0978d38943716a647e68fd6b7ff3e36965cb8aeb8 | Title: "Description of fast matrix multiplication algorithm: 14 x 16 x 16". Heading: "⟨14×16×16:2128⟩". Rank 2128 |
| 3a | Perminov README | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T09:20:52Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | Status row: ZT "2170 (?)", Z "2170 (?)", Q "2128 (2142)", ω 2.808914234. The bracket 2142 is the previous rank. The "New best ranks" table gives prev 2142 (Q), new 2128 (Q), file schemes/results/Q/14x16x16_m2128_Q.json. Minimum 2128 |
| 3b | Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T09:20:52Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | Only 14x16x16 entry, under "09.05.2026": "14x16x16: found scheme with 2128 multiplications (Q)". Latest section is 09/10/2026 (matyasstoch cloudroom-math schemes); it has no 14x16x16 line. No mention of 2117 or of any rank below 2128 |
| 4 | MerlijnW70 fmm-schemes tree | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-15T09:20:52Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 paths, truncated false. No file for 14x16x16 or any permutation. The nearest files are 13x14x16_m1805_ZT, 10x14x16_m1416_ZT and 9x14x16_m1260_ZT |
| 5 | V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T09:20:53Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | No 14x16x16 row in any axis order, and no 2117. The matrix-multiplication rows are 15x16x16 rank 2180, 14x15x15 rank 1842, 13x14x14 rank 1558, 14x14x15 rank 1716 and 13x14x15 rank 1677 |
| 6 | V3R1T4S open PRs | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T09:20:53Z | 200 | 7b69ba2e001ff158e1f3fb0fe924471fdac217f69257f01896d771c0351f197d | 40 open PRs. A case-insensitive scan of the whole response for 14x16x16, 16x14x16 and 16x16x14 found 0 hits, and no title or body pattern matched 14,16,16 or 2117. The two FMM PRs are #130 ((13,15,15) rank 1763) and #149 (4x6x7 additive complexity). Neither concerns this format |

### Lille construction text

The page has no separate "construction" entry for this format. The page does not describe the scheme as a composition, padding or block-split. Its provenance text, verbatim:

> Algorithm definition The algorithm ⟨14×16×16:2128⟩ is taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026. [ GitHub repository ]

Below that are links to the maple tensor, LRP and raw .mpl.bz2 files. The page also shows an "Algorithm type" polynomial.

The README, Lille page, digest, MerlijnW70 tree and trophy-case hashes are byte-identical to the hashes in the claim's table-record. Those sources have not changed since the author's 2026-10-14T18:44Z fetch.

## Literature and web search (last 24 months, any axis order)

What I searched:
- Web searches: "14x16x16 matrix multiplication rank scheme"; the format written as 14×16×16 and 16x16x14; "14x16x16" with 2117, 2120, 2125 and 2127; 2026 flip-graph and new-record queries for rectangular formats up to 16.
- A search for the matyasstoch cloudroom-math repository named in the CHANGELOG. It found nothing indexed.

What I checked:
- arXiv:2606.02480v2. Perminov, "Meta Flip Graph meets Serendipitous Product: new Fast Matrix Multiplication results", submitted 05 Jun 2026. Its Table 2 row reads "14×16×16 | 2142 | 2128 | ℚ | 2.809" (previous 2142, new 2128). This is the source of the current 2128.
- arXiv:2603.02398. Perminov, open-source flip graph framework, Mar 2026. It covers the 680 formats up to 16x16x16. No value below 2128 surfaced for this format.
- arXiv:2606.13408v1. The matmulcatalog article, Jun 2026, draft dated Aug 2026. The part I read (about the first 100,000 of 213,545 characters) has no 14x16x16 entry, and nothing in it is below 2128.
- Also seen, none with a 14x16x16 value below 2128:
  - arXiv:2511.20317 (ternary meta flip graphs)
  - arXiv:2510.19787 (Kauers and Wood, meta flip graph)
  - arXiv:2602.11041 (Kauers, Moosbauer and Wood)
  - arXiv:2502.04514 (flip graphs with symmetry)
  - arXiv:2506.22113 (commutative schemes)

Result: no published or posted rank at or below 2117, and none below 2128, for 14x16x16 in any axis order. The best known value everywhere I looked is 2128 over Q (Perminov, 2026). The cited ternary/integer value is 2170. The previous rank was 2142.

## Verdict

- Minimum over everything found: 2128 (fmm_sota.json, the Lille page, and the Perminov README Q column all give 2128). MerlijnW70 has no 14x16x16 file. The trophy case and open PRs have no entry for this format. The literature shows nothing at or below 2128.
- Claimed rank: 2117. That is 11 below 2128, so it strictly beats the minimum. This is not a tie.
- Scope: this checks novelty only. Whether the scheme is correct is for the other panelists.

novelty: PASS (2117 < 2128)
pass: true
