# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved straight-line program reproduces the claimed exact integer matrix multiplication with 183 product gates and 695 reduced additions. This is an object-reproducibility verdict. It does not assess current table values or novelty.

## Definition and criterion checked

Source: `CLAIM.md`, success criterion (quoted in full so that every locally checkable clause is visible):

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

In this quotation I changed only the brackets of the format placeholder to braces. The Lille URL template is written as https://fmm.univ-lille.fr/{n}x{m}x{p}.html; for this template, only the brackets are changed.

The exactness condition is:

> is verified symbolically to compute the full product A*B exactly over Z

The counting convention is:

> each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP

The saved-object definition in `CLAIM.md` is:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

## Independent construction and proof

I read `CLAIM.md` and the object schema, then wrote `skeptic/check.py` and ran it before opening any file in `verify-it-yourself/` or reading `REPRODUCE.md`. The checker uses Python integer arithmetic and sparse coefficient dictionaries, with no author's imports or sampling.

1. **Object and format.** Strict JSON parsing rejects duplicate keys, unexpected fields, noninteger indices/scalars, empty forms, out-of-range references, and forward references. The dimensions are 6x6x7, so the maximum dimension is 7 and satisfies the bound 8. There are exactly 183 U and V factors and 42 outputs. All 183 product gates have nonzero factors and occur in the expanded W map. Here rank 183 means the exhibited decomposition has 183 product gates; no lower-bound or best-known-rank assertion is inferred.
2. **Linear-form expansion and ternarity.** Each map starts with standard basis vectors for its inputs. Inductively, substituting the exact vectors of earlier nodes into each signed form yields its exact integer coefficient vector. Every term scalar is +1 or -1. Every coefficient in every expanded fresh and final form is in {-1,0,1}, including W expanded over the 183 product inputs. Implicit zero coefficients are retained mathematically by sparse representation. There are 184+182+119=485 fresh forms and 183+183+42=408 final forms; all 893 forms are checked.
3. **Exact bilinear identity.** For product gate t, the outer product of expanded U[t] and V[t] gives every coefficient of A[a]B[b]. For output k*6+i, summing those outer products with coefficients W[k*6+i,t] gives its full bilinear tensor. The expected tensor contains coefficient 1 exactly at (A[i,j],B[j,k]) for each j, and 0 elsewhere. Dictionary equality checks all 42*36*42=63,504 coefficients, including zeros. All 42 outputs match, with 252 nonzero coefficients altogether. Linear substitution and distributivity therefore prove equality over Z for every pair of input matrices. The output layout is the declared transposed layout, C[i,k] at k*6+i.
4. **Operation count.** A form with L terms is realizable by L-1 binary additions/subtractions; signs cost nothing. Summing over every saved fresh and final form gives U=184, V=182, W=329, total 695. The 183 bilinear products are counted separately. No other scalar multiplication occurs. Counting nonzeros in the expanded final maps gives the independent naive count 2502, matching the object's metadata.
5. **Saved numerical comparison and identity.** The object's SHA-256 matches `INDEX.csv`. Its target, cell, object path, value 695 and recorded table value 769 are consistent. The arithmetic comparison is 695 less than 769, an improvement of 74 additions. `table-record/README.md` records the same reference value. This checks the saved numbers, not their external truth or currency.
6. **Determinism and completeness.** Independent and author checker outputs are each byte-identical on two runs. The independent proof has no random tests and checks every tensor coefficient. The package claims an exhibited program, not an exhaustive search or optimality proof for 695; there is no search enumeration to sample.

The saved reference material is metadata only. The original reference scheme and fetched source bodies are absent, so I cannot independently recount the reference scheme, establish identity with the repository's scheme, or certify the external minimum, best-known rank, coefficient-class comparison, live-fetch timing or uniqueness of the claim. Those external comparisons are outside this skeptic's requested scope and are left to the other skeptic. The claimed candidate object itself is present.

## Commands and actual output

