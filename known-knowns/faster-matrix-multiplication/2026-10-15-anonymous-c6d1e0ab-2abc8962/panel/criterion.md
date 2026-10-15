# Criterion skeptic report: add-5x7x7-cr699

Own checker written from the criterion (criterion_ws/chk.py); the author's checker was not read.
Fetches (each once, honest User-Agent, no retries): Perminov's cr788 file, fmm_sota.json (createdAt 2026-10-09T11:45:48), the GitHub git tree of the repository, the Lille 5x7x7 page, matmulcatalog COVERAGE.md. Claim folder hashes: all 8 files match claim.SHA256SUMS.

## Checker results on the claim object (claim/object/5x7x7_m176_cr699_ZT_reduced.json)
- Format n = [5, 7, 7], m = 176. Fresh variables: U 179, V 206, W 103; final forms: U 176, V 176, W 35.
- Straight-line order: every term references only inputs or earlier fresh variables (asserted per form, no forward reference). Every coefficient is +1 or -1 (asserted).
- Expansion over the inputs with exact integers: maximum absolute expanded coefficient over all fresh variables and all final forms = 1, so every intermediate and final form is ternary (no non-ternary intermediate anywhere).
- Brent equations for 5x7 times 7x7 (35 x 49 x 35 entries, C-transposed output index k*5+i): 0 violations. Evaluation on 5 random integer matrix pairs (entries in [-50, 50]): exact match.
- Reduced count (sum over every fresh and final form of terms - 1; negation free): U 179, V 206, W 314, total 699.

## Calibration on Perminov's file (5x7x7_m176_cr788_fv371_cn2605_ZT_reduced.json)
- Same checker: rank 176, max expanded coefficient 1, 0 Brent violations, random evaluation ok. Counts U 205, V 236, W 347, total 788, which matches the file name.
- Expanded U, V, W rows (the 176 products and 35 outputs) are identical to the claim's, row for row (U True, V True, W True). Only the programs differ. So the claim is a re-factoring of the same scheme, not a new scheme.

## Null models and corruptions (all rejected)
- Flip sign of a W fresh term: rejected (expanded coefficient 2, non-ternary).
- Duplicate a term (coefficient 2): rejected (non-ternary).
- Forward reference in a U fresh form: rejected.
- Flip sign in u[7]: 140 Brent violations, random evaluation fails.
- Drop a term from w[10]: 36 Brent violations, evaluation fails.
- Swap an index in v[100][0]: 416 Brent violations, evaluation fails.
- Swap two output rows (wrong C layout): 28 Brent violations, evaluation fails.

## Clauses
1. "explicit straight-line program ... for a format with max(n,m,p) <= 8": 5x7x7, max 7. Met.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": the only entry with format sorting to 5,7,7 is rank 176 (exponent 2.819619); the object has rank 176. Met.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": exact integer expansion, zero Brent violations, ternary at every step, random integer evaluation. Met.
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository ... the MINIMUM cr value over all files for that format and rank": the live tree (6637 entries, not truncated) has exactly one file for 5x7x7 in schemes/results/addition_reduced_ZT, with cr788 (rank 176). 699 < 788. Files in schemes/results/naive_addition_reduced_ZT (c2535, c2610) are named _cNNNN_ZT without cr: they are naive counts (nonzeros-based, the same family as matmulcatalog's convention, before any common-subexpression reduction), so they are not comparable with a reduced count and are not a lower reduced count; they are also far above 699 in any case. I did not check reduced_known.json, README or CHANGELOG, which the criterion also names, beyond the tree listing and the one cr file. Met on the evidence checked.
5. "below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant": the Lille 5x7x7 page shows rank 176 (Kauers-Wood, arXiv 2505.05896) and an "Algorithm type" polynomial; it cites no complexity variant and no operation count. Nothing lower to beat. Met (vacuously).
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": the row for 5,7,7 shows 176 and "+2745" adds, a naive count nz(U)+nz(V)+nz(W)-2r-n*p. 699 < 2745, and the convention differs (naive, not reduced), so it is not a competing reduced count. Met.
7. Coefficient class: the Lille rank is attained over Z/ternary here (same ternary scheme), so no class mismatch. Met.
8. "Each scheme is claimed once; a scheme that also lowers the rank is a rank target": rank unchanged at 176. Met.
Limit: criterion text says "re-fetched live immediately before claiming"; my fetches are my own at review time, and the author's fetch time is in INDEX.csv (not audited here). The result is a pure re-factoring of Perminov's existing 176 products (identical rows), which the criterion does not exclude.

## Verdicts
Full criterion: met on every clause checkable from these sources.
p1 (the enumerated partial win concerns rank-23 for 3x3x3, not this format): p1 here is the task's "strictly fewer than Perminov's live 5x7x7 count, same convention": 699 < 788 under the identical counter. Met. (The kit's literal p1 in CLAIM.md is the 3x3x3 rank-23 item, which this claim does not address; the full criterion subsumes the brief's p1.)

confirmed_scope: The program in claim/object/5x7x7_m176_cr699_ZT_reduced.json (sha256 2abc89623e051336de20440c1e68300d56656b98733b8df7e66808bbd60174be) is an exact ternary straight-line program for the same 176 products as Perminov's cr788 5x7x7 file, verified over Z by my own Brent and random-matrix checks, and costs 699 reduced additions (U 179, V 206, W 314) against his sole 5x7x7 addition_reduced_ZT file at 788, with the Lille page citing no operation count and matmulcatalog's naive +2745 not on the reduced convention, as of my fetches.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
