# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved object passes the local reproduction checks: exact integer matrix multiplication, ternary expanded forms, valid straight-line references, 170 products, 667 reduced additions, matching object hash, and deterministic results.

## Scope

Only this package was inspected; no network was used. The independent definition and checker were written and successfully run before opening `verify-it-yourself/` or `REPRODUCE.md`. `skeptic/determinism.txt` records the independent checker and output hashes at that point.

`table-record/README.md` is metadata, not the reference scheme or saved source pages. Perminov's third-party reference object is deliberately absent; its URL and claimed sha256 are recorded there. Without network I cannot recount its 720 additions, verify its hash, or prove that its expanded products coincide with the candidate. These are scoped out as directed. I also do not assess table currency, novelty, optimal rank, the minimum over the live reference directory, live Lille/coefficient-class comparisons, matmulcatalog, or whether the scheme was previously claimed. The other skeptics handle those comparisons. The arithmetic comparison 667 < 720 is confirmed only against the recorded number. External-source hashes in the metadata cannot be authenticated without their missing source bytes; this is not a missing component of the saved candidate object.

## Quoted definition and criterion

The following was recorded in `skeptic/definition.txt` before writing the checker. It quotes every clause of the success criterion, including clauses outside this skeptic's offline scope, and the package's explicit SLP interpretation.

Source: CLAIM.md. Recorded before reading verify-it-yourself/.
Quotation notation: only angle brackets in format placeholders are changed to braces. If expressing the Lille URL template, it is https://fmm.univ-lille.fr/{n}x{m}x{p}.html (only the placeholder brackets changed); CLAIM.md itself names the live per-format page without that URL template.

Success criterion (quoted in full, with the bracket substitution above):
"Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one."

Object interpretation (quoted):
"the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free."

Local target: dimensions (5,6,8), 170 bilinear products, integer exactness, coefficients in {-1,0,1}, 667 reduced additions; stored naive count 2312; INDEX.csv object sha256; deterministic results. Comparing 667 with the recorded number 720 is arithmetic only and does not establish any live-table fact.

## Independent derivation and checks

The independent implementation is `skeptic/check.py` and uses only Python's standard library and exact integers. It does not import or call author code.

1. **Object, dimensions, products, and hashes.** Parse the object with duplicate JSON keys rejected. Require the complete expected schema; integer dimensions (5,6,8), maximum dimension 8, exactly 170 products, characteristic-zero arithmetic, and exactly 170 U rows, 170 V rows, and 40 output rows. All product factors are nonzero and all products occur in W. Recompute sha256 from the object bytes and compare with `INDEX.csv`; verify its target, cell, file, and value fields. The object hash is unchanged after all runs. This establishes a 170-product decomposition, not rank optimality.

2. **Straight-line order and allowed scalars.** U has 30 inputs, V has 48 inputs, W has 170 independent product inputs. For fresh row k, the only available indices are inputs and the earlier fresh rows. Final rows may refer to inputs and any completed fresh row, never other final rows. Require every form to be nonempty, every term index to be an integer in range, and every stored coefficient to be exactly +1 or -1. This proves the dependency order and excludes other scalar multiplications. Zero expanded coefficients are implicit.

3. **Every expanded intermediate and output is ternary.** Start with integer unit vectors over each map's inputs. Replace each referenced input or previously expanded row in every fresh and final form by its vector, multiply by the stored sign, and sum over Z. By induction this vector is the exact linear form computed by that assignment. Check all 844 declared fresh/final vectors coefficient by coefficient for membership in {-1,0,1}, including W intermediates over the independent product variables. No reduction modulo 2 is used.

   I also constructed an explicit binary summation order for every form, requiring every binary partial sum to be ternary. `skeptic/binary_orders.json` stores zero-based positions in each form. A separate replay in `skeptic/compare.py` verifies these schedules. My initial checker incorrectly imposed left-to-right summation on list forms; that extra condition rejected a partial sum in `w[11]`. The definition specifies a sum of terms, without requiring that association. Before reading author code I corrected this by checking declared expansions and constructing valid binary orders. Every form works in stored term order except `w[11]`, which works in order [0,2,1]. Integer commutativity/associativity preserves that form and its two-addition cost. Thus the initial rejection was a checker assumption, not a mismatch with the stated definition; the saved schedule also certifies ternary binary intermediates under the stronger interpretation.

4. **Full tensor identity over Z.** For product s, let U[s,a], V[s,b] be the exact expanded factors and W[o,s] the expanded output coefficient. Accumulate every integer coefficient T[o,a,b] = sum_s W[o,s] U[s,a] V[s,b]. Output o=k*5+i must have coefficient 1 exactly for a=i*6+j and b=j*8+k with the same j; every other coefficient must be 0. Check all 40*30*48 = 57,600 entries: 240 ones and 57,360 zeros. Substitution in item 3 and distributivity show that these are precisely the coefficients of every output polynomial. Matching every coefficient proves the complete matrix product for all inputs over Z, without sampling.

5. **Exhaustive separate SLP execution.** A second path executes the original stored assignments as scalar integer arithmetic, without using the expanded vectors. Evaluate all 30*48 = 1,440 pairs of A and B unit inputs and compare all 40 outputs each time to direct matrix multiplication. Bilinearity means these pairs cover every tensor coefficient. This is exhaustive, not a random spot check, and independently confirms the transposed output layout.

6. **Reduced addition count.** A form with L signed available quantities needs L-1 binary additions/subtractions; an initial sign and any unary negation are free. Sum this across all fresh and final forms and exclude the 170 bilinear products. U contributes 159+0=159; V contributes 196+0=196; W contributes 215+97=312. Total: 159+196+312=667. Independently expand away the sharing and compute nz(U)+nz(V)+nz(W)-2*170-40=2312. Both counts match the object's `complexity` fields. The reduced count matches `INDEX.csv`; 720-667=53 using only the recorded comparison number.

