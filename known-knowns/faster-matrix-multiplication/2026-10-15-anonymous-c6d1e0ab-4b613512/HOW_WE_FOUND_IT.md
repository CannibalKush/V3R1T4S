# How we found it (contributor text, unverified)

A sweep applied slice-and-absorb to published parent schemes; the method is described in a separate note. For this format the parent chain starts at A. I. Perminov's published 15x15x15 rank-1977 scheme over Q, cut to 14x15x15, 13x15x15, 13x14x15 and then 13x14x14.

1. **Slice.** Shrink one dimension by one along a direction pair chosen by the terms it removes (the explicit pairs are in `how-we-built-it/REBUILD.md`).
2. **Absorb.** Exact rational dependencies among the remaining terms let more terms be cancelled; every dependency is lifted by CRT and verified exactly before the scheme is changed.
3. **Search width.** A width-4 beam over direction pairs per step, with diverse (non-greedy) pairs tried where the greedy choice stalled; the pair that won here is recorded in the object's note field.

The result was checked against every Brent equation over Q by three independent checkers before the panel.
