# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved straight-line program passes every object property checked in this offline reproduction. The independent checker was written and run before reading any file in verify-it-yourself/ or REPRODUCE.md. No external data or author's checker was used in its derivation. Only files within this package were read or written.

## Definition checked

The complete success criterion from CLAIM.md is quoted below. Only the brackets around the format variables have been changed to braces to avoid the package checker's placeholder rejection; its words and mathematical conditions are unchanged. The Lille URL template is written as https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only its template brackets are changed. That URL template is notation supplied for this report, not an additional sentence attributed to CLAIM.md.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The object's explicit definition and counting rule from CLAIM.md:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

In particular, the exactness definition is “is verified symbolically to compute the full product A*B exactly over Z”. The counting convention is “each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP”. Both are quoted within the criterion above and in the independent checker's source.

## Scope

This audit confirms the saved object's exactness, ternary condition, straight-line order, 230 products, dimensions, addition counts, object hash, and determinism. It checks the saved numerical comparison 929 versus 974 only as arithmetic and consistent metadata.

Perminov's reference scheme is deliberately absent. table-record/README.md names its URL and recorded sha256, but without network its bytes cannot be obtained, its hash cannot be verified, and its 974 additions cannot be recounted. The claim that its expanded product factors equal this object's is likewise unverified here. Hashes of other external fetches are metadata without the source bytes and cannot be checked offline.

This report makes no judgment about the current live tables, record status, novelty, the minimum cr across the live repository, coefficient classes of competing schemes, or whether 230 is the current best rank. Those comparisons and the identity with Perminov's file belong to the other skeptics. The verified 230 is the number of products in this decomposition; this audit does not prove a minimal tensor rank or a globally optimal addition count. No exhaustive search is claimed or used to establish the result; every coefficient of this particular object's identity is checked exhaustively.

## Independent proof and checks

skeptic/check_slp.py uses python3 and the standard library, exact unbounded integers, and no imports from verify-it-yourself/. It rejects duplicate JSON keys, missing or unexpected schema keys, invalid dimensions and product count, characteristic-two mode, empty forms, noninteger terms, forbidden scalar coefficients, and out-of-order references.

For U, V, and W separately, assign an integer basis vector to each input. For fresh variable k, substitute the already expanded vectors for each signed term and add their coefficients exactly. An index must be less than the number of inputs plus k. Final forms may use inputs or completed fresh variables, never other final forms. This inductive recurrence uniquely expands every assignment over Z and proves the straight-line order. U has 40 input variables and V has 64; W has 230 formal product variables. All 1,168 named fresh and final forms have only coefficients -1, 0, 1 after cancellation. The checker also expands every partial sum in the listed binary evaluation order: none introduces a nonternary coefficient. Thus the lowering to the counted binary operations also respects the ternary condition, including its unnamed intermediates.

Write U[q,a] and V[q,b] for the expanded product factors, and W[o,q] for each expanded output coefficient. Multiplying the factors and substituting into W gives the coefficient

    T[o,a,b] = sum over q of W[o,q] * U[q,a] * V[q,b].

Output o corresponds to C[i,k] with i = o mod 5 and k = floor(o/5). Input a corresponds to A[floor(a/8), a mod 8]; input b to B[floor(b/8), b mod 8]. The required coefficient is exactly 1 if floor(a/8) = i, b mod 8 = k, and a mod 8 = floor(b/8), and exactly 0 otherwise. This follows directly by expanding C[i,k] = sum over j of A[i,j]B[j,k]. The checker independently constructs T and compares every one of 40 * 40 * 64 = 102,400 coefficients to this condition. All 320 required unit coefficients and all 102,080 required zero coefficients match. Since the bilinear monomials are a basis over Z, this proves every output polynomial equals the full matrix product exactly over Z, not merely at sampled matrices.

A nonempty form of length L requires L-1 binary additions/subtractions. Signs cost no extra operations, and the 230 bilinear multiplications are excluded by the quoted convention. Summing the lengths of the saved forms gives:

| Map | Fresh forms | Final forms | Fresh additions | Final additions | Total |
|---|---:|---:|---:|---:|---:|
| U | 205 | 230 | 205 | 0 | 205 |
| V | 327 | 230 | 327 | 0 | 327 |
| W | 136 | 40 | 251 | 146 | 397 |
| Total | 668 | 500 | 783 | 146 | 929 |

All 230 U and V factors are nonzero. The naive expanded count is nz(U) + nz(V) + nz(W) - 2*230 - 40 = 2747. Both computed counts match object metadata, and the reduced count matches CLAIM.md and INDEX.csv. The saved comparison is 929 less than 974 by 45 additions; this does not establish the external reference count's validity.

The SHA256 of the original object bytes is compared directly to INDEX.csv, and the file, target and cell fields also match. A second fresh interpreter execution produces byte-identical full output. Direct execution on 20 seeded integer matrix pairs agrees with both matrix multiplication and the expanded maps; these examples are ancillary and are not the symbolic proof.

Seven isolated negative controls exercise the checker's rejection paths. The control object's INDEX hash is updated when needed so a hash failure does not mask a tensor, ordering, ternary, scalar, or count failure. The original object and INDEX.csv are not edited. Per-control full output is saved in skeptic/negative-controls/.

## Exact commands and real output

Run from this folder:

```sh
python3 skeptic/check_slp.py object/5x8x8_m230_cr929_ZT_reduced.json > skeptic/output.txt 2>&1
python3 skeptic/check_slp.py object/5x8x8_m230_cr929_ZT_reduced.json > skeptic/output-repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output-repeat.txt
```

