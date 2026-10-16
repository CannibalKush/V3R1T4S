# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved straight-line program passes the offline object checks. Its exact integer tensor is matrix multiplication, all expanded map intermediates are ternary, and its reduced addition count is 156.

## Scope and independence

I read `CLAIM.md`, the object data, `table-record/README.md`, and `INDEX.csv`, then wrote `skeptic/check.py` from the stated definition. I ran it and saved its complete output in `skeptic/output.txt` before opening any file in `verify-it-yourself/` or reading `REPRODUCE.md`. I then read and ran the author's code. Only files in this package were read; no network was used. All independent mathematics uses Python's standard library and exact integers.

This verdict covers the saved object, not the currency of the table or novelty. Perminov's third-party reference file is deliberately absent. `table-record/README.md` identifies it as https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x4x5_m47_cr161_cn277_ZT_reduced.json with recorded SHA256 `d1248a3a32dd03bf5d9216edfdaf6b01be95987d7cefee03f5f9f9645271319a`. Without network I cannot recount that reference, verify its hash, or establish that its expanded products match this candidate. Those tasks, live minimum counts, the live best-rank assertion, coefficient-class comparisons, and previous-claim/novelty checks are outside this skeptic's assigned scope. Recorded remote hashes cannot authenticate absent remote bytes. I do not treat the saved table metadata as independent confirmation of those facts.

The numerical inequality 156 < 161 follows from the saved numbers; the reference value 161 itself is not independently established here. “47 products” certifies a 47-term bilinear algorithm, not a proof that no lower rank is possible. There is no claimed exhaustive search to reproduce; the identity verification below is exhaustive over coefficients and is not a random sample.

## Quoted definition and success criterion

The exactness condition in `CLAIM.md` is:

> is verified symbolically to compute the full product A*B exactly over Z

The counting convention in its success criterion is:

> each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP

The complete success criterion follows. For the format template, I changed only the angle brackets to braces. The requested Lille URL template is written as https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only the template brackets are changed.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The saved-object layout and counting definition in `CLAIM.md` is:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

## Properties and proof

| Property | Independent check and result |
|---|---|
| Explicit object, format and size | Strict JSON parsing rejects duplicate keys; exact field and integer types, dimensions `[3,4,5]`, maximum dimension 5, integer arithmetic (`z2` is false), 47 U factors, 47 V factors, and 15 outputs all checked. |
| Straight-line order | Every term must refer to a map input or an already appended fresh variable. U and V finish before the 47 paired products; W depends only on those products and earlier W fresh variables. All forms are nonempty, with valid indices and signed unit coefficients. |
| Ternary condition | Start with unit vectors over the original inputs of each map, then substitute exactly in dependency order. Check every coefficient of all 214 fresh/final forms in U, V, and W lies in {-1,0,1}. Also check all 370 signed prefixes: left-associated evaluation supplies an explicit binary schedule whose intermediate coefficients remain ternary. W expansion here is over the 47 product variables, as required for the linear output map. |
| Products | Exactly 47 paired U/V multiplications; each factor is nonzero and each product occurs in an expanded output. These multiplications are excluded from the addition count. |
| Reduced additions | Independently sum length minus one for every fresh and final form: U has 38, V has 44, W has 74; total 156. The 370 prefixes across 214 forms likewise require 370 minus 214 = 156 binary operations. Signs cost nothing; there are no other scalar multiplications. |
| Metadata and claimed value | Recomputed reduced count agrees with `complexity.reduced`, filename and `INDEX.csv`; expanded naive count is 277 and agrees with `complexity.naive`. Saved arithmetic comparison is a difference of 5 below recorded 161. |
| Exactness over Z | Expand U, V, W as integer vectors and compare every one of 15 times 12 times 20 = 3,600 tensor coefficients, including all 3,540 zeros. All 60 required ones agree. Output index is exactly `q = k*3+i`, without allowing an alternative layout to rescue a mismatch. |
| Separate exhaustive execution | Execute the raw JSON forms on all 12 times 20 = 240 pairs of unit input vectors, using a separate evaluator, and compare all 3,600 output entries against direct matrix multiplication. This exhausts bilinear basis pairs; it is not a sample. |
| Hashes | Hash the actual object bytes with SHA256 and compare with `INDEX.csv`: `e5731a01ecf58de14b5fc4a6e9a0de880b11146aeeeef4df6844dd83bfbb83a8`. Compare the bytes again during verification and after the author runs. They remain unchanged. |
| Determinism | Independent output from the first run and two fresh processes agrees byte-for-byte; the two repeat processes use hash seeds 0 and 1729. The author suite likewise agrees byte-for-byte across two fresh processes with those seeds. All exit statuses are zero. |

