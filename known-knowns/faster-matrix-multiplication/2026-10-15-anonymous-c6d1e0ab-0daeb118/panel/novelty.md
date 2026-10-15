# Novelty check: 4x6x6 rank 105, 373 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Claim checked: a ternary straight-line program for the 4x6x6 rank-105 scheme using 373 additions under Perminov's reduced convention, against 430 in Perminov's repository. Target: fmm-additive-complexity-records. The claim folder matched its hash list (all 8 files OK).

Fetch rules followed: one plain curl request per URL, User-Agent `V3R1T4S-research (honest client; curl)`, no retries. Pages saved in the panel's novelty_ws folder. Times are UTC from `date -u`.

## Primary table and status sources

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov repo tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T12:13:24Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | Tree not truncated. 195 files in addition_reduced_ZT. Exactly one 4x6x6 file: `4x6x6_m105_cr430_fv243_cn894_ZT_reduced.json`, so cr = 430, minimum 430. No 6x4x6 or 6x6x4 file. No 4x6x6 file in naive_addition_reduced_ZT. No 466 file in schemes/known/fmm_add_reduction. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T12:13:27Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | No `4x6x6-105` key. The only 4x6x6 key is `"4x6x6-116": {"Z2": 581}`. That is a different rank (116) and a different ring (Z2), so it does not compare. |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T12:13:27Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | Only the rank-table row `4x6x6 / 105 / 105 / 105 / 2.809337134`. No addition count for 4x6x6. |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T12:13:27Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No 4x6x6 entry under any "Reduced additions improvement" heading, and no 4x6x6 mention at all. |
| Lille per-format page | https://fmm.univ-lille.fr/4x6x6.html | 2026-10-15T12:13:28Z | 200 | 32bd27b99d224bba878517615f3d04b31d8102d0f9a616c47b111c88b5af6e44 | Rank 105: "The algorithm 4x6x6:105 is the (Kronecker) tensor product of 2x2x2:7 with 2x3x3:15". No Commentaries section, no complexity variant cited, and no addition or operation count stated. |
| Lille evaluation scheme (linked from the page) | https://fmm.univ-lille.fr/4x6x6_raw.mpl.bz2 | 2026-10-15T12:14:40Z | 200 | 648f3c31b4941078b3180451a63494182de573416c0db5f6309fe7e77a219791 | A Maple straight-line program for this rank-105 Kronecker scheme: 105 recursive products, coefficients plus or minus 1 only (no scalar multiplications). My count, one binary +/- per operation with leading negation free: 435 additions. The page does not state this number; I counted it. 435 is above 373. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T12:13:28Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row 4x6x6: "✓ 105 Dronperminov-ZT ... adds +965". This is a naive count, nz(U)+nz(V)+nz(W) - 2r - n·p, and is not comparable with a reduced straight-line count. It is above 373 in any case. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T12:13:28Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | `{"format": [4, 6, 6], "rank": 105, "exponent": 2.809337}` is the only 4x6x6 entry (createdAt 2026-10-09T11:45:48). Rank 105 is the best known rank, so the scheme is eligible. |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T12:13:29Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | No fmm-additive-complexity-records entry and no 4x6x6 entry. The only matrix-multiplication rows are rank records over Q. |
| V3R1T4S open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T12:13:29Z | 200 | 13f1b324a8cfa79c158feb8e70b0443f85468b9e5876637c06056247704260c2 | 44 open PRs. Four are for this target: #149 and #161 (4x6x7 rank 123: 503 and 469), and #159 and #162 (5x6x7 rank 150: 652 and 582). No title or body mentions 4x6x6, 6x4x6 or 6x6x4. |

All of my primary hashes are the same as the hashes in the author's table record, so the pages had not changed since the author fetched them.

## Literature (last 24 months)

arXiv export API: four queries in total. The first two used http and returned HTTP 301 with an empty body, at 2026-10-15T12:15:56Z (they count toward the four; I did not retry them). The two https queries returned 200:
- q3, 2026-10-15T12:16:21Z, sha256 a8d694b7c519b0df359bdb4a09ef8bab74f885e7db820acfb689c1a4f31cdfdf: abs "matrix multiplication" AND (abs additions OR abs "additive complexity"), newest 100.
- q4, 2026-10-15T12:16:28Z, sha256 b9c331a3cd30b097a71b6b07ce741ae4a77535734834d8e9c25750df4752f74e: au Martensson OR au Stankovski OR (abs "matrix multiplication" AND abs "straight-line").

