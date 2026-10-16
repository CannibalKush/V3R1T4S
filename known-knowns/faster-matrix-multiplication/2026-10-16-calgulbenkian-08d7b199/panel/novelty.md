# Novelty skeptic report: add-4x5x5-cr281 (rerun)

context: Claude Code subagent (Opus 5.5), fresh context

Claim under test: a ternary straight-line program for the 4x5x5 rank-76 scheme with 281 additions under Perminov's reduced convention, against 299 in Perminov's repository (target fmm-additive-complexity-records).

Claim folder hashes: all eight entries of claim.SHA256SUMS check OK (shasum -a 256 -c).

All fetches below were one plain curl GET each, User-Agent 'V3R1T4S-research (honest client; curl)', no retries. Times are UTC from `date -u` taken just before each request. Pages are saved in the panel's novelty_ws folder.

## Primary tables

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov repository tree (primary listing) | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-16T00:18:24Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | Tree not truncated (6637 entries; 321 under addition_reduced_ZT). The only addition_reduced_ZT file for 4x5x5 (no 5x4x5 or 5x5x4 file either) is `4x5x5_m76_cr299_fv112_cn530_ZT_reduced.json`, so the minimum reduced count cr is **299**. The other 4x5x5 rank-76 files are `naive_addition_reduced_ZT/4x5x5_m76_c528_ZT` and `4x5x5_m76_c532_ZT` (naive counts in a different convention, not comparable), plus `known/alpha_tensor/4x5x5_m76_ZT.json` and two `serendipitous_base` scheme files, which carry no addition count. The API was not refused, so the HTML fallback page was not needed. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-16T00:18:38Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | `"4x5x5-76": {"Z": 451, "Z2": 372}`. The Z value 451 is above 299 and 281. The Z2 value 372 is over a different ring, so it is not comparable. |
| Perminov README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-16T00:18:39Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | The 4x5x5 row is a rank table only (`4x5x5 / 76 / 76 / 76 / 2.821220388`). The README states no addition count for 4x5x5. |
| Perminov CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-16T00:18:39Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No "Reduced additions improvement" entry names 4x5x5, and 4x5x5 does not appear anywhere in the file. |
| Lille per-format page | https://fmm.univ-lille.fr/4x5x5.html | 2026-10-16T00:18:40Z | 200 | 792d090a2d741d3903959e7714f77f28933feab47182246e136dbe251ce0a435 | The page gives the format and rank as `⟨4×5×5:76⟩`. It has **no Commentaries section** and cites no complexity variant. Its only citation is Fawzi et al., "Discovering faster matrix multiplication algorithms with reinforcement learning", Nature 610 (2022). The page states no addition or operation count. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-16T00:18:40Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | The 4x5x5 row reads `⟨4,5,5⟩`, "✓ 76 Alphatensor-F2", "✓ 76 Alphatensor-Z", adds `+549`. The legend says "`+N adds` is the addition count (`nz(U)+nz(V)+nz(W) − 2r − n·p`)". That is a naive count, so it is not comparable with a reduced straight-line-program count. It is 549 in any case, above 281. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-16T00:18:41Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | `{"format": [4, 5, 5], "rank": 76, "exponent": 2.82122}` (createdAt 2026-10-09T11:45:48). Rank 76 is the best known rank for this format, so the claim meets the eligibility rule. |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-16T00:18:41Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | No row mentions 4x5x5 or an addition-count record. Its matrix-multiplication rows are rational rank results for formats from 13 to 16. |
| V3R1T4S open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-16T00:18:41Z | 200 | 28704d72eaed4c74b1b685f8b89a1c7e53bda8f9b69dec5d35584937a63c65c1 | 16 open pull requests, every title and body read. None mentions 4x5x5, ⟨4,5,5⟩, 455-76, fmm-additive-complexity-records, additive complexity or reduced additions. The only open matrix-multiplication pull request is #197, a rank claim for (13,15,15). |
| V3R1T4S known-knowns FMM listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-16T00:18:42Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 dated package folders, plus the family files. |
| V3R1T4S repository tree (to name the merged packages' objects) | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-10-16T00:19:51Z | 200 | f63c3cc8f48202557b7290f117f14aefdebe4f42ed79cf2448cb318d24b229db | Tree not truncated. The merged addition-count packages cover 4x6x6 cr373, 5x7x7 cr699, 6x6x7 cr695, 6x8x8 cr993, 4x6x8 cr476, 6x6x6 cr588, 5x6x7 cr582, 4x6x7 cr469, 6x6x8 cr719, 5x5x8 cr556 and 5x6x6 cr502 (the eleven anonymous packages), plus 5x5x5 cr358 (drzuzzjen). **None covers 4x5x5.** No path in the whole repository contains 4x5x5, 5x4x5 or 5x5x4. |
| family INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-16T00:19:39Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | Rational rank rows only, for 13x14x14 to 15x16x16. No 4x5x5 row. |
| family README.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/README.md | 2026-10-16T00:19:39Z | 200 | 740321f0f9287e13ee0f1dd229c47a974b49393560a453df125ad850b359ba07 | No mention of 4x5x5 or of any addition count. |

## Literature (last 24 months, back to 2024-10-15)

| Source | URL | UTC fetch time | HTTP | sha256 |
|---|---|---|---|---|
| ePrint 2026/849, abstract page | https://eprint.iacr.org/2026/849 | 2026-10-16T00:20:34Z | 200 | 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b |
| ePrint 2026/849, PDF | https://eprint.iacr.org/2026/849.pdf | 2026-10-16T00:20:35Z | 403 (challenge page) | 88e1e34af54c4e2923ffae261c516722256b7bf519a49294b842cd1d68de221c |
| ePrint 2026/849, the operator's hand-downloaded text extraction (local, read under rerun note 2) | not applicable | read 2026-10-16 | not applicable | 99b19def9c130bd95e7dd894fdb4d172b5f87bf5a0344620b2d9c02d9307de60 (text file) |
| werekorren/fmm_add_reduction tree, recursive | https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1 | 2026-10-16T00:20:35Z | 200 (truncated: true) | dfdf1cd6a43106f75700703a917a5bb0ecdb971b27858e2bceafeb5718df1573 |
| werekorren algorithms/hells_bells tree, non-recursive (needed because the recursive tree was truncated) | https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/74fd1431aae47cea715c0ef699c282bc2c651849 | 2026-10-16T00:21:34Z | 200 | 9f8e64021463ac5ae0982b037485de1389176842dbc7af162ab07508ea0dab1f |
| werekorren README.md | https://raw.githubusercontent.com/werekorren/fmm_add_reduction/main/README.md | 2026-10-16T00:21:35Z | 200 | 37b319e0a3cb960cb612d56e1b53ac61bdfcdd673a0cd9ebafd9599cc055e842 |
| arXiv:2512.21980, abstract | https://arxiv.org/abs/2512.21980 | 2026-10-16T00:20:44Z | 200 | 6dafdd2827cf2a4de56751afc6727b07f0a2411e5d0ef315e48efecf94d77a0e |
| arXiv:2512.13365, abstract | https://arxiv.org/abs/2512.13365 | 2026-10-16T00:20:44Z | 200 | 0597e5f12c2b0a08b901394f7fdb2252c23553a9ede952988e6122c21115b258 |
| arXiv:2512.13365, full HTML | https://arxiv.org/html/2512.13365 | 2026-10-16T00:21:00Z | 200 | 7fbf6570ffe7c946d1561d56587f53939bfb8be542f21adb1641813f2c17de3e |
| arXiv:2604.27645, abstract | https://arxiv.org/abs/2604.27645 | 2026-10-16T00:20:44Z | 200 | a6d00c5ad9da207503d58e08ebfa706d58ec8226c2018db8cb4233ad2be5a40c |
| arXiv:2607.28676, abstract | https://arxiv.org/abs/2607.28676 | 2026-10-16T00:20:44Z | 200 | d64fae5233a719c76c96d3d57c7a00bafa63d38b3e136f5ae1c8a4f9b0117baf |
| arXiv:2609.32388, abstract | https://arxiv.org/abs/2609.32388 | 2026-10-16T00:20:45Z | 200 | 97948d766566a3d9807b2cfe1bcce3b80dd9b8a60d6b8c5feb71551d7e46ad71 |
| arXiv:2609.06588, abstract | https://arxiv.org/abs/2609.06588 | 2026-10-16T00:20:45Z | 200 | bc4f57121e2c05eca5a9303fea5869a12eec437f0fad94e34f5b9f923b576044 |
| ePrint 2024/2063 (ACDA25 "Number of the Beast"), abstract | https://eprint.iacr.org/2024/2063 | 2026-10-16T00:22:45Z | 200 | dafa562b4f1ff2dd5beac64491d2cdb5cffc9877bc93edf087215977a55bb133 |
| ePrint 2024/2063, PDF | https://eprint.iacr.org/2024/2063.pdf | 2026-10-16T00:22:55Z | 403 (challenge page) | 6edaae5ff0eb0a9be866dc468be672c912f6fd368154c0dc1f4d9ffb8f0b1ea1 |
| ePrint 2026/1688 (Hell's Bells), abstract | https://eprint.iacr.org/2026/1688 | 2026-10-16T00:22:45Z | 200 | 8269492c23b40e63ae3303a37993bdd76d42ecd633dbbfc1bea2099ad587b8ff |
| ePrint 2026/1688, PDF | https://eprint.iacr.org/2026/1688.pdf | 2026-10-16T00:22:54Z | 403 (challenge page) | bbe85dad99ff6796940eec890548f2303ae2c74aaf6050e0216dff1b3714c358 |
| arXiv:2602.11041, abstract | https://arxiv.org/abs/2602.11041 | 2026-10-16T00:22:46Z | 200 | 97204d8b8e57fd765e8e464ff834163ddbafd4f72974eb66ee2a899789af9ac8 |
| Nature AlphaTensor article (the work the Lille page cites) | https://www.nature.com/articles/s41586-022-05172-4 | 2026-10-16T00:23:15Z | 303 (redirect, not followed) | dc9b4d151c92806167d1b4f230201c05e72a44690ce4c52e25ee7af9c1c31dac |
| arXiv API query 1 (abstract has "matrix multiplication" and "additions") | http://export.arxiv.org/api/query?search_query=abs:%22matrix%20multiplication%22%20AND%20abs:%22additions%22&sortBy=submittedDate&sortOrder=descending&max_results=100 | 2026-10-16T00:21:46Z | 301 (empty body; redirect to https, not followed) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| arXiv API query 2 ("additive complexity" and "matrix multiplication") | http://export.arxiv.org/api/query?search_query=abs:%22additive%20complexity%22%20AND%20abs:%22matrix%20multiplication%22&sortBy=submittedDate&sortOrder=descending&max_results=100 | 2026-10-16T00:21:50Z | 301 (empty body) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| arXiv API query 3 ("matrix multiplication" with additions, additive complexity, straight-line or subexpression) | https://export.arxiv.org/api/query?search_query=abs:%22matrix%20multiplication%22%20AND%20(abs:additions%20OR%20abs:%22additive%20complexity%22%20OR%20abs:%22straight-line%22%20OR%20abs:%22subexpression%22)&sortBy=submittedDate&sortOrder=descending&max_results=200 | 2026-10-16T00:21:59Z | 200 (200 entries) | 4a46a76a90d7603497cafa2596a192e5f4a3eaeb5f8be64abf1eb1a074e05817 |
| arXiv API query 4 (Martensson, "number of the beast", arithmetic complexity, flip graph) | https://export.arxiv.org/api/query?search_query=au:Martensson%20OR%20ti:%22number%20of%20the%20beast%22%20OR%20abs:%22arithmetic%20complexity%22%20AND%20abs:%22matrix%20multiplication%22%20OR%20abs:%22flip%20graph%22&sortBy=submittedDate&sortOrder=descending&max_results=100 | 2026-10-16T00:22:22Z | 200 (86 entries) | f7cfc45139b87fab427c553ebb6cf12770d6bf2f71127d3bc34c6ec9b9292ae3 |

Two web searches were also run, one for 4x5x5 rank-76 addition counts and one for the Mårtensson-Wagner "Number of the Beast" paper. Neither turned up any count for 4x5x5 below those listed here.

### Per paper

- **Perminov, arXiv:2512.13365** ("Parallel Heuristic Exploration for Additive Complexity Reduction in Fast Matrix Multiplication")
  - Gives a count for 4x5x5, and the count is comparable. Coverage: "reducing additive complexity in fast matrix multiplication algorithms with ternary coefficients $\{-1,0,1\}$".
  - Its Table 3 ("Equal addition counts (proposed method matches GP-40) for schemes with best-known rank") has the row `4 × 5 × 5, 76, 451 [1], 530, 315, 300, 299, 299`: best known 451 (ref [1] = Mårtensson and Wagner, ACDA 2025), naive 530, GV 315, GP-5 300, GP-40 299, proposed 299.
  - Its best is **299**, the same as the live repository file. 281 is below it.
  - Table 6 ("Component-wise addition counts for schemes improvable by approaches result combination") lists only 4x7x8, 4x8x8, 5x7x8, 6x6x10, 7x7x7, 7x8x8 and 8x8x8. **4x5x5 is not among them**, so no lowered combined count exists for this format.
- **Perminov, arXiv:2512.21980**
  - Covers only 3x3: "achieving a rank-23 scheme with only 58 scalar additions".
  - No count for 4x5x5.
- **Mårtensson and Stankovski Wagner, IACR ePrint 2026/849**
  - Read through the operator's text extraction. The format is **inside** the paper's range: "optimize the number of additions for schemes with dimensions up to $(n, m, k) = (5, 7, 10)$". The paper gives four 455-76 rows.
  - Table 3.3, ternary AlphaTensor scheme: `455-76  549  322  310  0.26, 0.01, 0.11  437`.
    - This is comparable. The caption says "All schemes have ternary coefficients. Recall that [14] assumes the KS framework while we do not", and the column header reads "without change of basis".
    - The comparable count is **310**, above 299 and 281.
    - The 437 column is the Karstadt-Schwartz (KS) framework count "with" change of basis, so it is not comparable. It is also higher.
  - Table 3.4, "Algorithms over Z", Moosbauer Z: `455-76  1,107  469  451`.
    - The count is **451**. The paper notes "Most of these algorithms feature non-ternary coefficients. For such schemes, in this work we only attempt to minimize the number of additions and not the number of scalar multiplications by non-ternary coefficients".
    - So it may be in a different coefficient class. It is above 281 either way.
  - Tables 3.5 and 3.6 are over Z2 (372, 310, 310), so they are not comparable. The caption reads "Results from applying Greedy Potential to a set of algorithms found by Deepmind [12, 30], all over Z2".
  - A Z2 row `455-73` (rank 73) is a different rank over a different ring, so it is not comparable.
  - The paper's best comparable count for 4x5x5 at rank 76 is 310. Nothing in it is below 281.
- **Mårtensson and Stankovski Wagner, ePrint 2024/2063 (ACDA 2025, "Number of the Beast")**
  - Only the abstract was read; the PDF returned 403. The abstract describes a method "without including any change of basis" for dimensions up to (6, 6, 6), so it covers this format.
  - Perminov's 2512.13365 cites its 4x5x5 rank-76 value as "best known 451 [1]".
  - The 2026 ePrint 2026/849 is its extension, and its 4x5x5 rows (310 and 451) were read in full.
- **werekorren/fmm_add_reduction (the authors' repository, including the Hell's Bells data)**
  - The recursive tree came back truncated. The full non-recursive listing of `algorithms/hells_bells` shows only the folders 222, 223, 224, 225, 226, 227, 228, 233, 234, 333, 432 and 532.
  - No file path in the returned tree matches 455, 4x5x5 or a permutation. The repository holds no 4x5x5 scheme.
- **Hells and others, ePrint 2026/1688 ("Hell's Bells: A Neural Network Pipeline for Ternary Fast Matrix Multiplication Algorithms")**
  - Only the abstract was read; the PDF returned 403. The abstract says: "We achieve record-low arithmetic (additive) complexity for various combinations of dimensions. For $(n,m,k) = (2,2,k)$, our method performs particularly well."
  - Its public scheme folders, listed above, do not include 455. No 4x5x5 count was seen.
- **Sun, arXiv:2604.27645**
  - Covers only 3x3: "a rank-$23$ algorithm for general $3\times3$ matrix multiplication that uses $56$ additions/subtractions".
  - No count for 4x5x5.
- **Karunaratne and Idamekorala, arXiv:2607.28676**
  - Covers only 3x3: "We give a 55-addition realization of rank-23 multiplication of two arbitrary $3\times3$ matrices".
  - No count for 4x5x5.
- **Stapleton and Perminov, arXiv:2609.32388**
  - Covers only 3x3, and with a basis change: "using 51 additions and subtractions in alternative bases. The input and output conversions require five further additions".
  - No count for 4x5x5. Its counts would not be comparable anyway.
- **Nielsen, arXiv:2609.06588**
  - Covers only 3x3, and with a basis change: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change".
  - No count for 4x5x5, and not comparable.
- **Other papers seen in the arXiv queries**
  - 2508.03857 (Stapleton), 2601.05272 and 2506.13242 (Dumas, Pernet, Sedoglavic): 3x3 or 4x4 only.
  - 2511.20317 (Perminov, ternary meta flip graphs): "minimizing naive additive complexity", a naive count with no reduced 4x5x5 value.
  - 2410.20538 and 2508.01748: asymptotic leading-constant or exponent results.
  - 2602.11041: exponents.
  - None gives a reduced count for 4x5x5.

## Comparison

The smallest comparable count for 4x5x5 at rank 76 is **299**. It is the same in Perminov's live addition_reduced_ZT file cr299 and in arXiv:2512.13365 Table 3. The other counts read are:

- 310 in ePrint 2026/849 Table 3.3 (comparable);
- 451 in reduced_known.json Z and ePrint 2026/849 Table 3.4;
- 549 naive in COVERAGE.md (not comparable);
- nothing on the Lille page;
- nothing in the V3R1T4S trophy case, open pull requests or merged packages.

281 is strictly below every one of them, by 18 against the 299 reference.

unresolved: The PDFs of ePrint 2024/2063 (ACDA25) and ePrint 2026/1688 (Hell's Bells) returned 403, and the Nature AlphaTensor article returned 303 (not followed). None of the three can plausibly hold a comparable count for 4x5x5 at rank 76 below 281:
- ePrint 2024/2063 is superseded by its extension 2026/849, whose 4x5x5 rows were read in full (best comparable 310). Perminov cites its 4x5x5 value as 451.
- The Hell's Bells public scheme folders contain no 455 format.
- The Nature paper (2022, outside the 24-month window) is a rank result, and the Lille page quotes no count from it.

## Verdicts

- **Full criterion: PASS, provided the claim's count and verification are confirmed by the other skeptics.** Rank 76 equals the best known rank in fmm_sota.json. The claimed 281 is strictly below:
  - (a) the minimum cr 299 over Perminov's live addition_reduced_ZT files for 4x5x5 at rank 76, and his reduced_known.json (Z 451), README and CHANGELOG (no lower count);
  - (b) the Lille page, which publishes no count and cites no complexity variant;
  - (c) matmulcatalog COVERAGE.md (+549, naive and not comparable);
  - and every comparable literature count read (best 299 in arXiv:2512.13365, 310 in ePrint 2026/849).
  - No open or merged V3R1T4S package or pull request holds a 4x5x5 count.
- **Partial win p1 as defined in this panel's brief (strictly fewer than Perminov's live count, same convention): PASS.** 281 < 299.
  - Note: the bank's own enumerated p1 is defined for a rank-23 <3,3,3> program. This claim does not address that one, so p1 holds only in the brief's sense.

pass: true
