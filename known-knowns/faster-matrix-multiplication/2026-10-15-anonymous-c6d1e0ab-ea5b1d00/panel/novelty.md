# Novelty check: 5x6x6 rank 130, 502 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Target: fmm-additive-complexity-records. Claim: a ternary straight-line program for 5x6x6 at rank 130 with 502 additions under Perminov's reduced convention, against 562 in Perminov's repository.

Claim folder hashes: CLAIM.md, INDEX.csv, table-record/README.md and the object file (5x6x6_m130_cr502_ZT_reduced.json) all match claim.SHA256SUMS.

Every fetch below was one plain curl request with the User-Agent 'V3R1T4S-research (honest client; curl)', with no retries and no redirects followed. Times are UTC from `date -u`.

## Primary table and status sources

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov repo tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T12:13:23Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | Tree not truncated. addition_reduced_ZT has exactly one file for 5x6x6: `5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json`, so the minimum cr is **562**. The files `naive_addition_reduced_ZT/5x6x6_m130_c1697_ZT` and `c1714_ZT` are naive counts under a different convention and do not compare. No reduced file exists for the permutations 6x5x6 or 6x6x5. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T12:13:26Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | No 5x6x6 key. The largest key is '4x6x6-116'. |
| Perminov README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T12:13:26Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | 5x6x6 appears only in the rank tables (rank 130, `Z/Q`; exponent 2.812001673). It states no addition count. |
| Perminov CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T12:13:27Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | It has no 5x6x6 entry. None of its "Reduced additions improvement" sections names 5x6x6. |
| Lille per-format page | https://fmm.univ-lille.fr/5x6x6.html | 2026-10-15T12:13:27Z | 200 | e25c8925f009b855df1a520c3aa5e204c5138eac2fa1e3666d5687c80a56e902 | "Description of fast matrix multiplication algorithm: ⟨5×6×6:130⟩". **No Commentaries section** and no 'best-known complexity' variant. The only cited work is Kauers and Wood, arXiv 2505.05896, which is a rank paper and states no addition or operation count (checked below). |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T12:13:28Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row for format ⟨5,6,6⟩: "✓ 130 Dronperminov-ZT", adds **+1716**. The legend defines it as "the addition count (nz(U)+nz(V)+nz(W) − 2r − n·p)", which is a naive count with no shared subexpressions. It is not comparable to a reduced count, and in any case it is higher than 502. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T12:13:28Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | `{'format': [5, 6, 6], 'rank': 130, 'exponent': 2.812002}` (createdAt 2026-10-09T11:45:48). Rank 130 is the best known rank, so the claim is eligible. |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T12:13:28Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | No fmm-additive-complexity-records entry and no 5x6x6 entry. The only "6,6" hit is the constant-weight code A(35,6,6), which is unrelated. |
| V3R1T4S open PRs | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T12:13:28Z | 200 | 13f1b324a8cfa79c158feb8e70b0443f85468b9e5876637c06056247704260c2 | 44 open PRs, all on one page, so the list is complete. Every title and body was searched. Four PRs are fmm-additive-complexity-records claims: #162 and #159 (5x6x7 rank 150) and #161 and #149 (4x6x7 rank 123). **No open PR mentions 5x6x6** in any spelling. |

The repository counts match the author's table record: the same sha256 for the tree, reduced_known.json, README, CHANGELOG, the Lille page, COVERAGE.md and fmm_sota.json, and the same minimum of 562.

## Literature (last 24 months)

arXiv export API: four requests in total.

