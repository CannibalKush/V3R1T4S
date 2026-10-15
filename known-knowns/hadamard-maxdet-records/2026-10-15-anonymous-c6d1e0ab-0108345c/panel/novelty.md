# Novelty skeptic report: maxdet-109 (`hadamard-maxdet-records`, n = 109)

context: Claude Code subagent (Opus 5.5), fresh context

## What I read and what was claimed

- I read only `claim/CLAIM.md`, `claim/table-record/` (`README.md`, `sources_2026-10-14T08-11-00Z.json`), the file name in `claim/object/`, and `claim.SHA256SUMS`. The sha256 values of CLAIM.md and both table-record files match `claim.SHA256SUMS`. I did not open the object file, REPRODUCE.md or verify-it-yourself/. Whether the determinant is correct is outside this report, so I take the value as claimed.
- The claimed value is |det| / 2^108 = 291 * 27^53 = 2119202655125403624550373680790052808829003860176536932438843923020304438454497, about 2.119202655E78. I checked that 291 * 27^53 equals this integer exactly (Python integers).
- 109 = 4*27 + 1, so n ≡ 1 mod 4 and the bound for this residue class is Barba's.

## Normalization and conversion

- Every value below is compared as D = |det| / 2^(n-1) = |det| / 2^108.
- Archived MaxDet table: page3 says "Det should be multiplied by 2^(N-1)", and key.html says an N×N sign matrix "has the stated maximum multiplied by 2^(N-1)". The table entry is therefore already D, and the conversion factor is 1.
- Math-AI-Caltech CSV: its README defines column `D` as |det X| / 2^(n-1). This is the same normalization.
- Cross-check: the Barba bound divided by 2^108 is sqrt(217) * 108^54 / 2^108 = sqrt(217) * 27^54, about 2.896497323E78. Dividing the archived 1.877483842E78 by this gives 0.6482, which matches the table's R column ("R .65", the ratio to the bound for that residue class). This confirms the normalization.

## How pages were fetched

Each page got one plain `curl` GET with User-Agent `V3R1T4S-research (honest client; curl)`. Redirects were followed with `-L` and are recorded below. There were no retries, no cookies and no proxy (`--noproxy '*'`). The UTC time was taken from `date -u` just before each request, the status from `-w '%{http_code}'`, and the sha256 from `shasum -a 256` of the saved body. Pages are saved under `novelty_ws/<label>/`, and the full log is `novelty_ws/fetch_log.tsv`. No fetch returned 401, 403, 429 or 503, and none hit a challenge page or a connection failure.

## Criterion sources for n = 109

