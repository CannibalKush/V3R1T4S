# Literature record for g(8,4)

There is no live table for this quantity. The author searched OEIS, the arXiv API, the Polymath wiki and the hypergraph Turán literature on 2026-10-15 (one honest GET per page, User-Agent naming V3R1T4S, no retries). No page is copied here.

| Source | What it says about this value |
|---|---|
| OEIS search by the r=3 column 10,12,12,14,16,16,20, by the r=4 column 15,24,27,31 and by the keywords sunflower, delta-system | no matching sequence; A332077 and A236397 tabulate unrestricted-ground-set values only; the r=4 column matched only unrelated sequences (A114436, A163077, A352457) |
| arXiv export API, five queries on sunflower-free uniform families and small exact values | only arXiv:2609.06175 (Sep 2026) computes small cases, all on an unrestricted ground set; no fixed-n value |
| Polymath10 wiki table | unrestricted ground set only (f(3,3) = 20 is the n-free value; g(12,3) = 20 is therefore known and not claimed) |
| Hypergraph Turan literature (complement view) | the complements are 5-sets (g(8,3)) or 4-sets (g(8,4)); neither is a standard named Turan problem; nothing found |
| V3R1T4S TROPHY_CASE.md and open pull requests | no sunflower claim |


## Known values excluded by this search (not claimed)

g(n, n-2) = floor(n^2/4) by Mantel's theorem (complements are 2-sets; three with pairwise equal unions form a triangle). g(n, n-3) equals the Turán number of the 3-graph with three edges on four vertices, tabulated by K. Markström (http://abel.math.umu.se/~klasm/Data/hypergraphs/turan3.html, fetched 2026-10-15T15:24:53Z, HTTP 200, sha256 abc2fd8d0142a7c993eaf5a635eb1f9c95035d48ed4904d1f9141ba70538b26f): n = 6..12 give 10, 15, 22, 32, 44, 60, 80. g(12,3) = 20 is Abbott and Gardner's f(3,3) = 20 with the Erdős-Rado witness on 12 points.

## The author's literature scout report (orchestrator's scout, 2026-10-15)

# Novelty scout: twenty-two exact values of g(n,r)

Scope: the claim in `candidates/exact_small_values/REPORT.md` (sections 1 and 4) and `INDEX.md`.
g(n,r) = maximum size of an r-uniform family on [n] with no three distinct members having pairwise
equal intersections (three pairwise disjoint members count). Scout run 2026-10-15, 25 plain GETs
(all HTTP 200), pages saved under `ws/`. Everything read is treated as data.

## Two exact reformulations used below (proved here, elementary)

Complementation: for distinct r-sets A, B, C, A∩B = A∩C = B∩C iff A'∪B' = A'∪C' = B'∪C' for the
(n-r)-set complements. Write s = n - r.

- s = 2. Three distinct pairs have equal pairwise unions only when the union has 3 points (a triangle);
  a 4-point union would force the third pair to equal one of the others. So **g(n, n-2) = ex(n, K3) =
  floor(n^2/4)** (Mantel). Values 12, 16, 20, 25 at n = 7..10 match the claim.
- s = 3. A 5-point union is impossible (the third triple would have to be the 4-set A△B) and so is a
  6-point union; a 4-point union means three triples inside one 4-set. So **g(n, n-3) = ex(n, K4^-)**,
  the Turán number of 3-graphs with no three edges on four vertices. Claimed: ex(6..10, K4^-) =
  10, 15, 22, 32, 44 (from g(6,3), g(7,4), g(8,5), g(9,6), g(10,7)).
- s = 4. Unions of 5 points (three 4-sets inside a 5-set) and of 6 points (the configuration
  {1234, 1256, 3456}) are both possible; 7 and 8 are not. So g(n, n-4) = ex^(4)(n, {3 edges on 5
  vertices, {1234,1256,3456}}), not a standard named Turán problem. Claimed sequence n = 7..12:
  12, 24, 42, 70, 110, 165 (from g(7,3), g(8,4), g(9,5), g(10,6), g(11,7), g(12,8)).

