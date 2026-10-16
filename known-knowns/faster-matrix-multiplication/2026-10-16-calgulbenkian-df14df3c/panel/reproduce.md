# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object passes this skeptic's delegated checks: exact integer matrix multiplication, ternary expanded forms and binary intermediates, straight-line order, 61 explicit products, 222 reduced additions, the recorded object hash, and deterministic reproduction. This verdict makes no live-table, novelty, or reference-product-identity judgment.

## Scope and reading order

I read `CLAIM.md`, the object, `INDEX.csv`, and `table-record/README.md`, then wrote `skeptic/check.py` from the definition. I completed its successful independent run and saved `skeptic/output.txt` before opening any author code in `verify-it-yourself/`. Only afterward did I read `REPRODUCE.md` and the author's code and run its checks. No network was used. Package reads were confined to this folder; the explicitly permitted external interpreter was used for the author's optional SymPy check.

The third-party reference scheme is deliberately absent. `table-record/README.md` names its URL and SHA256, but metadata cannot substitute for its bytes. I cannot recount that file, authenticate its recorded hash, or compare its U, V, W products offline. The live best rank, the minimum reference count across files, coefficient-class comparisons, Lille and matmulcatalog counts, and uniqueness/newness are assigned to the other skeptics. The saved assertion 233 is used here only to check the arithmetic 222 < 233. These scope exclusions follow the panel instruction and do not represent missing candidate-object data.

## Definition and criterion checked

The following success criterion is quoted from `CLAIM.md`, changing only the format's angle brackets to braces to avoid literal template placeholders. The Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html, with only its placeholder brackets changed to braces; that template is explanatory and is not present literally in the quoted paragraph in this copy of `CLAIM.md`.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The saved-file layout and counting definition, quoted from `CLAIM.md`:

> - `object/`: the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

The stated verification method, quoted from `CLAIM.md`:

> Parse the SLP (sequence of assignments t_k = +/- t_i +/- t_j over inputs A_ij, B_jl, intermediate sums, r products, and output assignments). Evaluate it with sympy (or exact integer evaluation at many random integer matrices plus one symbolic pass) and confirm every output equals the corresponding entry of A*B. Count the additions under the stated convention (exclude negations, exclude the r multiplications). Load the reference scheme from Perminov's addition_reduced_ZT directory (and reduced_known.json), recount its additions with the same counter to calibrate the convention, and compare. Re-fetch the repository, the Lille page and COVERAGE.md. Minutes on this Mac.

Thus the directly checkable clauses are: explicit linear forms and products; the dimension bound; the integer tensor identity; permitted signs and ternary expanded intermediates; valid straight-line dependencies; the addition convention and candidate count; and consistency with the saved object hash and metadata. Equality with the live best rank and all external comparison clauses remain outside this offline role. I verify 61 explicit nonzero products, not a lower bound proving minimal tensor rank.

## Independent derivation and properties

`skeptic/check.py` uses Python's standard library and exact arbitrary-precision integers. It imports no author code. JSON is parsed with duplicate-key rejection, strict integer types, exact expected keys, positive dimensions, and `z2` required to be false. The object SHA256 must equal the one-row `INDEX.csv` value; the object name, cell, target, product count and dimension labels must agree.

Each U input is the unit vector for row-major A[i,j], each V input is the unit vector for row-major B[j,k], and each W input is the unit vector for product q. For every fresh assignment, each index must designate an input or an earlier fresh assignment. Final rows may use only inputs and completed fresh assignments. Every stored scalar is exactly +1 or -1, every form is nonempty, and every expanded fresh and final vector is nonzero and has coefficients entirely in {-1,0,1}. All 297 named forms are checked: U has 59 fresh and 61 final; V has 61 fresh and 61 final; W has 35 fresh and 20 final. All 61 product forms are nonzero, distinct up to sign, and used by outputs.

For a form with L terms, a binary tree has exactly L-1 additions; signs on leaves are free. I additionally construct a binary tree whose every expanded internal node remains ternary. The construction searches subset partitions of each form, and a separate recursive execution verifies the resulting tree and its coefficients. The complete deterministic witness is `skeptic/binary_witness.json`. U, V and W require 59, 61 and 102 binary additions respectively, so the actual witnessed total is 222. No multiplication by any scalar other than a sign occurs. The 61 bilinear products are excluded as the definition requires. Expanded nonzero counts also give 452 naive additions, matching the object's other complexity field.

The first independent implementation imposed a left-to-right fold on each list. It stopped at `w.final[15]` because that arbitrary fold temporarily produces coefficient 2. The definition calls a form a sum and does not fix a binary parenthesization. I corrected that extra assumption before reading the author code. The saved binary witness proves that this form, and every other form, has a ternary binary realization at exactly L-1 additions. No object was changed. This is a parenthesization issue, not a failed tensor or expanded-form check.

For exactness, let U[q,a], V[q,b] and W[c,q] be the expanded integer rows. The output coefficient of A[a] B[b] is exactly

`T[c,a,b] = sum_q W[c,q] * U[q,a] * V[q,b]`.

Write c = k*4+i, a = iA*4+jA, b = jB*5+kB. The target coefficient is 1 exactly when iA=i, kB=k and jA=jB, and 0 otherwise. I compare every one of the 20*16*20 = 6,400 coefficients, including zeros. There are 80 ones and 6,320 zeros. This re-derives the full symbolic bilinear identity over Z without random sampling. A separate implementation directly executes the stored SLP on all 16*20 = 320 input basis pairs and compares all 6,400 output values. Because the SLP is bilinear, this is the complete basis, not a sample of an exhaustive search.

