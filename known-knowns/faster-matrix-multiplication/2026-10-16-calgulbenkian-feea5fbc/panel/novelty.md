# Novelty check: 4x4x6 rank 73, 256 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Claim folder hashes checked against claim.SHA256SUMS for CLAIM.md, INDEX.csv, table-record/README.md and the object file: all match. Each source below was fetched once with curl and User-Agent 'V3R1T4S-research (honest client; curl)'. Pages were saved in novelty_ws/ under the names shown. Note: novelty_ws/ already held files from an earlier run (local times 16:29 to 16:33) when I started; I did not read or use them, and every value below comes from my own fetches.

## Primary table and status pages

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov repo tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T23:53:57Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | Tree not truncated. Exactly one addition_reduced_ZT file for 4x4x6: 4x4x6_m73_cr280_cn540_ZT_reduced.json, so cr 280 is the minimum. No permuted 4x6x4 or 6x4x4 reduced files. naive_addition_reduced_ZT holds 4x4x6_m73_c534_ZT and 4x4x6_m73_c540_ZT; these are naive counts under another convention and are not comparable. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T23:53:58Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | No "4x4x6-73" key. The only 4x4x6 entry is "4x4x6-74": {"Z": 467, "Z2": 360}. It is at rank 74, not 73, and Z2 is a different ring, so it is not comparable. Both values are above 256 anyway. |
| Perminov README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T23:53:58Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | 4x4x6 appears only in the rank tables (rank 73, Z/Q; and "73 (?), 73, 73, 2.819981689"). It states no addition count for 4x4x6. |
| Perminov CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T23:53:58Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No line mentions 4x4x6. None of the "Reduced additions improvement" entries is for this format. |
| Lille per-format page | https://fmm.univ-lille.fr/4x4x6.html | 2026-10-15T23:53:58Z | 200 | f30768b4561049c721e286835986e541845a62f27b39ac16bef0a002bd17809e | "Description of fast matrix multiplication algorithm: 4x4x6:73", taken from "Alexey Vladimirovich Smirnov. Bilinear algorithm for matrix multiplication. January 2023." There is no Commentaries section, no cited complexity variant, and no addition or operation count. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T23:53:59Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | The 4,4,6 row shows rank 73 (Dronperminov-ZT) with adds "+565". The legend says: "`+N adds` is the addition count (`nz(U)+nz(V)+nz(W) − 2r − n·p`)". That is a naive count with no common-subexpression sharing, so it is not comparable to a reduced count. It is above 256 anyway. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T23:53:59Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48. Entry {"format": [4, 4, 6], "rank": 73, "exponent": 2.819982}. Rank 73 is the best known rank, so the scheme is eligible. |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T23:54:00Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | Its matrix-multiplication rows are rank records for large formats only. It has no addition-count row and no 4x4x6 row. |
| V3R1T4S open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T23:54:00Z | 200 | 12473dc228f9f201566453a3e87b1d4ed24a37bf8eca1240f665a443a7148a2e | 16 open pull requests (#9, #30, #153, #154, #190 to #201). I read every title and body. None names fmm-additive-complexity-records and none mentions 4x4x6 in any notation. The only fmm claim is #197, a rank claim for 13x15x15. |
| known-knowns fmm listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-15T23:54:01Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 merged package folders, listed below. |
| known-knowns family INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-15T23:54:55Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | Rank rows only, for formats 13x14x14 and larger. No 4x4x6 row. |
| known-knowns family README.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/README.md | 2026-10-15T23:54:55Z | 200 | 740321f0f9287e13ee0f1dd229c47a974b49393560a453df125ad850b359ba07 | No 4x4x6 and no addition count. |

### Merged packages: each package's INDEX.csv, fetched once from raw.githubusercontent.com

I first tried each package's API contents listing once. The first 12 listings returned 200. The last 9 returned 403 at 2026-10-15T23:55:11Z to 23:55:14Z: "API rate limit exceeded", the same body for all 9 (sha256 3209519d06deb9f4f950810899ddc6fafba9bcfb3fb8cad8b5e1b30459ace147). I did not retry those URLs. Instead I fetched each package's INDEX.csv once from a different host (raw), and all 21 returned 200 between 23:55:28Z and 23:55:32Z. The 12 addition-count packages are:

- 4x6x6 r105: 373 against 430
- 5x7x7 r176: 699 against 788
- 6x6x7 r183: 695 against 769
- 6x8x8 r266: 993 against 1161
- 4x6x8 r140: 476 against 551
- 6x6x6 r153: 588 against 655
- 5x6x7 r150: 582 against 664
- 4x6x7 r123: 469 against 517
- 6x6x8 r203: 719 against 836
- 5x5x8 r144: 556 against 620
- 5x6x6 r130: 502 against 562
- 5x5x5 r93: 358 against 383 (drzuzzjen)

The other 9 packages are rank packages: 13x15x15, 15x16x16, 13x14x15, 13x14x14, 15x15x16, 13x13x15, 14x16x16, 11x13x16 and 13x13x14. No merged package covers 4x4x6 or any permutation of it. The per-package hashes are in novelty_ws/kkidx_log.txt.

## Literature (last 24 months)

arXiv export API: four queries, each sent once. The first http:// attempts returned 301 redirects with empty bodies at 23:56:16Z to 23:56:17Z. I followed each redirect once to its https:// target, and all four returned 200:

- id_list for the six named papers: 23:56:25Z, sha256 f51ecc0487cea8cfa18d26891e64141549e52651794eb62dac6698ab25774ca9
- abstract search "matrix multiplication" AND additions, 60 newest: 23:56:29Z, sha256 2ab5ad472c6cc9967c147c0b6aac0271a803e72d2a930da797e0947307a82931
- author search Martensson AND Wagner: 23:56:32Z, sha256 2671f52d109c07383612fcb425496d906d79afb5c0db8162820c69720de192b1
- "additive complexity" AND matrix, 40 newest: 23:56:39Z, sha256 78f6ab3b710661aa4814bec56f9c7677e23670be6becad45ed012be162383f49

I also ran four web searches. No source states a count for 4x4x6 rank 73 other than 280 and higher.

- **Perminov, arXiv:2512.13365v2.** Fetched https://arxiv.org/pdf/2512.13365v2 at 2026-10-15T23:57:10Z, HTTP 200, sha256 82aff81bf22f80c13cf559f1c42ada3fecda51fb4efc773c3e7ee1ae5b135c27.
  - It gives a count for this format. Table 1 ("Schemes with optimal rank achieving new SOTA addition counts") has the row "4×4×6 73 540 288 282 281 280". The columns are Naive, GV, GP-5, GP-40 and Proposed. So the best is 280, and Martensson-Wagner's fmm_add_reduction (GP-40) reaches 281.
  - The count is comparable. The abstract says the method is "for reducing additive complexity in fast matrix multiplication algorithms with ternary coefficients {-1,0,1}". This is the same reduced convention and the same rank. 256 is below 280.
  - 4x4x6 is not in Table 6. That table lists only 4×7×8, 4×8×8, 5×7×8, 6×6×10, 7×7×7, 7×8×8 and 8×8×8.
- **Perminov, arXiv:2512.21980.** No count for 4x4x6. The abstract covers only 3x3: "achieving a rank-23 scheme with only 58 scalar additions."
- **Sun, arXiv:2604.27645.** No count for 4x4x6: "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions."
- **Karunaratne and Idamekorala, arXiv:2607.28676.** No count for 4x4x6: "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices."
- **Stapleton and Perminov, arXiv:2609.32388.** No count for 4x4x6. It is 3x3 only, and it uses a basis change, so it would not be comparable in any case: "using 51 additions and subtractions in alternative bases."
- **Nielsen, arXiv:2609.06588.** No count for 4x4x6. It is 3x3 only and uses a basis change, so it would not be comparable: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change."
- **Martensson, Stankovski Wagner and Stapleton, arXiv:2601.05272.** No count for 4x4x6; it is 3x3 only ("an algorithm requiring only 59 additions, still without a basis change").
- **Perminov, arXiv:2606.02480.** Fetched https://arxiv.org/abs/2606.02480 at 23:58:32Z, HTTP 200, sha256 5d9c3e5e3342c9ac31483958c43e1230a2480105b0a0e4ac5bde309537dac043. It reports ranks and coefficient types only, with no addition counts: "ranks are improved for 207 formats".
- **Martensson and Stankovski Wagner, IACR ePrint 2026/849.**
  - Abstract page https://eprint.iacr.org/2026/849: 23:57:11Z, HTTP 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b.
  - PDF https://eprint.iacr.org/2026/849.pdf: 23:57:11Z, HTTP 403 with a "Just a moment..." challenge page, sha256 821808858e20a5892f7288245d4b36d7112e56b1ba9f9fe7c6a734ca6545c635. Not retried.
  - Coverage: "We implement of our methods and use them to optimize the number of additions for schemes with dimensions up to (n, m, k) = (5, 7, 10)" and "for larger matrix sizes, and without any change of basis". 4x4x6 is inside that range, and the convention would be comparable.
  - The abstract gives no count, and I could not read the paper's tables.
  - No arXiv or conference copy was found (one arXiv author query, plus web searches). The repository README https://raw.githubusercontent.com/werekorren/fmm_add_reduction/main/README.md (23:58:32Z, HTTP 200, sha256 37b319e0a3cb960cb612d56e1b53ac61bdfcdd673a0cd9ebafd9599cc055e842) describes only the tool and lists no counts.
  - The repository tree https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1 was NOT fetched. The GitHub API quota for this address was exhausted (remaining 0, reset 2026-10-16T00:12:21Z), so a request would have been a certain 403.
  - Evidence on the count: Perminov's Table 1 shows that this group's earlier tool (GP-40) gave 281 on this exact scheme.
- **Martensson, Stankovski Wagner and Stapleton, "Hell's Bells", IACR ePrint 2026/1688.** This is the "Hells and others" fmm_add_reduction work.
  - Abstract page https://eprint.iacr.org/2026/1688: 23:58:12Z, HTTP 200, sha256 8269492c23b40e63ae3303a37993bdd76d42ecd633dbbfc1bea2099ad587b8ff.
  - PDF: 23:58:12Z, HTTP 403 challenge page, sha256 00a26735263d8c80d9c76d3eaca16ac7992ad4daa7e18ed07e25c9663c88c45d. Not retried.
  - Abstract: "We achieve record-low arithmetic (additive) complexity for various combinations of dimensions. For (n,m,k) = (2,2,k), our method performs particularly well." It does not name 4x4x6 or give any count.

unresolved: IACR ePrint 2026/849 full text (PDF 403 challenge), IACR ePrint 2026/1688 full text (PDF 403 challenge), and the werekorren/fmm_add_reduction repository tree (not fetched; GitHub API quota exhausted). 2026/849 covers formats up to (5,7,10) without basis change, so it could plausibly hold a comparable count for 4x4x6. No readable source says it does so at rank 73. The same group's earlier tool reached 281 on this scheme, so a count at or below 256 there is possible but unlikely. 2026/1688 could plausibly include 4x4x6, but its abstract highlights (2,2,k). Neither unread source is known to cover this format at rank 73.

## Verdicts

- Full criterion: PASS, provisional on the unresolved items above. 256 is strictly below all of these:
  - Perminov's live minimum cr, 280 (the only addition_reduced_ZT file for 4x4x6 at rank 73)
  - his paper's 280, and GP-40's 281
  - the Lille page, which states no count
  - matmulcatalog's +565, which is a naive count and not comparable anyway
  - reduced_known.json, which has only rank 74 (467 over Z, 360 over Z2) and is not comparable
  - every open pull request and merged package, none of which covers 4x4x6
- Rank 73 is the fmm_sota.json best rank for [4, 4, 6].
- Partial win p1 (strictly fewer than Perminov's live count, same convention): PASS in the sense asked here, 256 < 280. Note that the bank's own p1 is defined only for 3x3x3 rank 23, so this format does not literally qualify as the bank's p1.

pass: true
