# Novelty skeptic: degree-diameter (Delta, D) = (14, 3), claimed N = 1117

context: Claude Code subagent (Opus 5.5), fresh context

## What I read locally

Only the claim folder (CLAIM.md, the two table-record/ files, and the object/ file names) and claim.SHA256SUMS. The sha256 of CLAIM.md, table-record/README.md, table-record/sources_2026-10-14T07-37-19Z.json and both object/ files match claim.SHA256SUMS. I did not open the object files, and I did not check the graph's correctness; that belongs to the other skeptics. The claimed value I tested is N = 1117 (CLAIM.md; file name G_14_3_N1117).

## Primary status sources (one plain curl request each, no retries)

User-Agent `V3R1T4S-research (honest client; curl)`. Each time comes from `date -u` immediately before the request. Saved copies are in novelty_ws/ in the panel folder.

| Source | URL | UTC fetch time | HTTP | sha256 of saved page | Value read for (14, 3) |
|---|---|---|---|---|---|
| Comellas general-graph table | https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html | 2026-10-14T16:14:01Z | 200 | aa4e747b76562bc78a8b2a38946d35a2266ef5352cca59e623c3ea77c8720d35 | `&lowast;  1 116`, so **1116**. Not bold, so not proven optimal. Cell colour #99EF99 is "Dharunish Yugeswardeenoo, soft mint" in the legend. |
| Comellas D = 3 description page | https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g3.html | 2026-10-14T16:14:34Z | 200 | 0edff426ce79be1e8ba42d267ac7f3cf508609968efe15fcbe29ba04d369bf16 | Anchor 143: `Dhar_1116`, "Degree = 14, Diameter = 3; Order =1116; Moore bound= 2563", Dharunish Yugeswardeenoo, October 7, 2026 |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-14T16:14:53Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | **None.** It lists 7 degree-diameter graphs: (15,4), (15,3), (14,4), (9,4), (13,4), (13,6), (15,6). None is (14, 3). |
| V3R1T4S open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-14T16:14:54Z | 200 | a84f49feb658469f9fded0612b36fba64ab42987c4b05c04fe979e64b142446f | **None.** There are 25 open PRs on a single page (no `link` header). None mentions degree-diameter, Comellas, biggest-graphs or (14, 3) in its title, body or branch name. |

Headers on the table page: `Last-Modified: Wed, 14 Oct 2026 13:17:04 GMT`. On the D = 3 page: `Last-Modified: Sat, 10 Oct 2026 19:29:38 GMT`.

Comparison with the claim's own record. The claim recorded the table at 2026-10-14T07:37:19Z with sha256 69e48062…8cd6. The table has changed since then: its hash is now different and it was last modified at 13:17:04 GMT. The (14, 3) cell still reads 1116, so the claim's comparison value has not moved. The D = 3 page hash is identical to the claim's record (0edff426…bf16).

### Latest change to the (14, 3) cell

The D = 3 page gives this history for (14, 3):

| Order | Author | Date |
|---|---|---|
| 979 | Rajiv (Cayley graph) | communicated July 4, 2026 |
| 1032 | Marosi (Cayley graph) | Aug 17, 2026 |
| 1032 and 1053 | Rajiv (Cayley graphs) | Aug 24, 2026 |
| 1088 | Rajiv | Sept 30, 2026 |
| 1094 | de Messieres | Oct 3, 2026 |
| **1116** | **Yugeswardeenoo** | **Oct 7, 2026** |

The latest change was 1094 to 1116 by Dharunish Yugeswardeenoo, dated 7 October 2026: 28 vertices added to Rajiv's 1088-vertex graph. The table legend agrees, listing Yugeswardeenoo's "Oct. 2026" updates including (14,3). The table source also contains an HTML-commented (unrendered) "Latest Updates" block. It lists (14,3) only under July 2026, so it is stale.

## Extra repository checks (same curl rules)