| label | URL requested (final URL if redirected) | UTC fetch time | HTTP | sha256 of saved page | value read for n = 109 |
|---|---|---|---|---|---|
| 01_repo_meta | https://api.github.com/repos/Math-AI-Caltech/hadamard-maxdet | 2026-10-14T16:15:43Z | 200 | c38500e751c57e0f51884415d3ba7280fea05cb2550bbfdd040f3fde27387be3 | n/a (metadata: default branch `main`, pushed_at 2026-09-07T20:57:09Z) |
| 02_repo_tree | https://api.github.com/repos/Math-AI-Caltech/hadamard-maxdet/git/trees/main?recursive=1 | 2026-10-14T16:15:58Z | 200 | 5d9f96c749ee51107a5de1024eee900d85beea102ed441caa22fc552fd060979 | n/a (5 files; the only data file is `maxdet_records.csv`; tree not truncated) |
| 03_repo_csv | https://raw.githubusercontent.com/Math-AI-Caltech/hadamard-maxdet/main/maxdet_records.csv | 2026-10-14T16:16:11Z | 200 | 884d99a5b8ffd1a699a1f90b2f46b429323e7fc6fe3a037706dff5d8117ff2c9 | **no row for n = 109**. Rows are n = 51, 103, 107, 111, 115, 119, 115, so there is no `D` and no `D_prev` for 109 |
| 04_repo_readme | https://raw.githubusercontent.com/Math-AI-Caltech/hadamard-maxdet/main/README.md | 2026-10-14T16:16:12Z | 200 | a445d9670ccb33c604865f9e19d5dc4b1487fee1c616e5ab6223a5feaaea4abd | **none**. Its title and verification table cover only 51, 103, 107, 111, 115, 119. It gives the `_prev` source as `http://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/` |
| 05_orrick_wayback_index | http://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/ (final: https://wayback.archive-it.org/219/20190314205221/http://www.indiana.edu/~maxdet/, 2 redirects; memento 14 Mar 2019 20:52:21 GMT) | 2026-10-14T16:16:25Z | 200 | 1652f8b93f67c97cf7c2bfdf450b851c3025da578c6bbdd91c3c12c14b8d514d | not on this page (its table covers orders 0-39 and links to `page3.shtml` for 80-119). The page reads "Last modified 17 October 2012" and notes the Backstrom programming contest (ended 3 April 2005) and Rokicki's records |
| 06_orrick_wayback_page3 | https://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/page3.shtml (final: .../219/20190315055615/..., 1 redirect; memento 15 Mar 2019 05:56:15 GMT) | 2026-10-14T16:16:58Z | 200 | e7fffdbe1b10f48e9f2b57316022aaac75dce4b5ba0985e82d4f7d81d1029a98 | **N = 109: `1.877483842E78 ??`, R `.65`** ("??" = "not been proved maximal", per key.html) |
| 07_orrick_wayback_d109 | https://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/d109.html (final: .../219/20190316001217/..., 1 redirect) | 2026-10-14T16:17:39Z | 200 | 887f1614c55cb969b968d67e78e54648b19c6ae759d899e457a9841fe8a595ee | no number; "Matrix found by Tomas Rokicki", page created and last modified 12 April 2005 |
| 08_orrick_wayback_key | https://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/key.html (final: .../219/20190315055540/..., 1 redirect) | 2026-10-14T16:17:40Z | 200 | 300955fec214488bad07987120ef5ce34c441d14f28b43c117ea7a9e59dd9295 | n/a (definitions of Det, R and "??", quoted above) |
| 09_rokicki_newrec_wayback | https://wayback.archive-it.org/219/20190316001217/http://tomas.rokicki.com/newrec.html (link from d109) | 2026-10-14T16:17:57Z | 404 | 765bec8caffbacb0eae95ec76a0c4c19ad702f842253a827f47772ad7a928097 | none (not captured in collection 219; supplementary, not a criterion source, not retried) |
| 10_arxiv_abs_2608.22518 | https://arxiv.org/abs/2608.22518 | 2026-10-14T16:18:09Z | 200 | 8aa955cef9b47849f450b118da542b8333a5e07c6ee70e93890b3d4575799a7a | none. The latest version is **v3 (Thu, 1 Oct 2026)**, after v1 (23 Aug) and v2 (31 Aug). The abstract covers n = 51 and n ≡ 3 mod 4 in 103-119 only |
| 11_arxiv_html_2608.22518v3 | https://arxiv.org/html/2608.22518v3 | 2026-10-14T16:18:17Z | 200 | ed31ecc98caead7d86d22447a70f8219e9c99048569ca1cc07c935ad4fee0bb6 | **none**. The only "109" in the text is a citation volume ("Mathematische Annalen 109"). The paper cites "Orrick, 2012" as its prior-record source |
| 17_repo_branches | https://api.github.com/repos/Math-AI-Caltech/hadamard-maxdet/branches?per_page=100 | 2026-10-14T16:25:11Z | 200 | e0ab826ecb02243a52624c009e461f9cc0cd9fdd1b127b62f259ae42d10d9fea | none (only branch: `main`) |
| 18_repo_issues_all | https://api.github.com/repos/Math-AI-Caltech/hadamard-maxdet/issues?state=all&per_page=100 | 2026-10-14T16:25:12Z | 200 | 2ba33ca0557f1bb5b7ba88d67f9d0093c7185a36ec51fe2b7bd9372d3e001d6d | none (0 issues or PRs in any state) |

EinsteinArena is the remaining source the criterion names, but it names only the **order-51** leaderboard, so it cannot supply an n = 109 value. I did not fetch it. A domain-restricted web search found no order-109 problem there.

The primary status source in CLAIM.md is the Math-AI-Caltech repository. Fetched at 2026-10-14T16:16:11Z from https://raw.githubusercontent.com/Math-AI-Caltech/hadamard-maxdet/main/maxdet_records.csv, it lists no value for order 109. The value that actually stands for n = 109 is the archived MaxDet entry 1.877483842E78, read at 2026-10-14T16:16:58Z from https://wayback.archive-it.org/219/20190315055615/http://www.indiana.edu/~maxdet/page3.shtml.

## Checks in this repo (V3R1T4S)

