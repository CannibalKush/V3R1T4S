# Independent REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

## Scope and independence

This verdict covers the saved straight-line program: exactness over Z, ternarity of every expanded form and binary intermediate, dependency order, dimensions, 100 products, reduced and naive counts, the object hash and INDEX consistency, and deterministic execution. I read CLAIM.md, the object, INDEX.csv, table-record/README.md and REPRODUCE.md, wrote skeptic/check.py, and successfully ran it to skeptic/output.txt before opening any file in verify-it-yourself/. The independent checker uses Python's standard library and integer arithmetic and imports no author code. No network was used and no external claim-package files were inspected. The supplied virtual environment was used only as an interpreter/runtime for the later checks.

The reference scheme is deliberately absent as third-party data. table-record/README.md identifies it as https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x8x8_m100_cr424_cn608_ZT_reduced.json and records SHA256 215daedef7b298b38533f63b0ea2f7e8ee0a460f13848b5071a39fb0bc939250. Without network I cannot recount it, verify that hash, or establish product-identity with this object. I also cannot authenticate the other recorded source-page hashes, the live best rank, or the live table minimum. Those questions belong to the other two skeptics. Comparing the saved numbers establishes only 418 < 424, a difference of six. This is a scoped saved-object verdict, not a finding of novelty or a current table record. All locally required files are present; the expressly excluded reference is not treated as a missing candidate object.

## Quoted definition and success criterion

The success criterion below is quoted from CLAIM.md. I changed only the angle brackets around n,m,p to braces to avoid template-placeholder rejection. For the requested Lille URL-template notation, I write https://fmm.univ-lille.fr/{n}x{m}x{p}.html, changing only the brackets.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The saved-object definition, including the counting convention, is:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

Every clause checkable locally is covered: explicit SLP representation, dimension bound, declared product count, exact symbolic integer product, reduced-convention operation count, allowed scalars, ternary expanded intermediates, and the arithmetic inequality against the saved reference number. Equality to a live best rank, live minima across all repository files, the coefficient-class comparison to live catalogues, prior scheme claims and whether this also improves a known rank require external evidence and are not certified here. The enumerated partial wins are alternative targets, not claims made for this one object.

## Properties checked and proof re-derived

1. **Object and structure.** Parse the JSON with duplicate-key rejection. Check the exact expected keys, integer dimensions [2,8,8], dimension bound 8, integer product count 100, z2=false, 100 U rows, 100 V rows and 16 W rows. Require nonempty forms, precisely index/value terms, integer indices and literal integer signs +1 or -1. Each fresh form may reference inputs and strictly earlier fresh variables; each final form may reference inputs and all previously completed fresh variables. The three stages therefore admit a linear-stage / 100-products / linear-stage execution order. All 100 products have nonzero factors and output contributions. This establishes a 100-product bilinear representation; optimal tensor rank requires external comparison.

2. **Expansion and ternarity.** Start U with the 16 standard basis vectors for row-major A, V with 64 basis vectors for row-major B, and W with 100 basis vectors for the product values. For each signed term, add or subtract its already expanded source vector using exact integers. By induction on dependency order, the resulting vector is the form's exact expansion. Check every coordinate is in {-1,0,1}, including every prefix in the listed left-to-right binary evaluation. This checks all 363 saved fresh/final forms and all 781 prefixes, and also constructs a ternary binary implementation for each longer form. No unlisted scalar multiplications are needed.

3. **Full tensor identity.** For each output row c=k*2+i, each A coordinate a and each B coordinate b, compute sum over q=0..99 of W[c,q]*U[q,a]*V[q,b]. Require exactly 1 when a=i*8+j and b=j*8+k for some j, and exactly 0 otherwise. All 16*16*64=16,384 coefficients are checked, including zero coefficients; 128 are ones and 16,256 are zeros. Since the SLP is bilinear, these monomials form a complete basis. The coefficient equality proves every output is sum over j of A[i,j]*B[j,k] exactly over Z, for all inputs. No numeric sample substitutes for this proof.

4. **Execution cross-check.** Execute the actual dependency lists, independently of vector expansion, on all 16*64=1,024 pairs of input basis matrices and compare with direct matrix multiplication in the stipulated transposed output order. Supplement with zero, all-one, and 64 seeded signed-integer cases, each executed twice. The samples are supplementary only. This claim is not an exhaustive-search or optimality claim; no search completeness is asserted.

