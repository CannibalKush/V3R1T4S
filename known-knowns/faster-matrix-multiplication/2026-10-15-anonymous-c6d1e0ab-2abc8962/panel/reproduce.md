# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved SLP passes independent exact verification: format 5x7x7, 176 nonzero bilinear products, ternary expanded forms, and 699 reduced additions. This verdict covers reproduction from the saved object. It does not judge current table values, best-known rank, or novelty.

## Definition and criterion checked

The full success criterion from `CLAIM.md` is quoted below. In its format placeholder I changed only the angle brackets to braces to satisfy the package formatting rule. For the Lille URL template, the notation is `https://fmm.univ-lille.fr/{n}x{m}x{p}.html`; only the brackets have changed. The actual criterion in this package refers to the Lille per-format page in words.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The package's concrete encoding and counting definition is:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

In particular, the exactness condition is “is verified symbolically to compute the full product A*B exactly over Z”, and the counting convention is “each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP”.

## Independent construction and complete checks

I read `CLAIM.md`, the object's layout, `INDEX.csv`, and `table-record/README.md`; then wrote `skeptic/check.py` and ran it successfully before opening any file in `verify-it-yourself/` or `REPRODUCE.md`. The checker uses Python's standard library and exact integers. It imports no author code.

| Property | Independent method and result |
|---|---|
| Object identity | SHA256 of the saved JSON matches `INDEX.csv`; file, target, cell, value, and reference-value fields agree. Duplicate JSON keys and unexpected or missing fields are rejected. |
| Format and product count | Dimensions are exactly 5x7x7, maximum dimension 7, with exactly 176 U forms, 176 V forms, and 35 W forms. Every product factor and every product's expanded output contribution is nonzero. This verifies a 176-term decomposition, not minimal tensor rank. |
| Straight-line dependencies | Every term index is an integer referring to an input or an already defined fresh variable. All six lists contain nonempty forms. Every explicit scalar is an integer +1 or -1. |
| Expanded ternary condition | Expand every U, V, and W fresh form and final form as an integer vector over that map's independent inputs. Check every coefficient, including zeros, is in {-1,0,1}. All 875 forms and 55,431 expanded coefficients pass. W's independent inputs are the 176 product symbols. |
| Exactness over Z | Form every coefficient of every output bilinear polynomial from the expanded U, V, W maps. Compare all 60,025 coefficients with matrix multiplication: precisely 245 coefficients are 1 and 59,780 are 0. No probabilistic inference or sampling establishes this result. |
| Output layout | Enforce the specified layout `w[k*5+i] = C[i,k]`, rather than accepting whichever layout happens to work. |
| Reduced additions | Count each saved form of length L as L-1. U contributes 179, V 206, W 314: total 699. Free signs and the 176 bilinear products are excluded. The declared reduced count agrees. |
| Extra metadata check | Expand the final maps and recount their naive additions: 2605, matching the object's metadata. |
| Direct execution | Execute the original DAG on three fixed matrix pairs (zero, all ones, mixed signed integers) and compare all outputs. These are supplemental checks, not a substitute for the exhaustive tensor identity. |
| Saved comparison arithmetic | `INDEX.csv` and `table-record/README.md` both state 788 as the saved reference. The independently verified 699 is smaller by 89. This verifies arithmetic and consistency of the saved metadata, not the external sources. |
| Repeatability | Repeat the independent and author checkers with a fixed alternate Python hash seed. All checker results agree exactly; see the launcher-diagnostic detail below. |

The proof is reconstructed directly from the definitions. Initially each input is a standard basis vector. Inductively, summing the signed vectors of already computed quantities gives the exact integer linear form for the next variable. Thus the expanded U and V rows are the exact product factors and the expanded W rows are the exact output weights. For output o, A entry a, and B entry b, its bilinear coefficient is `sum_t W[o,t]*U[t,a]*V[t,b]`. With `i=o%5` and `k=o//5`, the required coefficient is 1 exactly when `a//7=i`, `b%7=k`, and `a%7=b//7`; otherwise it is 0. Exhaustive coefficient equality proves every output is `sum_j A[i,j]*B[j,k]` for all integer inputs. Finally a nonempty signed form of L terms requires L-1 binary additions/subtractions under the stipulated convention; summing over all fresh and final forms proves the reduced count.

There is no exhaustive search or optimality proof asserted for the 699 count. The exhaustive operation here is verification of the entire tensor identity.

## Exact commands and captured output

All commands below run from this folder. The first independent command was:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

Exit status: 0. The following is pasted directly from `skeptic/output.txt`:

```text
Independent checker: exact Python integer expansion; exhaustive tensor comparison
Object: object/5x7x7_m176_cr699_ZT_reduced.json
SHA256: 2abc89623e051336de20440c1e68300d56656b98733b8df7e66808bbd60174be
Format: 5x7x7; maximum dimension=7 <= 8; products=176; integer arithmetic
U: inputs=35, fresh=179, final=176, forms=355, additions=179, expanded coefficients checked=12425; dependencies/scalars/ternarity PASS
V: inputs=49, fresh=206, final=176, forms=382, additions=206, expanded coefficients checked=18718; dependencies/scalars/ternarity PASS
W: inputs=176, fresh=103, final=35, forms=138, additions=314, expanded coefficients checked=24288; dependencies/scalars/ternarity PASS
All 176 product factors and expanded output contributions are nonzero: PASS
Full tensor identity over Z: 60025 coefficients checked; 245 ones, 59780 zeros; PASS
Output layout: w[k*5+i] = C[i,k]; all 35 output polynomials equal sum_j A[i,j]*B[j,k]
Supplemental direct SLP evaluation: 3 fixed integer matrix pairs, all 35 outputs each; PASS
Reduced additions: U=179 + V=206 + W=314 = 699; claimed 699: PASS
Expanded naive additions: 2605; metadata agrees: PASS
INDEX target/cell/object/hash/value: PASS
Saved-reference arithmetic only: 699 < 788; difference=89; PASS
Live rank, live reference minimum, provenance, reference-scheme calibration, and novelty are not established by this checker.
RESULT: PASS for all object properties checked from the saved SLP and INDEX
```

Only after that completed, I read the author files and ran:

```sh
TMPDIR=skeptic sh verify-it-yourself/run_checks.sh > skeptic/author_output.txt 2>&1
```

Exit status: 0. `TMPDIR=skeptic` keeps the author's negative-control temporary files inside this folder. The following is pasted directly from `skeptic/author_output.txt`, including the original host diagnostics:

```text
sha256 matches INDEX.csv (2abc89623e051336de20440c1e68300d56656b98733b8df7e66808bbd60174be)
== check_slp.py on object/5x7x7_m176_cr699_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
2026-10-15 05:35:11.109 xcodebuild[85208:74047894]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 05:35:11.553 xcodebuild[85208:74047892] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
{"file": "5x7x7_m176_cr699_ZT_reduced.json", "format": "5x7x7", "rank": 176, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 179, "adds_V": 206, "adds_W": 314, "adds_total": 699, "naive_total": 2605, "declared_reduced": 699, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=699, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

The author agrees on format, product count, exact transposed output layout, reduced components, total 699, and naive count 2605. Its sign-flip negative control is rejected. I inspected `sym_check.py` but did not run the optional SymPy cross-check: the independent full coefficient comparison already proves the identity.

One author-checker limitation is visible in its code: `expand` returns the expanded fresh and final vectors, but `check` never tests those expanded coefficients for membership in {-1,0,1}. It only restricts the written term signs. The advertised expanded-intermediate ternarity check is therefore absent. This is a checker-coverage discrepancy, not a failed property of this object: my independent checker exhaustively checked the missing property and it passes.

## Repeatability and mismatches

An initial strict byte comparison of the first and second combined author logs differed. The entire difference is the two timestamped `xcodebuild` host-launcher diagnostic lines retained above. There is no difference in the author's checker JSON, verdict, counts, or negative-control result. `skeptic/author_repeat_output.txt` preserves that second combined log; `skeptic/repeat_output.txt` preserves the matching independent repeat.

To isolate actual checker stdout and stderr and test two further executions, I saved and ran:

```sh
python3 skeptic/repeat_checks.py > skeptic/determinism.txt 2>&1
```

Exit status: 0. This script sets `PYTHONHASHSEED=7919` and `TMPDIR=skeptic`, retains both stdout and stderr from each run, compares them byte for byte, and verifies that removing exactly the two identified launcher lines from the initial combined author log yields the later stdout exactly. Its real output is:

```text
independent: exits=0,0; stdout identical=True; stderr identical=True; stderr bytes=0,0
independent: stdout identical to first pre-author run=True
author: exits=0,0; stdout identical=True; stderr identical=True; stderr bytes=0,0
initial author combined log differs only by 2 macOS xcodebuild diagnostic lines; checker stdout agrees exactly
RESULT: checker results repeat exactly; initial host-launcher diagnostics are retained in author_output.txt
```

The initial combined logs are not byte-identical because of host startup diagnostics; the checked SLP and checker results show no nondeterminism. No mathematical, count, hash, or object mismatch was found. The author-checker coverage discrepancy is addressed independently above.

## Scope of the verdict

`table-record/README.md` explicitly saves metadata only. It contains no reference scheme, raw source pages, or source JSON, so I cannot independently calibrate the reference scheme's counter, prove identity with a specific Perminov repository scheme, authenticate the extraction, or establish any live minimum or best-known-rank assertion. Those historical/external assertions are not treated as reproduced facts, and the table's currency and the result's novelty are left to the other skeptic as instructed. The submitted SLP and all data required for its exactness, ternarity, format, 176-product decomposition, and 699-addition verification are present and pass. No network or outside-folder source material was used.

pass: true
