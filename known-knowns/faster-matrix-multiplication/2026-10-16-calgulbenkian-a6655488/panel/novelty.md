# Novelty check: 4x4x7 rank 85, 294 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Claim folder hashes checked against claim.SHA256SUMS: all 8 files OK.
Every fetch below was one plain curl GET with User-Agent "V3R1T4S-research (honest client; curl)", no retries. Saved copies are in the panel's novelty_ws/ folder.

## Primary sources (all HTTP 200)

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T23:53:56Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | tree not truncated; addition_reduced_ZT holds 195 files; the only 4x4x7 file is 4x4x7_m85_cr319_fv119_cn631_ZT_reduced.json, so the minimum cr for 4x4x7 at rank 85 is 319. No 4x7x4 or 7x4x4 file in any directory. naive_addition_reduced_ZT (the _cNNNN_ naive convention) has no 4x4x7 file. The fmm_add_reduction mirror (48 Moosbauer files) has no 4x4x7 file. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T23:53:57Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | no "4x4x7-85" key (largest 4x4 entries are 4x4x5-62 and 4x4x6-74) |
| Perminov README | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T23:53:58Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | the only 4x4x7 line is the rank table row "4x4x7 / 85 / 85 / 85 / 2.824617348"; no addition count for 4x4x7 |
| Perminov CHANGELOG | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T23:53:58Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | no mention of 4x4x7 or of 319 |
| Lille 4x4x7 page | https://fmm.univ-lille.fr/4x4x7.html | 2026-10-15T23:53:58Z | 200 | 8610f818a51ac353bbab8577a5eefe5d8c67150756a79aec673ae5ff652a46b5 | "4x4x7:85", taken from AlphaEvolve (Novikov et al., May 2025, arXiv:2506.13131). No Commentaries section and no "best-known complexity" variant. The only cited work gives a rank, not an addition or operation count (checked below). |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T23:53:59Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | row "4,4,7": "✓ 85 Alphaevolve", adds "+631". The page defines it as "nz(U)+nz(V)+nz(W) − 2r − n·p", a naive count with no shared subexpressions. It equals Perminov's cn631 naive count. It does not compare with a reduced count, and in any case 631 is above 294. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T23:53:59Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48; entry "format": [4,4,7], "rank": 85. So rank 85 is the best known rank and this format is eligible. |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T23:54:00Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | no 4x4x7 row and no addition-count row for this format (the matrix rows are rank records for 13x14x14 and up) |
| V3R1T4S open PRs | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T23:54:00Z | 200 | 12473dc228f9f201566453a3e87b1d4ed24a37bf8eca1240f665a443a7148a2e | 16 open PRs. I read every title and body. None targets fmm-additive-complexity-records or gives any count for 4x4x7. The only FMM PR is #197, a rank claim for 13x15x15. |
| V3R1T4S known-knowns FMM listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-15T23:54:01Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 dated package folders. Their contents are resolved by the next two rows. |
| known-knowns FMM INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-15T23:55:02Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | rank records only (13x14x14 and up); no 4x4x7 |
| V3R1T4S repo tree | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-10-15T23:55:09Z | 200 | f63c3cc8f48202557b7290f117f14aefdebe4f42ed79cf2448cb318d24b229db | No path in the repo contains 4x4x7, 4x7x4 or 7x4x4. The merged addition-count packages are 4x6x6 cr373, 4x6x7 cr469, 4x6x8 cr476, 5x5x8 cr556, 5x6x6 cr502, 5x6x7 cr582, 5x7x7 cr699, 6x6x6 cr588, 6x6x7 cr695, 6x6x8 cr719 and 6x8x8 cr993 (eleven), plus 5x5x5 cr358 (drzuzzjen). None covers 4x4x7. |

## Literature (last 24 months)

arXiv export API: four requests, the limit. The first was sent to the http URL and got a 301 redirect with no content. I counted it as used and sent the same id query to the https URL.

