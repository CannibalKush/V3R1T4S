# Independent REPRODUCE report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved candidate passes the independent reproduction checks. It computes the full 6x8x8 matrix product exactly over Z with 266 nonzero, used products and 993 reduced additions. This is a reproduction verdict, with no judgment of table currency, best-known rank, or novelty.

I read CLAIM.md and the object layout, wrote skeptic/definition.txt and skeptic/check.py, and ran that checker before opening any file in verify-it-yourself/. I used no network and inspected no outside documents or repositories. The only outside interpreter used was the explicitly permitted environment for the optional SymPy check. All artifact names below are relative to this folder.

## Quoted definition and locally checkable criterion

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs)

> with max(n,m,p) <= 8

> (1) is verified symbolically to compute the full product A*B exactly over Z

> (2) uses a number of additions/subtractions STRICTLY LESS (direction: min)

> counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP)

> The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

> the ternary condition on every expanded intermediate

The claim also states:

> using 993 additions/subtractions under Perminov's reduced counting convention, strictly fewer than 1161

The comparison clause is:

> AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column.

And the reference convention is:

> The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files).

For the Lille URL template, I use https://fmm.univ-lille.fr/{n}x{m}x{p}.html, changing only the brackets. The quotations above are excerpts from CLAIM.md; omitted live-source clauses concern the other skeptic's table review.

## Independent derivation and coverage

1. Parsed the saved JSON with duplicate-key rejection. Checked dimensions exactly (6,8,8), the dimension bound, the integer product count 266, characteristic-zero metadata, row counts, nonempty forms, integer indices and signs, and every reference's causal order. Final forms cannot refer to other final forms.
2. Assigned each map input its independent unit vector. For each fresh form, summed its signed referenced vectors using unbounded Python integers, then appended the result at the prescribed fresh index. Expanded all final forms the same way. Checked every expanded fresh and final coefficient belongs to {-1,0,1}. This includes W's linear combinations over independent product symbols. All 689 fresh forms and all 580 final forms pass; no scalar other than a sign is used.
3. Wrote each product as U[t](A)*V[t](B), and each output as the W-weighted sum of those products. By distributivity, its coefficient of A[a]*B[b] is sum over t of W[output,t]*U[t,a]*V[t,b]. Independently constructed the target coefficient: one exactly when a=i*8+j and b=j*8+k for a shared j, otherwise zero; output=k*6+i. Compared all 48*48*64=147456 coefficients, including all 147072 required zeros. This proves the polynomial identity over Z for every input, rather than sampling matrices. All 266 product factors are nonzero and all products occur in expanded W. This proves a 266-product decomposition, without proving rank minimality.
4. Counted each saved form of length L as L-1 binary additions/subtractions, including fresh and final forms, with free negations and excluding the 266 bilinear multiplications. U contributes 255, V 274, W 464, totaling 993. Expanded-map naive cost is independently 3788. Both values match the object's metadata. The saved comparison satisfies 993 < 1161, a difference of 168.
5. Checked the sole INDEX.csv row's target, cell, path, SHA256, candidate count and saved reference count. Repeated the independent checker and compared full output bytes. Then ran the author's checkers and its negative control, compared the two author tensor-check outputs, and checked agreement with the SymPy output. No candidate is missing and no numerical mismatch or non-determinism was observed. There is no exhaustive-search claim here; the tensor check itself is exhaustive.

## Exact commands and captured output

Run from this folder, in the order shown. The independent checker uses only python3's standard library.

```sh
python3 skeptic/check.py object/6x8x8_m266_cr993_ZT_reduced.json > skeptic/output.txt 2>&1
```

Exit status: 0. Full output, inserted directly from skeptic/output.txt:

```text
Independent exhaustive SLP verification (Python integer arithmetic)
Object: object/6x8x8_m266_cr993_ZT_reduced.json
SHA256: 353b922983ecc35f13d03a9e7136407be941d5a3282630c9eb9c13af94c236ec
Format: 6x8x8; max dimension <= 8; products=266; arithmetic=Z
U: inputs=48; fresh=255; finals=266; additions=255; all references causal; all stored scalars and expanded forms ternary
V: inputs=64; fresh=274; finals=266; additions=274; all references causal; all stored scalars and expanded forms ternary
W: inputs=266; fresh=160; finals=48; additions=464; all references causal; all stored scalars and expanded forms ternary
Tensor: checked all 147456 coefficients across 48 outputs; nonzero=384; zero=147072; mismatches=0
Identity: C[i,k] = sum(j=0..7) A[i,j]*B[j,k] exactly over Z; W output index=k*6+i
All 266 nonzero bilinear products are used; this verifies a 266-product decomposition, not minimality of rank
Reduced additions: 255+274+464=993; metadata matches; negations free; products excluded
Expanded naive additions: 3788; metadata matches
Numeric comparison only: 993 < 1161; improvement=168
Full tensor coefficient SHA256: f5589b9af6dba80825bde12aef4eb57255283d4d120aece2a02a16abd5960a9e
PASS: all object-local properties checked exhaustively; live/source/table claims require separate evidence
```

