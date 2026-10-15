# Criterion skeptic report: add-6x6x8-cr719

I wrote my own checker (criterion_ws/chk.py, pure Python, exact integers) before reading the author's checker. Hash list verified first: all 8 files in claim.SHA256SUMS report OK when run from inside the claim folder.

## My checker on the claimed object (claim/object/6x6x8_m203_cr719_ZT_reduced.json)

Real output:
straight_line_order True; coef_pm1 True (every written coefficient is +1 or -1); expanded_ternary True (every fresh variable AND every final form, expanded over the inputs with exact integers, has all coefficients in {-1,0,1}); shape True (203 U rows, 203 V rows, 48 W rows); brent_exact True (full tensor identity for 6x6 times 6x8 with output k*6+i = C[i][k], the transposed layout; equals the target tensor exactly); random_eval True (20 random integer matrix pairs, all 48 entries of C equal A*B).
Additions (sum over fresh and final forms of terms-1): U 174, V 195, W 350, total 719. (W 350 = 144 fresh forms plus 48 output forms.) Matches the object's own declared reduced 719.

## Calibration on Perminov's file (fetched once, 2026-10-15 11:39 UTC)

File 6x6x8_m203_cr836_fv454_cn1994_ZT_reduced.json: same checker returns valid=True, U 200, V 235, W 401, total 836. Calibration passes: my counter reproduces 836 and the declared naive 1994 (nonzeros 2448, minus 2r, minus 48).

Products comparison: the 203 expanded products of the claim are NOT the same as Perminov's. Only 18 of 189 distinct U rows and 12 of 189 distinct V rows (up to sign) are shared, and no product (u,v) pair matches. So the claim's CLAIM.md statement "the scheme is the one in Perminov's repository at that rank" is literally false: this is a different rank-203 scheme (nonzeros 2968, naive 2514, versus Perminov's 2448 and naive 1994) that is valid in its own right. The criterion does not require reusing his scheme, so this does not fail a clause, but the claim sentence is wider than the evidence on that point.

## Clauses

1. "explicit straight-line program ... for a format n x m x p with max(n,m,p) <= 8 and rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)". Format 6x6x8, max 8. Live fmm_sota.json (createdAt 2026-10-09T11:45:48) entry: format [6,6,8], rank 203, exponent 2.814715. Object rank 203. MET.
2. "(1) verified symbolically to compute the full product A*B exactly over Z". Exact integer expansion, tensor identity equals the matrix multiplication tensor, plus random integer evaluation. Ternary at every intermediate. MET.
3. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository ... counted under the reduced convention". Live tree (not truncated, 195 files in addition_reduced_ZT) has exactly one 6x6x8 file, cr836; minimum 836. 719 < 836 under a counter I calibrated to give 836 on his file. reduced_known.json (fetched once) has no 6x6x8 entry. I did not fetch README or CHANGELOG (not in my brief; the author's table-record says they state no lower count; unverified by me). MET for the files and reduced_known.json I checked. No file in that directory lacks "cr" in its name, so the naive-count caveat does not arise for this format; the naive numbers (cn) are the nonzero-count convention and would not compare anyway.
4. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant". The live page 6x6x8.html states rank 203, a Kronecker product of 2x2x2:7 with 3x3x4:29, and a polynomial type; it cites no complexity variant or operation count. Nothing to be below. MET (vacuously).
5. "and in matmulcatalog's live COVERAGE.md 'adds' column". The 6,6,8 row reads: verified 203 (Dronperminov cr836 file), adds cell "—" (empty). The column is the naive count nz(U)+nz(V)+nz(W)-2r-np and is shown for verified schemes only; here none. Nothing lower exists. MET (vacuously). Under its naive convention the claim's scheme (2514) is actually worse than Perminov's file (1994), so the claim must not be read as beating the naive convention; it does not claim that.
6. "If the Lille rank is attained only with non-ternary coefficients ..." Not triggered: Lille construction is a Kronecker product; the candidate is ternary and Perminov's ZT file is the same class.
7. "reference count is the MINIMUM cr over all files for that format and rank". Single file, 836. MET.
8. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target". Rank equals 203, not lowered. MET.

## Null models (my checker rejects all)

Baseline valid=True total 719. Rejected, valid=False: N1 flipped one sign in a U product factor (Brent and random fail); N2 dropped one term from an output form (count 718, Brent and random fail); N3 swapped an index between two V product factors; N4 shifted an index in a V fresh form (also breaks the ternary check); N5 swapped two output rows (layout error); N6 coefficient 2 (coefficient and ternary checks fail); N7 swapped two U rows; N8 forward reference (straight-line order fails). Full output in criterion_ws/nulls_out.txt.

## Verdicts

Partial win p1 as the panel brief defines it (strictly fewer than Perminov's live 6x6x8 count, same convention): met, 719 < 836. (The bank's own enumerated p1 concerns 3x3x3 rank 23 and is not what this claim targets; the panel brief's p1 is the one judged here.)
Full criterion: met for 6x6x8 at rank 203, with the Lille and COVERAGE clauses met only vacuously (no competing count published there) and README/CHANGELOG not independently fetched by me.

confirmed_scope: The file claim/object/6x6x8_m203_cr719_ZT_reduced.json (sha256 b60a9f0b2339bc2927201b903c73b030905b0b39cc6a12b3a3b53fc65da014cf) is a ternary straight-line program, exactly verified for 6x6 times 6x8 at rank 203, with 719 reduced additions (U 174, V 195, W 350) against 836 in the only 6x6x8 file of Perminov's live addition_reduced_ZT, on a different rank-203 scheme than his, with no lower count on the Lille page or in COVERAGE.md.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
