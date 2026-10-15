# How we found it (contributor text, unverified)

This condenses the original agent run's own account. The claim rests only on `object/win_q2_n173_k17_d72.json` and the checker in `verify-it-yourself/`.

1. **Lens 1** (`how-we-built-it/qc_search.c`): a quasi-cyclic / quasi-twisted search over polynomial ideals in GF(2)[x]/(x^m - 1), with zero-divisor CRT lifting and a coset-weighted Construction X step. The object's `construction` field records the parameters: m = 85, lambda = 1, l = 2, k_core = 16, s = 5, s' = 1, t = 3.
2. **Lens 2** (`how-we-built-it/bklc_opt.c`): puncturing guided by a histogram of the minimum-weight codewords, and column extension chosen to minimize the number of minimum-weight words.

The same run also reported [170,17,69], [171,17,70], [172,17,71] and [174,17,72]. Each follows from this code by puncturing or by adding a zero coordinate, so they are not claimed here.