After that run I opened verify-it-yourself/, REPRODUCE.md, table-record/README.md and INDEX.csv. The subsequent successful verification commands were:

```sh
python3 verify-it-yourself/check_slp.py object/6x8x8_m266_cr993_ZT_reduced.json > skeptic/author_output.txt 2>&1
python3 skeptic/check.py object/6x8x8_m266_cr993_ZT_reduced.json > skeptic/output_repeat.txt 2>&1
../../../.venv/bin/python verify-it-yourself/sym_check.py object/6x8x8_m266_cr993_ZT_reduced.json > skeptic/author_symbolic_output.txt 2>&1
sh verify-it-yourself/run_checks.sh > skeptic/author_run_output.txt 2>&1
python3 skeptic/compare.py > skeptic/comparison_output.txt 2>&1
```

All exited 0. The relative interpreter path above resolves to the interpreter explicitly permitted in the instructions. The initial optional SymPy command below exited 1 because system python3 lacked sympy; the complete diagnostic is preserved in skeptic/author_symbolic_system_output.txt. The successful invocation with the permitted interpreter resolves that environment issue.

```sh
python3 verify-it-yourself/sym_check.py object/6x8x8_m266_cr993_ZT_reduced.json > skeptic/author_symbolic_output.txt 2>&1
mv skeptic/author_symbolic_output.txt skeptic/author_symbolic_system_output.txt
```

Author tensor-check output, inserted from skeptic/author_output.txt:

```text
{"file": "6x8x8_m266_cr993_ZT_reduced.json", "format": "6x8x8", "rank": 266, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 255, "adds_V": 274, "adds_W": 464, "adds_total": 993, "naive_total": 3788, "declared_reduced": 993, "VALID": true}
```

Author SymPy output, inserted from skeptic/author_symbolic_output.txt:

```text
{"file": "6x8x8_m266_cr993_ZT_reduced.json", "format": "6x8x8", "rank": 266, "products": 266, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 993}
```

Author run-script output, inserted from skeptic/author_run_output.txt:

```text
sha256 matches INDEX.csv (353b922983ecc35f13d03a9e7136407be941d5a3282630c9eb9c13af94c236ec)
== check_slp.py on object/6x8x8_m266_cr993_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "6x8x8_m266_cr993_ZT_reduced.json", "format": "6x8x8", "rank": 266, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 255, "adds_V": 274, "adds_W": 464, "adds_total": 993, "naive_total": 3788, "declared_reduced": 993, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=993, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

Comparison output, inserted from skeptic/comparison_output.txt:

```text
Independent checker replay: byte-for-byte identical output.
INDEX.csv: one row; target, cell, file, SHA256, value=993 and table_value=1161 match.
Author checker agrees: exact tensor C^T; rank=266; U/V/W=255/274/464; total=993; naive=3788; random evaluation passes.
Author checker replay: identical JSON; run script passes; sign-flip negative control rejected.
Author SymPy check agrees: 266 products; exact C^T; reduced additions=993.
No numerical mismatch or observed non-determinism.
```

## Discrepancy and scope

REPRODUCE.md says the author's checker checks every expanded intermediate and output for ternary coefficients. Source inspection shows check_slp.py expands these forms but never tests their expanded coefficient range; sym_check.py also checks only stored signs. This is a documentation/checker-coverage discrepancy. The independent checker explicitly checks every expanded form and confirms that this candidate satisfies the promised condition, so the discrepancy does not invalidate the candidate or produce a disagreement about its tensor or count.

The table-record folder explicitly contains metadata only. It contains no reference scheme to recount and no source snapshots with which to rederive the asserted repository minimum, live rank, absence of lower published counts, or identity with Perminov's particular rank-266 scheme. I confirm the saved numeric comparison and metadata consistency only. I do not certify those external assertions or infer table currency or novelty. No reference recount or equivalence to an absent upstream scheme is claimed in this verdict.

The object-local exactness, ternary condition, product count, dimension bound, saved reduced count, and deterministic reproducibility are all independently confirmed.

pass: true
