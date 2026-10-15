# How we found it (contributor text, unverified)

The claim rests only on `object/code_q2_n175_k25_d61.json` and the checker in `verify-it-yourself/`.

1. **Where to look.** In the codetables.de binary table, the k = 25 row is flat at lower bound 60 for every length from 170 to 175. A length-170 code with distance 60 and few minimum-weight words leaves five columns to spare, and five well-chosen columns can lift the distance to 61.
2. **Base code.** A search over one-generator quasi-cyclic codes of index 2 with circulant size 85 (iterated local search on the multiplier f, 30 seconds) found the [170, 25, 60] code with h = 0x36a5431 and f = 0xe600fc, whose 680 weight-60 words form 8 orbits of the cyclic shift.
3. **Five columns.** A covering search (30 seconds) chose five message functionals such that each of the 680 weight-60 words has a 1 in at least one of them. The result has distance 61.
4. **Shorter attempts.** An exhaustive scan of all 394,759 multiplier classes for this h found no length-170 code with distance 61, and the best four-column covers of the 680 words left 3 to 5 words uncovered, so length 175 is the shortest this route reached.

The search programs are in `how-we-built-it/` for transparency (the versions at packaging time; they evolved during the run). The deterministic `rebuild.py` there, not the search, regenerates the object.
