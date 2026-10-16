context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object passes the assigned offline reproduction checks. I wrote `skeptic/definition.md`, `skeptic/check.py`, and `skeptic/run_checks.py` before opening anything in `verify-it-yourself/`, and ran the independent checker before reading or running the author's code. No network was used. All inspected package files and all written artifacts are within this folder; the explicitly permitted external interpreter was used only to run the optional SymPy cross-check.

**Definition and success criterion checked**

The success criterion in `CLAIM.md` is quoted below. In its format placeholder I changed only the angle brackets to braces. The Lille URL template is written https://fmm.univ-lille.fr/{n}x{m}x{p}.html, changing only the brackets; the supplied criterion itself names the per-format page descriptively rather than spelling out this template.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The exactness condition, counting convention, and saved representation are also quoted here, as fixed in `skeptic/definition.md` before reading the author's code:

> explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs)

> max(n,m,p) <= 8

> is verified symbolically to compute the full product A*B exactly over Z

> each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP

> The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.


The claimed saved-object value is quoted from `CLAIM.md`: "using 294 additions/subtractions under Perminov's reduced counting convention, strictly fewer than 319". The dimensions are 4x4x7 and the decomposition has 85 products. The additional promised check is "the ternary condition on every expanded intermediate".

**Scope**

This verdict covers the saved object's exactness over Z, all expanded ternary coefficients, straight-line order, dimensions, number of products, addition counts, saved-object hash, and determinism. The recorded inequality 294 < 319 is verified as arithmetic only. I do not judge current table status, best known rank, priority, or novelty.

`table-record/README.md` explicitly says that Perminov's reference scheme is third-party data and is not shipped. It gives its URL and sha256, but neither is an offline substitute for the file. Without network I cannot recount that reference, authenticate its hash, or confirm product-by-product identity with it. The live reference minimum, fmm_sota rank, Lille comparisons, and matmulcatalog comparisons are assigned to the other skeptics. Hashes of unsaved source responses are likewise metadata, not independently verified here. The absence of the expressly excluded reference is not a missing saved object under this assigned scope.

There is no exhaustive-search assertion needed to certify this supplied SLP. The tensor check is exhaustive over every coefficient, not a sample of integer matrices. I did not infer any optimality result from it.

**Properties and independent proof**

1. Object and integrity: require the named object to be a regular, non-symlink file, parse JSON with duplicate-key rejection, validate the field layout and integer types, and compute SHA-256 from its actual bytes. Compare the digest, filename, target, cell, and value with the sole `INDEX.csv` row. The object is 23,280 bytes and its hash matches.
2. Format and product count: independently require dimensions [4,4,7], maximum dimension at most eight, `z2` false, exactly 85 U factors and 85 V factors, and 28 W outputs. Every factor and product contribution is nonzero. This certifies a decomposition with 85 multiplication terms; it makes no lower-bound claim about tensor rank.
3. Straight-line order: initialize a separate integer identity basis for each map. For fresh variable k, require every reference index to be less than the current basis length (input count plus k). Append its expansion only after checking it. Final forms may use inputs and completed fresh variables only. All terms have integer scalar +1 or -1; all forms are nonempty.
4. Ternary condition: expand all 72 U, 83 V, and 50 W fresh rows and all 85 U, 85 V, and 28 W final rows over Z, checking every coefficient lies in {-1,0,1}. This covers all 403 saved forms. Also check all 697 partial sums in stored term order, so lowering each multi-term form to binary operations introduces no non-ternary partial expansion. All pass.
5. Exact tensor identity: write each left factor as U[q,a] A[a], each right factor as V[q,b] B[b], and each output o as the W[o,q]-weighted sum of their products. By substitution, the coefficient of A[a]B[b] in output o is sum over q of W[o,q] U[q,a] V[q,b]. For every i,k,a,b, compute this integer sum and compare with 1 exactly when a = i*4+j and b = j*7+k for some j, and 0 otherwise, using the required output index o = k*4+i. All 28*16*28 = 12,544 coefficients match: 112 ones and 12,432 zeros. Because the maps are homogeneous linear forms and the only products are U times V, there are no constant, linear, or other-degree monomials. This proves every output is sum over j of A[i,j]B[j,k] over Z for all inputs.
6. Reduced count: each L-term form can be evaluated in L-1 binary additions/subtractions, with signs free and the 85 bilinear multiplications excluded. Sum over every saved fresh and final form: U contributes 72, V contributes 83, W contributes 139, totaling 294. This agrees with both the claim and `complexity.reduced`. The expanded-map naive count is independently 631, agreeing with `complexity.naive`. The arithmetic improvement over the recorded 319 is 25.
7. Determinism: run the independent checker in two fresh Python processes with `PYTHONHASHSEED` 0 and 1. Both exit successfully with byte-identical output, including a SHA-256 of all expanded fresh and final rows. The SLP has no branch, randomness, external lookup, or unspecified evaluation dependency, and uses exact integers.

**Exact independent command and full real output**

Run from this folder:

```sh
python3 skeptic/run_checks.py
```

The runner invokes `python3 skeptic/check.py` twice as described above and saves both complete outputs and their equality result in `skeptic/output.txt`. The following is pasted directly from that saved file:

```text
=== Independent run 1; PYTHONHASHSEED=0; exit=0 ===
Independent checker: Python standard library; exact integer arithmetic; no network
Object: object/4x4x7_m85_cr294_ZT_reduced.json
Object bytes: 23280
Object sha256: a6655488fc692a5a552aed8c46ae58eff2a384d66f33966f3a53c0a33b3fec2e
Dimensions: 4x4x7; max dimension <= 8: PASS; products: 85
U map: {"additions": 72, "final": 85, "fresh": 72, "histogram": {"1": 85, "2": 72}, "inputs": 16, "prefixes": 229}
V map: {"additions": 83, "final": 85, "fresh": 83, "histogram": {"1": 85, "2": 83}, "inputs": 28, "prefixes": 251}
W map: {"additions": 139, "final": 28, "fresh": 50, "histogram": {"1": 2, "2": 40, "3": 22, "4": 7, "5": 1, "6": 6}, "inputs": 85, "prefixes": 217}
All references use inputs or earlier fresh variables: PASS
All stored scalars are +1 or -1; every fresh/final expansion and every stored-order partial sum is ternary: PASS
Every factor, output, fresh variable and product contribution is nonzero: PASS
Full tensor identity over Z: PASS; coefficients checked=12544; ones=112; zeros=12432
Reduced additions: 72 + 83 + 139 = 294; metadata and claim: PASS
Expanded naive additions: 631; metadata: PASS
INDEX.csv filename, target, cell, value and sha256: PASS
Recorded reference arithmetic only: 294 < 319; difference=25; reference not independently recounted
Expanded rows sha256: 00159227af58e1bbf18ebe484135eaec72b6249c5386378c6d905c8dd0ca388a
RESULT: PASS (all saved-object properties; external reference and live comparisons excluded)
=== Independent run 2; PYTHONHASHSEED=1; exit=0 ===
Independent checker: Python standard library; exact integer arithmetic; no network
Object: object/4x4x7_m85_cr294_ZT_reduced.json
Object bytes: 23280
Object sha256: a6655488fc692a5a552aed8c46ae58eff2a384d66f33966f3a53c0a33b3fec2e
Dimensions: 4x4x7; max dimension <= 8: PASS; products: 85
U map: {"additions": 72, "final": 85, "fresh": 72, "histogram": {"1": 85, "2": 72}, "inputs": 16, "prefixes": 229}
V map: {"additions": 83, "final": 85, "fresh": 83, "histogram": {"1": 85, "2": 83}, "inputs": 28, "prefixes": 251}
W map: {"additions": 139, "final": 28, "fresh": 50, "histogram": {"1": 2, "2": 40, "3": 22, "4": 7, "5": 1, "6": 6}, "inputs": 85, "prefixes": 217}
All references use inputs or earlier fresh variables: PASS
All stored scalars are +1 or -1; every fresh/final expansion and every stored-order partial sum is ternary: PASS
Every factor, output, fresh variable and product contribution is nonzero: PASS
Full tensor identity over Z: PASS; coefficients checked=12544; ones=112; zeros=12432
Reduced additions: 72 + 83 + 139 = 294; metadata and claim: PASS
Expanded naive additions: 631; metadata: PASS
INDEX.csv filename, target, cell, value and sha256: PASS
Recorded reference arithmetic only: 294 < 319; difference=25; reference not independently recounted
Expanded rows sha256: 00159227af58e1bbf18ebe484135eaec72b6249c5386378c6d905c8dd0ca388a
RESULT: PASS (all saved-object properties; external reference and live comparisons excluded)
Fresh-process output equality across seeds 0 and 1: PASS
```

**Author comparison**

Only after that independent run did I inspect `REPRODUCE.md` and the files in `verify-it-yourself/`. I ran these commands from this folder:

```sh
python3 verify-it-yourself/check_slp.py object/4x4x7_m85_cr294_ZT_reduced.json
python3 verify-it-yourself/sym_check.py object/4x4x7_m85_cr294_ZT_reduced.json
../../../.venv/bin/python verify-it-yourself/sym_check.py object/4x4x7_m85_cr294_ZT_reduced.json > skeptic/sympy_output.txt
```

The first command agrees on exact transposed output order, 85 products, 294 reduced additions, and naive count 631. The second initially failed because the default interpreter has no SymPy; the supplied interpreter ran the same symbolic cross-check successfully (exit 0). This is a dependency issue, not an object mismatch. Output below is pasted from `skeptic/author_output.txt`; the traceback frames are omitted, retaining the actual final exception line. Traceback filenames in the saved log were normalized to relative paths:

```text
$ python3 verify-it-yourself/check_slp.py object/4x4x7_m85_cr294_ZT_reduced.json
{"file": "4x4x7_m85_cr294_ZT_reduced.json", "format": "4x4x7", "rank": 85, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 72, "adds_V": 83, "adds_W": 139, "adds_total": 294, "naive_total": 631, "declared_reduced": 294, "VALID": true}
exit: 0
$ python3 verify-it-yourself/sym_check.py object/4x4x7_m85_cr294_ZT_reduced.json
ModuleNotFoundError: No module named 'sympy'
exit: 1
```

The successful symbolic output, pasted directly from `skeptic/sympy_output.txt`:

```text
{"file": "4x4x7_m85_cr294_ZT_reduced.json", "format": "4x4x7", "rank": 85, "products": 85, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 294}
```

The symbolic checker reports C^T true and C=AB false because the saved output ordering is explicitly k*n+i; this agrees with the definition, not a failure of matrix multiplication.

One verification-coverage discrepancy exists: `REPRODUCE.md` says the author's main checker checks every expanded intermediate for ternarity, but `verify-it-yourself/check_slp.py` checks term scalars and does not test the expanded coefficients for membership in {-1,0,1}. Its SymPy companion also only checks stored term scalars. My independent exhaustive expansion supplies that missing check and passes it, including all stored-order partial sums. There is no numerical, tensor, ordering, count, or hash disagreement on this object.

pass: true
