# Novelty skeptic: <11,13,16> rank 1445 over Q

context: Claude Code subagent (Opus 5.5), fresh context

## What was tested

- Claim (from `claim/CLAIM.md`): `object/11x13x16_r1445_Q.json` is a bilinear scheme over Q for <11,13,16> with 1445 rank-one terms. The claim says the best listed rank is 1446.
- Claim files read: `CLAIM.md`, `INDEX.csv`, `table-record/README.md`. Their sha256 values match `claim.SHA256SUMS` (4cd097b7..., 5109bded..., 304c22bb...). The object was not opened; only its file name was noted. Its listed sha256 is d2d1c96812918b46fa34436c66cdd27e51383b12a9686a975d715d69e6480c75.
- Rank does not change when the three dimensions are permuted, so every source was searched for all six orders (11x13x16, 11x16x13, 13x11x16, 13x16x11, 16x11x13, 16x13x11).

## How the pages were fetched

- Tool: curl 8.7.1 with User-Agent `V3R1T4S-research (honest client; curl)`.
- One plain GET per page. Redirects were not followed. No cookies. No proxy (`--noproxy '*'`; no proxy variables were set). No retries.
- The UTC time comes from `date -u`, taken just before each request. The status comes from `curl -w '%{http_code}'`. Each saved body was hashed with `shasum -a 256`.
- Pages are saved under `novelty_ws/`; the full log is `novelty_ws/fetch_log.tsv`.
- All 28 requests returned 200. None returned 401, 403, 429 or 503, and none was a challenge page: both Lille pages are the expected catalogue HTML with no challenge markers.

## Sources named by the success criterion (plus the CHANGELOG)

