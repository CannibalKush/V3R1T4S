# Criterion skeptic report: add-5x6x6-cr502

Own checker: criterion_ws/chk.py (expansion, ternary check, Brent identity, random evaluation, count) and criterion_ws/more.py (comparison, null models). Written before reading the author's checker (not read).

## Object checks (claim/object/5x6x6_m130_cr502_ZT_reduced.json, sha256 ea5b1d00...a097 matches claim.SHA256SUMS)

Clause (1): "verified symbolically to compute the full product A*B exactly over Z". Met.
- Format n,m,p = 5,6,6, m = 130. Every term has value +1 or -1. Straight-line order confirmed for U, V, W: every reference is to an input or an earlier fresh variable (u ok, v ok, w ok).
- Every fresh variable and every final form expanded over the inputs with exact integers: all expanded coefficients lie in {-1,0,1} (no non-ternary intermediate; the check would assert otherwise).
- Brent tensor identity for 5x6 times 6x6 (A index i*6+j, B index j*6+k, output index k*5+i = C[i][k], transposed layout): sum over 130 products equals the matrix multiplication tensor exactly, no missing or extra entries. Result: True.
- Random integer matrices (20 trials, entries -50..50): all 30 outputs equal A*B. Result: True.

Clause (2), count under the reduced convention (one per binary +/-, negation free, sum of terms-1 over all fresh and final forms). Own counter output:
- U: fresh 129, final 0, total 129
- V: fresh 147, final 0, total 147
- W: fresh 146, final 80, total 226
- Total 502. Met as a count.

## Calibration
Fetched Perminov's 5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json once. My counter: U 146, V 174, W 242, total 562 (matches the file name). Its Brent identity and random evaluation also pass. Its 130 products (expanded U,V,W rows, compared up to sign normalization of the u and v factors) are identical to the claim's: 130 of 130 in common. So the claim is a re-addition of the same scheme (same product set, new SLP), as CLAIM.md says; the criterion compares formats at the best rank, so this is allowed.

## Null models (all rejected)
- Flipped sign of one term in w_fresh[5]: Brent False, evaluation False.
- Dropped last term of w[3]: Brent False, evaluation False (count 501).
- Swapped an index in u_fresh[10]: Brent False, evaluation False.
- Flipped sign of v[7]: Brent False, evaluation False.
- Doubled coefficient (x0 + x0) in a fresh form: rejected as non-ternary.
- Forward reference (index 300 in v_fresh[3]): rejected as breaking straight-line order.

## Clause-by-clause
1. "format <n,m,p> with max(n,m,p) <= 8": 5,6,6. Met.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": fmm_sota.json fetched live (createdAt 2026-10-09T11:45:48); entry format [5,6,6], rank 130. Met.
3. "STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository": live tree (not truncated) holds exactly one addition_reduced_ZT file for this format at rank 130, cr562 (no 6x5x6 or 6x6x5 permutation files; 5 files contain m130 in that directory overall, only one for this format). reduced_known.json has no 5x6x6 or permutation key. Minimum cr = 562; 502 < 562. The files under naive_addition_reduced_ZT (c1697, c1714) and the _cNNNN names are naive counts (nonzero-entry style count of the unreduced scheme, same convention family as the COVERAGE adds column), not reduced SLP counts, so they do not compare and are not the reference; they are also far above 502 in any case. Met. I did not re-read README/CHANGELOG text beyond the tree and reduced_known.json.
4. "below any lower count published ... on the live Lille per-format page's cited complexity variant": the Lille 5x6x6 page cites the algorithm <5x6x6:130> from Kauers and Wood (arXiv 2505.05896) with a type polynomial in X,Y,Z; it cites no complexity variant and no operation count. No lower published count exists there to beat. Met (vacuously).
5. "and in matmulcatalog's live COVERAGE.md 'adds' column": row for <5,6,6> shows r=130 and "+1716" adds, under the naive convention nz(U)+nz(V)+nz(W) - 2r - n*p. 1716 is a naive count (Perminov's file cn1716 is the same number for his scheme); 502 is below it, and is not the same convention but the criterion asks only that the count be below. Met.
6. "If the Lille rank is attained only with non-ternary coefficients ...": the Lille rank 130 is attained by a ternary scheme (Perminov's), so the same-class comparison applies and holds. Met.
7. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": the rank stays 130, no rank lowering. Met.

Limits: the 502 count and ternary expansion rely on my checker plus the reduced convention stated in CLAIM.md; I did not run sympy or the author's code. Whether 562 is truly the minimum is established only from the live tree listing fetched once.

## Verdicts
Full criterion: all clauses met on the evidence above.
p1 (the brief's version: strictly fewer than Perminov's live 5x6x6 count under the same convention): met, 502 < 562. It is subsumed by the full criterion, which is also met. (The bank's own enumerated p1 concerns <3,3,3> and is not what this claim addresses.)

confirmed_scope: claim/object/5x6x6_m130_cr502_ZT_reduced.json (sha256 ea5b1d00e3702536a57a8598f0f09040f99b503e844d5018556128ac81d0a097) is a ternary straight-line program for 5x6 times 6x6 with the same 130 products as Perminov's cr562 file, verified exactly over Z with 502 additions under the reduced convention, below the sole live addition_reduced_ZT count of 562 and the COVERAGE.md naive count of 1716, with no operation count cited on the Lille 5x6x6 page.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
