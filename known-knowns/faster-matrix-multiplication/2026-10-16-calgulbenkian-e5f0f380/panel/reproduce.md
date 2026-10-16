# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved straight-line program passes every property in this skeptic's offline scope. This is a verification of the saved object, not a judgment of current table values or novelty.

## Scope and independence

I read `CLAIM.md`, inspected the object data and saved metadata, then wrote `skeptic/definition.md` and `skeptic/check.py` before reading anything in `verify-it-yourself/` or `REPRODUCE.md`. I first ran the independent checker to completion and saved `skeptic/output.txt`; only then did I read and run the author's code. No network was used and no other folder's content was inspected. The optional SymPy execution used the interpreter expressly permitted by the task, invoked by its relative path. All created artifacts are in this folder.

The reference scheme is third-party data deliberately absent from the package. Its saved URL is https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x4x8_m51_cr188_cn354_ZT_reduced.json and its recorded SHA-256 is `b68445935df00311217280a30d628395594619584691d8264723045b2b62131a`. Without network, I cannot recount that file, verify its hash or establish product identity with it. These are explicit scope exclusions, together with current best rank, live table minima, coefficient-class comparisons, publication priority, and novelty. The other skeptics handle those comparisons. The saved inequality 181 less than 188 is checked arithmetically; the truth or currency of 188 is not established here. Hashes of absent source pages in `table-record/README.md` cannot be authenticated offline.

## Quoted definition and criterion

Source: `CLAIM.md`. In the quoted criterion below, only the angle brackets around n,m,p were changed to braces to avoid literal placeholder syntax. The Lille URL template, if written out, is https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only its placeholder brackets are changed. The template is explanatory and is not an additional quotation from this claim.


> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

### Object definition and counting convention

> `object/`: the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

The saved-file clauses checked are: explicit ordered linear forms and 51 products; format dimensions at most 8; symbolic exactness over Z; the reduced counting convention, including free signs and exclusion of products; the ternary coefficient restriction; and the claimed saved count. The quoted live-source clauses are outside this offline scope as directed by the task. The enumerated partial wins are alternative claims and are not asserted for this single saved object.

## Checks and proof re-derived

1. **Schema, identity and integrity.** Strict JSON loading rejects duplicate keys. The checker requires the saved format `[2, 4, 8]`, integer rank 51, `z2` exactly false, the complete expected schema, integer metadata, the correct U/V/output dimensions, and nonempty forms. It checks the target, cell, file, claimed values, and SHA-256 against `INDEX.csv`. The object hash is `e5f0f3807baaa5f00a76f606bd33199db83dfd83ef82c21abbcb0fbc79c02d95`. `skeptic/package_hashes.json` records all eight original files; their hashes are rechecked after execution. Those additional hashes show unchanged bytes, not external provenance.
2. **Straight-line order and scalar restriction.** Start each map with integer unit vectors representing its inputs. For fresh form k, permit only input indices and earlier fresh indices; append its vector only after expansion. Final forms can use inputs and fresh variables. Every term must have an integer index and integer sign exactly +1 or -1. No other scalar operations are present. U and V are evaluated first, then their 51 pairwise products, then W. Every product has nonzero U and V factors and a nonzero expanded output factor.
3. **Ternary condition.** For each form, start from the zero vector and add the signed source vectors in stored order. Check every coordinate after every term, including all implicit binary accumulation prefixes, belongs to {-1, 0, 1}. This checks all 243 fresh/final forms and 424 prefixes over the original inputs of each map. It also proves a binary lowering of each multi-term form stays ternary. No modular reduction or floating arithmetic is used.
4. **Full tensor identity.** The expanded U rows have 8 coordinates, V rows 32, and W rows 51. For every output c=k*2+i, every A input a, and every B input b, compute the exact integer coefficient `sum(W[c][q]*U[q][a]*V[q][b] for q in range(51))`. Its required value is 1 exactly when `a//4 == i`, `b%8 == k`, and `a%4 == b//8`; otherwise it is 0. This is the coefficient of A[i,j]*B[j,k] in C[i,k]. All 16*8*32=4096 coefficients are checked, including every zero: 64 ones and 4032 zeros. Equality of all coefficients of these bilinear polynomials proves exact equality over Z for all input matrices. This exhausts the identity, not a sample. No exhaustive optimization search is claimed.
5. **Reduced count.** A nonempty form of L signed already-computed quantities uses L-1 binary additions/subtractions, with signs free. U has 125 terms across 88 forms, costing 37; V has 185 terms across 118 forms, costing 67; W has 114 terms across 37 forms, costing 77. Thus `(125-88)+(185-118)+(114-37)=181`. The 51 bilinear products are excluded. Expanded-map nonzero counts independently give the declared naive count 354. Both complexity metadata fields agree. The saved improvement is 188-181=7.
6. **Direct execution and determinism.** As a supplementary check, directly execute the stored SLP on 303 fixed-seed integer cases, including zeros, ones, alternating signs, and signed inputs up to 30 digits, and compare with ordinary matrix multiplication. These samples are not the proof of exactness. Independent checker runs with two different Python hash seeds match the first output byte for byte; the author's checker likewise has identical outputs under those seeds. The program has only fixed ordered integer operations and no randomness or branches; the verification fixtures are seeded. No object bytes changed during execution.

## Exact independent command and full output

Run from this folder (exit status 0):

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

The following is pasted directly from `skeptic/output.txt`:

```text
Independent saved-object verification
object: object/2x4x8_m51_cr181_ZT_reduced.json
sha256: e5f0f3807baaa5f00a76f606bd33199db83dfd83ef82c21abbcb0fbc79c02d95
INDEX: path, target, cell, claimed counts and object hash PASS
format=2x4x8; product slots=51; max dimension <= 8; integer ring PASS
U: inputs=8, fresh=37, final=51, additions=37, ternary prefixes=125; order/terms/expanded forms PASS
V: inputs=32, fresh=67, final=51, additions=67, ternary prefixes=185; order/terms/expanded forms PASS
W: inputs=51, fresh=21, final=16, additions=77, ternary prefixes=114; order/terms/expanded forms PASS
TENSOR: all 4096 integer coefficients checked; 64 unit coefficients, 4032 zero coefficients; full A*B identity PASS
COUNTS: reduced=37+67+77=181; expanded naive=354; 181 < saved threshold 188 by 7 PASS
Counting derivation: a nonempty L-term form needs L-1 binary additions; signed copies are free; 51 products excluded.
DIRECT EXECUTION: 303 reproducible integer cases, including 30-digit inputs, PASS (supplementary)
Object bytes unchanged during verification PASS
Scope: reference scheme absent; no recount, product-identity comparison, live-table/rank verification, or novelty judgment.
RESULT: PASS (saved-object properties)
```

## Author comparison, performed afterward

Exact command (exit status 0):

```sh
TMPDIR=skeptic/tmp sh verify-it-yourself/run_checks.sh > skeptic/author_output.txt 2>&1
```

`skeptic/tmp/` was created beforehand to keep temporary files in this folder. Full captured output, including the environment's incidental Xcode diagnostics:

```text
sha256 matches INDEX.csv (e5f0f3807baaa5f00a76f606bd33199db83dfd83ef82c21abbcb0fbc79c02d95)
== check_slp.py on object/2x4x8_m51_cr181_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
2026-10-15 16:29:18.383 xcodebuild[10249:76354362]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 16:29:18.571 xcodebuild[10249:76354353] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
{"file": "2x4x8_m51_cr181_ZT_reduced.json", "format": "2x4x8", "rank": 51, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 37, "adds_V": 67, "adds_W": 77, "adds_total": 181, "naive_total": 354, "declared_reduced": 181, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=181, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

The default `python3` lacks SymPy, so the optional symbolic checker was rerun with the task's designated interpreter. Exact successful command (exit status 0):

```sh
../../../.venv/bin/python verify-it-yourself/sym_check.py object/2x4x8_m51_cr181_ZT_reduced.json > skeptic/author_symbolic_output.txt 2>&1
```

Full successful output:

```text
{"file": "2x4x8_m51_cr181_ZT_reduced.json", "format": "2x4x8", "rank": 51, "products": 51, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 181}
```

Exact repeatability and comparison commands (all exit status 0; redirected commands produce no terminal output):

```sh
PYTHONHASHSEED=0 python3 skeptic/check.py > skeptic/repeat_seed0.txt 2>&1
PYTHONHASHSEED=123456 python3 skeptic/check.py > skeptic/repeat_seed123456.txt 2>&1
PYTHONHASHSEED=0 python3 verify-it-yourself/check_slp.py object/2x4x8_m51_cr181_ZT_reduced.json > skeptic/author_repeat_seed0.txt 2>&1
PYTHONHASHSEED=123456 python3 verify-it-yourself/check_slp.py object/2x4x8_m51_cr181_ZT_reduced.json > skeptic/author_repeat_seed123456.txt 2>&1
python3 skeptic/compare.py > skeptic/comparison_output.txt 2>&1
```

The two independent rerun files contain exactly the independent output pasted above. The two author rerun files each contain this full output:

```text
{"file": "2x4x8_m51_cr181_ZT_reduced.json", "format": "2x4x8", "rank": 51, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 37, "adds_V": 67, "adds_W": 77, "adds_total": 181, "naive_total": 354, "declared_reduced": 181, "VALID": true}
```

Full comparison output:

```text
Independent checker: original and both hash-seed reruns are byte-identical PASS
Author checker: both hash-seed reruns are byte-identical PASS
Independent/author agreement: format 2x4x8, 51 products, C^T output layout, exact tensor, counts 37/67/77/181, naive 354 PASS
Author SymPy execution: symbolic C^T identity and 181 additions agree PASS
All 8 original package files unchanged by verification PASS
All 51 product slots have nonzero expanded output factors PASS
No mismatch or observed nondeterminism in the saved object.
```

## Mismatches and limitations

No mismatch was found in the object, its declared properties, or the two checkers' results. `C^T` is the explicitly specified output storage order; the author's `C=AB: false` means row-major storage does not match, not a failed multiplication identity.

The author's standalone checker validates literal term signs but never tests that expanded intermediate coefficients stay ternary, despite that promise in `REPRODUCE.md`. Its SymPy checker also only checks literal term signs. This is a coverage gap in those checkers, which the independent checker closes: the saved object satisfies the stronger expanded ternary requirement, including binary prefixes. The author's negative control is rejected as expected. The initial missing SymPy dependency was resolved using the supplied interpreter; it is not a mathematical disagreement. The Xcode diagnostics did not affect the successful checker verdict or subsequent byte-identical direct checker runs.

The passing verdict applies to the saved object's exactness, ternary condition, straight-line order, 51 active product slots, counts, hash consistency, and observed determinism. It does not certify the excluded external comparisons.

Checker SHA-256, `skeptic/check.py`: `3a2f8432b7f333d25c8ee5d60f0f4189fce1879d18f7d3afc878ed5f859f70e8`.

Checker SHA-256, `skeptic/compare.py`: `dcae6a3b48b2acff6ee25813a7045e317c78f4da0b33a8ef5bf002a8e52426a9`.

pass: true
