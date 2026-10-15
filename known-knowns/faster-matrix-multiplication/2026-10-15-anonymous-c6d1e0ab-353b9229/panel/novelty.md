# Novelty check: 6x8x8 rank 266, 993 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Target: fmm-additive-complexity-records. Claim: a ternary straight-line program for the 6x8x8 rank-266 scheme with 993 additions under Perminov's reduced convention, against 1161.
Claim folder integrity: all 8 entries of claim.SHA256SUMS verified OK (object sha256 353b922983ecc35f13d03a9e7136407be941d5a3282630c9eb9c13af94c236ec).
Scope of this check: novelty only. I did not re-verify that the program is correct or recount its additions; that belongs to the other skeptics.

Every fetch below was one plain curl request with User-Agent 'V3R1T4S-research (honest client; curl)', no retries. Saved copies are in novelty_ws/ next to this folder.

## Primary sources

| Source | URL | UTC fetch time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov repo tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T11:38:35Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | Tree not truncated. schemes/results/addition_reduced_ZT holds 195 files. Exactly one addition_reduced_ZT file for 6x8x8 (no 8x6x8 or 8x8x6 file in any folder): 6x8x8_m266_cr1161_fv654_cn2780_ZT_reduced.json, so cr = [1161] and the minimum is 1161. No naive_addition_reduced_ZT file exists for this format. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T11:38:36Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | No "6x8x8-266" key. Its largest entry is "4x6x6-116". |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T11:38:36Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | The only 6x8x8 line is in the rank table: "6x8x8 / 266 / 266 / 266 / 2.814904236". It states no addition count for 6x8x8. |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T11:38:37Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | The string 6x8x8 does not appear. None of the "Reduced additions improvement" entries is for this format. |
| Lille per-format page | https://fmm.univ-lille.fr/6x8x8.html | 2026-10-15T11:38:37Z | 200 | 53797fcd03cb1fa8236289a63742f022ceb43d38539f43600a56dd33f9669cca | Rank 266: "The algorithm ⟨6×8×8:266⟩ is the (Kronecker) tensor product of ⟨2×2×2:7⟩ with ⟨3×4×4:38⟩." The page has no Commentaries section and cites no complexity variant. No addition or operation count appears on the page. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T11:38:38Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row for ⟨6,8,8⟩: "— / ✓ 266 Dronperminov-cr1161_fv654_cn2780_ZT_reduced / — / — / 266 in R/Q/Z / — / —". The adds column is "—", so no value is given. That column is a naive count (nz(U)+nz(V)+nz(W) − 2r − n·p), which is not comparable to reduced counts anyway. The scheme it holds is Perminov's cr1161 file. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T11:38:38Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48. The single [6, 8, 8] entry is rank 266 (exponent 2.814904). So 266 is the best known rank and the format is eligible (max dimension 8). |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T11:38:38Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | No fmm-additive-complexity-records entry. No addition count for any format. The only matrix multiplication rows are rank records for formats 13 to 16. |
| V3R1T4S open PRs | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T11:38:38Z | 200 | 1232e3cc680ac26d6174a430f2bc555b83fba1af177f26c2f9a5446c5721b008 | 42 open PRs. Two are for this target: #159 "⟨5,6,7⟩ rank 150 ternary SLP with 652 additions (table 664)" and #149 "⟨4,6,7⟩ rank 123 ternary SLP with 503 additions (table 517)". I scanned every title and body for 6x8x8 and its permutations, "266", "993" and "1161": no match. No open PR gives a count for 6x8x8. |

The values match the claim's table-record: the tree, reduced_known, README, CHANGELOG, Lille, COVERAGE and fmm_sota sha256 values are byte-identical to the author's earlier fetches.

## Literature (last 24 months)