| Source | URL | UTC fetch time | HTTP | sha256 of saved page | Exact value read for this format |
|---|---|---|---|---|---|
| Lille JSON digest | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-14T16:58:44Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | `{ "format": [11,13,16], "rank": 1446, "exponent": 2.822036 }`. This is the only entry for this sorted format. createdAt 2026-10-09T11:45:48; 5456 entries. |
| Lille per-format page | https://fmm.univ-lille.fr/11x13x16.html | 2026-10-14T16:58:45Z | 200 | ed06d78d6cf1be521a165983746e0954af6fb92e4e679eda7136a8b1da236546 | `⟨11×13×16:1446⟩`, "taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026." (Last-Modified Sat, 06 Jun 2026 11:15:07 GMT) |
| Lille main table (the claim's "Status source") | https://fmm.univ-lille.fr/ | 2026-10-14T17:10:20Z | 200 | d1580ec77377c36e3e21c66e51aa9b24c3c9a2544e0152395136bbee7816d627 | Row `id="11x13x16"`: `⟨11×13×16:1446⟩`, fast_tensor_rank 1446, classical 2288, "Perminov 2026" (Last-Modified Fri, 09 Oct 2026 15:35:36 GMT). No other order of the format appears. |
| Perminov README, "Research Findings & Status" table | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-14T16:58:46Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | `` `11x13x16` \|  1458 (?)   \| 1458 (1472)  \| 1446 (1472)  \|   2.822035717 ``, so ZT 1458, Z 1458, Q 1446; the minimum is **1446**. The "New best ranks" row gives previous 1472 (Z) and new 1446 (Q), file `schemes/results/Q/11x13x16_m1446_Q.json`. |
| Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-14T16:58:47Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | Two entries for this format. 12.02.2026: "`11x13x16`: found scheme with `1452` multiplications (`Q`)". 03.04.2026: "`11x13x16`: found [scheme](schemes/results/Q/11x13x16_m1446_Q.json) with `1446` multiplications (`Q`)". No later entry for this format. The newest entry (09/10/2026, schemes imported from matyasstoch/cloudroom-math) does not touch it. |
| MerlijnW70 fmm-schemes, file list via GitHub API | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-14T16:58:47Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | Tree e4c499ff6bd5ac7d7d58d35eccce9947c56888ec (not truncated, 39 entries) holds 31 scheme files and **none for any order of 11x13x16**, so this source gives no value. Two follow-up fetches agree. The repo metadata (https://api.github.com/repos/MerlijnW70/fmm-schemes, 2026-10-14T17:01:41Z, 200, eb13d56644a7379614b7485866ed96916b7c551f594a02afc69c409713638be1) shows default branch main, last pushed 2026-09-30T13:42:30Z. The README (https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/README.md, 2026-10-14T17:01:41Z, 200, 6ef17ff86e9a74b710e4e6173f67187b735ecdef760d2634a16d33bdf73b904b) has no 11×13×16 row. |

**Minimum over the criterion sources: 1446** (fmm_sota.json 1446, Lille 1446, Perminov min(ZT,Z,Q) = 1446, MerlijnW70 none). These values match the author's `table-record/README.md` exactly.

## Other sources checked for this format

| Source | URL | UTC | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| matmulcatalog COVERAGE.md (bank-named; F2 column) | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-14T17:01:44Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | `` `⟨11,13,16⟩` \| **✓ 1458** Dronperminov-ZT [Z→F₂] \| **✓ 1446** Dronperminov-Q \| — \| — \| **1446** in R/Q/Z ``. That is F₂ 1458; best over any field 1446. |
| Perminov repository, full file tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-14T17:01:44Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | Tree f0efd4f6... (6637 entries, not truncated). Scheme files for this format: `11x13x16_m1446_Q`, `11x13x16_m1452_Q`, `11x13x16_m1458_ZT`, `11x13x16_m1460_ZT`, plus `schemes/known/tensor/11x13x16_tensor.mpl`. The lowest is 1446. |
| Perminov repository, open pull requests | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/pulls?state=open&per_page=100 | 2026-10-14T17:07:51Z | 200 | 953c527e335e70ba978e7f3c62053743a7ff330fb56ade8659f4bb9f069deb2f | There is one open PR (#6, additions for the 3x4x5 rank-47 scheme). It is not about this format. |
| MerlijnW70/FastMatrixMultiplication (a fork of Perminov's repo) | https://api.github.com/repos/MerlijnW70/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-14T17:08:01Z | 200 | 10a733f6f00dc2f70a3b9f76990ff80251fc2e1501eaeb06b859076897174b10 | Same four files as upstream; the lowest is 1446. Its metadata (17:07:51Z, 200, 013808e2460eda0c3c81caa554b96f5410e881d591ee96846ce36c9dfdf650b0) shows last push 2026-09-29. |
| matyasstoch/cloudroom-math (imported by Perminov 09/10/2026) | https://api.github.com/repos/matyasstoch/cloudroom-math/git/trees/main?recursive=1 | 2026-10-14T17:02:40Z | 200 | 9af3b97c700fa9bcc7be6065033b48b40464816bc48cfc55ebc5279ffa00cf6e | No file for this format (99 entries). Its README (17:03:33Z, 200, 5d97910225ed2ff9e5a8de65af12d87d8d5f58ebebefc671c1dcd5e0d6ad64a1) does not mention it. Metadata: 17:02:30Z, 200, d36a2913...; last push 2026-10-08. |
| khoruzhii/lita (LITA) | https://api.github.com/repos/khoruzhii/lita/git/trees/main?recursive=1 | 2026-10-14T17:02:41Z | 200 | d923a68888fc427aa8e9d216c6e54d45eb078afb8718ea55ae4990f443b89339 | Square schemes only (13³ through 32³). The README (17:03:09Z, 200, 97df246f15643a7396307765d23432d03bcb5af97a9f8bf92cae85cb428d5b3f) lists squares only and says the manuscript is "in preparation". It gives no rectangular value. Metadata: 17:02:31Z, 200, 499291ee...; last push 2026-10-07. |
| dronperminov/ternary_flip_graph (bank-named) | https://api.github.com/repos/dronperminov/ternary_flip_graph/git/trees/master?recursive=1 | 2026-10-14T17:03:45Z | 200 | 2648d91c889344150c9672d127fda436658d8dd60cbadbef144398fb82d851d3 | Code only; no scheme for this format. Metadata: 17:03:33Z, 200, b302b2b0.... |
| jakobmoosbauer/flips (bank-named) | https://api.github.com/repos/jakobmoosbauer/flips/git/trees/main?recursive=1 | 2026-10-14T17:03:46Z | 200 | e6d1422bd46033780a5885723c561bd5161ab290e526bff14d1ab35642636e8e | Formats up to 6x6x6 only; nothing for this format. Metadata: 17:03:33Z, 200, 54acf7b4.... |

I also checked whether the tables have missed a trivial construction. Splitting one dimension of <11,13,16> into two blocks and using the digest's own ranks, the best bound is 1454 = R(11,1,16) 176 + R(11,12,16) 1278. That is above 1446, so the listed 1446 is not stale against simple splits.

## This repository: TROPHY_CASE.md and pull requests

| Source | URL | UTC | HTTP | sha256 | Finding |
|---|---|---|---|---|---|
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-14T16:58:48Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | Five matrix-multiplication rows: <15,16,16> 2180, <14,15,15> 1842, <13,14,14> 1558, <14,14,15> 1716, <13,14,15> 1677. **None is for <11,13,16>** or any reordering of it. |
| Open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-14T16:58:48Z | 200 | 3d5ee004ac3902500a41fb55373702859608cd06d1dfa3b1965226021997e5df | 25 open PRs on one page (no Link header). The only claim on this target is #130, (13,15,15) rank 1763. **No PR title, body or branch mentions any order of 11x13x16.** |
| Repository file tree (extra) | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-10-14T17:01:46Z | 200 | 2f18e1394f1e4df5803b20591b88b66a68bb3512f647df54ce6e01140b77ef54 | Tree 9b1d444e... (609 entries): no file names any order of 11x13x16. |
| Closed pull requests (extra) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=closed&per_page=100 (and `&page=2`) | 2026-10-14T17:08:24Z / 17:08:38Z | 200 / 200 | 9a9a92ba4ba5a2173672b398d2dc4ef547d1477b98aae1fcf485ca2cf74630c8 / bab0f28dbbe6f113839420400deba096dc0a4cfe6302ca3a07cb7a4329a8d11e | 115 closed PRs. They include 19 claims on this target, all unmerged, and none is for (11,13,16). |

## Literature search (last 24 months, 2024-10-14 to 2026-10-14)

Coverage:
- An arXiv title search for "matrix multiplication", newest first, read in full; it reaches back to March 2026.
- A date-filtered arXiv advanced search over 2024-10-14 to 2026-03-15 (160 results), read in full.
- Web searches for: "11x13x16" matrix multiplication rank; 11×13×16 with 1445 or 1446; "11x13x16" / "11×13×16" / "<11,13,16>" on GitHub; "1445" with matrix multiplication; 2026 rectangular rank upper bounds up to 16; Kauers–Wood; arXiv 2606.02480; LITA; October 2026 records.
- Full-text checks of the papers listed below.

Found:
- Two papers give a value for this format, both by A. I. Perminov:
  - arXiv:2603.02398v1 (2 Mar 2026), Table 1: "11×13×16 | 1472 | ℤ | 1452 | ℚ".
  - arXiv:2606.02480v2 (5 Jun 2026), Table 2: "11×13×16 | 1452 | 1446 | ℚ | 2.822".
- These papers were checked and give no value for this format:
  - 2606.13408v3 (Chatain Lacelle, 14 Aug 2026), a catalogue up to 32. It reports strict improvements only for 17 ≤ max dimension ≤ 32 and says formats up to 16 are saturated.
  - 2510.19787 (Kauers–Wood, Oct 2025): largest dimension 8.
  - 2602.11041v3 (Kauers–Moosbauer–Wood): exponents for small formats.
  - 2505.05896 (Kauers–Wood, May 2025): largest dimension 7.
  - 2502.04514 (Moosbauer–Poole): 5x5 and 6x6.
  - 2511.20317 (Perminov, ternary meta flip graphs): up to dimension 12.
  - 2508.01748 (Schwartz–Zwecher): large square formats.
  - 2511.10786: structured matrix multiplication.
  - 2506.13131 (AlphaEvolve): the abstract covers 4x4.
  - The Sep–Oct 2026 arXiv batch: 3x3 addition counts, lower bounds, exponent papers, and an F₂ GPU search at 7x7.
- **No source, in any order of the dimensions and over any ring, gives a rank of 1445 or lower for <11,13,16>.** Every other value found is higher: 1446 (Q, the record), 1452 (Q), 1458 (ZT, Z, F₂), 1460 (ZT), and 1472 (Z, the earlier record).

## Verdict

novelty: PASS. 1445 is strictly below the best known 1446 (over Q; Perminov, found 03.04.2026, published in arXiv:2606.02480). The margin is one multiplication, so this is not a tie.

Limits:
- The margin is the smallest possible.
- The result holds as of the fetch times (2026-10-14T16:58:44Z to 17:10:20Z). These tables have been changing within days of each other.
- This check covers novelty only; I did not open or verify the scheme.
- Not covered: GitHub-wide code search (it needs authentication), social media, and unpublished work. For example, the LITA rectangular restrictions are not published.

pass: true
