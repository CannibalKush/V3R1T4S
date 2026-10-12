# How we found the seven degree-diameter graphs

**The brief.** AI agents were pointed at F. Comellas' table of the largest known (Δ,D)-graphs and asked for a graph
that beats a live, non-optimal entry, checked by exhaustive all-pairs BFS and compared with the table re-fetched just
before any claim. The table was moving daily in Oct 2026 (several groups, some AI-assisted, were updating it). The
brief ranked angles; the first was "slack-cell surgery": take a published record graph that still has free degree,
insert a vertex and repair the diameter by simulated annealing on edges, because pure attachment provably cannot
work. Other suggested angles were Delorme-style duplication on polarity quotients, voltage and route-chart lifts
over small controllers, and pushing the parameters of Rajiv's generalized-polygon compounds.

**Timeline.** The first agents started on 2026-10-04 (16:39 PDT) and the last graph, (13,4) on 6 630 vertices, was
found on 2026-10-08 (18:21 PDT), about four days of wall-clock time in five working sessions on one laptop.
Each attempt kept notes, code and logs, and each claimed graph was checked by independent reviewer agents with their
own checkers before it was kept.

**What worked, per cell.**
- (13,4): the slack-insertion annealer. Rajiv's 6 611-vertex graph -> 6 612 (one run, seed 1) -> 6 614 (a chain with
  edge pruning) -> 6 629 (a second chain, about 17 hours) -> a 6 630-vertex near-miss with 2 far pairs -> closed by a
  low-temperature resume of the same annealer (2.5 minutes). Code: `how-we-built-it/13_4/`.
- (15,4): a bipartite (15,5) route-chart lift over a 330-element metacyclic group, found by an exhaustive generator
  scan plus a seeded search over the chart matrices (minutes), then folded by Delorme's polarity quotient.
- (15,3): a 60-vertex controller from a seeded annealing over Z_15 voltages on a 4-vertex base, and a route chart
  over F_3^3 solved exactly by a SAT solver (Mizuno's construction with a larger controller).
- (14,4): an affine frame lift over F_3^4 of Bhakar's 104-vertex (4,4) graph; random local data plus a SAT solver
  for the transports (about one minute per seed).
- (9,4): a Z_2 voltage lift of the W(7) incidence graph found by a symmetric local search (about 100 s), plus twin
  vertices along a spread.
- (13,6) and (15,6): Rajiv's compounds of generalized hexagons, cut at larger cut sets found by iterated local
  search (10–35 minutes per side), with surgery vertices and a few shortcut edges placed by a greedy/exact pass.
`how-we-built-it/README.md` lists, per cell, the rebuild command, the search code and what could not be recovered.

**What did not work.** The insertion annealer stalls on regular records with no free degree ((13,3), (14,3)) and
stalled on (12,3) at 2 far pairs; an exact CP-SAT neighbourhood repair of annealing near-misses was locally rigid;
the (13,4) chain itself stopped at 6 629 after 30 failed attempts and needed the separate low-temperature resume.
Graphs for (12,3) on 810 and (11,4) on 3 444 vertices turned out to tie entries posted independently the same week,
and a (14,3) graph on 1 107 vertices was overtaken by the table before release; none of these is claimed.

**Credits.** Rishabh Rajiv (seed graph for (13,4), the compounds and surgery behind (13,6) and (15,6); Zenodo
10.5281/zenodo.23052995, CC BY 4.0); Ryosuke Mizuno (route-chart lifts, arXiv:2606.15860); Charles Delorme
(polarity quotients); Nishant Bhakar (the (4,4) controller); Gómez and Fiol (compound graphs); Payne and Thas (W(q));
F. Comellas for maintaining the table. The searches, graphs and code are by AI agents; the checks before release were
made by independent reviewer agents. No outside expert has reviewed the graphs yet.