5. **Counting.** A form with L signed terms can be evaluated as a left fold with L-1 binary additions/subtractions, with signs free. The prefix checks establish that implementation also stays ternary. Count every fresh and final form, excluding the 100 bilinear multiplications. U costs 90+0=90, V costs 16+138=154, and W costs 54+120=174, giving 418. Equivalently, 781 terms minus 363 forms gives 418. The expanded naive formula nz(U)+nz(V)+nz(W)-2*100-16 independently gives 608. Both match the JSON metadata; the reduced value also matches the filename, CLAIM.md and INDEX.csv.

6. **Hashes and saved records.** Compute SHA256 over the object's raw bytes and compare with INDEX.csv, also checking its target, cell, relative filename, value 418 and saved reference value 424. The exact object SHA256 is 674e65a792736a9bf4930d7e529fb901990cafa22ddf52baaf6c2ed0d256a87f. Record SHA256 values of all eight original package files before and after the repeated checks; none changes. Only the object has a shipped expected-content hash that can be authenticated against its saved bytes. Hashes for unshipped third-party pages remain unauthenticated.

7. **Determinism and author comparison.** Repeat the independent checker in separate processes and compare its entire output byte for byte with the original output. Run the author's shell check and SymPy check twice each with the supplied virtual environment pinned; each exits zero and produces byte-identical complete output. The author's checker agrees on transposed output order, all counts and the exact tensor identity; its sign-flip negative control is rejected. SymPy expands all symbolic outputs and independently confirms the same product. Inspection reveals that the author's check_slp.py does not itself check ternarity of expanded intermediate vectors, despite REPRODUCE.md's description; my independent checker verifies that extra property for this object. There is no mathematical or count disagreement.

## Independent command and actual output

Run from this folder, before inspecting the author's checker:

```sh
python3 skeptic/check.py object/2x8x8_m100_cr418_ZT_reduced.json > skeptic/output.txt 2>&1
```

Exit status: 0. The following is pasted directly from skeptic/output.txt:

```text
Independent checker: Python integer arithmetic; no network; no author imports
object: object/2x8x8_m100_cr418_ZT_reduced.json
object sha256: 674e65a792736a9bf4930d7e529fb901990cafa22ddf52baaf6c2ed0d256a87f
format: 2x8x8; dimension bound <= 8 PASS; products: 100; arithmetic: Z
U: inputs=16 fresh=90 final=100 additions=90+0=90; order/scalars/expanded ternarity PASS; binary prefixes=280 max_abs=1
V: inputs=64 fresh=16 final=100 additions=16+138=154; order/scalars/expanded ternarity PASS; binary prefixes=270 max_abs=1
W: inputs=100 fresh=41 final=16 additions=54+120=174; order/scalars/expanded ternarity PASS; binary prefixes=231 max_abs=1
100/100 products have nonzero factors and nonzero output contribution PASS
Full tensor identity: 16384/16384 integer coefficients match; 128 ones, 16256 zeros PASS
Reduced count: 90 + 154 + 174 = 418; metadata and claim agree PASS
Expanded naive count: 608; metadata agrees PASS
Arithmetic comparison with saved reference number only: 418 < 424; difference=6 PASS
Direct SLP execution: all 1024 input-basis pairs match A*B PASS
Supplementary integer execution: 66 fixed/seeded cases, each repeated identically PASS
INDEX: object path, SHA256, target, cell and saved counts agree PASS
Offline scope: live minima/best rank, source-page hashes and unshipped reference identity/recount NOT CHECKED
SAVED OBJECT CHECKS PASS
```

## Author commands and actual output

The first shell invocation was `TMPDIR=skeptic sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1` and exited 0. Its full log is preserved in [skeptic/author-output.txt](skeptic/author-output.txt); macOS emitted launcher/cache warnings on that initial invocation. A default-interpreter SymPy invocation, `python3 verify-it-yourself/sym_check.py object/2x8x8_m100_cr418_ZT_reduced.json > skeptic/author-symbolic-output.txt 2>&1`, exited 1 because that interpreter lacks SymPy. Its unmodified traceback is retained in [skeptic/author-symbolic-output.txt](skeptic/author-symbolic-output.txt). This is an interpreter dependency issue, not an object disagreement. Retrying with the supplied runtime succeeded:

```sh
../../../.venv/bin/python verify-it-yourself/sym_check.py object/2x8x8_m100_cr418_ZT_reduced.json > skeptic/author-symbolic-venv-output.txt 2>&1
```

