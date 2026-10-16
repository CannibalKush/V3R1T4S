# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved straight-line program passes the independent offline checks. It computes 4x5x5 matrix multiplication exactly over Z with 76 nonzero, used products and 281 reduced additions/subtractions.

## Scope and independence

I read `CLAIM.md`, `INDEX.csv`, `table-record/README.md`, and the object layout/data before writing `skeptic/check.py`. I wrote and ran that checker, saved `skeptic/output.txt`, and repeated its execution before opening `verify-it-yourself/` or `REPRODUCE.md`. The checker uses Python's standard library and exact integers, with no imported author code and no network access.

The verdict concerns the saved object: exactness, ternary condition, straight-line order, dimension and product counts, reduced and naive counts, its recorded hash, and deterministic evaluation. The arithmetic comparison 281 less than the recorded 299 is checked; it does not validate that reference count. This is not a judgment about current tables, novelty, best-known rank, coefficient-class comparisons, or an exhaustive optimization search.

The third-party reference scheme is deliberately absent. `table-record/README.md` records its URL and sha256, but supplies no reference bytes. Without network I cannot recount it, validate its hash, or establish equality of its expanded U/V/W rows with this object's. Those reference-product and live-table checks belong to the other skeptics, as specified in the task. The source hashes in `table-record/README.md` likewise cannot be verified from metadata alone. No object needed for the scoped saved-object checks is missing.

## Quoted definition and criterion

The following quotes are from `CLAIM.md`. In the criterion's format placeholder I changed only the angle brackets to braces. The Lille URL template is written as `https://fmm.univ-lille.fr/{n}x{m}x{p}.html`, changing only the brackets of its parameter notation.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The exactness condition is:

> is verified symbolically to compute the full product A*B exactly over Z

The success criterion's counting convention is:

> each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP

The saved-file definition of the maps and count is:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

## Independent checks and derivation

1. **Schema, format, rank and hashes.** Reject duplicate JSON keys, unexpected schema, noninteger dimensions/counts, incorrect row counts, and arithmetic modulo two. Confirm dimensions [4,5,5], maximum dimension at most 8, and 76 products; each factor is nonzero and every product appears in the expanded output map. Compute SHA-256 directly from the object bytes and compare with the single `INDEX.csv` row. Confirm the row's path, target, cell and value; confirm both declared complexity values. The object bytes remain unchanged after verification and after the author's harness.
2. **Straight-line order and permitted scalars.** In each map, initialize a pool of coordinate unit vectors. For each fresh form, permit only indices into inputs or earlier fresh forms; append its expansion only after checking it. Final forms may use inputs or fresh variables, not one another. Reject empty forms, malformed terms, booleans masquerading as integer indices/scalars, out-of-range indices, and coefficients other than +1 or -1.
3. **Ternary expansions.** Expand each term using signed integer dictionary addition. Reject every nonzero coefficient outside {-1,+1}. Check every declared fresh and final form, and additionally every left-to-right partial sum, thereby exhibiting a binary lowering with ternary intermediates. This covers 362 declared forms and 643 prefixes, including all 190 fresh variables. Zero coefficients are omitted from sparse vectors and are allowed.
4. **Full symbolic identity.** Write U[q,a] and V[q,b] for expanded input factors and W[o,q] for expanded output coefficients. Distributivity gives the coefficient of A[a]B[b] in output o as sum over q of W[o,q]U[q,a]V[q,b]. Independently accumulate that integer sum. For o=k*4+i, a=ar*5+aj and b=bj*5+bc, the required coefficient is 1 exactly when ar=i, bc=k and aj=bj, and 0 otherwise. Compare all 20*20*25=10,000 coefficients, including the zeros. Exactly 4*5*5=100 target coefficients are 1. Equality of all coefficients proves equality over Z for arbitrary inputs; no numerical sampling is used as a substitute for proof.
5. **Direct evaluation.** Separately interpret the original forms on every one of the 20*25=500 pairs of coordinate inputs and compare all 20 outputs with a direct matrix product. This is exhaustive over bilinear basis pairs. Also run 12 fixed dense signed-integer cases twice. These execution checks supplement the full symbolic proof.
6. **Addition count.** Lower each L-term form into L-1 binary additions/subtractions using free signs. Sum all fresh and final forms, excluding the 76 bilinear multiplications. U costs 75+0=75; V costs 84+0=84; W costs 60+62=122; total 281. For expanded final maps, the naive count is nz(U)+nz(V)+nz(W)-2*76-20=530. Both agree with object metadata; 281 agrees with `INDEX.csv` and is 18 below its recorded 299.
7. **Determinism.** Re-run the whole independent checker in separate processes, including PYTHONHASHSEED=1 and 73, requiring successful exits and byte-for-byte equality with the original output. Recheck the object hash. No non-determinism was observed.

