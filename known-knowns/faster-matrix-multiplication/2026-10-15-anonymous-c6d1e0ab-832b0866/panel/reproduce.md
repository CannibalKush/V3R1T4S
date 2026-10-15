# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved 5x6x7, 150-product SLP is exact over Z, is ternary in every listed expanded fresh and final form, and costs 582 additions/subtractions under the stated reduced convention. All locally checkable candidate properties pass. This verdict does not assess current table values or novelty.

I read CLAIM.md and the saved object, recorded the quoted definition in skeptic/definition.md, wrote skeptic/check.py using Python's standard library, and ran it successfully before reading REPRODUCE.md or any file in verify-it-yourself/. Only afterward did I read and run the author's checker. No network was used and no files outside this package were inspected.

The definition and criterion checked are quoted below. The complete success criterion is retained to distinguish the checkable object clauses from the external status clauses.

Object and counting definition (quoted):

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

Success criterion (quoted in full):

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

Bracket-only formatting change: the generic format notation uses {n,m,p} in place of angle brackets; only the brackets were changed. The Lille URL template is written as https://fmm.univ-lille.fr/{n}x{m}x{p}.html, changing only the brackets. This CLAIM.md names the Lille per-format page in prose rather than spelling out that URL template in the success criterion.

Verification method (quoted):

> Parse the SLP (sequence of assignments t_k = +/- t_i +/- t_j over inputs A_ij, B_jl, intermediate sums, r products, and output assignments). Evaluate it with sympy (or exact integer evaluation at many random integer matrices plus one symbolic pass) and confirm every output equals the corresponding entry of A*B. Count the additions under the stated convention (exclude negations, exclude the r multiplications). Load the reference scheme from Perminov's addition_reduced_ZT directory (and reduced_known.json), recount its additions with the same counter to calibrate the convention, and compare. Re-fetch the repository, the Lille page and COVERAGE.md. Minutes on this Mac.


Properties and derivation:

| Property | Independent check and result |
|---|---|
| Explicit valid SLP | JSON parsing rejects duplicate keys. Dimensions, exact key set, field types, nonempty forms, signed unit terms, and every reference are checked. Fresh references are restricted to inputs and earlier fresh variables; final forms see all fresh variables. |
| Format and product count | Dimensions are exactly [5,6,7], maximum 7 is at most 8, U and V each have 150 nonzero factors, and W has 35 nonzero outputs. There are exactly 150 bilinear products; no product is charged as an addition. This establishes the saved decomposition size, not minimal tensor rank. |
| Integer rather than characteristic-two arithmetic | z2 is false; every expansion, outer product, and sum uses unbounded Python integers with ordinary signs. |
| Every expanded intermediate is ternary | Begin with standard coordinate unit vectors for the 30 A inputs, 42 B inputs, or 150 product inputs. For each saved form, add the signed vectors of its references. Check every coordinate is in {-1,0,1}, including zeros. This checks U's 147 fresh and 150 final forms (8,910 coordinates), V's 171 fresh and 150 final forms (13,482), and W's 94 fresh and 35 final forms (19,350): 747 forms and 41,742 coordinates in total. W is expanded over its product inputs, as a linear map. |
| Product tensors | For product t, independently form every coefficient U[t,a] V[t,b] of A[a] B[b]. Combining these with expanded W gives output coefficient sum_t W[o,t] U[t,a] V[t,b]. A separate propagation of polynomial coefficient vectors directly through every saved W assignment gives exactly the same tensors. |
| Full tensor identity and layout | Decode output o as i=o mod 5, k=floor(o/5). Decode A index a as row_a=floor(a/6), column_a=a mod 6, and B index b as row_b=floor(b/7), column_b=b mod 7. Expanding the definition C[i,k]=sum_j A[i,j]B[j,k] gives coefficient 1 exactly when row_a=i, column_a=row_b, column_b=k, and 0 otherwise. Compare all 35*30*42=44,100 coefficients, obtaining exactly 210 ones and 43,890 zeros, with zero mismatches. These are all coefficients of the bilinear output polynomials, so their equality proves exactness for every integer input. No random sample is used as a substitute for this proof. |
| Reduced count and its realization | A nonempty k-term signed sum can be evaluated with k-1 binary additions/subtractions; a one-term copy or negation is free. Sum k-1 across every saved fresh and final form. U costs 147+0, V costs 171+0, W costs 183+81; total 582. These counts match the saved complexity metadata. This verifies the program's cost, without asserting its optimality. |
| Other saved count metadata | The nonzero counts of expanded U,V,W give nz(U)+nz(V)+nz(W)-2*150-35=2039, agreeing with the declared naive count. |
| Saved-reference arithmetic | table-record/README.md states a reference of 664. The verified count satisfies 582 less than 664, by 82. This checks arithmetic against the saved assertion only. |
| Object integrity | The actual candidate SHA256 agrees with INDEX.csv, whose candidate path and value 582 and saved reference 664 also agree. The independently computed SHA256 is pasted in the output below. |
| Determinism | Independent checker runs in separate processes produce byte-identical full output. Author checker runs also produce byte-identical output. The object still matches its INDEX.csv hash after the comparisons. |

