# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved object's checkable properties pass. This is an offline reproduction verdict, not a determination of a live record, novelty, minimum possible rank, or identity with the unshipped reference scheme.

## Scope and independence

I read CLAIM.md, the object schema/data, INDEX.csv and table-record/README.md before writing skeptic/definition.md and skeptic/check_slp.py. I wrote and ran the independent checker before listing or reading verify-it-yourself/ or reading REPRODUCE.md. The independent checker uses only the Python standard library, exact integers, and the saved object and INDEX.csv. It does not import the author's code. I accessed no network or outside task data. The supplied Python environment was used only as an interpreter for the author's optional SymPy check.

The reference scheme is third-party data and deliberately absent. table-record/README.md records its URL and claimed SHA256, but without its bytes I cannot verify that hash, recount its additions or compare its expanded products. The fetched table/repository source bodies are also absent: their recorded SHA256 values cannot be independently verified here. Live comparisons, best-listed rank, current table values, coefficient-class comparisons, scheme identity with Perminov's file, and novelty belong to the other skeptics. The saved numerical assertion 470 is strictly below 513 is checked only as arithmetic on saved metadata. No exhaustive optimization search is presented by this package; I do not claim optimality. Exactness is checked exhaustively, not by sampling.

## Quoted definition and criterion

Source: CLAIM.md. In these quotations I changed only angle brackets to braces, including format notation. The bracket-normalized Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html; CLAIM.md's criterion actually links fmm_sota.json rather than spelling out that URL template.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) {= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

> - `object/`: the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

In particular, the exactness definition is “is verified symbolically to compute the full product A*B exactly over Z”. The counting definition is “each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP”. The saved-format rule specifies “The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.” All these conditions are checked below. The local dimension bound, explicit product count, output layout and integer coefficient class are checked as well; the external ranking and comparison clauses are outside the scope just stated.

## Independent derivation and checks

1. **Saved bytes and schema.** Parse JSON with duplicate-key rejection and check the exact key set. Require dimensions [4, 5, 8], rank field 118, z2 false, correctly typed integer indices and coefficients, nonempty forms, and the prescribed numbers of factors and outputs. Match the object path, target, cell and SHA256 to INDEX.csv. skeptic/input_hashes.json records all supplied package files' byte hashes; except for the object hash in INDEX.csv, these are reproducibility fingerprints, not independently authenticated external hashes.
2. **Straight-line order and expansion.** Start U with the 20 unit vectors for A, V with the 40 unit vectors for B, and W with the 118 unit vectors for formal products. For fresh assignment k, allow only the input basis and the k earlier fresh vectors. For a final form, allow inputs and all fresh vectors, never other final forms. Inductively replace each reference with its already-established integer coefficient vector and add it with its explicit sign. This proves by induction the expanded vector is the exact value of every stored form. Check every scalar is exactly +1 or -1, and every expanded fresh/final vector has entries in {-1, 0, 1}. There are 599 stored forms: 331 fresh forms and 268 final forms. All 118 product factor pairs are nonzero and every product contributes to an output. “Rank 118” here means a 118-product decomposition; minimality is not inferred.
3. **Ternary binary realization.** A listed form denotes a signed sum, not a specified binary parenthesization. For each form, exhaustively search reachable subsets of its signed summands for an ordering whose every prefix vector is ternary. The largest form has six terms, so this search is complete. Replay and verify each permutation and each prefix independently of the search. Save the chosen zero-based term orders in skeptic/binary_realization.json. All 1,069 prefixes pass, with one form needing reordered terms. A k-term form takes k-1 binary additions, including when it is reordered; a first-term sign is a free negation. Thus this is also a constructive ternary binary realization of the stored sums at the claimed cost. U/V expansion is over their original matrix entries; W expansion is over the formal product inputs, as the definition requires.
4. **Full tensor identity.** After expansion, write product q as (sum_a U[q,a] A[a]) times (sum_b V[q,b] B[b]). For output o, distributivity gives coefficient T[o,a,b] = sum_q W[o,q] U[q,a] V[q,b]. Compute these coefficients in exact integers. Output o = k*4+i must equal sum_j A[i,j] B[j,k]; hence the required coefficient is one exactly when a = i*5+j and b = j*8+k for some j, and zero otherwise. Compare every coefficient, including all zeros: 32 outputs times 20 A entries times 40 B entries = 25,600 comparisons, with 160 required ones and 25,440 required zeros. Equality of every coefficient proves the polynomial identity over Z for every integer A and B, not merely the test cases.
5. **Reduced count and saved metadata.** Sum k-1 over every fresh and final form. U costs 102+0, V costs 146+0, and W costs 152+70, giving 102+146+222 = 470. Equivalently 1,069 signed terms minus 599 forms = 470. The 118 bilinear multiplications and unary signs are excluded. The expanded naive count is nz(U)+nz(V)+nz(W)-2*118-32 = 1,521; this agrees with the object's separate naive metadata. The reduced count agrees with the object and INDEX.csv, and the saved comparison is 470 less than 513 by 43. This does not recount or authenticate the reference's 513.
6. **Execution and determinism.** Execute the saved SLP directly on zero/constant cases and 20 fixed-seed integer cases, checking every output in its specified transposed layout. These 23 cases supplement the exhaustive coefficient proof. Re-read the original bytes at the end and require they are unchanged. Run the independent checker in two separate processes and compare the entire output byte-for-byte. The output hashes agree, as do the deterministically generated expansion and binary-witness hashes. The checker has no stochastic success criterion.

## Exact commands and actual outputs

All commands are run from this folder. All named artifact paths are relative to this folder.

Independent checker and repeat:

```sh
python3 -u skeptic/check_slp.py > skeptic/output.txt 2>&1
python3 -u skeptic/check_slp.py > skeptic/output-repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output-repeat.txt
```