| label | URL | UTC fetch time | HTTP | sha256 | finding for n = 109 |
|---|---|---|---|---|---|
| 12_v3r1t4s_trophy_case | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-14T16:18:55Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | no hadamard-maxdet row and no Hadamard or determinant entry at all. The only "109" is in an unrelated codes row (LP optimum 26784/109) |
| 13_v3r1t4s_open_prs | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-14T16:18:55Z | 200 | a84f49feb658469f9fded0612b36fba64ab42987c4b05c04fe979e64b142446f | 25 open PRs on a single page (no Link header). None mentions maxdet, Hadamard, a determinant or order 109 in its title, body or branch |
| 20_v3r1t4s_search_all_prs | https://api.github.com/search/issues?q=repo%3Aelder-plinius%2FV3R1T4S+is%3Apr+hadamard+OR+maxdet+OR+determinant&per_page=100 | 2026-10-14T16:25:41Z | 200 | 9aa12ef17a138ebe0f12da00ebbedd489b1399438411b7a31b604fdcf575ba2e | 5 PRs, all closed: #65 (n = 109), #66 (n = 105), #67 (n = 117), #68 and #69 (p2 Gram targets, n = 49 and 81). Only #65 concerns n = 109 |
| 21_v3r1t4s_pr65 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/65 | 2026-10-14T16:26:09Z | 200 | c02416247c8612dd8bdb3d6589939d29f145f24df5150fa78b88bea69237815b | **the same claim, not independent prior art.** The body gives object SHA-256 `0108345c2f3cbffdd58f23eef8aba73546583f02062a013a5b64ab95e198faa6`, identical to `claim.SHA256SUMS`. The branch is `claim/2026-10-14-anonymous-c6d1e0ab-0108345c`. Created 08:24:49Z, closed 12:51:03Z, not merged |
| 22_v3r1t4s_pr65_files | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/65/files?per_page=100 | 2026-10-14T16:26:10Z | 200 | 02ab24ae9d0db8349cdc353345506cedcf7f856db49ce106d444f1acbbee8117 | adds the same object file name under `known-knowns/hadamard-maxdet-records/`. I read file names only, not the earlier panel's files |
| 23_v3r1t4s_pr65_comments | https://api.github.com/repos/elder-plinius/V3R1T4S/issues/65/comments?per_page=100 | 2026-10-14T16:26:11Z | 200 | 2ba33ca0557f1bb5b7ba88d67f9d0093c7185a36ec51fe2b7bd9372d3e001d6d | 0 comments |

Nothing merged into this repo covers order 109. The only other public posting of this value is PR #65, which is the same object.

## Literature search (window 2024-10-14 to 2026-10-14, plus the canonical older sources)

arXiv API, one curl request per query, sorted newest first:

| label | query | UTC fetch time | HTTP | sha256 | coverage and finding |
|---|---|---|---|---|---|
| 14_arxiv_api_maxdet | abs "maximal determinant(s)" OR "maximum determinant" OR "Barba bound" OR "Ehlich" OR ti "D-optimal" | 2026-10-14T16:19:50Z | 200 | e5dafad45e72b432ee331d95db1154d4ffe9fcb28284b7d4d16a50f03b511c33 | 136 hits. The first page of 100 spans the whole window. The only ±1 records paper is 2608.22518 (n = 51 and n ≡ 3 mod 4). Others concern roots of unity (2503.11114), complex matrices (2404.09040) or statistical D-optimal designs. No n = 109 value |
| 15_arxiv_api_hadamard | broad: Hadamard AND (determinant OR excess), "large determinant", sign/binary matrices AND determinant | 2026-10-14T16:20:10Z | 200 | d98c6f2e40cd5bf2b2aaaba17ce9b9387fc845b2c0bffc7d485571b0a7d5e748 | 949 hits, so the first page only reaches back to 2026-05-25 (supplementary). Filtered: no ±1 maxdet result other than 2608.22518 |
| 16_arxiv_api_hadamard_excess_det | ("Hadamard matrix/matrices" OR "sign matrix/matrices") AND (excess OR determinant(s)) | 2026-10-14T16:20:43Z | 200 | f8f4bbf66e4d1aeb89d9907889dd383eb2a075c026b3c4f3dff9ff2f6425af2c | 112 hits; the first page spans the whole window. Nothing on order-108 excess or order-109 determinants. 2510.06489 is about large-excess quaternary (complex) Hadamard matrices |
| 19_arxiv_api_mathCO_determinant | cat:math.CO AND determinant (stemmed, so it also matches "determine") | 2026-10-14T16:25:17Z | 200 | 4f442bc7331df30d367adfcac53e61004ac36c3e373cbdcd857a48bc5890e958 | 200 newest entries, 2026-09-23 to 2026-10-14. No ±1 maximal-determinant paper appeared after 2608.22518v3 |

