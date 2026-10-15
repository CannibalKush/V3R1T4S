# Novelty review: 4x6x7 rank 123, 469 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Target: fmm-additive-complexity-records. Claimed cell: format 4x6x7, rank 123, 469 additions/subtractions under Perminov's reduced convention (sum over all forms of terms minus 1; negation free; coefficients in {-1,0,1}). Claim hashes checked against claim.SHA256SUMS: CLAIM.md, INDEX.csv, table-record/README.md and the object file all match.

Every page below was fetched once with curl, User-Agent 'V3R1T4S-research (honest client; curl)', no retries. Times are UTC. Pages are saved in the panel's novelty_ws folder.

## Primary tables

| Source | URL | UTC | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T11:38:38Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | truncated: false. addition_reduced_ZT files for 4x6x7: exactly one, schemes/results/addition_reduced_ZT/4x6x7_m123_cr517_cn1586_ZT_reduced.json, so cr = 517, minimum 517. Other 4x6x7 files are naive_addition_reduced_ZT/4x6x7_m123_c1562_ZT and _c1586_ZT (naive counts, different convention, not comparable), ZT/4x6x7_m123_ZT and one serendipitous_base file (no counts). No permuted format (4x7x6, 6x4x7, 6x7x4, 7x4x6, 7x6x4) appears. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T11:38:39Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | no 4x6x7 key; largest entries are 4x6x6-116 (Z2 581) and 4x5x6-93 (Z 542). |
| Perminov README | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T11:38:39Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | only rank rows for 4x6x7 ("123 (?) / 123 / 123" for ZT / Z / Q ranks); no addition count for 4x6x7. |
| Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T11:38:40Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | no line mentions 4x6x7; no reduced-additions entry for this format. |
| Lille 4x6x7 page | https://fmm.univ-lille.fr/4x6x7.html | 2026-10-15T11:38:40Z | 200 | 46442ede7f2649079321c1b5f681ae6a9f962c0b34956e5da9e319ba4c8fa62b | rank 123 ("The algorithm 4x6x7:123 is taken from: Manuel Kauers and Isaac Wood. Consequences of the Moosbauer-Poole algorithms ... arXiv 2505.05896"). No Commentaries section; no complexity variant cited; the cited work states no addition or operation count (its abstract is about ranks only, see below). |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T11:38:40Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | row 4,6,7: "123 Dronperminov-ZT ... adds +1586". The legend says "+N adds is the addition count (nz(U)+nz(V)+nz(W) − 2r − n·p)": a naive count, not comparable to a reduced count, and in any case far above 469. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T11:38:41Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48; entry {format [4, 6, 7], rank 123, exponent 2.817458}. Rank 123 is the best known rank, so the scheme is eligible. |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T11:38:41Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | no addition-count rows and no 4x6x7 entry (matrix rows are rank records for larger formats). |
| V3R1T4S open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T11:38:41Z | 200 | 1232e3cc680ac26d6174a430f2bc555b83fba1af177f26c2f9a5446c5721b008 | 42 open PRs read (title and body). Relevant: #149 and #159 (below). No other open PR names this target or 4x6x7. |

All seven primary-table hashes equal the hashes in the author's table-record, so the live pages are unchanged since the author's comparison.

Open PR #149 (DrZuzzjen, head c019f1ac48d6eeab859164a5dc108d378f3bfcf9), title "[claim] fmm-additive-complexity-records: 4,6,7 rank 123 ternary SLP with 503 additions (table 517)". Quoted: "computes A*B exactly over Z with 503 additions/subtractions under Perminov's reduced convention (recounted with the same counter that reproduces 517 on Perminov's file)". Known count: 503, same convention, same rank. 469 is below it by 34.

Open PR #159 (5x6x7 rank 150, 652 additions) is a different format. Its body also states: "Prior closed PR #10 concerns 4x6x7 at 505 additions, and our open PR #149 concerns the same 4x6x7 cell at 503 additions". Known count 505 (closed PR, not read directly); 469 is below it.

Primary verdict: no primary page was blocked, so no PENDING STATUS CHECK.

## Literature (last 24 months)

