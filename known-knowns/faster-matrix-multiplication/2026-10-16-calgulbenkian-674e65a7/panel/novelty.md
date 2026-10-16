# Novelty check: fmm-additive-complexity-records, 2x8x8 rank 100, 418 reduced additions (rerun)

context: Claude Code subagent (Opus 5.5), fresh context

Scope read locally: the claim folder (CLAIM.md, table-record/README.md, INDEX.csv, the object file name) and claim.SHA256SUMS (all eight hashes check OK), plus the operator's text extraction of IACR ePrint 2026/849 that the rerun notes allow. Every web page below was fetched once with curl, User-Agent 'V3R1T4S-research (honest client; curl)', no retries. Saved copies are in novelty_ws/rerun/ with a fetch log.

Claim under test: 418 additions (Perminov reduced convention) for the rank-100 scheme for 2x8x8, against 424.

## Primary table and status sources

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov repository tree (API) | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-16T00:18:27Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | Not truncated, 6637 entries. Every path containing 2x8x8, 8x2x8 or 8x8x2: schemes/known/tensor/2x8x8_tensor.mpl and schemes/results/addition_reduced_ZT/2x8x8_m100_cr424_cn608_ZT_reduced.json. Only one addition_reduced_ZT file for this format, rank 100, cr 424. Minimum cr = 424. (The API answered 200 this time, so the HTML fallback was not needed.) |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-16T00:18:40Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | No 2x8x8 key. Largest 2-row key is "2x6x6-56": Z 419, Z2 327. |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-16T00:18:40Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | One 2x8x8 line, a rank table row (line 842): "2x8x8, 100, 100, 100, 2.847366938". No addition count for 2x8x8. |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-16T00:18:40Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No line mentions 2x8x8. Its "Reduced additions improvement" entries cover other formats only. |
| Lille per-format page | https://fmm.univ-lille.fr/2x8x8.html | 2026-10-16T00:18:41Z | 200 | 82b21f1d54215bbd138341ff96de261aead48995d92e42918607c87b9e334e0e | Rank 100 ("2x8x8:100"), taken from Hopcroft and Kerr, SIAM J. Appl. Math. 20(1), 1971. No Commentaries section. No complexity variant is cited. The words "complexity" and "addition" do not appear on the page. The page links Maple tensor, LRP and evaluation-scheme files but states no count. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-16T00:18:41Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row for ⟨2,8,8⟩: F2 "—", R/Q/Z "✓ 100 Dronperminov-cr424_cn608_ZT_reduced", best "100 in R/Q/Z", adds "—", history "—". The adds cell has no value. That column would be a naive count (nz(U)+nz(V)+nz(W) − 2r − n·p), which is a different convention and would not compare in any case. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-16T00:18:42Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48. Entry {"format": [2, 8, 8], "rank": 100, "exponent": 2.847367}. Rank 100 is the best known rank, so the scheme is eligible. |

## This repository (V3R1T4S)

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-16T00:18:42Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | No 2x8x8 entry. The words "addition" and "additive" do not appear. The matrix-multiplication rows are rank records over Q for formats 13 and above. |
| Open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-16T00:18:42Z | 200 | 28704d72eaed4c74b1b685f8b89a1c7e53bda8f9b69dec5d35584937a63c65c1 | 16 open pull requests, every title and body read: 201, 200, 199, 198, 197, 196, 195, 194, 193, 192, 191, 190, 154, 153, 30, 9. None names fmm-additive-complexity-records. None mentions 2x8x8, 2,8,8 or 288-100. The only matrix-multiplication claim is #197, a (13,15,15) rank claim. |
| known-knowns/faster-matrix-multiplication (contents API) | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-16T00:18:43Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 dated package folders plus the family files. |
| Repository tree (one call to map packages to formats) | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-10-16T00:19:55Z | 200 | f63c3cc8f48202557b7290f117f14aefdebe4f42ed79cf2448cb318d24b229db | Not truncated. 12 merged addition-count packages. Eleven are anonymous and dated 2026-10-15: 4x6x6 cr373, 5x7x7 cr699, 6x6x7 cr695, 6x8x8 cr993, 4x6x8 cr476, 6x6x6 cr588, 5x6x7 cr582, 4x6x7 cr469, 6x6x8 cr719, 5x5x8 cr556, 5x6x6 cr502. The twelfth is 5x5x5 cr358 from drzuzzjen. The other packages are rank packages over Q. No path anywhere in the repository contains 2x8x8, 8x2x8 or 8x8x2. No merged package covers this format. |
| Family INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-16T00:19:44Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | Rank rows only (13x14x14 to 15x16x16). No 2x8x8. |
| Family README.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/README.md | 2026-10-16T00:19:44Z | 200 | 740321f0f9287e13ee0f1dd229c47a974b49393560a453df125ad850b359ba07 | No 2x8x8 and no addition count. |

## Literature (last 24 months)

arXiv export API: four distinct queries. Query 1 was first sent over http and got a 301 redirect with an empty body (2026-10-16T00:20:10Z). The same query was then sent once to the https endpoint.

