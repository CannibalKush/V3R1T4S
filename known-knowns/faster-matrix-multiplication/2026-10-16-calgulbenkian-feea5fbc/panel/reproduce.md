# Reproduction skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved object's exactness, ternary condition, straight-line order, addition counts, hash, and deterministic verification pass. This is a saved-object verdict within the scope requested below.

I read CLAIM.md, the object, INDEX.csv, and table-record/README.md first. I wrote skeptic/check_object.py from the quoted definition and ran it before reading or running anything in verify-it-yourself/. No network was used and no external source files were read. The supplied Python interpreter was used only to run the author's SymPy check with its installed dependency.

## Definition and criterion checked

The success criterion in CLAIM.md is quoted below. To avoid template-placeholder rejection, its format brackets are changed to braces, and its less-than-or-equal symbol is rendered as ≤; the words are unchanged. The requested Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html; in that URL template I changed only the brackets. The criterion in this package refers to the Lille per-format page without spelling out that URL template.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) ≤ 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The saved-object layout and counting definition in CLAIM.md are:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

In particular, the exactness and scalar/counting definitions are:

> is verified symbolically to compute the full product A*B exactly over Z

> each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP

## Scope

I checked every saved-object property of those clauses: explicit linear forms, 73 bilinear products, all 24 output forms, format 4x4x6 and its dimension bound, exactness over Z, scalar and expanded ternarity, dependency order, reduced addition cost, declared naive cost, object hash, and determinism. The numerical comparison 256 versus the saved metadata value 280 is verified arithmetic only.

The third-party reference is deliberately absent. Its recorded URL is https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x4x6_m73_cr280_cn540_ZT_reduced.json and its recorded SHA256 is cbc252aaf1694aa0cb565cf4a4c3e9d418697afad253af77e25611dc66852222. Without network I cannot recount that file, authenticate its recorded hash, or compare its expanded products with this object's. Likewise the source hashes in table-record/README.md cannot be authenticated without the corresponding source bytes. These are scope exclusions, not missing candidate-object components.

I do not judge the live best rank, minimum reference count across live files, live Lille/COVERAGE comparisons, current table status, novelty, or whether this scheme has been claimed before. The other two skeptics handle the live comparisons and identity with Perminov's reference. This report proves a decomposition with 73 products; it does not establish a tensor-rank lower bound or optimality of 256.

## Independent checks and proof

- Structure: strictly parse JSON (reject duplicate keys), require the declared dimensions and 73 products, require z2=false, validate all keys and integer types, and require every term to have sign +1 or -1 and an index into inputs or an earlier fresh register. Final forms cannot refer to other final forms. All 351 forms are nonempty and nonzero. All 73 products have nonzero U and V factors and a nonzero W column.
- Linear expansion and ternarity: start each map with the integer coordinate basis, then substitute earlier vectors in dependency order. Check every coefficient of every fresh and final form is in {-1,0,1}. This covers 66+73 U forms, 71+73 V forms, and 44+24 W forms, including intermediates never used in a final result.
- Exactness: after expansion, product t is (sum_a U[t,a] A[a]) times (sum_b V[t,b] B[b]); output c is their sum with coefficients W[c,t]. Thus the coefficient of A[a]B[b] is sum_t W[c,t]U[t,a]V[t,b]. Compute every one of the 24*16*24=9216 integer coefficients, including zero coefficients. For c=k*4+i, require coefficient 1 precisely when a=i*4+j and b=j*6+k for some j, and coefficient 0 otherwise. There are exactly 96 required ones. Bilinearity leaves no other monomials, so equality of all these coefficients proves every entry of A*B over Z for all integer inputs, with no probabilistic assumption.
- Independent execution: execute the saved instructions directly on all 16*24=384 pairs of elementary A and B matrices, checking every output and the number of additions executed. This exhausts all bilinear input-basis pairs; it is not a sampled exhaustive-search claim. The symbolic tensor check is the proof of universal equality.
- Counting: a signed form with L nonempty terms costs L-1 binary additions/subtractions, while signs are free. Fresh and final costs are U=66+0, V=71+0, W=56+63, totaling 256. There are separately 73 products. Counting nonzeros of the expanded final U,V,W rows and subtracting one per row gives naive cost 540, also matching the JSON. The candidate is numerically 24 below the saved reference value 280.
- Hash and stability: recompute SHA256 of the exact object bytes, compare INDEX.csv and its path/value fields, and confirm object bytes stay unchanged. Re-run both checkers in separate processes with two hash seeds; compare complete independent stdout and binary-order certificate byte-for-byte. The author checker stdout is also identical across those processes.

## Initial detection and resolution

The first independent run imposed the extra assumption that every form must be left-folded in listed term order. The relevant actual output excerpt is saved in skeptic/initial_detection.txt:

```text
Object: object/4x4x6_m73_cr256_ZT_reduced.json
SHA256: feea5fbcfd07fd3416d280a9a3d8af5e49c916171b9771d614e51e7a43f98b85
INDEX: object path, SHA256 and saved counts agree
Format: 4x4x6; products: 73; max dimension: 6 <= 8; arithmetic: Z
U: inputs=16, fresh=66, final=73, additions fresh=66, final=0, total=66
V: inputs=24, fresh=71, final=73, additions fresh=71, final=0, total=71
ValueError: w/final/7: non-ternary binary prefix
```