The Polymath wiki (fetch 18) names the quantity itself: "Let f(k,r;m,n) denote the largest cardinality
of a family of k-sets from {1,2,…,n} such that the link of every set A of size at most m-1 does not
contain r pairwise disjoint sets. Thus f(k,r) = f(k,r;k,n) for n large enough." So g(n,r) = f(r,3;r,n)
in that notation; the page tabulates no values of it for fixed small n.

## Verdict table

| (n,r) | claimed g | status | source and evidence | reformulation exact? |
|---|---|---|---|---|
| (6,3) | 10 | LIKELY PUBLISHED | Elementary: on 6 points no 3 disjoint triples and no 1-point-core sunflower fit, so the only obstruction is a pair in 3 triples; pair degree <= 2 gives <= 2·15/3 = 10. The 10-triple witness on points 1..6 is printed in OEIS A332077 file a332077.txt (fetch 6, first ten lines). Also = ex(6, K4^-) = 10, attained by the 6-vertex 10-edge 3-graph in the Frankl-Füredi K4^- construction (MPS open-problems note, fetch 25: "partitioning [n] into six parts, taking certain 10 complete 3-partite 3-graphs"). | yes |
| (7,3) | 12 | NOT FOUND | s = 4 sequence; no source | - |
| (7,4) | 15 | NOT FOUND | = ex(7, K4^-); no small-n table of ex(n, K4^-) reached (see caveat) | yes (s = 3) |
| (7,5) | 12 | LIKELY PUBLISHED | Mantel: floor(49/4) = 12 | yes (s = 2) |
| (8,3) | 12 | NOT FOUND | - | - |
| (8,4) | 24 | NOT FOUND | s = 4 sequence; OEIS search 24,42,70,110,165 returned nothing (fetch 4) | - |
| (8,5) | 22 | NOT FOUND | = ex(8, K4^-) | yes (s = 3) |
| (8,6) | 16 | LIKELY PUBLISHED | Mantel: floor(64/4) = 16 | yes (s = 2) |
| (9,3) | 14 | NOT FOUND | - | - |
| (9,4) | 27 | NOT FOUND | Related only: arXiv 2609.06175 (Axante et al., Sep 2026, fetches 19-20) proves "the maximum size of an intersecting 4-uniform family containing no sunflower with three petals is 27" (ψ(4,3,2) = 27, any ground set). That neither bounds g(9,4) (families on [9] need not be intersecting) nor places the 27-family on 9 points in what was read. | no |
| (9,5) | 42 | NOT FOUND | s = 4 sequence | - |
| (9,6) | 32 | NOT FOUND | = ex(9, K4^-) | yes (s = 3) |
| (9,7) | 20 | LIKELY PUBLISHED | Mantel: floor(81/4) = 20 | yes (s = 2) |
| (10,3) | 16 | NOT FOUND | - | - |
| (10,4) | 31 | NOT FOUND | - | - |
| (10,6) | 70 | NOT FOUND | s = 4 sequence | - |
| (10,7) | 44 | NOT FOUND | = ex(10, K4^-); the REPORT itself flags this as "probably a known value"; not confirmed | yes (s = 3) |
| (10,8) | 25 | LIKELY PUBLISHED | Mantel: floor(100/4) = 25 | yes (s = 2) |
| (11,3) | 16 | NOT FOUND | - | - |
| (11,7) | 110 | NOT FOUND | s = 4 sequence | - |
| (12,3) | 20 | LIKELY PUBLISHED (immediate) | Upper bound: f(3,3) = 20 for 3-uniform families on any ground set. arXiv 2609.06175 p. 22: "The following exact value is due to Abbott and Gardner [2]: f(3,3) = 20." Polymath wiki small-values table (rows r = petals, columns k = 2,3,4,...), row r=3 reads "3 6 20 54- 160- 600-" (dash = lower bound only, so f(3,3) = 20 is exact). Lower bound on exactly 12 points: OEIS A332077 file a332077.txt, "Example for Sun(3,3)=21, a family of 20 sets with no 3-flowers ... (Found by Erdős and Rado)", whose 20 triples use points 1..12 (two copies of the 10-triple 6-point family). | yes (bound holds for every n; witness has n = 12) |
| (12,8) | 165 | NOT FOUND | s = 4 sequence | - |

