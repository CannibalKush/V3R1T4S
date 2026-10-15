# Reproduce skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved straight-line program passes every object property checked in this offline scope. Its 140 products compute 4x6x8 matrix multiplication exactly over Z using 476 reduced additions/subtractions. This is a reproduction verdict about the saved object, not a verdict about current records or novelty.

## Scope and independence

I read CLAIM.md, the object, INDEX.csv, and table-record/README.md before author code. I recorded the definition in skeptic/definition.md and wrote skeptic/check.py without reading or importing verify-it-yourself/. I ran it successfully and saved its complete output in skeptic/output.txt before opening REPRODUCE.md or any author checker. Only then did I inspect and run the author code. The independent checker uses Python's standard library and exact integers. After comparing the author code, I wrote the additional independent binary-prefix check and the repeat-run harness. No network was used and no external claim files were read. The user-designated environment interpreter was used only to execute the supplied SymPy cross-check; its command below is relative to this folder.

Perminov's reference file is deliberately absent. table-record/README.md gives its URL and SHA256, but metadata is not its contents. I cannot recount that file or verify its hash without network. Likewise, the other recorded remote-response hashes cannot be validated against absent response bodies. The live best-rank comparison, live minimum reference count, Lille and matmulcatalog comparisons, coefficient-class comparisons, whether this scheme is claimed elsewhere, and any product identity/provenance involving the source schemes or Perminov's reference are outside this offline scope. I do not judge whether the table value is current or whether the result is new. None of those absent third-party files is required to establish the saved object's identity, exactness, ternarity, order, count, or reproducibility. The saved object required here is present.

## Quoted definition and success criterion

From CLAIM.md, Success criterion (verbatim apart from replacing angle brackets around the dimension placeholder with braces):

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

From CLAIM.md, Files in this folder, object definition:

> The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

The dimension placeholder's angle brackets were changed to braces to avoid literal template markers. The instructed Lille template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only the brackets were changed. The relevant exactness clause is "is verified symbolically to compute the full product A*B exactly over Z". The quoted success criterion includes the scalar and counting restrictions; the quoted object definition fixes input indexing, fresh-variable order, output indexing, and the count for each form.

## Properties and independent derivation

| Property | Check and result |
|---|---|
| Object identity and saved hash | Read the complete JSON bytes, compute SHA256, and compare with the single INDEX.csv row. Exact agreement: 45256d75a05660145a239129ba59524edf864bbda68bcf5297be8fdf7c38158e. Repeated runs read the same bytes and reproduce that digest. |
| Format and product count | Validate the dimensions as positive integers bounded by eight, require [4,6,8], m=140, exactly 140 U forms, 140 V forms, and 32 W outputs. These are 140 explicitly evaluated bilinear products; no claim of a lower bound on tensor rank is inferred. |
| Schema and integer domain | Reject duplicate JSON keys, unexpected schema, empty forms, noninteger indices/coefficients, coefficients outside +/-1, and characteristic-two mode. No scalar multiplication other than a free sign is used. |
| Straight-line order | Begin each map with its basis inputs; permit each fresh form to reference only input indices or earlier fresh indices, then append it. Final forms can use only these established values. All references pass. |
| Expanded ternary forms | Expand all 645 stored forms as integer coordinate vectors: 108+140 U, 136+140 V, and 89+32 W. Every coefficient in every fresh and final vector is -1, 0, or 1; all forms are nonzero. |
| Binary realization | Independently expand every left-to-right prefix of every form. Each of the 476 actual binary addition/subtraction results is itself ternary over its map's basis. Thus the saved n-ary forms admit a concrete binary evaluation with exactly the claimed cost and ternary intermediates throughout. |
| Exact full tensor | Compare every one of 32*24*48=36,864 integer coefficients. There are exactly 192 required coefficients equal to one and 36,672 required coefficients equal to zero, all matched. The output order is C[i][k] at k*4+i. |
| Reduced addition count | Each nonempty L-term form folds to L-1 binary operations. U costs 108+0=108, V costs 136+0=136, and W costs 146+86=232; total 476. Signs and the 140 bilinear multiplications are excluded. This matches complexity.reduced and INDEX.csv. |
| Other saved count metadata | Count nonzero coefficients of each fully expanded final U, V, and W form, subtract one per form, and sum: 1620, matching complexity.naive. |
| Recorded comparison arithmetic | The indexed value 476 is less than the indexed table value 551 by 75. This checks arithmetic and internal metadata consistency only, not the source or current status of 551. |
| Execution | Run the actual SLP independently on zero, all-one, alternating-sign, and 32 seeded integer input pairs, each twice: all 35 cases match direct matrix multiplication. These supplement the exhaustive tensor proof; they do not substitute for it. |
| Determinism | Repeat the independent checker, binary-prefix checker, author run script, and author SymPy checker in fresh processes. Every exit code is zero and every complete output is byte-identical to the first saved run. The object has fixed instruction order; neither exact proof nor counting uses randomness. Seeded numeric tests are supplemental. |

The exact proof is as follows. For each input map, start from unit vectors and replace every assignment by the signed sum of its previously computed vectors. Induction on straight-line order makes these expansions exact over Z. Let U[q,a] and V[q,b] denote the resulting product factors and W[o,q] the expansion of output o in the product basis. Executing the program therefore gives output coefficients

`T[o,a,b] = sum(q=0..139) W[o,q] * U[q,a] * V[q,b]`.

