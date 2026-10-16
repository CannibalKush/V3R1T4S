# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object passes the offline reproduction obligations. This judgment is
limited to the saved object and its saved metadata, as instructed. There is no
judgment about the live table, novelty, or identity with the external reference.

## Independence and quoted definition

I read CLAIM.md, the object, INDEX.csv and table-record/README.md first. I wrote
skeptic/definition.md and skeptic/check.py, then successfully ran the independent
checker and saved skeptic/output.txt, before opening any file in
verify-it-yourself/ or REPRODUCE.md. The independent checker uses only the Python
standard library and imports no author code. Its source hash is in its output.

In the quoted dimension template, only the angle brackets have been changed to
braces; all words are unchanged. The Lille URL template is rendered as
https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only the brackets have been changed.
The actual success-criterion paragraph in CLAIM.md describes that page without
spelling out the URL template.


> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

## Saved-object layout and counting definition

> The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

Here CLAIM.md uses m for the number of products in its JSON description;
the mathematical format's middle dimension is 5, while JSON m is 104.

## Scope

The checkable clauses are the explicit SLP, dimensions at most 8, its 104
bilinear products, integer exactness, the signed-unit coefficient restriction,
the reduced counting convention, and the locally recorded values and hash.
I additionally checked ternarity of every expanded intermediate and final form,
straight-line order and deterministic replay, as required by the task.

The comparison 379 against the saved number 400 is only an arithmetic comparison
with metadata. No live table was accessed or judged. The best listed rank,
minimum over all live reference files, other published counts, coefficient-class
comparisons, previous claiming and novelty cannot be established from these
saved files and are assigned to the other skeptics.

Perminov's reference scheme is explicitly not shipped. Its recorded location is
https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x5x7_m104_cr400_fv163_cn931_ZT_reduced.json
and its recorded sha256 is
0c4cb3e3de6b9a820a3d231be3be5137d9791e513cfb297ef55dadced2793931.
Without network I cannot verify those bytes, recount the reference, calibrate
against its SLP or establish identity of its products with this object's.
Those are scope exclusions expressly allowed by the task, rather than missing
candidate-object evidence. All candidate files required for the local proof
are present.

## Properties and re-derived proof

| Property | Independent method and result |
|---|---|
| Well-defined data | Reject duplicate JSON keys, unexpected keys, malformed terms, empty forms and noninteger indices or coefficients. JSON z2 is false. The dimensions are positive integers 4, 5, 7. |
| Straight-line order | Start U with 20 A inputs, V with 35 B inputs and W with 104 product inputs. Fresh assignment k is appended at input-count+k; each term index must already exist. Final rows can refer only to inputs and fresh variables. All references pass. |
| Products and output layout | Exactly 104 U rows, 104 V rows and 28 W rows. All product factors are nonzero; all products are used and their stored expanded factor pairs are distinct. Output k*4+i is C[i][k], precisely the declared transposed layout. This checks a 104-product representation, without asserting a minimal tensor rank. |
| Allowed scalars and ternarity | Every term coefficient is an integer +1 or -1. Expand each U/V form over the original input basis and each W form over independent product variables using integer vector arithmetic. Every coefficient of all 263 fresh forms and 236 final forms is in {-1,0,1}. Also check every signed left-to-right prefix, so all introduced binary addition intermediates are ternary. |
| Full exactness over Z | Construct every coefficient T[o,a,b] = sum over t of W[o,t]*U[t,a]*V[t,b]. Check all 28*20*35 = 19600 entries, including all required zeros. The expected entry is 1 exactly when o=k*4+i, a=i*5+j and b=j*7+k for some valid i,j,k, otherwise 0. Exactly 140 coefficients are nonzero, all equal 1; there are no mismatches. |
| Literal execution | A separate numerical evaluator follows the original assignments, without expanded vectors. It checks every one of the 20*35 = 700 input-basis pairs and all 28 outputs for each, plus 12 deterministic dense integer pairs. All results equal direct matrix multiplication. The basis check is exhaustive for this bilinear map; dense cases are supplementary. |
| Reduced count | Count every fresh and final form of length s as s-1. U costs 91, V costs 113 and W costs 175. There are 878 signed terms in 499 forms, giving 878-499 = 379 additions/subtractions. Negations cost zero; 104 bilinear multiplications are excluded. Literal execution independently counts 379 operations each time. |
| Other saved count fields | Recounting expanded final forms without sharing gives 931 naive additions, matching complexity.naive; 379 matches complexity.reduced and INDEX.csv. 379 is 21 below the metadata's 400. |
| Hash and metadata | Recompute the candidate sha256 and match INDEX.csv exactly; check target, format/rank cell, object path, claimed value, table value, and consistency of the saved summary in table-record/README.md. External-source hashes cannot be checked against absent source files. |
| Determinism and integrity | Two fresh independent-checker processes with PYTHONHASHSEED 7 and 913 produce byte-identical complete results, including hashes of all expanded forms and the full tensor. Six definition/input/checker files are hashed before and after those runs and remain unchanged. Both author checkers also replay identically in two fresh processes. |

The symbolic expansion is justified inductively: each initial register is a
basis vector; each signed sum of already established vectors equals its declared
linear form over Z. The syntax separates A-only and B-only maps, then forms
104 products, then a linear map of those products. Every output is therefore a
bilinear polynomial with coefficients exactly T[o,a,b]. Checking every
coefficient against the multiplication tensor proves equality for all integer
matrices, with no probabilistic assumption. Checking all prefix expansions also
exhibits a permitted binary implementation of each longer form. A form with s
terms has exactly s-1 binary operations after its free first sign, which proves
the addition count under the quoted convention. No exhaustive search or
optimality proof is claimed, and no sample substitutes for an exhaustive check.

