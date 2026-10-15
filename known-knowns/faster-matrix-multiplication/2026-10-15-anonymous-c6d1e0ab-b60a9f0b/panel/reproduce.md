Reproduction skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved straight-line program passes all locally checkable mathematical properties. It computes 6x6x8 matrix multiplication exactly over Z using 203 bilinear products and 719 additions/subtractions under the stated reduced convention. This report does not judge currency, novelty, or the external best-rank/table claims.

I read CLAIM.md, the object, INDEX.csv and table-record/README.md; wrote skeptic/check.py and skeptic/definition.md; and ran the independent checker before reading REPRODUCE.md or anything in verify-it-yourself/. The independent checker imports no author code and uses only standard-library Python integer arithmetic. No source outside this package was inspected and no network was used. For the optional SymPy check I used the preinstalled interpreter explicitly supplied in the task, named relatively below.

Definition and criterion read before author code

Source: CLAIM.md. In the quoted format notation, only angle brackets have been changed to braces to avoid template detection. For the requested Lille URL template, https://fmm.univ-lille.fr/{n}x{m}x{p}.html changes only the brackets; this URL template is not present in the supplied criterion paragraph.

Success criterion (including external clauses for scope)

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

Saved-object definition

> - `object/`: the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

Verification method

> Parse the SLP (sequence of assignments t_k = +/- t_i +/- t_j over inputs A_ij, B_jl, intermediate sums, r products, and output assignments). Evaluate it with sympy (or exact integer evaluation at many random integer matrices plus one symbolic pass) and confirm every output equals the corresponding entry of A*B. Count the additions under the stated convention (exclude negations, exclude the r multiplications). Load the reference scheme from Perminov's addition_reduced_ZT directory (and reduced_known.json), recount its additions with the same counter to calibrate the convention, and compare. Re-fetch the repository, the Lille page and COVERAGE.md. Minutes on this Mac.


Properties checked and proof re-derived

| Property | Independent method and result |
|---|---|
| Saved object integrity | Parsed JSON with duplicate-key rejection. SHA-256 matches INDEX.csv; filename, target and 719/836 values agree. |
| Explicit SLP and dimensions | Checked object fields, positive integer dimensions [6,6,8], maximum dimension 8, integer mode, exactly 203 U rows, 203 V rows and 48 W rows. Every term has an integer index and coefficient +1 or -1, and each reference targets an input or an already defined fresh variable. Empty forms are rejected. |
| Expanded ternary condition | Starting with identity basis vectors, expanded every fresh and final form by exact signed integer vector addition. All 377 U forms, 398 V forms and 192 W forms have every coefficient in {-1,0,1}. U/V use input-entry bases; W uses the 203-product basis. |
| Bilinear product count | Paired the 203 U and V forms. Each factor is nonzero and each product is used in W. This establishes a decomposition with 203 products; it does not prove a lower bound on tensor rank. |
| Full tensor identity | For every output, calculated every coefficient of every A-entry/B-entry pair over Z, including zeros. All 48*36*48 = 82,944 coefficients agree with matrix multiplication; exactly 288 are 1 and the rest are 0. Output indexing is exactly the specified k*6+i. No sampling was used for this proof. |
| Reduced addition count | Independently summed L-1 for each nonempty fresh/final form of length L. U: 174+0; V: 195+0; W: 244+106. Total 719. Unary negations cost zero; the 203 products are excluded; no other scalar coefficient is admitted. |
| Other saved numeric claims | Expanded-map naive count is 2514, matching complexity metadata. 719 is strictly less than the recorded number 836 by 117. |
| Repeatability | Repeated the independent checker and the author tensor checker; each pair of captured output files is byte-for-byte identical. Both cmp commands exited 0 with no output. |

The expansion proof is induction in the saved assignment order: input index a represents basis vector e_a, and a form with signed terms (index s, sign c) represents the vector sum of c times the previously established vectors. Thus the final vectors U[q], V[q] and W[o] are the exact integer linear maps executed by the SLP. For output o=k*6+i, its A[a]B[b] coefficient is sum over q of W[o][q]*U[q][a]*V[q][b]. Writing a=6*i_a+j_a and b=8*j_b+k_b, the required coefficient is 1 exactly when i_a=i, k_b=k and j_a=j_b, and 0 otherwise. The checker compares this formula at every index. Distributivity over Z then proves every output equals sum over j=0..5 of A[i,j]*B[j,k] for all inputs. This is a complete identity proof, not a random test or a claim of an exhaustive optimization search.

A form with L signed terms can be evaluated using one starting signed quantity and L-1 binary additions/subtractions; the permitted free sign handles a negative starting term. Summing this cost over all saved forms yields the claimed reduced count.

