# Novelty check: 2x5x5 rank 40, 147 reduced additions (target fmm-additive-complexity-records)

context: Claude Code subagent (Opus 5.5), fresh context

Role: novelty skeptic (rerun). Local reads were limited to the claim folder (CLAIM.md, table-record/README.md, INDEX.csv, the object file name), claim.SHA256SUMS, and the operator's text extraction of IACR ePrint 2026/849 (rerun note 2). Each remote page got one plain curl request with User-Agent 'V3R1T4S-research (honest client; curl)'. Copies are saved in novelty_ws/r4/ of this panel. Every 200 response below was a real payload, not a challenge page.

Claimed value: 147 reduced additions (Perminov convention). Object file: object/2x5x5_m40_cr147_ZT_reduced.json (sha256 62737a117df29bc9dc6194509ed47f95a6f763ea3ca21fca84f79a78c44e6e1a, matching claim.SHA256SUMS).

## Primary tables

| source | URL | UTC fetch | HTTP | sha256 | value read |
|---|---|---|---|---|---|
| Perminov tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-16T00:18:26Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | truncated=false. 321 entries under schemes/results/addition_reduced_ZT/. The only file for 2x5x5 is `2x5x5_m40_cr153_cn283_ZT_reduced.json`, so the **minimum cr is 153**. There are no addition_reduced_ZT files for 5x2x5 or 5x5x2. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-16T00:18:39Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | `"2x5x5-40": {"Z": 313, "Z2": 218}`. Z 313 is comparable and higher. Z2 218 is over a different ring and not comparable. |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-16T00:18:39Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | The only 2x5x5 line is the rank table row (rank 40). No addition count is given for 2x5x5. |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-16T00:18:40Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No "Reduced additions improvement" entry for 2x5x5. The string 2x5x5 does not occur. |
| Lille page | https://fmm.univ-lille.fr/2x5x5.html | 2026-10-16T00:18:40Z | 200 | b1284cd181e11906ca3da9dbf7af7bc64f00eabc5a1b807111a8968c7608bcc4 | Rank 40, taken from Hopcroft and Kerr (SIAM J. Appl. Math. 20(1), 1971). **No Commentaries section.** No complexity variant is cited and no addition or operation count is stated. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-16T00:18:41Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row for 2,5,5: "✓ 40 Alphatensor-F2, ✓ 40 Alphatensor-Z, ... adds +256". The legend says "+N adds is the addition count (nz(U)+nz(V)+nz(W) − 2r − n·p)". This is a naive count, so it is not comparable. It is above 147 in any case. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-16T00:18:41Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48. Its only 2,5,5 entry is `{'format': [2, 5, 5], 'rank': 40, 'exponent': 2.828879}`. Rank 40 is the best known rank, so the scheme is eligible. |
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-16T00:18:41Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | No addition-count rows. No 2x5x5. Its matrix-multiplication rows are rank results over Q only. |
| open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-16T00:18:42Z | 200 | 28704d72eaed4c74b1b685f8b89a1c7e53bda8f9b69dec5d35584937a63c65c1 | 16 open PRs: 201, 200, 199, 198, 197, 196, 195, 194, 193, 192, 191, 190, 154, 153, 30, 9. I read every title and body. None is for fmm-additive-complexity-records and none gives a count for 2x5x5. The only regex matches were the word "additional" and "reduced fractions". |
| merged FMM packages | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-16T00:18:42Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 package folders. I fetched each folder's INDEX.csv once via raw.githubusercontent.com (2026-10-16T00:20:35Z to 00:20:41Z, all 200). An earlier attempt to fetch each CLAIM.md got 404 for all 21, because that layout does not exist. Twelve packages are addition counts: 4x6x6 r105 cr373, 5x7x7 r176 cr699, 6x6x7 r183 cr695, 6x8x8 r266 cr993, 4x6x8 r140 cr476, 6x6x6 r153 cr588, 5x6x7 r150 cr582, 4x6x7 r123 cr469, 6x6x8 r203 cr719, 5x5x8 r144 cr556 and 5x6x6 r130 cr502 (the eleven anonymous packages of 2026-10-15), plus 5x5x5 r93 cr358 (drzuzzjen). **None covers 2x5x5.** The other nine packages are rank results. The family INDEX.csv (sha256 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7) and README.md (sha256 740321f0f9287e13ee0f1dd229c47a974b49393560a453df125ad850b359ba07) list only rank results. |