arXiv export API requests (four in total): two plain-http requests returned 301 redirects with empty bodies (2026-10-15T11:39:51Z and 11:39:56Z, sha256 of empty body e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855); the same two queries over https returned 200:
- id_list query for 2512.21980, 2512.13365, 2604.27645, 2607.28676, 2609.32388, 2609.06588, 2505.05896, 2601.05272: https://export.arxiv.org/api/query?id_list=... at 2026-10-15T11:40:05Z, 200, sha256 1a5ebcdc32497e4e509d6cd2880e6631d32ed453384dbac095359e1f37c5c5eb.
- search abs:"matrix multiplication" AND (abs:additions OR abs:"additive complexity"), newest first, 60 results: 2026-10-15T11:40:09Z, 200, sha256 a6fa98c9a641523eee01eb6cd71aeb19d676273c4bb253efe9c7633e6f104b9b. Relevant hits are the papers below plus 2511.20317 (Perminov, ternary meta flip graphs, naive additive complexity only) and 2607.29291 (F2 SAT certificates, rank only). No other paper gives a 4x6x7 addition count.
Two web searches (Mårtensson-Wagner title; "4x6x7 ... rank 123 additions") found no further 4x6x7 addition count and no arXiv or conference copy of ePrint 2026/849.

| Paper | Fetch | Count for 4x6x7? | Settling sentence |
|---|---|---|---|
| Perminov, arXiv:2512.13365v2 | https://arxiv.org/pdf/2512.13365v2, 2026-10-15T11:40:24Z, 200, sha256 82aff81bf22f80c13cf559f1c42ada3fecda51fb4efc773c3e7ee1ae5b135c27 | Yes. Table 1 ("Schemes with optimal rank achieving new SOTA addition counts"), row "4×6×7 123 1586 535 533 518 517": naive 1586, Greedy-Vanilla 535, GP-5 533, GP-40 518, proposed 517. Comparable (ternary, no basis change, same rank, same reduced convention); the minimum is 517. 4x6x7 is NOT in Table 6 (Table 6 lists 4x7x8, 4x8x8, 5x7x8, 6x6x10, 7x7x7, 7x8x8, 8x8x8). | "This paper presents a parallel random-search method for reducing additive complexity in fast matrix multiplication algorithms with ternary coefficients {-1,0,1}." |
| Perminov, arXiv:2512.21980 | arXiv id_list query above | No, 3x3x3 only (58). | "achieving a rank-23 scheme with only 58 scalar additions." |
| Mårtensson, Stankovski Wagner, Stapleton, arXiv:2601.05272 | arXiv id_list query above | No, 3x3x3 only (59). | "finding an algorithm requiring only 59 additions, still without a basis change." |
| Sun, arXiv:2604.27645 | arXiv id_list query above | No, 3x3x3 only (56). | "We present a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions and 23 multiplications". |
| Karunaratne and Idamekorala, arXiv:2607.28676 | arXiv id_list query above | No, 3x3x3 only (55). | "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices." |
| Stapleton and Perminov, arXiv:2609.32388 | arXiv id_list query above | No, 3x3x3 only; and its 51 is after a basis change, so not comparable even there. | "We give a rank-23 algorithm for 3×3 matrix multiplication using 51 additions and subtractions in alternative bases." |
| Nielsen, arXiv:2609.06588 | arXiv id_list query above | No, 3x3x3 only; uses a basis change, not comparable. | "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change". |
| Kauers and Wood, arXiv:2505.05896 (cited by Lille) | arXiv id_list query above | No addition count; rank paper. | "we found improved matrix multiplication schemes for various rectangular matrix formats using a flip graph search." |
| Perminov, arXiv:2606.02480 (found by web search) | https://arxiv.org/abs/2606.02480, 2026-10-15T11:41:40Z, 200, sha256 5d9c3e5e3342c9ac31483958c43e1230a2480105b0a0e4ac5bde309537dac043 | No addition count in the abstract; rank and coefficient-class paper. | "Compared to the previous state of the art, ranks are improved for 207 formats." |
| Mårtensson and Stankovski Wagner, ePrint 2024/2063 (ACDA25, "Number of the Beast") | https://eprint.iacr.org/2024/2063, 2026-10-15T11:41:41Z, 200, sha256 dafa562b4f1ff2dd5beac64491d2cdb5cffc9877bc93edf087215977a55bb133 | Outside range: 4x6x7 has a dimension 7, beyond 6x6x6. Perminov's reduced_known.json, whose entries all stay within 6x6x6, has no 4x6x7 key. | "very efficient for dimensions including (and surpassing) the 666 limit, i.e. (n, m, k) = (6, 6, 6), in our reference set". |
| Mårtensson and Stankovski Wagner, ePrint 2026/849 | abstract page https://eprint.iacr.org/2026/849, 2026-10-15T11:40:25Z, 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b. PDF https://eprint.iacr.org/2026/849.pdf, 2026-10-15T11:40:25Z, 403, a Cloudflare "Just a moment..." challenge page (sha256 d74c7d1413a68b97c324be4fcf4217427192d88d4435f04eede7b6cc31028619); not retried. | Unknown. 4x6x7 IS inside the range of formats the paper covers. Whether it reports a count for 4x6x7 at rank 123 cannot be read. Its counts would be comparable in convention (no basis change). | "We implement of our methods and use them to optimize the number of additions for schemes with dimensions up to (n, m, k) = (5, 7, 10)." and "We present improved methods for optimizing the number of additions in Strassen-type matrix multiplication schemes for larger matrix sizes, and without any change of basis." |
| werekorren/fmm_add_reduction (authors' repository, Hells and others) | tree https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1, 2026-10-15T11:40:25Z, 200, sha256 dfdf1cd6a43106f75700703a917a5bb0ecdb971b27858e2bceafeb5718df1573 (GitHub marked it truncated at 65074 entries). Because of the truncation, one non-recursive listing: https://api.github.com/repos/werekorren/fmm_add_reduction/contents/algorithms/hells_bells, 2026-10-15T11:41:11Z, 200, sha256 f3e52cb096f5292ed759cf99810bf9e4b09a287716b36e4ef531f9653d8e8754. README https://raw.githubusercontent.com/werekorren/fmm_add_reduction/main/README.md, 2026-10-15T11:41:11Z, 200, sha256 37b319e0a3cb960cb612d56e1b53ac61bdfcdd673a0cd9ebafd9599cc055e842. | No. Top folders are algorithms/grey (13 files, formats no larger than 4x4x2, 4x3x3, 3x4x3 and 5x2x2) and algorithms/hells_bells with only 222, 223, 224, 225, 226, 227, 228, 233, 234, 333, 432, 532. No 4x6x7 (or permutation) file anywhere. | README: "This is further described in the ACDA25 paper 'The Number of the Beast: Reducing Additions in Fast Matrix Multiplication Algorithms for Dimensions up to 666'." |

Indirect evidence on ePrint 2026/849: Perminov's Dec 2025 Table 1 already ran Greedy-Potential (the Mårtensson-Wagner method, GP-40) on this rank-123 scheme and got 518; the authors' public repository holds no 4x6x7 scheme; Perminov's live README lists that repository as a tracked data source and his live tree still shows 517 as the minimum. None of this proves the PDF lacks a lower 4x6x7 count, but no source I could read reports or cites one.

## Known comparable counts for 4x6x7 at rank 123

517 (Perminov live file, and 2512.13365 Table 1), 518 (GP-40), 533 (GP-5), 535 (GV), 503 (open V3R1T4S PR #149), 505 (closed V3R1T4S PR #10, as reported in PR #159). Smallest known: 503. Not comparable: 1586 and 1562 (naive counts), COVERAGE +1586 (naive).

469 is strictly below every comparable count I could read (below 503 by 34, below 517 by 48). It is not a tie.

unresolved: ePrint 2026/849 PDF (https://eprint.iacr.org/2026/849.pdf, HTTP 403 Cloudflare challenge, not retried). Its abstract says it optimizes additions without a change of basis for schemes up to (5,7,10), so 4x6x7 is inside its range and it could plausibly contain a comparable count for 4x6x7; whether it covers rank 123 and whether any such count is below 469 is unknown. Nothing I could read (the authors' repository, Perminov's live tree, README, reduced_known.json and 2512.13365) reports or cites a 4x6x7 count from it. The panel should read this PDF by another honest route before publication.

## Verdicts

Full criterion: PASS. 469 is strictly below (a) the minimum cr 517 over Perminov's live addition_reduced_ZT files for 4x6x7 rank 123, with no lower value in reduced_known.json, README or CHANGELOG; (b) the Lille page, which has no Commentaries section and cites no complexity variant; (c) COVERAGE.md, whose +1586 is a naive count; rank 123 equals the fmm_sota.json best rank; and 469 also beats the open competing claim of 503 (PR #149) and 505 (closed PR #10). The one unread source (ePrint 2026/849 PDF) covers the dimension range but is not known to cover this format at rank 123; this is a stated risk, not a known lower count.

Partial win p1 (as defined for this panel: strictly fewer than Perminov's live count, same convention): PASS, 469 is less than 517. Note that the bank's own enumerated p1 text concerns 3x3x3 rank 23 and does not apply to this format.

pass: true