Bound g(11,4) <= 38: NOT FOUND (no source states it; the published f(3,3)-type tables do not
address fixed n).

Caveat on the five s = 3 values (10, 15, 22, 32, 44 = ex(n, K4^-), n = 6..10): K4^- is one of the most
studied hypergraph Turán problems, and flag-algebra and computer-search papers (Razborov, Baber-Talbot,
Markström-Talbot, Falgas-Ravry-Vaughan) routinely compute ex(n, F) for small n. None of the pages
reached within the 25-fetch budget prints those numbers: the OEIS search for 10,15,22,32,44 (fetch 3)
matched only A073470 (a partition trisection, coincidence); Shi 2016 (fetch 23) and Mubayi-Pikhurko-
Sudakov (fetch 25) give only densities (2/7 <= π(K4^-) <= 0.2871). A panel should treat
(7,4), (8,5), (9,6), (10,7) as at risk until Markström's small Turán data or Baber's thesis is checked.

## OEIS results (all fetches with fmt=json)

| query | result |
|---|---|
| 10,12,12,14,16,16,20 (r = 3 column, n = 6..12) | no results |
| 15,24,27,31 (r = 4 column) | A114436 (indices of 5-almost-prime triangular numbers), A163077 (swinging-factorial primes), A352457 (Lyndon symmetric functions): all coincidences |
| 10,15,22,32,44 (s = 3, ex(n, K4^-)) | A073470 "Trisection of A007294": 1,2,4,6,10,15,22,32,44,60,...: coincidence |
| 24,42,70,110,165 (s = 4) | no results |
| sunflower | A236397 "Weight of the largest-weight sunflower-free set of width n" 1,2,4,8,20,40,96,224 (cap-set style, not uniform on [n]); A332077 "Square array of sunflower numbers Sun(m,n) = minimal number of distinct sets of cardinality <= m such that there is a sunflower with at least n sets among them": data 1,2,1,3,2,1,4,7,2,1,5,11,21,2,1,6,21, i.e. Sun(3,3) = 21, f(3,3) = 20; A266696, A399802 unrelated |
| "delta-system" OR "delta system" | A266696, A332077 only |
| "pairwise intersections" sets equal | A326854, A327061, A332077, A076336, A200976: none tabulate g(n,r) |
| Turan hypergraph triples; Turan 3-uniform | no results |

No OEIS sequence holds any column, row or complement column of the claimed table.

## arXiv (5 API queries: fetches 8-12)

- Fetch 8 (sunflower AND exact): 2511.17142 Kupavskii-Noskov (Duke-Erdős problem, large n), 2410.23611
  focal-free hypergraphs; no small-n tables.
- Fetch 9 (Delta-system): 2508.20132 Kupavskii "Delta-system method: a survey" (asymptotic method),
  2203.13370 weak Delta-systems, 2504.15264 Janzer-Jin-Sudakov-Wu; no small-n tables in abstracts.
