Independent REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object reproduces: an exact rational bilinear matrix multiplication scheme for (15,16,15), with 2105 nonzero rank-one terms. The exhaustive independent check and the author's check agree. The saved numerical baseline is 2132, so the saved claimed improvement is 27 multiplications. This report does not judge table freshness or novelty.

I read CLAIM.md and the object before writing skeptic/check.py and recording the definition in skeptic/definition.md. I completed the independent exhaustive run and saved skeptic/output.txt before reading REPRODUCE.md or anything in verify-it-yourself/. The independent checker uses only Python's standard library and does not import the author's code. Only files in this package supplied claim evidence; no network was used.

The definition and success criterion checked are quoted below. In the success criterion, I changed only the template angle brackets to braces: the format placeholder and the Lille URL template https://fmm.univ-lille.fr/{n}x{m}x{p}.html. All other quoted wording is unchanged.

> Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format {n,m,p} with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

Quoted verification definition from CLAIM.md:

> Parse the candidate scheme (JSON U, V, W integer/rational matrices, or a Maple-style product list as in the Lille *_raw.mpl files). With exact fractions/sympy, form the r products m_k = (sum_ij U_k,ij A_ij)*(sum_jl V_k,jl B_jl) and check that for every (i,l) sum_k W_k,il m_k equals the symbolic entry (A*B)_il with exact coefficients over the claimed ring (reduce mod p for GF(p)); equivalently check the Brent equations. Count r after dropping zero terms. Re-fetch fmm_sota.json, the Lille per-format page, Perminov's README (all three ZT/Z/Q columns) and MerlijnW70's repo, and compare against the sorted format (rank is invariant under axis permutation/transposition). For p2 also re-fetch COVERAGE.md and the GF(2) schemes. Whole check runs in minutes on a 10-core Mac even for 16x16x16.

Properties checked and proof re-derived:

- Explicit saved scheme and integrity: parsed object/15x16x15_r2105_Q.json with duplicate JSON keys rejected. Checked the ring Q, exact integer or rational vocabulary entries, encoding grammar, all vocabulary references, row lengths, and equal row counts. U, V and W have 2105 rows of widths 240, 240 and 225. The object's SHA256 matches INDEX.csv.
- Allowed format: dimensions are (15,16,15), maximum 16, sorted format (15,15,16), and neither excluded cubic format. INDEX.csv uses the same sorted format.
- Term count: tested all three vectors of every term for nonzeroness. All 2105 terms have three nonzero factors, so each is a nonzero rank-one tensor over Q. No zero terms were counted. This certifies a scheme with 2105 products, without asserting that 2105 is the minimum possible tensor rank.
- Ordered bilinear definition: U[i*16+j] multiplies A[i,j]; V[j*15+l] multiplies B[j,l]; W[l*15+i] contributes to output C[i,l]. This flattening was stated in my independent checker before reading the author. The author's documented convention later agreed. Each product has the A linear form first and the B linear form second, so the identity does not assume that input entries commute.
- Exact rational reduction: for term t, clear denominators separately in each of its three vectors, obtaining integer vectors and a positive denominator d_t equal to the product of their three denominator LCMs. The resulting integer outer product divided by d_t equals the original rational outer product. With D = lcm_t(d_t) = 50400, multiplying each integer outer product by D/d_t produces exactly D times the original tensor contribution. No rounding, modular test, or random test enters this argument.
- Exhaustive identity: for each of the 225 output coordinates, directly accumulate the coefficient of every one of the 240*240 ordered A/B monomials in a separate integer array. For output C[i,l], the desired coefficient is D precisely at A[i,j]*B[j,l] for j from 0 through 15; all other coefficients must be zero. Every array entry is compared. The run checked 12,960,000 coefficients, with exactly 3,600 unit coefficients and 12,956,400 zero coefficients after dividing by D. Equality of all formal monomial coefficients proves every output equals the defining matrix product for all inputs over Q. This is an exhaustive symbolic check, not a sample or a claimed search for all possible schemes.
- Saved numerical comparison: INDEX.csv and table-record/README.md consistently state 2132 for the digest and Lille page and 2132/2132/2132 for Perminov's ZT/Z/Q columns. I checked 2105 is strictly smaller than every one of those saved numeric entries. The metadata reports no matching Merlijn scheme and no trophy-case row. Those absence assertions cannot be independently established without the missing raw source responses; I do not promote them to verified source facts.
- Applicability of the remaining clauses: this is an exact Q scheme, so the GF(2)-only condition and partial win p2 do not apply; maximum dimension 16 rules out partial win p1. The proposed change is a lower product count relative to the saved 2132 baseline, not an addition-count improvement. Equality with an already-listed rank, the construction exclusion, and re-derivation of an already-attained rank require table/newness evidence; I make no ruling on those external questions. All saved numeric comparisons are strict inequalities.
- Determinism: a second full independent run exited 0 and its entire output was byte-identical to the first. The checker has no random choices, hash-order-dependent arithmetic, floating-point operations or external data dependencies.