Both checker runs exited 0. cmp exited 0 and produced no output. The following is pasted programmatically from skeptic/output.txt without alteration:

```text
Object: object/4x5x8_m118_cr470_ZT_reduced.json
SHA256: 8f63968828f21bb5d9ac3954a4424a742a68f22c641afbd4c507d26d3f7e3a2f
INDEX.csv: object path, target, cell and SHA256 agree
Format: 4x5x8; products: 118; max dimension: 8; arithmetic: Z
U: inputs=20, fresh=102, final=118, additions fresh=102, final=0, total=102
V: inputs=40, fresh=146, final=118, additions fresh=146, final=0, total=146
W: inputs=118, fresh=83, final=32, additions fresh=152, final=70, total=222
Straight-line order and scalar signs: PASS for all 599 stored forms
Ternary integer expansions: PASS for all 599 stored forms
Ternary binary realization: PASS, 1069 prefixes; 1 forms need reordered terms
Binary realization witness: skeptic/binary_realization.json; SHA256: c0bef753c5a95aad32372ef3d54d40da537832a5fa63b9751c18179a10071aeb
All 118 products have nonzero factors and contribute to an output
Full tensor identity: PASS, 25600 integer coefficients checked exhaustively (160 ones, 25440 zeros)
Reduced additions: 470; naive expanded count: 1521; both agree with object metadata
Saved numerical comparison only: 470 < 513, difference=43
Direct execution: PASS for 23 deterministic integer cases (supplementary to exhaustive tensor proof)
Expanded U/V/W SHA256: ce198b4576057dfe89ac41b2518dd01f7343fd3d0d8d8bc9e3cdb9b117bf7744
Object reread: identical bytes and parsed data
Scope: reference scheme absent; no reference recount, product-identity comparison or live-table verification
RESULT: PASS (all saved-object properties checked)
```

Only after that independent run, I read REPRODUCE.md and the author's source files, then ran:

```sh
python3 verify-it-yourself/check_slp.py object/4x5x8_m118_cr470_ZT_reduced.json > skeptic/author-output.txt 2>&1
../../../.venv/bin/python verify-it-yourself/sym_check.py object/4x5x8_m118_cr470_ZT_reduced.json > skeptic/author-symbolic-output.txt 2>&1
python3 skeptic/compare_checks.py > skeptic/comparison-output.txt 2>&1
```

All exited 0. The following outputs are pasted directly from their saved files.

Author checker, skeptic/author-output.txt:

```text
{"file": "4x5x8_m118_cr470_ZT_reduced.json", "format": "4x5x8", "rank": 118, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 102, "adds_V": 146, "adds_W": 222, "adds_total": 470, "naive_total": 1521, "declared_reduced": 470, "VALID": true}
```

Author SymPy cross-check, skeptic/author-symbolic-output.txt:

```text
{"file": "4x5x8_m118_cr470_ZT_reduced.json", "format": "4x5x8", "rank": 118, "products": 118, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 470}
```

Automated comparison, skeptic/comparison-output.txt:

```text
Independent checker: two separate process outputs are byte-identical
Independent output SHA256: 718dc639c97d567e29d9a6d7c9e247698e6156aaf24e2013798156142d66b46b
Author checker: exactness, output layout, products, per-map counts and naive count agree
Author SymPy checker: exactness, output layout, products and reduced count agree
W fresh 78 ternary binary term order (zero-based positions): [0, 1, 3, 2, 4]
Saved package-byte SHA256 manifest: skeptic/input_hashes.json
COMPARISON: PASS; no result disagreements
```

## Initial diagnostic, correction and checker limitations

The independent checker's initial extra requirement treated the listed summand order as a mandatory left-to-right binary order. That initial run exited 1 and its full actual output is preserved in skeptic/initial_output.txt:

```text
RESULT: FAIL: AssertionError: w fresh 78: nonternary binary prefix
Object: object/4x5x8_m118_cr470_ZT_reduced.json
SHA256: 8f63968828f21bb5d9ac3954a4424a742a68f22c641afbd4c507d26d3f7e3a2f
INDEX.csv: object path, target, cell and SHA256 agree
Format: 4x5x8; products: 118; max dimension: 8; arithmetic: Z
U: inputs=20, fresh=102, final=118, additions fresh=102, final=0, total=102
V: inputs=40, fresh=146, final=118, additions fresh=146, final=0, total=146
```

This prefix diagnostic is real, but it does not contradict the stated definition of a form as a sum. For w_fresh[78], the saved term indices/signs are (+191, +165, -163, +140, -66). The original order has a nonternary partial sum, while the independently found and replayed order of term positions [0, 1, 3, 2, 4], namely (+191, +165, +140, -163, -66), has only ternary partial sums and the identical final vector and four-addition cost. I corrected this extra assumption before reading the author's code; skeptic/definition.md records the clarification. No input object was modified. The initial shell wrapper also attempted to assign zsh's read-only variable named status after executing the checker; later commands use check_exit and their real exit results are reported above.

The author's documented claim to check every expanded intermediate's ternarity is broader than its implementation: check_slp.py validates stored term signs and expands vectors, but never asserts that each expanded vector is ternary. Its SymPy checker likewise checks stored signs. This is a checker coverage limitation, not a disagreement about this object: the independent checker explicitly verifies all expanded forms and constructs the stronger ternary binary realization. The author's tensor identity, 118 products, transposed layout, per-map costs, total cost and naive count all agree with the independent results. The negative-control run script was read but not run; the two standalone author checkers above were run directly.

No mismatch remains among the saved-object claims within scope. The external omissions described under scope remain unverified and are not represented as reproduction of the full live-record claim.

pass: true
