# Novelty skeptic: add-4x6x8-cr476

context: Claude Code subagent (Opus 5.5), fresh context

Claim under test: a straight-line program for format 4x6x8 at rank 140 using 476 additions/subtractions under Perminov's reduced convention, against 551 in Perminov's repository. Target: fmm-additive-complexity-records.

Claim folder integrity: all 8 entries of claim.SHA256SUMS check OK (sha256 of object/4x6x8_m140_cr476_ZT_reduced.json = 45256d75a05660145a239129ba59524edf864bbda68bcf5297be8fdf7c38158e).

Method: one plain curl GET per URL, User-Agent 'V3R1T4S-research (honest client; curl)', no retries. Saved pages are in novelty_ws/ next to this folder.

## Primary table and status pages

| Source | URL | UTC fetch | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov repo tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T12:13:23Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | truncated=false. addition_reduced_ZT holds 195 files. The only one for 4x6x8 (any axis order) is schemes/results/addition_reduced_ZT/4x6x8_m140_cr551_cn1248_ZT_reduced.json, so cr = 551 and the minimum is 551. naive_addition_reduced_ZT (126 files) and schemes/known/fmm_add_reduction (48 files) have no 4x6x8 file. The only other 4x6x8 file is schemes/known/tensor/4x6x8_tensor.mpl, which has no count. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T12:13:26Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | No "4x6x8-140" key. The largest formats listed are "4x5x6-93" (Z 542, Z2 465) and "4x6x6-116" (Z2 581). |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T12:13:26Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | Rank table row: "`4x6x8` \| 140 \| 140 \| 140 \| 2.819769913". It states no addition count for 4x6x8. Convention: "`reduced` - number of additions after elimination of common subexpressions and simplification." |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T12:13:27Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No mention of 4x6x8 and no addition count for it. The newest entry is 09/10/2026. |
| Lille per-format page | https://fmm.univ-lille.fr/4x6x8.html | 2026-10-15T12:13:27Z | 200 | 3d257dc6355ae9225f54d2bd686a90fccb47070c154cc485dc3603e8cfdb4de9 | Rank 140. "The algorithm ⟨4×6×8:140⟩ is the (Kronecker) tensor product of ⟨2×2×2:7⟩ with ⟨2×3×4:20⟩." There is no Commentaries section, no "complexity" variant, and no cited work stating an addition or operation count. It links to the maple tensor, LRP, raw evaluation and symmetry files, none of which states a count. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T12:13:28Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row "`⟨4,6,8⟩` \| — \| **✓ 140** Dronperminov-cr551_cn1248_ZT_reduced \| — \| — \| **140** in R/Q/Z \| — \| —". The adds cell is empty (—). In any case its adds column is the naive nz(U)+nz(V)+nz(W)−2r−n·p count, which does not compare with reduced counts. No lower comparable count is stated. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T12:13:28Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48. Entry {"format": [4, 6, 8], "rank": 140, "exponent": 2.81977}. Rank 140 is the best known rank, so the claim's rank is eligible. |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T12:13:28Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | No fmm-additive-complexity-records row and no 4x6x8 entry. The only matrix-multiplication rows are rank records for formats 13x14x14 to 15x16x16. |
| V3R1T4S open PRs | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T12:13:28Z | 200 | 13f1b324a8cfa79c158feb8e70b0443f85468b9e5876637c06056247704260c2 | 44 open PRs, with every title and body searched. Four are for this target: #162 (5,6,7 rank 150, 582), #161 (4,6,7 rank 123, 469), #159 (5,6,7 rank 150, 652) and #149 (4,6,7 rank 123, 503). None mentions 4x6x8 in any axis order or rank 140, so no competing open claim exists for this cell. |

The tree, reduced_known.json, README, CHANGELOG, Lille page, COVERAGE.md and fmm_sota.json hashes are identical to those in the author's table-record. The tables have not changed since the author's fetch.

## Literature (last 24 months)

arXiv export API: 4 requests.
- Request 1 was the id_list of the seven named papers over http. It returned 301 with an empty body.
- Request 2 was the same id_list over https, fetched 2026-10-15T12:14:55Z, HTTP 200, sha256 ef5f9907064d85c73b966830ea2a6d460258fb98ee173dbc17bc0dac59e35f18.
- Request 3 was au:Martensson AND abs:"matrix multiplication", fetched 12:16:28Z, HTTP 200, sha256 c1b514fb1f93ba26c4834df54c5163a2b58b9ecc21f8df5866174b60882711cb, 0 results.
- Request 4 was abs:"matrix multiplication" AND (additions OR "additive complexity"), newest first, 60 of 371 results back to 2025-11, fetched 12:16:29Z, HTTP 200, sha256 b26cfa6a923163bd2a514da18f9c7c047cd4d02f83ab8b6799a03b997496f47b.

