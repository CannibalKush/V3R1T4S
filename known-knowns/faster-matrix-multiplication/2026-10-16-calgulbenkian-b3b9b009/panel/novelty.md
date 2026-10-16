# Novelty skeptic: 4x5x7 rank 104, 379 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Claim folder hashes: all five files read (CLAIM.md, INDEX.csv, table-record/README.md, and the object file name 4x5x7_m104_cr379_ZT_reduced.json) match claim.SHA256SUMS.

Fetch method: one plain curl request per URL, User-Agent 'V3R1T4S-research (honest client; curl)', no retries. Pages saved in the panel's novelty_ws folder. Times are UTC from `date -u`.

## Primary sources

| Source | URL | UTC time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T23:53:56Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | Not truncated. 195 files in addition_reduced_ZT. Exactly one for 4x5x7 at rank 104 (and none for any axis permutation): `4x5x7_m104_cr400_fv163_cn931_ZT_reduced.json`, so cr = 400. The naive_addition_reduced_ZT folder holds `4x5x7_m104_c924_ZT` and `4x5x7_m104_c927_ZT`; those are naive counts, a different convention. schemes/known/fmm_add_reduction holds Moosbauer files only up to 6x6x6, none for 4x5x7. Minimum reduced cr = 400. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T23:53:58Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | No "4x5x7-104" key. The largest 4x5 entry is "4x5x6-93": Z 542, Z2 465. |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T23:53:58Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | 4x5x7 appears only in the rank tables (rank 104, `Z/Q`; 104 in every column). No addition count for 4x5x7 is stated. |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T23:53:58Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No line mentions 4x5x7. None of the "Reduced additions improvement" entries is for this format. |
| Lille per-format page | https://fmm.univ-lille.fr/4x5x7.html | 2026-10-15T23:53:58Z | 200 | 60e8179037a90c97729cbe804347add757509088e65af3229154908495f71b7f | Rank 104: "The algorithm ⟨4×5×7:104⟩ is taken from: Manuel Kauers and Issaac Wood. Consequences of the Moosbauer-Poole algorithms. ... 2505.05896, arXiv, May 2025." There is no Commentaries section and no "best-known complexity" variant is cited. The cited work is a rank paper and states no addition count for this format. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T23:53:59Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | The cell for 4,5,7 reads "✓ 104 Dronperminov-ZT", adds "+927". The legend defines it as "`nz(U)+nz(V)+nz(W) − 2r − n·p`", a naive count with no common-subexpression sharing, so it is not comparable with the reduced convention. It is above 379 in any case. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T23:53:59Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48. Entry `{ "format": [4,5,7], "rank": 104, "exponent": 2.819543 }`. Rank 104 is the best known rank, so the scheme is eligible. |
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T23:54:00Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | No mention of 4x5x7 and no addition-count row. The matrix-multiplication rows are rank records for large formats only. |
| Open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T23:54:00Z | 200 | 12473dc228f9f201566453a3e87b1d4ed24a37bf8eca1240f665a443a7148a2e | 16 open PRs. I read every title and body. None names fmm-additive-complexity-records or 4x5x7. The only FMM PR is #197, a rank claim for 13x15x15. |
| known-knowns FMM family | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-15T23:54:01Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 dated package folders, with no format in their names. See the next row. |
| V3R1T4S repo tree (to map packages to formats) | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-10-15T23:54:58Z | 200 | f63c3cc8f48202557b7290f117f14aefdebe4f42ed79cf2448cb318d24b229db | Not truncated. The merged addition-count packages cover 4x6x6 cr373, 5x7x7 cr699, 6x6x7 cr695, 6x8x8 cr993, 4x6x8 cr476, 6x6x6 cr588, 5x6x7 cr582, 4x6x7 cr469, 6x6x8 cr719, 5x5x8 cr556, 5x6x6 cr502 (eleven anonymous packages) and 5x5x5 cr358 (drzuzzjen). No path anywhere in the repo contains 4x5x7 or an axis permutation of it. No merged package covers this format. |
| known-knowns INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-15T23:54:59Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | Rank rows for 13x14x14 through 15x16x16 only. Nothing for 4x5x7. |

The primary hashes match the author's table-record exactly: tree, reduced_known.json, README, CHANGELOG, Lille page, COVERAGE.md and fmm_sota.json. The live state has not changed since the author's fetch.