Both checker executions exited 0. cmp exited 0 with empty output. The complete contents of skeptic/output.txt are pasted directly below:

```text
object: object/5x8x8_m230_cr929_ZT_reduced.json
sha256: 0fb366e6a2a5cc6bc6fd0b31334b1d859df86c180c0fc30759cbbd41c4867501 (matches INDEX.csv)
format: 5x8x8; products: 230; max dimension <= 8; integer arithmetic
U: inputs=40, fresh=205, final=230, additions_fresh=205, additions_final=0, total=205
U: every reference precedes its use; every term is +/-1; all 435 expanded forms are ternary
U: nonternary partial sums in listed binary evaluation order=0
V: inputs=64, fresh=327, final=230, additions_fresh=327, additions_final=0, total=327
V: every reference precedes its use; every term is +/-1; all 557 expanded forms are ternary
V: nonternary partial sums in listed binary evaluation order=0
W: inputs=230, fresh=136, final=40, additions_fresh=251, additions_final=146, total=397
W: every reference precedes its use; every term is +/-1; all 176 expanded forms are ternary
W: nonternary partial sums in listed binary evaluation order=0
tensor: checked all 102400 integer coefficients; expected ones=320; mismatches=0
expanded ternary forms checked: 1168
reduced additions: 205+327+397=929; matches claim, object metadata, and INDEX.csv
naive additions: 2747; matches object metadata
saved comparison arithmetic: 929 < 974; improvement=45 (external reference not recounted)
direct integer execution: 20 deterministic seeded examples, all outputs match matrix multiplication and expanded maps
PASS: saved object exactness, ternary forms, straight-line order, product count, counts, and object hash
```

Only after the independent checker had been written, executed and its output saved were verify-it-yourself/ and REPRODUCE.md read. The author's primary checker was then run:

```sh
python3 verify-it-yourself/check_slp.py object/5x8x8_m230_cr929_ZT_reduced.json > skeptic/author-output.txt 2>&1
python3 verify-it-yourself/check_slp.py object/5x8x8_m230_cr929_ZT_reduced.json > skeptic/author-output-repeat.txt 2>&1
cmp skeptic/author-output.txt skeptic/author-output-repeat.txt
```

Both executions and cmp exited 0; cmp output was empty. The complete contents of skeptic/author-output.txt are pasted directly below:

```text
{"file": "5x8x8_m230_cr929_ZT_reduced.json", "format": "5x8x8", "rank": 230, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 205, "adds_V": 327, "adds_W": 397, "adds_total": 929, "naive_total": 2747, "declared_reduced": 929, "VALID": true}
```

The author's checker agrees on the tensor identity in the specified transposed output layout, direct evaluation, 230 products, U/V/W counts, reduced count 929 and naive count 2747. There is no result disagreement. A coverage gap was found: despite the package's description, check_slp.py checks individual term coefficients but does not test the coefficients of every expanded intermediate. Its VALID field also does not independently enforce count metadata equality. The independent checker explicitly enforces both conditions and they pass for the saved object. The author's sympy script and shell wrapper were inspected but not executed; the comparison above is with its primary checker.

The negative controls were run with:

```sh
python3 skeptic/run_negative_controls.py > skeptic/negative-controls-output.txt 2>&1
```

The control runner exited 0. The complete captured summary is pasted below; each control's full checker output is also saved in its own output.txt:

```text
tensor-sign: exit=1; FAIL: ValueError: tensor mismatch: [(38, 26, 3, 2, 0), (38, 26, 4, -2, 0), (38, 26, 6, 2, 0), (38, 26, 7, -2, 0), (38, 26, 19, 2, 0), (38, 26, 20, -2, 0), (38, 26, 22, 2, 0), (38, 26, 23, -1, 1), (38, 26, 35, -2, 0), (38, 26, 39, 2, 0)]
forward-reference: exit=1; FAIL: ValueError: u_fresh[0]: forward/out-of-range reference
expanded-nonternary: exit=1; FAIL: ValueError: u_fresh[0]: nonternary expanded form
forbidden-scalar: exit=1; FAIL: ValueError: v_final[0]: forbidden scalar
count-metadata: exit=1; FAIL: ValueError: complexity metadata mismatch
hash-mismatch: exit=1; FAIL: ValueError: object SHA256 mismatch
missing-object: exit=1; FAIL: FileNotFoundError: [Errno 2] No such file or directory: 'object/5x8x8_m230_cr929_ZT_reduced.json'
PASS: all 7 independent-checker negative controls rejected; control hashes updated except the intentional hash mismatch
```

## Artifacts and mismatch assessment

- Independent source and quoted definition: skeptic/check_slp.py and skeptic/definition.txt.
- Independent output and deterministic repeat: skeptic/output.txt and skeptic/output-repeat.txt.
- Author comparison output and repeat: skeptic/author-output.txt and skeptic/author-output-repeat.txt.
- Negative control runner and output: skeptic/run_negative_controls.py and skeptic/negative-controls-output.txt.
- SHA256 of independent checker source: 463ffdf5dfcd728078607c58c139976bececd5d597c8619e3dc8c3cfce0ee5be.
- SHA256 of independent output: dd68c128b2518eaf0d30296ffbd709467bbbbf0ab92ce72749d5a1e8beea71dd.

No mismatch, missing required saved object, or nondeterminism was found within this audit's scope. The deliberately unshipped reference and external comparison evidence remain out of scope as instructed, and do not establish the broader record claim here.

pass: true