No exhaustive optimization search is asserted in CLAIM.md. The verification above exhausts the complete saved tensor and every listed form; it is not a spot check.

Exact commands, run from this folder:

```sh
python3 skeptic/check.py object/5x6x7_m150_cr582_ZT_reduced.json > skeptic/output.txt 2>&1
python3 skeptic/compare.py > skeptic/comparison-output.txt 2>&1
```

The first command exited successfully. The comparison script reruns the independent checker and then runs the following author command twice, checks return codes, validates reported values, compares complete outputs, and checks INDEX.csv:

```sh
python3 verify-it-yourself/check_slp.py object/5x6x7_m150_cr582_ZT_reduced.json
```

Full independent output, pasted directly from skeptic/output.txt:

```text
Object: object/5x6x7_m150_cr582_ZT_reduced.json
SHA256: 832b08667df7d72d5c12f78f7073168f43dd50e323aaaf547290f0533d2585f3
Dimensions: 5x6x7; maximum=7 <= 8; products=150; arithmetic=Z
U: inputs=30, fresh=147, final=150, expanded coefficients checked=8910, fresh additions=147, final additions=0, total=147
V: inputs=42, fresh=171, final=150, expanded coefficients checked=13482, fresh additions=171, final additions=0, total=171
W: inputs=150, fresh=94, final=35, expanded coefficients checked=19350, fresh additions=183, final additions=81, total=264
SLP: all term coefficients are signed units; all references are to inputs or earlier fresh variables
Ternary condition: every listed fresh and final form expands over its map inputs into {-1,0,1}
Proof cross-check: direct W polynomial DAG equals expanded W times product tensors
Tensor identity: coefficients checked=44100, expected ones=210, expected zeroes=43890, mismatches=0
Exactness: every output equals sum_j A[i,j]*B[j,k] over Z, for all inputs
Counts: reduced=582 (U=147, V=171, W=264); naive=2039
Counting: each k-term form costs k-1 binary additions/subtractions; signs are free; 150 products excluded
Saved-reference arithmetic: 582 < 664; difference=82; external table status not assessed
PASS: every locally checkable object property verified exhaustively using exact Python integers
```

Full author output, pasted directly from skeptic/author-output.txt:

```text
{"file": "5x6x7_m150_cr582_ZT_reduced.json", "format": "5x6x7", "rank": 150, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 147, "adds_V": 171, "adds_W": 264, "adds_total": 582, "naive_total": 2039, "declared_reduced": 582, "VALID": true}
```

Full comparison output, pasted directly from skeptic/comparison-output.txt:

```text
Command: python3 skeptic/check.py object/5x6x7_m150_cr582_ZT_reduced.json
Exit code: 0
Independent repeat output byte-identical: True
Command: python3 verify-it-yourself/check_slp.py object/5x6x7_m150_cr582_ZT_reduced.json
Exit code: 0
Command: python3 verify-it-yourself/check_slp.py object/5x6x7_m150_cr582_ZT_reduced.json
Exit code: 0
Author repeat output byte-identical: True
Author comparison: exact identity, layout, rank, all addition subtotals and metadata agree
INDEX.csv: candidate file, SHA256, value=582 and saved reference=664 agree
PASS: no numerical disagreement or observed nondeterminism
```

There is no numerical disagreement. The author's exact tensor identity, output layout, 150-product count, reduced-count subtotals, total 582, and naive total 2039 all agree with the independent checker. Its seeded integer evaluation also reports success; that sample is supplemental and is not the exactness proof here. I did not run the optional sympy checker or shell wrapper; the author comparison uses check_slp.py directly.

An author-verifier coverage gap is worth recording: despite REPRODUCE.md saying every expanded intermediate is checked for ternarity, check_slp.py checks each stored term's sign but never explicitly tests the coefficients of the expanded fresh and final vectors. Its VALID flag also does not itself require the declared reduced count to match. My independent checker explicitly verifies both conditions, and both hold for this saved object. Thus this is a coverage gap, not a disagreement about this candidate.

The required candidate is present and no locally checkable object property is missing. The saved table record contains metadata only: the original reference scheme and fetched source bodies are absent. Accordingly I cannot recount the reference scheme, establish source identity with Perminov's original rank-150 scheme, authenticate the extracted table cells, or check best-rank status from the external source. I do not infer those facts from hashes of absent files. Current rank/table status, live-fetch requirements, coefficient-class reference selection, and novelty are outside this REPRODUCE verdict and remain for the other skeptic. The only reference comparison made here is the explicit arithmetic against the saved 664 assertion.

pass: true
