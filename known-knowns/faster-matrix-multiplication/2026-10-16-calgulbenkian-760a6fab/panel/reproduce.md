# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object passes the independent checks: exact integer matrix multiplication for 5x5x6, 110 nonzero products, ternary expanded forms, valid dependency order, and 413 reduced additions. This verdict concerns the saved object, not a current-record or novelty claim.

## Scope and independence

I read CLAIM.md, the object, INDEX.csv, and table-record/README.md before writing skeptic/definition.md and skeptic/check.py. I ran the independent checker successfully and repeated it before opening REPRODUCE.md or any file in verify-it-yourself/. No author code was imported or used to implement the independent checker. I used python3 and its standard library. No network access was used; no source material outside this folder was inspected.

The reference scheme is deliberately absent. table-record/README.md identifies it at https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/5x5x6_m110_cr460_fv204_cn1215_ZT_reduced.json with recorded sha256 cf3594827381eb28f74442e5c6f1699c24d487fc67791bfa523af08d66e2129e. I cannot recount or hash that absent file offline. I do not confirm product identity with it, its 460 count, the minimum reference count, best-rank status, live-source fetches, current table values, or novelty. Those comparisons belong to the other skeptics. External-source hashes in table-record/README.md are metadata without corresponding saved source bytes and cannot be verified here. The arithmetic inequality against the saved metadata, 413 less than 460, is checked.

## Quoted definitions and criterion

The following counting and layout definition is quoted from CLAIM.md:

> The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

The full success criterion follows. Only the angle brackets around the format parameters have been changed to braces to avoid literal template placeholders. The Lille URL template is written https://fmm.univ-lille.fr/{n}x{m}x{p}.html, with only its template brackets changed; CLAIM.md itself refers to the live per-format page without spelling out that URL template.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

Every locally checkable clause is covered: explicit linear-form SLP and product/output cardinalities; format and dimension bound; exactness over Z; allowed coefficients and dependencies; reduced counting with free negation; and the strict numerical inequality relative to the saved comparison value. The live and third-party clauses are excluded only as specified in Scope.

## Independent proof and checks

1. Parse JSON with duplicate-key rejection. Validate the exact top-level schema, integer dimensions [5,5,6], rank field 110, integer-arithmetic flag, term schemas, integer indices, and signs restricted to +1 or -1. Reject empty forms, zero expanded forms, missing fields, incorrect cardinalities, or unavailable references. The 110 U factors, 110 V factors, and 30 W outputs are all present; every product contributes to at least one output.
2. Start each map from the appropriate unit basis (25 A entries, 30 B entries, 110 product symbols). Expand each fresh variable in order over Z, then the final forms. Require every coordinate of every expanded form to be in {-1,0,1}. This checks all 296 fresh variables and all 250 final forms, not merely the written signs. Fresh index k is interpreted as input count plus k; final forms cannot introduce additional variables.
3. Certify a binary realization of every multi-term form. For each subset of signed operands, compute its exact expanded vector. A subset is admissible only if its vector is ternary. Recursively split it into two disjoint admissible subsets, terminating at operands. Save the resulting trees in skeptic/binary_witness.json. This establishes ternary coefficients even at the implicit binary intermediates, with L-1 binary operations for a form with L operands. Term negations cost zero.
4. Re-derive the tensor identity: if U[q,a] and V[q,b] are the expanded input factors and W[o,q] the expanded output map, the coefficient of A[a]*B[b] in output o is the integer sum over q of W[o,q]*U[q,a]*V[q,b]. Construct all coefficients. For output o, use row o mod 5 and column floor(o/5), exactly the required transposed storage. For A index a use row floor(a/5), inner a mod 5; for B index b use inner floor(b/6), column b mod 6. The expected coefficient is 1 precisely when both output indices and the inner indices match, and otherwise 0. Compare every one of 30*25*30 = 22,500 coefficients: 150 ones and 22,350 zeros. Equality of all coefficients proves the polynomial identity for arbitrary integer inputs. This is a complete finite symbolic check, not a sample.
5. Sum L-1 over every fresh and final form. U costs 108+0, V 114+0, W 128+63, totaling 413. Exclude 110 bilinear products and free negations. Independently count nonzero expanded coefficients to obtain naive count nz(U)+nz(V)+nz(W)-2*110-30 = 1215. Both counts agree with object metadata; the reduced count agrees with INDEX.csv and satisfies 413 less than the saved 460 by 47.
6. Separately execute the saved SLP directly on zero matrices, all-one matrices, and 32 reproducibly generated integer cases. These 34 cases supplement the exhaustive tensor proof; they are not its basis.
7. Hash the original object bytes and match INDEX.csv, including its relative filename, target, cell, and count fields. Re-read to ensure byte stability. Record hashes of expanded maps/tensor and binary witness. Repeat in fresh Python processes and compare entire checker output. Repeat the author suite and standalone checker as well, and check the object hash again afterward.

## Regrouping diagnostic and mismatches

There is no mismatch with the stated form-sum definition. During development, I initially imposed an additional left-to-right accumulation assumption. It detected this diagnostic (copied from skeptic/initial_diagnostic.txt):

```text
AssertionError: W/final/6: nonternary expanded partial sum
```

The definition represents a form as a sum and does not prescribe left associativity. I corrected that extra assumption before viewing any author code and constructed binary witnesses instead. W/final/6 is the only form needing regrouping to keep its binary intermediates ternary. Its five signed operands, in stored order, are x180, x179, -x171, -x159, x32, with xj denoting W-map variable j. The certified order is (((x180+x32)-x159)-x171)+x179, using four additions/subtractions and only existing operands. Its expanded final form and each binary intermediate are ternary. No object bytes or addition counts were changed. A Python-version compatibility issue in the development checker was also corrected before the author comparison.