arXiv export API, four requests in all:
- id_list lookup over http: http://export.arxiv.org/api/query?id_list=2512.21980,2512.13365,2604.27645,2607.28676,2609.32388,2609.06588 at 2026-10-15T11:40:10Z. HTTP 301 (a redirect to https, empty body). This is not a block.
- The same lookup over https at 2026-10-15T11:40:20Z. HTTP 200, sha256 b53faa947618f49a31c52db1dfa072b59d1c2e58c32dc44876546501bd45822b.
- Search: abs "matrix multiplication" AND (abs "additive complexity" OR "number of additions" OR "common subexpression"), at 2026-10-15T11:40:49Z. HTTP 200, sha256 a8aecf54c5415cef0d8e8fc013c0e65c03b34be5208694bc602b96b99da427eb. 13 hits. The only addition-count papers are 2512.21980 and 2512.13365.
- Search: (abs or title "matrix multiplication") AND (abs additions OR "arithmetic complexity" OR "straight-line" OR "scalar operations"), newest first, 80 results, at 2026-10-15T11:40:58Z. HTTP 200, sha256 c84aa3f2584db8c2a3aacbe84a7304c0539e86ebca4fdc00a167abc3a71cfa1b. The addition-count papers found were 2609.32388, 2609.06588, 2607.28676, 2604.27645, 2512.21980, 2512.13365, 2508.03857 (3x3) and 2609.12027 (4x4x4:48). None covers 6x8x8.

Two web searches surfaced arXiv 2606.02480 and ePrint 2024/2063, which I also checked below.

For each paper: does it give a count for 6x8x8, and is that count comparable?

- **Perminov, arXiv:2512.13365v2** (https://arxiv.org/html/2512.13365v2, 2026-10-15T11:40:26Z, HTTP 200, sha256 7fbf6570ffe7c946d1561d56587f53939bfb8be542f21adb1641813f2c17de3e).
  - **Yes, 1161, and it is comparable.** Its Table 1, "Schemes with optimal rank achieving new SOTA addition counts", has the row "6 × 8 × 8 … 266 2780 1244 1214 1181 1161". The columns are Naive, GV, GP-5, GP-40 and Proposed, so the published best is 1161.
  - Convention, quoted: "a parallel random-search method for reducing additive complexity in fast matrix multiplication algorithms with ternary coefficients {−1,0,1}". Common subexpression elimination "operates directly on a fixed scheme's c[oefficients]", with no basis change. This is the same convention as the claim.
  - Table 6 (component-wise minima) lists only 4x7x8, 4x8x8, 5x7x8, 6x6x10, 7x7x7, 7x8x8 and 8x8x8. 6x8x8 is not among them.
  - So the best published comparable count is 1161, and 993 is below it.
- **Perminov, arXiv:2512.21980.** No count for 6x8x8. It covers 3x3 only: "achieving a rank-23 scheme with only 58 scalar additions".
- **Sun, arXiv:2604.27645.** No count for 6x8x8. It covers 3x3 only: "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions".
- **Karunaratne and Idamekorala, arXiv:2607.28676.** No count for 6x8x8. It covers 3x3 only: "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices."
- **Stapleton and Perminov, arXiv:2609.32388.** No count for 6x8x8. It covers 3x3 only, and its kernel count is not comparable because it uses a basis change: "using 51 additions and subtractions in alternative bases."
- **Nielsen, arXiv:2609.06588.** No count for 6x8x8. It covers 3x3 only, and is not comparable: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change".
- **Mårtensson and Stankovski Wagner, IACR ePrint 2026/849.**
  - Abstract page: https://eprint.iacr.org/2026/849, 2026-10-15T11:39:37Z, HTTP 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b.
  - PDF: https://eprint.iacr.org/2026/849.pdf, 2026-10-15T11:39:37Z, HTTP 403 with a Cloudflare "Just a moment..." challenge, sha256 4982db22954adf0f40f3c0a72586cd09b9757608df087ddc86f8320cd7e267ea. Not retried.
  - Coverage, quoted from the abstract: "We implement of our methods and use them to optimize the number of additions for schemes with dimensions up to (n, m, k) = (5, 7, 10)."
  - **6x8x8 is outside that range.** Every arrangement of (6, 8, 8) has two dimensions equal to 8. The bound (5, 7, 10) allows only one dimension above 7, so no arrangement fits.
  - Comparability, quoted: "without any change of basis". So any count it gave would be comparable, but its stated range excludes this format.
- **Hells and others' fmm_add_reduction** (the authors' repository): https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1, 2026-10-15T11:39:37Z, HTTP 200, sha256 dfdf1cd6a43106f75700703a917a5bb0ecdb971b27858e2bceafeb5718df1573.
  - The response says "truncated": true and lists 65,074 entries.
  - The listed format folders are algorithms/hells_bells/{222, 223, 224, 225, 226, 227, 228, 233, 234, 333}, plus algorithms/grey with formats up to 2x3x4, 3x4x3 and 4x4x2.
  - No 6x8x8, 8x6x8 or 8x8x6 file or folder appears in the part that was returned.
