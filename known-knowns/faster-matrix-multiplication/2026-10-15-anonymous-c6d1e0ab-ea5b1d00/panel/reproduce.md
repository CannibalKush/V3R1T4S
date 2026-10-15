# Independent reproduction skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object passes the offline reproduction checks: exact integer matrix multiplication, ternary expanded forms, valid straight-line order, 130 nonzero used products, 502 reduced additions, the object hash, and deterministic results. This verdict is limited to the saved object, as directed by the panel instructions.

## Scope and independence

I read `CLAIM.md`, the object, `INDEX.csv`, and `table-record/README.md`, then wrote `skeptic/definition.txt` and my standard-library checker `skeptic/check_slp.py` without reading `verify-it-yourself/`. I ran the independent checker and saved its output before opening or running the author's code. The initial checker and its output are preserved as `skeptic/check_initial.py` and `skeptic/output_initial.txt`. No network was used, and no material outside this package was read; the optional symbolic check used the Python interpreter explicitly supplied in the task.

The third-party reference scheme is deliberately absent. `table-record/README.md` identifies it as `5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json`, gives its source URL, and records SHA-256 `8f899e560b2d2976b031272c59ebf6ea0472ae2d9616eaeb05d52027d818344f`. Without its bytes and without network I cannot recount its additions, validate that hash, or compare its expanded products with this object's. The other recorded source hashes likewise cannot be validated against absent source bytes. The live rank, minimum reference count, Lille and catalogue comparisons, novelty, and uniqueness of the claim are outside this verdict. In particular, 562 is recorded metadata here; I confirm the arithmetic inequality 502 less than 562, not the provenance or currency of 562. No reference recount is claimed.

## Quoted definition and criterion

The following is the entire success criterion from `CLAIM.md`. Its format placeholder uses braces in place of angle brackets; nothing else in the quote was changed. The panel's Lille URL template is rendered as `https://fmm.univ-lille.fr/{n}x{m}x{p}.html`; I changed only the template brackets.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The saved-object definition, including the counting convention and layout, is:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

The bank's verification method is:

> Parse the SLP (sequence of assignments t_k = +/- t_i +/- t_j over inputs A_ij, B_jl, intermediate sums, r products, and output assignments). Evaluate it with sympy (or exact integer evaluation at many random integer matrices plus one symbolic pass) and confirm every output equals the corresponding entry of A*B. Count the additions under the stated convention (exclude negations, exclude the r multiplications). Load the reference scheme from Perminov's addition_reduced_ZT directory (and reduced_known.json), recount its additions with the same counter to calibrate the convention, and compare. Re-fetch the repository, the Lille page and COVERAGE.md. Minutes on this Mac.

All saved-object clauses of these definitions are checked below. The externally sourced comparison and calibration clauses are scoped out explicitly above, following this panel's offline instructions.

## Independent derivation and properties checked

1. **Dimensions, products, domain, and schema.** Strict JSON parsing rejects duplicate keys. The dimensions are exactly 5 by 6 by 6, hence maximum dimension 6 is at most 8; `m` is the integer 130 and `z2` is false. U and V each have exactly 130 factors; W has exactly 30 outputs. Every factor is nonzero, and every product is used by at least one expanded output. This checks a scheme with 130 products, rather than proving a lower bound on tensor rank.

2. **Straight-line order and allowed operations.** Start U with the 30 row-major A basis vectors, V with the 36 row-major B basis vectors, and W with the 130 formal product basis vectors. At fresh step k, admit only indices strictly below the number of inputs plus k. Finals may refer only to the map's inputs and fresh variables. Every listed form is nonempty, every index is a genuine integer, and every listed scalar is exactly integer +1 or -1. Thus there are no forward references, cycles, other scalar multiplications, or products inside a linear map.

3. **Expanded ternarity.** Inductively replace each referenced quantity by its previously expanded integer basis vector and add its signed coefficients. Check every coefficient of every fresh and final form is in {-1, 0, 1}, including unused intermediates. This covers 129 + 147 + 85 = 361 fresh forms and 130 + 130 + 30 = 290 final forms, 651 forms in total. The maximum absolute coefficient is 1 in each map.

4. **Binary realization.** For each multi-term sum, a deterministic search over prefix subsets finds a term permutation for which every binary partial sum is ternary. A separate loop validates that the witness uses every term exactly once, that every prefix is ternary, and that the final sum equals the expanded stored form. This adds no operations beyond length minus one. All witnesses are saved in `skeptic/binary_orders.json`. The one ordering qualification is explained below.

