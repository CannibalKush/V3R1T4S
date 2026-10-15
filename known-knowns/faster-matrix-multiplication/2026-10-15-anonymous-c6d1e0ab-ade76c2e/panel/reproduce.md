# Independent reproduction report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved straight-line program passes the properties assigned to this offline skeptic. Its tensor identity is exact over Z, all expanded linear forms and binary prefixes are ternary, and the reduced addition count is 469.

## Scope and independence

I read CLAIM.md, the saved object, INDEX.csv and table-record/README.md. I wrote skeptic/definition.md and skeptic/check.py from the definition, then ran the independent checker and saved skeptic/output.txt before opening REPRODUCE.md or anything in verify-it-yourself/. The independent checker uses only Python's standard library. No network was used and no other project files were inspected outside this folder.

The Perminov reference scheme is third-party data and is deliberately absent. table-record/README.md identifies its source as https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x6x7_m123_cr517_cn1586_ZT_reduced.json and records SHA-256 8c385f50b3e85e7c750e6ace7e1e3b835e2fdf3f348f8ff9ae94931a755367dd. Without network I cannot recount it, verify its hash, or establish that its expanded products coincide with this object's. The other two skeptics handle reference-product identity, live-table comparison, best listed rank, coefficient-class comparisons and novelty. The metadata hashes for unshipped fetched pages cannot be validated from the package. The scoped pass below does not certify those external claims. I checked only the arithmetic inequality against the recorded 517, not the correctness or currency of that reference value.

This is verification of a supplied object, not an exhaustive optimization search. No search transcript or optimality proof is claimed. The full tensor comparison is exhaustive; random matrix trials are supplementary.

## Quoted definition and criterion

The saved-file layout and counting definition in CLAIM.md is:

> The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

The complete success criterion in CLAIM.md is quoted here to distinguish locally checkable clauses from external ones:

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

In that quotation I changed only the format's angle brackets to braces, to avoid literal template placeholders. The Lille URL template requested for this report is https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only its placeholder brackets have been changed to braces. CLAIM.md itself names the live Lille per-format page without spelling out a URL template.

The exactness condition checked is “(1) is verified symbolically to compute the full product A*B exactly over Z”. The counting and scalar condition checked is “each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP”.

## Properties and independently re-derived proof

1. **Saved data, dimensions and product count.** Strict JSON parsing rejects duplicate keys. The schema, integer types, dimensions [4,6,7], maximum dimension 7, integer-arithmetic flag, 123 U factors, 123 V factors and 28 W outputs all pass. The 123 ordered pairs of nonzero factor rows are distinct. This proves a bilinear algorithm with 123 products; it does not prove a minimum tensor rank.
2. **Straight-line order and exact expansion.** Each input begins as a standard integer basis vector. At fresh assignment k, the checker requires every index to be less than the input count plus k; final forms can use only inputs and constructed fresh variables. Each form is nonempty and each scalar is the integer +1 or -1. Inductively, adding the signed source basis vectors produces exactly the linear form computed by that assignment. Fresh variables are appended only after their forms are checked. The checker expands all 328 fresh assignments and all 274 final forms, without relying on the author's code or a sampled subset.
3. **Ternary condition.** Every expanded vector has coefficients in {-1,0,1}. This holds for every one of the 1,071 term prefixes as well, so each multi-term form can be evaluated in its listed order as binary additions/subtractions while maintaining the ternary property over that map's inputs. W is expanded over the 123 product symbols. No non-unit scalar multiplication is used.
4. **Full integer tensor identity.** Let U[q,a] and V[q,b] be the independently expanded factors, and W[c,q] the expanded output map. Distributivity gives coefficient T[c,a,b] = sum_q W[c,q] U[q,a] V[q,b] for the monomial A[a]B[b]. For output c=k*4+i, matrix multiplication requires coefficient 1 precisely when a//6=i, b%7=k and a%6=b//7, and 0 otherwise. The checker compares every one of 28*24*42=28,224 integer coefficients: all 168 required ones and all 28,056 required zeros agree. Distinct commuting input symbols make coefficient equality a symbolic proof of each output polynomial over Z. This proves all 28 entries, with the exact transposed output order stated in CLAIM.md.
5. **Reduced counting convention.** A length-L form requires L-1 binary additions/subtractions when evaluated in order. U costs 114, V costs 140, W fresh forms cost 143 and W final forms cost 72: 114+140+143+72=469. This also equals 1,071 terms minus 602 forms. Unary sign changes and the 123 bilinear products contribute no additions. The count agrees with complexity.reduced, the filename and INDEX.csv. Recounting the expanded factor/output supports gives the metadata's naive count 1,586. The recorded numerical comparison is 469 < 517, a difference of 48.
6. **Actual execution.** A separate numeric executor runs the saved assignments themselves, multiplies their 123 factor pairs, and evaluates W. The zero pair, all-ones pair and 16 seeded integer matrix pairs agree with direct multiplication. These 18 trials supplement the exhaustive symbolic proof.
7. **Hashes and metadata.** The object's SHA-256 is ade76c2eef28cca082e6f87f2ca0294f6a6e5bcdce1e1cb9356fe068bab0dd65, exactly the INDEX.csv digest. The target, cell, filename, claimed value and recorded table value agree with saved metadata. The object bytes are unchanged during each run.
8. **Determinism.** Two fresh independent-checker processes exit 0 and produce byte-identical complete outputs. Two fresh author-checker processes also exit 0 and produce byte-identical JSON outputs. Deterministic integer arithmetic establishes the result; the random trials use fixed seeds.

