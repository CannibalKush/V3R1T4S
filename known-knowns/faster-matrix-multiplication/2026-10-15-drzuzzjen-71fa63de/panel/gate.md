# Honesty gate (run's main session, 2026-10-15T15:30:03Z)

REPRODUCE pass (own checker, all 15625 triples, 358 calibrated at 383 and the README example 15, deterministic, 16/16
mutants rejected, single-term aliases inlined without changing the count). NOVELTY pass (own fetches 15:21:27Z-15:25:42Z,
all HTTP 200, identical to the claim's 15:20Z snapshot; live minimum 383, also 383 in arXiv:2512.13365; lowest visible
anywhere 378 in closed unmerged V3R1T4S PR #21; no open PR covers 5x5x5; 5 is prime, so no Kronecker construction).
CRITERION pass (clause by clause; re-reduction of Perminov's exact bilinear scheme, allowed by the criterion; every
intermediate ternary).

Downgrade checks: hedging panelist - no; reproduction mismatch - none; not strictly better - no (358 < 378 < 383);
stretched criterion - no; scope wider than reproduced - no; sample presented as complete - no (full tensor identity);
capped search used as exclusion - no; table value by evasion - no; several objects bundled - no. Panel fetches < 6 h old.
Method credit: Boyar-Peralta heuristic; ternary-cancellation variant as described in PR #161 (own code, tools/bp.py).

status: CONFIRMED_SOLUTION
confirmed_scope: The file 5x5x5_m93_cr358_ZT_reduced.json (sha256 71fa63de…129f5c) is a ternary straight-line program that computes the 5x5x5 matrix product exactly over Z with 93 multiplications and 358 binary additions/subtractions counted under Perminov's reduced convention (negations and single-term aliases free, every intermediate ternary); it is a re-reduction of the same bilinear scheme as Perminov's 5x5x5_m93_cr383 file and strictly below 383, which is the only and hence minimum reduced count for 5x5x5 rank 93 in the Perminov sources fetched 2026-10-15T15:20Z; no lower count for this format and rank appears in reduced_known.json, the README, the CHANGELOG, the Lille 5x5x5 page or matmulcatalog COVERAGE.md (+846).
