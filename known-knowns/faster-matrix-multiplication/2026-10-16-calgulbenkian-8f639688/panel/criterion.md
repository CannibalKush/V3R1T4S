# Criterion skeptic report: add-4x5x8-cr470

Object: claim/object/4x5x8_m118_cr470_ZT_reduced.json, sha256 8f63968828f21bb5d9ac3954a4424a742a68f22c641afbd4c507d26d3f7e3a2f (matches claim.SHA256SUMS; I re-hashed it). Fetches were made 2026-10-15 about 22:30 UTC, one each, curl with the stated User-Agent, no retries (the first tree request failed locally on shell globbing before any request was sent; it was then fetched once, quoted).

My checker is criterion_ws/chk.py, written before opening the author's scripts (which I did not read). It uses pure Python with exact integers (no numpy available).

## Own checker output on the claim object

```
{'r': 118, 'tensor_exact': True, 'random_eval': True, 'ternary_all': True,
 'U': {'fresh': 102, 'final': 0}, 'V': {'fresh': 146, 'final': 0},
 'W': {'fresh': 152, 'final': 70}, 'total': 470}
```

- Straight-line order: every term index is below the number of already-computed quantities (asserted for every fresh and final form); every coefficient is +1 or -1 (asserted).
- Expansion: all fresh variables and all final forms were expanded to integer forms over the inputs. Every expanded coefficient is in {-1,0,1} for U, V and W (ternary_all True), so no non-ternary intermediate exists.
- Tensor identity: the sum over the 118 products of U[r][a] V[r][b] W[c][r] equals the 4x5 by 5x8 matrix-multiplication tensor exactly, with output index c = k*4+i for C[i][k] (the C-transposed layout). 30 random integer matrix pairs also give C = A*B on all 32 entries.
- Count (sum of terms-1 over every fresh and final form, negation free): U 102, V 146, W 222 (152 fresh + 70 final); total 470, equal to the file's own complexity.reduced field.

## Calibration on Perminov's file

File 4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json, sha256 7a273fbb34339b6123e5e9253fb088af12c8f11362e46cfe0789b2c3bd9e3860 (matches the hash in the author's record). My counter gives 513 (U 111, V 166, W 236), tensor exact, ternary throughout. Its expanded U, V, W rows are identical to the claim's, row for row and in order (the 118 products are the same). No map's program is shared: u_fresh, u, v_fresh, v, w_fresh and w all differ from his. So the claim is a new straight-line program for his scheme, with 9 fewer U, 20 fewer V and 14 fewer W additions.

## Null models (all rejected)

- Flipped one sign in a W output: tensor_exact False, random_eval False.
- Dropped a term in a V fresh form: tensor_exact False, random_eval False (count 469).
- Swapped two U product factors: tensor_exact False, random_eval False.
- Forward reference to a not-yet-computed quantity: rejected by the straight-line assertion.
- Coefficient 2 on a term: rejected by the +/-1 assertion.
- Duplicated term making an expanded coefficient 2: ternary_all False and tensor_exact False.
- The unmodified object passes all checks, so the checker is not rejecting everything.

## Clauses

1. "format n,m,p with max(n,m,p) <= 8 and rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)". Met. The fetched fmm_sota.json has the single entry format [4,5,8], rank 118; max dim 8; the object has rank 118.
2. "(1) verified symbolically to compute the full product A*B exactly over Z". Met: exact tensor identity over the integers plus random evaluation (see above). The identity check is symbolic in effect, because it is exact equality of the full coefficient tensor.
3. "(2) STRICTLY LESS than the smallest reduced addition count for that format and rank in Perminov's live repository ... MINIMUM cr over all files". Met. The live git tree (truncated False) holds exactly one addition_reduced_ZT file for 4x5x8 (or any permutation of it) at rank 118: cr513. Minimum cr is 513; 470 < 513. Perminov's reduced_known.json, README and CHANGELOG were not re-fetched by me (outside the brief's fetch list); the author's record states no lower count there, and the only lower-count source I could check is the tree, which shows none. This is a limit of my evidence.
4. "counted under Perminov's 'reduced' convention (each binary +/- counts one; negation free; no other scalar)". Met: my counter gives 513 on his file, matching his cr value, and 470 on the claim.
5. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant". Met (vacuously). The live page 4x5x8.html lists rank 118, cites Perminov's repository (February 2026) as source, and gives no complexity variant, operation count or Commentaries section; only maple encodings are linked. There is nothing to be below.
6. "and in matmulcatalog's live COVERAGE.md 'adds' column". Met. The row for the 4x5x8 format shows 118 with Dronperminov-ZT and "+1521". That is the naive count nz(U)+nz(V)+nz(W)-2r-np, which equals Perminov's cn1521 and is a different convention (no sharing of subexpressions). 470 < 1521 anyway, and no lower count is published there.
7. Naive files. The directory naive_addition_reduced_ZT holds 4x5x8 files named c1463 and c1521 (no "cr"). They use the naive convention, not the reduced one, and are in a different directory from addition_reduced_ZT, so they do not set the reduced reference. 470 is below both numbers regardless.
8. "If the Lille rank for the format is attained only with non-ternary coefficients ...". Not triggered: Perminov's scheme is ternary over Z (z2 False) and the candidate is ternary.
9. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target". Met: rank 118 equals the live best rank and is not lowered.

## Verdicts

Full criterion: met on every clause I could check from the named sources, with the caveat in clause 3. The win is genuine and non-subsumed: it beats the only live reduced count (513) by 43, using the same products as Perminov's scheme. It is a program-level improvement, not a new scheme; the criterion asks only for a lower SLP count at the best rank.

Enumerated partial win p1 as written in the bank is the rank-23 3x3x3 SLP below 58. The claim is not that. Under the brief's reading of p1 (strictly fewer than Perminov's live 4x5x8 count under the same convention), the claim meets it (470 < 513); the full criterion is met as well, so p1 adds nothing beyond the full verdict.

confirmed_scope: The program in claim/object/4x5x8_m118_cr470_ZT_reduced.json (sha256 8f63968828f21bb5d9ac3954a4424a742a68f22c641afbd4c507d26d3f7e3a2f) is a ternary straight-line program that computes the 4x5 by 5x8 integer matrix product exactly with Perminov's 118 products, using 470 additions under the reduced convention (U 102, V 146, W 222), against 513 for his only live addition_reduced_ZT file for that format and rank, with the Lille page citing no count and COVERAGE.md giving only a naive 1521.

context: Claude Code subagent (Fable 5.1), fresh context

p1: true
pass: true