For the identity proof, let U[t,x] and V[t,y] be the expanded factors and W[q,t] the expanded output coefficients. The coefficient of A[i,j] B[k,l] in output C[a,b] is the integer sum over t of W[b*3+a,t] U[t,i*4+j] V[t,k*5+l]. The required value is 1 exactly when i=a, j=k, and l=b, and is 0 otherwise. The checker verifies every such coefficient. Each U and V factor is linear with no constant, products pair one U with one V, and W is linear in the products. Therefore there are no other degrees or terms to check, and coefficient equality proves the full product for every integer input, without probabilistic assumptions. Exact dependency expansion also proves that the actual straight-line program evaluates those vectors. The raw basis execution independently checks that substitution and indexing.

## Exact commands and real output

All commands run from this folder. The independent checker was written and run before the author's checker was read:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

Exit status: 0. Complete output, pasted from `skeptic/output.txt`:

```text
object: object/3x4x5_m47_cr156_ZT_reduced.json
sha256: e5731a01ecf58de14b5fc4a6e9a0de880b11146aeeeef4df6844dd83bfbb83a8; matches INDEX.csv
format: 3x4x5; max dimension=5; products=47; exact integer arithmetic
U: inputs=12, fresh=38, final=47, additions=38; order, signed terms, ternary expanded forms and 123 binary prefixes OK
V: inputs=20, fresh=44, final=47, additions=44; order, signed terms, ternary expanded forms and 135 binary prefixes OK
W: inputs=47, fresh=23, final=15, additions=74; order, signed terms, ternary expanded forms and 112 binary prefixes OK
all 47 products have nonzero factors and occur in expanded outputs
expanded forms checked: 214; reduced additions=38+44+74=156; naive additions=277; metadata agrees
saved numerical comparison: 156 < 161; difference=5 (reference value not independently verified)
full tensor identity over Z: 3600/3600 coefficients agree; 60 ones and 3540 zeros
independent raw SLP execution: all 240 basis pairs, 3600 output entries agree
proof: linear U and V, paired products, and linear W make every output bilinear; complete coefficient equality proves A*B for all integer inputs
object bytes unchanged during verification
PASS: all saved-object properties checked
```

Afterward, I ran the process audit:

```sh
python3 skeptic/run_audit.py > skeptic/audit-output.txt 2>&1
```

It invokes `python3 skeptic/check.py` twice, `sh verify-it-yourself/run_checks.sh` twice, and `python3 verify-it-yourself/check_slp.py object/3x4x5_m47_cr156_ZT_reduced.json` once. The exact argument lists, output destinations and hash-seed settings are in `skeptic/run_audit.py`. Complete repeated outputs are preserved in `skeptic/output-repeat.txt`, `skeptic/output-repeat2.txt`, `skeptic/author-output.txt`, `skeptic/author-output-repeat.txt`, and `skeptic/author-checker-output.txt`.

Exit status: 0. Complete audit output, pasted from `skeptic/audit-output.txt`:

```text
independent checker: original plus 2 fresh processes agree byte-for-byte (hash seeds 0 and 1729)
author suite: 2 fresh processes agree byte-for-byte (hash seeds 0 and 1729); both exit 0
author checker agrees: format=3x4x5, products=47, layout=C^T, exact tensor, additions=38+44+74=156, naive=277
candidate SHA256 after all checks: e5731a01ecf58de14b5fc4a6e9a0de880b11146aeeeef4df6844dd83bfbb83a8
PASS: repeatability, author agreement, and object immutability
```

Complete author suite output, pasted from `skeptic/author-output.txt` (the repeat is byte-identical):

```text
sha256 matches INDEX.csv (e5731a01ecf58de14b5fc4a6e9a0de880b11146aeeeef4df6844dd83bfbb83a8)
== check_slp.py on object/3x4x5_m47_cr156_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "3x4x5_m47_cr156_ZT_reduced.json", "format": "3x4x5", "rank": 47, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 38, "adds_V": 44, "adds_W": 74, "adds_total": 156, "naive_total": 277, "declared_reduced": 156, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=156, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

Complete direct author-checker output, pasted from `skeptic/author-checker-output.txt`:

```text
{"file": "3x4x5_m47_cr156_ZT_reduced.json", "format": "3x4x5", "rank": 47, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 38, "adds_V": 44, "adds_W": 74, "adds_total": 156, "naive_total": 277, "declared_reduced": 156, "VALID": true}
```

## Comparison and limitations

No numerical or identity mismatch was found. The author's reported format, 47 products, transposed output storage, exact tensor, reduced counts 38/44/74/156, and naive count 277 agree with the independent derivation. Its negative control flips a saved coefficient in a temporary copy and is rejected, as the suite reports.

One limitation in the author's advertised checker: `check_slp.py` expands intermediates but does not test their expanded coefficients for ternarity. It checks only the signed coefficients written in the forms. `sym_check.py` likewise checks written term signs rather than expanded map intermediates. This omission does not falsify the object: the independent checker explicitly verifies every expanded form and every binary prefix. I did not rely on the author's random evaluations or run its optional Sympy checker; my exact full-tensor check and exhaustive raw basis check establish the identity independently.

All required files for the assigned saved-object checks are present. The deliberately omitted third-party reference and live comparisons remain outside this offline verdict, as instructed. Every assigned saved-object property was confirmed.

pass: true