- Fetch 10 (sunflower AND SAT/computer/computational): 2609.06175 Axante-Budala-Chitic-Dumitru-Nacu,
  "Sunflower-Free Uniform Families: Recursive Constructions and Explicit Bounds" (2026-09-05), the only
  computer-assisted small-case paper found. Its Table 1 ("Published comparisons and bounds proved in
  this paper") covers f(3,4): 39..49, f(3,5) <= 146, f(3,6): 153..255, f(3,7): 259..474,
  f(4,3): 54..83, all with an unrestricted ground set. It also proves ψ(4,3,2) = 27 and
  Proposition 6.1(ii): an intersecting 3-sunflower-free family of 10 triples "has support at most
  6 points" (SAT plus drat-trim). It gives no fixed-n values g(n,r). Abstract and PDF fetched (19, 20).
- Fetch 11 (Szemeredi AND sunflower): zero entries (arXiv spells it with accents and TeX).
- Fetch 12 (Turán, K4^- or three edges, small n/exact/computer): one hit, 2609.27495 (tetrahedron
  density); nothing on small ex(n, K4^-).

## Classical sources (task item 4)

- Polymath10 wiki (archived copy, fetch 18): defines f(k,r;m,n) (our g with m = k) but tabulates only
  f(k,r) over an unrestricted ground set, "taken from Abbott-Exoo". Not fetched within budget: the Gowers
  and Kalai blog posts, Kostochka's survey "Extremal problems on Δ-systems", Erdős-Szemerédi 1978,
  Deza 1974, Frankl-Füredi "Forbidding just one intersection", Naslund-Sawin, Ellenberg-Gijswijt,
  Abbott-Hanson-Sauer 1972, Abbott-Exoo 1992. From general knowledge (UNVERIFIED this run): these give
  asymptotic or unrestricted-ground-set results (Deza: a large family with one intersection size is a
  sunflower; Erdős-Szemerédi and Naslund-Sawin: exponential bounds on non-uniform sunflower-free
  families on [n]), not fixed small-n uniform values. Abbott-Exoo 1992 and Abbott-Hanson 1974 are the
  likeliest places for fixed-n 3-uniform data and were not readable here.

## V3R1T4S repo (fetches 13-14)

TROPHY_CASE.md: no match for sunflower, Delta-system or Δ-system. Open PRs: 66, none mentioning
sunflower, delta-system, Erdős-Rado or g(n,r) in title or body.

## Fetch log

| # | saved as | URL | UTC | HTTP | sha256 |
|---|---|---|---|---|---|
| 1 | `ws/01_oeis_r3col.json` | https://oeis.org/search?q=10%2C12%2C12%2C14%2C16%2C16%2C20&fmt=json | 2026-10-15T15:12:26Z | 200 | `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b` |
| 2 | `ws/02_oeis_r4col.json` | https://oeis.org/search?q=15%2C24%2C27%2C31&fmt=json | 2026-10-15T15:12:26Z | 200 | `c2478704bfaaca49398ef63c2277c65d8c268335907f7d269cb7914c7974af87` |
| 3 | `ws/03_oeis_nminus3.json` | https://oeis.org/search?q=10%2C15%2C22%2C32%2C44&fmt=json | 2026-10-15T15:12:27Z | 200 | `06b35c694db84381fb0618fe044b487d152bec82e8f6ebe929800f2381c35580` |
| 4 | `ws/04_oeis_nminus4.json` | https://oeis.org/search?q=24%2C42%2C70%2C110%2C165&fmt=json | 2026-10-15T15:12:27Z | 200 | `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b` |
| 5 | `ws/05_oeis_sunflower.json` | https://oeis.org/search?q=sunflower&fmt=json | 2026-10-15T15:12:27Z | 200 | `77e3d20ee32853a3d9d8e5ce3b59ecbcc842ac19ce45cae3d0d0ea2dcf2b0a93` |
| 6 | `ws/06_oeis_a332077_example.txt` | https://oeis.org/A332077/a332077.txt | 2026-10-15T15:12:58Z | 200 | `9604107655e9d9552f0c5770130de417c89e583e33b2defa21e1d7446e8c537f` |
| 7 | `ws/07_oeis_turan_kw.json` | https://oeis.org/search?q=Turan+hypergraph+triples&fmt=json | 2026-10-15T15:12:58Z | 200 | `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b` |
| 8 | `ws/08_arxiv_sunflower_exact.xml` | http://export.arxiv.org/api/query?search_query=all:sunflower+AND+all:exact&max_results=30 | 2026-10-15T15:12:59Z | 200 | `270f27d2ca951aa669c41ec3de370d07edf7d15b9eccfca717632f59f6094dc7` |
| 9 | `ws/09_arxiv_deltasystem_small.xml` | http://export.arxiv.org/api/query?search_query=all:%22Delta-systems%22+OR+all:%22Delta-system%22&max_results=30 | 2026-10-15T15:12:59Z | 200 | `0515971809b86353e790d9464ccdaed1808e6cb21870a4f7667c3436cd3c6391` |
| 10 | `ws/10_arxiv_sunflower_SAT.xml` | http://export.arxiv.org/api/query?search_query=all:sunflower+AND+(all:SAT+OR+all:computer+OR+all:computational)&max_results=30 | 2026-10-15T15:13:00Z | 200 | `f33b415b666b930853a7bfc87007c01d7e9e2a225bb1c26d91b2b85edad994be` |
| 11 | `ws/11_arxiv_ES_sunflower.xml` | http://export.arxiv.org/api/query?search_query=all:Szemeredi+AND+all:sunflower&max_results=30 | 2026-10-15T15:13:29Z | 200 | `2f1b443ee649292a3705a461846713f9f373b6b91a4d13e85e816233368d7797` |
| 12 | `ws/12_arxiv_turan_K4minus.xml` | http://export.arxiv.org/api/query?search_query=all:Turan+AND+(all:%22K_4%5E-%22+OR+all:%22three+edges%22)+AND+(all:%22small+n%22+OR+all:exact+OR+all:computer)&max_results=40 | 2026-10-15T15:13:29Z | 200 | `95b1615a58fa046c5b3512336c4e453964cfd3ab0603c4485b4625a912c2716a` |
| 13 | `ws/13_v3r1t4s_trophy.md` | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T15:13:30Z | 200 | `b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412` |
| 14 | `ws/14_v3r1t4s_pulls.json` | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T15:13:30Z | 200 | `48c623ce3a79aaba234d4ce2137c013a3aa8385426a61d6e53054d64384ee511` |
| 15 | `ws/15_oeis_deltasystem.json` | https://oeis.org/search?q=%22delta-system%22+OR+%22delta+system%22&fmt=json | 2026-10-15T15:13:59Z | 200 | `e9ae1d6ef9427d19e16d3632d4cbca335b3ed27793bf39dd272b8d906d6da699` |
| 16 | `ws/16_oeis_pairwise_equal_intersections.json` | https://oeis.org/search?q=%22pairwise+intersections%22+sets+equal&fmt=json | 2026-10-15T15:14:00Z | 200 | `5e737eb063ab49d92d3c5a02dda4f06ab7e29d487c8cfe9a1a873249c17f75ab` |
| 17 | `ws/17_oeis_turan_3graph.json` | https://oeis.org/search?q=Turan+3-uniform&fmt=json | 2026-10-15T15:14:00Z | 200 | `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b` |
| 18 | `ws/18_polymath_wiki_sunflower_archive.html` | https://web.archive.org/web/20220705073934/https://asone.ai/polymath/index.php?title=The_Erdos-Rado_sunflower_lemma | 2026-10-15T15:14:17Z | 200 | `6e226121bed1fe64f65af29e243b33ffc77b16fa37f8b2311bdfff7a38533dd8` |
| 19 | `ws/19_arxiv_abs_2609.06175.html` | https://arxiv.org/abs/2609.06175 | 2026-10-15T15:14:17Z | 200 | `a7b82aac7c91bd0b086e73252a4f022e1e504e4d7566e1b5f707e0bdc8085fb8` |
| 20 | `ws/20_arxiv_pdf_2609.06175.pdf` | https://arxiv.org/pdf/2609.06175 | 2026-10-15T15:14:17Z | 200 | `8ca521d68179497b496c1177e47b5922142fdc91e45c305fe6dd8020867b1976` |
| 21 | `ws/21_ddg_K4minus_small.html` | https://html.duckduckgo.com/html/?q=%22K_4%5E-%22+Turan+number+small+n+exact+values+3-graph | 2026-10-15T15:14:18Z | 200 | `87f8ee131a92a3a560ed706bf004191cc24df0b01aaf1d7a6875ca7954491f02` |
| 22 | `ws/22_ddg_markstrom_small_turan.html` | https://html.duckduckgo.com/html/?q=Markstr%C3%B6m+small+Tur%C3%A1n+numbers+3-graphs+K4-+table+exact+values+n%3D7+n%3D8 | 2026-10-15T15:15:22Z | 200 | `642a51be0c4549cc185915829b631f3894d53ead3ac5d723a6d69b2e52cf9b29` |
| 23 | `ws/23_tsinghua_turan_small_triple_graphs.pdf` | https://archive.ymsc.tsinghua.edu.cn/pacm_download/138/4637-YEUJC2016Turan.pdf | 2026-10-15T15:15:33Z | 200 | `b2e2ad0fb12dc6fa260a6005f86957e38514dbec3401609283d30cc34ef7bec2` |
| 24 | `ws/24_ddg_K4minus_exact_small_n.html` | https://html.duckduckgo.com/html/?q=%22any+four+points+span+at+most+two%22+3-graph+maximum+edges+small+n+computer+search+exact | 2026-10-15T15:15:54Z | 200 | `1e9bb6cd7148101f94313b036d9350aedf850165641387765b6343e0541f4028` |
| 25 | `ws/25_mubayi_pikhurko_sudakov_open_questions.pdf` | https://pikhurko.github.io/E/MubayiPikhurkoSudakov11aim.pdf | 2026-10-15T15:16:03Z | 200 | `e176c3ba4d3d68147e2719625143117a3f05b03e41bc3656cbdcf906cd75e1b3` |

User-Agent on every fetch: `V3R1T4S-research (honest client; curl)`. No retries; no 401/403/429/503 seen.
Fetches 21, 22 and 24 were DuckDuckGo HTML searches used to locate small Turán tables (none found).

## Result

LIKELY PUBLISHED (6): g(6,3)=10 (elementary + published witness), g(7,5)=12, g(8,6)=16, g(9,7)=20,
g(10,8)=25 (all Mantel via exact complementation), g(12,3)=20 (f(3,3)=20 plus the published 12-point
Erdős-Rado family). At risk but not found (4): g(7,4)=15, g(8,5)=22, g(9,6)=32, g(10,7)=44 (equal to
ex(n, K4^-), n = 7..10).

novel_values: 16 of 22 — g(7,3)=12, g(7,4)=15, g(8,3)=12, g(8,4)=24, g(8,5)=22, g(9,3)=14, g(9,4)=27, g(9,5)=42, g(9,6)=32, g(10,3)=16, g(10,4)=31, g(10,6)=70, g(10,7)=44, g(11,3)=16, g(11,7)=110, g(12,8)=165


## Orchestrator addendum (2026-10-15 15:25 UTC): Markström's table read
One honest GET of http://abel.math.umu.se/~klasm/Data/hypergraphs/turan3.html (HTTP 200, sha256
abc2fd8d0142a7c993eaf5a635eb1f9c95035d48ed4904d1f9141ba70538b26f, saved in lit/ws3/). Its table for the 3-graph with
three edges on four vertices reads: N 6 to 19 gives ex 10, 15, 22, 32, 44, 60, 80, 101, 126, 156, 190, 230, 276, 322.
By the exact complement reformulation g(n, n-3) = ex(n, that 3-graph), the values g(6,3)=10, g(7,4)=15, g(8,5)=22,
g(9,6)=32, g(10,7)=44 are PUBLISHED (Markström; the counts of extremal hypergraphs 1, 1, 5, 6, 43 are also listed).
Our proofs reproduce them.
Novel after this check, 12 values: g(7,3)=12, g(8,3)=12, g(8,4)=24, g(9,3)=14, g(9,4)=27, g(9,5)=42, g(10,3)=16,
g(10,4)=31, g(10,6)=70, g(11,3)=16, g(11,7)=110, g(12,8)=165. Known, not claimed: g(6,3), g(7,4), g(7,5), g(8,5),
g(8,6), g(9,6), g(9,7), g(10,7), g(10,8), g(12,3).