Exit status: 0. Actual output:

```text
{"file": "2x8x8_m100_cr418_ZT_reduced.json", "format": "2x8x8", "rank": 100, "products": 100, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 418}
```

The complete repeatability command below pins the same supplied virtual environment on PATH for the author's shell script, and captures each subprocess's combined stdout/stderr in skeptic/. For direct reproduction, the equivalent pinned shell invocation is:

```sh
PATH="../../../.venv/bin:$PATH" TMPDIR=skeptic sh verify-it-yourself/run_checks.sh
```

The actual first pinned shell run, saved by the repeatability checker in skeptic/author-shell-run1.txt, exited 0 and printed:

```text
sha256 matches INDEX.csv (674e65a792736a9bf4930d7e529fb901990cafa22ddf52baaf6c2ed0d256a87f)
== check_slp.py on object/2x8x8_m100_cr418_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "2x8x8_m100_cr418_ZT_reduced.json", "format": "2x8x8", "rank": 100, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 90, "adds_V": 154, "adds_W": 174, "adds_total": 418, "naive_total": 608, "declared_reduced": 418, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=418, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

## Repeatability command and actual output

```sh
python3 skeptic/check_reproducibility.py > skeptic/reproducibility-output.txt 2>&1
```

This runs each checker twice in separate processes, requires zero exits, compares complete output bytes, compares independent output with the first pre-author run, and checks all original package hashes before and after. It uses the supplied interpreter by its relative path, with TMPDIR=skeptic for the author's temporary negative-control file. Exit status: 0. Pasted from skeptic/reproducibility-output.txt:

```text
3a9b14f1ef8893a1313f9811c95b6a478b48dff093db40ab48047bc4c33eba05  CLAIM.md
e27bfad7e155b146591247f5c4b2b0c11ec06ee2b0697929f445d2e805e90d5e  INDEX.csv
b91103540299c4e4680d3719aad97f811ba284e65d08fa0b2e2412b5b9865cd4  REPRODUCE.md
674e65a792736a9bf4930d7e529fb901990cafa22ddf52baaf6c2ed0d256a87f  object/2x8x8_m100_cr418_ZT_reduced.json
7b36792b58bf69ea9674d518868a0be899a69c2439c3970976494d4ba31b5b40  table-record/README.md
dea835d4a2e797112ab6d25f35149ce48feba5b3431a5f1d1de1d42086aab110  verify-it-yourself/check_slp.py
7fddb394313bcc8129dfd68073a01b27a3437a91a2730a26a1bb7327fc6891fd  verify-it-yourself/run_checks.sh
5f16abd59b3dc1b5737529b37984a34e90f53b20afb4e77e0297ad75fcc063de  verify-it-yourself/sym_check.py
independent: 2/2 exit=0; full output byte-identical; output sha256=f1f6fb67c3019a765062f8ae88434de2ad856652f8373c88d03e09b4933bd926 PASS
author-shell: 2/2 exit=0; full output byte-identical; output sha256=cedca188db026d56a28f93a44df6ed98b0669011b56bbd5383368473d79c1a9c PASS
author-symbolic: 2/2 exit=0; full output byte-identical; output sha256=bb105da25b3cfdb846632004f3c21a9bdc4a0f96a62055df2ab208189b5476d7 PASS
Original package files: 8/8 SHA256 values unchanged across all repeated checks PASS
REPRODUCIBILITY PASS
```

The six full repeated-run logs are skeptic/independent-run1.txt, skeptic/independent-run2.txt, skeptic/author-shell-run1.txt, skeptic/author-shell-run2.txt, skeptic/author-symbolic-run1.txt and skeptic/author-symbolic-run2.txt. The additional early repeat is skeptic/output-repeat.txt. No nondeterminism was observed in the object computation or complete checker outputs under the pinned interpreter. The initial system-launcher diagnostic lines are preserved separately and are not SLP outputs.

## Verdict

All saved-object properties in scope are confirmed. No object mismatch, invalid coefficient, missing candidate component, invalid dependency, count discrepancy, hash discrepancy or computational nondeterminism was found. The author's incomplete expanded-ternarity check and the default interpreter's missing optional dependency are documented above and resolved for this verification by the independent exhaustive check and the supplied runtime. The unshipped reference and live comparisons remain explicitly outside this offline skeptic's verdict.

pass: true
