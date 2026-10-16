# Independent REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

## Definition and criterion checked

Source: `CLAIM.md`. The complete success criterion is quoted below so the locally checkable obligations and the externally delegated obligations remain explicit. The symbolic format tuple's ASCII angle brackets are rendered as Unicode angle brackets; no words are changed. The Lille URL template is written as https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only the brackets of that URL template are changed.

```text
Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format ⟨n,m,p⟩ with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.
```

The saved-object definition in `CLAIM.md` is:

```text
the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.
```

In particular, the counting convention is “each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP”, and the exactness condition is “is verified symbolically to compute the full product A*B exactly over Z”.

## Scope and independence

I read `CLAIM.md`, `INDEX.csv`, `table-record/README.md`, and the saved object before creating `skeptic/check_object.py`. I completed and ran that independent checker, saving `skeptic/output.txt`, before opening any file in `verify-it-yourself/` or `REPRODUCE.md`. The independent checker uses Python's standard library, imports no author code, and uses exact integer arithmetic. No network was used and no other folder's claim data or code was read.

This verdict covers the saved object's exactness, ternary condition, straight-line order, dimension bound, 58-product representation, operation counts, indexed object hash, and deterministic reproduction. It does not certify a tensor-rank lower bound or whether 58 is the current best listed rank.

The reference scheme is deliberately absent. `table-record/README.md` identifies it at https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x5x5_m58_cr221_cn357_ZT_reduced.json and records SHA256 `17cdcab30fdacdaf92464bbfd7ff135a1d39fada357114d400586e8cad1dcd9e`. Without network I cannot recount that reference, validate its hash against its bytes, or verify product identity with it. The other source bodies are also absent, so their recorded hashes and extracted table cells cannot be independently authenticated here. The arithmetic comparison with the saved value 221 is checked, but live minimum, coefficient-class comparisons, freshness, novelty, and identity with Perminov's scheme are delegated to the other skeptics as instructed. These disclosed external omissions do not determine this saved-object verdict.

## Properties and proof steps

1. **Presence, integrity, and schema.** Require the indexed object to exist; compute SHA256 from all 16,102 saved bytes and compare it with `INDEX.csv`. Require the single index row, target, cell, file, count, exact object keys, exact integer types, integer-ring flag, format 3x5x5, rank/product count 58, 58 U rows, 58 V rows, and 15 W rows. Reject duplicate JSON keys, malformed or empty forms, and any scalar other than integer +1 or -1. Maximum dimension is 5, within the stated bound of 8.
2. **Straight-line order.** Start U, V, and W with respectively 15, 25, and 58 formal basis vectors. For each fresh assignment, require every index to lie in the already-built basis, then append the result at the next index. Final forms can reference only those same inputs and completed fresh variables. Thus U and V are computed before the 58 products, and W after them; no future reference or cycle is possible. Every U/V factor is nonzero, and all 58 products have nonzero coefficients in the expanded outputs.
3. **Expanded ternary condition.** Expand every fresh and final row as an exact signed sum of basis vectors. U coefficients are over A entries, V over B entries, and W over the 58 formal product symbols. Check every coefficient belongs to {-1, 0, 1}. This includes all 143 fresh rows and all 131 final rows. Also check all 485 signed prefixes, giving an explicit left-to-right binary realization whose temporary sums remain ternary. W's ternary condition is on its linear map over product symbols; its composed bilinear polynomials are checked by the tensor identity.
4. **Full tensor identity.** By induction over the ordered assignments, expanded U and V rows equal the saved factor programs, and expanded W rows equal the saved output program. Product t therefore contributes W[o,t] U[t,a] V[t,b] to the coefficient of A[a]B[b] in output o. Compute that sum over all 58 products for every one of the 15*15*25 = 5,625 coefficient positions. For o = k*3+i, the required coefficient is 1 exactly when a = i*5+j and b = j*5+k for some j; otherwise it is 0. All 75 ones and 5,550 zeros match. Every output is bilinear because the program first forms linear U/V factors, then multiplies one of each, then forms linear combinations of the products. Equality of all coefficients therefore proves equality over Z for every pair of integer input matrices, rather than just a sample.
5. **Separate execution check.** A second interpreter directly runs the saved assignments as scalar integer operations. Run all 375 pairs of an A basis entry and a B basis entry and compare all 15 outputs with the matrix-product definition in the specified transposed storage order. These are all bilinear input basis pairs, not a randomized spot check. This independently confirms the implementation of expansion and the output layout.
6. **Reduced count.** A nonempty L-term signed sum costs L-1 binary additions/subtractions; signed copies and unary negations cost zero. U has 48 fresh additions and 0 final additions. V has 69 and 0. W has 39 fresh and 55 final additions. Thus 48+69+39+55 = 211, excluding exactly the 58 bilinear multiplications. This agrees with the object's declared reduced count and the indexed claimed value. Recounting nonzeros of the fully expanded U/V/W rows gives the object's declared naive count 357. The saved arithmetic improvement is 221-211 = 10; this is not a recount of the missing reference.
7. **Determinism and immutability.** The independent algorithm has fixed iteration orders, exact integers, and no random source. Its three additional fresh processes with distinct hash seeds exit successfully and produce byte-identical full output. A canonical serialization of all expanded maps has a stable SHA256 in the transcript. The object is reread at the end of each run to confirm unchanged bytes. The author's checker also gives byte-identical output on repetition; its extra random trials use a fixed seed.

