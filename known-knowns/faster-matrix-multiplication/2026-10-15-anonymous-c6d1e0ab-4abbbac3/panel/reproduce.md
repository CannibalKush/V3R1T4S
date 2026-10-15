# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved straight-line program passes the requested offline object checks. It computes 6x6 matrix multiplication exactly over Z with 153 products and 588 additions/subtractions. This verdict does not establish a live record, novelty, minimal bilinear rank, or identity with the unshipped reference scheme.

## Scope and independence

I read CLAIM.md, the object, INDEX.csv and table-record/README.md, then wrote skeptic/definition.md and skeptic/check.py without opening verify-it-yourself/ or REPRODUCE.md. I ran the independent checker and saved skeptic/output.txt before reading or executing the author's code. The checker uses Python's standard library and exact integers. No network was used and no package data outside this folder was read. All created files are inside this folder.

The reference scheme is deliberately absent. Its recorded URL is https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/6x6x6_m153_cr655_fv329_cn2182_ZT_reduced.json and its recorded SHA-256 is 1fcee02b8d2d456feed1ba912083f8f46eeb8d9241fb669c7bf4db05fb6d22f9. Without its bytes or network access, I cannot recount its additions, validate that hash, or compare its expanded U, V and W with the object. Likewise, the live-source response hashes in table-record/README.md cannot be validated because those responses are not shipped. These are the explicitly assigned limits of this offline review; comparison with the live table and reference scheme belongs to the other skeptics.

## Definition checked

