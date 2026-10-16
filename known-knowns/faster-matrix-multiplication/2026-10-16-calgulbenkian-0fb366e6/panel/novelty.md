# Novelty check: 5x8x8 rank 230, 929 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Claim checked: a ternary straight-line program for the rank-230 ⟨5,8,8⟩ scheme using 929 additions under Perminov's reduced convention, against 974 in his repository.

Method: one plain curl request per page, User-Agent `V3R1T4S-research (honest client; curl)`, no redirects followed by curl, no retries of any blocked URL. Every page I fetched is saved under `novelty_ws/run_nov929/` (fetch log: `novelty_ws/run_nov929/LOG.txt`). Files that were already in `novelty_ws/` from an earlier run were not read or used.

## Primary tables (criterion parts a, b, c and eligibility)

| Source | URL | UTC fetch | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T23:54:07Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | not truncated (6637 entries). Only one addition_reduced_ZT file for 5x8x8: `5x8x8_m230_cr974_fv447_cn2747_ZT_reduced.json`, so the minimum cr is **974**. The other 5x8x8 files are naive counts of a different convention and do not compare: `naive_addition_reduced_ZT/5x8x8_m230_c2638_ZT` and `..._c2741_ZT`. No 8x5x8 or 8x8x5 files. The hash matches the author's fetch, so the tree has not changed. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T23:54:08Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | 33 keys. The largest is 4x6x6-116. There is no 5x8x8-230 key. |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T23:54:09Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | The only 5x8x8 line is the rank row `5x8x8 / 230 / 230 / 230 / 2.828247238`. No addition count is given for 5x8x8. |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T23:54:09Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | The "Reduced additions improvement" entries cover only 2x2xk, 2x3xk, 2x4xk, 3x3x4, 3x3x5 and 3x4x4. Nothing for 5x8x8. |
| Lille 5x8x8 page | https://fmm.univ-lille.fr/5x8x8.html | 2026-10-15T23:54:09Z | 200 | 60dc7bc3f88fd6087d701c539f604aaafbb815b676f6ad9810b03be58a38d173 | Shows ⟨5x8x8:230⟩, built from 3x4x4:38 and 2x4x4:26 blocks. Section headings: type, Algorithm definition, Algorithm description. There is **no Commentaries section**, no cited work, no complexity variant, and no addition or operation count. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T23:54:11Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Cell `⟨5,8,8⟩`: "✓ 230 Dronperminov-c2638_ZT", adds **+2638**. Its legend says "`+N adds` is the addition count (`nz(U)+nz(V)+nz(W) − 2r − n·p`)". That is the naive count, which is not comparable to a reduced SLP count. It is far above 929 either way. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T23:54:12Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48. Entry `{'format': [5, 8, 8], 'rank': 230, 'exponent': 2.828247}`. Rank 230 is the best known rank, so the claim is eligible. |

## This repository (V3R1T4S)

| Source | URL | UTC fetch | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T23:54:12Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | No mention of additions, fmm-additive-complexity-records or 5x8x8. Its matrix-multiplication rows are rank records for formats 13 and up, over Q. |
| open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T23:54:12Z | 200 | 12473dc228f9f201566453a3e87b1d4ed24a37bf8eca1240f665a443a7148a2e | 16 open PRs, all titles and bodies read. None is for fmm-additive-complexity-records and none mentions 5x8x8. The only matrix-multiplication PR is #197, a (13,15,15) rank claim. |
| FMM known-knowns listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-15T23:54:13Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 merged package folders. |
| family INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-15T23:55:13Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | Rank records only (13x14x14 to 15x16x16). |
| each package's INDEX.csv (21 files) | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/(package)/INDEX.csv | 2026-10-15T23:55:37Z to 23:55:48Z | 200 (all 21) | per-file hashes in `novelty_ws/run_nov929/LOG.txt` | 12 are fmm-additive-complexity-records packages: 4x6x6 r105 373, 5x7x7 r176 699, 6x6x7 r183 695, 6x8x8 r266 993, 4x6x8 r140 476, 6x6x6 r153 588, 5x6x7 r150 582, 4x6x7 r123 469, 6x6x8 r203 719, 5x5x8 r144 556, 5x6x6 r130 502, 5x5x5 r93 358. The other 9 are rank packages. **None covers 5x8x8.** |

Before these I tried the package CLAIM.md files at the same raw paths. All 21 returned 404 because packages have no root CLAIM.md. This was a missing file, not a block.