The author's check_slp.py validates written term signs but does not explicitly assert that every expanded coefficient is ternary; its VALID flag alone would therefore be insufficient for that property. The independent checker supplies that missing check and also checks the implicit binary intermediates. This is a verification-coverage limitation, not a disagreement on this object.

The first author-suite invocation emitted two macOS xcodebuild startup diagnostic lines containing varying timestamps/process IDs. Its complete combined stream is preserved in skeptic/author-initial-output.txt; the next combined stream is skeptic/author-initial-repeat.txt. skeptic/compare_runs.py verifies that removing exactly those two toolchain diagnostics makes the streams identical, and that the remaining verifier output equals subsequent runs. Subsequent separate stdout captures are byte-identical and stderr captures empty. No object, count, tensor, or verifier-result nondeterminism was observed. The initial system diagnostic stream itself was not byte-identical, and is disclosed here rather than suppressed from the record.

## Exact commands and captured output

All commands were run from this folder. The independent run was completed before any author-code read:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output-repeat.txt
```

The full independent output below is inserted directly from skeptic/output.txt:

```text
Independent saved-object verification; exact Python integers
object: object/5x5x6_m110_cr413_ZT_reduced.json
sha256: 760a6fabaf3fef7778e29b48d9b96dca9ae9dc8686afa84060805ac3be723354
format: 5x5x6; max dimension <= 8; products: 110; INDEX metadata/hash OK
U: inputs=25, fresh=108, finals=110, additions=108+0=108, ternary_forms=218, ternary_binary_results=108; order OK
U: binary ternary parenthesizations certified; forms requiring regrouping=0
V: inputs=30, fresh=114, finals=110, additions=114+0=114, ternary_forms=224, ternary_binary_results=114; order OK
V: binary ternary parenthesizations certified; forms requiring regrouping=0
W: inputs=110, fresh=74, finals=30, additions=128+63=191, ternary_forms=104, ternary_binary_results=191; order OK
W: binary ternary parenthesizations certified; forms requiring regrouping=1
binary witness sha256: 1ddfd6576872008972955d18bf02a5f5b7d3413e66d3e319ab243c8190701fea
count: reduced=413; naive=1215; saved comparison: 413 < 460 (difference 47)
full tensor identity over Z: 22500 coefficients checked; 150 ones, 22350 zeros; all equal A*B
direct ordered SLP execution: 34 deterministic integer cases OK (supplemental to full proof)
expanded maps/tensor sha256: 73676d81686461e5f695584e0b5c7a7574fe8c7a9177661c62e436ca69f7a3cf
object byte stability: OK
scope: third-party reference bytes and live sources absent; no reference recount or product-identity/live-table verdict
PASS: every saved-object property checked
```

Afterward, the author's suite was first run twice with combined output (preserved as the initial logs described above). The recorded clean runs used:

```sh
TMPDIR="$PWD/skeptic" sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2> skeptic/author-stderr.txt
TMPDIR="$PWD/skeptic" sh verify-it-yourself/run_checks.sh > skeptic/author-output-repeat.txt 2> skeptic/author-stderr-repeat.txt
python3 verify-it-yourself/check_slp.py object/5x5x6_m110_cr413_ZT_reduced.json > skeptic/author-checker.txt 2> skeptic/author-checker-stderr.txt
python3 verify-it-yourself/check_slp.py object/5x5x6_m110_cr413_ZT_reduced.json > skeptic/author-checker-repeat.txt 2> skeptic/author-checker-stderr-repeat.txt
python3 skeptic/compare_runs.py > skeptic/determinism.txt 2>&1
```

TMPDIR keeps the author's negative-control temporary files inside skeptic/. The full suite output is inserted directly from skeptic/author-output.txt:

```text
sha256 matches INDEX.csv (760a6fabaf3fef7778e29b48d9b96dca9ae9dc8686afa84060805ac3be723354)
== check_slp.py on object/5x5x6_m110_cr413_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x5x6_m110_cr413_ZT_reduced.json", "format": "5x5x6", "rank": 110, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 108, "adds_V": 114, "adds_W": 191, "adds_total": 413, "naive_total": 1215, "declared_reduced": 413, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=413, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

The standalone author-checker output is inserted directly from skeptic/author-checker.txt:

```text
{"file": "5x5x6_m110_cr413_ZT_reduced.json", "format": "5x5x6", "rank": 110, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 108, "adds_V": 114, "adds_W": 191, "adds_total": 413, "naive_total": 1215, "declared_reduced": 413, "VALID": true}
```

The comparison output is inserted directly from skeptic/determinism.txt:

```text
skeptic/output.txt == skeptic/output-repeat.txt: byte-for-byte identical
output sha256: 361421acc736e7543304eb20e335fff994b8230463a1f84b325b0449ebf146a6
skeptic/author-output.txt == skeptic/author-output-repeat.txt: byte-for-byte identical
output sha256: b5f923237c33508b80909e12d6b6ddfeaa293c7c41698398fadcfded4e4d9578
skeptic/author-checker.txt == skeptic/author-checker-repeat.txt: byte-for-byte identical
output sha256: 0403107e416d62c9d9c0c210adcf0206d150e5a9ee8fe02c874170e5711a3765
repeated author suite and standalone checker stderr: empty
initial combined-stream difference: exactly 2 macOS xcodebuild startup diagnostics; all verifier output identical
object sha256 after independent and author runs: unchanged
Both author runs ended ALL CHECKS PASS; no disagreement on tensor, layout, rank, or counts.
```

The optional author SymPy cross-check was not needed or run: the independent integer tensor proof already checks every coefficient. All saved-object properties within the requested scope are confirmed.

pass: true
