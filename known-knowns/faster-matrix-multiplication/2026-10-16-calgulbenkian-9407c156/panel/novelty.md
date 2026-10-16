# Novelty check: 3x5x5 rank 58, 211 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Claim under test: a ternary straight-line program for the 3x5x5 rank-58 scheme with 211 additions under Perminov's reduced convention, against 221 in Perminov's live repository. This file covers novelty only (is 211 lower than every comparable known count). It does not check correctness; other skeptics do that.

Claim folder integrity: every line of claim.SHA256SUMS matched (shasum -a 256 -c, all OK).

Fetch method: one plain curl GET per URL, User-Agent `V3R1T4S-research (honest client; curl)`, time from `date -u`, status from `curl -w '%{http_code}'`, sha256 of the saved body. Pages saved in the panel's novelty_ws folder.

Workspace disclosure: novelty_ws already held files from an earlier fetch session (22:31Z to 22:33Z, rows at the top of fetchlog.txt; files pulls.json, v3_tree.json, pkg/, arxiv/, kk_fmm_README.md). That session was not mine and I did not read or use its files. My own requests start at 23:53:59Z. Where the earlier session saved a file under the same name, the sha256 values match mine (tree.json, reduced_known.json, README.md, CHANGELOG.md, Lille page, COVERAGE.md, fmm_sota.json, TROPHY_CASE.md). That earlier session also used up part of the shared unauthenticated GitHub API quota, which probably caused the 403 on the fmm_add_reduction tree below.

## Primary sources (criterion parts a, b, c and eligibility)

| source | URL | UTC fetch time | HTTP | sha256 | value read |
|---|---|---|---|---|---|
| Perminov repo tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T23:53:59Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | truncated=false, 6637 entries. Only one addition_reduced_ZT file for 3x5x5: `schemes/results/addition_reduced_ZT/3x5x5_m58_cr221_cn357_ZT_reduced.json`, so cr = 221 and the minimum cr is 221. No 5x3x5 or 5x5x3 reduced file. The other 3x5x5 m58 file, `naive_addition_reduced_ZT/3x5x5_m58_c351_ZT`, is a naive count under a different convention and does not compare. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T23:54:01Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | `"3x5x5-58": {"Z": 326, "Z2": 255}`. Z2 is a different ring and does not compare. Z 326 is above 221. |
| Perminov README | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T23:54:01Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | The only 3x5x5 line is the rank-table row "3x5x5 / 58 / 58 / 58 / 2.821392604". No addition count is given for 3x5x5. |
| Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T23:54:01Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No "Reduced additions improvement" entry for 3x5x5. Latest entry is dated 09/10/2026. No 3x5x5 string appears anywhere. |
| Lille 3x5x5 page | https://fmm.univ-lille.fr/3x5x5.html | 2026-10-15T23:54:01Z | 200 | be33b9a99092ed2cec4c4d39f3bdbb2c62bd272885668be05e04d0303fee406a | Rank 58, "taken from: Alexandre Sedoglavic and Alexey Vladimirovich Smirnov. The tensor rank of 5x5 matrices multiplication is bounded by 98 and its border rank by 89 ... arXiv 2101.12568". There is no Commentaries section and no complexity variant is cited. No addition or operation count appears on the page. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T23:54:02Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row for 3,5,5: "58 Alphatensor-F2 / 58 Alphatensor-Z / ... / adds +413". The legend says this column is "the addition count (nz(U)+nz(V)+nz(W) − 2r − n·p)". That is a naive count with no shared subexpressions, so it does not compare with reduced counts. In any case 413 is above 211. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T23:54:02Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | `{ "format": [3,5,5], "rank": 58, "exponent": 2.821393 }` (createdAt 2026-10-09T11:45:48). Rank 58 is the best known rank, so the scheme is eligible. |

## This repository (V3R1T4S)

