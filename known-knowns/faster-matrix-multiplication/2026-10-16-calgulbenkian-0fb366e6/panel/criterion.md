# Criterion skeptic report: add-5x8x8-cr929

Method: I wrote my own checker (criterion_ws/chk.py) from the criterion before reading the author's. All fetches were done once, with the honest User-Agent, no retries, into criterion_ws/.

## Own checker output on the claim object (claim/object/5x8x8_m230_cr929_ZT_reduced.json)

- Straight-line order: every form references only inputs or earlier fresh variables (no order errors). Every written coefficient is +1 or -1 (no coefficient errors).
- Expanded to linear forms over the inputs with exact integers: every fresh variable and every final form has all coefficients in {-1,0,1}; maximum absolute expanded coefficient = 1; zero ternary violations. U has 205 fresh forms, V 327, W 136.
- Full tensor identity for <5,8,8> (Brent equations, exact, C-transposed output layout, output k*5+i is C[i][k]): the sum over 230 products of U x V x W equals the matrix multiplication tensor exactly (0 mismatching entries). Random integer matrices (5 trials, entries -9..9): all 40 outputs equal A*B.
- Count under the reduced convention, sum over fresh and final forms of (terms - 1): U 205, V 327, W 397; total 929. Matches the claimed 929.

## Calibration on Perminov's file (5x8x8_m230_cr974_fv447_cn2747_ZT_reduced.json, fetched once)

- My counter gives 974 (U 225, V 337, W 412); his file also passes the ternary and tensor checks. The file's own metadata says reduced 974.
- The 230 expanded U, V, W rows (final product factors and outputs) are identical to the claim's, row for row in the same order. So only the programs differ.
- No map's program is identical to his: u_fresh, u, v_fresh, v, w_fresh, w all differ as JSON. Fresh counts differ (his 115/101/231, claim 205/327/136). Per-map reduction: U 225 to 205, V 337 to 327, W 412 to 397.

## Clauses

1. "explicit straight-line program ... for a format <n,m,p> with max(n,m,p) <= 8": MET. Format 5x8x8, max 8.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": MET. fmm_sota.json entries has format [5,8,8] rank 230; the object has m = 230. (File createdAt 2026-10-09T11:45:48.)
3. "(1) verified symbolically to compute the full product A*B exactly over Z": MET, exact integer expansion and tensor identity as above, plus random evaluation. (Exact integer tensor expansion, not a sympy pass; equivalent for a bilinear program.)
4. "(2) STRICTLY LESS than the smallest reduced addition count for that format and rank in Perminov's live repository ... counted under the 'reduced' convention": MET. The tree listing (6637 entries, not truncated) shows exactly one file for 5x8x8 in addition_reduced_ZT: the cr974 file, so the minimum cr is 974. 929 < 974. The convention is the same one my counter reproduces as 974. I did not fetch reduced_known.json, README or CHANGELOG (not in my brief's fetch list); the criterion names them, so that part is unchecked by me.
5. Files named _cNNNN_ZT without "cr": c2638 and c2741 exist for 5x8x8 m230, but they are in the separate directory schemes/results/naive_addition_reduced_ZT, not in addition_reduced_ZT. They are naive counts nz(U)+nz(V)+nz(W)-2r-np style (the object's own metadata has naive 2747) with no shared-subexpression reuse, so they are not on the reduced convention and are not comparable; they are also not in the directory the criterion's minimum ranges over.
6. "AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant": MET vacuously. The fetched 5x8x8.html page text contains no complexity variant, addition count or operation count for rank 230 (searches for complexity, addition, operation, cost, variant, best return nothing); it gives the algorithm type polynomial and decomposition only. So no lower count is published there.
7. "and in matmulcatalog's live COVERAGE.md 'adds' column": MET. Its row for <5,8,8> shows "+2638" for rank 230 (Dronperminov-c2638_ZT). The column is the naive count nz(U)+nz(V)+nz(W) - 2r - n*p, a different convention; 929 is below it in any case, and it does not undercut the claim.
8. "same coefficient class" / Lille rank only non-ternary: not triggered; the Lille rank 230 is matched by a Z/ternary scheme.
9. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": MET. Rank equals the best rank (230), not lowered.

## Null models and corruptions (my checker rejects each)

- Flipped sign of one term in w_fresh[5]: tensor identity fails (216 mismatching entries), random evaluation fails, and expanded ternary condition violated.
- Replaced u[17] by another form (dropped term): tensor fails (48 mismatches), random fails.
- Shifted one input index in v[40]: tensor fails (27), random fails.
- Swapped output forms 3 and 4: tensor fails (32), random fails.
- Coefficient 2 in u_fresh[10]: coefficient error and non-ternary expansion reported, tensor fails.
- Forward reference in u_fresh[0]: order error reported, tensor fails.
Counts are unchanged by these corruptions (929), so the count alone does not validate; the identity check does, and it rejects all six.

## Verdicts

- Full criterion: MET, with the limit that reduced_known.json, README and CHANGELOG of Perminov's repository were not fetched by me. The addition_reduced_ZT directory, which the criterion makes the minimum's source ("the MINIMUM cr value over all files for that format and rank in the live directory"), was checked.
- Partial win p1 as written in this bank is about <3,3,3>:23 and is not what this claim is. In the brief's sense (strictly fewer than Perminov's live 5x8x8 count, same convention): met, 929 < 974. The claim meets the full criterion, which subsumes this p1.

confirmed_scope: claim/object/5x8x8_m230_cr929_ZT_reduced.json (sha256 0fb366e6a2a5cc6bc6fd0b31334b1d859df86c180c0fc30759cbbd41c4867501) is a ternary straight-line program that exactly computes the <5,8,8> product over Z with the same 230 products as Perminov's cr974 scheme and 929 additions under the reduced convention (U 205, V 327, W 397), strictly below the 974 in his only addition_reduced_ZT file for this format and rank, with the Lille 5x8x8 page citing no operation count and COVERAGE.md listing only the naive +2638.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
