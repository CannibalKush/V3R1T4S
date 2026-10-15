# REPRODUCE skeptic: 5x5x5_m93_cr358_ZT_reduced.json

(Saved verbatim by the run's main session from the subagent's returned text; subagents in this harness return
findings as text instead of writing files. ../work/ refers to the skeptic's own isolated scratch folder.)

## Claim under test (CLAIM.md)
`5x5x5_m93_cr358_ZT_reduced.json` is a ternary ({-1,0,1}) straight-line program computing <5,5,5> exactly over Z with 93 multiplications and 358 additions/subtractions under Perminov's 'reduced' convention. The reference minimum is 383 (`reference/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json`).

## Definition relied on (sources/perminov_README.md, quoted exactly)
Full format, which the reduced format inherits for `n`, `m`, `z2`:
- l.572 "* `u` (machine-readable) - matrix encoding the linear form of `A`, size `m × (n₁·n₂)`;"
- l.573 "* `v` (machine-readable) - matrix encoding the linear form of `B`, size `m × (n₂·n₃)`;"
- l.574 "* `w` (machine-readable) - matrix encoding the linear form of `Cᵀ`, size `m × (n₃·n₁)`;"
- Row-major flattening, from the l.588 example: "m2 = (a12 - a22) * (b21 + b22)" with u row "[0, 1, 0, -1]". This puts a12 at index 1, so a_{ij} is at index i*n2+j.
- C^T index order, from the full example: w column 1 = m6+m7 = "c21 = m6 + m7". This puts c_{il} at row l*n1+i.

Reduced format:
- l.652 "* `n`, `m`, `z2` - these fields have the same meaning as in the full scheme format"
- l.656 "* `reduced` - number of additions after elimination of common subexpressions and simplification."
- l.665 "[{ "index": i, "value": c }, ...]"
- l.670 "* For `U`: original indices: `0 ... n₁·n₂ - 1`, fresh indices start from: n1·n2;"
- l.671 "* For `V`: original indices: `0 ... n₂·n₃ - 1`, fresh indices start from: n2·n3;"
- l.672 "* For `W`: original indices: `0 ... m - 1`, fresh indices start from: m."
- l.679 "`u` and `v` arrays have exactly `m` rows each, `w` have `n₃·n₁` rows, and each row represents a sparse linear form:"
- l.686 "Reduced `(2, 2, 2: 7)` from 24 to 15 additions:" (worked example used for calibration)

Counting convention (CLAIM.md / success criterion): "each binary +/- between already-computed quantities counts one; multiplication by -1 is free". So a form with t terms costs t-1.

## Method
I wrote `../work/my_check.py` from the definition above, before I opened `author_checker_fmm_check.py`. It does the following:
- **Strict parse:**
  - Top-level keys must be exactly the README set.
  - `z2` must be false.
  - Every term must be `{index, value}` with integer (non-bool) fields and value in {-1,+1}.
  - It rejects empty forms, duplicate indices within a form, and indices outside [0, base + (number of earlier fresh)). This rejects self and forward references.
  - It requires exactly m `u` rows, m `v` rows and n3*n1 `w` rows.
- **Expansion:** every fresh form and every final form is expanded to dense integer vectors over the original variables (A entries, B entries, products). Every expanded coefficient must be in {-1,0,1}, and no form may expand to zero.
- **Exactness:** it checks the full tensor identity over Z on all 25*25*25 = 15625 index triples:
  `sum_k U[k][i*n2+j] * V[k][j'*n3+l] * W[l'*n1+i'][k] = [j=j'][l=l'][i=i']`, with w read as C^T.
  As a diagnostic it also counts mismatches when w is read as plain C.
- **Count:** the sum over all fresh and final forms of (terms - 1).
- **Calibration:**
  - The README 2x2x2 example (z2 forced to false so it parses) gives count 15, matching its stated 15. The example is a Z2 scheme, so I checked it mod 2: 0 mismatches under C^T, 8 under C. This confirms the C^T reading.
  - The reference gives 383, matching its stated complexity.reduced.
- **Other checks:**
  - sha256 against CLAIM_SHA256.txt.
  - Two runs, compared byte-for-byte.
  - 16 mutants.
  - Direct execution of the SLP on random integers (`../work/slp_exec.py`). This is only a supplementary spot check; the exact proof is the tensor identity.
  - Inlining all single-term fresh forms (`../work/inline_singletons.py`), then rechecking.
  - Then the author's checker, run exactly as REPRODUCE.md says (with the workspace venv python).

## Real outputs

sha256 (`sha256sum`), matching CLAIM_SHA256.txt exactly:
```
71fa63deb8df8c92975304438d449e61cd92b777fcd2bec9cb2090c01e129f5c *5x5x5_m93_cr358_ZT_reduced.json
808285b8fb393d2e950ecff4ffe9881a209b6d3eff0d787e34d801a3f22293da *reference/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json
```

My checker (calibration + object):
```
{"cost_u_v_w": [4, 4, 7], "exact_over_Z": false, "file": "readme_example_z2false.json", "format": "2x2x2", ..., "reduced_additions": 15, "stated_complexity": {"naive": 24, "reduced": 15}, ...}
   (README example is a Z2 scheme; mod-2 check: "CT mod2 mismatches 0", "C mod2 mismatches 8")
{"cost_u_v_w": [103, 105, 175], "exact_over_Z": true, "file": "5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json", "format": "5x5x5", "fresh_counts": [49, 43, 68], "m": 93, "products_used_by_outputs": 93, "reduced_additions": 383, "sha256": "808285b8...93da", "stated_complexity": {"naive": 843, "reduced": 383}, "tensor_mismatches_CT": 0, "tensor_mismatches_if_W_were_C": 200, "ternary_all_forms": true, "triples_checked": 15625, "u_rows": 93, "v_rows": 93, "w_rows": 25}
{"cost_u_v_w": [98, 96, 164], "exact_over_Z": true, "file": "5x5x5_m93_cr358_ZT_reduced.json", "format": "5x5x5", "fresh_counts": [98, 96, 96], "m": 93, "products_used_by_outputs": 93, "reduced_additions": 358, "sha256": "71fa63de...9f5c", "stated_complexity": {"naive": 843, "reduced": 358}, "tensor_mismatches_CT": 0, "tensor_mismatches_if_W_were_C": 200, "ternary_all_forms": true, "triples_checked": 15625, "u_rows": 93, "v_rows": 93, "w_rows": 25}
```

Determinism: two runs on object + reference, both rc=0:
```
e0d9837c318bf463efe911635f91702b483c959432fb985ebdddf0eb04c52abe *work/run1.txt
e0d9837c318bf463efe911635f91702b483c959432fb985ebdddf0eb04c52abe *work/run2.txt
IDENTICAL
```

Mutants, all 16 rejected by my checker (either REJECT or exact=False):
```
bool_value.json REJECT: u[1]: non-integer term {'index': 75, 'value': True}
cancel_to_zero_vfresh.json REJECT: v_fresh[96]: duplicate index 0
coef_0_v0.json REJECT: v[0]: coefficient 0 not in {-1,1}
coef_2_u0.json REJECT: u[0]: coefficient 2 not in {-1,1}
drop_term_w3.json exact=False mism=1 adds=357
drop_u_row.json REJECT: u: 92 final rows, expected 93
drop_w_row.json REJECT: w: 24 final rows, expected 25
dup_index_u_fresh0.json REJECT: u_fresh[0]: duplicate index 8
empty_w_fresh0.json REJECT: w_fresh[0]: empty form
expanded_coef_2_ufresh.json REJECT: u_fresh[99]: expanded coefficient outside {-1,0,1}
flip_sign_w0.json REJECT: w[0]: expanded coefficient outside {-1,0,1}
forward_ref_u_fresh3.json REJECT: u_fresh[3]: index 75 out of range [0,28) (forward/self/out-of-range ref)
self_ref_v_fresh5.json REJECT: v_fresh[5]: index 30 out of range [0,30) (forward/self/out-of-range ref)
swap_two_w_rows.json exact=False mism=20 adds=358
z2_true.json REJECT: z2 is not false (not an integer scheme)
zero_expansion_ufresh.json REJECT: u_fresh[99]: expands to zero form
```

Direct SLP execution (5 random integer pairs in [-10^6, 10^6], seed 12345; supplementary only):
```
trial 0..4: C^T-ordered output == A*B: True, ops executed: 358 (each trial)
u_fresh term-count histogram: {2: 98}
v_fresh term-count histogram: {2: 96}
w_fresh term-count histogram: {1: 48, 2: 28, 3: 9, 4: 8, 5: 3}
u term-count histogram: {1: 93}
v term-count histogram: {1: 93}
w term-count histogram: {2: 5, 3: 5, 4: 4, 5: 6, 6: 2, 7: 1, 8: 1, 9: 1}
```

The object has 48 single-term w_fresh forms. These are aliases or negations: 28 with value +1 and 20 with value -1, referenced 96 times in total. The reference has none.

To make sure these free forms do not hide any cost, I inlined all of them. This substitutes sign*variable into every referencing form. I then reran my checker on the result:
```
fresh counts after inlining: 98 96 48
{"cost_u_v_w": [98, 96, 164], "exact_over_Z": true, ..., "reduced_additions": 358, "tensor_mismatches_CT": 0, ...}
```
After inlining there are no duplicate indices, no non-ternary coefficients and the count is still 358. The aliases are cost-neutral, so the 358 does not depend on the free single-term forms.

Author's checker, as REPRODUCE.md says: `python -X utf8 author_checker_fmm_check.py 5x5x5_m93_cr358_ZT_reduced.json reference/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json`. I ran it twice and the outputs were IDENTICAL:
```
{"format": "5x5x5", "rank": 93, "adds_U": 98, "adds_V": 96, "adds_W": 164, "reduced_additions": 358, "nonternary_coeffs": [], "exact_over_Z": true, "valid_ternary_slp": true, "stated_reduced": 358, "count_matches_stated": true, "error": null, "file": "5x5x5_m93_cr358_ZT_reduced.json"}
{"format": "5x5x5", "rank": 93, "adds_U": 103, "adds_V": 105, "adds_W": 175, "reduced_additions": 383, "nonternary_coeffs": [], "exact_over_Z": true, "valid_ternary_slp": true, "stated_reduced": 383, "count_matches_stated": true, "error": null, "file": "5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json"}
```
This matches my checker on every field: per-matrix costs 98/96/164 and 103/105/175, totals 358 and 383, exact and ternary.

## Saved-source consistency (snapshot only; I had no network, so I could not re-check live)
- **sources/FETCH_LOG.md:** all 7 saved files' sha256 match their logged hashes.
- **fmm_sota.json:** the entry is `{'format': [5, 5, 5], 'rank': 93, ...}`, so 93 is the best listed rank.
- **perminov_tree.json** (truncated: False): the only file in `addition_reduced_ZT` for 5x5x5 is `5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json`. The minimum reference is therefore 383, and it equals the reference copy.
- **reduced_known.json:** no 5x5x5 entry.
- **README / CHANGELOG:** no 5x5x5 reduced count. The only README 5x5x5 line is the rank table row "93 | 93 | 93".
- **matmul_COVERAGE.md:** the <5,5,5> row shows adds "+846".
- **lille_5x5x5.html:** gives <5x5x5:93> (Moosbauer-Poole) and cites no addition-count variant.
- **Conclusion:** 358 < 383 and 358 < 846.
- **Rank:** all 93 products are used by the outputs, so this is not a hidden rank-92 scheme.

## Discrepancies
- **Author's checker ignores the `z2` field.** My `z2_true` mutant was accepted by it with exact=True, ternary=True, adds=358. My checker rejects it. This does not affect the claimed object, which has `"z2": false`, and both checkers agree on the object and the reference.
- **Mutant classification differs, but the outcome does not.** For the `coef_2_u0`, `coef_0_v0`, `flip_sign_w0` and `expanded_coef_2_ufresh` mutants, the author's checker reports valid_ternary_slp=false, or an error/exact=false, where mine REJECTs. Every mutant is non-passing in both checkers.
- **No mismatch on the claimed object or the reference** between the definition, my checker and the author's checker.

## Verdict
- **Exact:** yes. Full tensor identity over Z, 15625/15625 triples, with w read as C^T per the README.
- **Ternary:** yes. Every raw coefficient is ±1 and every expanded fresh and final form is in {-1,0,1}.
- **Rank:** 93. That is 93 u rows, 93 v rows and 25 w rows, with all 93 products used; 93 equals the fmm_sota.json best.
- **Count:** 358. This matches the stated complexity.reduced and the author's checker. My counter is calibrated on the README example (15) and on the reference (383).
- **Integrity and determinism:** the sha256 values match, both checkers are deterministic, and all 16 mutants are rejected.

context: Claude Code Agent-tool subagent, model claude-opus-5-5, effort high, saw only a copy of claim/
pass: true