All file names below are relative to this folder. First, before reading the author's code:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output-repeat.txt
```

`cmp` exited 0 with no output. Full `skeptic/output.txt`:

```text
Independent exact integer SLP check
object: object/6x6x7_m183_cr695_ZT_reduced.json
sha256: 34a5c13ccfa01ac91606b8899c53be5f1facf7f62f1e06e9ddf5f9ec6bf82ea5
format=6x6x7; dimension bound <=8: OK; product gates=183; z2=false
u: inputs=36, fresh=184, final=183, forms=367, additions=184, term_histogram={1: 183, 2: 184}
u: all references valid; all term scalars +/-1; all fresh and final expansions ternary
v: inputs=42, fresh=182, final=183, forms=365, additions=182, term_histogram={1: 183, 2: 182}
v: all references valid; all term scalars +/-1; all fresh and final expansions ternary
w: inputs=183, fresh=119, final=42, forms=161, additions=329, term_histogram={1: 2, 2: 74, 3: 45, 4: 17, 5: 12, 6: 5, 7: 1, 8: 5}
w: all references valid; all term scalars +/-1; all fresh and final expansions ternary
tensor identity: 42 outputs; 63504 coefficients checked; 252 nonzero coefficients; exact over Z: OK
reduced additions: 184 + 182 + 329 = 695; claimed 695: OK
expanded naive additions: 2502; metadata: OK
695 < 769: OK (numeric comparison only; external reference status not assessed)
All 183 product gates have nonzero factors and occur in the expanded output map.
No sampling or probabilistic identity test used.
PASS: all object-level checks
```

Only afterward, I read the author's code and reproduction instructions, then ran:

```sh
python3 verify-it-yourself/check_slp.py object/6x6x7_m183_cr695_ZT_reduced.json > skeptic/author-output.txt 2>&1
python3 verify-it-yourself/check_slp.py object/6x6x7_m183_cr695_ZT_reduced.json > skeptic/author-output-repeat.txt 2>&1
cmp skeptic/author-output.txt skeptic/author-output-repeat.txt
```

`cmp` exited 0 with no output. Full `skeptic/author-output.txt`:

```text
{"file": "6x6x7_m183_cr695_ZT_reduced.json", "format": "6x6x7", "rank": 183, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 184, "adds_V": 182, "adds_W": 329, "adds_total": 695, "naive_total": 2502, "declared_reduced": 695, "VALID": true}
```

The default `python3` lacks SymPy (`ModuleNotFoundError: No module named 'sympy'` on the initial symbolic-check attempt). I reran that check using the interpreter explicitly supplied in the task, expressed relatively below. This was a runtime dependency issue, not an object mismatch.

```sh
../../../.venv/bin/python verify-it-yourself/sym_check.py object/6x6x7_m183_cr695_ZT_reduced.json > skeptic/author-symbolic-output.txt 2>&1
```

Full successful `skeptic/author-symbolic-output.txt`:

```text
{"file": "6x6x7_m183_cr695_ZT_reduced.json", "format": "6x6x7", "rank": 183, "products": 183, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 695}
```

Finally:

```sh
python3 skeptic/check_package.py > skeptic/package-output.txt
```

Full `skeptic/package-output.txt`:

```text
INDEX.csv: one row; object path, sha256, target, cell, value 695 and recorded comparison 769 match.
object/: exactly the one claimed object is present.
Independent checker repeated output: byte-identical.
Author checker repeated output: byte-identical (its random trials use a fixed seed).
Author and independent results agree: C^T, rank 183, additions 184+182+329=695, naive 2502.
Saved reference metadata gives 769; arithmetic improvement is 74 additions.
No claim of exhaustive search or optimality of 695 appears in the package; no search result is being sampled.
```

## Discrepancies and verdict

There is no disagreement about the saved object's tensor identity, format, product count, output ordering, ternarity, SHA-256 or addition counts. Both author checks agree with the independent proof.

There is one verification-documentation discrepancy: `REPRODUCE.md` advertises a check of every expanded intermediate's ternarity, but `verify-it-yourself/check_slp.py` only validates the term scalars; it never tests the expanded coefficient magnitudes. `verify-it-yourself/sym_check.py` likewise tests term scalars rather than every expanded linear intermediate. The independent checker explicitly supplies the missing test and all forms pass, so this gap does not invalidate this object.

All object properties checkable from the saved files have been confirmed. No network was used, and no external claim package or repository material was inspected.

pass: true
