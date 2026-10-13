# Degree-diameter graphs: seven cells of the Comellas table

**Claim (exact scope), as of 2026-10-10.** Each of the seven edge lists in `graphs/` is a simple undirected graph with
the maximum degree Δ and diameter at most D stated below, on more vertices than the entry of the cell (Δ,D) in
Francesc Comellas' *Table of the largest known (Δ,D)-graphs*
(https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), version
`Last-Modified: Sat, 10 Oct 2026 10:26:18 GMT`, fetched 2026-10-10T19:22:57Z with one plain curl GET (sha256 of the
page `5482007a83c3ec57cfa03a9df9af0fa98336fd7c5f7509c49ea1cf202b8bfea3`, 46,092 bytes, ETag `"b40c-65d79e532c680"`;
`the-record-we-beat/*2026-10-10T19-22-57Z*`). None of the seven table entries is printed in bold, i.e. none is proven optimal, and
every N below is far below the Moore bound, so these are lower bounds for the cells, nothing more. An earlier
snapshot (version of 7 Oct 2026, fetched 2026-10-08T23:29:28Z, sha256 `142d5d1b…5ec9`) is also kept in `the-record-we-beat/`;
none of the six cells it covers changed between the two versions.

| cell (Δ,D) | our N | table entry 2026-10-10 | margin | Moore bound | file (sha256 of the decompressed edge list) |
|---|---|---|---|---|---|
| (15,4) | **13 365** | 11 780 (R. Rajiv, 30 Sep 2026) | +1 585 (+13.5 %) | 44 326 | `graphs/G_15_4_n13365.edges` `2d36814028c63e32e527fc0f88ac08cbc70be134f8786de4867c58d748dae52f` |
| (15,3) | **1 620** | 1 539 (R. Rajiv, 30 Sep 2026) | +81 (+5.3 %) | 3 166 | `graphs/G_15_3_n1620.edges.txt` `da9faa8c8a875ac789506ca3f91a45db37b3f1f3952b729c88199557caa792ce` |
| (14,4) | **8 424** | 8 303 (M. de Messieres, 3 Oct 2026) | +121 (+1.5 %) | 33 321 | `graphs/G_14_4_n8424.edges.txt` `71ef820b5804f77c626209fbcda3a8bd50c546a5fb70175cbe36a9f98f22f281` |
| (13,4) | **6 630** | 6 615 (D. Yugeswardeenoo, Oct 2026) | +15 (+0.2 %) | 24 506 | `graphs/G_13_4_n6630.edges` `7c44e128901d6dd6b64e0574b90ff8aa21872462338fd267bab466cb268e10a4` |
| (9,4) | **1 700** | \*1 640 (F. Comellas 2024, Cayley graph; the asterisk is the table's Cayley mark) | +60 (+3.7 %) | 5 266 | `graphs/G_9_4_n1700.edges` `d271a1e84aa9539ba47f8d036cd15e4a5a9ccc5a4752d0dacc94a9d35f17eebd` |
| (13,6) | **535 495** | 535 302 (D. Yugeswardeenoo, Oct 2026) | +193 (+0.04 %) | 3 528 890 | `graphs/G_13_6_n535495.edges.gz` `4ed4fc62000b3cbc6c23b08d9db4af383aa28b01e69fc802b5b1bbdbab170e94` |
| (15,6) | **1 424 896** | 1 424 474 (D. Yugeswardeenoo, Oct 2026) | +422 (+0.03 %) | 8 687 926 | `graphs/G_15_6_n1424896.edges.gz` `554149b59ffe151197dff3ae48ae315596d9c618924d25db4775b1315ab47a75` |

The table entries, their raw text (an asterisk marks a Cayley graph), the holders as given on the description pages
and the HTTP headers of the fetch are in `the-record-we-beat/live_cells_2026-10-10T19-22-57Z.json` and the `the-record-we-beat/*.http-headers.txt`
files (the `Server:` banner line was dropped from the saved headers); `the-record-we-beat/parse_comellas_table.py` is the parser we
used (126 cells). At the earlier snapshot, Wikipedia's *Table of the largest known graphs of a given diameter and maximal degree*
(raw wikitext fetched 2026-10-08T23:30:31Z) agreed with the Comellas table on those six cells. **Re-fetch the table
before relying on any margin**: the D=6 cells and (13,4) were updated by their current holder in Oct 2026, (14,4) on
3 Oct 2026, the page still carries an "Updating" banner, and the (13,4) margin is only +15.

**Not claimed.** Our agents also built graphs for (12,3) on 810 vertices and (11,4) on 3 444 vertices; the 7 Oct 2026
table update lists exactly those orders (independently, by D. Yugeswardeenoo), so they are ties and are not included.
A (14,3) graph on 1 107 vertices was overtaken by the live 1 116 and is not included either. Nothing is claimed for
the Cayley-graph or bipartite special tables.

**Status.** These graphs have been produced by agents (see `READ_BEFORE_CITING.md` at the repository root) and checked only
internally. As of this release they have **not** been submitted to F. Comellas, whose page is the table of record
(the page asks for new results by email), and no outside expert has examined them. The page states that it is
"AI-free"; how AI-produced graphs should be credited there is for the maintainer to decide. The (9,4) entry would
replace a Cayley graph of the maintainer's own by a non-Cayley graph in the general table; the Cayley-graph table is
unaffected.

## File format

Plain text, one undirected edge `u v` per line, 0-based integer labels `0..N-1`, each edge listed once, no header.
The two D=6 files are gzip-compressed (`gzip -d` them first; the sha256 values above are of the decompressed text).

## How the graphs were checked, and how to check them yourself

Diameter is established by **exhaustive all-pairs breadth-first search**: from every vertex, grow the ball of
radius D and count the vertices not reached. Simplicity (no loops, no repeated edges, labels 0..N-1 all used) and the
degree bound are checked at the same time. Before release each graph passed at least three separately written
all-pairs checkers (the author's and those of two independent reviewers; the (13,6) graph also a fourth). For this release two more checkers were written from the definition and run on the shipped files:

- `verify-it-yourself/ddcheck.c` — C, pthreads, bitset ball growth (1024 sources per batch). `cc -O3 -o ddcheck ddcheck.c -lpthread`,
  then `./ddcheck GRAPH DELTA D THREADS`. Prints N, edges, loops, duplicates, degree histogram, the number of ordered
  pairs within distance r for r = 0..D and the number of ordered pairs at distance > D; last line VALID/INVALID.
- `verify-it-yourself/ddcheck.py` — python3 + numpy, same method, for the five small graphs (a few seconds each).

Results on the shipped files are in `verify-it-yourself/RECEIPTS.md`: both release checkers report VALID on the
five small graphs, and the C checker, run to completion on the two large graphs, reports 0 ordered pairs at distance
> 6 and VALID for both. Negative controls: running either checker with D−1 instead of D reports far pairs > 0 and
INVALID for every graph (all seven graphs have diameter exactly D); the (13,4) near-miss parent in
`how-we-built-it/13_4/` is INVALID with 4 far ordered pairs. `verify-it-yourself/run_checks.sh` runs everything (`BIG=1` includes the
two large graphs). The (13,4) file starts with one `#` comment line, which both checkers skip.

## What the graphs are (construction and credit)

All seven were found by our agents between 5 and 8 Oct 2026. For six of them the rebuild scripts and parameters in
`how-we-built-it/` regenerate each edge list byte for byte (see `RUN_IT_YOURSELF.md`; the five rebuilds other than (15,6) were
rerun on 2026-10-09 and matched); the (13,4) graph comes from a local search and `how-we-built-it/13_4/` gives its
near-miss parent, the 5-edge switch that closes it and the insertion/annealing code of the whole chain (its final step
reproduces the shipped file byte for byte). The code that searched for the construction parameters of the other cells
is in `how-we-built-it/<cell>/search/`; `how-we-built-it/README.md` is the index, and `HOW_WE_FOUND_IT.md` tells the
story. The all-pairs check is the proof, the descriptions below only explain where the graphs come
from.

**(15,4), N = 13 365 — polarity quotient of a bipartite route-chart lift.**
Let Γ = Z_11 ⋊ Z_30 with (i,j)(i',j') = (i + 2^j i', j + j'), and let B be the route-chart lift over the Cayley graph
Cay(Γ, {a, a⁻¹, b, b⁻¹, c}), a = (0,3), b = (1,5), c = (6,15), with fibre F_3^4 and charts (h,x) ~ (h t, A_t x + λ b_t),
λ ∈ F_3 (the matrices A_t, b_t are the 381-byte state `how-we-built-it/15_4/state_Z11x2Z30.json`). B is a bipartite
(15,5) graph on 26 730 vertices. Left multiplication by the involution c0 = (0,15), which has odd Z_30 coordinate,
is an automorphism that swaps the two colour classes, i.e. a polarity; the quotient G = B/ρ has 13 365 vertices,
maximum degree 15 (405 absolute vertices have degree 14) and diameter ≤ 4 because
d_G([u],[w]) = min(d_B(u,w), d_B(u,ρw)) and the two distances have opposite parity. *Credits:* polarity quotients of
bipartite graphs are Charles Delorme's construction (C. Delorme, *Grands graphes de degré et diamètre donnés*,
European J. Combin. 6 (1985)); the route-chart lift is Ryosuke Mizuno's method (arXiv:2606.15860,
github.com/rmizuno42/ddp). The table entry it exceeds is Rishabh Rajiv's (Zenodo 10.5281/zenodo.23052995).