`skeptic/recheck.py` reruns the independent checker and each author command in fresh processes with two different hash seeds, comparing complete output bytes. It also checks the binary witness bytes and hashes all eight original saved package files before and after these reruns. `skeptic/package_hashes.json` is an inventory of the saved bytes, not an external authenticity claim. The object hash has the additional independent expected value in `INDEX.csv`.

## Exact commands and captured output

All commands below are run from this folder and exited 0. The SymPy command uses the user-specified interpreter via a relative executable path; default `python3` lacks SymPy. The independent checker requires no additional packages.

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output.repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output.repeat.txt
```

The complete successful output in `skeptic/output.txt` follows, inserted directly from that file:

```text
object: object/4x4x5_m61_cr222_ZT_reduced.json
sha256: df14df3c1a01189e540ab5a0eedebc331cd08e12714d795df0884481da292366 (matches INDEX.csv)
format: 4x4x5; max dimension=5 <= 8; products=61; ring=Z
U: inputs=16, fresh=59, final=61, additions=59, ternary_forms=120, ternary_binary_nodes=59; order/scalars OK
V: inputs=20, fresh=61, final=61, additions=61, ternary_forms=122, ternary_binary_nodes=61; order/scalars OK
W: inputs=61, fresh=35, final=20, additions=102, ternary_forms=55, ternary_binary_nodes=102; order/scalars OK
  ternary parenthesization required instead of list-order fold: w.final[15]
binary witness: skeptic/binary_witness.json sha256=9b412e81e85ed15c74b78d1fc755efe9c3af20e75bcb22d1b58f86bd1abcd4f8
products: 61 nonzero, distinct up to sign, and used in outputs
exact tensor: 6400/6400 integer coefficients match A*B; 80 ones and 6320 zeros; all 20 outputs
exhaustive basis execution: 320/320 input basis pairs; 6400 output values match (complete bilinear basis, not sampling)
reduced additions: 59 + 61 + 102 = 222; matches object, filename, CLAIM.md, INDEX.csv
expanded naive additions: 452; matches object metadata
saved-reference arithmetic only: 222 < 233, difference=11
object bytes unchanged during verification
scope: reference scheme and live sources are absent; no reference recount, product-identity comparison, live-table or novelty judgment
PASS: all saved-object checks
```

```sh
python3 verify-it-yourself/check_slp.py object/4x4x5_m61_cr222_ZT_reduced.json > skeptic/author_output.txt 2>&1
```

```text
{"file": "4x4x5_m61_cr222_ZT_reduced.json", "format": "4x4x5", "rank": 61, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 59, "adds_V": 61, "adds_W": 102, "adds_total": 222, "naive_total": 452, "declared_reduced": 222, "VALID": true}
```

```sh
sh verify-it-yourself/run_checks.sh > skeptic/author_run_output.txt 2>&1
```

```text
sha256 matches INDEX.csv (df14df3c1a01189e540ab5a0eedebc331cd08e12714d795df0884481da292366)
== check_slp.py on object/4x4x5_m61_cr222_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x4x5_m61_cr222_ZT_reduced.json", "format": "4x4x5", "rank": 61, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 59, "adds_V": 61, "adds_W": 102, "adds_total": 222, "naive_total": 452, "declared_reduced": 222, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=222, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

```sh
../../../.venv/bin/python verify-it-yourself/sym_check.py object/4x4x5_m61_cr222_ZT_reduced.json > skeptic/author_sympy_output.txt 2>&1
```

```text
{"file": "4x4x5_m61_cr222_ZT_reduced.json", "format": "4x4x5", "rank": 61, "products": 61, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 222}
```

```sh
python3 skeptic/recheck.py > skeptic/determinism_output.txt 2>&1
```

```text
saved-file SHA256 manifest: skeptic/package_hashes.json
python3: Python 3.9.6
sympy interpreter: Python 3.9.6
independent: exit 0; complete output identical to saved output for hash seeds 1 and 8675309
author: exit 0; complete output identical to saved output for hash seeds 1 and 8675309
author run script: exit 0; complete output identical to saved output for hash seeds 1 and 8675309
author sympy: exit 0; complete output identical to saved output for hash seeds 1 and 8675309
original saved files unchanged: 8/8
binary witness bytes identical across independent reruns
PASS: deterministic outputs, witness, and unchanged saved package
```

## Comparison and mismatches

The independent result and both author checkers agree on the 4x4x5 format, 61 products, exact transposed output layout, and 222 additions. The author's main checker also agrees on U/V/W subtotals and naive count. SymPy's `C=AB: false` is expected because the saved output order is `C^T`, as specified in the definition; every corresponding matrix entry is correct.

There is a verification-coverage discrepancy: `REPRODUCE.md` advertises checking every expanded intermediate's ternary coefficients, but `verify-it-yourself/check_slp.py` merely checks each stored term's sign and never tests the coefficients of its expanded vectors. `sym_check.py` also checks stored signs, not every expanded intermediate. Neither omission establishes a false candidate property here: the independent checker explicitly verifies all expanded forms and also witnesses every binary intermediate. The author's run script rejects its sign-flipped negative control, but that control alone would not cover this omission.

No disagreement about the saved object's claimed properties remains. The reference recount, reference-product identity and external record comparisons were not attempted or inferred from metadata. Within the explicitly assigned offline scope, every checkable property passes.

pass: true
