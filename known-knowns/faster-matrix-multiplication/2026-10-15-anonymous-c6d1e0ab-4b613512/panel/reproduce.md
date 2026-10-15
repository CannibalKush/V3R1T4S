# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object reproduces an exact rational bilinear matrix multiplication scheme with 1,538 nonzero rank-one terms. All 6,492,304 tensor coordinates agree exactly. The independent checker and author checker agree.

## Quoted claim, criterion, and definition

> object/13x14x14_r1538_Q.json is an exact bilinear scheme over Q for the matrix multiplication format ⟨13,14,14⟩ with 1538 rank-one terms, strictly fewer than 1558, the lowest rank listed for the sorted format 13x14x14 in the four live record tables and the V3R1T4S trophy case.

> Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format ⟨n,m,p⟩ with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

> Parse the candidate scheme (JSON U, V, W integer/rational matrices, or a Maple-style product list as in the Lille *_raw.mpl files). With exact fractions/sympy, form the r products m_k = (sum_ij U_k,ij A_ij)*(sum_jl V_k,jl B_jl) and check that for every (i,l) sum_k W_k,il m_k equals the symbolic entry (A*B)_il with exact coefficients over the claimed ring (reduce mod p for GF(p)); equivalently check the Brent equations. Count r after dropping zero terms. Re-fetch fmm_sota.json, the Lille per-format page, Perminov's README (all three ZT/Z/Q columns) and MerlijnW70's repo, and compare against the sorted format (rank is invariant under axis permutation/transposition). For p2 also re-fetch COVERAGE.md and the GF(2) schemes. Whole check runs in minutes on a 10-core Mac even for 16x16x16.

Only brackets were changed in these quotations: format brackets are Unicode, and the Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html.

Independent interpretation: A has shape n by m and B has shape m by p. Flatten A and B row by row. Interpret the third factor as the cyclic trace coordinate C[l,i], flattened row by row, so its coefficient contributes to output (i,l). For every i,j,j2,l,i2,l2, the sum of products of the three saved coefficients must equal 1 precisely when j=j2, i=i2 and l=l2, and 0 otherwise. Check every coordinate, with exact rational coefficients and without sampling.

The claim quotation also changes only its format brackets. The complete success criterion is quoted above, including clauses that require live evidence. Current table values, historical priority, and novelty are not adjudicated in this report.

## Independence and scope

I read `CLAIM.md` and inspected the saved object, `INDEX.csv`, and `table-record/README.md`. I wrote `skeptic/definition.md` and `skeptic/check_independent.py`, then ran the independent checker successfully and saved `skeptic/output.txt`, before reading anything in `verify-it-yourself/` or `REPRODUCE.md`. The checker uses Python's standard library, `Fraction`, and arbitrary precision integers; it does not import author code. Its cyclic third-factor convention was specified before author-code access and subsequently matched the author's documented convention.

Only package content in this folder was inspected. No network was used. The supplementary `skeptic/audit_saved_metadata.py` was written after the initial independent reproduction to audit the saved comparison arithmetic and the author's integer-packing proof bounds.

## Properties checked and proof derivation