## Literature (last 24 months)

arXiv export API: the queries were sent to http first, and both returned 301 with an empty body. They were then sent over https once each.

- id_list query for 2512.21980, 2512.13365, 2604.27645, 2607.28676, 2609.32388, 2609.06588 and 2601.05272: https://export.arxiv.org/api/query?id_list=... at 2026-10-15T23:55:21Z, 200, sha256 147b75f0a48dc986cebb6144c54c20e9c2ed91f5dabc197edf10028aa0cb3daa.
- Query "matrix multiplication" AND (additions OR "additive complexity"), sorted by date, 60 results: 2026-10-15T23:55:21Z, 200, sha256 f47c1c4898d93dd84c4d7be929f5635b34b7128d08fdf9a7882e2ca1df536aea. Its only addition-count papers are the 3x3 series below and 2512.13365.
- Query "additions" AND "matrix multiplication" AND (rectangular OR "common subexpression" OR "straight-line"): 2026-10-15T23:55:37Z, 200, sha256 d3ada8260c4170441c5c32badc8a7570870920523b08b2484b7c2be7804e6f7a. It returned 18 results and no new addition-count paper for 4x5x7.
- Query for authors Martensson or Stankovski: 2026-10-15T23:56:38Z, 200, sha256 d85e5b27b9f6a2b41ce2ad7a055faee353f67573905aa5f0d485977792f7f881. Zero entries, so there is no arXiv copy of ePrint 2026/849.
- Web search: three queries. They found no 4x5x7 addition count and no other copy of ePrint 2026/849.

### Perminov, arXiv:2512.13365 (v2): gives a count for 4x5x7, and it is comparable

PDF https://arxiv.org/pdf/2512.13365v2, 2026-10-15T23:55:36Z, 200, sha256 82aff81bf22f80c13cf559f1c42ada3fecda51fb4efc773c3e7ee1ae5b135c27.

- Table 1, "Schemes with optimal rank achieving new SOTA addition counts", row: "4×5×7 104 931 423 413 405 400". The columns are Naive, GV, GP-5, GP-40 and Proposed. So the paper's best is 400. The Martensson-Wagner Greedy-Potential tool (fmm_add_reduction), run here as GP-40, reaches 405 on the same scheme.
- Comparability: "a parallel random-search method for reducing additive complexity in fast matrix multiplication algorithms with ternary coefficients {−1, 0, 1}". This is common-subexpression elimination on a fixed scheme with no basis change, at the same rank, and the result is the same as the repository's cr400.
- Table 6 (component-wise minima) lists 4×7×8, 4×8×8, 5×7×8, 6×6×10, 7×7×7, 7×8×8 and 8×8×8. 4x5x7 is not among them.
- Comparable counts read: 400 and 405. 379 beats both.

### Perminov, arXiv:2512.21980: no count for 4x5x7

"achieving a rank-23 scheme with only 58 scalar additions". The paper is about 3x3x3 only.

### Martensson, Stankovski Wagner and Stapleton, arXiv:2601.05272: no count for 4x5x7

"finding an algorithm requiring only 59 additions, still without a basis change". The paper is about 3x3 only.

### Sun, arXiv:2604.27645: no count for 4x5x7

"We present a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions". The paper is about 3x3 only.

### Karunaratne and Idamekorala, arXiv:2607.28676: no count for 4x5x7

"We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices." The paper is about 3x3 only.

### Stapleton and Perminov, arXiv:2609.32388: no count for 4x5x7

"We give a rank-23 algorithm for 3×3 matrix multiplication using 51 additions and subtractions in alternative bases." The paper is about 3x3 only, and the count uses a basis change, so it would not be comparable anyway.

### Nielsen, arXiv:2609.06588: no count for 4x5x7

"using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change". The paper is about 3x3 only, and the count uses a basis change, so it is not comparable.

### Martensson and Stankovski Wagner, IACR ePrint 2026/849: full text unread