## Exact independent command and full saved output

Run from this folder:

```sh
python3 skeptic/check_object.py > skeptic/output.txt 2>&1
```

Exit status: 0. The following is inserted directly from `skeptic/output.txt`:

```text
Object: object/3x5x5_m58_cr211_ZT_reduced.json
Object bytes: 16102
SHA256: 9407c156647ed8a24fbd9e29d7f644e1fd6281aabc4eaa317bb5cb3a3a9b5b23 (matches INDEX.csv)
Format: 3x5x5; max dimension <= 8 PASS; products=58; ring=Z
U: inputs=15, fresh=48, finals=58, additions_fresh=48, additions_final=0, additions=48
U: order, signed terms, expanded ternarity and 154 signed prefixes PASS
V: inputs=25, fresh=69, finals=58, additions_fresh=69, additions_final=0, additions=69
V: order, signed terms, expanded ternarity and 196 signed prefixes PASS
W: inputs=58, fresh=26, finals=15, additions_fresh=39, additions_final=55, additions=94
W: order, signed terms, expanded ternarity and 135 signed prefixes PASS
All 58 product factors are nonzero and all 58 products occur in expanded outputs: PASS
Count: 48+69+94=211 reduced additions; metadata and INDEX.csv match
Expanded naive additions: 357; object metadata matches
Saved numeric comparison only: 211 < 221; difference=10 (live reference NOT verified)
Exact tensor identity over Z: PASS; coefficients=5625, ones=75, zeros=5550
Direct SLP execution: PASS; all 375 input basis pairs, all 15 outputs per pair
Expanded maps SHA256: 83aceb532ec78f2d56f06c31cb6d6e9afd3cfd1a8927ec5d31ff04004c0e3922
Object unchanged during verification: PASS
RESULT: PASS (saved-object properties only)

```

Three new checker processes were launched with `PYTHONHASHSEED` set respectively to `0`, `1`, and `8675309`, using argument vector `python3 skeptic/check_object.py`. Their complete outputs are saved in `skeptic/output-seed-0.txt`, `skeptic/output-seed-1.txt`, and `skeptic/output-seed-8675309.txt`. Captured comparison output from `skeptic/determinism.txt`:

```text
PYTHONHASHSEED=0: exit=0, output byte-identical to skeptic/output.txt=True
PYTHONHASHSEED=1: exit=0, output byte-identical to skeptic/output.txt=True
PYTHONHASHSEED=8675309: exit=0, output byte-identical to skeptic/output.txt=True
Determinism: PASS (three new processes; no randomness in independent checker)

```

## Author comparison, performed afterward

After the independent run succeeded, I read `REPRODUCE.md` and all three files in `verify-it-yourself/`. I ran the author's standalone checker directly:

```sh
python3 verify-it-yourself/check_slp.py object/3x5x5_m58_cr211_ZT_reduced.json > skeptic/author-output.txt 2>&1
```

Exit status: 0. Full output inserted directly from `skeptic/author-output.txt`:

```text
{"file": "3x5x5_m58_cr211_ZT_reduced.json", "format": "3x5x5", "rank": 58, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 48, "adds_V": 69, "adds_W": 94, "adds_total": 211, "naive_total": 357, "declared_reduced": 211, "VALID": true}

```

A repeat with the same argument vector is saved in `skeptic/author-repeat.txt`. Comparison output inserted directly from `skeptic/comparison.txt`:

```text
Author checker: exit=0; all reported properties agree with independent results.
Author repeat: exit=0; output byte-identical=True.
Author coverage gap: check_slp.py checks +/-1 terms but never tests expanded fresh/final coefficients for ternarity; independent checker verifies these exhaustively.
Disagreements on saved object: none.

```

The author checker correctly reports exactness, transposed layout, 58 products, 211 reduced additions, and 357 naive additions for this object. Its advertised expanded-ternarity coverage is missing: `expand` returns fresh and final vectors, but `check` never tests their coefficients for membership in {-1, 0, 1}. Its `VALID` field also does not itself enforce the declared reduced count. Neither gap causes a disagreement for the saved object because the independent checker explicitly verifies both properties and all binary prefixes. I did not rely on the author's 20 random trials, run its shell wrapper, or run the optional Sympy checker; exact exhaustive coefficient equality is already established independently.

## Mismatches and verdict

No saved-object mismatch, missing required saved object, or nondeterminism was found. The author's coverage gaps are documented above; the independent checks establish the omitted properties for this object. Pass applies only to the saved-object scope stated above, without any judgment about current table values or novelty.

pass: true