Neither query found any paper that gives an addition count for 4x6x6 beyond those listed below. The relevant hits were 2508.03857, 2601.05272, 2604.27645, 2607.28676, 2609.06588, 2609.32388, 2512.21980, 2512.13365 and 2511.20317. I found no arXiv copy of the Mårtensson–Wagner paper.

- **Perminov, arXiv:2512.13365** (https://arxiv.org/abs/2512.13365 at 2026-10-15T12:15:08Z, 200, sha256 0597e5f12c2b0a08b901394f7fdb2252c23553a9ede952988e6122c21115b258; PDF https://arxiv.org/pdf/2512.13365 at 2026-10-15T12:15:56Z, 200, sha256 82aff81bf22f80c13cf559f1c42ada3fecda51fb4efc773c3e7ee1ae5b135c27).
  - Gives a 4x6x6 count. Table 1 ("Schemes with optimal rank achieving new SOTA addition counts") has the row "4×6×6 105 894 467 435 435 430": naive 894, Greedy-Vanilla 467, Greedy-Potential GP-5 435, GP-40 435, proposed method 430. GP is the fmm_add_reduction method.
  - Comparable: same convention and same rank. The quoted sentence is "This paper presents a parallel random-search method for reducing additive complexity in fast matrix multiplication algorithms with ternary coefficients {−1, 0, 1}".
  - Table 6 ("Component-wise addition counts for schemes improvable by approaches result combination") lists 4x7x8, 4x8x8, 5x7x8, 6x6x10, 7x7x7, 7x8x8 and 8x8x8. 4x6x6 is not among them.
  - Best comparable value: 430, which is above 373.
- **Perminov, arXiv:2512.21980** (https://arxiv.org/abs/2512.21980 at 2026-10-15T12:15:08Z, 200, sha256 6dafdd2827cf2a4de56751afc6727b07f0a2411e5d0ef315e48efecf94d77a0e). 3x3 only, so no 4x6x6 count: "achieving a rank-23 scheme with only 58 scalar additions. This improves the previous best additive complexity of 60 additions without a change of basis."
- **Mårtensson and Wagner, IACR ePrint 2026/849** (abstract https://eprint.iacr.org/2026/849 at 2026-10-15T12:15:09Z, 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b).
  - The PDF https://eprint.iacr.org/2026/849.pdf returned 403 with a "Just a moment..." challenge page at 2026-10-15T12:15:10Z (sha256 of the challenge body 7d47d9aabf5508c720f532fe7c64954326a3f6f74a0c97632d83eaf9b6fa541b). I did not retry.
  - Coverage sentence: "We implement of our methods and use them to optimize the number of additions for schemes with dimensions up to (n, m, k) = (5, 7, 10)." So 4x6x6 IS inside the range of formats the paper covers (4 ≤ 5, 6 ≤ 7, 6 ≤ 10).
  - Comparability sentence: "optimizing the number of additions in Strassen-type matrix multiplication schemes for larger matrix sizes, and without any change of basis". So any 4x6x6 count it gives at rank 105 with ternary coefficients would be comparable.
  - Whether it gives a 4x6x6 count at rank 105 could not be read.
  - Indirect evidence that it does not have one below 373:
    - The authors' repository has no 4x6x6 data (see the next item).
    - Perminov's Table 1 records the authors' GP method at 435 on this rank-105 scheme.
    - Perminov's reduced_known.json, which collects external reduced counts, lists 4x6x6 only at rank 116 over Z2 (581).
    - Neither the Lille page nor COVERAGE.md cites any such count.
- **Mårtensson and Wagner, ePrint 2024/2063 (ACDA25 "Number of the Beast", the earlier version)** (abstract https://eprint.iacr.org/2024/2063 at 2026-10-15T12:15:56Z, 200, sha256 dafa562b4f1ff2dd5beac64491d2cdb5cffc9877bc93edf087215977a55bb133).
  - The PDF https://eprint.iacr.org/2024/2063.pdf returned 403 with a challenge page at 2026-10-15T12:17:04Z (sha256 03134d9f5389c5d1bb9c7fe1175f48cf0c0cfd157fa8034b55c469bb17af119e). I did not retry.
  - Its abstract names a reference set "due to Moosbauer and Kauers" and dimensions "including (and surpassing) the 666 limit". It states no 4x6x6 count.
- **werekorren/fmm_add_reduction (the Hells Bells data and the repository of the fmm_add_reduction method)**
  - Recursive tree https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1 at 2026-10-15T12:15:10Z, 200, sha256 dfdf1cd6a43106f75700703a917a5bb0ecdb971b27858e2bceafeb5718df1573. It is truncated.
  - To see the full directory list I made one non-recursive request, https://api.github.com/repos/werekorren/fmm_add_reduction/contents/algorithms/hells_bells, at 2026-10-15T12:15:55Z, 200, sha256 f3e52cb096f5292ed759cf99810bf9e4b09a287716b36e4ef531f9653d8e8754. The format folders are 222, 223, 224, 225, 226, 227, 228, 233, 234, 333, 432 and 532. The algorithms/grey folder holds formats up to 5x2x2 and 4x4x2.
  - README https://raw.githubusercontent.com/werekorren/fmm_add_reduction/main/README.md at 2026-10-15T12:15:55Z, 200, sha256 37b319e0a3cb960cb612d56e1b53ac61bdfcdd673a0cd9ebafd9599cc055e842.
  - No 4x6x6 file.
- **Sun, arXiv:2604.27645** (https://arxiv.org/abs/2604.27645 at 2026-10-15T12:15:08Z, 200, sha256 a6d00c5ad9da207503d58e08ebfa706d58ec8226c2018db8cb4233ad2be5a40c). 3x3 only, so no 4x6x6 count: "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions".
- **Karunaratne and Idamekorala, arXiv:2607.28676** (https://arxiv.org/abs/2607.28676 at 2026-10-15T12:15:09Z, 200, sha256 d64fae5233a719c76c96d3d57c7a00bafa63d38b3e136f5ae1c8a4f9b0117baf). 3x3 only, so no 4x6x6 count: "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices."
- **Stapleton and Perminov, arXiv:2609.32388** (https://arxiv.org/abs/2609.32388 at 2026-10-15T12:15:09Z, 200, sha256 97948d766566a3d9807b2cfe1bcce3b80dd9b8a60d6b8c5feb71551d7e46ad71). 3x3 only, and its count uses a change of basis, so it would not compare anyway: "using 51 additions and subtractions in alternative bases. The input and output conversions require five further additions".
- **Nielsen, arXiv:2609.06588** (https://arxiv.org/abs/2609.06588 at 2026-10-15T12:15:09Z, 200, sha256 bc4f57121e2c05eca5a9303fea5869a12eec437f0fad94e34f5b9f923b576044). 3x3 only, and its count uses a change of basis, so it does not compare: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change".
- **Perminov, arXiv:2511.20317 (ternary meta flip graphs)** (https://arxiv.org/abs/2511.20317 at 2026-10-15T12:17:13Z, 200, sha256 391adbbda9830d06ee69f7b93de644ea7fd75dcbc58fa3753b9f8e15a9cc8507). Concerns ranks and "naive additive complexity". It gives no reduced count, so nothing in it compares.

## Comparison

Comparable counts I could read for 4x6x6 at rank 105 (ternary coefficients, no basis change, same convention):
- 430: Perminov's live cr430 file, and Table 1 of arXiv:2512.13365.
- 435: GP-40 in arXiv:2512.13365 Table 1.
- 435: my count of the Lille Maple evaluation scheme.

The minimum is 430, and 373 is 57 below it. There is no tie. Not comparable: the COVERAGE naive count (+965), and reduced_known's 4x6x6-116 Z2 entry (581).

I checked only whether 373 is new. I did not recheck the program's correctness or the count of 373; that is the other skeptics' job.

unresolved: ePrint 2026/849 PDF and ePrint 2024/2063 PDF (both 403 challenge pages). 2026/849 covers formats up to 5x7x10, so 4x6x6 is inside its range, and it could plausibly hold a comparable 4x6x6 count. Nothing I could read shows it covers 4x6x6 at rank 105, and nothing indicates a count below 373. The authors' repository has no 4x6x6 data, and Perminov's catalogue of external counts lists 4x6x6 only at rank 116 over Z2.

## Verdicts

- Full criterion, parts (a), (b) and (c):
  - (a) 373 < 430, the minimum over Perminov's live files, reduced_known.json, README and CHANGELOG.
  - (b) The Lille page cites no complexity variant, and its published evaluation scheme uses 435.
  - (c) The COVERAGE adds value (+965) is a naive count and not comparable, and it is higher anyway.
  - No open pull request or trophy-case entry has a 4x6x6 count.
  - Verdict: PASS. No unread source is known to cover this format at this rank. The one unread source that covers this range of formats is flagged above.
- Partial win p1, read as the brief defines it (strictly fewer than Perminov's live count, same convention): PASS, 373 < 430. The bank's own p1 is a 3x3x3 item, which this claim does not address.

pass: true