| source | URL | UTC fetch time | HTTP | sha256 | value read |
|---|---|---|---|---|---|
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T23:54:03Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | 53 rows. The matrix-multiplication rows are rank records for formats 13 to 15 only. There is no addition-count row and no 3x5x5 row. |
| open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T23:54:03Z | 200 | 12473dc228f9f201566453a3e87b1d4ed24a37bf8eca1240f665a443a7148a2e | 16 open PRs (#9, #30, #153, #154, #190 to #201). I read every title and body. None names fmm-additive-complexity-records, and none gives a count for 3x5x5 (or 3,5,5). The only FMM one is #197, a rank claim for 13x15x15. Every "addition" match was the English word ("additional check"). |
| merged FMM packages (listing) | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-15T23:54:03Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 package folders plus the family files. |
| family INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-15T23:54:52Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | Rank records for 13x14x14 up to 15x16x16 only. |
| the 21 package INDEX.csv files | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/(package)/INDEX.csv | 2026-10-15T23:55:00Z to 23:55:05Z | 200 for all 21 | one per file, in fetchlog.txt | 12 addition-count packages for fmm-additive-complexity-records: 4x6x6 (373), 5x7x7 (699), 6x6x7 (695), 6x8x8 (993), 4x6x8 (476), 6x6x6 (588), 5x6x7 (582), 4x6x7 (469), 6x6x8 (719), 5x5x8 (556), 5x6x6 (502). These are the eleven merged on 2026-10-15, plus drzuzzjen's 5x5x5 (358). The other 9 packages are rank records. None covers 3x5x5. |

## Literature (last 24 months)

arXiv export API, four distinct queries. The first two went to http:// and got 301 redirects with empty bodies (23:55:15Z and 23:55:19Z, sha256 e3b0c442... of the empty body). I sent each query once more to the https:// redirect target. That followed the redirect; it was not a retry after a block.

| query | URL | UTC | HTTP | sha256 |
|---|---|---|---|---|
| q1 id_list (2512.21980, 2512.13365, 2604.27645, 2607.28676, 2609.32388, 2609.06588, 2601.05272) | https://export.arxiv.org/api/query?id_list=... | 2026-10-15T23:55:31Z | 200 | 147b75f0a48dc986cebb6144c54c20e9c2ed91f5dabc197edf10028aa0cb3daa |
| q2 abs "matrix multiplication" AND (abs "additive complexity" OR abs "number of additions" OR ti additions) | https://export.arxiv.org/api/query?search_query=... | 2026-10-15T23:55:35Z | 200 | 1ddacab3e849e22ae33fe4c8dd3e19567cd00f3b2a66078fdcd692d35473f3ab |
| q3 abs "matrix multiplication" AND (common subexpression OR straight-line OR additions OR change of basis) | https://export.arxiv.org/api/query?search_query=... | 2026-10-15T23:55:48Z | 200 | 775d840c851184a4cadd7017d8827f44580f90f844bc7ab008baa4d68f9d4ec9 |
| q4 abs "flip graph" OR (matrix multiplication AND ternary) | https://export.arxiv.org/api/query?search_query=... | 2026-10-15T23:55:53Z | 200 | c395fe3937fde200ce1d42ddab947c7538b7d7a54f06ad4bc0a3eb53e9004edc |

I also ran three web searches (search engine only, no page fetches). None turned up an addition count for 3x5x5 at rank 58 other than Perminov's.

Paper-by-paper:

- **Perminov, arXiv:2512.13365** (PDF https://arxiv.org/pdf/2512.13365, 2026-10-15T23:56:13Z, HTTP 200, sha256 82aff81bf22f80c13cf559f1c42ada3fecda51fb4efc773c3e7ee1ae5b135c27). Gives a count for 3x5x5. Table 1, "Schemes with optimal rank achieving new SOTA addition counts", has the row "3×5×5 58 357 230 224 223 221". In order, those are naive 357, Greedy-Vanilla 230, Mårtensson-Wagner Greedy-Potential GP-5 224 and GP-40 223, and Perminov's method 221. The count is comparable: same rank, ternary, no basis change ("additive complexity in fast matrix multiplication algorithms with ternary coefficients {-1,0,1}"). It is the 221 of the live repository. Table 6 lists only 4x7x8, 4x8x8, 5x7x8, 6x6x10, 7x7x7, 7x8x8 and 8x8x8, so 3x5x5 is not among its lowered counts. 211 is below 221 and below 223.
- **Perminov, arXiv:2512.21980**. No 3x5x5 count. It is about 3x3 only: "a rank-23 scheme with only 58 scalar additions" for "exact 3×3 matrix multiplication".
- **Mårtensson and Stankovski Wagner, IACR ePrint 2026/849** (abstract page https://eprint.iacr.org/2026/849, 2026-10-15T23:56:13Z, HTTP 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b). The PDF https://eprint.iacr.org/2026/849.pdf came back HTTP 403 with a "Just a moment..." challenge page (23:56:14Z, sha256 46c5d742d8e4057107e10c44a797fed8d9a4f7e0f71f599ccaeb376be6e6089d). I did not retry. The abstract says: "We present improved methods for optimizing the number of additions in Strassen-type matrix multiplication schemes for larger matrix sizes, and without any change of basis" and "use them to optimize the number of additions for schemes with dimensions up to (n, m, k) = (5, 7, 10)". So 3x5x5 IS inside the range of formats this paper covers, and its counts would be comparable (no basis change). The abstract names no format or rank, so I cannot tell whether it reports a count for 3x5x5 at rank 58, or what that count is. Indirect evidence: Perminov's 2512.13365 (Table 1) ran these authors' own tool (Greedy-Potential, GP-40) on the rank-58 scheme and got 223, and called 221 a new state of the art. The authors' repository could not be listed: https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1 returned HTTP 403 "API rate limit exceeded" (23:56:14Z, sha256 3209519d06deb9f4f950810899ddc6fafba9bcfb3fb8cad8b5e1b30459ace147), and I did not retry. Its README (https://raw.githubusercontent.com/werekorren/fmm_add_reduction/main/README.md, 23:57:07Z, HTTP 200, sha256 37b319e0a3cb960cb612d56e1b53ac61bdfcdd673a0cd9ebafd9599cc055e842) describes the tool and gives no per-format counts. I found no arXiv or conference copy of 2026/849.
- **Mårtensson and Stankovski Wagner, "The Number of the Beast" (ACDA25, ePrint 2024/2063)**. The PDF https://eprint.iacr.org/2024/2063.pdf returned HTTP 403 with a challenge page (23:57:07Z, sha256 2d05cfe1cdd35a5437635c081d874594ce73e35be0f06c9b4763655d00da268d). It covers "dimensions up to 666", which includes 3x5x5. It is reference [1] in Perminov's 2512.13365, which calls its own 221 "new SOTA" against it. So it is very unlikely to hold a count of 211 or lower.
- **Mårtensson, Stankovski Wagner and Stapleton, "Hell's Bells", IACR ePrint 2026/1688** (this is the Hells-family fmm_add_reduction work; abstract page https://eprint.iacr.org/2026/1688, 2026-10-15T23:57:46Z, HTTP 200, sha256 8269492c23b40e63ae3303a37993bdd76d42ecd633dbbfc1bea2099ad587b8ff, revised 2026-10-06). The PDF https://eprint.iacr.org/2026/1688.pdf returned HTTP 403 with a challenge page (23:57:53Z, sha256 4d62271dcc1470d8559b90dba11ff893ce44ee028488389bc56f066522bda551). The abstract says: "We achieve record-low arithmetic (additive) complexity for various combinations of dimensions. For (n,m,k) = (2,2,k), our method performs particularly well." It targets ternary schemes, with addition reduction done separately, so its counts would be comparable. The abstract does not name 3x5x5 or rank 58.
- **Sun, arXiv:2604.27645**. No 3x5x5 count. It is about 3x3 only: "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions".
- **Karunaratne-Idamekorala, arXiv:2607.28676**. No 3x5x5 count. It is about 3x3 only: "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices."
- **Stapleton-Perminov, arXiv:2609.32388**. No 3x5x5 count. It is about 3x3 only, and its kernel count uses a basis change, so it would not compare anyway: "using 51 additions and subtractions in alternative bases. The input and output conversions require five further additions, giving 56 additions in ordinary coordinates."
- **Nielsen, arXiv:2609.06588**. No 3x5x5 count. It is about 3x3 only, and its count comes with a basis change, so it is not comparable: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change".
- **Mårtensson, Stankovski Wagner and Stapleton, arXiv:2601.05272**. No 3x5x5 count. It is about 3x3 only: "finding an algorithm requiring only 59 additions".
- **Perminov, arXiv:2511.20317, 2603.02398 and 2606.02480** (flip-graph rank papers). Their abstracts report ranks and naive additive complexity, not reduced counts for 3x5x5.

unresolved: IACR ePrint 2026/849 PDF (403 challenge), ePrint 2026/1688 PDF (403 challenge), ePrint 2024/2063 PDF (403 challenge) and the werekorren/fmm_add_reduction tree (403 rate limit). 3x5x5 is inside 2026/849's stated range (up to 5x7x10), and 2026/1688 covers "various combinations" of small dimensions, so both could plausibly contain a comparable count for 3x5x5 at rank 58. Neither abstract says it covers this format at this rank, and nothing I could read shows a count at or below 211. Perminov's live repository, updated through 2026-10-09 (after both papers appeared), still lists 221. 2024/2063 predates Perminov's 221 and is beaten by it, per 2512.13365.

## Verdict

Full criterion: PASS on what could be read. 211 is strictly below:
- (a) Perminov's live minimum cr, 221 (the only addition_reduced_ZT file for 3x5x5 m58), with reduced_known.json at Z 326, and nothing lower in the README or CHANGELOG;
- (b) the Lille page, which cites no complexity variant and gives no count;
- (c) matmulcatalog, whose +413 is naive, not comparable, and higher anyway;
- the literature I could read (best comparable count 221, Perminov 2512.13365 Table 1; Greedy-Potential 223);
- this repository's trophy case, its open PRs and its 12 merged addition-count packages, none of which covers 3x5x5.

Rank 58 is the best known rank (fmm_sota.json), so the scheme is eligible. One caveat remains: the full texts of ePrint 2026/849 and 2026/1688 could not be read. They could contain a lower count, but neither is known to cover 3x5x5 at rank 58.

Partial win p1 as defined for this panel (strictly fewer than Perminov's live count, same reduced convention): PASS, 211 versus 221. Note that the bank's own enumerated p1 is the 3x3x3 rank-23 case, which this claim does not address.

pass: true