- **Mårtensson and Stankovski Wagner, ePrint 2024/2063** ("dimensions up to 666"): https://eprint.iacr.org/2024/2063, 2026-10-15T11:41:56Z, HTTP 200, sha256 dafa562b4f1ff2dd5beac64491d2cdb5cffc9877bc93edf087215977a55bb133.
  - Coverage, quoted: "very efficient for dimensions including (and surpassing) the 666 limit, i.e. (n, m, k) = (6, 6, 6), in our reference set of fast multiplication algorithms".
  - The reference set is Moosbauer and Kauers. The abstract gives no 6x8x8 count, and the 2026 extension states its own range, (5, 7, 10), which excludes 6x8x8.
- **Perminov, arXiv:2606.02480**: https://arxiv.org/html/2606.02480, 2026-10-15T11:41:38Z, HTTP 200, sha256 0f74f2206ae4add9ba08652a6718938b36ac0a987404ea1a019353673fcda37d. No count for 6x8x8. It is a rank paper. Its Section 5.5 discusses additive complexity only as future work: "Minimizing additions is a natural next step after rank optimization."
- **Others found by the searches.** None of these gives a count for 6x8x8:
  - arXiv 2508.03857 is about 3x3: "from the previous records of 61 … to 60 without a change of basis".
  - arXiv 2601.05272 is about 3x3 and uses its own total-operations convention.
  - arXiv 2609.12027 is about 4x4x4:48 and counts "48 multiplications and 204 other operations (addition, subtraction or scaling by a constant)". Its convention includes scalings, so it is not comparable.
  - arXiv 2511.20317 minimizes naive additive complexity, which is a different convention.

Derived bound (not a published count; noted for honesty):
- The Lille page says the rank-266 scheme is the Kronecker product of ⟨2×2×2:7⟩ and ⟨3×4×4:38⟩.
- Perminov's repository has Winograd-type 2x2x2 at cr15 and 3x4x4:38 at cr125.
- Composing them recursively gives 125·4 + 38·15 = 1070 reduced additions, or 7·125 + 196 = 1071 in the other order.
- That bound is above 993, so it does not threaten the claim.

## Verdict

- Comparable counts read for 6x8x8 at rank 266: Perminov's live addition_reduced_ZT minimum is 1161 (one file), and arXiv:2512.13365 Table 1 also gives 1161.
- No lower or comparable count appears in reduced_known.json, README, CHANGELOG, the Lille page (no Commentaries section, no cited complexity variant) or matmulcatalog COVERAGE.md (adds "—").
- TROPHY_CASE.md and the open PRs have no entry for this format.
- 993 < 1161, a margin of 168, and 993 is also below the unpublished Kronecker composition bound of 1070.
- **Full criterion: PASS on novelty.** 993 is strictly below every comparable count I could read, and no unread source is known to cover 6x8x8 at rank 266. Rank 266 equals the best known rank in fmm_sota.json, and the format satisfies max dimension ≤ 8. This assumes the other panel members confirm the program is correct and the count is 993.
- **Partial win p1, as the panel brief defines it (strictly fewer than Perminov's live count, same convention): PASS**, 993 < 1161.
  - The bank's own enumerated p1 is specific to 3x3x3 rank 23 and does not apply to this format.

unresolved: two sources were not fully read.
- The ePrint 2026/849 PDF returned HTTP 403 with a Cloudflare challenge and was not retried. It is not plausible that it holds a comparable count for 6x8x8, because its abstract limits the paper to dimensions up to (5, 7, 10), and no arrangement of (6, 8, 8) fits inside that.
- The werekorren/fmm_add_reduction tree listing was truncated by GitHub after the hells_bells/333 folder, so folders after 333 were not listed. This is low plausibility, since the companion paper's stated range excludes this format, but it is not fully excluded.

pass: true
