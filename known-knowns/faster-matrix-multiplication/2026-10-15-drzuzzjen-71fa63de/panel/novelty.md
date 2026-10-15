# Novelty review: <5,5,5> rank 93 ternary SLP, 358 additions (claim r1520)

(Saved verbatim by the run's main session from the subagent's returned text; subagents in this harness return
findings as text instead of writing files. work/ refers to the skeptic's own isolated scratch folder.)

Reviewer: NOVELTY skeptic (one of three). Input: a copy of claim/ plus my own web fetches. Every fetch was one plain curl per URL with `-A "V3R1T4S-panel (honest client; curl)" -w '%{http_code}'`, no retries, no browser imitation. Time is `date -u` taken right before each request. Each page is saved under work/ and its sha256 is listed here. Full log: work/FETCH_LOG.txt.

Claimed object: `5x5x5_m93_cr358_ZT_reduced.json`, sha256 `71fa63deb8df8c92975304438d449e61cd92b777fcd2bec9cb2090c01e129f5c`. This matches claim/CLAIM_SHA256.txt.

## Primary sources (fetched 2026-10-15)

| # | time (UTC) | HTTP | sha256 | URL | value found |
|---|---|---|---|---|---|
| 1 | 2026-10-15T15:21:27Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | `truncated: false`, 6637 entries. The tree has 9 files for 5x5x5, across all directories: `known/alpha_evolve/5x5x5_m93_mod0.json`, `known/alpha_tensor/5x5x5_m98_Z.json`, `known/tensor/5x5x5_tensor.mpl`, `results/addition_reduced_ZT/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json` (the only addition_reduced file for 5x5x5 in any directory), `results/naive_addition_reduced_ZT/5x5x5_m93_c843_ZT.{json,m}` and three `results/serendipitous_base/5x5x5_m93_*_ZT.json`. The **minimum cr in addition_reduced_ZT for 5x5x5 rank 93 is 383**. |
| 1b | 2026-10-15T15:22:34Z | 200 | 808285b8fb393d2e950ecff4ffe9881a209b6d3eff0d787e34d801a3f22293da | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json | The file states `complexity {naive 843, reduced 383}`. My own counter also gives 383. It is byte-identical to claim/reference/ (same sha256). |
| 2a | 2026-10-15T15:21:29Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | The only 5x5x5 row is the rank table (93/93/93, ω 2.816262409). No 5x5x5 addition count appears, and nothing below 383. |
| 2b | 2026-10-15T15:21:30Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | No mention of 5x5x5, and no count 358 or 383. |
| 2c | 2026-10-15T15:21:30Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | There is no `5x5x5-93` key. The largest square entry is 4x4x4. |
| 2d | 2026-10-15T15:22:40Z | 200 | 0ca5f642860ed79cac76e72bccbac40276096484b9dfa413151cdb432b0d17ad | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/commits?per_page=10 | The latest commit is 2026-10-13T14:54:59Z ("add .sms read/save"). None of the last 10 commits touches 5x5x5 additions. |
| 3 | 2026-10-15T15:21:31Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | createdAt 2026-10-09T11:45:48. Entry `{"format":[5,5,5],"rank":93,"exponent":2.816262}`. **The best rank is 93**, and the claim uses rank 93. |
| 4 | 2026-10-15T15:21:31Z | 200 | 3daec22adb7e0efa20ebc2f2e9847b32951da7c57dc0980fbd00bc476645b593 | https://fmm.univ-lille.fr/5x5x5.html | The page shows ⟨5×5×5:93⟩ from Moosbauer-Poole (arXiv:2502.04514), a group of 3 isotropies, and links to the tensor, LRP, raw and sym maple files. **It cites no complexity variant and no addition count.** I did not download the linked .mpl.bz2 files. |
| 5 | 2026-10-15T15:21:32Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | Row `⟨5,5,5⟩`: ✓ 93 (Alphaevolve) over F₂ and R/Q/Z, **adds +846**. This is a naive nz-based count. It is the only rank-93 scheme listed, and none has a count below 358. |
| 7a | 2026-10-15T15:21:32Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | There are no fmm-additive-complexity-records rows. The matrix-multiplication rows are rank records only, for <13..15,…> over Q. **No 5x5x5 entry.** |
| 7b | 2026-10-15T15:21:33Z | 200 | 48c623ce3a79aaba234d4ce2137c013a3aa8385426a61d6e53054d64384ee511 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | There are 66 open PRs (fewer than 100, so the list is complete), and I read every title and body. Open fmm-additive-complexity-records PRs: calgulbenkian #185 <6,6,6>, #184 <4,6,6>, #183 <5,6,6>, #181 <5,5,8>, #180 <4,6,8>, #173 <6,8,8>, #171 <6,6,8>, #167 <6,6,7>, #165 <5,7,7>, #162 <5,6,7>, #161 <4,6,7>; DrZuzzjen #159 <5,6,7>, #149 <4,6,7>. **No open PR covers 5x5x5** in its title or body. |
| 7c | 2026-10-15T15:21:34Z | 200 | 953c527e335e70ba978e7f3c62053743a7ff330fb56ade8659f4bb9f069deb2f | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/pulls?state=open&per_page=100 | There is 1 open PR: #6 (nehal-a2z), "Add 160-addition evaluation of the 3x4x5 rank-47 scheme". It does not cover 5x5x5. |
| 7d | 2026-10-15T15:25:18Z | 200 | 9e884e9084f3e924abe3ab91665eca9ead09ce01a07b6ad910b481b757db5a99 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=closed&per_page=100 | I checked closed PRs as an extra step (#21 through #182). **Closed, unmerged PR #21** (calgulbenkian, opened 2026-10-14T04:06:15Z, closed 2026-10-14T12:52:19Z, merged_at null) claims "(5, 5, 5) rank 93 SLP in 378 additions over Z (beats 383 by -5)". The other closed fmm-additive PRs (#22–#27) cover other formats. |
| 7e | 2026-10-15T15:25:36Z | 200 | 1a91db1be8cda833df7a957ab7f17b5c8648519a7042ab9eb972afa40fcb0e16 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/21/files?per_page=100 | This lists the PR #21 object, `.../object/5x5x5_m93_cr378_fv157_cn844_ZT_reduced.json`. |
| 7f | 2026-10-15T15:25:42Z | 200 | 118237670d742163d9f8caa3fd4e5c6a850fe9570fbb39ce3f32906b427c2a4a | https://raw.githubusercontent.com/calgulbenkian/V3R1T4S/8349fb0300c2b11cafbc950fa9b4a8740c6c8460/known-knowns/faster-matrix-multiplication/2026-10-14-anonymous-c6d1e0ab-11823767/object/5x5x5_m93_cr378_fv157_cn844_ZT_reduced.json | The sha256 equals the one stated in the PR. The file states `reduced 378`, and my own counter gives **378**. It is ternary and computes the product exactly over Z. 378 > 358. |

The primary sources match the claim's sources/ copies. The sha256 values of my fetches 1, 2a, 2b, 2c, 3, 4, 5 and 7b are identical to those in claim/sources/FETCH_LOG.md, which were fetched about one minute earlier at 15:20Z.

## Independent count (own script, work/scripts/count.py, sha256 c52728930100e2eae3e907d3024ab81d18654b3988618dac4e27b158db577b15)

The script follows Perminov's reduced convention: the cost is the sum of (terms − 1) over u_fresh, v_fresh, w_fresh, u, v and w, and every coefficient is ±1. It expands each scheme symbolically and checks it against the C^T tensor. I wrote it without reading the author's checker.

| file | stated reduced | counted | ternary | exact over Z |
|---|---|---|---|---|
| claim object (5x5x5_m93_cr358) | 358 | **358** | yes | yes |
| Perminov live cr383 | 383 | 383 | yes | yes |
| V3R1T4S closed PR #21 (cr378) | 378 | 378 | yes | yes |

## Literature, last 24 months (arXiv API over https, 2024-10-15 to 2026-10-15)

| time (UTC) | HTTP | sha256 | query |
|---|---|---|---|
| 2026-10-15T15:23:06Z | 200 | 0c7538adcdcc715499245e780a8c7c6fe4dbbc6a368df15488c699b3ba9379c2 | abs:"matrix multiplication" AND abs:additions (371 hits, newest 60) |
| 2026-10-15T15:23:10Z | 200 | 3ae30c0b3acffbe5712a67ab4deffd51b26ee41e08fb8a1fd543ba98bc88f3ba | id_list 2512.13365, 2502.04514, 2506.13242, 2512.21980 |
| 2026-10-15T15:23:14Z | 200 | f2dada10f145d125022f8ca3f7dfdd060ecc7025aa01afbb97d80c3e0ba64fa2 | MM AND (additive complexity OR common subexpression OR addition count) |
| 2026-10-15T15:23:18Z | 200 | d2bd7de31e655ef3c70c9f1805f2bdd3a135bcd7076c4f86facc4ebf6cc0b489 | MM AND (flip graph OR AlphaEvolve OR "5x5") |
| 2026-10-15T15:23:35Z | 200 | 7fbf6570ffe7c946d1561d56587f53939bfb8be542f21adb1641813f2c17de3e | https://arxiv.org/html/2512.13365v2 (full text) |
| 2026-10-15T15:23:55Z | 200 | e348dcdc640c2d9a96b30a50ccf054be4f0edd64cf686e6b1e10809e52d5d5ff | au:Martensson AND abs:matrix (0 hits) |
| 2026-10-15T15:23:59Z | 200 | c9b3d9a1740baaa687cb7687b526b310a8769884fd7118c892539ea83817081f | (au:Dumas OR au:Sedoglavic OR au:Pernet) AND abs:matrix |
| 2026-10-15T15:24:03Z | 200 | 42c08250adf335c62bb3838358daa8d0466ce55cb2791d9e0530b76fee0228e5 | (au:Perminov OR au:Moosbauer OR au:Kauers) AND abs:matrix |
| 2026-10-15T15:24:06Z | 200 | b6243d42ae51e83cd8b23ef282b6d6a01babcb8722c8f349e89b41e7b1493a6e | MM AND (straight-line OR bilinear) AND additions |
| 2026-10-15T15:24:24Z | 200 | c2519d61eeab3bbb91d4389b2441e118b00358ca32b5d728aff892b6f1466b64 | au:Wagner AND abs:"matrix multiplication" |
| 2026-10-15T15:24:31Z / 15:25:06Z | 200 / 200 | d5b2448e… / b6f2b2f8… | ti:"number of the beast"; ti:beast AND ti:matrix (0 hits for both) |

Hits relevant to 5x5x5 rank 93:
- **Perminov, arXiv:2512.13365v2** (2025-12-15), "Parallel Heuristic Exploration for Additive Complexity Reduction…". The table row for 5×5×5 at rank 93 reads: Naive 843, GV 392, GP 391, GP 387, Proposed **383**. This is the best published count and the same as the live repo value. The GP columns are the Mårtensson-Wagner greedy-potential method, run at two settings.
- **Mårtensson-Wagner**, "The Number of the Beast…" (ACDA25), via the repo werekorren/fmm_add_reduction:
  - Fetches: README 2026-10-15T15:24:48Z, HTTP 200, 37b319e0…; tree 15:22:35Z, 200, dfdf1cd6…, truncated; `algorithms/` 15:24:48Z, 200, 1058ca76…; `algorithms/moosbauer` 15:24:55Z, 200, e2eacfca…; `algorithms/other` 15:24:56Z, 200, db23b35f….
  - The repo holds 5x5x5 *input* schemes only: `Moosbauer-555-93-mod0.exp`, `MoosbauerPooleKemper-555-93-mod0.exp`, 555-95/97 and `Adaptive-555-94-mod2.m`.
  - It has no published 5x5x5 rank-93 output count. The paper is not on arXiv; my API search returned 0 hits. Its method's result on this scheme is covered by the GP columns (391/387) of 2512.13365.
- **Moosbauer-Poole, arXiv:2502.04514** (2025-02-06) gives the rank-93 scheme with symmetry, but no addition count.
- **Kauers-Wood, arXiv:2505.05896** gives consequences of the Moosbauer-Poole scheme; no 5x5x5 addition count. Kauers-Moosbauer-Wood, arXiv:2602.11041, concerns exponent and leading coefficient for 6x6, with no 5x5x5 SLP count.
- **AlphaEvolve:** the only 5x5x5 artefact found is the rank-93 mod0 scheme in Perminov known/alpha_evolve. It gives no addition count.
- **Perminov, arXiv:2511.20317, 2603.02398 and 2606.02480** are rank and ternary-coefficient searches. They are naive-complexity only, with no reduced count for 5x5x5 below 383.
- **arXiv:2512.21980, 2604.27645, 2609.06588 and 2609.32388** are 3x3x3 addition records only. **arXiv:2506.13242 and 2506.19405** (Dumas-Pernet-Sedoglavic) cover 4x4x4 and 2x2x2 accuracy and operation counts, not 5x5x5. **arXiv:2606.13408** (the catalog) has no 5x5x5 addition count in its abstract.
- **jgdumas/plinopt** (tree 15:22:38Z, 200, 0fbfae75…; 407 entries, not truncated) has no 5x5x5 or rank-93 file.
- **dronperminov/ternary_addition_reducer** (tree 15:22:40Z, 200, 1da19dce…; 14 entries) contains code only, with no result files.

## Constructions

- 5 is prime, so no Kronecker or tensor product of smaller formats yields <5,5,5>.
- The Moosbauer-Poole scheme is Z/3-symmetric (Lille: a group of 3 isotropies). The symmetry-based and cyclic sources I found (2502.04514, the Lille page, werekorren's Moosbauer files) publish no shorter program, and none gives 358 or fewer.
- Lille's "maple evaluation scheme" (5x5x5_raw.mpl.bz2) was not downloaded, and the page states no count for it. Counts from alternative-basis constructions (Dumas et al.) use a different convention and do not exist for 5x5x5 in what I found.

## Comparison

- Best known reduced count for <5,5,5> at rank 93 in the criterion sources: **383** (Perminov live repo, matching arXiv:2512.13365).
- matmulcatalog: 846 (naive). Lille: none. reduced_known.json: none. TROPHY_CASE: none. Open PRs (V3R1T4S and Perminov): none for 5x5x5.
- Lowest publicly visible count anywhere: **378**, in closed and unmerged V3R1T4S PR #21 (calgulbenkian, 2026-10-14). It is not a criterion source, but I compared against it anyway.
- The claim's **358** is strictly below all of these: 25 below 383 and 20 below 378. It is not a tie.

injection_suspected: none. PR bodies contain only "Generated with Claude Code" attribution footers, and no page addressed agents.

context: Claude Code Agent-tool subagent, model claude-opus-5-5, effort high, saw only a copy of claim/ plus its own web fetches

pass: true
