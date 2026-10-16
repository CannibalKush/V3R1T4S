# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved object passes the reproducible mathematical and program checks. This verdict does not establish a current record, novelty, minimum tensor rank, or identity with an unavailable third-party scheme.

## Scope and order of work

I read `CLAIM.md`, the saved object data, `INDEX.csv` and `table-record/README.md`. I fixed the quoted definition in `skeptic/definition.md`, wrote `skeptic/check_slp.py` using Python's standard library, and ran it before opening `verify-it-yourself/` or `REPRODUCE.md`. I corrected the extra left-fold assumption described below and completed the successful independent run before reading or executing the author's checker. No author code is imported by the independent checker. No network was used and no other package, repository instructions or outside source material was read. The supplied environment interpreter was used only to execute the author's optional SymPy check.

The reference scheme is deliberately absent. `table-record/README.md` identifies it as https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/5x5x7_m127_cr531_fv245_cn1607_ZT_reduced.json and records SHA256 `9adf1d758482220195bcb6868c46440059153d072f9b716da58734f8ce9d064c`. Without its bytes or network access, I cannot recount it, verify that hash, or establish that its products equal the candidate's. The other external-source hashes in `table-record/README.md` are likewise metadata, not verified content. Live rank, the live minimum count, Lille, matmulcatalog, coefficient-class comparisons, and novelty belong to the other skeptics. The arithmetic 483 less than the saved comparison value 531 is checked; the provenance and currency of 531 are not independently confirmed here. Those scoped exclusions do not substitute for any check of the saved object.

## Quoted definition and criterion

The following is quoted from CLAIM.md. In generic format notation, only angle brackets have been changed to braces. The Lille URL template uses the same bracket-only substitution: https://fmm.univ-lille.fr/{n}x{m}x{p}.html.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

> `object/`: the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

Offline scope: check the saved straight-line program, every expanded form, full integer tensor identity, dimensions, product count, reduced count, metadata consistency, saved object hash and repeatability. External rank optimality, live comparison counts and identity with the absent Perminov reference are outside this review. No exhaustive search is claimed; the full tensor identity will be checked exhaustively.

## Independent proof and property checks

1. **Object, dimensions, products and hash.** Parse JSON while rejecting duplicate fields, validate its fields and integer types, require dimensions 5x5x7, maximum dimension at most 8, 127 U forms, 127 V forms, 35 W outputs and `z2: false`. Compare the raw object's SHA256, relative file name, target, cell and value with `INDEX.csv`. Each of the 127 products has nonzero left and right factors and a nonzero column in the expanded W map. This verifies 127 bilinear multiplication gates, not a lower bound proving optimal rank.
2. **Straight-line order and legal coefficients.** Start with the coordinate basis for the 25 A entries, 35 B entries and 127 abstract products. For each fresh form in saved order, require every reference to name an input or an earlier fresh form. Final forms may reference inputs and all fresh forms, never other final forms. Every term has integer coefficient +1 or -1; forms are nonempty. U and V precede the 127 pairwise multiplications; W follows them. This supplies a complete acyclic evaluation order.
3. **Exact expansion and ternarity.** Inductively replace each referenced variable by its integer coordinate vector and add signed vectors. Check every coefficient of all 335 fresh forms and 289 final forms, 624 forms total, is in {-1, 0, 1}. No floating point or modular arithmetic is used. Additionally, find and verify an explicit term ordering for every form so that every temporary in its binary fold is ternary. The complete constructive witness is `skeptic/binary_schedule.json`; each `term_order` lists zero-based term positions in the corresponding saved form. All 483 binary addition temporaries are checked. This is a finite exact search for a witness for each saved form, not an exhaustive search for an optimum SLP.
4. **Full tensor identity.** Write the expanded factors as U[t,a] and V[t,b], and output weights as W[o,t]. By distributivity, the coefficient of A[a] B[b] in output o is exactly the integer sum over all 127 t of W[o,t] U[t,a] V[t,b]. For o = k*5+i, a = i0*5+j0 and b = j1*7+k0, the matrix product requires coefficient 1 exactly when i0=i, j0=j1 and k0=k, and 0 otherwise. The checker reconstructs and compares all 35*25*35 = 30,625 coefficients, including every zero. There are exactly 175 required ones and 30,450 required zeros. Together with the form expansions this proves every output is the corresponding entry of A*B over Z for all integer inputs; samples are not the proof.
5. **Reduced count.** Charge L-1 for every saved form of length L, fresh and final. Free signs require no additions and the 127 bilinear multiplications are excluded. The verified binary schedules realize exactly the same charges. U costs 116, V costs 137 and W costs 230, totaling 483. This agrees with the claim, object's reduced metadata and `INDEX.csv`, and is 48 below the saved reference value. The expanded-map naive count, independently computed as nz(U)+nz(V)+nz(W)-2*127-35, is 1607 and agrees with the object's other count metadata.
6. **Direct execution and determinism.** A separate scalar evaluator executes the saved forms without using their expanded vectors, on zero, constant-sign and 64 seeded integer matrix pairs, 67 cases total. It verifies the transposed output layout k*5+i and repeats the output evaluation. These are supplementary spot checks. Three separate successful checker processes produce byte-identical combined output and binary schedules; the checker also verifies that the object bytes are unchanged during each run.