7. **Determinism and author comparison.** Run the independent checker twice in separate processes and compare its complete outputs byte for byte. Afterward run the author's supplied shell script and standalone checker. Their JSON results are identical across runs and agree with the independent dimensions, products, tensor layout, exactness, and counts. The shell script reports `ALL CHECKS PASS`, including its sign-flip negative control. Its random trials supplement an exact tensor computation; no random sample is used as the basis for this verdict. Inspection shows that the author's `check_slp.py` validates stored term signs but does not explicitly check ternarity of every expanded intermediate; the independent checks above establish that property for this object. There is no remaining numerical or structural disagreement.

## Exact commands and captured output

All commands are run from this folder. No external dependencies are required.

Independent checker:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output_repeat.txt 2>&1
```

Both runs exit 0. Full actual output from `skeptic/output.txt` follows, inserted directly from that file:

```text
object: object/5x6x8_m170_cr667_ZT_reduced.json
sha256: efb7f10c7e3a5dcd2481aacbd72ae5e308550dd825927d1c1114574354447c80 (matches INDEX.csv)
format: 5x6x8; products: 170; max dimension: 8; arithmetic: Z
U: inputs=30, fresh=159, final=170, additions fresh=159, final=0, total=159
V: inputs=48, fresh=196, final=170, additions fresh=196, final=0, total=196
W: inputs=170, fresh=109, final=40, additions fresh=215, final=97, total=312
straight-line order and +/-1 term coefficients: PASS; all 844 declared expanded forms ternary: PASS
ternary binary evaluation orders: PASS; reordered sums: w[11]
binary evaluation schedules: skeptic/binary_orders.json (zero-based term positions)
full tensor over Z: PASS; 57600 coefficients, 240 required ones, 57360 required zeros
exhaustive direct SLP evaluation: PASS; 1440 basis pairs, 57600 output entries
reduced additions: 667; expanded naive additions: 2312; stored complexity: MATCH
667 < recorded 720: TRUE (difference 53; reference count not independently recounted)
expanded maps sha256: 2388f58c04dcebddba4c40d4845e3f39f2b87b7a0e5e4dab68877a8bfda729ba
local object checks: PASS
scope: no live-table verification or comparison of products with absent third-party reference
```

The independent-output comparison and pre-author-read hashes were captured in `skeptic/determinism.txt`:

```text
independent checker: two successful runs; outputs byte-identical
output sha256: 3319f0d2ac4767657577221c59a8a0e82e95e18f24fe2f5854bb034f0d73411e
e366b8503e3efb332e9be3f8c11b40e815472c1677f7f613c4ab027a936ac52e skeptic/definition.txt
652f7884c995fd54e60df6b3f6246cb0a8d37696b293f5d083357a8aaf786402 skeptic/check.py
3319f0d2ac4767657577221c59a8a0e82e95e18f24fe2f5854bb034f0d73411e skeptic/output.txt
9f33b1be354b36552099407a8d12c09e625d31c54fe90d28aea9e9380b6b1f1f skeptic/binary_orders.json
These hashes were recorded before reading verify-it-yourself/.
```

Author's checker, run only after the independent checker:

```sh
sh verify-it-yourself/run_checks.sh > skeptic/author_output.txt 2>&1
python3 verify-it-yourself/check_slp.py object/5x6x8_m170_cr667_ZT_reduced.json > skeptic/author_repeat.txt 2>&1
```

Both commands exit 0. Full actual shell-script output from `skeptic/author_output.txt`:

```text
sha256 matches INDEX.csv (efb7f10c7e3a5dcd2481aacbd72ae5e308550dd825927d1c1114574354447c80)
== check_slp.py on object/5x6x8_m170_cr667_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x6x8_m170_cr667_ZT_reduced.json", "format": "5x6x8", "rank": 170, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 159, "adds_V": 196, "adds_W": 312, "adds_total": 667, "naive_total": 2312, "declared_reduced": 667, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=667, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

Full actual standalone repeat output from `skeptic/author_repeat.txt`:

```text
{"file": "5x6x8_m170_cr667_ZT_reduced.json", "format": "5x6x8", "rank": 170, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 159, "adds_V": 196, "adds_W": 312, "adds_total": 667, "naive_total": 2312, "declared_reduced": 667, "VALID": true}
```

Determinism, agreement, binary-schedule replay, and final object hash:

```sh
python3 skeptic/compare.py > skeptic/comparison.txt 2>&1
```

Exit 0. Full actual output from `skeptic/comparison.txt`:

```text
author checker: two runs produce identical JSON results
agreement: format 5x6x8, 170 products, C^T layout, exact tensor, U=159, V=196, W=312, total=667, naive=2312
author run script: ALL CHECKS PASS; sign-flip negative control rejected
independent checker: two runs produce byte-identical full output
saved ternary binary schedules replayed: 844 forms; all prefixes ternary
w[11] zero-based term order: [0, 2, 1]
object sha256 after all runs: efb7f10c7e3a5dcd2481aacbd72ae5e308550dd825927d1c1114574354447c80
```

## Mismatches and verdict

No mismatch remains for the properties of the saved candidate object. The initial left-association assumption and its correction are disclosed above. A temporary log-comparison attempt also selected the shell log's first informational line instead of its JSON line; `skeptic/compare.py` corrects that parsing and compares the actual JSON results. Neither issue was an object defect. The independent checker has not been modified since its pre-author-read hash was recorded.

The local saved-object reproduction verdict is pass. It does not certify the external table comparisons or identity with the unshipped reference.

pass: true