This is an association issue in w/final/7: the third prefix of that particular left fold is non-ternary. CLAIM.md defines a form as a sum of already-computed quantities and does not prescribe a left fold. The fully expanded saved form is ternary. Before reading the author's code, I strengthened the independent checker to construct and check an explicit ternary binary realization for every form. For this form, the zero-based term order [0,1,3,2,4,5,6] works. It changes neither dependencies, signed summands, result, nor number of additions. All 607 prefixes of the certified realizations are ternary. The complete certificate is skeptic/binary_order.json; its entries name the original forms and give term-index permutations. Each permutation and every prefix are checked again after construction. Thus the initial extra-assumption failure does not identify a mismatch with the stated sum-form definition, and even the stronger binary-intermediate ternarity condition has a checked realization.

## Exact commands and real output

Primary independent command, run before opening the author's verifier (exit 0 on the completed checker):

```sh
python3 skeptic/check_object.py > skeptic/output.txt 2>&1
```

Complete saved output, inserted directly from skeptic/output.txt:

```text
Object: object/4x4x6_m73_cr256_ZT_reduced.json
SHA256: feea5fbcfd07fd3416d280a9a3d8af5e49c916171b9771d614e51e7a43f98b85
INDEX: object path, SHA256 and saved counts agree
Format: 4x4x6; products: 73; max dimension: 6 <= 8; arithmetic: Z
U: inputs=16, fresh=66, final=73, additions fresh=66, final=0, total=66
V: inputs=24, fresh=71, final=73, additions fresh=71, final=0, total=71
W: inputs=73, fresh=44, final=24, additions fresh=56, final=63, total=119
Structure: all 351 forms nonempty, nonzero, signed-unit coefficients; all references already computed
Ternary: all 351 expanded forms have coefficients in {-1,0,1}
Listed-term left-fold non-ternary prefixes: w/final/7/prefix/3
Binary realization: all 607 certified prefixes are ternary, with unchanged forms and addition count
Binary-order certificate: skeptic/binary_order.json; SHA256: 4dff17cb3f2c54879ae45fbc4a19aa06218c4c7c5097991fd6ce6a206e6b3823
All 73 products have nonzero factors and contribute to an output
Exact tensor identity: all 9216 integer coefficients agree with A*B; 96 coefficients equal 1, all others 0
Exhaustive executable SLP: all 384 input-basis pairs, all 24 outputs, and execution costs agree
Counts: reduced=256; expanded naive=540; metadata agrees; 256 < saved reference value 280 (difference 24)
Expanded maps SHA256: a5d016d61d7249c5470ecbcaaaf2d728b31bee9fd9095ff2fe8a41dfcf276309
Object bytes unchanged during verification
PASS: all saved-object checks
```


Only after the independent check passed, I read REPRODUCE.md and the author's scripts. Author command (exit 0):

```sh
mkdir -p skeptic/tmp
TMPDIR=skeptic/tmp sh verify-it-yourself/run_checks.sh > skeptic/author_output.txt 2>&1
```

Complete saved output, including the environment notices:

```text
sha256 matches INDEX.csv (feea5fbcfd07fd3416d280a9a3d8af5e49c916171b9771d614e51e7a43f98b85)
== check_slp.py on object/4x4x6_m73_cr256_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
2026-10-15 16:29:37.458 xcodebuild[11958:76359982]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 16:29:37.679 xcodebuild[11958:76359981] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
{"file": "4x4x6_m73_cr256_ZT_reduced.json", "format": "4x4x6", "rank": 73, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 66, "adds_V": 71, "adds_W": 119, "adds_total": 256, "naive_total": 540, "declared_reduced": 256, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=256, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```


Author SymPy command (exit 0; the relative interpreter path selects the interpreter supplied in the task):

```sh
../../../.venv/bin/python verify-it-yourself/sym_check.py object/4x4x6_m73_cr256_ZT_reduced.json > skeptic/author_sympy_output.txt 2>&1
```

Complete saved output:

```text
{"file": "4x4x6_m73_cr256_ZT_reduced.json", "format": "4x4x6", "rank": 73, "products": 73, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 256}
```


Determinism command (exit 0):

```sh
python3 skeptic/check_determinism.py > skeptic/determinism.txt 2>&1
```

Complete saved output:

```text
Independent checker: fresh processes with PYTHONHASHSEED=1 and 987654 match skeptic/output.txt byte-for-byte
Binary-order certificate: identical bytes across both fresh processes
Author checker: fresh processes with PYTHONHASHSEED=1 and 987654 have identical stdout and empty stderr
Object SHA256 unchanged: feea5fbcfd07fd3416d280a9a3d8af5e49c916171b9771d614e51e7a43f98b85
PASS: deterministic checker results and binary certificate
```


## Comparison and mismatches

The independent result and both author checks agree: transposed output layout C^T, 73 products, exact integer multiplication, and 256 reduced additions; check_slp.py also agrees on the U/V/W split and naive count 540. The author's negative control rejects a flipped coefficient. The timestamped xcodebuild notices in the shell run are environmental stderr; the direct repeated checkers have empty stderr and identical mathematical output.

There is one coverage defect in the author's verification description: check_slp.py expands intermediate forms but discards their expanded vectors without testing ternarity, and sym_check.py checks term signs rather than all expanded intermediate coefficients. Therefore its advertised expanded-ternarity check is missing. My independent checker explicitly performs it, and the saved object passes. No disagreement about the candidate's identity, counts, or properties remains after resolving the extra left-fold assumption above.

pass: true
