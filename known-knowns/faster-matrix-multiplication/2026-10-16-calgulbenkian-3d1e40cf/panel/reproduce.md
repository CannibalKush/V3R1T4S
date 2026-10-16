REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved object's properties pass independent reproduction. This is a scoped offline verdict, not certification of a live addition-count record.

Scope: I read only this claim-package folder and used no network. I read CLAIM.md, the saved object, INDEX.csv, and table-record/README.md, then wrote skeptic/check.py and ran it successfully before reading REPRODUCE.md or any file in verify-it-yourself/. The checker uses python3 and the standard library; it imports no author code. The full initial output is saved in skeptic/output.txt. Only after that run did I inspect and execute the author's code.

Perminov's reference scheme is deliberately absent. table-record/README.md supplies its URL and reported SHA256, but not its bytes. Without network I cannot recount that file, validate its hash, or compare its expanded products with this object's. The recorded reference count 181 is metadata, not an independently verified reference count. Verification of reference-product identity, live minimum, coefficient-class comparisons, best listed rank, table currency, and novelty belongs to the other skeptics. None is inferred here. No required saved object is missing within this assigned scope.

Definition checked, quoted from CLAIM.md's success criterion (full criterion, including clauses outside this skeptic's scope):

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

Quotation notation: only the brackets around the format placeholder have been changed, from angle brackets to braces. For the Lille URL template I use https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only the template brackets are changed. No mathematical clause is changed.

The two operative definitions, quoted exactly from that criterion, are:

> each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP

> is verified symbolically to compute the full product A*B exactly over Z

The saved-layout definition and counting formula, quoted from CLAIM.md:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

Every saved-file clause and how it was checked:

| Property | Independent check and result |
| --- | --- |
| Explicit SLP and format bound | Strict JSON parsing rejects duplicate keys, unexpected schema, noninteger dimensions/rank/scalars/indices, invalid terms, and empty forms. Dimensions are [2,5,6], maximum 6 is at most 8, z2 is false, and the integer evaluator implements the supplied layout. |
| 47 bilinear products and 12 outputs | U and V each contain exactly 47 final factors; W contains 12 output forms over 47 product inputs. Each product has two nonzero factors and a nonzero output-map column. This proves a 47-product decomposition, not a lower bound on tensor rank. |
| Straight-line order | For fresh form k, every index is less than the input count plus k. Final factors/outputs can use only map inputs or existing fresh variables. U uses 10 A entries, V uses 30 B entries, W uses 47 products. U/V final rows are not made available as fresh variables. |
| Permitted scalars and expanded ternarity | Every written coefficient is an integer +1 or -1. Every one of the 192 named fresh/final forms expands to coefficients in {-1,0,1}. The checker also tests every partial sum in listed term order, so the implied binary realization introduces no nonternary accumulator. For W, ternarity is checked over its 47 independent product inputs, as required for this ternary linear map. |
| Full exact product over Z | Dense integer vectors expand U, V, W. Every one of 12 times 10 times 30 = 3,600 tensor coefficients is compared against the matrix-product definition. All 60 required ones and 3,540 required zeros agree, with output index c=k*2+i. This is exhaustive symbolic coefficient checking, not numerical sampling. |
| Execution of the actual SLP | A separate evaluator executes every instruction on all 10 times 30 = 300 pairs of standard-basis inputs, comparing all 12 outputs, twice per pair. Given the proven bilinear syntax, those basis pairs also determine the function on every integer input. |
| Reduced counting convention and claimed 179 | Each nonempty L-term form is realized by L-1 binary additions/subtractions, with signed first term/negations free. The counter counts these binary operations and separately sums L-1 over all forms. U: 38 fresh + 0 final = 38; V: 28 + 37 = 65; W: 20 + 56 = 76; total 179. The 47 products are excluded. No scalar other than signed unity is used. |
| Other saved count metadata | Expanded nonzero counts give naive total nz(U)+nz(V)+nz(W)-2*47-12 = 332. Both naive and reduced values match the object's complexity fields. INDEX.csv target, cell, path, and value agree. |
| Arithmetic relative to recorded reference | INDEX.csv and table-record/README.md agree on candidate 179 and recorded reference 181; 179 is strictly smaller by 2. This checks arithmetic and internal metadata consistency only. |
| Saved-object hash | The SHA256 of the actual object bytes matches INDEX.csv. The checker also verifies that those bytes did not change during the run. Hashes of absent downloaded reference files/pages cannot be validated from metadata alone. |
| Determinism | Full independent stdout/stderr is byte-identical across two processes, including a changed Python hash seed. Direct author-checker output is also byte-identical across two processes with different hash seeds. Every basis-pair execution is repeated within each independent run. No object or checker result nondeterminism was observed. |