1. **Object and claimed value.** Parsed the complete JSON with duplicate-key rejection. Required dimensions `[13,14,14]`, ring `Q`, the stated sparse encoding, and exactly 1,538 rows in each factor. Checked integer indices, their ranges and uniqueness, and every integer or rational coefficient. Dropped explicit zero coefficients when determining whether factors vanish. Every term has three nonzero factors, so dropping zero terms leaves 1,538 terms. This establishes a scheme of tensor rank at most 1,538; no minimal-rank lower bound is claimed or needed.
2. **Target format.** The largest dimension is 14, the sorted format is 13×14×14, and it is neither excluded format. Factor widths are 182, 196, and 182. There are 47,575, 42,591, and 37,455 nonzero coefficients in the three factors.
3. **Exact rational scaling.** For each factor row, let d be the least common multiple of its coefficient denominators and multiply the row by d. For each term let q be the product of its three row denominators. Let L be the least common multiple of all q. Multiply that term's integral outer product by L/q. The resulting integer tensor is exactly L times the rational tensor, with L = 54,400. All divisions used to scale coefficients are exact; there is no reduction modulo a prime or floating point approximation.
4. **Complete bilinear identity.** Expanded all 57,577,685 nonzero outer-product contributions into a dense tensor indexed by the ordered pair of input variables and the output coordinate. Subtracted L at each required product A[i,j]B[j,l] contributing to output (i,l). Examined every one of the 6,492,304 residual coordinates, including all zero requirements: 2,548 unit targets and 6,489,756 zero targets. Every residual is zero. Since the ordered noncommutative monomials A[i,j]B[j2,l] are the formal bilinear basis, equality of every coefficient proves the claimed multiplication identity, with each A factor preceding its B factor. Rational coefficients are central and give the required bilinear scheme over Q.
5. **Saved index and comparison arithmetic.** Recomputed the object SHA256 and matched `INDEX.csv`, including target, relative object filename, cell, and value. Independently extracted the saved numerical ranks: digest 1,582; Lille 1,614; Perminov ZT/Z/Q 1,614/1,614/1,582; trophy 1,558. The smallest saved numerical baseline is 1,558, and 1,538 is smaller by 20. The Merlijn record states no matching scheme; its repository tree is not saved, so that absence cannot be established independently from the metadata. These checks establish internal arithmetic consistency, not the truth or freshness of remote-source extracts.
6. **Applicability of remaining criterion clauses.** The exact characteristic-zero identity establishes that this is not a GF(2)-only verification, so the conditional F2 requirement and partial win p2 do not apply. The dimensions do not fall under partial win p1. The result counts multiplications, rather than additions. Whether a composition matches a listed construction, whether a rank was already attained over Q, and whether the result beats every current source require external historical/table evidence and belong to the other skeptic. No such judgment is made here. The object's note mentions a parent construction; that parent is not saved, so I do not certify the search history or provenance. The full saved tensor directly proves the final object without relying on that history. This is an explicit certificate, not an exhaustive-search claim; the verification itself is exhaustive.
7. **Author proof re-derived.** The author's factor-wide denominator scales, independently recomputed, are 5,440/40/40, giving D = 8,704,000. The sum of the products of termwise maximum absolute integral factor coefficients is B = 2,471,396,582,400. By the triangle inequality, B bounds each accumulated coefficient. The packed base is b = 2^44 = 17,592,186,044,416; both B and D are below b/2. For a packed residual, every signed coefficient therefore has magnitude below b. If a finite such polynomial evaluates to zero at b, reduction modulo b forces its constant coefficient to be zero; division by b and repetition forces every coefficient to zero. Thus packed equality really proves coordinate equality. The author's 35,672 blocks of 182 coordinates cover the same 6,492,304 equations as the independent check. Different denominator-clearing choices explain the different common scales; there is no disagreement.
8. **Repeatability and negative control.** Repeated the independent full expansion: both complete output files are byte-for-byte identical. Repeated the author's standalone checker: its mathematical output is byte-for-byte identical to the corresponding lines from the wrapper. The author's wrapper also removed the last term and correctly rejected the resulting 1,537-term tensor, detecting 729 bad input-pair blocks. The wrapper's first run emitted two platform diagnostics, preserved below; they do not affect the computed result. No object or mathematical-result nondeterminism was found.

## Exact commands and actual saved output

All commands were issued from this folder. Each check exited with status 0. Output blocks below are inserted directly from the saved files, without retyping or filtering.

Initial independent check:

```sh
python3 skeptic/check_independent.py > skeptic/output.txt 2>&1
```

