# Criterion skeptic report: add-3x5x5-cr211

Own checker: criterion_ws/chk.py (written before reading the author's). Data fetched once each with the stated User-Agent, no retries.

## My checker's output
- Object parsed; layout n=3, 58 products, U inputs 15 (A 3x5), V inputs 25 (B 5x5), W inputs 58. Fresh counts u 48, v 69, w 26; finals u 58, v 58, w 15.
- Straight-line order: every form references only inputs or strictly earlier fresh variables (a forward reference is rejected by the checker). No errors. Every coefficient is +1 or -1. No form repeats an index. No fresh variable is unused.
- Expanded over Z with exact integers: every fresh variable and every final form expands to coefficients in {-1,0,1}. No non-ternary intermediate. Result: 0 errors.
- Brent equations for 3x5 times 5x5, exact, all 3*5*5*5*3*5 index combinations, output k*3+i read as C[i][k] (transposed layout): 0 failures. Random integer matrices (20 trials, entries -9..9): C equals A*B every time.
- Additions, reduced convention (sum of terms-1 over all fresh and final forms): U 48, V 69, W 94, total 211. Confirmed 211. Expanded nonzeros U 159, V 168, W 161 give naive count 159+168+161-116-15 = 357.

## Calibration
- Perminov's file 3x5x5_m58_cr221_cn357_ZT_reduced.json fetched: my counter gives U 53, V 72, W 96, total 221 (file says reduced 221, naive 357); it passes my checker with 0 errors.
- The 58 expanded U, V, W rows of the claim are identical to his, row by row, with signs, in the same order. So it is the same scheme with a different program.
- No map's program is identical to his: u_fresh, u, v_fresh, v, w_fresh, w all differ. Counts per map: claim 48/69/94, his 53/72/96.

## Null models and corruptions (all run through my checker)
- Flipped sign in w_fresh[3]: rejected (non-ternary expansion and Brent failure).
- Dropped a term from u_fresh, v_fresh, w_fresh and w (one each): all four rejected (Brent failure).
- Swapped an index in u[5]: rejected.
- Coefficient 2 in u_fresh[0]: rejected (non-unit coefficient, non-ternary expansion).
- Forward reference in v_fresh: rejected.
- Extra term in w[0]: rejected.
- Swapped outputs w[0], w[1] (wrong layout): rejected.
- Appended an intermediate 2*a0 (non-ternary): rejected.
- Note: my first "dropped term" trial hit a single-term form, so nothing was removed and it was accepted; I redid it on multi-term forms and all were rejected.

## Clauses
1. "an explicit straight-line program ... for a format <n,m,p> with max(n,m,p) <= 8": met. Format 3x5x5, max 5.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": met. Live fmm_sota.json (createdAt 2026-10-09T11:45:48) lists format [3,5,5] rank 58; the claim has rank 58.
3. "(1) is verified symbolically to compute the full product A*B exactly over Z": met. Exact integer Brent identity plus random evaluation, above. The author's sympy cross-check was not run by me.
4. "(2) ... STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository ... counted under ... 'reduced' convention": met against the file set I could read. The live tree (git trees API, not truncated) has exactly one file for this format in addition_reduced_ZT: 3x5x5_m58_cr221_cn357_ZT_reduced.json, so the minimum cr is 221 (no 5x5x3 or 5x3x5 variants either). 211 < 221. The same counter gives 221 on his file. Not checked by me (outside the fetches named): reduced_known.json, README and CHANGELOG.
5. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant": met, vacuously. The Lille 3x5x5 page (fetched) cites no operation count or complexity variant for rank 58. It only gives the type polynomial, the source (Sedoglavic and Smirnov, arXiv 2101.12568) and Maple encodings. There is no lower count to beat.
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": met. Row for 3,5,5 shows +413. Its convention is the naive count nz(U)+nz(V)+nz(W)-2r-np for its own scheme file. That is not the reduced convention, but 211 is below it, and below this scheme's own naive 357 as well.
7. Files named _cNNNN_ZT without "cr" (here naive_addition_reduced_ZT/3x5x5_m58_c351_ZT.json, 351) are naive counts (no common-subexpression sharing), a different convention, so they are not comparable to a reduced count and are not in the addition_reduced_ZT directory the criterion names. Even so 211 < 351.
8. "If the Lille rank is attained only with non-ternary coefficients": not applicable. The candidate is ternary and the comparison is in the same class.
9. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": met. Rank 58 equals the live best, it does not lower it.
10. Hidden-quantifier hunt: "strictly fewer" is against a minimum over a single-file set, so the reference is 221. The products are Perminov's, so the win is purely in the program, which is what the target (addition counts at fixed rank) is for. How the program was found is not examined here, and literature novelty is left to the other skeptic. The win depends on the live repository state at fetch time (2026-10-15).

## Verdicts
Full criterion: met on every checkable clause. The comparison to Perminov's live reduced count (221 to 211) is genuine and not subsumed by any lower count in the sources named.
p1 concerns <3,3,3>, not <3,5,5>, so the claim does not meet it; the claim meets the full criterion, not a partial win.

confirmed_scope: The program claim/object/3x5x5_m58_cr211_ZT_reduced.json (sha256 9407c156647ed8a24fbd9e29d7f644e1fd6281aabc4eaa317bb5cb3a3a9b5b23) is, on my checks, a ternary straight-line program for the rank-58 scheme for <3,5,5> (the same 58 products as Perminov's cr221 file) that exactly computes A*B over Z and uses 211 reduced additions (U 48, V 69, W 94), below 221, the only addition_reduced_ZT count for this format and rank in his live tree on 2026-10-15, and below the +413 naive adds in matmulcatalog COVERAGE.md; the Lille 3x5x5 page cites no operation count.
context: Claude Code subagent (Fable 5.1), fresh context
p1: false
pass: true