5. **Complete tensor identity over Z.** Let U[t,a], V[t,b], and W[c,t] be the expanded integer coefficients. By induction through the ordered forms, output c is exactly the sum over t of W[c,t] times (the sum over a of U[t,a] A[a]) times (the sum over b of V[t,b] B[b]). Therefore the coefficient of each monomial A[a]B[b] is the integer sum over all 130 t of W[c,t]U[t,a]V[t,b]. My checker constructs that entire coefficient array and compares all 30 times 30 times 36 = 32,400 entries, including every expected zero. For c = k*5+i, the expected coefficient is 1 precisely when a = i*6+j and b = j*6+k for a common j; otherwise it is 0. All entries agree: there are 180 coefficients equal to 1 and 32,220 zeros. There are no constant, linear, A*A, or B*B terms by the bilinear construction. This proves every output is the required entry of A*B for every integer input; it is not a sample or randomized substitute for the symbolic proof.

6. **Counts.** A form of L signed, already available quantities requires L-1 binary additions/subtractions; signs are free. Sum over all fresh and final forms, including the factor forms and output forms. U costs 129, V costs 147, and W costs 226, so the total is 502. Equivalently there are 1,153 listed terms in 651 forms, yielding 1,153 - 651 = 502. The 130 bilinear multiplications are excluded exactly as specified. The independently expanded maps also give naive count 1,716. Both counts agree with the object's `complexity` metadata; 502 also agrees with `INDEX.csv` and the object filename. The saved numerical comparison is 502 less than 562 by 60.

7. **Hash and determinism.** The object's actual SHA-256 matches `INDEX.csv`. Each invocation parses and verifies twice from unchanged bytes and compares all derived results and binary witnesses. Independent subprocess runs, including `PYTHONHASHSEED=1` and `PYTHONHASHSEED=2`, give byte-identical output. The author's main checker also gives identical output on repetition. No search over schemes, optimality assertion, or exhaustive-search result is being inferred from a sample: the exhaustive check here is the full tensor identity.

8. **Checker controls.** Seven deliberate in-memory corruptions are rejected for their expected reasons, including a changed product sign that reaches the tensor comparison, a self-reference, scalar 2, a nonternary unused intermediate, a false count, a missing factor, and the wrong coefficient-domain flag. These controls never modify the saved object.

## Exact independent command and real output

Run from this folder with the system `python3` (standard library only):

```sh
python3 skeptic/check_slp.py object/5x6x6_m130_cr502_ZT_reduced.json > skeptic/output.txt 2>&1
```

Exit code: 0. The following is pasted directly from `skeptic/output.txt`:

```text
Independent checker: exact integer arithmetic; no author imports; no random sampling
Object: object/5x6x6_m130_cr502_ZT_reduced.json
SHA-256: ea5b1d00e3702536a57a8598f0f09040f99b503e844d5018556128ac81d0a097 (matches INDEX.csv)
Format: 5x6x6; maximum dimension: 6 <= 8; products: 130
Schema, integer coefficient domain, nonzero product factors, and use of all products: PASS
U: inputs=30; fresh=129; final=130; terms=388; additions=129; max_abs=1; binary_prefixes=388
V: inputs=36; fresh=147; final=130; terms=424; additions=147; max_abs=1; binary_prefixes=424
W: inputs=130; fresh=85; final=30; terms=341; additions=226; max_abs=1; binary_prefixes=341
Straight-line references, +/-1 terms, every expanded form, and every binary partial sum: PASS
Binary lowering: deterministic term permutations, verified ternary at each prefix, no extra additions
Forms whose listed left-to-right order needs a ternary permutation: 1
  W.fresh[83]: zero-based term order 0,1,3,2,4,5
Full tensor identity: 32400 integer coefficients checked; 180 nonzero; 0 mismatches
Output layout: output k*5+i = C[i][k]; expected sum over all 6 inner indices: PASS
Reduced additions: 502 = object metadata = INDEX.csv value
Naive additions: 1716 = object metadata
Saved reference comparison: 502 < 562; difference 60 (reference not recounted)
Expanded U,V,W SHA-256: efb28fc6b28e56b85b1c3ee46ce9c6af70bdc033a7c1e6e4e16e77430b540233
Full tensor SHA-256: b4d106bc56754eae8f47a6e49fa9934f4fc03d2d8599844855e215d31dd4dbc0
Two fresh parses and full verifications with unchanged object bytes: identical
Binary lowering witnesses: skeptic/binary_orders.json
Offline scope: live tables, missing reference hashes/recount, and identity with reference products unverified
PASS: all saved-object properties checked
```

Repetition commands, each producing the same bytes as `skeptic/output.txt`:

```sh
python3 skeptic/check_slp.py object/5x6x6_m130_cr502_ZT_reduced.json > skeptic/output_repeat.txt 2>&1
PYTHONHASHSEED=1 python3 skeptic/check_slp.py object/5x6x6_m130_cr502_ZT_reduced.json > skeptic/output_seed1.txt 2>&1
PYTHONHASHSEED=2 python3 skeptic/check_slp.py object/5x6x6_m130_cr502_ZT_reduced.json > skeptic/output_seed2.txt 2>&1
cmp skeptic/output.txt skeptic/output_repeat.txt
cmp skeptic/output.txt skeptic/output_seed1.txt
cmp skeptic/output.txt skeptic/output_seed2.txt
```

The comparison commands returned 0 and produced no output. The shared output SHA-256 is `af3c0a92294ddd6fc8d6497321274f3d0873f4cf821cb1c14084a1ff199bcdc0`.

The control command and its real output are:

```sh
python3 skeptic/control_checks.py > skeptic/control_output.txt 2>&1
```

Exit code: 0.

```text
Wrong product sign: rejected (tensor mismatch output=5, A=0, B=1: -1 != 1)
Self reference: rejected (U.fresh[0]: unavailable reference)
Forbidden scalar: rejected (U.fresh[0]: invalid scalar)
Nonternary unused intermediate: rejected (U.fresh[129]: nonternary expansion)
Wrong claimed count: rejected (reduced count mismatch)
Missing product factor: rejected (U: wrong number of final forms)
Wrong coefficient domain: rejected (object is not declared over Z)
PASS: all 7 deliberate corruptions rejected for the expected reason
```

## Initial finding and interpretation

The initial independent checker imposed an extra restriction: accumulate the listed terms in their serialized left-to-right order while requiring every binary prefix to be ternary. Its real output, preserved in `skeptic/output_initial.txt`, was:

```text
FAIL: ValueError: W.fresh[83]: nonternary binary partial sum
```

In `w_fresh[83]`, the first three listed terms yield coefficient 2 on formal product 35. The full stored form is nevertheless ternary. The quoted saved-object definition defines a form as a sum and does not prescribe binary association or term order. Requiring the serialized left fold was therefore stronger than the definition. The corrected checker still checks every full expanded form, and additionally supplies a valid binary ordering with zero-based term positions 0,1,3,2,4,5. Every prefix in that order is ternary, and the six terms require exactly five additions. Only this one form requires reordering for ternary binary prefixes. The object bytes were never changed. This is an evaluation-order qualification, not a failure of any property defined for the saved forms or of the claimed addition count.

## Author comparison, performed afterward

After the independent checker passed, I read `REPRODUCE.md` and `verify-it-yourself/`. I ran the author's checker directly:

```sh
python3 verify-it-yourself/check_slp.py object/5x6x6_m130_cr502_ZT_reduced.json > skeptic/author_output.txt 2>&1
```

Exit code: 0. Real output:

```text
{"file": "5x6x6_m130_cr502_ZT_reduced.json", "format": "5x6x6", "rank": 130, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 129, "adds_V": 147, "adds_W": 226, "adds_total": 502, "naive_total": 1716, "declared_reduced": 502, "VALID": true}
```

The author's results agree on 130 products, the transposed C layout, exactness, the U/V/W addition breakdown, 502 total, and 1,716 naive additions. Its 20 seeded random evaluations are additional spot checks; my pass relies on the exhaustive coefficient identity above. Repeating this command into `skeptic/author_output_repeat.txt` gave identical bytes.

There is a limitation in the author's implementation: despite the description in `REPRODUCE.md` and the run script, `check_slp.py` validates listed term signs but does not assert that the expanded fresh and final coefficients are ternary. Its `VALID` flag also does not itself enforce the declared count. The run script checks total 502 separately. My independent checker explicitly enforces both properties, so this omission does not leave either property unchecked for this object. There is no numerical disagreement between the checkers.

For the optional symbolic cross-check, `SKEPTIC_SYMPY_PYTHON` was set to the interpreter supplied in the task; that interpreter location is intentionally not written as an absolute path in this report. System `python3` does not have SymPy. The exact invocation after setting that variable was:

```sh
"$SKEPTIC_SYMPY_PYTHON" verify-it-yourself/sym_check.py object/5x6x6_m130_cr502_ZT_reduced.json > skeptic/author_symbolic_output.txt 2>&1
```

Exit code: 0. Real output:

```text
{"file": "5x6x6_m130_cr502_ZT_reduced.json", "format": "5x6x6", "rank": 130, "products": 130, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 502}
```

Here `C=AB: false` tests the alternate row-major flattening; `C^T: true` is the transposed flattening explicitly specified by `CLAIM.md`, so this is expected and is not a mismatch.

## Verdict

All properties of the saved object within the requested offline scope are confirmed. There is no mismatch in exactness, expanded ternarity, straight-line order, product count, addition counts, object hash, or repeatability. The omitted third-party reference and live comparisons remain for the other skeptics, as directed; this report makes no claim about the current table value, newness, or identity with the reference products.

pass: true
