context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

REPRODUCE skeptic result: the saved object is an exact rational bilinear scheme for 13x13x14 with 1,479 nonzero rank-one terms. All 5,597,956 tensor coefficients agree exactly. This is a certificate of a rank upper bound of 1,479, not a lower-bound proof of minimal rank.

I read CLAIM.md, the object, INDEX.csv and table-record/README.md first. I wrote skeptic/check_scheme.py independently, including its quoted definition, and completed its first successful run into skeptic/output.txt before opening REPRODUCE.md or anything in verify-it-yourself/. The primary checker was not changed after reading the author's checker. No network was used and no external source documents or parent construction files were read. The Python interpreter supplied in the task and its installed arithmetic library were used to execute the checker.

Definition and criterion checked, quoted from CLAIM.md:

> object/13x13x14_r1479_Q.json is an exact bilinear scheme over Q for the matrix multiplication format &lt;13,13,14&gt; with 1479 rank-one terms, strictly fewer than 1511, the lowest rank listed for the sorted format 13x13x14 in the four live record tables and the V3R1T4S trophy case.

> For a matrix-multiplication format &lt;n,m,p&gt; with max(n,m,p) &lt;= 16, OTHER THAN &lt;3,3,3&gt; and &lt;4,4,4&gt; (those two are the separate moonshot target fmm-4x4x4-rank47-3x3x3-rank22), find a bilinear (non-commutative) scheme with strictly fewer multiplications (tensor rank) than the best known value over ANY ring.

> Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format &lt;n,m,p&gt; with max(n,m,p) &lt;= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

> Parse the candidate scheme (JSON U, V, W integer/rational matrices, or a Maple-style product list as in the Lille *_raw.mpl files). With exact fractions/sympy, form the r products m_k = (sum_ij U_k,ij A_ij)*(sum_jl V_k,jl B_jl) and check that for every (i,l) sum_k W_k,il m_k equals the symbolic entry (A*B)_il with exact coefficients over the claimed ring (reduce mod p for GF(p)); equivalently check the Brent equations. Count r after dropping zero terms. Re-fetch fmm_sota.json, the Lille per-format page, Perminov's README (all three ZT/Z/Q columns) and MerlijnW70's repo, and compare against the sorted format (rank is invariant under axis permutation/transposition). For p2 also re-fetch COVERAGE.md and the GF(2) schemes. Whole check runs in minutes on a 10-core Mac even for 16x16x16.

In the quoted Lille URL template I changed only the brackets, writing https://fmm.univ-lille.fr/{n}x{m}x{p}.html. Other angle-bracket characters in quotations are HTML-escaped to preserve their rendered text without literal template markers.

Properties checked and proof re-derived:

1. Explicit object and encoding: strict JSON parsing rejects duplicate keys; all 336 vocabulary values are integers or exact rational strings; every RLE token, vocabulary index, repetition count and decoded width is checked. There are exactly 1,479 rows in each factor, with widths 169, 182 and 182. All coefficients are in Q; floating-point values are rejected.
2. Format eligibility: dimensions are exactly (13,13,14), positive, at most 16, already sorted and outside both excluded formats. The p1 and p2 partial-win branches do not apply: this object is within the main size limit and is verified over Q.
3. Term count and claimed value: each of the three factors of every term has a nonzero coefficient. No term is discarded; the effective term count is exactly 1,479. The three-factor outer product of nonzero vectors over Q is nonzero, so these are nonzero rank-one terms.
4. Full matrix-multiplication identity: independently interpret u[i*m+j] as the coefficient of A[i,j], v[s*p+t] as that of B[s,t], and w[l*n+h] as the weight for output (h,l). Expansion gives the coefficient sum over k of u[k,i*m+j] v[k,s*p+t] w[k,l*n+h]. The definition requires this to equal 1 exactly when i=h, j=s and t=l, and 0 otherwise. These are independent formal noncommuting input products A[i,j]B[s,t], in that order, so equality of every coefficient proves the bilinear identity; no commutativity between A and B is assumed. This convention was encoded before reading the author's code and subsequently agreed with its documented convention.
5. Exact denominator clearing: the vocabulary denominator LCM is D=5440, and each scaled coefficient is checked to represent its original fraction exactly. Multiplying each of the three factors by D multiplies the tensor by D^3=160989184000. Since D is nonzero in Q, scaled integer equality is equivalent to the original rational identity. For each of the 169 u coordinates, an arbitrary-precision FLINT integer matrix product computes the complete 182 by 182 coefficient slice. Every entry is compared with the independently constructed target. This exhausts 169*182*182=5,597,956 coefficients: 2,366 expected ones and 5,595,590 expected zeros. There is no sampling, floating point, modular reduction or assumed machine-integer overflow bound.
6. Saved-file consistency: the object SHA-256 equals INDEX.csv; target, filename, format, claimed value and recorded threshold agree. The saved metadata says 1511 for the digest and Lille page, and 1511 in each current ZT/Z/Q cell in the quoted Perminov row; 1524 is the parenthetical previous rank. Thus 1479 is below each recorded numeric value by 32. The metadata says no matching Merlijn scheme and no matching trophy-case row; this absence cannot be independently established from source bodies because only metadata is saved. I make no judgment on table currentness, completeness, live fetches, novelty, or whether a construction was previously listed. Those are assigned to the other skeptic. These limitations are not a claim to have satisfied the external-table clauses of the full target criterion.
7. Determinism: repeated full independent runs produced byte-identical output, checked with cmp and exit status 0. Repeated author-wrapper runs with the supplied interpreter also produced byte-identical output and exit status 0. Neither checker uses random choices. This package supplies an explicit certificate, not an exhaustive search; its full certificate has been checked.