## Exact commands and captured output

All commands run from this folder. The independent checker commands were:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output-repeat.txt
```

Both checker runs and cmp exited 0. The full actual contents of skeptic/output.txt are pasted directly below:

```text
Independent checker: Python standard library, exact integers, no network
object=object/4x6x7_m123_cr469_ZT_reduced.json
sha256=ade76c2eef28cca082e6f87f2ca0294f6a6e5bcdce1e1cb9356fe068bab0dd65
format=4x6x7; max_dimension=7 <= 8; products=123; arithmetic=Z
U: inputs=24 fresh=114 finals=123 additions_fresh=114 additions_final=0 additions=114
U: arities={1: 123, 2: 114}; all references earlier, all stored forms and 351 term prefixes ternary
V: inputs=42 fresh=140 finals=123 additions_fresh=140 additions_final=0 additions=140
V: arities={1: 123, 2: 140}; all references earlier, all stored forms and 403 term prefixes ternary
W: inputs=123 fresh=74 finals=28 additions_fresh=143 additions_final=72 additions=215
W: arities={1: 3, 2: 42, 3: 25, 4: 10, 5: 18, 6: 3, 7: 1}; all references earlier, all stored forms and 317 term prefixes ternary
products: 123 nonzero, distinct ordered pairs of ternary factors
tensor: all 28224 integer coefficients verified; ones=168; zeros=28056
identity: output[k*4+i] = sum_j A[i,j]*B[j,k] exactly over Z
counts: reduced=469; expanded_naive=1586; multiplication/negation charges=0
execution: 18 deterministic integer matrix pairs agree (supplement to exhaustive tensor proof)
INDEX.csv: target, cell, file, SHA-256 and value agree; table-record metadata agrees
recorded comparison only: 469 < 517; improvement=48
scope: no reference file or live tables available; no claim of their validation
object unchanged during run; expanded term prefixes checked=1071
PASS: every saved-object assertion passed
```

The captured determinism evidence in skeptic/determinism.txt is:

```text
Two fresh python3 processes exited 0; full output files are byte-identical.
skeptic/output.txt sha256=0927b466da32a9df76a154d128a0eb72c480044bda6215af1e8d7192fdd9b56d
skeptic/output-repeat.txt sha256=0927b466da32a9df76a154d128a0eb72c480044bda6215af1e8d7192fdd9b56d
```

Only after the independent run, I inspected and ran the author's checker. Commands:

```sh
mkdir -p skeptic/tmp
TMPDIR="$PWD/skeptic/tmp" sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
python3 verify-it-yourself/check_slp.py object/4x6x7_m123_cr469_ZT_reduced.json > skeptic/author-check.txt 2>&1
python3 verify-it-yourself/check_slp.py object/4x6x7_m123_cr469_ZT_reduced.json > skeptic/author-check-repeat.txt 2>&1
cmp skeptic/author-check.txt skeptic/author-check-repeat.txt
```

All exited 0. TMPDIR keeps the author's negative-control temporary files in this folder. The full actual contents of skeptic/author-output.txt are:

```text
sha256 matches INDEX.csv (ade76c2eef28cca082e6f87f2ca0294f6a6e5bcdce1e1cb9356fe068bab0dd65)
== check_slp.py on object/4x6x7_m123_cr469_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
2026-10-15 05:45:43.542 xcodebuild[96707:74098885]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 05:45:43.991 xcodebuild[96707:74098881] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
{"file": "4x6x7_m123_cr469_ZT_reduced.json", "format": "4x6x7", "rank": 123, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 114, "adds_V": 140, "adds_W": 215, "adds_total": 469, "naive_total": 1586, "declared_reduced": 469, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=469, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

The first full standalone author-checker output, repeated byte-for-byte in skeptic/author-check-repeat.txt, is:

```text
{"file": "4x6x7_m123_cr469_ZT_reduced.json", "format": "4x6x7", "rank": 123, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 114, "adds_V": 140, "adds_W": 215, "adds_total": 469, "naive_total": 1586, "declared_reduced": 469, "VALID": true}
```

The author script's platform diagnostics above are retained verbatim; they did not alter the checker results. The optional SymPy script was inspected but not run: the independent standard-library checker already proved the complete symbolic identity.

## Comparison and mismatches

The independent and author results agree on the format, 123 products, C^T layout, exact tensor identity, successful integer evaluation, per-map costs 114/140/215, reduced total 469 and naive total 1,586. The author's sign-flip negative control is rejected.

There is an author-checker coverage limitation: despite its advertised expanded-ternary check, check_slp.py only checks the stored term scalars and never tests expanded row coefficients for membership in {-1,0,1}. It also reports declared_reduced without comparing it to its computed count; the shell wrapper separately checks 469. Neither omission creates a saved-object mismatch: skeptic/check.py independently verifies both properties, including every expanded binary prefix. No saved-object mismatch or result nondeterminism was found. External comparisons remain scoped out as described above.

pass: true
