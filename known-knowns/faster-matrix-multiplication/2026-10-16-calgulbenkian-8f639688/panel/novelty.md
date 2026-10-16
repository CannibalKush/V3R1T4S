# Novelty check: fmm-additive-complexity-records, 4x5x8 rank 118, 470 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Claim folder hashes: all eight files match claim.SHA256SUMS (shasum -c: OK). The object is object/4x5x8_m118_cr470_ZT_reduced.json. Its claimed count is 470 against a table value of 513.

Method: one plain curl GET per URL with User-Agent 'V3R1T4S-research (honest client; curl)'. No retries. Times come from `date -u`, status codes from `curl -w '%{http_code}'`, and each sha256 is of the saved body. Pages were saved in the panel's novelty_ws folder.

## Primary table sources

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov repository tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T23:53:59Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | truncated: false, 6637 entries. Exactly one addition_reduced_ZT file for 4x5x8 at rank 118: `4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json`, so the minimum cr is **513**. No addition_reduced_ZT file exists for any permutation of 4x5x8. The naive_addition_reduced_ZT files `4x5x8_m118_c1463_ZT` and `4x5x8_m118_c1521_ZT` use the naive convention and do not compare. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T23:54:01Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | 33 keys; none for 4x5x8, or any permutation of it, at rank 118. No entry. |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T23:54:01Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | 4x5x8 appears only in rank tables: "`4x5x8` \| [118](schemes/results/ZT/4x5x8_m118_ZT.json) \| `Z/Q`" and "`4x5x8` \| 118 (122) \| 118 \| 118". No addition count is given for 4x5x8. |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T23:54:01Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | The "Reduced additions improvement" sections list 2x2x6, 2x2x7, 2x2x8, 2x2x9, 2x2x10, 2x3x3, 2x3x5, 2x3x6, 2x3x7, 2x3x8, 2x4x4, 2x4x5, 2x4x6, 3x3x4, 3x3x5, 3x4x4 and 3x3x3 (58). None of them is 4x5x8. |
| Lille per-format page | https://fmm.univ-lille.fr/4x5x8.html | 2026-10-15T23:54:01Z | 200 | 11e5204283178c8e5cc37ed61832e7d3d5da95e0faab8cf4c67fdae1b5399c80 | "⟨4×5×8:118⟩ ... is taken from: Andrew I. Perminov. FastMatrixMultiplication, GitHub, February 2026." There is **no Commentaries section** and no cited complexity variant. No addition or operation count appears on the page. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T23:54:02Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row "`⟨4,5,8⟩` \| **✓ 118** Dronperminov-ZT ... \| +1521". Its legend says: "`+N adds` is the addition count (`nz(U)+nz(V)+nz(W) − 2r − n·p`)". This is a naive count with no common-subexpression elimination, so it is not comparable to a reduced count. It is also above 470. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T23:54:02Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48; entry `{"format": [4,5,8], "rank": 118, "exponent": 2.820013}`. Rank 118 is the best known rank, so the bank's eligibility rule holds. |

All seven primary sha256 values are identical to the author's table-record. The pages have not changed since the author fetched them.

## This repository (V3R1T4S)

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T23:54:03Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | No row mentions additions, the target fmm-additive-complexity-records, or 4x5x8. The matrix multiplication rows are rank records only. |
| Open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T23:54:03Z | 200 | 12473dc228f9f201566453a3e87b1d4ed24a37bf8eca1240f665a443a7148a2e | 16 open PRs (201, 200, 199, 198, 197, 196, 195, 194, 193, 192, 191, 190, 154, 153, 30, 9). I read every title and body. None mentions 4x5x8, fmm-additive-complexity-records or an addition count. The only FMM PR is #197, a rank claim for 13x15x15. |
| known-knowns FMM listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-15T23:54:03Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 dated package folders. |
| known-knowns INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-15T23:55:08Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | Rank schemes only (13x14x14 through 15x16x16). |
| Each package's INDEX.csv (21 files, one raw GET each) | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/ followed by the folder name and /INDEX.csv | 2026-10-15T23:55:28Z to 23:55:31Z | 200 (all 21) | per-file hashes are kept in the workspace fetch log | There are 12 merged addition-count packages: 4x6x6 (373), 5x7x7 (699), 6x6x7 (695), 6x8x8 (993), 4x6x8 (476), 6x6x6 (588), 5x6x7 (582), 4x6x7 (469), 6x6x8 (719), 5x5x8 (556), 5x6x6 (502) and 5x5x5 (358, drzuzzjen). **None covers 4x5x8.** The other 9 packages are rank claims. |
| Repository tree (recursive) | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-10-15T23:55:16Z | 403 | 3209519d06deb9f4f950810899ddc6fafba9bcfb3fb8cad8b5e1b30459ace147 | The API rate limit was exceeded. I did not retry. The per-package INDEX.csv reads above already settle coverage. |

## Literature, last 24 months