Request 4 surfaced no paper on addition counts for 4x6x8 beyond those below. The web search for "4x6x8 additions rank 140" also found none.

- **Perminov, arXiv:2512.13365v2** (PDF https://arxiv.org/pdf/2512.13365v2, fetched 2026-10-15T12:15:56Z, HTTP 200, sha256 82aff81bf22f80c13cf559f1c42ada3fecda51fb4efc773c3e7ee1ae5b135c27). It gives a count for 4x6x8. Table 1 ("Schemes with optimal rank achieving new SOTA addition counts") has the row "4×6×8 140 1248 576 558 558 551": naive 1248, GV 576, GP-5 558, GP-40 558, proposed 551. This is comparable: the paper treats "fast matrix multiplication algorithms with ternary coefficients {-1,0,1}" by common-subexpression elimination with no basis change, which is the same convention as the repository's cr551 file. The minimum is 551. Table 6 ("Component-wise addition counts for schemes improvable by approaches result combination") lists 4×7×8, 4×8×8, 5×7×8, 6×6×10, 7×7×7, 7×8×8 and 8×8×8. 4x6x8 is not among them, so there is no lowered combined count for this format. The GP-40 column is the Mårtensson–Wagner fmm_add_reduction tool, which reaches 558 on this scheme.
- **Perminov, arXiv:2512.21980** (abstract via request 2). No count for 4x6x8. Scope: "achieving a rank-23 scheme with only 58 scalar additions". That is 3x3x3 only.
- **Mårtensson and Stankovski Wagner, IACR ePrint 2026/849**, "On Why and How to Minimize the Arithmetic Complexity of Fast Matrix Multiplication Algorithms".
  - Fetches: the abstract page https://eprint.iacr.org/2026/849 (2026-10-15T12:14:45Z, HTTP 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b) and the PDF https://eprint.iacr.org/2026/849.pdf (2026-10-15T12:14:45Z, HTTP 403, a Cloudflare "Just a moment..." challenge, sha256 859478d2d293d1099c27914dd930fcd95cc2f4ee94399b2f3b7f4568a3340cc0; not retried).
  - Coverage sentence: "We implement of our methods and use them to optimize the number of additions for schemes with dimensions up to $(n, m, k) = (5, 7, 10)$." The convention matches: "without any change of basis".
  - 4x6x8 is inside that range (4 ≤ 5, 6 ≤ 7, 8 ≤ 10), so the paper could in principle contain a count for this format. Whether it covers rank 140 cannot be settled without the PDF.
  - Indirect evidence from the authors' repository, all fetched once with HTTP 200:
    - Tree https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1 (12:14:45Z, sha256 dfdf1cd6a43106f75700703a917a5bb0ecdb971b27858e2bceafeb5718df1573) is truncated at 65074 entries.
    - The directory listings fill the gaps: algorithms/ (12:15:30Z, sha256 1058ca768cab872a4c6f811c8a6be8661fff93566c5e163dfbe9172e1887c77f), algorithms/moosbauer (12:15:38Z, sha256 e2eacfca2c01f6f9132f395b8736e603cfa21a7f5a89f2cbf97a6cad36c17eb3), algorithms/other (12:15:39Z, sha256 db23b35fa8b428128e7e2b2fe1c1763fa260e571b1a4e3e023c31523871786f8), algorithms/hells_bells (12:15:39Z, sha256 f3e52cb096f5292ed759cf99810bf9e4b09a287716b36e4ef531f9653d8e8754), other/unsorted (12:15:56Z, sha256 cf0125af11315d657903cda62dbea6e9301480431fd4edaf23a65fabf508ba5b), unsorted/deepmind (sha256 397dcd441b00006446161d6f1a1543398620617fd6aea0f744ad3faa0096aca4), unsorted/kauerswood (sha256 ce01a4d50979d9f765fd0894e04486615acbfb89276eb9b62a95cc95e8a86ec3) and unsorted/misc (sha256 65fc231f285fa375c108a917a996e8c779400347225edda69e20de7d07264c96), the last three at 12:16:06–07Z. README: https://raw.githubusercontent.com/werekorren/fmm_add_reduction/main/README.md (12:15:31Z, sha256 37b319e0a3cb960cb612d56e1b53ac61bdfcdd673a0cd9ebafd9599cc055e842).
    - The schemes found:
      - moosbauer: 223 to 666, with formats up to 466:116, 566:144 and 666:153/164.
      - kauerswood: 456, 457, 466, 467, 477, 556, 557, 566, 567, 577, 667.
      - hells_bells: 222 to 228, 233, 234, 333, 432, 532.
      - grey and other: small formats only.
    - No 468 scheme (any order) appears in the repository. Perminov's reduced_known.json, which records known counts, has no 4x6x8 entry. Perminov's Table 1 shows the authors' own GP-40 reducer reaching 558 on 4x6x8:140.
  - Status: unresolved (PDF blocked). A comparable count below 476 for 4x6x8:140 is possible but not indicated anywhere.
- **Sun, arXiv:2604.27645**. No count for 4x6x8: "a rank-$23$ algorithm for general $3\times3$ matrix multiplication that uses $56$ additions/subtractions".
- **Karunaratne and Idamekorala, arXiv:2607.28676**. No count for 4x6x8: "We give a 55-addition realization of rank-23 multiplication of two arbitrary $3\times3$ matrices."
- **Stapleton and Perminov, arXiv:2609.32388**. No count for 4x6x8, and not comparable in any case: "a rank-23 algorithm for $3\times3$ matrix multiplication using 51 additions and subtractions in alternative bases" (basis change).
- **Nielsen, arXiv:2609.06588**. No count for 4x6x8, and not comparable: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change" (3x3 only).
- **Mårtensson, Stankovski Wagner and Stapleton, arXiv:2601.05272**. No count for 4x6x8: "finding an algorithm requiring only 59 additions, still without a basis change" (3x3x3 only).
- **Mårtensson, Stankovski Wagner and Stapleton, "Hell's Bells", IACR ePrint 2026/1688** (https://eprint.iacr.org/2026/1688, 2026-10-15T12:17:55Z, HTTP 200, sha256 8269492c23b40e63ae3303a37993bdd76d42ecd633dbbfc1bea2099ad587b8ff). No count for 4x6x8 in the abstract: "efficiently generating fast matrix multiplication (FMM) algorithms of small but arbitrary dimensions ... For $(n,m,k) = (2,2,k)$, our method performs particularly well." Its published schemes (hells_bells/ in fmm_add_reduction) stop at 228, 234, 333, 432 and 532.
- **Perminov, arXiv:2606.02480** (https://arxiv.org/pdf/2606.02480, 12:17:14Z, HTTP 200, sha256 a68a85ea35e138bd678cb7a2f3b1069bb28490d1eedf49b6fc440074f8b83a4f). This is a rank paper with no addition count for 4x6x8: "The Sedoglavic catalog [2] focuses exclusively on ranks and does not track additive complexity. A systematic study of additive complexity across many formats is still missing".
- **Dumas, Pernet and Sedoglavic, arXiv:2506.19405** (https://arxiv.org/pdf/2506.19405, 12:17:14Z, HTTP 200, sha256 384c14f348121522c1a6548c4a6fd2927cb9e19e433d552b09eec327b3275061). No count for 4x6x8. Table 3 ("Number of Additions for some matrix multiplications") lists only 3×3×3, 4×2×4, 4×3×2, 4×3×3 and 5×2×2. Its PLinOpt counts also handle "general integer and rational coefficients" with multiplications/divisions, which is a different class.

A sanity bound from my own arithmetic, not a published source: nesting the two factor programs recursively gives 506 or 516 additions.
- Winograd 2x2x2 over 2x3x4 blocks costs 4·6 + 4·12 + 7·8 + 7·54 = 506.
- 2x3x4 over 2x2 blocks costs 54·4 + 20·15 = 516.

Both are above 476, so the naive Kronecker construction does not supply a lower count.

## Verdict

- Comparable counts read for 4x6x8 at rank 140: 551 (Perminov live repository and arXiv:2512.13365 Table 1), 558 (fmm_add_reduction GP-40/GP-5 in the same table) and 576 (GV). Lille states none. COVERAGE.md adds is empty and its convention is not comparable. reduced_known.json has none. No open PR or trophy row exists for this cell.
- Full criterion: 476 is strictly less than 551, the minimum over every comparable source read. Lille gives no lower count and COVERAGE.md gives no lower comparable count. Rank 140 equals the fmm_sota.json best rank. PASS on novelty, assuming the other skeptics confirm correctness and the count.
- Partial win p1, as the brief defines it (strictly fewer than Perminov's live count in the same convention): PASS, 476 against 551 (−75). The bank's enumerated p1 is a different cell (3x3x3 rank 23, against 58). This claim does not touch that cell, and it is not claimed for it.

unresolved: IACR ePrint 2026/849 PDF (HTTP 403 Cloudflare challenge, not retried). Its stated range "up to (5,7,10)" includes 4x6x8, so it could in principle hold a comparable count. Nothing found shows it covers 4x6x8 at rank 140: the authors' repository has no 4x6x8 scheme, reduced_known.json has no entry, and the authors' reducer scores 558 on this scheme in arXiv:2512.13365. Plausibility of a comparable count below 476 is low, but it is not excluded.

pass: true