**(13,4), N = 6 630 — a local-search descendant of Rajiv's Q9(T4)++.**
Starting from Rishabh Rajiv's (13,4) graph Q9(T4)++ on 6 611 vertices, our agents repeatedly inserted a vertex joined
to vertices with free degree and annealed over 2-switches and edge rewires to remove the pairs at distance 5, reaching
a valid 6 629-vertex graph; one more insertion gave a 6 630-vertex near-miss with exactly 2 far pairs, and a
low-temperature resume of the annealer closed it with a 5-edge switch (`how-we-built-it/13_4/`: the near-miss, the switch,
`apply_diff.py`, which rebuilds the edge set, and in `search/` the annealing code with the seeds of every step). Degrees {11: 4, 12: 10, 13: 6 616}. The diameter rests on the
exhaustive BFS alone. *Credits:* the seed graph and its compound/surgery construction are Rishabh Rajiv's
(Zenodo 10.5281/zenodo.23052995, CC BY 4.0); the compound family goes back to Gómez and Fiol. The entry exceeded is
Dharunish Yugeswardeenoo's 6 615 (Oct 2026), itself above Rajiv's 6 611.

**(15,3), N = 1 620 — route-chart lift over F_3^3 of a 60-vertex controller.**
Vertices (u, x) with u a vertex of a 5-regular controller graph C on 60 vertices and x ∈ F_3^3; for every controller
edge {a,b}, every x and every λ ∈ F_3, (a,x) ~ (b, T_ab x + λ w_ab). The lift is 15-regular on 27·60 = 1 620
vertices. The controller (`how-we-built-it/15_3/controller_own_k5_n60.adj`) is a Z_15-voltage lift of a 4-vertex base
found by our agents; an algebraic certificate (3 300 rank-3 walks and 300 complete pencils, `check_route_certificate.py`)
shows the diameter is ≤ 3 independently of the BFS. *Credits:* this is exactly Mizuno's route-chart construction
(arXiv:2606.15860), which gives the (16,3) entry 1 920 = 64·30 and whose public (15,3) attempt reached 1 458 = 27·54;
the difference here is a larger controller. The entry exceeded is Rajiv's 1 539.