## Literature (last 24 months)

| Source | URL | UTC fetch | HTTP | sha256 |
|---|---|---|---|---|
| Perminov arXiv:2512.13365 abstract | https://arxiv.org/abs/2512.13365 | 2026-10-15T23:55:58Z | 200 | 0597e5f12c2b0a08b901394f7fdb2252c23553a9ede952988e6122c21115b258 |
| Perminov arXiv:2512.13365 full text (v2) | https://arxiv.org/html/2512.13365 | 2026-10-15T23:56:34Z | 200 | 7fbf6570ffe7c946d1561d56587f53939bfb8be542f21adb1641813f2c17de3e |
| Perminov arXiv:2512.21980 | https://arxiv.org/abs/2512.21980 | 2026-10-15T23:55:57Z | 200 | 6dafdd2827cf2a4de56751afc6727b07f0a2411e5d0ef315e48efecf94d77a0e |
| Martensson-Wagner-Stapleton arXiv:2601.05272 | https://arxiv.org/abs/2601.05272 | 2026-10-15T23:55:59Z | 200 | 1e3a8189674162a82d8e83ce8f876b3febf5199d048e943fb491385c26bf1e08 |
| Sun arXiv:2604.27645 | https://arxiv.org/abs/2604.27645 | 2026-10-15T23:55:58Z | 200 | a6d00c5ad9da207503d58e08ebfa706d58ec8226c2018db8cb4233ad2be5a40c |
| Karunaratne-Idamekorala arXiv:2607.28676 | https://arxiv.org/abs/2607.28676 | 2026-10-15T23:55:58Z | 200 | d64fae5233a719c76c96d3d57c7a00bafa63d38b3e136f5ae1c8a4f9b0117baf |
| Stapleton-Perminov arXiv:2609.32388 | https://arxiv.org/abs/2609.32388 | 2026-10-15T23:55:58Z | 200 | 97948d766566a3d9807b2cfe1bcce3b80dd9b8a60d6b8c5feb71551d7e46ad71 |
| Nielsen arXiv:2609.06588 | https://arxiv.org/abs/2609.06588 | 2026-10-15T23:55:58Z | 200 | bc4f57121e2c05eca5a9303fea5869a12eec437f0fad94e34f5b9f923b576044 |
| Perminov arXiv:2511.20317 full text (v2) | https://arxiv.org/html/2511.20317v2 | 2026-10-15T23:59:07Z | 200 | 4724a50e77f0c8e2e4820c9efda3ac3177e7994223a394403a4e7dc9669fcfb6 |
| Perminov arXiv:2606.02480 | https://arxiv.org/abs/2606.02480 | 2026-10-15T23:59:07Z | 200 | 5d9c3e5e3342c9ac31483958c43e1230a2480105b0a0e4ac5bde309537dac043 |
| Martensson-Wagner ePrint 2026/849 abstract | https://eprint.iacr.org/2026/849 | 2026-10-15T23:55:59Z | 200 | 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b |
| ePrint 2026/849 PDF | https://eprint.iacr.org/2026/849.pdf | 2026-10-15T23:55:59Z | **403** (Cloudflare "Just a moment..." challenge) | 4b8e8cb60e6c15e99fe6683466da39e199bd3c265f3437f8218abdb52ac45107 |
| Martensson-Wagner ePrint 2024/2063 abstract | https://eprint.iacr.org/2024/2063 | 2026-10-15T23:56:36Z | 200 | dafa562b4f1ff2dd5beac64491d2cdb5cffc9877bc93edf087215977a55bb133 |
| ePrint 2024/2063 PDF | https://eprint.iacr.org/2024/2063.pdf | 2026-10-15T23:59:17Z | **403** (challenge) | fafbcde41bb21cac777da84d799378a22a9a5e3b030742dfb40ea44c3c8727c2 |
| Hell's Bells ePrint 2026/1688 abstract | https://eprint.iacr.org/2026/1688 | 2026-10-15T23:59:07Z | 200 | 8269492c23b40e63ae3303a37993bdd76d42ecd633dbbfc1bea2099ad587b8ff |
| ePrint 2026/1688 PDF | https://eprint.iacr.org/2026/1688.pdf | 2026-10-15T23:59:17Z | **403** (challenge) | 5b3f488ce4ff3708bf09a5c924da6f6bb0716f2b30f9c91aac2dcbccc33e6c29 |
| fmm_add_reduction tree (API) | https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1 | 2026-10-15T23:55:59Z | **403** (API rate limit) | 3209519d06deb9f4f950810899ddc6fafba9bcfb3fb8cad8b5e1b30459ace147 |
| fmm_add_reduction README | https://raw.githubusercontent.com/werekorren/fmm_add_reduction/main/README.md | 2026-10-15T23:56:34Z | 200 | 37b319e0a3cb960cb612d56e1b53ac61bdfcdd673a0cd9ebafd9599cc055e842 |
| fmm_add_reduction folder pages (github.com HTML, one request each) | https://github.com/werekorren/fmm_add_reduction plus /tree/main/ algorithms, algorithms/hells_bells, algorithms/moosbauer, algorithms/grey, algorithms/other, algorithms/other/unsorted, .../unsorted/deepmind, .../unsorted/deepmind/factorizations_r, .../unsorted/kauerswood, .../unsorted/kauerswood/kemper, .../unsorted/misc, hells_bells_src_and_data, hells_bells_src_and_data/raw_data_and_images | 2026-10-15T23:56:35Z to 23:58:27Z | 200 (all) | per-page hashes in `novelty_ws/run_nov929/LOG.txt` |

