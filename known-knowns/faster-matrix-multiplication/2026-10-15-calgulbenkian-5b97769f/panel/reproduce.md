# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

## Definition and success criterion checked

The quotations below come from `CLAIM.md`. I changed only the brackets around format symbols and Lille URL placeholders to braces; the Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html. Mathematical inequalities are unchanged.

## Success criterion

> Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format {n,m,p} with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

## Mathematical definition and verification method

> Parse the candidate scheme (JSON U, V, W integer/rational matrices, or a Maple-style product list as in the Lille *_raw.mpl files). With exact fractions/sympy, form the r products m_k = (sum_ij U_k,ij A_ij)*(sum_jl V_k,jl B_jl) and check that for every (i,l) sum_k W_k,il m_k equals the symbolic entry (A*B)_il with exact coefficients over the claimed ring (reduce mod p for GF(p)); equivalently check the Brent equations. Count r after dropping zero terms. Re-fetch fmm_sota.json, the Lille per-format page, Perminov's README (all three ZT/Z/Q columns) and MerlijnW70's repo, and compare against the sorted format (rank is invariant under axis permutation/transposition). For p2 also re-fetch COVERAGE.md and the GF(2) schemes. Whole check runs in minutes on a 10-core Mac even for 16x16x16.


## Scope and independence

I read `CLAIM.md`, the object, `INDEX.csv`, and `table-record/README.md`, then wrote `skeptic/definition.md` and `skeptic/check.py` without opening `verify-it-yourself/` or `REPRODUCE.md`. The independent checker uses Python's standard library, exact integers, and `fractions.Fraction`. Its tensor calculation reads only the candidate object; the index and table metadata are checked separately afterward. No network was used. Only this package supplied evidence; no neighboring package, repository history, or external source was consulted. The author runner creates and reads its own temporary negative-control copy; an additional run placed its temporary files in `skeptic/tmp`.

Currentness, novelty, the truth of asserted remote fetches, and historical construction claims are outside this reproduction judgment. `table-record/README.md` explicitly contains metadata only: the fetched response bodies and the prior rank-1763 scheme are not saved here. Their digests cannot be recomputed, Merlijn's asserted absence cannot be independently established, and the individual Perminov ZT/Z/Q entries cannot be inspected. I check only the saved statements and arithmetic comparisons, without treating metadata as independently authenticated source data.

## Properties and full proof

1. **Object and format.** Decode `object/13x15x15_r1762_Q.json`, reject duplicate JSON keys, require format 13x15x15, positive integer dimensions, maximum dimension at most 16, and neither excluded sorted format. Require ring Q and the declared sparse encoding. Require exactly 1,762 rows in each factor, even sparse row lengths, unique in-bounds indices, and integer or rational-string coefficients. Count terms after removing zero vectors. Each surviving U, V, and W vector is nonzero; over Q its outer product is a nonzero rank-one tensor.
2. **Exact arithmetic and noncommutative bilinearity.** Interpret A as 13x15 and B as 15x15. Each product multiplies a Q-linear combination of A entries on the left by a Q-linear combination of B entries on the right. The checker never reverses that multiplication order. Q coefficients are central, so an identity of the ordered A-entry/B-entry coefficients proves the stated noncommutative bilinear scheme.
3. **Every coefficient, including zeros.** For a = i*15+j, b = h*15+l, and c = l0*13+i0, independently expand

   `T[a,b,c] = sum_k U[k,a] * V[k,b] * W[k,c]`.

   The required coefficient is `delta(i,i0) * delta(j,h) * delta(l,l0)`. This follows directly from `C[i0,l0] = sum_j A[i0,j]*B[j,l0]`. The checker adds all 39,018,661 saved scalar contributions with exact integers/Fractions and scans all 195*225*195 = 8,555,625 positions. Equality at every position proves every output polynomial, including the absence of every unwanted monomial. There is no probabilistic or numerical tolerance step. This is an exhaustive identity check, not a sample of input matrices or terms.