**(14,4), N = 8 424 — affine frame lift of Bhakar's (4,4) graph.**
Vertices (u, p) with u a vertex of Nishant Bhakar's (4,4) graph on 104 vertices (entry "Bhakar_104", 27 Aug 2026)
and p ∈ F_3^4; for every arc u→w of an orientation of the controller and every λ ∈ F_3, (u,p) ~ (w, A_uw p + c_uw +
λ b_uw) (12 edges per vertex), plus one in-fibre edge (u,p) ~ (u, p + t_u) (degree 14). N = 81·104. The parameters
(including Bhakar's controller) are `how-we-built-it/14_4/G_14_4_n8424.params.json`. *Credits:* Nishant Bhakar for the
controller; the affine-lift family is the one used in Rajiv's and Mizuno's recent entries. The entry exceeded is
Michel de Messieres' 8 303 (Zenodo concept 10.5281/zenodo.23113462), itself a 15-vertex extension of Rajiv's 8 288.

**(9,4), N = 1 700 — Z_2 lift of the W(7) generalized-quadrangle incidence graph with spread twins.**
Take the incidence graph of the symplectic generalized quadrangle W(7) (400 points, 400 lines, 8 points per line, 8
lines per point). Double every vertex (fibre Z_2) and lift each incidence with a Z_2 voltage chosen by local search
(`how-we-built-it/9_4/voltage_q7_Z2.txt`): 800 point copies and 800 line copies, each line copy joined to its twin copy
(degree 9), each point copy with one free slot. Take a spread (50 lines partitioning the points,
`how-we-built-it/9_4/spread_q7.txt`) and for each spread line add two "twin" vertices, each adjacent to 8 point copies
of that line (one per point, parities chosen by the voltage) and to each other: 100 more vertices of degree 9.
N = 800 + 800 + 100. The pure-python `rebuild_1700.py` re-verifies the W(7) geometry and rebuilds the edge list.
*Credits:* the "delete a spread matching and attach new vertices" idea is shared with Rajiv's surgery
(Zenodo 10.5281/zenodo.23052995); the W(q) incidence graphs are the classical bipartite (q+1, 4) graphs. The entry
exceeded, *1 640, is a Cayley graph of F. Comellas (2024); the Cayley-graph table is not affected.

**(13,6), N = 535 495 — Rajiv's H_9(T_4) compound with relaxed cut sets, surgery vertices and shortcuts.**
Rajiv's Definition 3 takes four copies of the incidence graph of the generalized hexagon H(9) (P = 66 430 points
and lines each; 2·4·P = 531 440 base vertices), joins them by a tournament of point–line matchings and by point–point
or line–line matchings from which a *cut set* of points S_P and lines S_L is removed, and attaches surgery vertices
to the freed slots. Here S_P has 4 055 points and S_L 4 067 lines (`how-we-built-it/13_6/SP_relaxed_t4055.json`,
`SL_relaxed_t4055.json`), *relaxed*: up to two cut points per line and two cut lines per point, so Rajiv's Lemma 5
does not apply and the diameter is established only by the exhaustive BFS. 4 055 new vertices each take one point
and one line of every block (8 edges) and are joined by a random 5-regular graph (degree 13); 2 643 shortcut edges
between base vertices with free degree close the remaining far pairs. The 46 740 edges that are not in the bare
compound are the certificate `how-we-built-it/13_6/G_13_6_n535495.extra_vs_compound.txt`; `rebuild13.py` rebuilds the
graph from Rajiv's published H_9(T_4) file plus this certificate. *Credits:* the compound, its lemmas and the surgery
are Rishabh Rajiv's (Zenodo 10.5281/zenodo.23052995, CC BY 4.0); the generalized-hexagon compounds go back to
Gómez and Fiol. The entry exceeded is Yugeswardeenoo's 535 302 (its description was not yet public at fetch time; the
former entry was Rajiv's 534 234).