arXiv export API: four queries.
1. "matrix multiplication" AND additions
2. "additive complexity" AND matrix
3. au:Martensson AND matrix
4. "common subexpression elimination" AND "matrix multiplication"

The first requests went to http://export.arxiv.org and each got a 301 redirect with an empty body (23:56:36Z). I sent the same four queries once to the https target, and all returned 200. Times and full sha256 values:
- q1: 23:56:45Z, 20f616a807f40ad8be69862e286338b81d4d7d32b968cd63354137f189137724
- q2: 23:56:49Z, ff5a2a20d7374ae3cbae0cf51b03462773ff1332311798ef83c6ef70cf1960b0
- q3: 23:56:51Z, b59ba8af401bd79776acec59ab52f656bfdfb011e97864b5fe54edd21f406c57 (0 entries)
- q4: 23:56:52Z, bf06c8315520038e76b10a1e872d5cbc948ae426ba59926447b17cd448fab4cf

I also ran two web searches. Among results from the last 24 months, the only new sources relevant to addition counts were arXiv:2606.02480, arXiv:2511.20317 and ePrint 2026/1688. All three are listed above.

### Per-paper findings

- **Perminov, arXiv:2512.13365 (Parallel Heuristic Exploration for Additive Complexity Reduction).** It **gives a count for 5x8x8.** Table 1 ("Schemes with optimal rank achieving new SOTA addition counts") has the row `5 × 8 × 8 230 2747 1019 1010 980 974`. The columns are naive, GV, GP-5, GP-40 and proposed. The count is comparable: the abstract says "reducing additive complexity in fast matrix multiplication algorithms with ternary coefficients {-1,0,1}", which is the same convention and rank. The best count is **974**, which is the repository figure. GP-40 is the Martensson-Wagner greedy-potential tool, and on this scheme it gives 980. **5x8x8 is not in Table 6.** Table 6 lists only 4x7x8, 4x8x8, 5x7x8, 6x6x10, 7x7x7, 7x8x8 and 8x8x8, so no lowered component-wise total exists for 5x8x8. 929 < 974.
- **Perminov, arXiv:2512.21980.** No count for 5x8x8; the paper is 3x3 only: "achieving a rank-23 scheme with only 58 scalar additions."
- **Martensson, Wagner, Stapleton, arXiv:2601.05272.** No count for 5x8x8; it is 3x3 only: "finding an algorithm requiring only 59 additions, still without a basis change."
- **Sun, arXiv:2604.27645.** No count for 5x8x8; it is 3x3 only: "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions."
- **Karunaratne-Idamekorala, arXiv:2607.28676.** No count for 5x8x8; it is 3x3 only: "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices."
- **Stapleton-Perminov, arXiv:2609.32388.** No count for 5x8x8. It is 3x3 only and also not comparable because of the basis change: "using 51 additions and subtractions in alternative bases. The input and output conversions require five further additions."
- **Nielsen, arXiv:2609.06588.** No count for 5x8x8. It is 3x3 only and not comparable: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change."
- **Perminov, arXiv:2511.20317 (Ternary Meta Flip Graphs).** It **gives a 5x8x8 count, but not a comparable one.** Table 4 ("Reduce naive addition complexity") has the row `( 5 , 8 , 8 ) 230 2842 2741`. The abstract says the method works by "minimizing naive additive complexity", and naive is a different convention.
- **Perminov, arXiv:2606.02480 (Meta Flip Graph meets Serendipitous Product).** No addition count. It is a rank paper: "Compared to the previous state of the art, ranks are improved for 207 formats."
- **Martensson and Wagner, ePrint 2026/849.** The PDF was blocked (403 challenge). The abstract says the authors "optimize the number of additions for schemes with dimensions up to (n, m, k) = (5, 7, 10)" and that they work "without any change of basis", so their counts would be comparable. **Is 5x8x8 inside that range?**
  - Read entry by entry, no: the middle dimension 8 is above 7.
  - The authors' public input sets also point to no. Their repository, fetched once per folder, holds scheme inputs for these formats and no others: Moosbauer flip-graph schemes up to 666, Kauers-Wood and Kemper schemes 456 to 667, Grey schemes, Hell's Bells schemes 222 to 532, misc 555/666, and the AlphaTensor `factorizations_r` files. The AlphaTensor folder lists `5,7,10.npy` directly before `5,7,11.npy`, `5,7,9.npy`, `5,8,10.npy`, `5,8,11.npy` and `5,8,9.npy`. That fits "up to (5,7,10)" as a stopping point in that list.
  - There is **no 5,8,8 input file anywhere** in the repository. AlphaTensor has no 5x8x8 file at all.
  - Perminov's Table 1 shows the authors' GP-40 tool scoring 980 on this exact rank-230 scheme.
  - Conclusion: the paper very probably has no 5x8x8 count, and nothing suggests a comparable count of 929 or below.
