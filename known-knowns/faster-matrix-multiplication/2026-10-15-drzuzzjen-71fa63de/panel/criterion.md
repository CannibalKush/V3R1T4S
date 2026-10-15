# Criterion skeptic verdict: r1520 (5x5x5, rank 93, 358 reduced additions)

(Saved verbatim by the run's main session from the subagent's returned text; subagents in this harness return
findings as text instead of writing files. work/ refers to the skeptic's own isolated scratch folder.)

Scope I saw: only a copy of claim/ (CLAIM.md, REPRODUCE.md, the object, reference/, sources/, author checker). I wrote my own checkers in work/ (check.py, nullmodel.py, convention.py, numeric.py) before running the author's checker. I had no network, so the "live" clauses rest on the saved fetches and their hashes.

## Integrity of inputs
- `sha256sum` of the object is 71fa63de...129f5c and of the reference copy is 808285b8...93da. Both match CLAIM_SHA256.txt.
- `sha256sum` of every file in sources/ matches the FETCH_LOG.md hashes: tree 71f2669d, README 7b0761ec, CHANGELOG 07fbb324, reduced_known ef67c137, fmm_sota d0da2c36, COVERAGE c2a9bd92, lille 3daec22a.
- The git blob sha1 of the reference copy is c71013fca406e0d2d7936fc53a42197179a9a8e5. It equals the tree entry for `schemes/results/addition_reduced_ZT/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json` (size 24492), so the reference is byte-identical to Perminov's file at tree f0efd4f6.
- FETCH_LOG also lists `v3r1t4s_open_prs.json`, but that file is not in my copy. It does not bear on this criterion.

## Clause-by-clause

1. **Explicit SLP (linear forms over the inputs, r products, linear forms producing the outputs): PASS.**
   - The object is in Perminov's reduced layout:
     - u_fresh: 98 forms, all 2 terms. u: 93 forms, all 1 term.
     - v_fresh: 96 forms, all 2 terms. v: 93 forms, all 1 term.
     - w_fresh: 96 forms. w: 25 output forms.
   - Every coefficient is an int in {-1, 1}. There are no forward references, no duplicate operands in a form, no out-of-range indices and no unused fresh variables (my check.py reports `issues` only of type "short-form", covered under clause 6).
   - Executing it literally (numeric.py) performs exactly 358 binary operations and 93 products.

2. **max(n,m,p) <= 8: PASS.** n = [5,5,5].

3. **Rank equals the fmm_sota.json best for the sorted format: PASS.**
   - fmm_sota.json (createdAt 2026-10-09T11:45:48, 5456 entries) has exactly one 5x5x5 entry: `[{'format': [5, 5, 5], 'rank': 93, 'exponent': 2.816262}]`. The object has m = 93.
   - The Lille page agrees: "⟨5×5×5:93⟩", from Moosbauer–Poole 2025.

4. **Exact over Z: PASS.**
   - Symbolic check (check.py): I expanded every fresh variable and every final form to base variables, then formed sum_k W[r][k]·U_k⊗V_k. Result: `"ok": {"CT": true, "C": false}`. That is exact equality with the ⟨5,5,5⟩ tensor in the C^T output layout, which the README specifies ("matrix encoding the linear form of `Cᵀ`").
   - Numeric check (numeric.py): 200 random integer trials with entries up to ±10^6, executing the SLP step by step, all equal to C^T.
   - z2 = false.

5. **Count strictly below the MINIMUM cr over ALL addition_reduced_ZT files for format and rank: PASS.**
   - The tree is complete (`truncated: False`, 6637 entries). Its only reduced-type directories are `schemes/results/addition_reduced_ZT` and `naive_addition_reduced_ZT`.
   - The only addition_reduced_ZT file for 5x5x5 is `5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json`. The only 5x5x5 ranks in the whole tree are [93, 98]. So the minimum cr is 383.
   - My recount of the reference gives 103+105+175 = 383, equal to its stated complexity.reduced.
   - My recount of the object gives cu=98, cv=96, cw=164, total = 358. 358 < 383.

6. **Perminov's reduced convention: PASS, with one note.**
   - Each form costs (terms − 1), which reproduces the README's (2,2,2:7) example (15).
   - Single-term w_fresh entries: 48 in total, 20 negations and 28 aliases. 8 of them point at another fresh variable. Each costs 0, which is allowed because negation is free and an alias is no operation.
   - Null check on those (convention.py): I inlined all single-term fresh variables. The w count stays 164, with 0 forms in which operands merge as duplicates. So the zero-cost entries hide no work.
   - Cancelling intermediates: 17 u, 19 v and 4 w fresh variables have expansions that involve cancellation. Every expanded intermediate and final form still has coefficients in {-1,0,1}: no "nonternary-expansion" was found anywhere, so every intermediate stays ternary.
   - No scalar other than ±1 appears.
   - Note: Perminov's own file uses no cancellations and no single-term fresh variables. The object relies on both. Both are allowed by the criterion's literal definition ("each binary +/- between already-computed quantities counts one; multiplication by -1 is free"), so I do not treat this as a stretch.
   - The author's checker independently agrees: adds_U 98, adds_V 96, adds_W 164, reduced_additions 358, exact_over_Z true, valid_ternary_slp true.

7. **Below reduced_known.json, README and CHANGELOG (all headings): PASS.**
   - reduced_known.json has no "5x5x5" key. Its largest format is "4x6x6-116".
   - README: the only 5x5x5 line is 1083, a rank table row (`5x5x5 | 93 | 93 | 93`). It gives no addition count. The "383" at line 1450 is a count of ZT schemes, not additions.
   - CHANGELOG: there are zero hits for 5x5x5 or "5, 5, 5" under any of its 254 heading lines, including every "Reduced additions improvement" and "Additions reducing" section.

8. **Lille cited complexity variant: PASS (nothing to beat).** The page's text has no complexity, addition or operations count and cites no complexity variant for ⟨5×5×5:93⟩. It cites only the algorithm source and the Maple files.

9. **matmulcatalog COVERAGE.md 'adds': PASS.** Row: `⟨5,5,5⟩ | ✓ 93 Alphaevolve | ... | +846`. The legend defines this as nz(U)+nz(V)+nz(W) − 2r − n·p, a naive count. 358 < 846.

10. **Coefficient-class rule: PASS / moot.**
    - Lille publishes no count, so there is nothing to compare by class.
    - The object is ternary ZT and is compared against Perminov's ZT directory, which is the same class.

11. **Not a rank target: PASS.** The rank is 93, equal to the SOTA and not below it.

12. **Live re-fetch timing: PASS on the record, not independently re-fetched.**
    - All 8 fetches are logged on 2026-10-15T15:20:24Z–15:20:28Z with HTTP 200, the same day as this review. Hashes match the saved files.
    - I could not re-fetch (no network), so whether anything changed after 15:20Z is outside my evidence.

13. **Tie or subsumption: none found.**
    - 358 vs 383 is a strict improvement of 25.
    - No source in the folder lists any count below 383 for 5x5x5 rank 93.
    - 5 is prime, so no Kronecker or product composition of smaller formats yields ⟨5,5,5⟩ at rank 93.
    - "Each scheme is claimed once": no prior-claims ledger is in my copy, so I cannot check this beyond the folder.

14. **Null model (re-reduction?): CONFIRMED re-reduction, which the criterion allows.**
    - nullmodel.py, with sign-normalised rank-one terms, gives: "distinct products obj/ref 93 93 common rank-one terms 93", "identical bilinear scheme (multiset of rank-one terms): True", nnz 1054 vs 1054, naive 843 vs 843.
    - So the object is Perminov's exact bilinear scheme (Moosbauer–Poole / AlphaEvolve family, as in the tree) with a better straight-line program for the linear maps. It is not a new scheme.
    - The criterion is about the addition count of an SLP at the SOTA rank, not about scheme novelty, so this is a genuine win of the stated kind.
    - Residual unknown: other reducers' counts for this scheme that are not in the named sources (e.g. werekorren's fmm_add_reduction) are outside the criterion's listed comparators and were not visible to me.

## Partial-win check
This is claimed as the full criterion, not p1, p2 or p3. The format is not 3x3x3 or 4x4x4, and it is a single format, so no partial win applies or is needed.

confirmed_scope: The file 5x5x5_m93_cr358_ZT_reduced.json (sha256 71fa63de…129f5c) is a ternary straight-line program that computes the 5x5x5 matrix product exactly over Z with 93 multiplications and 358 binary additions/subtractions counted under Perminov's reduced convention (negations and single-term aliases free, every intermediate ternary); it is a re-reduction of the same bilinear scheme as Perminov's 5x5x5_m93_cr383 file and strictly below 383, which is the only and hence minimum reduced count for 5x5x5 rank 93 in the Perminov sources fetched 2026-10-15T15:20Z; no lower count for this format and rank appears in reduced_known.json, the README, the CHANGELOG, the Lille 5x5x5 page or matmulcatalog COVERAGE.md (+846).
context: Claude Code Agent-tool subagent, model claude-opus-5-5, effort high, saw only a copy of claim/
pass: true
