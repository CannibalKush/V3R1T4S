# Novelty check: 2x4x8 rank 51, 181 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Claim read: CLAIM.md, INDEX.csv, table-record/README.md and the object file name (object/2x4x8_m51_cr181_ZT_reduced.json). All four sha256 values match claim.SHA256SUMS. Claimed value 181; the claim's reference value is 188.

Fetch rules followed: one plain curl GET per URL, User-Agent "V3R1T4S-research (honest client; curl)", no retries. Saved copies are in the panel's novelty_ws folder. Times are UTC from `date -u` taken just before each request.

## Primary sources

| Source | URL | UTC time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T23:53:57Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | Tree not truncated. addition_reduced_ZT holds 195 files. Exactly one is for 2x4x8: `2x4x8_m51_cr188_cn354_ZT_reduced.json` (cr 188, naive cn 354). No file for any permutation of 2,4,8 (2x8x4, 4x2x8, 4x8x2, 8x2x4, 8x4x2) in addition_reduced_ZT, and none for 2x4x8 in naive_addition_reduced_ZT (126 files). Minimum cr = 188. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T23:53:58Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | No "2x4x8-51" key. It lists 2x4x4-26, 2x4x5-33, 2x4x6-39 and others, but nothing for 2x4x8. |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T23:53:59Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | The only 2x4x8 line is the rank table row "`2x4x8` 51 51 51 2.836212671". No addition count for 2x4x8 is stated. The README credits "Work on additive reductions by @werekorren (fmm_add_reduction/tree/main/algorithms)". |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T23:53:59Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No 2x4x8 entry. Its "Reduced additions improvement" sections name other formats only (2x4x5, 2x4x6, 3x4x4, 2x3x7, 2x3x8, 2x2x9, 2x2x10, 2x4x4, 3x3x4, 3x3x5, 2x3x3, 2x3x5, 2x3x6, 2x2x6, 2x2x7, 2x2x8). |
| Lille 2x4x8 page | https://fmm.univ-lille.fr/2x4x8.html | 2026-10-15T23:53:59Z | 200 | dfb8035a9fb6c0ffa4f52f6edcf5c4626a5864d332ce4fe87349f319d62fa805 | Rank 51 ("2x4x8:51"). Source cited: AlphaEvolve (Novikov et al., Google DeepMind, May 2025, arXiv 2506.13131). No Commentaries section, and no complexity variant is cited. The cited work is a rank result; the page states no addition or operation count. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T23:54:00Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row for format 2,4,8: rank 51 (AlphaEvolve) in F2 and R/Q/Z, adds "+354". The page defines adds as "nz(U)+nz(V)+nz(W) − 2r − n·p", which is a naive count. That is a different convention from the reduced count, so it does not compare. It equals Perminov's naive cn354. In any case 354 is above 181. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T23:54:00Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48. Entry `{ "format": [2,4,8], "rank": 51, "exponent": 2.836213 }` is the only one for this format or its permutations. Rank 51 is the best known rank, so the scheme is eligible. |
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T23:54:00Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | No 2x4x8 entry and no addition-count row. Its matrix-multiplication rows are rank records for formats from 13x14x14 to 15x16x16. |
| Open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T23:54:00Z | 200 | 12473dc228f9f201566453a3e87b1d4ed24a37bf8eca1240f665a443a7148a2e | 16 open PRs; I read every title and body. None names fmm-additive-complexity-records, 2x4x8, or any addition count. #197 is fmm-catalogue-small-format-rank (13,15,15 rank 1762), a rank claim. #9 mentions fmm only in a verifier fix. |
| known-knowns fmm listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-15T23:54:01Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 merged package folders. I fetched each package's INDEX.csv once (below). |

Merged package INDEX.csv files, each fetched once from https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/ followed by the folder name and /INDEX.csv. All returned HTTP 200 between 2026-10-15T23:55:39Z and 23:55:43Z.

- Addition-count packages (fmm-additive-complexity-records), 12 in all:
  - 0daeb118: 4x6x6:105, cr 373 (sha 59386398...)
  - 2abc8962: 5x7x7:176, cr 699 (8e64a446...)
  - 34a5c13c: 6x6x7:183, cr 695 (11fb6617...)
  - 353b9229: 6x8x8:266, cr 993 (b63ec6a1...)
  - 45256d75: 4x6x8:140, cr 476 (41a5bdee...)
  - 4abbbac3: 6x6x6:153, cr 588 (a4b984d8...)
  - 832b0866: 5x6x7:150, cr 582 (d8e6dcf1...)
  - ade76c2e: 4x6x7:123, cr 469 (a0aaeb0d...)
  - b60a9f0b: 6x6x8:203, cr 719 (389e958e...)
  - cd6b1a18: 5x5x8:144, cr 556 (4469ff33...)
  - ea5b1d00: 5x6x6:130, cr 502 (5cd7c3ed...)
  - drzuzzjen-71fa63de: 5x5x5:93, cr 358 (391c20c3...)
