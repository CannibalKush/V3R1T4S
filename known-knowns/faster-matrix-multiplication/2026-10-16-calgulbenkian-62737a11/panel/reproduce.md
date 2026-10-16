# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object passes this skeptic's assigned checks: exact integer matrix multiplication, expanded ternarity, straight-line order, 40 bilinear products, 147 reduced additions/subtractions, object hash, and repeatability. This is a verdict on the saved object within the scope assigned in the request.

## Scope and independence

I read CLAIM.md, the saved object, INDEX.csv, table-record/README.md, and REPRODUCE.md before implementing skeptic/check.py using Python's standard library. I wrote and ran that independent checker and saved its complete output before opening any file under verify-it-yourself/. I subsequently inspected and ran the author's two Python checkers. No network was used or attempted. No external project files were inspected; the supplied Python environment was used only to execute the author's SymPy cross-check.

The reference scheme is deliberately absent. table-record/README.md identifies it as https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x5x5_m40_cr153_cn283_ZT_reduced.json, with recorded SHA256 89296c6dd94e052ca7cb517fa4d59b8a1dc335dc08c7dfc73edb420bba0c1bab. Without network or its bytes I cannot verify that hash, recount its additions, or confirm identity of its expanded U, V and W with this object. The other metadata-only external-source hashes are likewise unverified. These are explicit scope exclusions assigned by the request, rather than missing components required to evaluate this saved SLP.

I make no judgment about whether rank 40 is the current table rank, whether 153 is the live minimum, whether the result is new, the coefficient classes of external schemes, or duplicate/rank-target status. Live-table and reference-product comparisons belong to the other two skeptics. The saved arithmetic inequality 147 versus the recorded 153 is checkable and holds, but does not certify that external reference value.

## Quoted definition and success criterion

Definition recorded before opening the author checker.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

Angle brackets around the generic format were changed to braces to avoid template-placeholder rejection; no wording was changed. The Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html, with only its brackets changed when expressed as a template.

Saved-object interpretation quoted from CLAIM.md:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

## Checks and re-derived proof

All saved-object clauses of the quoted criterion were checked as follows.

1. **Explicit SLP, dimensions, product count and coefficient domain.** Strict JSON parsing rejects duplicate keys. Schema and integer types are checked. Dimensions are exactly 2x5x5, so the maximum dimension is 5, within 8. There are 40 U factors and 40 V factors, and 10 W output forms; z2 is false. Each factor is nonzero, and every one of the 40 products has a nonzero coefficient in some expanded output. Here rank 40 denotes the decomposition's 40 nonzero bilinear products; this is not a proof of minimum tensor rank.

2. **Straight-line order.** Each U/V/W map starts with the specified input basis. Before expanding fresh form k, an operand index must be nonnegative and strictly below the number of inputs plus k. Final rows may reference only inputs or defined fresh variables. There are 31 U, 54 V and 17 W fresh variables. Every operand has exactly the fields index and value, with a strict integer sign of +1 or -1. Forms are nonempty and have distinct operands. Thus there are no undefined references, cycles, future references, or forbidden scalar multiplications.

3. **Expanded ternarity, including intermediates.** Starting from integer unit vectors, for a form with terms (j,s), compute its coefficient vector by adding s times the already-derived vector j. Induction in straight-line order makes this exactly the form's linear expansion. All 102 fresh and 90 final forms have every coordinate in {-1,0,1}; none is zero. The same test passes for all 339 left-to-right term prefixes, so lowering a multi-term form to the literal sequence of binary operations preserves this stronger condition as well. U expands over the 10 independent A entries, V over the 25 B entries, and W over the 40 bilinear products, exactly as the layout defines.

4. **Full symbolic tensor identity over Z.** Let U[t,a], V[t,b], W[o,t] be the expanded integer coefficients. The coefficient of A[a]*B[b] in output o is sum over all 40 t of W[o,t]*U[t,a]*V[t,b]. For each of all 10 outputs, all 10 A coordinates and all 25 B coordinates, compare this integer sum to 1 exactly when a=i*5+j, b=j*5+k, and o=k*2+i, and to 0 otherwise. All 2500 coefficients agree: 50 ones and 2450 zeros. Each U factor is homogeneous in A, each V factor homogeneous in B, and W is linear in their products, so no other monomial types can occur. Equality of every coefficient proves every output equals the full A*B identically over Z, without probabilistic inference.

5. **Independent operational execution.** A separate direct register evaluator runs the literal SLP for every one of the 250 pairs consisting of one A basis entry and one B basis entry, and compares all 2500 resulting output entries to ordinary matrix multiplication. Sixteen deterministic signed-integer matrix pairs also pass. These are supplemental execution checks; the symbolic proof above covers the entire tensor. The package claims a particular saved SLP, not exhaustive optimality or a search; no search sample is substituted for an exhaustive verification.

6. **Reduced addition count.** A nonempty L-term form costs exactly L-1 binary additions/subtractions under the quoted convention: signs are free and the operands already exist. Count every fresh and final form. U costs 31+0=31; V costs 54+0=54; W costs 24+38=62. Total: 31+54+62=147. Exclude the 40 bilinear multiplications. This equals both complexity.reduced and INDEX.csv's value. Recounting expanded nonzeros minus 2r minus the 10 outputs gives naive count 283, agreeing with complexity.naive. The recorded 153 exceeds 147 by 6; its external recount remains outside scope.

