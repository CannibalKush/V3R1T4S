# Criterion skeptic report: add-5x6x7-cr582

I wrote my own checker (criterion_ws/chk.py, standard library only) before reading the author's. All sums below were verified from the claim folder files listed in claim.SHA256SUMS (all eight entries verify OK when run inside the claim folder).

## My checker's real output on the claim object

Inputs: U map has 30 inputs (A row-major), V map 42 inputs (B row-major), W map 150 inputs (products). Fresh variable k has index inputs+k.

- Straight-line order: every form references only inputs or strictly earlier fresh variables (all three maps): True.
- Every coefficient in the file is +1 or -1: True.
- Expanded to linear forms over the inputs with exact integers, every fresh variable AND every final form has all coefficients in {-1,0,1}: True (ternary, so no non-ternary intermediate hides a cancellation).
- Shapes: 150 u rows, 150 v rows, 35 w outputs: True.
- Full tensor identity (exact, all 5*6*6*7*5*7 index triples), sum_t U[t][a] V[t][b] W[o][t] = 1 exactly when a=(i,j), b=(j,l), o=l*5+i (the C-transposed layout, output k*n+i is C[i][k]), 0 elsewhere: True.
- 20 random integer matrix pairs (entries -9..9): all 35 outputs equal A*B: True.
- Additions under the reduced convention, sum over fresh and final forms of (terms - 1): U 147 + V 171 + W 264 = 582. The file's own complexity field also says reduced 582, naive 2039.
  (Fresh form counts: u 147, v 171, w 94 fresh forms; one addition each for two-term forms is only an example, the total is computed from term counts.)

## Calibration on Perminov's file

Fetched once: schemes/results/addition_reduced_ZT/5x6x7_m150_cr664_fv310_cn2039_ZT_reduced.json (HTTP 200). My counter gives U 172 + V 198 + W 294 = 664, matching the cr664 in its name; the file also passes my ternary, order, tensor-identity and random-evaluation checks. Its 150 products (expanded U rows, V rows) and expanded W rows are identical to the claim's (U equal True, V equal True, W equal True). So only the straight-line programs differ, and the claim cuts 664 to 582 (U 172->147, V 198->171, W 294->264).

## Clauses

1. "explicit straight-line program ... for a format <n,m,p> with max(n,m,p) <= 8": 5x6x7, max 7. Met.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": fetched once (HTTP 200); entries contain format [5,6,7] rank 150 (exponent 2.811222). The object has m=150. Met.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": exact integer expansion of all forms and exact tensor identity (a symbolic identity over all index triples) plus random evaluation. Met.
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository ... the MINIMUM cr value over all files for that format and rank": tree API fetched once (HTTP 200, not truncated). Under addition_reduced_ZT/ there is exactly one file for 5x6x7 (and none for any permutation of the format): cr664. Minimum is 664. 582 < 664. reduced_known.json (fetched once, HTTP 200) has no 5x6x7 entry. Met. The counting convention (binary +/- one each, negation free, no other scalars) is the one my counter reproduced on cr664.
5. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant": fetched 5x6x7.html once (HTTP 200). The page shows rank 150, an "Algorithm type" polynomial in X,Y,Z, and the source (Kauers and Wood, arXiv 2505.05896). It cites no complexity variant and no operation or addition count (no occurrence of complexity, addition, operation, or a Commentaries section). Nothing lower exists to beat. Met (vacuously). The page's algorithm type is a structural polynomial, not an addition count, so I do not treat it as a rival number.
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": fetched once (HTTP 200). Row for <5,6,7>: 150, Dronperminov-ZT, adds "+2039". Its legend defines adds as nz(U)+nz(V)+nz(W) - 2r - n*p, a naive count with no common-subexpression sharing, equal to Perminov's naive 2039 and to this object's naive field 2039. It is a different convention, so not comparable with 582; 582 is not below it in a like-for-like sense but also no lower reduced figure is published there. Taken literally (582 < 2039) it is also met. Met either way.
7. "If the Lille rank is attained only with non-ternary coefficients, compare in the same coefficient class": the candidate is ternary; the Perminov baseline is the same ternary class; the Lille page has no count. Not triggering.
8. "Each scheme is claimed once; a scheme that also lowers the rank is a rank target": rank 150 equals the live best, not lower. The products are the same as Perminov's scheme, only the straight-line program changed. Met.

Note on files named _cNNNN_ZT without "cr": they sit in a different directory, schemes/results/naive_addition_reduced_ZT/ (5x6x7_m150_c1994_ZT and c2039_ZT, json and .m). They count naive nonzero-based additions of the product tables with no shared subexpressions, a different convention and a different directory, so they do not enter the "minimum cr over addition_reduced_ZT files" the criterion defines. Observation: c1994 is a lower naive count than 2039, but that is a naive count, not an SLP count, and it is not claimed against.

Limits: the checker confirms ternary expanded coefficients and an exact bilinear identity; it does not judge literature novelty.

## Null models and corruptions (my checker, real output)

- Flip one sign in a W output term: REJECTED (non-ternary expansion, tensor identity False, random False).
- Drop a term from u[10]: REJECTED (tensor False, random False).
- Swap v rows 5 and 6: REJECTED (tensor False).
- Shift one input index inside v_fresh[100]: REJECTED (tensor False).
- Swap two outputs w[0], w[1] (wrong C layout): REJECTED (tensor False).
- Forward reference in u_fresh[50]: REJECTED (straight-line order False).
The unmodified object is accepted in the same run.

## Verdicts

Full criterion: met. A ternary rank-150 SLP for <5,6,7> with 582 reduced additions, verified exact over Z, strictly below the single live Perminov addition_reduced_ZT count of 664 for this format and rank, with no lower count on the Lille page or in COVERAGE.md.

Partial win p1 as written in the bank is for <3,3,3> rank 23, so it does not apply to this claim. Per your brief's definition (strictly fewer than Perminov's live 5x6x7 count under the same convention) it is met, but that is subsumed by the full criterion, not a separate win.

confirmed_scope: The file claim/object/5x6x7_m150_cr582_ZT_reduced.json (sha256 832b08667df7d72d5c12f78f7073168f43dd50e323aaaf547290f0533d2585f3) is a ternary straight-line program for the rank-150 scheme of <5,6,7> (same 150 products as Perminov's cr664 file) that exactly computes A*B over Z with 582 additions under Perminov's reduced convention (U 147, V 171, W 264), against 664 for the only live addition_reduced_ZT file at that rank, with no lower count cited on the Lille page or in COVERAGE.md.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