| Query | URL (abridged) | UTC | HTTP | sha256 | Result |
|---|---|---|---|---|---|
| q1 id_list (seven named papers) | https://export.arxiv.org/api/query?id_list=2512.21980,2512.13365,2604.27645,2607.28676,2609.32388,2609.06588,2601.05272 | 2026-10-16T00:20:19Z | 200 | 147b75f0a48dc986cebb6144c54c20e9c2ed91f5dabc197edf10028aa0cb3daa | All seven abstracts read |
| q2 abs "matrix multiplication" AND ("additive complexity" OR "number of additions" OR "addition count") | https://export.arxiv.org/api/query?search_query=... | 2026-10-16T00:21:52Z | 200 | 6300d5cc16df8c85dfb30c604f3a6d3a0852e789e3e656a70b2656ad0588167a | 12 results. Relevant: 2512.21980, 2512.13365, 2511.20317 |
| q3 abs "matrix multiplication" AND (additions OR "straight-line" OR "common subexpression"), newest 60 | https://export.arxiv.org/api/query?search_query=... | 2026-10-16T00:22:02Z | 200 | 6161fafb0e67d62c9db485592c7eaa2d298f004ad79a63a4064d91f4903c4328 | Back to 2025-11. Relevant: the 3x3 papers already listed, 2512.13365, 2511.20317 |
| q4 ("fast matrix multiplication" OR "flip graph") AND (addition(s) OR additive OR "arithmetic complexity") | https://export.arxiv.org/api/query?search_query=... | 2026-10-16T00:22:13Z | 200 | dcf51cac4d29be587c320390bdf30cb45c330e61066cf9535feff66df59d1aa4 | 34 results. No new relevant work |

Web search: two queries. The first was "2x8x8" matrix multiplication rank 100 additions reduced scheme. The second was about 2026 addition-count records. They surfaced 2512.13365, ePrint 2026/849 and 2024/2063, 2606.02480, 2604.27645 and 2506.19405. None reports a 2x8x8 count other than the 424 in 2512.13365.

Per paper:

- **Perminov, arXiv:2512.13365 (v2)**, https://arxiv.org/html/2512.13365v2, fetched 2026-10-16T00:20:27Z, HTTP 200, sha256 7fbf6570ffe7c946d1561d56587f53939bfb8be542f21adb1641813f2c17de3e.
  - **Gives a count for 2x8x8: 424, comparable.** Table 3 ("Equal addition counts (proposed method matches GP-40) for schemes with best-known rank") has the row "2 × 8 × 8, 100, best known -, naive 608, GV 427, GP-5 424, GP-40 424, Proposed 424".
  - The convention is the same: "This work focuses on schemes where all coefficients in U, V, W are restricted to the set {−1, 0, 1}". This is the source of the repository's cr424 file.
  - **Table 6 does not include 2x8x8.** Its rows are 4x7x8, 4x8x8, 5x7x8, 6x6x10, 7x7x7, 7x8x8 and 8x8x8. The component-wise minimum gives no lower 2x8x8 value.
  - 418 is below 424.
- **Perminov, arXiv:2512.21980** (abstract in q1): 3x3x3 only. "achieving a rank-23 scheme with only 58 scalar additions". No 2x8x8 count.
- **Sun, arXiv:2604.27645** (abstract in q1): 3x3x3 only. "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions". No 2x8x8 count.
- **Karunaratne and Idamekorala, arXiv:2607.28676** (abstract in q1): 3x3x3 only. "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices." No 2x8x8 count.
- **Stapleton and Perminov, arXiv:2609.32388** (abstract in q1): 3x3x3 only. It is also not comparable: "using 51 additions and subtractions in alternative bases". No 2x8x8 count.
- **Nielsen, arXiv:2609.06588** (abstract in q1): 3x3x3 only. It is also not comparable: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change". No 2x8x8 count.
- **Martensson, Stankovski Wagner and Stapleton, arXiv:2601.05272** (abstract in q1): 3x3x3 only, "59 additions, still without a basis change". No 2x8x8 count.
- **Martensson and Stankovski Wagner, IACR ePrint 2026/849**
  - Fetches:
    - Abstract page https://eprint.iacr.org/2026/849, fetched 2026-10-16T00:20:49Z, HTTP 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b.
    - PDF https://eprint.iacr.org/2026/849.pdf, fetched 2026-10-16T00:20:49Z, HTTP 403, a Cloudflare "Just a moment..." challenge, sha256 1c5f50de88351330dd5d07b8b3c852f086606819adaec0a90dc6dc073d32778f. It was not retried.
    - In its place I read the operator's hand-downloaded text extraction (sha256 of the text file 99b19def9c130bd95e7dd894fdb4d172b5f87bf5a0344620b2d9c02d9307de60).
  - Convention: the abstract says "optimizing the number of additions in Strassen-type matrix multiplication schemes for larger matrix sizes, and without any change of basis". Table 3.4 is "Algorithms over Z". Table 3.5 is over Z2, which is not comparable.
  - **Coverage: this format is outside the paper's range.** The abstract says "schemes with dimensions up to (n, m, k) = (5, 7, 10)".
  - Tables 3.1 to 3.6 contain these scheme codes: 222-7, 223-11, 224-14, 225-18, 226-21, 227-25, 228-28, 232-11, 233-15, 234-20, 235-25, 236-30, 244-26, 245-33, 246-39, 247-45, 248-51, 255-40, 256-47/48, 266-56, 322-11, 323-15, 333-23, 334-29, 335-36, 336-42, 343-29, 344-38, 345-47, 346-56, 348-74, 353-36, 355-58, 356-68/71, 357-80, 359-105, 366-85, 422-14, 423-20, 433-29, 444-47/49, 445-60..63, 446-74, 447-85, 455-73/76, 456-90/93, 457-104, 459-139, 466-106/116, 467-123, 477-144, 522-18, 555-93..98, 556-110/116, 557-127/128/134, 566-130/144, 567-150, 577-176, 579-234, 666-153/164, 667-183.
  - No code 288, 828 or 882 appears, in any orientation, and no text matches "2 × 8 × 8". **The paper gives no count for 2x8x8 at rank 100.**