The primary checker commands actually executed (the interpreter is the task-supplied environment, written relative to this folder):

```sh
../../../.venv/bin/python -u skeptic/check_scheme.py > skeptic/output.txt 2>&1
../../../.venv/bin/python -u skeptic/check_scheme.py > skeptic/output_repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output_repeat.txt
```

Both checker executions and cmp exited 0. The first successful run preceded inspection of the author's code; the canonical relative command was also rerun afterward with unchanged code and identical output. Full actual output, inserted directly from skeptic/output.txt:

```text
Independent exhaustive exact matrix-multiplication tensor check
Object: object/13x13x14_r1479_Q.json
SHA256: e738d0f367b67ba740109db2687b58811da516ee74f67c42ccb934eab382548d
Format: 13x13x14; ring: Q; vocabulary: 336 exact rationals
Decoded row widths: u=169, v=182, w=182
Convention: u[i*m+j], v[j*p+l], w[l*n+i] (dual/transposed output)
Common denominator D: 5440
Nonzero coefficients: u=33474, v=38722, w=65761
Stored terms: 1479; zero terms: 0; effective rank upper bound: 1479
INDEX.csv: object path, SHA256, target, dimensions, value and saved threshold match
Saved numeric comparison: 1479 < 1511; margin 32
Source table bodies are absent; no live-table/currentness/novelty judgment is made
Exact target coefficient for each matrix-product monomial: D^3 = 160989184000
Checked u coordinates 13/169: 430612 coefficients, 0 mismatches
Checked u coordinates 26/169: 861224 coefficients, 0 mismatches
Checked u coordinates 39/169: 1291836 coefficients, 0 mismatches
Checked u coordinates 52/169: 1722448 coefficients, 0 mismatches
Checked u coordinates 65/169: 2153060 coefficients, 0 mismatches
Checked u coordinates 78/169: 2583672 coefficients, 0 mismatches
Checked u coordinates 91/169: 3014284 coefficients, 0 mismatches
Checked u coordinates 104/169: 3444896 coefficients, 0 mismatches
Checked u coordinates 117/169: 3875508 coefficients, 0 mismatches
Checked u coordinates 130/169: 4306120 coefficients, 0 mismatches
Checked u coordinates 143/169: 4736732 coefficients, 0 mismatches
Checked u coordinates 156/169: 5167344 coefficients, 0 mismatches
Checked u coordinates 169/169: 5597956 coefficients, 0 mismatches
Total tensor coefficients checked: 5597956
Expected nonzero coefficients: 2366
Expected zero coefficients: 5595590
Mismatches: 0
PASS: all saved scheme identities hold exactly over Q; all 1479 terms are nonzero
```

Author comparison and packing proof:

Only after the independent check passed, I read verify-it-yourself/check_fmm_fast.py and verify-it-yourself/run_checks.sh. The author scales the three matrices separately. Independent recomputation in skeptic/audit_packing.py gives DU=5440, DV=40, DW=40 and product 8704000. For a fixed coefficient, the triangle inequality bounds its magnitude by B=sum_k max(abs(U_k))*max(abs(V_k))*max(abs(W_k))=1135320031680. Packing with base 2^43 is exact because B and the target scale are strictly below 2^42=4398046511104. Thus both actual and target vectors have every coordinate strictly between negative half-base and positive half-base. If their packed integers agree, the difference of their lowest coordinates is a multiple of the base and has magnitude smaller than the base, so it must be zero. Divide by the base and repeat to prove every coordinate agrees. This re-derives the balanced-digit injectivity argument, including negative coefficients. The author's loops compare every 169*182=30,758 pair, each representing 182 coordinates; no coefficient is omitted. Its integer scaling, bound and packing therefore justify exactly the same equations that my unpacked checker checked independently.

Independent bound-audit command (exit 0):

```sh
../../../.venv/bin/python skeptic/audit_packing.py > skeptic/packing_output.txt 2>&1
```

Actual output inserted from skeptic/packing_output.txt:

```text
Independent packing-proof arithmetic audit
Per-factor denominator LCMs: 5440, 40, 40
Target scale: 8704000
Sum of per-term maximum absolute coefficient products: 1135320031680
Coefficient bound bit length: 41
Slot width in bits: 43
Half-base: 4398046511104
PASS: both actual coefficient magnitudes and target coefficients are strictly below half-base
```

The first author-wrapper execution used the system python3 launcher and exited 0, with environment diagnostics on stderr. Exact command:

```sh
TMPDIR="$PWD/skeptic/tmp" sh verify-it-yourself/run_checks.sh > skeptic/author_output.txt 2>&1
```

Its complete captured output, including those diagnostics, inserted from skeptic/author_output.txt:

```text
sha256 matches INDEX.csv (e738d0f367b67ba740109db2687b58811da516ee74f67c42ccb934eab382548d)
== check_fmm_fast.py on object/13x13x14_r1479_Q.json
2026-10-15 03:14:48.284 xcodebuild[12083:73652713]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 03:14:48.600 xcodebuild[12083:73652710] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 41 bits, slot width 43 bits, 30758 blocks of 182 slots compared
PASS format=13x13x14 rank=1479
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x13x14 rank=1478: 833 of 30758 (a, b) blocks differ; first at A[5][0] x B[0][0])
ALL CHECKS PASS
```

I then selected the task-supplied interpreter for repeatable wrapper runs; all temporary negative-control files stayed inside skeptic/tmp. Exact commands, all exiting 0:

```sh
PATH="$PWD/../../../.venv/bin:$PATH" TMPDIR="$PWD/skeptic/tmp" sh verify-it-yourself/run_checks.sh > skeptic/author_output_controlled.txt 2>&1
PATH="$PWD/../../../.venv/bin:$PATH" TMPDIR="$PWD/skeptic/tmp" sh verify-it-yourself/run_checks.sh > skeptic/author_output_repeat.txt 2>&1
cmp skeptic/author_output_controlled.txt skeptic/author_output_repeat.txt
```

Actual output inserted from skeptic/author_output_controlled.txt:

```text
sha256 matches INDEX.csv (e738d0f367b67ba740109db2687b58811da516ee74f67c42ccb934eab382548d)
== check_fmm_fast.py on object/13x13x14_r1479_Q.json
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 41 bits, slot width 43 bits, 30758 blocks of 182 slots compared
PASS format=13x13x14 rank=1479
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x13x14 rank=1478: 833 of 30758 (a, b) blocks differ; first at A[5][0] x B[0][0])
ALL CHECKS PASS
```

There is no mathematical disagreement. Both checkers confirm the same format and 1,479 terms. The author's negative control removes one term and fails 833 coefficient blocks, so rejection is due to broken identities as well as the changed count. The initial launcher diagnostics are environmental stderr, not a varying arithmetic result; both later full wrapper transcripts agree byte for byte. All files needed for the exact scheme verification are present. The object's note references a parent construction and a term-order trace that are not supplied, but neither the claim of a valid explicit scheme nor the proof above relies on reconstructing that history.

REPRODUCE verdict: every saved-object property in this skeptic's remit is confirmed, with zero mismatches and no computational nondeterminism observed. External record status and novelty remain outside this verdict.

pass: true