4. **Representation convention.** Before reading the author's convention, compare the complete tensor against both common W interpretations, `W[i0*15+l0]` and `W[l0*13+i0]`. Report both mismatch counts. A full match establishes the valid interpretation; the alternative is a representation diagnostic, not a second claimed mathematical property.
5. **Count and claimed improvement.** Require 1,762 surviving terms, hence a bilinear algorithm using 1,762 multiplications and a tensor-rank upper bound of 1,762. Check 1762 strictly below the saved numbers 1763, 1776, 1797, and 1776. This does not purport to prove a lower bound of 1,762 for the tensor's minimal rank. Read the saved Merlijn metadata assertion and explicitly leave its external truth unadjudicated.
6. **Package consistency.** Compute SHA256 of the actual object bytes and match `INDEX.csv`; check its target, cell, file, value, and table value. Match the saved table statements used for the inequalities. The metadata's minimum 1763 includes the asserted repository scheme; the minimum of its numeric live-table entries alone is 1776.
7. **Conditional criteria.** The GF(2)-only and p2 clauses do not apply to an identity proved over Q. The 17-to-32 partial-win format clause does not apply. Historical rank-equality exclusions and live-fetch timing belong to the other skeptic; the saved metadata alone cannot establish them. No exhaustive search or optimality proof is claimed by this package, so there is no search space to sample or certify.


The object's `note` names a parent transformation and says raw rank 1796, absorbed 34. The arithmetic 1796 - 34 = 1762 agrees. The parent and transformation history are not provided, so I do not assert that history was reproduced. No such history is needed for the direct, exhaustive proof of the final saved object above.

## Exact commands and actual output

All commands ran from this folder. Both independent runs exited 0. The independent checker had already completed successfully before I opened either author-checker file.

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
```

Actual complete contents of `skeptic/output.txt` (copied directly from the saved output; the repeat is byte-identical):

```text
Object: object/13x15x15_r1762_Q.json
SHA256: 5b97769fb1c3115c7195f0c508e0cae9ded013ef2543a7f0d5aa4147410e1647
Format: 13x15x15; ring: Q; eligible dimensions and exclusions: PASS
Decoded terms: 1762; nonzero rank-one terms: 1762; zero terms: 0
Sparse bounds, unique indices, row lengths, exact rational coefficients: PASS
Nonzero coefficients U/V/W: 41928 34058 40741
Expanded scalar contributions: 39018661
Exhaustive coefficient comparisons per convention: 8555625
Actual nonzero tensor coefficients: 2925
W convention row-major: 5760 coefficient mismatches
W convention transposed: 0 coefficient mismatches
Confirmed mapping: U[i*m+j], V[j*p+l], W[l*n+i] contributes to C[i,l]
Every required coefficient is 1; every other coefficient is 0 over Q: PASS
INDEX target/cell/value/file/SHA256/table value: PASS
Saved numerical comparisons: 1762 < 1776; 1762 < 1797; 1762 < 1776; 1762 < 1763: PASS
Saved Merlijn metadata: no entry (source contents absent; not independently audited)
GF(2)-only clause: not applicable; identity verified over Q
External source truth, fetch freshness, novelty and construction history: not adjudicated
INDEPENDENT CHECK: PASS (all object coefficients; saved metadata consistency)
```

Only after the first independent run, I inspected `REPRODUCE.md`, `verify-it-yourself/check_fmm_fast.py`, and `verify-it-yourself/run_checks.sh`, then ran:

```sh
sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
```

Exit status: 0. Actual complete contents of `skeptic/author-output.txt`:

```text
sha256 matches INDEX.csv (5b97769fb1c3115c7195f0c508e0cae9ded013ef2543a7f0d5aa4147410e1647)
== check_fmm_fast.py on object/13x15x15_r1762_Q.json
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 40 bits, slot width 42 bits, 43875 blocks of 195 slots compared
PASS format=13x15x15 rank=1762
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x15x15 rank=1761: 8550 of 43875 (a, b) blocks differ; first at A[0][1] x B[0][0])
ALL CHECKS PASS
```

## Re-derivation of the author's arithmetic proof

The author's method is different from the independent direct Fraction expansion:

1. Compute the least common multiple of every denominator separately in U, V, W. Multiplication by DU, DV, DW makes every coefficient integral; every triple product is multiplied by D = DU*DV*DW. I independently recomputed those LCMs and explicitly checked divisibility before integer conversion.
2. For any a,b,c, the triangle inequality gives

   `abs(sum_t U'[t,a]*V'[t,b]*W'[t,c]) <= sum_t max_abs(U'[t])*max_abs(V'[t])*max_abs(W'[t]) = B`.

   The independent bound reconstruction gives B = 607511887040, which has 40 bits. D = 8704000. The author chooses s = 42 and base b = 2^s. Thus every actual and target coefficient has absolute value strictly below b/2; indeed each coefficient difference has absolute value at most B+D, also strictly below b/2 for this saved object.
3. Packing a row as `sum_c W'[t,c]*b^c` commutes with exact integer sums and multiplication, so the author's packed difference is exactly `sum_c difference[c]*b^c`. If that integer is zero, reduction modulo b forces difference[0] = 0 because its magnitude is below b/2. Divide by b and repeat for all remaining positions. This proves zero packed difference is equivalent to all slot equations, including negative coefficients. There is no hash collision or modular acceptance probability.
4. The code enumerates every one of 195*225 = 43875 input-entry pairs, including absent dictionary entries as zero, and compares the full packed target of 195 slots. This covers the same 8,555,625 coefficients checked independently. Its W indexing agrees with the independently established `W[l*13+i]` convention. Its surviving-term count agrees with 1762.
5. Its negative control removes one actual term; its reported rank 1761 and 8550 failing coefficient blocks show it rejects a mathematically wrong tensor before the expected-rank comparison. No negative-control failure is a candidate-object mismatch.