Exact independent commands (run from this folder; both checker runs exited 0):

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output-repeat.txt
```

Full real output from skeptic/output.txt, inserted directly from the saved file:

```text
object: object/6x6x8_m203_cr719_ZT_reduced.json
sha256: b60a9f0b2339bc2927201b903c73b030905b0b39cc6a12b3a3b53fc65da014cf
format: 6x6x8; max dimension=8; products=203; arithmetic=Z
U: inputs=36, fresh=174, final=203, additions(fresh,final)=(174, 0), expanded_max_abs=1
U: all 377 expanded forms ternary; all references in range and acyclic; all term coefficients signed units
V: inputs=48, fresh=195, final=203, additions(fresh,final)=(195, 0), expanded_max_abs=1
V: all 398 expanded forms ternary; all references in range and acyclic; all term coefficients signed units
W: inputs=203, fresh=144, final=48, additions(fresh,final)=(244, 106), expanded_max_abs=1
W: all 192 expanded forms ternary; all references in range and acyclic; all term coefficients signed units
products: exactly 203 nonzero bilinear products; every product used
tensor: all 82944 coefficients checked exactly; nonzero=288, expected=288; mismatches=0
identity: every C[i,k] = sum(j=0..5) A[i,j]*B[j,k], over Z
reduced additions: U=174, V=195, W=350, total=719; claimed=719
expanded naive additions: 2514; matches saved complexity metadata
recorded comparison: 719 < 836; margin=117
INDEX.csv: object filename, sha256, target and candidate/reference numbers agree
scope: external table freshness, best-rank status and source-scheme provenance not established by metadata
PASS: all locally checkable object properties verified exhaustively
```

Author comparison, run only after the independent checker passed:

```sh
TMPDIR=./skeptic sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
python3 verify-it-yourself/check_slp.py object/6x6x8_m203_cr719_ZT_reduced.json > skeptic/author-direct-output.txt 2>&1
python3 verify-it-yourself/check_slp.py object/6x6x8_m203_cr719_ZT_reduced.json > skeptic/author-direct-repeat.txt 2>&1
cmp skeptic/author-direct-output.txt skeptic/author-direct-repeat.txt
../../../.venv/bin/python verify-it-yourself/sym_check.py object/6x6x8_m203_cr719_ZT_reduced.json > skeptic/author-symbolic-output.txt 2>&1
```

All these commands exited 0. TMPDIR kept the author script's temporary negative-control files inside skeptic/. The relative interpreter location denotes the task-provided environment; ordinary python3 lacked SymPy on an initial optional attempt. The successful symbolic run is captured below.

Full real output from skeptic/author-output.txt:

```text
sha256 matches INDEX.csv (b60a9f0b2339bc2927201b903c73b030905b0b39cc6a12b3a3b53fc65da014cf)
== check_slp.py on object/6x6x8_m203_cr719_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
2026-10-15 05:35:19.536 xcodebuild[85319:74048464]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 05:35:19.852 xcodebuild[85319:74048463] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
{"file": "6x6x8_m203_cr719_ZT_reduced.json", "format": "6x6x8", "rank": 203, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 174, "adds_V": 195, "adds_W": 350, "adds_total": 719, "naive_total": 2514, "declared_reduced": 719, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=719, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

Full real output from skeptic/author-direct-output.txt (identical to skeptic/author-direct-repeat.txt):

```text
{"file": "6x6x8_m203_cr719_ZT_reduced.json", "format": "6x6x8", "rank": 203, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 174, "adds_V": 195, "adds_W": 350, "adds_total": 719, "naive_total": 2514, "declared_reduced": 719, "VALID": true}
```

Full real output from skeptic/author-symbolic-output.txt:

```text
{"file": "6x6x8_m203_cr719_ZT_reduced.json", "format": "6x6x8", "rank": 203, "products": 203, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 719}
```

Comparison and limitations

There is no numerical or identity disagreement: all checkers obtain 203 products, 719 additions and the specified transposed C layout; the author tensor checker also agrees on 174/195/350 and naive count 2514. The SymPy result C=AB false concerns the alternative row-major output interpretation, which CLAIM.md does not specify; C^T true is the required interpretation. The platform diagnostic lines in the run-script capture are incidental interpreter-launch messages, not differing mathematical results.

The author checker has an implementation omission relative to its advertised verification: check_slp.py checks each written term's sign but expand() never rejects coefficients outside {-1,0,1} in the expanded vectors. sym_check.py likewise checks written signs, not expanded intermediate coefficients. This gap does not invalidate this object because skeptic/check.py independently checks every expanded fresh and final form, and all pass. The author's 20 seeded random trials provide an additional spot check only; the exhaustive integer tensor identity supplies the proof.

table-record/README.md contains extraction metadata and hashes rather than the fetched reference objects, directory listing, source scheme, or page contents. Therefore the saved files support the arithmetic comparison 719 < 836, but cannot independently establish the minimum over reference files, recount a reference scheme, establish best-known rank or coefficient-class comparisons, or prove this is the specific scheme in Perminov's repository. I make no judgment about current table values, live re-fetch timing, or novelty; those are outside this reproduction check. There is no locally checkable object mismatch or missing object, and repeat executions gave deterministic checker results.

pass: true