## Exact commands and real output

All commands were run from this folder. Every displayed output block below is inserted directly from its saved output file, not manually retyped.

Independent checker (exit status 0):
```sh
python3 skeptic/check_slp.py object/5x5x7_m127_cr483_ZT_reduced.json > skeptic/output.txt 2>&1
```
```text
Independent checker: exact Python integers; no external dependencies
Object: object/5x5x7_m127_cr483_ZT_reduced.json
SHA256: 1e59f08cf1870f4ade6b3ab5efc2d004e5bb1a0edb455b7e250ed4a7cfc6a65a
Format: 5x5x7; max dimension <= 8 PASS; multiplication gates=127; arithmetic=Z
INDEX.csv: target/cell/path/object SHA256 PASS
U: inputs=25, fresh=116, final=127, forms_checked=243, additions=116, binary_prefixes_checked=116; order/unit signs/expanded ternarity PASS
U: explicit ternary binary folds PASS; forms requiring reordered terms=0
V: inputs=35, fresh=137, final=127, forms_checked=264, additions=137, binary_prefixes_checked=137; order/unit signs/expanded ternarity PASS
V: explicit ternary binary folds PASS; forms requiring reordered terms=0
W: inputs=127, fresh=82, final=35, forms_checked=117, additions=230, binary_prefixes_checked=230; order/unit signs/expanded ternarity PASS
W: explicit ternary binary folds PASS; forms requiring reordered terms=2
Binary schedule: skeptic/binary_schedule.json; SHA256=5faafb0464de73c8ad9023489d6c06028eb9493d52a68698afcee4b27163b19b
All 127 products have nonzero factors and contribute to an expanded output: PASS
Reduced additions: 116 + 137 + 230 = 483; object/claim/INDEX agreement PASS
Expanded-map naive additions: 1607; object metadata agreement PASS
Saved comparison arithmetic only: 483 < 531; reduction=48; PASS
Full integer tensor: outputs=35, coefficients_checked=30625, actual_nonzero=175, expected_nonzero=175; A*B identity PASS
Direct integer SLP execution: 67 deterministic cases; output layout k*n+i and repeat execution PASS
Expanded U,V,W SHA256 (compact JSON): a4cfe2d3133dd4f00db5f49415a87f95de0c3a3103ce1e54120f87888c581f80
Object bytes unchanged during verification: PASS
Scope: no external reference recount, product-identity comparison, live-table comparison or rank-optimality check
RESULT: PASS (saved-object properties)
```

Process repeatability (exit status 0):
```sh
python3 skeptic/repeat_runs.py > skeptic/determinism.txt 2>&1
```
```text
Independent checker process runs: 3; all exit statuses=0; stdout/stderr byte-identical; binary schedules byte-identical: PASS
Output SHA256: 4b5e6bf05e9f0c5d085fc46c384538bdeae5298804ecfa633297e909b9128505
Binary schedule SHA256: 5faafb0464de73c8ad9023489d6c06028eb9493d52a68698afcee4b27163b19b
```