| URL | UTC time | HTTP | sha256 | Finding |
|---|---|---|---|---|
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=closed&per_page=100 | 2026-10-14T16:20:32Z | 200 | 17a2b5aec2964609aee84289147e92e7ef9e13502a314834e39aeb98eba85f40 | 100 closed PRs. The only degree-diameter item is #60, "[claim] degree-diameter-table: (14, 3) N = 1117", closed unmerged at 12:51:10Z. Its body cites object sha256 3fc25411…c8a4 and contributor anonymous-c6d1e0ab. That is this same claim and object, not an independent result. |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=closed&per_page=100&page=2 | 2026-10-14T16:21:04Z | 200 | b9db8b76fa426719590d705558a906f2ca74a6f348af3c01182d5404554f8e1a | 15 closed PRs, none about degree-diameter |
| https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/biggest-graphs/graphs | 2026-10-14T16:20:33Z | 200 | d8115cdb1cd289af59e349d3a1a865e0b4a67cd0b9346d7161dedda6a34d4a0a | 7 graph files. None is (14, 3). |

## Literature search (last 24 months: Oct 2024 to Oct 2026)

All literature reads were made with WebSearch and WebFetch between 2026-10-14T16:15Z and 16:22Z. WebFetch does not expose HTTP status or a page hash, so none is quoted for these reads.

- **arXiv, date-filtered advanced search (submitted 2024-10-01 to 2026-10-14):**
  - Abstract phrase "degree-diameter" and "degree/diameter": 18 results each (the same set).
  - "Moore bound": 13 results.
  - "largest known" graphs diameter: 0 results.
  - A general "degree diameter" listing, newest first, reached back to May 2026.
  - None of these gives a (14, 3) order.
- **arXiv:2608.27253** (Isham, Lakhotia, Monroe, Petrini; 27 Aug 2026; bank-named). I read the full HTML text. Its new diameter-3 graphs are at degrees 18, 19 and 20 (2340, 2470, 2600) and 27 to 30. It has no degree-14 entry.
- **arXiv:2608.03965** (Cames van Batenburg and Korsky; 4 Aug 2026; bank-named). Asymptotic Moore-bound result only, with no explicit (14, 3) order.
- **arXiv:2606.15860** (Mizuno) and its companion repo github.com/rmizuno42/ddp. Results at (12,4), (12,5), (13,5), (14,5), (15,3), (15,5), (16,3), (16,5); none at (14, 3).
- **Other arXiv items in the window** (2606.10954, 2610.04815, 2608.12425, 2608.08997, 2507.18797, 2406.18994v2 of 24 Jan 2026): none gives a (14, 3) order.
- **Zenodo records:**
  - de Messieres 10.5281/zenodo.23176213, v4 of 6 Oct 2026: n(14,3) ≥ 1094.
  - Rajiv 23052995 (30 Sep 2026): lists (14,3) among improved pairs; the D = 3 page gives its order as 1088.
  - Rajiv 22928337 and 23057003: landing pages give no (14, 3) order. The D = 3 page shows Rajiv's best (14, 3) as 1088.
  - The Zenodo search API returned HTTP 400 (Retry-After: 60). I did not retry; I used a zenodo.org-restricted web search instead.
- **Wikipedia,** "Table of the largest known graphs of a given diameter and maximal degree" (as of 14 Oct 2026; last edited 15:17 UTC): (14, 3) = **1116**, credited to Dharunish Yugeswardeenoo.
- **Mendeley Data** d75dzbjd4k: latest version V11 (28 Jan 2026).
- **Combinatorics Wiki** general-graph page: TLS certificate error, not retried. It is a legacy mirror, not the status source.
- **Web searches** for n(14,3), "Dhar_1116", "deg14_diam3", 1117, 1118 or 1120 vertices, and the authors Yugeswardeenoo, Rajiv and de Messieres: no (14, 3) graph with 1117 or more vertices other than this claim.

## Best known before this claim

The best known (14, 3) order is **1116**. The live Comellas table, the D = 3 description page and Wikipedia all agree on it. Nothing in the literature, TROPHY_CASE.md, or open or closed pull requests matches or exceeds 1117, except this claim's own earlier PR #60 (same object).

## Verdict

**1117 > 1116: a strict improvement of +1 vertex, not a tie.** It is below the Moore bound M(14,3) = 2563, and the cell is not boldface (not proven optimal).

Limits:
- The margin is one vertex. The table changes daily (it was edited at 13:17 GMT today), so the claimant must re-fetch it immediately before claiming.
- The credits in PR #60's body date Dhar_1116 to "Sept. 14, 2026". The D = 3 page dates it October 7, 2026. This does not change the verdict.
- Correctness of the graph is outside this skeptic's scope.

novelty: PASS (1117 strictly beats the best known 1116 as of 2026-10-14T16:14:01Z)

pass: true