arXiv export API: I ran four queries, the most allowed.
- Query 1, `http://export.arxiv.org/api/query?id_list=2512.21980,2512.13365,2604.27645,2607.28676,2609.32388,2609.06588,2601.05272`, ran at 2026-10-15T23:56:05Z and returned 301, a redirect to https with an empty body (sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855).
- Query 2 was the same id_list over https, at 2026-10-15T23:56:14Z: 200, sha256 147b75f0a48dc986cebb6144c54c20e9c2ed91f5dabc197edf10028aa0cb3daa.
- Query 3 searched abstracts for "matrix multiplication" AND (additions OR "additive complexity" OR "arithmetic complexity"), sorted by date, 60 results, at 2026-10-15T23:56:22Z: 200, sha256 cddce0ff431403e45aaeb70a5136c6cf455473602b4e8d4e7c8176f4818b264a.
- Query 4 searched for au:Stankovski OR au:Martensson OR au:Mårtensson at 2026-10-15T23:56:49Z: 200, sha256 a94bdb7b93f0bd7a6435ae9ee001badb8a7b997c0000f6c0ef6567c2a5ee2158. It found no arXiv copy of ePrint 2026/849.

I also ran two web searches, one for the 2026/849 title and one for "4x5x8 matrix multiplication rank 118 additions reduced scheme". Neither surfaced a reduced count for 4x5x8 at rank 118. They did point to arXiv:2511.20317 and arXiv:2606.02480, which I checked below.

Each paper below is listed with whether it gives a 4x5x8 count and whether that count is comparable:

- **Perminov, arXiv:2512.13365v2**, "Parallel Heuristic Exploration for Additive Complexity Reduction in Fast Matrix Multiplication". PDF https://arxiv.org/pdf/2512.13365v2, fetched 2026-10-15T23:56:21Z, HTTP 200, sha256 82aff81bf22f80c13cf559f1c42ada3fecda51fb4efc773c3e7ee1ae5b135c27.
  - It gives a count for 4x5x8 and the count is comparable. The scope is ternary, from the abstract: "reducing additive complexity in fast matrix multiplication algorithms with ternary coefficients {-1,0,1}". The row is in Table 1, "Schemes with optimal rank achieving new SOTA addition counts": "4×5×8 118 1521 543 538 522 513". The columns are Naive 1521, GV 543, GP-5 538, GP-40 522 and Prop. 513.
  - The best comparable count is 513, the same as the live repository file. GP-40 at 522 is the Mårtensson-Wagner Greedy-Potential tool as Perminov ran it.
  - Table 6, "Component-wise addition counts for schemes improvable by approaches result combination", lists only 4×7×8, 4×8×8, 5×7×8, 6×6×10, 7×7×7, 7×8×8 and 8×8×8. **4x5x8 is not among them**, so it has no lower combined count.
- **Perminov, arXiv:2512.21980**, "A 58-Addition, Rank-23 Scheme for General 3x3 Matrix Multiplication". Abstract read from query 2. It covers 3x3x3 only: "achieving a rank-23 scheme with only 58 scalar additions." It has no 4x5x8 count.
- **Mårtensson and Stankovski Wagner, IACR ePrint 2026/849**, "On Why and How to Minimize the Arithmetic Complexity of Fast Matrix Multiplication Algorithms".
  - Abstract page https://eprint.iacr.org/2026/849: fetched 2026-10-15T23:54:04Z, HTTP 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b.
  - PDF https://eprint.iacr.org/2026/849.pdf: fetched 2026-10-15T23:54:04Z, **HTTP 403**, a Cloudflare "Just a moment..." challenge page (sha256 c5fd0d4a1b82dc6b9439195f8947330ad3f3d4cd7c7624996408809e1d410bc2). I did not retry.
  - Coverage, quoted from the abstract: "We implement of our methods and use them to optimize the number of additions for schemes with dimensions up to $(n, m, k) = (5, 7, 10)$." The paper also says it works "without any change of basis", so its counts would be comparable. **4x5x8 lies inside that range** (sorted 4 ≤ 5, 5 ≤ 7, 8 ≤ 10). The paper therefore could in principle contain a count for 4x5x8, but the abstract does not say which ranks or scheme sets it optimised.
  - Authors' repository tree https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1: fetched 2026-10-15T23:54:04Z, HTTP 200, sha256 dfdf1cd6a43106f75700703a917a5bb0ecdb971b27858e2bceafeb5718df1573. It is truncated (65074 entries). To cover the cut-off part, I fetched the GitHub directory pages once each (all HTTP 200, 2026-10-15T23:56:49Z to 23:57:27Z): algorithms, hells_bells, moosbauer, other, other/unsorted, and unsorted/deepmind, kauerswood and misc.
    - The format folders are: hells_bells 222, 223, 224, 225, 226, 227, 228, 233, 234, 333, 432 and 532; Moosbauer files up to 666; Kauers-Wood 456, 457, 466, 467, 477, 556, 557, 566, 567, 577 and 667; plus grey, other and AlphaEvolve/DeepMind sets.
    - **No 4x5x8 scheme or count appears** in any of these folders. The README describes the earlier ACDA25 paper.
  - Perminov's Table 1, above, records the Mårtensson-Wagner GP-40 method at 522 on this scheme.
  - I found no arXiv or conference copy of 2026/849.