Supplementary independent reconstruction command, written after the initial exhaustive proof:

```sh
python3 skeptic/audit_packing.py > skeptic/packing-output.txt 2>&1
```

Exit status: 0. Actual complete contents of `skeptic/packing-output.txt`:

```text
Independent denominator LCMs DU/DV/DW: 5440 40 40
Independent target scale D: 8704000
Independent coefficient bound B: 607511887040
Bound bit length: 40 ; slot width: 42
2^(s-1) > max(D,B): PASS
Packing proof numerical premises: PASS
```

## Repeats, output differences, and disagreement assessment

For an extra author-run check, I changed the temporary-directory environment:

```sh
mkdir -p skeptic/tmp
TMPDIR=skeptic/tmp sh verify-it-yourself/run_checks.sh > skeptic/author-output-repeat.txt 2>&1
mv skeptic/author-output-repeat.txt skeptic/author-output-tmpdir.txt
```

That runner exited 0, but comparing its raw output with the original detected two additional `xcodebuild` platform diagnostic lines. I retained the complete output rather than concealing that difference. Actual complete contents of `skeptic/author-output-tmpdir.txt`:

```text
sha256 matches INDEX.csv (5b97769fb1c3115c7195f0c508e0cae9ded013ef2543a7f0d5aa4147410e1647)
== check_fmm_fast.py on object/13x15x15_r1762_Q.json
2026-10-15 15:09:57.519 xcodebuild[62680:76021557]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 15:09:57.899 xcodebuild[62680:76021556] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 40 bits, slot width 42 bits, 43875 blocks of 195 slots compared
PASS format=13x15x15 rank=1762
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x15x15 rank=1761: 8550 of 43875 (a, b) blocks differ; first at A[0][1] x B[0][0])
ALL CHECKS PASS
```

This was a changed environment, not a repeated identical invocation. The diagnostic lines concern the filesystem event stream and developer cache lookup. Removing exactly those two identified platform lines yields the original author output byte for byte; no mathematical result or negative-control result changed. I then repeated the original command with its original environment:

```sh
sh verify-it-yourself/run_checks.sh > skeptic/author-output-repeat.txt 2>&1
python3 skeptic/compare_runs.py > skeptic/comparison-output.txt 2>&1
```

Both exited 0. The comparison checks that each repeated output is complete, has its expected final PASS marker, and is byte-identical to its corresponding original. It also checks the exact characterization of the changed-environment output above. Actual complete contents of `skeptic/comparison-output.txt`:

```text
Independent repeat comparison: PASS (byte-identical complete output)
Author repeat comparison: PASS (byte-identical complete output)
Changed-TMPDIR author run: same checker output plus 2 platform diagnostic lines
Observed non-determinism with unchanged command/environment: none
```

The 5760 mismatches under the alternative row-major W interpretation are fully resolved by the transposed interpretation established before reading the author's code; that interpretation has zero mismatches and is precisely the author's documented convention. There is no disagreement about the actual candidate. Both methods are deterministic exact exhaustive checks. Identical-command repeats produced identical complete outputs; no result non-determinism was observed. The environment-dependent platform diagnostics are disclosed above.

## Verdict

The explicit saved object is a valid bilinear matrix-multiplication scheme over Q for 13x15x15 with exactly 1762 nonzero rank-one terms. Every tensor equation passes independently and agrees with the author's checker, and the object matches the index digest. All saved numerical comparisons stated above hold. This is a reproduction pass for the checkable mathematical and package-consistency properties, without a judgment on current table records or novelty. The absent remote response bodies and parent history are recorded limitations, not premises of the exhaustive identity proof.

pass: true
