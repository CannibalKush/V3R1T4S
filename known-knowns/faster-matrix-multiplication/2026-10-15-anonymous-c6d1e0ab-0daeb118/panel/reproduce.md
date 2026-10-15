# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved object passes every locally checkable property in the assigned scope. This is an exact check of the complete saved SLP, not a sampled search check.

**Scope and chronology.** I read CLAIM.md, the saved JSON object, INDEX.csv, and table-record/README.md. I then wrote skeptic/check_slp.py from the quoted definition and completed its first run before opening any file in verify-it-yourself/ or REPRODUCE.md. I used no network and inspected no external claim data. Only after the independent check did I inspect and execute the author's checkers. No subagents were used.

Perminov's reference scheme is deliberately not shipped. table-record/README.md identifies it as https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x6x6_m105_cr430_fv243_cn894_ZT_reduced.json with declared SHA-256 9427b13b5509d45df8c56294f2abe6bc4e478f2aa079a1925e600ca2183739b5. Without network I cannot recount that file or validate its declared hash. The hashes of the other fetched sources in table-record/README.md likewise cannot be validated without their contents. They are metadata, not saved proof objects. This report does not judge current tables, novelty, best-known-rank status, whether all live reference counts were minimized, or product identity with the named third-party schemes. Those comparisons belong to the other skeptics. I confirm that the saved object has 105 nonzero contributing products, not that 105 is a proven minimal tensor rank. I check 373 less than the recorded 430 only as arithmetic, not as independent authentication of 430.

**Quoted definition and success criterion.** In the quotations, only angle brackets have been changed to braces to avoid unfilled-template detection. The Lille URL template is written as https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only its brackets have been changed. CLAIM.md's criterion refers to the Lille per-format page without spelling out that template.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) {= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The saved-object layout and count definition in CLAIM.md:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

The prescribed verification method in CLAIM.md:

> Parse the SLP (sequence of assignments t_k = +/- t_i +/- t_j over inputs A_ij, B_jl, intermediate sums, r products, and output assignments). Evaluate it with sympy (or exact integer evaluation at many random integer matrices plus one symbolic pass) and confirm every output equals the corresponding entry of A*B. Count the additions under the stated convention (exclude negations, exclude the r multiplications). Load the reference scheme from Perminov's addition_reduced_ZT directory (and reduced_known.json), recount its additions with the same counter to calibrate the convention, and compare. Re-fetch the repository, the Lille page and COVERAGE.md. Minutes on this Mac.

**Independent checks and proof.** All arithmetic in skeptic/check_slp.py uses exact Python integers. No author module is imported.

- Parse JSON while rejecting duplicate keys; check the schema, integer dimensions 4x6x6, dimension bound 6 at most 8, exactly 105 U and V outputs, exactly 24 W outputs, and z2 false. Reject empty forms, noninteger indices, and scalars other than integer +1 or -1.
- For each map, initialize its coordinate basis. At fresh step k permit only indices below the input count plus k. Final forms use only inputs or defined fresh variables. Thus there are no cycles, forward references, cross-map references, or extra multiplication operations.
- By induction, replacing every referenced value by its exact basis vector gives the exact expanded coefficients of that form. Check every coefficient of every fresh and final form lies in {-1,0,1}. Additionally check every left-to-right summation prefix is ternary, which exhibits a valid binary realization of every multi-term form. There are 273 fresh forms and 234 final forms, all checked. Every one of the 105 products has two nonzero factors and contributes to W.
- For each of the 24 outputs, expand all products. If U[q,a], V[q,b], and W[c,q] denote the computed coefficients, the coefficient of A[a]B[b] is exactly sum over q of W[c,q]U[q,a]V[q,b]. For c=k*4+i, a=ai*6+aj, b=bj*6+bk, the desired coefficient is 1 exactly when ai=i, bk=k, and aj=bj; otherwise it is 0. Compare all 24*24*36=20,736 coefficients, including all zeros. All 144 required ones and 20,592 zeros match. Since the validated program is bilinear and has no other monomials, this proves the identity for all integer A and B, not just selected inputs.
- Independently execute the scalar SLP on every pair of coordinate-basis matrices: 24*36=864 cases and all 24 outputs per case. These are exhaustive for this bilinear coefficient space, and agree with the tensor proof. No random sampling is used by the independent checker.
- Realize each L-term form with L-1 binary additions/subtractions and free signs. U costs 95 fresh plus 0 final; V costs 106 fresh plus 0 final; W costs 114 fresh plus 58 final. Total 373. The expanded naive count is 1376. Both match the JSON metadata; 373 matches INDEX.csv. The recorded comparison has difference 430-373=57.
- Hash the actual object bytes and compare with INDEX.csv. Repeat the complete independent checker in a separate process and compare captured output bytes. Repeat both author checks and compare their outputs too. Rehash the object after all checks. All agree. The independent checker has no randomness; the author's integer trials use its fixed seed. This determinism check applies to the saved verification, not the unsupplied process that constructed the object.