- The other 9 packages are rank packages (fmm-catalogue-small-format-rank) for formats 11x13x16 through 15x16x16.
- None of the 21 covers 2x4x8.

Also fetched: the known-knowns fmm INDEX.csv and README.md (2026-10-15T23:55:07Z, both 200; sha 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 and 740321f0f9287e13ee0f1dd229c47a974b49393560a453df125ad850b359ba07). Both list only the five rank schemes. I made two attempts to list package contents:
- https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 at 2026-10-15T23:55:14Z returned 403 (GitHub API rate limit). Not retried.
- One github.com tree page for package 0daeb118 at 2026-10-15T23:55:27Z returned 200 (sha 4052c4d811443de365d1f69312656b494f9756743c41706f133acf98888c7cc8). It showed that each package has an INDEX.csv.

Repo status: no merged package, open pull request or trophy entry gives a count for 2x4x8.

## Literature (last 24 months)

arXiv export API: I sent four requests, the most the brief allows.
- Request 1 (2026-10-15T23:55:53Z, a search for "matrix multiplication" AND additions or "additive complexity", sent over http) returned 301 with an empty body (sha e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855). It redirects to https.
- Request 2 (2026-10-15T23:55:57Z, a search for straight-line program AND matrix multiplication, sent over http) returned 301 with an empty body, same reason.
- Request 3 (2026-10-15T23:56:04Z, https://export.arxiv.org/api/query?search_query=abs:"matrix multiplication" AND (abs:additions OR abs:"additive complexity" OR abs:"straight-line"), newest first, 100 results) returned 200, sha 0088ecbc729b78ed2b9cdd1446212fe175776a4e6351b6b9f97b5c46d2365403.
- Request 4 (2026-10-15T23:56:09Z, https://export.arxiv.org/api/query?id_list=2512.21980,2512.13365,2604.27645,2607.28676,2609.32388,2609.06588,2601.05272) returned 200, sha 147b75f0a48dc986cebb6144c54c20e9c2ed91f5dabc197edf10028aa0cb3daa.

Request 3 found, in the window, the addition papers below plus 2508.03857 (60 additions, 3x3 only). It found no other paper that gives addition counts for 2x4x8.

I also ran two web searches: the ePrint title with "arXiv", and "2x4x8 rank 51 additions straight-line program". They found no arXiv copy of ePrint 2026/849 and no 2x4x8 addition count. I fetched two more abstract pages once each:
- https://arxiv.org/abs/2606.02480 at 2026-10-15T23:57:34Z, 200, sha 5d9c3e5e3342c9ac31483958c43e1230a2480105b0a0e4ac5bde309537dac043.
- https://arxiv.org/abs/2506.19405 at 2026-10-15T23:57:34Z, 200, sha dc0731bcb2db87d7e5fc95fa8a4d743edce9adbd646aec51fc04b029fbf96b46.

### Perminov, arXiv:2512.13365 (Parallel Heuristic Exploration for Additive Complexity Reduction)
Fetched https://arxiv.org/html/2512.13365v2 at 2026-10-15T23:56:25Z: HTTP 200, sha 7fbf6570ffe7c946d1561d56587f53939bfb8be542f21adb1641813f2c17de3e.

- **Gives a count for 2x4x8: yes.** Table 1 ("Schemes with optimal rank achieving new SOTA addition counts") has the row "2 × 4 × 8, 51, 354, 197, 191, 190, 188". The columns are Naive, GV, GP-5, GP-40 and Proposed. So the best is 188, with 190 from fmm_add_reduction GP-40 and 197 from Greedy-Vanilla.
- **Comparable: yes.** The paper's method is "a parallel random-search method for reducing additive complexity in fast matrix multiplication algorithms with ternary coefficients {-1,0,1}". It is common-subexpression elimination on a fixed scheme, with no basis change; the paper sets this apart from "sparser algebraic representations via basis change", which it calls a different strategy. All of 188, 190 and 197 are above 181.
- **Table 6 does not include 2x4x8.** It lists component-wise combinations for 4x7x8:164, 4x8x8:182, 5x7x8:206, 6x6x10:252, 7x7x7:250, 7x8x8:310 and 8x8x8:343 only.

### Perminov, arXiv:2512.21980 (from request 4)
- **Gives a count for 2x4x8: no.** The abstract covers 3x3 only: "achieving a rank-23 scheme with only 58 scalar additions".

### Mårtensson and Stankovski Wagner, IACR ePrint 2026/849
The abstract page https://eprint.iacr.org/2026/849 was fetched at 2026-10-15T23:56:24Z: HTTP 200, sha 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b. The PDF https://eprint.iacr.org/2026/849.pdf, fetched at the same time, returned 403 with a Cloudflare "Just a moment... Enable JavaScript and cookies" challenge page (sha e65c66953cf7f189a8e0b47b8503d6751584e985fc92cf1ac040188312a9d9ed). Not retried.

- The paper's convention would be comparable. The abstract says: "We present improved methods for optimizing the number of additions in Strassen-type matrix multiplication schemes for larger matrix sizes, and without any change of basis."
- **The format is inside the paper's range.** The abstract says: "use them to optimize the number of additions for schemes with dimensions up to (n, m, k) = (5, 7, 10)". Sorted, 2x4x8 is 2,4,8, inside 5,7,10. The rank-51 scheme (AlphaEvolve, May 2025) was public before the paper was received (2026-04-30).
- **Whether it gives a count for 2x4x8 at rank 51: unknown.** The abstract names no format-level counts.
- The abstract also says "We optimize the arithmetic complexity for two sets of thousands of schemes with the same rank". So the paper may hold counts for rank-51 schemes other than Perminov's.
- No arXiv copy was found. The predecessor, ePrint 2024/2063 ("dimensions up to 666"), would not include 2x4x8 because 8 is above 6. I did not fetch it.

### Hells and others' fmm_add_reduction, which is Mårtensson and Stankovski Wagner's repository werekorren/fmm_add_reduction
https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1, fetched at 2026-10-15T23:56:25Z, returned 403 "API rate limit exceeded" (sha 3209519d06deb9f4f950810899ddc6fafba9bcfb3fb8cad8b5e1b30459ace147). Not retried, and no other URL for this repository was tried.

- **Known count from this tool: 190, comparable.** Perminov's 2512.13365 Table 1 reports 190 for the tool's best mode (GP-40) on 2x4x8:51. 190 is above 181.
- Its algorithms folder is unread. Perminov's README credits it as a source.

### Sun, arXiv:2604.27645 (from request 4)
- **Gives a count for 2x4x8: no.** The abstract covers 3x3 only: "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions".

### Karunaratne-Idamekorala, arXiv:2607.28676 (from request 4)
- **Gives a count for 2x4x8: no.** The abstract covers 3x3 only: "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices".

### Stapleton-Perminov, arXiv:2609.32388 (from request 4)
- **Gives a count for 2x4x8: no.** It is 3x3 only.
- **Not comparable in any case: it uses a basis change.** The abstract says: "using 51 additions and subtractions in alternative bases. The input and output conversions require five further additions, giving 56 additions in ordinary coordinates."

### Nielsen, arXiv:2609.06588 (from request 4)
- **Gives a count for 2x4x8: no.** It is 3x3 only.
- **Not comparable in any case: it uses a basis change.** The abstract says: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change".

### Other papers checked
- **arXiv:2601.05272:** 3x3 only, "an algorithm requiring only 59 additions".
- **arXiv:2606.02480 (meta flip graph meets serendipitous product):** a rank paper, "ranks are improved for 207 formats". No addition counts are stated.
- **arXiv:2506.19405 (Dumas et al.):** only 2x2x2:7 and 3x3x6:40 are named. Its operation counts use "alternative basis sparsification", which is a basis change, so they do not compare.

## Comparison

These are all the comparable counts for 2x4x8 at rank 51 that I could read:
- Perminov repository: 188 (the cr188 file).
- arXiv:2512.13365 Table 1: 188, 190 (GP-40), 191 (GP-5) and 197 (GV).

The minimum is 188, and 181 is 7 below it. The Lille page states no count. The COVERAGE.md value of 354 is a naive count in a different convention; it is also above 181. No merged package, open pull request or trophy entry covers this format.

unresolved: ePrint 2026/849 PDF (403 Cloudflare challenge) and the werekorren/fmm_add_reduction repository tree (403 GitHub API rate limit). Both are by the same authors, use a comparable convention (ternary, no basis change), and cover a format range that includes 2x4x8; the abstract also says they optimize "thousands of schemes with the same rank". So each could plausibly hold a comparable count for 2x4x8 at rank 51, and I cannot rule out that it is 181 or lower. Neither is known to give a count for this format at this rank. The only known count from their tool on this scheme is 190 (Perminov arXiv:2512.13365 Table 1).

## Verdict

- **Full criterion: PASS on everything I could read.** 181 is strictly below Perminov's live minimum of 188. No count on the Lille page or its cited work, matmulcatalog (naive count, not comparable; 354 in any case), merged packages or open pull requests is lower. Rank 51 equals the fmm_sota best rank. The verdict depends on the two unresolved sources above, which are not known to cover 2x4x8 at rank 51. A reviewer who can read the ePrint 2026/849 PDF or the fmm_add_reduction algorithms folder should check for a 2x4x8:51 count of 181 or lower.
- **Partial win p1:** as written in the bank, p1 is about 3x3x3:23, so it does not apply to this object. Read as the brief asks (strictly fewer than Perminov's live count, same convention), it is a **PASS**: 181 against 188 in the same reduced convention. This is not a tie.

pass: true
