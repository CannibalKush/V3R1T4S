# How we found it (contributor text, unverified)

This condenses the original agent run's own account. The claim rests only on `object/G_14_3_N1117.edges` and the checker in `verify-it-yourself/`.

1. **Spare degree.** The (14, 3) record graph Dhar_1116 is not 14-regular. It has 998 vertices of degree 14 and 118 of degree 13, so 118 edge slots are unused.
2. **Add one vertex.** A new vertex, number 1116, was joined to 14 degree-13 vertices chosen to cover as much of the graph as possible within distance 2. This left 29 vertex pairs at distance more than 3.
3. **Repair.** A compiled bit-parallel BFS with simulated annealing (`how-we-built-it/sa2_opt.c`) added edges between remaining degree-13 vertices and made targeted edge switches. It brought the 29 bad pairs to 0 in 11.5 seconds (48 accepted moves).