| Source | URL | UTC fetch time | HTTP | sha256 |
|---|---|---|---|---|
| arXiv id query (http) | http://export.arxiv.org/api/query?id_list=2512.21980,2512.13365,2604.27645,2607.28676,2609.32388,2609.06588,2601.05272&max_results=10 | 2026-10-15T23:55:27Z | 301 (empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| arXiv id query (https) | same query at https://export.arxiv.org | 2026-10-15T23:55:35Z | 200 | 147b75f0a48dc986cebb6144c54c20e9c2ed91f5dabc197edf10028aa0cb3daa |
| arXiv search au:Martensson AND abs:matrix | https://export.arxiv.org/api/query?search_query=au:Martensson+AND+abs:matrix&sortBy=submittedDate&sortOrder=descending&max_results=20 | 2026-10-15T23:56:25Z | 200 (0 entries) | 5c3cc8c271eaa15f9db1904ae8abcad725eb3986a8ecb4b3ecf54f471b07a553 |
| arXiv search abs:"matrix multiplication" AND abs:additions | https://export.arxiv.org/api/query?search_query=abs:%22matrix+multiplication%22+AND+abs:additions&sortBy=submittedDate&sortOrder=descending&max_results=60 | 2026-10-15T23:56:26Z | 200 | 8e3412ddc57bad85170f83ffa7c5fc8e2231fb994ad695e16b0855df75a60e2d |
| Perminov arXiv:2512.13365v2 PDF | https://arxiv.org/pdf/2512.13365v2 | 2026-10-15T23:55:42Z | 200 | 82aff81bf22f80c13cf559f1c42ada3fecda51fb4efc773c3e7ee1ae5b135c27 |
| ePrint 2026/849 abstract | https://eprint.iacr.org/2026/849 | 2026-10-15T23:56:00Z | 200 | 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b |
| ePrint 2026/849 PDF | https://eprint.iacr.org/2026/849.pdf | 2026-10-15T23:56:00Z | 403 (Cloudflare "Just a moment... Enable JavaScript and cookies to continue" challenge) | 4a29eaa6330dcddefd72b8f3587fe923ec0d3e50b49ce6ded8781ac1839f3b85 |
| werekorren/fmm_add_reduction tree | https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1 | 2026-10-15T23:56:00Z | 403 ("API rate limit exceeded") | 3209519d06deb9f4f950810899ddc6fafba9bcfb3fb8cad8b5e1b30459ace147 |
| ePrint 2026/1688 abstract (Hell's Bells) | https://eprint.iacr.org/2026/1688 | 2026-10-15T23:57:14Z | 200 | 8269492c23b40e63ae3303a37993bdd76d42ecd633dbbfc1bea2099ad587b8ff |
| ePrint 2026/1688 PDF | https://eprint.iacr.org/2026/1688.pdf | 2026-10-15T23:57:22Z | 403 (Cloudflare challenge) | 3d166dcdbfdd1ab909b4401a0e68c3fc6b245a57c80ae8eeb8a24700f4faf1b5 |
| AlphaEvolve arXiv:2506.13131 PDF (the Lille page's cited work) | https://arxiv.org/pdf/2506.13131 | 2026-10-15T23:57:40Z | 200 | f092c8cbd65da89951ee6496374da9a54963f9035758c25ac6e4625f506df9ad |

I also ran four web searches: the ePrint 2026/849 title, "4x4x7 rank 85 additions", "fmm_add_reduction 447 85", and "4x4x7 additive complexity AlphaEvolve 85". None returned a reduced addition count for 4x4x7 at rank 85. One search summary attributed to ePrint 2026/849 a "3x4x7 rank-63" program with divisions. I could not check that against the paper. It is a different format in any case.

### Per paper

- **Perminov, arXiv:2512.13365v2 (Parallel Heuristic Exploration...).** It gives a count for 4x4x7. Table 1 ("Schemes with optimal rank achieving new SOTA addition counts") has the row "4×4×7  85  631  326  323  320  319": naive 631, GV 326, GP-5 323, GP-40 320, proposed 319. This is comparable: the abstract says "reducing additive complexity in fast matrix multiplication algorithms with ternary coefficients {-1,0,1}". It is the same convention and rank, and the count is the same 319 as the live repository file. Table 6 ("Component-wise addition counts for schemes improvable by approaches result combination") lists only 4×7×8, 4×8×8, 5×7×8, 6×6×10, 7×7×7, 7×8×8 and 8×8×8. **4x4x7 is not among them.** GP-40 is the fmm_add_reduction (Mårtensson-Wagner Greedy-Potential) method, so that method's count on this scheme was 320.
- **Perminov, arXiv:2512.21980.** No count for 4x4x7. The paper covers 3x3 only: "a rank-23 scheme with only 58 scalar additions".
- **Mårtensson and Stankovski Wagner, IACR ePrint 2026/849** (received 2026-04-30). I could read only the abstract; the PDF was blocked. On coverage the abstract says "We implement of our methods and use them to optimize the number of additions for schemes with dimensions up to $(n, m, k) = (5, 7, 10)$." **4x4x7 is inside that range** (4 ≤ 5, 4 ≤ 7, 7 ≤ 10). The abstract also says "We also apply our algorithms to a large number of schemes where we do not have apples-to-apples results in the KS framework". Its convention is comparable: "optimizing the number of additions in Strassen-type matrix multiplication schemes ... without any change of basis". From the abstract I cannot tell whether it lists 4x4x7 at rank 85, or what count it gives. The authors' repository listing was rate-limited (403). Neither arXiv search found an arXiv copy.
- **Sun, arXiv:2604.27645.** No count for 4x4x7. It covers 3x3 only: "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions".
- **Karunaratne and Idamekorala, arXiv:2607.28676.** No count for 4x4x7. It covers 3x3 only: "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices."
- **Stapleton and Perminov, arXiv:2609.32388.** No count for 4x4x7. It covers 3x3 only, and its kernel count uses a basis change, so it would not compare anyway: "51 additions and subtractions in alternative bases. The input and output conversions require five further additions".
- **Nielsen, arXiv:2609.06588.** No count for 4x4x7. It covers 3x3 only and uses a basis change: "52 additions or subtractions, together with a Karstadt-Schwartz-style basis change".
- **Mårtensson, Stankovski Wagner and Stapleton, arXiv:2601.05272.** No count for 4x4x7. It covers 3x3 only: "finding an algorithm requiring only 59 additions, still without a basis change."
- **Hell's Bells, IACR ePrint 2026/1688** (Mårtensson, Stankovski Wagner, Stapleton; received 2026-08-14). I could read only the abstract; the PDF was blocked. It says "We achieve record-low arithmetic (additive) complexity for various combinations of dimensions. For $(n,m,k) = (2,2,k)$, our method performs particularly well." The abstract names no other formats. Its schemes come from its own neural generator, and the abstract does not say whether any is a 4x4x7 scheme at rank 85.
- **AlphaEvolve, arXiv:2506.13131** (cited by the Lille page). Gives a rank only: "⟨4, 4, 7⟩ 87 [93] 85". The full text states no addition or operation count for this format.

## Comparison

- The lowest comparable count I could read is 319: Perminov's live addition_reduced_ZT file (cr319) and Table 1 of arXiv:2512.13365.
- No lower count appears in reduced_known.json, the README, the CHANGELOG, the Lille page (no complexity variant), COVERAGE.md (naive 631, not comparable), TROPHY_CASE.md, the open PRs, or the merged packages.
- 294 is less than 319 (by 25), so it strictly beats every comparable count I read.

unresolved: ePrint 2026/849 PDF (403 Cloudflare challenge) and the werekorren/fmm_add_reduction repository tree (403 GitHub API rate limit). Their abstract puts 4x4x7 inside the paper's format range (up to 5x7x10), so the paper could plausibly hold a comparable count for 4x4x7. Nothing I read says it treats 4x4x7 at rank 85. The authors' own earlier method (GP-40) scored 320 on this scheme, so a count below 294 there seems unlikely, but I have not ruled it out. The ePrint 2026/1688 PDF (Hell's Bells, 403 Cloudflare challenge) is also unread. Its abstract claims records "for various combinations of dimensions" and names only (2,2,k); nothing read places 4x4x7 at rank 85 in it.

## Verdicts

- Full criterion: PASS. Rank 85 equals the fmm_sota.json best rank. 294 is strictly below 319, the minimum over Perminov's live files, reduced_known.json, README and CHANGELOG. The Lille page publishes no complexity count for this format and rank. COVERAGE.md shows only the naive 631. No merged package or open PR covers this format. No unread source is known to cover 4x4x7 at rank 85, but ePrint 2026/849 covers a format range that includes it (see unresolved).
- Partial win p1, as the brief defines it (strictly fewer than Perminov's live count, same convention): MET, 294 against 319. The bank's own enumerated p1 is a different thing: a rank-23 3x3x3 program below the live 3x3x3 count. This claim does not address that one.

pass: true