**(15,6), N = 1 424 896 — Rajiv's H_11(T_4) compound with larger cut sets.**
The same compound with q = 11 (P = 177 156; base 1 417 248 vertices), cut at larger Lemma-5 cut sets found by iterated
local search: 7 679 pairwise non-collinear points and 7 648 pairwise non-concurrent lines (Rajiv used 7 369 and
7 226; `how-we-built-it/15_6/H11_points_s5.json`, `H11_lines_s1.json`). 7 648 new vertices (Rajiv: 7 224), each adjacent
to one point and one line of every block and to at most 7 other new vertices (degree ≤ 15), plus 9 shortcut edges
(`shortcuts_9.txt`). Our own novelty review calls this incremental: the base graph, the lemmas and the
capacity rule are Rajiv's and only a parameter was pushed. *Credits:* Rishabh Rajiv (Zenodo 10.5281/zenodo.23052995).
The entry exceeded is Yugeswardeenoo's 1 424 474 (former entry Rajiv's 1 424 472).

## Limitations

- Lower bounds only; nothing here is a proof of optimality, and the two D=6 margins (+0.04 %, +0.03 %) and the
  (13,4) margin (+15) are small enough to be overtaken by the current holders at any time.
- All verification so far is internal: the checkers shipped here and the earlier ones were written by the same
  team of agents on the same machine. No outside expert has examined any graph yet.