For output o=k*4+i, decompose a=s*6+t and b=h*8+l. The coefficient required by matrix multiplication is 1 exactly when s=i, l=k, and t=h; otherwise it is 0. The independent checker constructs T with exact integer arithmetic and compares every coefficient with that rule, including zeros. Bilinearity precludes any other monomials. Thus all 32 output polynomials equal A*B over Z for every integer input, with no numerical tolerance or probabilistic proof step. A left-to-right fold of each form proves the binary count and, by the supplemental prefix checks, preserves ternary coefficients at every binary intermediate.

There is no exhaustive-search optimality claim or search certificate here. The exhaustive obligation is the complete tensor identity, which was checked in full.

## Exact commands and complete saved output

Commands were run from this folder. The following blocks are inserted directly from the saved output files, without retyping or summarizing their contents.

Independent checker, run before reading author code:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

```text
Independent checker: Python standard library; exact integer arithmetic
Object: object/4x6x8_m140_cr476_ZT_reduced.json
SHA256: 45256d75a05660145a239129ba59524edf864bbda68bcf5297be8fdf7c38158e (matches INDEX.csv)
Format: 4x6x8; max dimension 8 <= 8; explicit products: 140
Schema, nonempty forms, integer +/-1 terms, and straight-line references: PASS
u_fresh: forms=108, reduced additions=108; all expanded forms ternary and nonzero
u: forms=140, reduced additions=0; all expanded forms ternary and nonzero
v_fresh: forms=136, reduced additions=136; all expanded forms ternary and nonzero
v: forms=140, reduced additions=0; all expanded forms ternary and nonzero
w_fresh: forms=89, reduced additions=146; all expanded forms ternary and nonzero
w: forms=32, reduced additions=86; all expanded forms ternary and nonzero
Reduced additions: 476; declared metadata and INDEX agree
Expanded naive additions: 1620; declared metadata agrees
Recorded comparison only: 476 < 551 (difference 75)
Full tensor identity over Z: PASS; 36864 coefficients checked, 192 ones, 36672 zeros
Direct SLP evaluation: PASS; 35 deterministic cases, each evaluated twice (supplement to exhaustive tensor proof)
Expanded U/V/W SHA256: 8b0ac1cf66cef2cf415f26036118ba17b140b7647a9328af8fef16209f2d4acf
Scope: no live-table claims, reference recount, provenance, or product identity checked
RESULT: PASS (all saved-object obligations)
```

Author run script, inspected and executed only after the independent pass:

```sh
sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
```

```text
sha256 matches INDEX.csv (45256d75a05660145a239129ba59524edf864bbda68bcf5297be8fdf7c38158e)
== check_slp.py on object/4x6x8_m140_cr476_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x6x8_m140_cr476_ZT_reduced.json", "format": "4x6x8", "rank": 140, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 108, "adds_V": 136, "adds_W": 232, "adds_total": 476, "naive_total": 1620, "declared_reduced": 476, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=476, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

Author symbolic cross-check using the user-designated environment interpreter:

```sh
../../../.venv/bin/python verify-it-yourself/sym_check.py object/4x6x8_m140_cr476_ZT_reduced.json > skeptic/author-symbolic-output.txt 2>&1
```

```text
{"file": "4x6x8_m140_cr476_ZT_reduced.json", "format": "4x6x8", "rank": 140, "products": 140, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 476}
```

Independent supplemental check of every binary-prefix intermediate:

```sh
python3 skeptic/check_binary_prefixes.py > skeptic/binary-prefix-output.txt 2>&1
```

```text
U: 108 binary addition/subtraction results checked; every expanded prefix ternary
V: 136 binary addition/subtraction results checked; every expanded prefix ternary
W: 232 binary addition/subtraction results checked; every expanded prefix ternary
PASS: explicit left-to-right binary realization uses 476 additions/subtractions; all intermediate vectors ternary
```

Repeat all four processes and compare complete outputs, saving the repeated outputs alongside the originals:

```sh
python3 skeptic/check_determinism.py > skeptic/determinism-output.txt 2>&1
```

```text
PASS: fresh-process output byte-identical: python3 skeptic/check.py
PASS: fresh-process output byte-identical: python3 skeptic/check_binary_prefixes.py
PASS: fresh-process output byte-identical: sh verify-it-yourself/run_checks.sh
PASS: fresh-process output byte-identical: ../../../.venv/bin/python verify-it-yourself/sym_check.py object/4x6x8_m140_cr476_ZT_reduced.json
PASS: all four runs reproduced their full saved output
```

## Comparison and mismatches

There is no object-property disagreement: the independent proof, author's tensor checker, and author's symbolic checker agree on the 4x6x8 format, 140 products, transposed storage C^T, exactness, and 476 reduced additions. The author's tensor checker also agrees on U=108, V=136, W=232 and naive count 1620. C=AB being false in the author's symbolic output refers to the alternative row-major output interpretation; C^T is the documented storage layout and passes.

There is one verification-coverage mismatch in the supplied description: REPRODUCE.md and CLAIM.md say the author checker verifies every expanded intermediate is ternary. In verify-it-yourself/check_slp.py, expand() accepts integer-expanded coefficients without restricting their magnitude; check() discards the fresh expansions and never checks their coefficient sets. The SymPy checker similarly checks only stored term signs. Consequently, those author checks alone do not establish the advertised expanded-intermediate property. This is a checker-coverage defect, not a violation by this object: skeptic/check.py explicitly checks every expanded stored form, and skeptic/check_binary_prefixes.py additionally checks every implicit binary intermediate, all successfully. The author's successful run is supporting agreement, not the basis for accepting ternarity.

No missing required object, tensor discrepancy, nonternary intermediate, invalid dependency, count mismatch, digest mismatch, or observed nondeterminism was found. The absent third-party reference and remote response bodies remain explicitly outside this offline verdict as instructed.

pass: true