Exact independent commands, run from this folder (all exited 0):

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output-repeat.txt
```

Full actual output pasted directly from skeptic/output.txt:

```text
object: object/15x16x15_r2105_Q.json
sha256: 4b68518ac7f293047071df6723a04783e4d38f302c6b98ccaa02f0c66669ae3b
format: (15, 16, 15) sorted: (15, 15, 16)
ring: Q; exact rational parsing; encoding: vocab_rle_v1
matrix widths: 240 240 225 ; rows each: 2105
nonzero entries U,V,W: 64728 57863 41552
nonzero rank-one terms: 2105 ; zero terms: 0
claimed saved baseline: 2132; strict inequality: True
common tensor denominator: 50400
integer contribution updates: 72912151
verified output coordinates: 25/225
verified output coordinates: 50/225
verified output coordinates: 75/225
verified output coordinates: 100/225
verified output coordinates: 125/225
verified output coordinates: 150/225
verified output coordinates: 175/225
verified output coordinates: 200/225
verified output coordinates: 225/225
exhaustive tensor coefficients checked: 12960000
unit coefficients: 3600 ; zero coefficients: 12956400
expected unit coefficients n*m*p: 3600
RESULT: PASS (complete exact matrix multiplication identity and claimed rank)
```

The output in skeptic/output-repeat.txt is byte-identical to the pasted output; cmp emitted no output.

Only after the first independent exhaustive run completed did I read and run the author's checker. Exact standalone command (exit 0):

```sh
python3 verify-it-yourself/check_fmm_fast.py object/15x16x15_r2105_Q.json --expect-rank 2105 > skeptic/author-output.txt 2>&1
```

Full actual output pasted directly from skeptic/author-output.txt:

```text
exact integer check: D=15120000 (DU=60, DV=120, DW=2100), coefficient bound 42 bits, slot width 44 bits, 57600 blocks of 225 slots compared
PASS format=15x16x15 rank=2105
```

I also ran the supplied run script, keeping its temporary negative-control object inside skeptic/. Exact command (exit 0):

```sh
TMPDIR="$PWD/skeptic" sh verify-it-yourself/run_checks.sh > skeptic/author-run-output.txt 2>&1
```

Full actual output pasted directly from skeptic/author-run-output.txt, including its toolchain diagnostics:

```text
sha256 matches INDEX.csv (4b68518ac7f293047071df6723a04783e4d38f302c6b98ccaa02f0c66669ae3b)
== check_fmm_fast.py on object/15x16x15_r2105_Q.json
2026-10-15 03:33:10.781 xcodebuild[26265:73712383]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 03:33:11.592 xcodebuild[26265:73712381] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
exact integer check: D=15120000 (DU=60, DV=120, DW=2100), coefficient bound 42 bits, slot width 44 bits, 57600 blocks of 225 slots compared
PASS format=15x16x15 rank=2105
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=15x16x15 rank=2104: 330 of 57600 (a, b) blocks differ; first at A[1][0] x B[3][2])
ALL CHECKS PASS
```

The two Xcode diagnostics are environmental messages in that shell run; the positive checker exited successfully and the deliberately altered object failed. They do not change the mathematical output. The negative control drops the last term, leaving 2104 terms; the author checker found 330 incorrect input-pair blocks, rather than merely rejecting the expected-rank argument.

The author's packing proof was also re-derived, independently of its implementation. Global denominator LCMs 60, 120 and 2100 give D_author = 15120000, which is 300 times my termwise common denominator. This scaling difference is expected, not a disagreement. The sum of per-term products of maximum absolute integer vector entries bounds the absolute value of every tensor coefficient by the triangle inequality. That bound is B = 2759360934600. The author's slot width 44 gives base 2^44 = 17592186044416. Every difference between a reconstructed coefficient and its target has magnitude at most B + D_author, strictly below that base. If the packed difference is zero, reduction modulo the base forces its first coefficient to be zero, since that coefficient's magnitude is below the base; division by the base repeats the argument for every coefficient. Thus packed equality implies every coefficient equality. Comparing all 57,600 input pairs covers all 225 output slots in each pair. My original checker instead accumulates each output's coefficients directly and needs no packing argument.

Exact command re-deriving those numerical bounds (exit 0):

```sh
python3 skeptic/check_packing_argument.py > skeptic/packing-output.txt 2>&1
```

Full actual output pasted directly from skeptic/packing-output.txt:

```text
global vector denominator LCMs: 60 120 2100
global tensor denominator: 15120000 = 300 * independent denominator 50400
sum of per-term maximum absolute integer products: 2759360934600
bound bits: 42 ; slot width: 44 ; base: 17592186044416
maximum coefficient difference bound B+D: 2759376054600 ; strictly below base: True
proof: if sum_c e[c]*base**c = 0 and abs(e[c]) < base, reduction modulo base forces e[0]=0; divide and repeat
packing covers: 57600 input pairs times 225 output slots = 12960000 tensor equations
RESULT: PASS (packing-bound and coefficient-injectivity argument re-derived)
```

Local metadata consistency and output comparison were checked with this exact command (exit 0):

```sh
python3 skeptic/check_saved_metadata.py > skeptic/metadata-output.txt 2>&1
```

Full actual output pasted directly from skeptic/metadata-output.txt:

```text
INDEX: one object; relative file exists; target, sorted format, value, fetch timestamp and SHA256 consistent
saved metadata: digest 2132; Lille 2132; Perminov ZT/Z/Q = 2132/2132/2132
saved metadata reports: Merlijn no matching scheme; trophy case no matching row
saved numeric baseline: 2132; claimed term count: 2105; improvement: 27
source metadata: five HTTP-200 entries with SHA256 fields; raw source responses absent
external source contents, freshness and novelty: not assessed
independent full rerun: byte-identical output; both exits were 0
independent and author checkers: agree on exact identity and 2105 nonzero terms
RESULT: PASS (local metadata consistency and deterministic reproduction only)
```

No mismatch, missing claimed object, or mathematical nondeterminism was found. The raw scoreboard responses are not saved: their recorded HTTP statuses, hashes, fetch times and extracted cells are author metadata, not authenticated snapshots. Live fetching, source extraction accuracy, current records, prior attainment and novelty are outside this offline REPRODUCE determination and are left to the table skeptic. Every property of the explicit scheme and every local numerical consistency property available in the saved files was confirmed.

pass: true
