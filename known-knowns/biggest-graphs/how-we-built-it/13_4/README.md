# (13,4), N = 6 630: where the graph comes from

The graph is the end of a local-search chain, not a closed-form construction; the exhaustive all-pairs BFS of
`../../graphs/G_13_4_n6630.edges` is the proof.

1. **Seed.** Rishabh Rajiv's (13,4) graph Q9(T4)++ on 6 611 vertices (Zenodo 10.5281/zenodo.23052995, CC BY 4.0), a
   compound of generalized-quadrangle incidence graphs with his surgery, formerly the table entry (13,4).
2. **Agent chain (2026-10-04 to 2026-10-08).** Repeated "slack" vertex insertion (a new vertex joined to vertices with
   free degree) followed by simulated annealing over 2-switches and single-edge rewires, minimising the number of
   pairs at distance > 4, reached a valid 6 629-vertex graph and then, with one more insertion, the near-miss
   `near_miss_N6630_cost2.edges`: 6 630 vertices, maximum degree 13, exactly 2 unordered pairs at distance 5.
   (Its first-line comment was shortened for this release; the edge lines are unchanged.)
3. **Closing the near-miss (2026-10-08).** Resuming the annealer from the near-miss at low temperature found a
   5-edge switch (`G_13_4_n6630.diff_vs_near_miss.txt`) that leaves no pair at distance > 4.

```sh
python3 apply_diff.py near_miss_N6630_cost2.edges G_13_4_n6630.diff_vs_near_miss.txt ../../graphs/G_13_4_n6630.edges
#   -> EDGE SETS IDENTICAL
../../verify-it-yourself/ddcheck near_miss_N6630_cost2.edges 13 4 4     # control: 4 ordered far pairs, INVALID
```
The annealing code is not part of the release (as for the constant-weight codes, the object and the checker are the
claim). The table entry it exceeds, 6 615, is Dharunish Yugeswardeenoo's (Oct 2026).

*Credits:* Rishabh Rajiv for the seed graph and the compound/surgery idea; Gómez and Fiol for the compound-graph
family; our agents for the insertion/annealing chain.