Web searches (WebSearch) covered:

- order 109 directly, including the equivalent 108×108 0/1-matrix phrasing;
- "new records" in 2025-2026, and records for n ≡ 1 mod 4 near the Barba bound;
- AI-driven efforts (AlphaEvolve, FunSearch, OpenEvolve, reinforcement learning, annealing);
- EinsteinArena (open search and a domain-restricted search);
- the maximal excess of Hadamard matrices of order 108;
- the 2005 Backstrom contest.

None surfaced an order-109 value other than the archived MaxDet entry.

Pages checked with WebFetch:

- ThetaEvolve, arXiv:2511.23473 (Nov 2025): its Hadamard task is order 29 only.
- "Mathematical exploration and discovery at scale", arXiv:2511.02864v3 (whole text read): it has no maximal-determinant or excess problem.
- The Browne-Egan-Hegarty-Ó Catháin survey, arXiv:2104.06756 (whole text via ar5iv): there is no order-109 value. Its record table covers n ≡ 3 mod 4 from 23 to 99. It reports Orrick-Solomon's n ≡ 1 mod 4 computations only for n ≤ 100.
- Orrick-Solomon, arXiv:math/0311292: its records are at n = 37, 49, 65, 73, 77, 85, 93 and 97, not 109.

A possible route to an implicitly known value: bordering a Hadamard matrix H of order 108 gives det = det(H) * (1 + e/108), where e is the excess. That is D = 27^53 * (108 + e) / 4, so 291 * 27^53 corresponds to e = 1056. This is my own derivation. I found no published order-108 Hadamard matrix with excess ≥ 1056. The excess and bordered-lower-bound tables my searches surfaced stop at order 100, going by their snippets and abstracts.

## Comparison (same normalization, |det| / 2^108)

- Best value known for n = 109: the archived MaxDet entry **1.877483842E78** (10 significant digits, so the true value lies in [1.8774838415E78, 1.8774838425E78]). It is tagged "??" (not proved maximal), has R = .65 (0.6482 recomputed), and was found by T. Rokicki in 2005. No later source lists order 109.
- Claimed value: **2.119202655E78** (291 * 27^53).
  - It exceeds the top of the archived rounding interval by 2.417E77, a ratio of about 1.12875 (+12.9 %). The inequality is strict, so this is not a tie.
  - It is below the Barba bound: 291^2 = 84681 < 217 * 27^2 = 158193, so claimed/Barba = 0.7316 < 1.
  - The previous record was strictly below the bound (0.648), and 2*109 - 1 = 217 is not a perfect square, so order 109 is a live target, not a closed one.

## Defects in the claimant's table record (they do not change the verdict)

- `table-record/README.md` and the sources JSON say the n = 109 value 1877483841834222713683125485573890072927341503771574105042244268774869908324352 was read from the Math-AI-Caltech README.md (sha256 `7b6160e3...`) and from arXiv:2608.22518v3. Neither contains an n = 109 value.
  - The live README has sha256 `a445d967...`, and its 2146 bytes match the git tree.
  - The repo was last pushed at 2026-09-07T20:57:09Z, before their stated fetch time of 08:11:00Z today, so its content could not have differed.
  - The body of PR #65 likewise says the value came from `maxdet_records.csv`, which has no n = 109 row.
- Their baseline integer does lie inside the rounding interval of the archived MaxDet entry. The baseline value is right, but it is attributed to the wrong source. The record should cite the Archive-It `page3.shtml` and `d109.html` captures.
- All of their source rows carry one identical timestamp, 08:11:00Z, which cannot be checked independently.

## Limits

- The archive shows only 10 significant digits, and the exact archived integer was not retrievable (the archived Rokicki page returns 404). The 12.9 % margin is far larger than that rounding.
- No search can prove that something is absent. Journal-only papers without an arXiv version, and non-indexed tables, are covered only by the web searches listed above.
- This report addresses novelty only. Whether the object really attains the claimed determinant is for the reproduction skeptic.

## Verdict

novelty: PASS. The claimed |det| / 2^108 = 291 * 27^53 (about 2.1192E78) strictly beats the best known order-109 value, the archived Orrick MaxDet entry 1.877483842E78 (Rokicki, 2005), by a factor of 1.1287. Neither the Math-AI-Caltech CSV, nor arXiv:2608.22518v3, nor any newer arXiv work, nor TROPHY_CASE.md, nor any open PR lists order 109. The only other posting, PR #65, is this same object (same SHA-256), closed without merging.

pass: true