```text
Object: object/13x14x14_r1538_Q.json
SHA256: 4b613512756bdb5c0303dc17236ad63b3b8a4e931d898e75e863d95d6dd9ab9e
Format: 13x14x14; sorted format eligible: PASS
Ring: Q; every saved coefficient parsed as an exact Fraction: PASS
Sparse indices, unique coordinates, and factor dimensions: PASS
Nonzero entries u/v/w: 47575/42591/37455
Terms declared=1538; saved=1538; nonzero=1538
Index convention: u[i*m+j], v[j*p+l], w[l*n+i] -> output[i,l]
Exact common tensor denominator: 54400
Rank-one coefficient contributions expanded: 57577685
Tensor coordinates checked: 6492304
Required unit coefficients: 2548
Required zero coefficients: 6489756
Exact residual mismatches: 0
INDEX.csv target, file, format, value, and object SHA256: PASS
Recorded comparison: 1538 < 1558; gap=20: PASS
Table metadata: saved source bodies absent; freshness and novelty not adjudicated
EXHAUSTIVE EXACT BILINEAR IDENTITY: PASS
```

Independent repeat:

```sh
python3 skeptic/check_independent.py > skeptic/output-repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output-repeat.txt
```

`cmp` exited 0 with no output. The second checker output is identical to the complete initial output pasted above.

Author wrapper, with its temporary negative-control files kept within this folder:

```sh
TMPDIR=skeptic sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
```

```text
sha256 matches INDEX.csv (4b613512756bdb5c0303dc17236ad63b3b8a4e931d898e75e863d95d6dd9ab9e)
== check_fmm_fast.py on object/13x14x14_r1538_Q.json
2026-10-15 03:14:34.728 xcodebuild[11863:73651869]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 03:14:35.144 xcodebuild[11863:73651867] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 42 bits, slot width 44 bits, 35672 blocks of 182 slots compared
PASS format=13x14x14 rank=1538
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x14x14 rank=1537: 729 of 35672 (a, b) blocks differ; first at A[0][0] x B[0][0])
ALL CHECKS PASS
```

Author standalone repeat:

```sh
python3 verify-it-yourself/check_fmm_fast.py object/13x14x14_r1538_Q.json --expect-rank 1538 > skeptic/author-repeat.txt 2>&1
```

```text
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 42 bits, slot width 44 bits, 35672 blocks of 182 slots compared
PASS format=13x14x14 rank=1538
```

Supplementary saved-metadata and proof-bound audit:

```sh
python3 skeptic/audit_saved_metadata.py > skeptic/audit-output.txt 2>&1
```

```text
Independently recomputed author denominator scales: 5440/40/40
Author global denominator product: 8704000
Sum of termwise maximum absolute integer products: 2471396582400
Bound bit length: 42
Slot width: 44
Base: 17592186044416
Both coefficient and target magnitudes are strictly below half the base: PASS
Residual magnitudes are strictly below the base: PASS
Saved digest rank: 1582
Saved Lille rank: 1614
Saved Perminov ZT/Z/Q columns: 1614/1614/1582
Saved trophy rank: 1558
Minimum of saved numeric baseline entries: 1558; strict gap: 20; PASS
Saved Merlijn statement: no 13x14x14 scheme; source tree not included, not independently established
Source freshness, completeness, and novelty: outside reproduction scope; no network used
Independent run outputs byte-for-byte identical: PASS
Independent output SHA256: e5404155d85a7c3bee22e4a64529c3cde294f2d0850d6abe5ede72713496bff5
```

## Mismatches and verdict scope

No mismatch was found in the saved object, index hash, claimed term count, exact bilinear equations, saved numerical comparison arithmetic, or agreement between the two independent verification methods. The explicit scheme and all locally checkable mathematical properties pass reproduction. The table record contains metadata only, with no saved source bodies; live fetches, completeness of remote tables, construction history, and novelty are outside this reproduction verdict and remain unverified here.

pass: true