**Exact commands.** These ran from this folder in the order shown. Every command exited 0. The first command completed before I read the author's code. The relative virtual-environment executable below is the interpreter explicitly authorized in the task; no claim data outside this folder were read. System python3 lacks SymPy, so the optional symbolic check used that interpreter. The system-Python import probe produced ModuleNotFoundError and was not an object-verification failure.

```sh
python3 skeptic/check_slp.py > skeptic/output.txt 2>&1
python3 skeptic/check_slp.py > skeptic/output-repeat.txt 2>&1
python3 verify-it-yourself/check_slp.py object/4x6x6_m105_cr373_ZT_reduced.json > skeptic/author-output.txt 2>&1
python3 verify-it-yourself/check_slp.py object/4x6x6_m105_cr373_ZT_reduced.json > skeptic/author-output-repeat.txt 2>&1
../../../.venv/bin/python verify-it-yourself/sym_check.py object/4x6x6_m105_cr373_ZT_reduced.json > skeptic/author-sympy-output.txt 2>&1
../../../.venv/bin/python verify-it-yourself/sym_check.py object/4x6x6_m105_cr373_ZT_reduced.json > skeptic/author-sympy-output-repeat.txt 2>&1
python3 skeptic/compare.py > skeptic/comparison-output.txt 2>&1
```

**Independent full output.** Pasted directly from skeptic/output.txt:

```text
object: object/4x6x6_m105_cr373_ZT_reduced.json
bytes=29557; sha256=0daeb11814025acb716cc2cb7432d358a83e8bff7985faec2ef73e5efad21bda; INDEX match=PASS
format=4x6x6; max_dimension=6 <= 8; products=105; arithmetic=Z
u: inputs=24; fresh=95; final=105; additions fresh=95 final=0 total=95; term-count histogram={1: 105, 2: 95}; max_abs_binary_prefix=1
v: inputs=36; fresh=106; final=105; additions fresh=106 final=0 total=106; term-count histogram={1: 105, 2: 106}; max_abs_binary_prefix=1
w: inputs=105; fresh=72; final=24; additions fresh=114 final=58 total=172; term-count histogram={1: 1, 2: 44, 3: 29, 4: 18, 5: 4}; max_abs_binary_prefix=1
SLP order, integer +/-1 terms, every expanded fresh/final form and every binary prefix ternary: PASS
All 105 products have nonzero U/V factors and contribute to W: PASS
reduced additions=95+106+172=373; expanded naive additions=1376; metadata=PASS
Saved threshold arithmetic: 373 < 430; difference=57 (reference not recounted)
Exact full tensor identity: 20736 integer coefficients checked; nonzero=144; zero=20592; PASS
Exhaustive direct SLP basis-pair execution: cases=864; outputs=20736; PASS
Object bytes unchanged during checking: PASS
No random sampling, floating point, external packages, or network used.
RESULT: PASS (saved-object properties only)
```

**Author checker output.** Pasted directly from skeptic/author-output.txt:

```text
{"file": "4x6x6_m105_cr373_ZT_reduced.json", "format": "4x6x6", "rank": 105, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 95, "adds_V": 106, "adds_W": 172, "adds_total": 373, "naive_total": 1376, "declared_reduced": 373, "VALID": true}
```

**Author symbolic cross-check output.** Pasted directly from skeptic/author-sympy-output.txt:

```text
{"file": "4x6x6_m105_cr373_ZT_reduced.json", "format": "4x6x6", "rank": 105, "products": 105, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 373}
```

**Comparison and determinism output.** Pasted directly from skeptic/comparison-output.txt. The repeat captures are retained alongside the first captures.

```text
Independent: two separate runs have byte-identical stdout/stderr; sha256=e35e0a1b4a786b51a7f224c8f79d4bdc47c34639d35ea3f1d2dce593adae58f2
Author: two separate runs have byte-identical stdout/stderr; sha256=b29bfa6061d95c09dabb74fc4b08a0cbe9006b85aa9a249ebf8fb677671fe32d
Author SymPy: two separate runs have byte-identical stdout/stderr; sha256=fad7104af8fe87f40772589f3091e7dc5f5cdcaed367b9771aed2ad5f39e902d
Independent, author tensor/evaluation, and author SymPy results agree: PASS
Object sha256 after every run=0daeb11814025acb716cc2cb7432d358a83e8bff7985faec2ef73e5efad21bda; INDEX match=PASS
Comparison result: PASS
```

**Mismatches and checker limitation.** There is no disagreement about the saved object: dimension, product count, output layout, exactness, counts, hash, and repeatability all agree. C=AB false in the author's SymPy output means its alternative row-major interpretation fails; C^T true is exactly the transposed storage convention required by CLAIM.md.

The documentation for verify-it-yourself/check_slp.py says it checks expanded intermediate ternarity, but the implementation only checks literal term signs and does not reject expanded coefficients outside {-1,0,1}. Its VALID field also does not itself enforce the declared count, although its shell wrapper checks the expected count. These limitations do not invalidate this object: the independent checker explicitly verifies all expanded forms, every binary prefix, and the declared count. No advertised search needs to be reproduced for this explicit certificate; all tensor coefficients and all saved forms were checked exhaustively. The only unavailable objects are the deliberately unshipped third-party references, excluded from this skeptic's assigned scope.

pass: true