## Exact commands and real output

Run from this folder. The relative interpreter used for SymPy is the interpreter
expressly supplied in the task. No additional package or network access was used.
All displayed output blocks below are inserted verbatim from the saved files.
All four commands exited with status 0.

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

```text
Independent checker: Python standard library; exact integer arithmetic
Definition fixed in skeptic/definition.md before reading author code
Object: object/4x5x7_m104_cr379_ZT_reduced.json
Object sha256: b3b9b009a9de20414ff66a9309bc4092c31b6ad74a3aec0e235e470cd5d07335 (matches INDEX.csv)
Checker sha256: db781bf54c5a9a9aac79bd4ecfc9173d6f7322cea2899c230af4e9243e69820c
Format: 4x5x7 ; maximum dimension 7 <= 8
Bilinear products: 104 ; all active, nonzero and distinct as stored
U: inputs=20 fresh=91 final=104 forms=195 additions=91 binary_prefixes=286 max_abs_expanded_coefficient=1
U expanded sha256: 1dbd3ad0f27a6dba086c6052967051d032fcd2e99c562a38c5e64b412b55c6ef
V: inputs=35 fresh=113 final=104 forms=217 additions=113 binary_prefixes=330 max_abs_expanded_coefficient=1
V expanded sha256: 473ace34223b61a5e442ae4d04fd0e89493b707a1135e9c94e2369c527d697c0
W: inputs=104 fresh=59 final=28 forms=87 additions=175 binary_prefixes=262 max_abs_expanded_coefficient=1
W expanded sha256: eab24dcc8e216bcaaba76e122a345dd5b7506a6dde1a4f226a57163800bdb96a
Straight-line order: every index is nonnegative and already available
Coefficients: signed unit integers; every form and binary prefix expands ternarily
Exact full tensor: 19600 coefficients checked; 140 nonzero coefficients; zero mismatches
Tensor sha256: d539a1385bad5b13026ce1ed41d21261cbfec0051e1a44321bf2223ab23a5def
Literal SLP replay: 700 exhaustive basis pairs, 19600 output checks, 12 dense integer cases; zero mismatches
Reduced additions: 379 = 91 + 113 + 175; 104 products excluded, negations free
Expanded naive additions: 931 ; both complexity metadata fields agree
Saved comparison: 379 < 400; improvement 21
INDEX.csv target, cell, path, value, table value, sha256: consistent
Determinism: two fresh processes, PYTHONHASHSEED=7 and 913, identical full results
Input/checker integrity: all six files unchanged during both runs
Scope: external reference absent; no network, live comparison, rank optimality or reference-product identity checked
PASS: all saved-object obligations satisfied
```

Only after that independent run, run the author's primary checker:

```sh
python3 verify-it-yourself/check_slp.py object/4x5x7_m104_cr379_ZT_reduced.json > skeptic/author_output.txt 2>&1
```

```text
{"file": "4x5x7_m104_cr379_ZT_reduced.json", "format": "4x5x7", "rank": 104, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 91, "adds_V": 113, "adds_W": 175, "adds_total": 379, "naive_total": 931, "declared_reduced": 379, "VALID": true}
```

The author's separate symbolic execution:

```sh
../../../.venv/bin/python verify-it-yourself/sym_check.py object/4x5x7_m104_cr379_ZT_reduced.json > skeptic/author_symbolic_output.txt 2>&1
```

```text
{"file": "4x5x7_m104_cr379_ZT_reduced.json", "format": "4x5x7", "rank": 104, "products": 104, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 379}
```

The comparison script rechecks the independent result, replays each author
checker in two fresh processes, compares full output to the original saved runs,
and checks all shared result fields explicitly:

```sh
python3 skeptic/compare.py > skeptic/comparison_output.txt 2>&1
```

```text
Author primary checker: VALID=true, exact C^T, integer replay passed
Author SymPy checker: C^T=true, C=AB=false (the required transposed layout)
Agreement: format 4x5x7; 104 products; U=91, V=113, W=175; total=379; naive=931
Author determinism: each checker replayed in two fresh processes with hash seeds 7 and 913
Both author outputs are byte-identical to their original saved runs
Author code gap: neither checker explicitly asserts ternarity of expanded intermediates
Independent coverage: every declared form and binary prefix is ternary; no object mismatch
PASS: independent and author results agree on every reported shared property
```

## Mismatches and author-checker limitation

No saved-object mismatch, missing candidate object, hash mismatch or observed
nondeterminism was found. The author results agree on the format, number of
products, exact tensor, layout, separate addition counts, total and naive count.
The author's C=AB=false result is expected: the specified layout is C^T.

There is a documentation/coverage discrepancy in the author's checker:
REPRODUCE.md promises checking every expanded intermediate for ternarity, but
verify-it-yourself/check_slp.py checks only the signed term coefficients and
discards the returned expanded fresh vectors without checking their coefficient
range. Its VALID field therefore does not establish that promised property.
verify-it-yourself/sym_check.py also checks signed term coefficients rather than
expanded intermediate coefficient ranges. My independently written checker
explicitly verifies that property, including binary prefixes, and the saved
object passes it. This is a gap in the author's checker, not a disagreement
about the verified object.

pass: true