No GitHub API request was refused this run, so the rerun fallback HTML pages were not needed. I made one extra fetch of https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns/faster-matrix-multiplication (2026-10-16T00:20:24Z, 200, sha256 8b5af3bbd20bb95deecedf722d5e8d68fde1f85e7220986ca52c60981a3285af). It confirmed the same 21 folders.

## Literature (last 24 months)

arXiv export API, 4 queries in total (an earlier http:// request got a 301 redirect with an empty body, then the https:// form was used):
1. One id_list request for 2512.21980, 2512.13365, 2604.27645, 2607.28676, 2609.32388 and 2609.06588 (2026-10-16T00:22:17Z, 200, sha256 f51ecc0487cea8cfa18d26891e64141549e52651794eb62dac6698ab25774ca9).
2. all:"matrix multiplication" AND (abs:additions OR abs:"additive complexity"), newest first, 100 results (00:23:18Z, 200, sha256 f744957dd18238a0f40bac3de611365da593a556f41e28c9f4a714ef18afce12).
3. abs:"matrix multiplication" AND (common subexpression OR straight-line OR arithmetic complexity) (00:23:22Z, 200, sha256 66832fde1222f6bd09b56985b209c9652b280ac345042afe33db9a024706e489).
4. abs:"matrix multiplication" AND (ternary OR flip graph(s) OR Brent equations) (00:23:47Z, 200, sha256 e40c9346cbeab35efdc3f13581acbc379ca7ffc931bce8bea04cca1885b9252c).

I also ran two web searches. Neither turned up any 2x5x5 rank-40 addition count beyond the sources below.

- **Perminov, arXiv:2512.13365v2.** Full text: https://arxiv.org/html/2512.13365v2, 2026-10-16T00:22:25Z, 200, sha256 7fbf6570ffe7c946d1561d56587f53939bfb8be542f21adb1641813f2c17de3e.
  - **It gives a count for 2x5x5.** Table 1 ("Schemes with optimal rank achieving new SOTA addition counts") has the row `2\times 5\times 5 | 40 | 283 | 156 | 154 | 154 | 153`. The columns are Naive, GV, GP-5, GP-40 and Proposed, so the best count is **153**.
  - It is comparable. Quote: "This work focuses exclusively on schemes with coefficients in the ternary set Z_{T}=\{-1,0,1\}". The count is plain common-subexpression elimination without basis change, the same convention as the repository file cr153.
  - **Table 6 does not include 2x5x5.** Its rows are 4x7x8, 4x8x8, 5x7x8, 6x6x10, 7x7x7, 7x8x8 and 8x8x8.
  - 147 < 153.
- **Martensson and Stankovski Wagner, IACR ePrint 2026/849.** Abstract page: https://eprint.iacr.org/2026/849, 2026-10-16T00:20:47Z, 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b. The PDF https://eprint.iacr.org/2026/849.pdf got 403 at 2026-10-16T00:20:48Z (sha256 of the saved challenge page 1761efab40880207c05cd53f9998eecc98a62f3f28a5235d29503b01c0b33eba). I did not retry. Per rerun note 2, I read the operator's text extraction instead (sha256 of the text file 99b19def9c130bd95e7dd894fdb4d172b5f87bf5a0344620b2d9c02d9307de60).
  - **Coverage: 2x5x5 is inside the paper's range.** The abstract says "optimize the number of additions for schemes with dimensions up to $(n, m, k) = (5, 7, 10)$", and the tables do contain 255-40.
  - **Comparable counts (over Z, ternary, no basis change):**
    - Table 3.3 (AlphaTensor schemes) row `255-40  283  156  154  0.29, 0, 0  156`, so the best is **154**. The caption reads: "All schemes have ternary coefficients. Recall that [14] assumes the KS framework while we do not." Its column header reads "without change of basis". The last value, 156, is the Karstadt-Schwartz (KS) count from [14], which allows a change of basis, so it is not comparable.
    - Table 3.4 ("Algorithms over Z", Moosbauer Z) row `255-40  682  323  313`, so the best is **313**.
  - **Not comparable (over Z2):**
    - Table 3.5 ("Algorithms over Z2") gives 218.
    - Table 3.6 gives 144 and 155. Its caption reads: "Results from applying Greedy Potential to a set of algorithms found by Deepmind [12, 30], all over Z2 . The top part consists of algorithm presented over Z2 in [12]." The 144 row (`255-40  256  148  144`) is in the top part. It is a mod-2 AlphaTensor scheme over a different ring, so it is not comparable.
  - The best comparable count in the paper for this format is 154. 147 < 154.
- **Martensson and Stankovski Wagner, IACR ePrint 2024/2063 ("The Number of the Beast", the predecessor of 2026/849).** Abstract page: https://eprint.iacr.org/2024/2063, 2026-10-16T00:24:36Z, 200, sha256 dafa562b4f1ff2dd5beac64491d2cdb5cffc9877bc93edf087215977a55bb133. The PDF got 403 at 2026-10-16T00:24:36Z (sha256 0389da80be5a66ef22cf55a233815baeba8a5de669aadc38f2a8b920e4729718); not retried. The abstract says only "very efficient for dimensions including (and surpassing) the 666 limit". See `unresolved:` below.
- **Martensson and Stankovski Wagner's fmm_add_reduction repository (it includes the hells_bells scheme set).**
  - Tree https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1: 2026-10-16T00:20:48Z, 200, sha256 dfdf1cd6a43106f75700703a917a5bb0ecdb971b27858e2bceafeb5718df1573. It came back with truncated=true and 65074 entries.
  - I fetched the following folder listings once each: contents/algorithms (00:21:48Z, 200, sha256 1058ca768cab872a4c6f811c8a6be8661fff93566c5e163dfbe9172e1887c77f), algorithms/other (00:21:54Z, 200, sha256 db23b35fa8b428128e7e2b2fe1c1763fa260e571b1a4e3e023c31523871786f8), algorithms/moosbauer (00:21:55Z, 200, sha256 e2eacfca2c01f6f9132f395b8736e603cfa21a7f5a89f2cbf97a6cad36c17eb3) and algorithms/other/unsorted (00:22:00Z, 200, sha256 cf0125af11315d657903cda62dbea6e9301480431fd4edaf23a65fabf508ba5b).
  - What they show:
    - hells_bells holds folders 222, 223, 224, 225, 226, 227, 228, 233, 234 and 333. There is no 255 folder, which would sort before 333.
    - grey holds no 255 file.
    - moosbauer holds only the input scheme `Moosbauer-255-40-mod0.exp/.m` (the naive-682 scheme of Table 3.4).
    - other and unsorted hold nothing for 255.
  - No reduced 2x5x5 count appears below 153.
- **Perminov, arXiv:2512.21980** (https://arxiv.org/html/2512.21980v1, 00:22:48Z, 200, sha256 7042544f98edaf71aa588c6c8f4f350d06f9b76ac91bbcaf2a579bba814db8d6). 3x3 only ("achieving a rank-23 scheme with only 58 scalar additions"). No count for 2x5x5.
- **Sun, arXiv:2604.27645** (https://arxiv.org/html/2604.27645v1, 00:22:49Z, 200, sha256 080416d6117d91b4b7b5b586f93e372f893a764bd0c6cfb66ace1661e1f1671e). 3x3 only ("rank-23 algorithm for general 3x3 matrix multiplication that uses 56 additions"). No count for 2x5x5.
- **Karunaratne and Idamekorala, arXiv:2607.28676** (https://arxiv.org/html/2607.28676v1, 00:22:49Z, 200, sha256 9a55bfe1cc9f6706e7133b0e9c29b8172a5414510520e27c8d79fee2564d15a9). 3x3 only ("a 55-addition realization of rank-23 multiplication of two arbitrary 3x3 matrices"). No count for 2x5x5.
- **Stapleton and Perminov, arXiv:2609.32388.**
  - The HTML page https://arxiv.org/html/2609.32388v1 returned 404 (00:22:50Z): no HTML rendering exists, which is not a block.
  - I read the PDF instead: https://arxiv.org/pdf/2609.32388v1, 00:22:59Z, 200, sha256 a5b84dba693efff328ce69c1d81934b82952f77e8572020074d78e57548b9e5c.
  - 3x3 only. It would also not be comparable, because it uses a change of basis ("51 additions and subtractions in alternative bases"). No count for 2x5x5.
- **Nielsen, arXiv:2609.06588** (https://arxiv.org/html/2609.06588v1, 00:22:50Z, 200, sha256 80aceffd92df45f035e4bd8c210fea14fad5620dfb39ba2dc8a1577ddeeb3607). 3x3 only, and not comparable: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change". No count for 2x5x5.
- **Other hits from the queries, checked for a 2x5x5 count.**
  - These three are rank or naive-count papers, and their full texts contain no 2x5x5 row:
    - arXiv:2511.20317 (https://arxiv.org/html/2511.20317v2, 00:23:47Z, 200, sha256 4724a50e77f0c8e2e4820c9efda3ac3177e7994223a394403a4e7dc9669fcfb6). Its count is "reduced naive addition complexity for 40 ternary schemes", a naive count.
    - arXiv:2606.02480 (https://arxiv.org/html/2606.02480v2, 00:24:00Z, 200, sha256 0f74f2206ae4add9ba08652a6718938b36ac0a987404ea1a019353673fcda37d).
    - arXiv:2603.02398 (https://arxiv.org/html/2603.02398v1, 00:24:02Z, 200, sha256 4223b911c664ac5348fd0984ddc4c5dad8e9c12ee783ce3b34196343f4a6c968).
  - These are about 3x3 or 4x4 only, judged from their titles and abstracts:
    - arXiv:2508.03857 (Stapleton, 3x3 at 60 additions).
    - arXiv:2601.05272 (3x3 at 59 operations, its own convention).
    - arXiv:2609.12027 (4x4x4:48, counts include scaling).

## Comparison

Comparable counts I could read for 2x5x5 at rank 40, all ternary over Z with no basis change:

| source | count |
|---|---|
| Perminov repository, minimum cr | 153 |
| Perminov arXiv:2512.13365 Table 1 | 153 |
| Martensson and Stankovski Wagner ePrint 2026/849, Table 3.3 | 154 |
| ePrint 2026/849 Table 3.4 and reduced_known.json Z | 313 |

The minimum is 153. The claimed 147 is strictly lower, by 6.

Counts I set aside:
- Lower but not comparable: 144 in Table 3.6 is over Z2, and Z2 218 also does not compare.
- Higher and not comparable: the KS-framework 156 (allows a change of basis) and the matmulcatalog naive +256.
- No count at all: the Lille page states none, and there is no open PR, merged package or trophy row for this format.

unresolved: IACR ePrint 2024/2063 PDF (403 challenge, not retried). It is the earlier version of 2026/849, which describes itself as "a major extension". That extension's best comparable count for 2x5x5 is 154, and Perminov's Dec 2025 paper ran the same team's tool (GP-40) on this scheme and got 154 too. So it is not plausible that 2024/2063 holds a comparable count below 147. A second gap: the recursive fmm_add_reduction tree was truncated, but the per-folder listings fetched above cover every top-level algorithm folder, and none holds a reduced 2x5x5 count. ePrint 2026/849 is not unresolved, because I read the operator's text.

## Verdicts

- **Full criterion (novelty part):** PASS. Rank 40 equals the best known rank in fmm_sota.json. 147 is strictly below the live minimum of Perminov's addition_reduced_ZT files (153), reduced_known.json, README and CHANGELOG. No count is published on the Lille page or in any variant it cites. The matmulcatalog adds value (+256) is naive and not comparable. No comparable count in the literature is at or below 147.
- **Partial win p1, as defined in this panel's brief** (strictly fewer than Perminov's live count, same convention): PASS, 147 < 153. Note that the bank's enumerated p1 in CLAIM.md is a different target: a 3x3x3 rank-23 scheme below 58. This 2x5x5 claim does not address it.
- Scope: this verdict is about novelty only. I did not check correctness of the straight-line program or of the count of 147; that belongs to the other skeptics.

pass: true