## Exact commands and real output

All commands are run from this folder. The primary command completed with exit status 0:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

The following is pasted directly from `skeptic/output.txt`:

```text
object: object/4x5x5_m76_cr281_ZT_reduced.json
sha256: 08d7b199e9ecc9f7254dc46c23ecf2128e83444277b19eac6bbcb678a107f819 (matches INDEX.csv)
format: 4x5x5; max dimension <= 8; products=76; arithmetic=Z
U: inputs=20, fresh=75, final=76, additions=75+0=75, ternary_forms=151, ternary_prefixes=226, order=OK
V: inputs=25, fresh=84, final=76, additions=84+0=84, ternary_forms=160, ternary_prefixes=244, order=OK
W: inputs=76, fresh=31, final=20, additions=60+62=122, ternary_forms=51, ternary_prefixes=173, order=OK
exact tensor identity: 10000 integer coefficients checked, 100 target nonzeros, mismatches=0
direct SLP evaluation: all 500 input basis pairs, all 20 outputs each, mismatches=0
direct SLP evaluation: 12 fixed dense integer cases, repeated identically, mismatches=0
reduced additions: 75+84+122=281; metadata and INDEX.csv agree
expanded naive additions: 530; metadata agrees
saved numeric comparison: 281 < 299; improvement=18 (live reference not verified)
object bytes unchanged during verification
PASS: all saved-object checks
```

The separate repeat command completed with exit status 0 and produced identical bytes:

```sh
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output-repeat.txt
```

`cmp` produced no output and exited 0. The saved deterministic-run driver was then executed with exit status 0:

```sh
python3 skeptic/check_determinism.py > skeptic/determinism.txt 2>&1
```

Pasted from `skeptic/determinism.txt`:

```text
PYTHONHASHSEED=1: exit=0; output byte-identical to skeptic/output.txt
PYTHONHASHSEED=73: exit=0; output byte-identical to skeptic/output.txt
separate default-environment repeat: output byte-identical to skeptic/output.txt
object sha256 after independent and author runs: 08d7b199e9ecc9f7254dc46c23ecf2128e83444277b19eac6bbcb678a107f819
PASS: deterministic repeated execution and unchanged object
```

## Author comparison

Only after the independent check and its first repeat, I read the author's two Python checkers and harness. I ran this command, which completed with exit status 0:

```sh
sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
```

Pasted directly from `skeptic/author-output.txt`:

```text
sha256 matches INDEX.csv (08d7b199e9ecc9f7254dc46c23ecf2128e83444277b19eac6bbcb678a107f819)
== check_slp.py on object/4x5x5_m76_cr281_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x5x5_m76_cr281_ZT_reduced.json", "format": "4x5x5", "rank": 76, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 75, "adds_V": 84, "adds_W": 122, "adds_total": 281, "naive_total": 530, "declared_reduced": 281, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=281, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

The author's exact tensor identity, transposed output layout, U/V/W counts, total, naive count, and object hash agree with the independent results. The harness's coefficient-flip negative control is rejected. I did not run the optional SymPy checker; the complete exact-integer tensor proof already establishes symbolic equality.

There is one limitation in the author's checker implementation: `check_slp.py` checks literal term coefficients but does not inspect expanded-vector coefficients for ternarity; its returned expanded fresh vectors are discarded. `sym_check.py` also checks literal signs rather than expanded intermediates. Thus the author's documentation overstates that particular check. This produces no disagreement about the saved object: the independent checker explicitly confirms all expanded forms and prefixes are ternary. No saved-object mismatch was found.

pass: true