- **Martensson and Wagner, ePrint 2024/2063 (Number of the Beast).** The PDF was blocked (403). The title limits it to "Dimensions up to 666", so 5x8x8 (8 > 6) is outside its range.
- **Martensson, Wagner, Stapleton, ePrint 2026/1688 (Hell's Bells).** The PDF was blocked (403). The abstract claims "record-low arithmetic (additive) complexity for various combinations of dimensions", and its focus is "(n,m,k) = (2,2,k)". The released data folder has addition data only for 222 to 228, 233, 234, 333, 432 and 532. Nothing for 5x8x8.
- **Hells and others, fmm_add_reduction (repository).** It has no 5x8x8 input scheme and no 5x8x8 result file in any folder listed above. Its tool's figure for this scheme is the GP-40 value 980 that Perminov reports, and 980 > 929.

unresolved: these sources could not be read:
- the PDFs of ePrint 2026/849, 2026/1688 and 2024/2063 (each a 403 Cloudflare challenge)
- the GitHub API recursive trees of werekorren/fmm_add_reduction and of elder-plinius/V3R1T4S (each a 403 rate limit)

None of them is plausibly a source of a comparable lower count for 5x8x8 at rank 230:
- 2024/2063 stops at 666.
- 2026/849 states a range of "up to (5,7,10)". Its public input sets contain no 5x8x8 scheme, and its tool gives 980 on this scheme according to arXiv:2512.13365 Table 1.
- 2026/1688's released data stops at 532.
- The two trees were replaced by one-request-per-folder HTML listings and per-package INDEX.csv files, which together show no 5x8x8 entry.

## Verdict

- **Full criterion: PASS (novelty).**
  - (a) The minimum cr for 5x8x8 at rank 230 across Perminov's live addition_reduced_ZT files is 974. reduced_known.json, the README and the CHANGELOG have no lower figure. 929 < 974.
  - (b) The Lille 5x8x8 page has no Commentaries section, no cited complexity variant and no count.
  - (c) The matmulcatalog adds value for 5x8x8 is 2638. It is a naive count, not comparable, and above 929 anyway.
  - No literature source in the last 24 months gives a comparable count at or below 929. The best comparable published count is Perminov's 974.
  - No merged V3R1T4S package and no open pull request covers this format.
  - Rank 230 is the best known rank in fmm_sota.json, so the claim is eligible.
  - This is a strict improvement of 45, not a tie.
- **Partial win p1 (strictly fewer than Perminov's live count, same convention): PASS.** 929 < 974. This is a novelty verdict only. Correctness and the count recount are for the other skeptics.

pass: true