- For (13,6) and (13,4) the diameter rests solely on exhaustive BFS (for (13,6) the relaxed cut sets void Rajiv's
  Lemma 5 by design; (13,4) comes from local search). For the other five graphs the BFS is backed by a structural argument (polarity parity, route-chart certificate,
  Lemma 5 hypotheses re-checked), but the BFS is what we ask you to run.
- Not submitted to the table maintainer at release time; the recorded table state is the only comparison made.
- The constructions reuse published ideas; the contribution is the search for parameters (controllers, charts,
  voltages, cut sets) and the resulting explicit graphs.

## Files

```
README.md, RUN_IT_YOURSELF.md, INDEX.csv, HOW_WE_FOUND_IT.md
graphs/              the seven edge lists (two gzip-compressed)
verify-it-yourself/  ddcheck.c, ddcheck.py, run_checks.sh; RECEIPTS.md: output of the release checkers on the shipped files
the-record-we-beat/  HTTP headers and sha256 of the table page (2026-10-08 and 2026-10-10 fetches) and three description
                     pages (2026-10-08), parsed values of our cells (live_cells_*.json), the parser
how-we-built-it/     per cell: construction parameters / certificates and the rebuild scripts; search/ subfolders: the code
                     that found the parameters (and for (13,4) the whole local-search chain); README.md: index; SMOKE.md
```

## References

- F. Comellas, *Table of the largest known (Δ,D)-graphs*, https://web.mat.upc.edu/francesc.comellas/delta-d/ (created 1995 with C. Delorme).
- R. Rajiv, dataset *compound graphs of generalized hexagons*, Zenodo, doi:10.5281/zenodo.23052995 (30 Sep 2026), CC BY 4.0.
- R. Mizuno, arXiv:2606.15860 (2026); code github.com/rmizuno42/ddp.
- C. Delorme, *Grands graphes de degré et diamètre donnés*, European J. Combin. 6 (1985).
- J. Gómez, M. A. Fiol, compound graphs from generalized polygons (the Q_q(T_k) and H_q(T_k) families cited on the table's description pages).
- N. Bhakar, (4,4) graph on 104 vertices, table entry of 27 Aug 2026 (desc_g4.html).
- M. de Messieres, degree-diameter graphs, Zenodo concept doi:10.5281/zenodo.23113462 (Oct 2026).
- S. E. Payne, J. A. Thas, *Finite Generalized Quadrangles* (the quadrangle W(q)).