Proof re-derived: start each input map with the standard basis vectors e_j. If all earlier vectors denote the already computed quantities, then replacing each signed reference by its vector and adding gives exactly the next linear form over Z. Dependency checks make this an induction through every fresh variable and final row. A first signed term costs no addition; appending each further signed term costs one binary operation, giving L-1 by induction on form length. The ternary checks cover the vectors at every such step.

For product q, the expanded bilinear coefficients are U[q,a] times V[q,b]. Therefore output c has coefficient T[c,a,b] = sum over q of W[c,q]*U[q,a]*V[q,b]. Writing a=i'*5+j and b=j'*6+k', the matrix-product coefficient for output c=k*2+i is 1 exactly when i'=i, k'=k, and j=j', and 0 otherwise. The checker tests this equation for every c,a,b using arbitrary-precision integers. Thus every output polynomial equals its required entry of A*B over Z, for all inputs. These induction and coefficient identities are the entire exactness proof; there is no probabilistic step or unexamined proof assertion.

No exhaustive optimization search is claimed or needed for this reproduction. All instructions, partial sums, tensor entries, and input-basis pairs are checked. This verifies a 179-addition construction; it does not claim 179 is an optimal addition count.

Exact commands, run from this folder in the order shown (every command exited 0):

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
mkdir -p skeptic/tmp
TMPDIR=skeptic/tmp sh verify-it-yourself/run_checks.sh > skeptic/author_output.txt 2>&1
PYTHONHASHSEED=1 python3 skeptic/check.py > skeptic/output.repeat.txt 2>&1
TMPDIR=skeptic/tmp PYTHONHASHSEED=2 sh verify-it-yourself/run_checks.sh > skeptic/author_output.repeat.txt 2>&1
python3 verify-it-yourself/check_slp.py object/2x5x6_m47_cr179_ZT_reduced.json > skeptic/author_checker.txt 2>&1
PYTHONHASHSEED=3 python3 verify-it-yourself/check_slp.py object/2x5x6_m47_cr179_ZT_reduced.json > skeptic/author_checker.repeat.txt 2>&1
python3 skeptic/compare_runs.py > skeptic/comparison.txt 2>&1
```

Actual full independent output, inserted directly from skeptic/output.txt:

```text
Object: object/2x5x6_m47_cr179_ZT_reduced.json
SHA256: 3d1e40cf65f343ad2edfe3735c1d4eccd1fd4aeaca82b31980779e38a059dcc1
Format: 2x5x6; products=47; maximum dimension <= 8 PASS
U: inputs=10, fresh=38, final=47, forms=85, additions=38+0=38; order/scalars/expanded ternary/prefixes PASS
V: inputs=30, fresh=28, final=47, forms=75, additions=28+37=65; order/scalars/expanded ternary/prefixes PASS
W: inputs=47, fresh=20, final=12, forms=32, additions=20+56=76; order/scalars/expanded ternary/prefixes PASS
All 47 bilinear products have nonzero factors and occur in the output map PASS
Exact integer tensor: all 3600 coefficients PASS; 60 ones, 3540 zeros; output c=k*2+i
Direct SLP execution: all 300 input-basis pairs, all 12 outputs, each repeated twice PASS
Counts: reduced=38+65+76=179; expanded naive=332; metadata PASS
INDEX: path, SHA256, target, cell, value=179, recorded reference=181 PASS
Recorded comparison arithmetic: 179 < 181, improvement=2 PASS (reference unverified offline)
Expanded maps SHA256 (sorted-key compact JSON): 2d1023db0636b672e44258b9de4e2dc468dbf0c49496c498f634a2e3d24762d8
Object bytes stable during run PASS
Scope: no reference scheme bytes or live pages available; their hashes, reference recount,
optimal rank, live minimum, novelty, and identity with Perminov are not certified here.
RESULT: PASS saved-object properties
```

Actual full first author-wrapper output, inserted directly from skeptic/author_output.txt:

```text
sha256 matches INDEX.csv (3d1e40cf65f343ad2edfe3735c1d4eccd1fd4aeaca82b31980779e38a059dcc1)
== check_slp.py on object/2x5x6_m47_cr179_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
2026-10-15 16:29:18.478 xcodebuild[10268:76354418]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 16:29:18.641 xcodebuild[10268:76354413] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
{"file": "2x5x6_m47_cr179_ZT_reduced.json", "format": "2x5x6", "rank": 47, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 38, "adds_V": 65, "adds_W": 76, "adds_total": 179, "naive_total": 332, "declared_reduced": 179, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=179, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

Actual full second author-wrapper output, inserted directly from skeptic/author_output.repeat.txt:

```text
sha256 matches INDEX.csv (3d1e40cf65f343ad2edfe3735c1d4eccd1fd4aeaca82b31980779e38a059dcc1)
== check_slp.py on object/2x5x6_m47_cr179_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "2x5x6_m47_cr179_ZT_reduced.json", "format": "2x5x6", "rank": 47, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 38, "adds_V": 65, "adds_W": 76, "adds_total": 179, "naive_total": 332, "declared_reduced": 179, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=179, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

Actual direct author-checker output, inserted directly from skeptic/author_checker.txt:

```text
{"file": "2x5x6_m47_cr179_ZT_reduced.json", "format": "2x5x6", "rank": 47, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 38, "adds_V": 65, "adds_W": 76, "adds_total": 179, "naive_total": 332, "declared_reduced": 179, "VALID": true}
```

Actual repeat/comparison output, inserted directly from skeptic/comparison.txt:

```text
output.txt == output.repeat.txt: byte-identical PASS; SHA256=fc69e78ad72c6b27cff9e900fc95fc6cb73e1c7b8ad3a3053e980283411d2881
author_checker.txt == author_checker.repeat.txt: byte-identical PASS; SHA256=8f5ad77c203a4327465dc6c4177fd058e9dd2a6f6261e9983f53cbcec75e82f9
Author versus independent: format, products, layout, exactness, U/V/W/total/naive counts agree PASS
Both author wrapper runs: identical JSON result and ALL CHECKS PASS
Wrapper raw logs differ: initial run includes two Xcode runtime diagnostics;
these are retained verbatim in author_output.txt; direct checker outputs are byte-identical.
```

Comparison and mismatches: there is no disagreement on format, product count, exactness, transposed output layout, object hash, or any addition count. The author's negative control is rejected. Its random trials are supplementary; the independent verification above is exhaustive over coefficients and basis inputs.

Two limitations of the author's tooling are visible from inspection. check_slp.py expands forms but never checks that expanded coefficients remain ternary; it only validates the written signs. Also its VALID flag does not require the counted total to equal declared_reduced (the wrapper separately checks 179). These are coverage gaps, not counterexamples for this object: the independent checker explicitly verifies expanded ternarity and both declared counts. The optional sympy checker was not needed or run because the full exact integer tensor identity already supplies the symbolic proof.

The first author-wrapper log contains two Xcode runtime startup diagnostics absent from the second wrapper log, so those raw wrapper logs are not byte-identical. Both complete logs are preserved and pasted above. Their checker JSON and verdicts agree, and direct invocations of the author checker are byte-identical; these startup diagnostics do not arise from the saved SLP or its arithmetic. No mathematical mismatch, missing required local object, or nondeterministic object/checker result was found. The scoped saved-object verdict is therefore pass.

pass: true