- **Hells and others' fmm_add_reduction** (the authors' repository)
  - Fetched once: https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1 at 2026-10-16T00:20:49Z, HTTP 200, sha256 dfdf1cd6a43106f75700703a917a5bb0ecdb971b27858e2bceafeb5718df1573.
  - The response is truncated at 65074 entries, but the top two levels are complete. algorithms/ holds grey and hells_bells. Grey's files are 234, 322, 323, 333, 343, 422, 423, 433, 442 and 522. hells_bells has the folders 222, 223, 224, 225, 226, 227, 228, 233, 234 and 333.
  - The listing is path-sorted and reaches 333, so a folder named 288 would have appeared before it and does not exist. No path contains 288-100 or 2x8x8. **No count for 2x8x8.**
- **Perminov, arXiv:2511.20317** (Ternary Meta Flip Graphs), https://arxiv.org/html/2511.20317v2, fetched 2026-10-16T00:22:30Z, HTTP 200, sha256 4724a50e77f0c8e2e4820c9efda3ac3177e7994223a394403a4e7dc9669fcfb6.
  - It counts additions naively, so it would not be comparable: "minimizing naive additive complexity".
  - The text never mentions 2x8x8 in any orientation. No count.
- **Perminov, arXiv:2606.02480** (Meta Flip Graph meets Serendipitous Product), https://arxiv.org/html/2606.02480, fetched 2026-10-16T00:23:00Z, HTTP 200, sha256 0f74f2206ae4add9ba08652a6718938b36ac0a987404ea1a019353673fcda37d. The text never mentions 2x8x8 in any orientation. No count.
- **Dumas, Pernet, Sedoglavic and others, arXiv:2506.19405** (accurate recursive matrix multiplication, PLinOpt), https://arxiv.org/html/2506.19405, fetched 2026-10-16T00:23:00Z, HTTP 200, sha256 c9f7f266a2145958d2520a9b355b771ab827527ab26349b94287d38f528243db. The text never mentions 2x8x8 in any orientation. No count.

## Comparison

- Comparable counts found for 2x8x8 at rank 100 under the reduced ternary convention:
  - 424 in Perminov's live addition_reduced_ZT, the minimum over one file.
  - 424 in arXiv:2512.13365, Table 3.
- No other source gives a count:
  - reduced_known.json, README and CHANGELOG: none.
  - Lille page: no count and no cited complexity variant.
  - matmulcatalog: adds cell "—".
  - ePrint 2026/849: no row, and the format is outside its range.
  - fmm_add_reduction: no file.
  - No merged V3R1T4S package and no open pull request.
- 418 is strictly below 424, by 6. It is not a tie.
- Rank 100 equals the best rank in fmm_sota.json.

This panel seat checks novelty only. It does not re-verify that the program is correct.

unresolved: none. The ePrint 2026/849 PDF URL returned HTTP 403 (Cloudflare challenge) and was not retried, but its full text was read from the operator's hand-downloaded copy, which settles that the paper has no 2x8x8 row. The fmm_add_reduction tree response was truncated, but path order shows there is no 288 folder. Neither could plausibly hold a comparable lower count for 2x8x8 at rank 100.

verdict (full criterion): PASS. 418 is strictly below the minimum live reduced count of 424 in Perminov's repository. It is also below every other comparable count found: arXiv:2512.13365 Table 3 gives 424, and the Lille page, matmulcatalog COVERAGE.md, ePrint 2026/849, fmm_add_reduction, TROPHY_CASE.md, open pull requests and merged packages give none.

verdict (p1, strictly fewer than Perminov's live count, same convention): PASS (418 is less than 424). Note: the bank's own enumerated p1 is about 3x3x3 rank 23 and does not apply to this format. This p1 verdict uses the brief's definition.

pass: true