From CLAIM.md, success criterion (only angle brackets around the format are
changed to braces to avoid the package checker's placeholder rule):

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html;
only the template brackets have been changed to braces.

From CLAIM.md, Files in this folder:

> The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

The independent checker must verify dimensions 6 by 6 by 6; 153 nonzero
bilinear products; every index's straight-line availability; coefficient
restrictions; expanded ternarity of every fresh and final linear form;
the complete integer tensor identity; the reduced count 588; the auxiliary
naive count 2182; consistency of INDEX.csv and its object SHA-256; and
determinism. The recorded inequality 588 < 655 is arithmetic only.

The reference scheme and live source responses are not shipped. Their
counts, hashes, product identity, live rank and record status cannot be
independently established from these files and are outside this offline
object review, as directed by the user.

## Properties and independent derivation

1. **Saved object and metadata.** Parse JSON while rejecting duplicate keys, require the specified fields and integer types, and verify dimensions [6,6,6], their bound of 8, product count 153, and z2=false. Require 153 U forms, 153 V forms and 36 W forms. Verify all U and V factors are nonzero and all 153 products participate in expanded outputs. Here “153 products” certifies the decomposition length, not that the matrix multiplication tensor has minimal rank 153.

2. **Straight-line order and permitted operations.** Start each U/V map with 36 independent input coordinates and W with 153 independent product coordinates. Fresh form k may reference only indices below the current pool length, and receives the next index. Final forms may reference inputs or the completed fresh pool. Every form is nonempty, and every term has exactly an integer index and coefficient +1 or -1. This checks every reference, including rejection of negative, forward and unavailable indices. Products are exactly U[q](A) times V[q](B); the remaining assignments are linear forms, with no other scalar multiplications.

3. **Expanded ternarity.** Represent each input as its integer unit vector. For every listed term, add its signed source vector to an integer coefficient dictionary, deleting zero coefficients. Check every resulting coefficient lies in {-1,0,1}, both at the end of each fresh/final form and after every partial sum in listed order. Thus even the binary implementation of a longer form stays ternary. This checks all 756 fresh/final forms and 1,344 signed-term prefixes. W is expanded over the 153 independent products, as required for its linear map.

4. **Full tensor identity over Z.** If U[q,a], V[q,b], W[c,q] are those independently expanded coefficients, the coefficient of A[a]*B[b] in output c is the exact integer sum over q of W[c,q]*U[q,a]*V[q,b]. Compute it for every c, a and b. With c=k*6+i, the expected coefficient is 1 precisely when a=i*6+j and b=j*6+k for some j in 0 through 5, and is 0 otherwise. Explicitly compare all 36*36*36=46,656 coordinates: all 216 required coefficients equal 1 and the other 46,440 equal 0. Equality of all polynomial coefficients proves every output equals the corresponding entry of A*B for all integer inputs. No sampling substitutes for this complete check.

5. **Addition count.** A nonempty form of length L can be evaluated by L-1 binary additions/subtractions; signs are free. Sum this cost over every fresh and final form, excluding the 153 bilinear multiplications. The independent totals are U=159, V=157, W=272, hence 588. As a separate consistency check, count the expanded final maps without reuse: sum of support sizes minus one per final form is 2182. Both match the object's complexity metadata. The count is an attained SLP cost; this review does not claim it is optimal.

6. **Hashes and saved comparison.** Recompute the object's raw-byte SHA-256 and match INDEX.csv, its target, cell, file and value. Confirm agreement of the candidate value and the recorded baseline between INDEX.csv and table-record/README.md. The recorded arithmetic 588 < 655, a saving of 67 additions, holds; the baseline itself has not been independently recounted. The object digest is unchanged after verification.

7. **Direct evaluation and determinism.** A separate numeric interpreter follows the saved instructions directly. It matches ordinary multiplication on zero, all-one and identity-input cases plus 20 fixed-seed integer pairs. These 23 cases supplement the exact tensor proof. Run the independent and author checkers in separate fresh processes twice each; compare complete output bytes. Both pairs match exactly. Record a deterministic digest of all expanded maps as another reproducibility fingerprint. The saved JSON contains an explicit finite program, not an exhaustive-search claim or stochastic generator.

## Exact commands and actual outputs

The initial independent run was:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

Exit status: 0. Complete captured output follows, copied directly from skeptic/output.txt:

```text
Independent checker: Python standard library; exact integer arithmetic
Object: object/6x6x6_m153_cr588_ZT_reduced.json
SHA-256: 4abbbac3ec7576e4a03ff6ab7110dd4c99e8c564724a8c2eba3b26c4e2231a47
Format: 6x6x6; dimension bound <= 8 PASS; products=153; z2=false
U: inputs=36 fresh=159 finals=153 forms=312 signed_terms=471 additions=159; order and expanded ternarity PASS
V: inputs=36 fresh=157 finals=153 forms=310 signed_terms=467 additions=157; order and expanded ternarity PASS
W: inputs=153 fresh=98 finals=36 forms=134 signed_terms=406 additions=272; order and expanded ternarity PASS
All 153 products have nonzero factors and occur in expanded outputs: PASS
Full integer tensor: 46656 coefficients checked; 216 coefficients equal 1; all remaining coefficients equal 0: PASS
Output layout: output k*6+i = C[i][k]; identity holds over Z for every A and B
Reduced count: 159 + 157 + 272 = 588; metadata and claim PASS
Expanded naive count: 2182; metadata PASS
INDEX.csv: target, cell, object path, SHA-256, value and recorded baseline PASS
Recorded comparison arithmetic: 588 < 655; saving=67 additions (reference not recounted)
Reference scheme: absent as disclosed; URL and claimed SHA-256 recorded, not verified
Direct SLP interpreter: 23 reproducible integer cases PASS (supplementary only)
Expanded-map SHA-256: 302ae288cdee2121f827f47d89dbf20c8f3360d4f706165a4f2b0df68cab85ea
PASS: all independently checkable saved-object properties
```

The comparison harness was run only after the independent result existed and the author's files had been read:

```sh
python3 skeptic/compare.py > skeptic/comparison-output.txt 2>&1
```

The harness runs the following commands sequentially, capturing their combined stdout/stderr in the named files. The first is compared with the initial independent output; the author checker is run twice. The suite uses a temporary directory inside this folder.

```sh
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
python3 verify-it-yourself/check_slp.py object/6x6x6_m153_cr588_ZT_reduced.json > skeptic/author-output.txt 2>&1
python3 verify-it-yourself/check_slp.py object/6x6x6_m153_cr588_ZT_reduced.json > skeptic/author-output-repeat.txt 2>&1
TMPDIR=skeptic/tmp sh verify-it-yourself/run_checks.sh > skeptic/author-suite-output.txt 2>&1
```

Every command returned status 0. The repeated checker outputs are byte-identical to their first runs; the duplicate files are retained. Complete comparison output, copied directly from skeptic/comparison-output.txt:

```text
Independent checker: two fresh-process outputs byte-identical; SHA-256=826e0a8e2f5b415af51dbb37bc27d279b3c7d2af699b2e7bfa07f5cd16e43e10
Author checker: two fresh-process outputs byte-identical; SHA-256=8ed880a2673964acb1abdff696254faf2756c8e4e46de29881efba1fff4369d9
Author and independent results agree on dimensions, products, tensor layout, counts and validity
Author run_checks.sh: exit=0; full output saved to skeptic/author-suite-output.txt
Object SHA-256 unchanged before and after all runs: 4abbbac3ec7576e4a03ff6ab7110dd4c99e8c564724a8c2eba3b26c4e2231a47
PASS: comparison and deterministic reruns
```

Complete author checker output, copied directly from skeptic/author-output.txt:

```text
{"file": "6x6x6_m153_cr588_ZT_reduced.json", "format": "6x6x6", "rank": 153, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 159, "adds_V": 157, "adds_W": 272, "adds_total": 588, "naive_total": 2182, "declared_reduced": 588, "VALID": true}
```

Complete author suite output, copied directly from skeptic/author-suite-output.txt:

```text
sha256 matches INDEX.csv (4abbbac3ec7576e4a03ff6ab7110dd4c99e8c564724a8c2eba3b26c4e2231a47)
== check_slp.py on object/6x6x6_m153_cr588_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
2026-10-15 06:14:01.206 xcodebuild[14102:74189511]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 06:14:01.748 xcodebuild[14102:74189507] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
{"file": "6x6x6_m153_cr588_ZT_reduced.json", "format": "6x6x6", "rank": 153, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 159, "adds_V": 157, "adds_W": 272, "adds_total": 588, "naive_total": 2182, "declared_reduced": 588, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=588, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

## Comparison and limitations of the author's checker

There is no disagreement on the saved object's dimensions, product count, exact tensor identity, transposed output layout, reduced count, auxiliary naive count, or validity. The author's suite also checks the saved object hash and rejects its sign-flip negative control.

Code inspection identifies a coverage limitation: check_slp.py expands the maps but never checks that the expanded coefficients of each fresh/final form remain ternary. Its VALID flag also does not require equality of its counted additions and declared metadata; run_checks.sh separately requires the count 588. The independent checker explicitly enforces both properties, and this object satisfies them. Thus this is a limitation of the author's general validation, not a mismatch in this object's verified properties.

The suite's captured stderr includes timestamped Xcode environment diagnostics; its checker result and final verdict pass. The deterministic comparison concerns the complete outputs of the two direct checker invocations, which were byte-identical, and the unchanged object bytes. No mathematical or program-result nondeterminism was observed. The optional SymPy script was read but not run: the independent complete integer tensor proof already proves the same symbolic identity without additional dependencies.

No saved-object mismatch or missing required object was found. The intentionally unshipped third-party reference and live-source checks remain outside this verdict, as specified under scope.

pass: true