- Abstract page https://eprint.iacr.org/2026/849: 2026-10-15T23:55:36Z, 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b. The paper was received 2026-04-30 and approved 2026-05-05. The abstract says: "We present improved methods for optimizing the number of additions in Strassen-type matrix multiplication schemes for larger matrix sizes, and without any change of basis." It also says: "We implement of our methods and use them to optimize the number of additions for schemes with dimensions up to (n, m, k) = (5, 7, 10)."
- PDF https://eprint.iacr.org/2026/849.pdf: 2026-10-15T23:55:36Z, 403. The response was a Cloudflare "Just a moment..." challenge page (sha256 d8cd2b3c5dbb24dd3e07c96cbd66791bcf01220c55b26a70b1775c09b21bcd3b). I did not retry.
- Authors' repository tree https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1: 2026-10-15T23:55:37Z, 403, "API rate limit exceeded" (sha256 3209519d06deb9f4f950810899ddc6fafba9bcfb3fb8cad8b5e1b30459ace147). I did not retry.
- Coverage: 4x5x7 lies inside the stated range up to 5x7x10. The counting convention is comparable: no basis change, additions of a straight-line program. Rank 104 for 4x5x7 dates from May 2025 (Kauers and Wood), before the paper was submitted. So the paper could plausibly hold a comparable count for 4x5x7 at rank 104. The abstract does not say that it does, and I found no copy of the tables.
- Its predecessor, ePrint 2024/2063 ("dimensions up to 666", Dec 2024), predates rank 104 for 4x5x7. That record fell from 109 to 104 only in May 2025. So the predecessor cannot hold a count at this rank.

### Martensson, Stankovski Wagner and Stapleton, IACR ePrint 2026/1688, "Hell's Bells" (fmm_add_reduction group): full text unread

- Abstract page https://eprint.iacr.org/2026/1688: 2026-10-15T23:57:15Z, 200, sha256 8269492c23b40e63ae3303a37993bdd76d42ecd633dbbfc1bea2099ad587b8ff. The abstract says: "We achieve record-low arithmetic (additive) complexity for various combinations of dimensions. For (n,m,k) = (2,2,k), our method performs particularly well." Its schemes are ternary and their additions are reduced separately, so the convention is comparable. The abstract names no 4x5x7 count.
- PDF https://eprint.iacr.org/2026/1688.pdf: 2026-10-15T23:57:22Z, 403, Cloudflare challenge (sha256 64909c23c562d2d57be83faba1f8a22044be0f8e2799369891322ff55ea003a3). I did not retry.

### Perminov, arXiv:2606.02480: no count for 4x5x7

Abstract https://arxiv.org/abs/2606.02480: 2026-10-15T23:57:15Z, 200, sha256 5d9c3e5e3342c9ac31483958c43e1230a2480105b0a0e4ac5bde309537dac043. "Compared to the previous state of the art, ranks are improved for 207 formats." This is a rank paper and gives no addition count.

unresolved: The full texts of IACR ePrint 2026/849 (PDF 403, Cloudflare challenge) and ePrint 2026/1688 (PDF 403, Cloudflare challenge) were not read, and the werekorren/fmm_add_reduction tree was not read (GitHub API 403, rate limit). ePrint 2026/849 covers formats up to 5x7x10, which includes 4x5x7. It counts additions without a basis change, which is comparable. It postdates the rank-104 scheme. So it could plausibly contain a comparable count for 4x5x7 at rank 104, and that count could be below 379. ePrint 2026/1688 and the repository could also plausibly hold one, though less likely. No read source shows that any of them actually covers 4x5x7 at rank 104. Perminov's live reduced_known.json, which imports external counts, has no 4x5x7 entry.

## Verdict

- Comparable counts read for 4x5x7 at rank 104, reduced convention:
  - Perminov's live minimum cr: 400
  - arXiv:2512.13365 Table 1: 400 (Proposed) and 405 (GP-40)
  - No 4x5x7 entry in reduced_known.json, README or CHANGELOG
  - No count on the Lille page or in the work it cites
  - matmulcatalog's +927 is a naive count, not comparable
  - No open PR, merged package or TROPHY_CASE row for this format
- 379 is strictly below every comparable count I read, by 21 against 400. It is not a tie.
- Full criterion: pass. Parts (a), (b) and (c) of the criterion are met. Rank 104 equals the best rank in fmm_sota.json. No unread source is known to cover this format at this rank. Residual risk: ePrint 2026/849 is unread, and 4x5x7 lies inside its stated range (see the unresolved line).
- Partial win p1, defined for this panel as strictly fewer than Perminov's live count under the same convention: pass (379 < 400). Note that the bank's own enumerated p1 is the 3x3x3 rank-23 partial win, which this claim does not address.

pass: true
