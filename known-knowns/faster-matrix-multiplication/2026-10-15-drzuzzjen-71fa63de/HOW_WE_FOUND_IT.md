# How we found it (contributor text, unverified)

Brief: fewer additions than Perminov's addition-reduced ternary schemes at the best rank. We split each scheme into its three linear maps (U on A, V on B, W from products to outputs), which can be optimized independently.

What failed: pair-greedy common-subexpression elimination (direct and transposed) tied Perminov on this cell. What worked: a Boyar-Peralta-style search with cancellation, keeping every intermediate ternary, run on U, V and on W^T (W recovered by the transposition principle), with many random restarts on 28 CPU threads (lens 'bp', run 2026-10-15-1414). The method was suggested by the description in another contributor's PR #161, which in turn credits our PR #149 for the transposition step.
