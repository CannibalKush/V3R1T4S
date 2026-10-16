# Criterion skeptic report: add-4x4x5-cr222

Object: claim/object/4x4x5_m61_cr222_ZT_reduced.json (sha256 df14df3c1a01189e540ab5a0eedebc331cd08e12714d795df0884481da292366). All eight hashes in claim.SHA256SUMS verified OK with shasum -a 256 -c (paths prefixed with claim/). I wrote my own checker (criterion_ws/chk.py) before opening the author's; I did not read the author's scripts.

## My checker, real output on the claim object
- Parse: n,m,p = 4,4,5; rank 61; u_fresh 59, v_fresh 61, w_fresh 35 forms; 61 u, 61 v, 20 w final forms. Every term has value +1 or -1 (0 violations). Every form references only inputs or earlier fresh variables (0 order violations). Inputs: U 16 (A row-major), V 20 (B row-major), W 61 (products).
- Expansion over Z of every fresh variable and every final form to a linear form over the inputs: number of forms with an expanded coefficient outside {-1,0,1}: U 0, V 0, W 0. So no non-ternary intermediate, no cancellation through one.
- Tensor identity (Brent equations) for 4x4 times 4x5, sum over t of U[t][a_ij] V[t][b_jk] W[out][t] = [j==j' and out == k*4+i (C transposed layout)], over all 16*20*20 triples: 0 mismatches. Random integer evaluation (20 pairs of matrices, entries -9..9, all 20 outputs): 0 mismatches.
- Addition count, reduced convention (sum over all fresh and final forms of terms-1; negation free; multiplications not counted): U 59, V 61, W 102, total 222. The file's own complexity field says reduced 222, naive 452, consistent.

## Calibration on Perminov's file
Fetched 4x4x5_m61_cr233_fv93_cn452_ZT_reduced.json. My counter gives U 67, V 62, W 104, total 233 (matches the cr233 name), 0 ternary violations, Brent 0 mismatches, random 0 mismatches. Expanded U, V, W rows (61 products, 61 rows each of U and V, 20 W output rows) of the claim and of his file are identical, row for row in the same order (dictionary equality of the expanded forms). So the scheme is his and only the programs differ. No map's program is identical to his: u_fresh, u, v_fresh, v, w_fresh, w all differ as JSON; per map the claim is lower in all three (59 vs 67, 61 vs 62, 102 vs 104).

## Null models (all rejected by my checker)
- Flip one sign in a U product row: Brent 8 mismatches, random 38.
- Drop the last term of W output 3 (count becomes 221): Brent 6, random 20.
- Swap V products 10 and 11: Brent 96, random 90.
- Shift one index in a W fresh form: Brent 40, random 90.
- Coefficient 2 in a fresh form: coefficient violation flagged, 17 non-ternary expanded U forms, Brent 7.
- Forward reference in a U fresh form: order violation flagged.
- Swap two W outputs (layout corruption, 1 and 4): Brent 16, random 40.
- Fresh form x+x+y (non-ternary expansion, count 223): 17 non-ternary expanded forms, Brent 7.

## Clauses
1. "explicit straight-line program ... for a format n by m by p with max(n,m,p) <= 8": met. Format 4x4x5, max 5, straight-line, JSON layout.
2. "rank r equal to the best rank listed for that format in ... fmm_sota.json (re-fetched live)": met. Fetched fmm_sota.json (createdAt 2026-10-09T11:45:48); entry {"format":[4,4,5],"rank":61}. Claim rank 61. (Lille 4x4x5 page also says 4x4x5:61.)
3. "(1) verified symbolically to compute the full product A*B exactly over Z": met. Exact integer expansion over the inputs plus full tensor identity, 0 mismatches; random integer evaluation agrees.
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository (addition_reduced_ZT file, reduced_known.json, README and CHANGELOG)": met. Live git tree (not truncated) lists exactly one addition_reduced_ZT file for 4x4x5, rank 61: cr233. Minimum cr is 233 and 222 is less than 233. All 195 files in that directory carry a cr in the name; none for 4x4x5 other than cr233. Files named _cNNN_ZT (here schemes/results/naive_addition_reduced_ZT/4x4x5_m61_c452_ZT.json) are in a different directory and use the naive convention (nz(U)+nz(V)+nz(W) minus 2r minus n*p style: no common-subexpression sharing, 452 here), which is not comparable to the reduced convention; they are not reduced counts and cannot be the reference. reduced_known.json (path schemes/reduced_known.json) has 4x4x5 keys only for ranks 60 (Z2 281) and 62 (Z 476), none for rank 61. README has only the rank table row (4x4x5, 61, exponent 2.814); CHANGELOG has no 4x4x5 mention. Counting convention matches (calibration 233 reproduced).
5. "AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant": met vacuously. Fetched fmm.univ-lille.fr/4x4x5.html: it describes 4x4x5:61 taken from AlphaEvolve (2025), gives the algorithm-type polynomial and downloads; it cites no complexity variant and no operation count. Nothing lower exists there to compare against.
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": met. The 4x4x5 row shows +455 adds under its own naive formula nz(U)+nz(V)+nz(W) - 2r - n*p; 222 is less than 455 (and that is a different, non-shared-subexpression convention, so the comparison is only a weak one, but no count below 222 is published there).
7. "If the Lille rank is attained only with non-ternary coefficients, compare in the same coefficient class": not triggered; the candidate is ternary (Z) and compared with Perminov's ZT file.
8. "reference count is the MINIMUM cr value over all files for that format and rank": 233 (single file).
9. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": met. Rank 61 equals the live best; it does not lower the rank.

Limits: the checker establishes correctness and the count for this object under the stated convention; I did not search for hidden lower counts beyond the named sources, and the scheme itself (rank 61) is not new.

## Verdicts
Full criterion: met on every clause checkable from these sources. Not a rank claim, genuinely below the single live reduced reference (233), no lower published count at Lille or COVERAGE.md.
p1 is about 3x3x3 rank 23, not this format, so the enumerated partial wins p1, p2 and p3 as written are not what this claim is (p3 needs three formats). The task's p1 (strictly fewer than Perminov's live 4x4x5 count, same convention) is met: 222 is less than 233.

p1: true
confirmed_scope: The program claim/object/4x4x5_m61_cr222_ZT_reduced.json (sha256 df14df3c1a01189e540ab5a0eedebc331cd08e12714d795df0884481da292366) is a ternary straight-line program that, with its 61 products identical to those of Perminov's 4x4x5_m61_cr233 scheme (rank 61, the best rank in fmm_sota.json), computes the 4x4 by 4x5 product exactly over Z (full tensor identity and random integer evaluation, all expanded forms in {-1,0,1}) using 222 additions under Perminov's reduced convention (U 59, V 61, W 102), below his single live reduced file's 233 and below any count on the Lille 4x4x5 page (none cited) or in COVERAGE.md (+455 naive); it does not lower the rank and I judged no novelty beyond these sources.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