7. **Hashes, saved metadata, determinism.** Recompute the raw object's SHA256 and compare it to INDEX.csv; check the index's sole row, relative object path, target, cell, and numbers. Record SHA256 values for all eight original package files in skeptic/package_hashes.json, and verify they remain unchanged after the runs. Only the object's digest has an independently supplied saved-file counterpart; recording other local digests is an integrity inventory, not external authentication. Each of the independent checker, author tensor checker, and author symbolic checker was executed twice in separate processes. Each pair of complete captured outputs is byte-identical. The object is a fixed acyclic program using exact integer operations; the independent checker uses no randomness. The author's numeric trials use a fixed random seed.

## Exact commands and captured output

All commands below run from this folder. Every command exited with status 0. Output blocks are inserted directly from the captured files, without retyping.

Independent checker, before reading the author's code, followed by its repeat:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
```

Complete skeptic/output.txt (the repeat is byte-identical):

```text
Independent checker: exact integer arithmetic; no network; no third-party libraries
object: object/2x5x5_m40_cr147_ZT_reduced.json
SHA256: 62737a117df29bc9dc6194509ed47f95a6f763ea3ca21fca84f79a78c44e6e1a (matches INDEX.csv)
format: 2x5x5; max dimension 5 <= 8; products: 40; domain: Z
U: inputs=10 fresh=31 final=40 additions_fresh=31 additions_final=0 total=31
U: order, signed-unit operands, expanded ternary forms and 102 prefixes PASS
V: inputs=25 fresh=54 final=40 additions_fresh=54 additions_final=0 total=54
V: order, signed-unit operands, expanded ternary forms and 148 prefixes PASS
W: inputs=40 fresh=17 final=10 additions_fresh=24 additions_final=38 total=62
W: order, signed-unit operands, expanded ternary forms and 89 prefixes PASS
count: 31 + 54 + 62 = 147 additions/subtractions; 40 products excluded; negations free
expanded naive count: 283 (matches object metadata)
saved reference number: 153; 147 < 153; difference 6 (reference not independently recounted)
tensor identity: all 2500 coefficients PASS (50 ones, 2450 zeros); exact over Z
direct SLP execution: all 250 bilinear basis pairs / 2500 output entries PASS
direct SLP execution: 16 deterministic signed-integer matrix pairs PASS (supplement only)
object bytes unchanged during check: PASS
Scope: reference scheme absent; live sources and reference-product identity not checked
ALL INDEPENDENT SAVED-OBJECT CHECKS PASS
```

Author tensor checker, run only after independent checking:

```sh
python3 verify-it-yourself/check_slp.py object/2x5x5_m40_cr147_ZT_reduced.json > skeptic/author-output.txt 2>&1
python3 verify-it-yourself/check_slp.py object/2x5x5_m40_cr147_ZT_reduced.json > skeptic/author-output-repeat.txt 2>&1
```

Complete skeptic/author-output.txt:

```text
{"file": "2x5x5_m40_cr147_ZT_reduced.json", "format": "2x5x5", "rank": 40, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 31, "adds_V": 54, "adds_W": 62, "adds_total": 147, "naive_total": 283, "declared_reduced": 147, "VALID": true}
```

Author symbolic checker, using the supplied environment's interpreter expressed relative to this folder:

```sh
../../../.venv/bin/python verify-it-yourself/sym_check.py object/2x5x5_m40_cr147_ZT_reduced.json > skeptic/author-symbolic-output.txt 2>&1
../../../.venv/bin/python verify-it-yourself/sym_check.py object/2x5x5_m40_cr147_ZT_reduced.json > skeptic/author-symbolic-output-repeat.txt 2>&1
```

Complete skeptic/author-symbolic-output.txt:

```text
{"file": "2x5x5_m40_cr147_ZT_reduced.json", "format": "2x5x5", "rank": 40, "products": 40, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 147}
```

Comparison and integrity audit:

```sh
python3 skeptic/compare.py > skeptic/comparison-output.txt 2>&1
```

Complete skeptic/comparison-output.txt:

```text
independent checker: two separate runs have byte-identical full output PASS
author tensor checker: two separate runs have byte-identical full output PASS
author sympy checker: two separate runs have byte-identical full output PASS
author results agree with independent exactness, output layout, rank length and counts PASS
all 8 original package files unchanged after all checker runs PASS
Object hash is corroborated by INDEX.csv; metadata-only external-source hashes cannot be verified without their bytes
No saved-object mismatch or observed nondeterminism
```

## Mismatches and checker limitations

No mismatch in the saved object's mathematics, counts, layout, hash, or repeated outputs was found. The author's symbolic result C=AB=false concerns the alternative row-major output ordering; C^T=true agrees with the exact transposed layout required by CLAIM.md, so this is not a discrepancy.

The author's check_slp.py verifies literal operand signs but does not test ternarity of expanded fresh or final vectors, despite the package's coverage description. Its VALID field also does not itself require agreement with declared_reduced. These are limitations of that checker, not failures of this saved object: skeptic/check.py separately enforces expanded ternarity, ternary binary prefixes, exact count metadata, and the specific required output layout. Both author checkers agree with the independent result on this object.

The reference's absent bytes prevent its recount and product-identity comparison. Live-table, novelty and rank-status claims are not included in this verdict, as assigned by the request. Every property of the saved object within this skeptic's assigned scope has been confirmed.

pass: true