## Initial checker correction

The first independent run rejected an extra assumption I had imposed: that each saved multi-term sum must be implemented as a left fold in its listed term order, with all unnamed prefixes ternary. The quoted definition prescribes a sum of already-computed quantities, not this fold order. The initial output is preserved in `skeptic/initial_output.txt`; it was not silently discarded:
```text
RESULT: FAIL: ValueError: w: a binary prefix is non-ternary
Independent checker: exact Python integers; no external dependencies
Object: object/5x5x7_m127_cr483_ZT_reduced.json
SHA256: 1e59f08cf1870f4ade6b3ab5efc2d004e5bb1a0edb455b7e250ed4a7cfc6a65a
Format: 5x5x7; max dimension <= 8 PASS; multiplication gates=127; arithmetic=Z
INDEX.csv: target/cell/path/object SHA256 PASS
U: inputs=25, fresh=116, final=127, forms_checked=243, additions=116, binary_prefixes_checked=116; order/unit signs/expanded ternarity PASS
V: inputs=35, fresh=137, final=127, forms_checked=264, additions=137, binary_prefixes_checked=137; order/unit signs/expanded ternarity PASS
```

Before opening the author's code, I corrected the checker to construct a ternary binary fold, searching all permissible next terms with exact subset memoization. Every required witness exists. Only `w.final[0]` and `w.final[6]` require reordering: their zero-based term orders are respectively `[0, 1, 3, 2, 4, 5]` and `[0, 2, 3, 1, 4]`. Associativity and commutativity of integer addition preserve each saved form, and each uses L-1 binary operations. The object bytes were not changed. Thus the initial failure concerns my unnecessary implementation restriction; the final checker proves the defined condition and also verifies ternarity of all binary temporaries in an explicit implementation.

## Author comparison after the independent run

Author checker (exit status 0):
```sh
python3 verify-it-yourself/check_slp.py object/5x5x7_m127_cr483_ZT_reduced.json > skeptic/author_output.txt 2>&1
```
```text
{"file": "5x5x7_m127_cr483_ZT_reduced.json", "format": "5x5x7", "rank": 127, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 116, "adds_V": 137, "adds_W": 230, "adds_total": 483, "naive_total": 1607, "declared_reduced": 483, "VALID": true}
```

Author run script, including its sign-flip negative control (exit status 0):
```sh
sh verify-it-yourself/run_checks.sh > skeptic/author_run_checks_output.txt 2>&1
```
```text
sha256 matches INDEX.csv (1e59f08cf1870f4ade6b3ab5efc2d004e5bb1a0edb455b7e250ed4a7cfc6a65a)
== check_slp.py on object/5x5x7_m127_cr483_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x5x7_m127_cr483_ZT_reduced.json", "format": "5x5x7", "rank": 127, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 116, "adds_V": 137, "adds_W": 230, "adds_total": 483, "naive_total": 1607, "declared_reduced": 483, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=483, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

Author SymPy check, using the task-specified environment interpreter by relative path (exit status 0):
```sh
../../../.venv/bin/python verify-it-yourself/sym_check.py object/5x5x7_m127_cr483_ZT_reduced.json > skeptic/author_sympy_output.txt 2>&1
```
```text
{"file": "5x5x7_m127_cr483_ZT_reduced.json", "format": "5x5x7", "rank": 127, "products": 127, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 483}
```

All checked mathematical values agree: format 5x5x7, 127 products, exact transposed output layout, U/V/W counts 116/137/230, total 483 and naive count 1607. SymPy's `C=AB: false` is expected for the alternative row-major output indexing; `C^T: true` is the declared saved layout.

The author's main checker validates term signs and expands forms, but its code does not actually reject non-ternary expanded rows; the SymPy script also checks term signs rather than every expanded coefficient. The independent checker explicitly supplies that missing validation, including all fresh forms and the binary witnesses. This is a limitation of the author's checker, not a mismatch in the saved object. No unresolved saved-object mismatch, missing required local object, or observed non-determinism remains within this review's stated scope.

pass: true