- **Request 1** (http://export.arxiv.org/api/query?id_list=2512.21980,2512.13365,2604.27645,2607.28676,2609.32388,2609.06588,2505.05896&max_results=10) returned HTTP 301 with an empty body at 2026-10-15T12:14:35Z (sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855). This was an http-to-https redirect, not a block.
- **Request 2** was the same query over https, at 2026-10-15T12:14:42Z. HTTP 200, sha256 bde52decc68b906b1ef074a2f65203fb65d80c9d157de17e7255e440421a3cb9.
- **Request 3** searched abstracts for "matrix multiplication" with additions or "additive complexity", newest first, 60 results (https://export.arxiv.org/api/query?search_query=abs:%22matrix%20multiplication%22%20AND%20(abs:additions%20OR%20abs:%22additive%20complexity%22)&sortBy=submittedDate&sortOrder=descending&max_results=60). Fetched 2026-10-15T12:15:57Z, HTTP 200, sha256 e55e9e0da66ff3a46a026eda0072652673e50d5b4e63e01365801e23c2a63c7d.
- **Request 4** searched for "common subexpression elimination" with "matrix multiplication" (https://export.arxiv.org/api/query?search_query=all:%22common%20subexpression%20elimination%22%20AND%20all:%22matrix%20multiplication%22&sortBy=submittedDate&sortOrder=descending&max_results=40). Fetched 2026-10-15T12:15:58Z, HTTP 200, sha256 ab499ff9498733f1fa1ee4e7e8294303485919063ba4d363b367f930b016d219.

Two web searches turned up no published addition count for 5x6x6 at rank 130 other than Perminov's. The searches were the ePrint 2026/849 title and "5x6x6 rank 130 matrix multiplication additions reduced scheme".

### Paper by paper

- **Perminov, arXiv 2512.13365v2**: Parallel Heuristic Exploration for Additive Complexity Reduction. Full text from https://arxiv.org/html/2512.13365v2, fetched 2026-10-15T12:14:53Z, HTTP 200, sha256 7fbf6570ffe7c946d1561d56587f53939bfb8be542f21adb1641813f2c17de3e.
  - **Count for 5x6x6: yes, 562, which is comparable.** It is the same convention and the same repository file. It is not lower than 562.
  - Table 1 ("Schemes with optimal rank achieving new SOTA addition counts") has the row 5×6×6, rank 130: Naive 1716, GV 589, GP-5 587, GP-40 573, Prop. 562.
  - On scope and convention, the paper says: "This work focuses exclusively on schemes with coefficients in the ternary set ZT={−1,0,1}."
  - **Table 6 does not include 5x6x6.** Its formats are 4×7×8, 4×8×8, 5×7×8, 6×6×10, 7×7×7, 7×8×8 and 8×8×8.
  - The GP-40 column is the fmm_add_reduction tool by Mårtensson and Wagner, run on the same scheme. It gives **573**, which is comparable and higher than 502.
- **Perminov, arXiv 2512.21980**: the abstract covers only 3x3: "a rank-23 scheme with only 58 scalar additions. This improves the previous best additive complexity of 60 additions without a change of basis." **No count for 5x6x6.**
- **Sun, arXiv 2604.27645**: "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions". **No count for 5x6x6.**
- **Karunaratne and Idamekorala, arXiv 2607.28676**: "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices." **No count for 5x6x6.**
- **Stapleton and Perminov, arXiv 2609.32388**: "a rank-23 algorithm for 3×3 matrix multiplication using 51 additions and subtractions in alternative bases." This covers only 3x3, and its count is also not comparable because it uses a basis change. **No count for 5x6x6.**
- **Nielsen, arXiv 2609.06588**: "a rank-23 algorithm for general 3 x 3 matrix multiplication using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change". This covers only 3x3 and uses a basis change. **No count for 5x6x6.**
- **Mårtensson and Wagner, IACR ePrint 2026/849**: On Why and How to Minimize the Arithmetic Complexity of Fast Matrix Multiplication Algorithms.
  - The abstract page https://eprint.iacr.org/2026/849 was fetched at 2026-10-15T12:14:53Z: HTTP 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b. It says the authors work "without any change of basis" and that "We implement of our methods and use them to optimize the number of additions for schemes with dimensions up to $(n, m, k) = (5, 7, 10)$." It also says they "apply our algorithms to a large number of schemes" and "optimize the arithmetic complexity for two sets of thousands of schemes with the same rank."
  - **The PDF https://eprint.iacr.org/2026/849.pdf was blocked.** At 2026-10-15T12:14:53Z it returned HTTP 403 with a Cloudflare "Just a moment..." challenge page (sha256 880dd6898726a6564918c3f62843420e86e00c557fd81739c5716f7b8c86c77a). It was not retried.
  - **5x6x6 is inside the stated dimension range**, because 5 ≤ 5, 6 ≤ 7 and 6 ≤ 10. The abstract does not say which formats or ranks are in the paper's tables, so it is not known whether the paper gives a count for 5x6x6 at rank 130.
  - The authors' repository was fetched once: https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1 at 2026-10-15T12:14:53Z, HTTP 200, sha256 dfdf1cd6a43106f75700703a917a5bb0ecdb971b27858e2bceafeb5718df1573. The API marked it truncated: 65074 entries. The visible part has algorithms/grey (14 files, largest format 5x2x2) and algorithms/hells_bells subfolders 222, 223, 224, 225, 226, 227, 228, 233, 234 and 333. **No 5x6x6 file appears in the visible part**, but the truncation hides the rest.
  - The repository README (https://raw.githubusercontent.com/werekorren/fmm_add_reduction/main/README.md, 2026-10-15T12:15:59Z, HTTP 200, sha256 37b319e0a3cb960cb612d56e1b53ac61bdfcdd673a0cd9ebafd9599cc055e842) points only to the ACDA25 paper. It gives no 5x6x6 count.
  - I found no arXiv copy of 2026/849.
  - The best comparable evidence for this tool on this format is Perminov's Table 1. Run on the rank-130 scheme, GP-40 gives 573.
- **Mårtensson and Wagner, IACR ePrint 2024/2063** (ACDA25, "dimensions up to 666"). This is the predecessor of 2026/849. The abstract page https://eprint.iacr.org/2024/2063 was fetched at 2026-10-15T12:15:59Z: HTTP 200, sha256 dafa562b4f1ff2dd5beac64491d2cdb5cffc9877bc93edf087215977a55bb133.
  - It applies the method to "another reference set of algorithms due to Moosbauer and Kauers", and the paper was received on 2024-12-23.
  - **It cannot contain a rank-130 count for 5x6x6.** That rank first appeared in May 2025: Kauers and Wood's table lists (5,6,6) as "180 137 130", meaning the previous best rank was 137.
- **Kauers and Wood, arXiv 2505.05896**: the work the Lille page cites. Full text from https://arxiv.org/html/2505.05896v1, fetched 2026-10-15T12:17:15Z, HTTP 200, sha256 c4b7567beeb768c2c0cd153a1a79611011df19aa7f57a19c109ff08140a035e8. It says: "For the format (5,6,6) we have a multiplication scheme of rank 130." It is about rank only and states **no addition or operation count**.
- **Perminov, arXiv 2606.02480**: Meta Flip Graph meets Serendipitous Product, the abstract page https://arxiv.org/abs/2606.02480, fetched 2026-10-15T12:16:47Z, HTTP 200, sha256 5d9c3e5e3342c9ac31483958c43e1230a2480105b0a0e4ac5bde309537dac043. It covers rank and coefficient type only: "ranks are improved for 207 formats." **No addition count.**
- **Hells and others, through fmm_add_reduction**: this is the hells_bells data in the repository above. The visible formats are 2x2xk for k up to 8, 2x3x3, 2x3x4 and 3x3x3. **No 5x6x6 is visible**, and the listing is truncated.
- Other recent hits from the arXiv queries:
  - arXiv 2601.05272 and arXiv 2508.03857 are 3x3 only.
  - arXiv 2511.20317 minimizes the naive additive complexity of ternary schemes. It reports no reduced count for 5x6x6.

unresolved: The IACR ePrint 2026/849 PDF (Mårtensson and Wagner) was blocked with HTTP 403 and a Cloudflare challenge. The authors' repository tree came back truncated. 5x6x6 lies inside the paper's stated range of "dimensions up to (5, 7, 10)", so the paper could plausibly give a count for this format. It is not known to cover 5x6x6 at rank 130. A comparable count below 502 is plausible only if its scheme-generation pipeline found a different rank-130 scheme. The only published result for their reduction tool on this format is GP-40 = 573 (Perminov 2512.13365, Table 1), which is well above 502.

## Verdicts

- **Partial win p1** (strictly fewer than Perminov's live count, same reduced convention): **PASS.** 502 is strictly less than 562, the minimum and only addition_reduced_ZT file for 5x6x6 at rank 130. reduced_known.json, the README and the CHANGELOG have no lower value.
- **Full criterion**: **PASS, with the unresolved caveat above.**
  - (a) Perminov's live minimum is 562.
  - (b) The Lille page has no Commentaries section and no complexity variant, and its cited work states no count.
  - (c) The COVERAGE.md adds value is 1716. It is naive, not comparable, and higher anyway.
  - Rank 130 is the best rank in fmm_sota.json.
  - No TROPHY_CASE entry or open PR covers 5x6x6.
  - No paper from the last 24 months that I could read gives a comparable count below 562 for this format and rank.
  - 502 strictly beats every comparable count I could read: 562 and 573. It is not a tie. The one unread source is not known to cover this format at this rank.

pass: true