- **Mårtensson and Stankovski Wagner, ePrint 2024/2063** (ACDA25, the predecessor). Abstract page https://eprint.iacr.org/2024/2063, fetched 2026-10-15T23:57:58Z, HTTP 200, sha256 dafa562b4f1ff2dd5beac64491d2cdb5cffc9877bc93edf087215977a55bb133.
  - Scope, quoted: "We additionally apply our algorithms to another reference set of algorithms due to Moosbauer and Kauers". It works "for dimensions including (and surpassing) the 666 limit".
  - The paper is dated December 2024. Lille dates the rank-118 4x5x8 scheme to Perminov, February 2026. So this paper gives no 4x5x8 count at rank 118.
- **Sun, arXiv:2604.27645**. It covers 3x3 only: "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions". It has no 4x5x8 count.
- **Karunaratne-Idamekorala, arXiv:2607.28676**. It covers 3x3 only: "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices." It has no 4x5x8 count.
- **Stapleton-Perminov, arXiv:2609.32388**. It covers 3x3 only, and its counts use a basis change, so they are not comparable: "using 51 additions and subtractions in alternative bases. The input and output conversions require five further additions". It has no 4x5x8 count.
- **Nielsen, arXiv:2609.06588**. It covers 3x3 only, with a basis change, so its counts are not comparable: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change". It has no 4x5x8 count.
- **Hells and others, fmm_add_reduction (hells_bells data)**. Its folders cover 222 through 532 only, as listed above. It has no 4x5x8 count.
- **Perminov, arXiv:2511.20317**, "Fast Matrix Multiplication via Ternary Meta Flip Graphs". PDF https://arxiv.org/pdf/2511.20317, fetched 2026-10-15T23:57:57Z, HTTP 200, sha256 150d6111dde1c314fe6dcdeaab2ec715f2e5d380a0f3905f09a60d2d021f9215.
  - Table 4, "Reduce naive addition complexity", gives "(4, 5, 8) 118 1566 1521".
  - These are naive counts, so they are not comparable: "The additive complexity metric used (non-zero coefficients - 2 × r − m × p)".
- **Perminov, arXiv:2606.02480**, "Meta Flip Graph meets Serendipitous Product". PDF https://arxiv.org/pdf/2606.02480, fetched 2026-10-15T23:57:57Z, HTTP 200, sha256 a68a85ea35e138bd678cb7a2f3b1069bb28490d1eedf49b6fc440074f8b83a4f.
  - It gives no addition counts. Section 5.5 only discusses the topic: "A systematic study of additive complexity across many formats is still missing".
  - It also says of Lille: "The Sedoglavic catalog [2] focuses exclusively on ranks and does not track additive complexity."
- **arXiv:2601.05272** (Mårtensson, Stankovski Wagner and Stapleton, 59 additions). It covers 3x3 only. It has no 4x5x8 count.

## Comparison

- The comparable counts I could read for 4x5x8 at rank 118 are:
  - Perminov live addition_reduced_ZT: 513.
  - arXiv:2512.13365 Table 1: 513 (Prop.) and 522 (GP-40).
  - reduced_known.json, README and CHANGELOG: no entry.
- Lille cites no complexity variant.
- matmulcatalog's 1521 is a naive count and does not compare. 470 is below it in any case.
- No merged V3R1T4S package and no open PR covers this format.
- The minimum comparable count is 513. 470 is below it by 43, so the claim strictly beats it and is not a tie.

unresolved: the ePrint 2026/849 PDF (https://eprint.iacr.org/2026/849.pdf, HTTP 403 Cloudflare challenge, not retried) could not be read. The paper's stated range "up to (5, 7, 10)" includes the format 4x5x8, and its counts (no change of basis) would be comparable. So it plausibly could contain a comparable count for 4x5x8. However, nothing I could read shows that it covers rank 118 for this format: the abstract names no scheme set, and the authors' repository has no 4x5x8 scheme. On this scheme Perminov measured their GP-40 tool at 522, which is above 513. A count from that paper below 470 is therefore possible but not known. The V3R1T4S recursive tree API call (403 rate limit) is also unread, but the per-package INDEX.csv reads cover it.

verdict (full criterion): PASS. 470 is strictly below every comparable count I read: Perminov 513, arXiv:2512.13365 513/522, no Lille variant, and the matmulcatalog naive 1521, which does not compare. No unread source is known to cover 4x5x8 at rank 118.

verdict (partial win p1, as the brief defines it: strictly fewer than Perminov's live count, same convention): PASS. Under the reduced convention, 470 is below 513. Note: the bank's enumerated p1 is about a different format (a rank-23 SLP for 3x3x3 below 58), so this claim cannot satisfy the bank's own p1 text. It stands on the full criterion.

pass: true
