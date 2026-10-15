REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object passes independent exhaustive exact verification: it represents 13x13x15 matrix multiplication over Q using 1578 nonzero rank-one terms. This is a reproducibility verdict on the supplied files. Table currency and novelty are not judged here.

I read CLAIM.md, the object, INDEX.csv, table-record/README.md and REPRODUCE.md before examining any file in verify-it-yourself/. I first wrote skeptic/definition.md and skeptic/check.py, then ran the independent checker to completion and saved skeptic/output.txt. Only after its successful exit did I read the author implementation. skeptic/pre_author_sha256.json records the independent checker, definition and output hashes at that boundary; they remain unchanged. No package file was modified. No network was used, and no external claim materials were read.

The claim checked (quoted from CLAIM.md):
> object/13x13x15_r1578_Q.json is an exact bilinear scheme over Q for the matrix multiplication format {13,13,15} with 1578 rank-one terms, strictly fewer than 1591, the lowest rank listed for the sorted format 13x13x15 in the four live record tables and the V3R1T4S trophy case.

The mathematical definition and verification instruction (quoted from CLAIM.md):
> Parse the candidate scheme (JSON U, V, W integer/rational matrices, or a Maple-style product list as in the Lille *_raw.mpl files). With exact fractions/sympy, form the r products m_k = (sum_ij U_k,ij A_ij)*(sum_jl V_k,jl B_jl) and check that for every (i,l) sum_k W_k,il m_k equals the symbolic entry (A*B)_il with exact coefficients over the claimed ring (reduce mod p for GF(p)); equivalently check the Brent equations. Count r after dropping zero terms. Re-fetch fmm_sota.json, the Lille per-format page, Perminov's README (all three ZT/Z/Q columns) and MerlijnW70's repo, and compare against the sorted format (rank is invariant under axis permutation/transposition). For p2 also re-fetch COVERAGE.md and the GF(2) schemes. Whole check runs in minutes on a 10-core Mac even for 16x16x16.

The entire success criterion is quoted so that every clause checkable from the saved files is explicit. In these quotations I changed only the angle brackets delimiting format notation and URL placeholders to braces; in particular the Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html.

> Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format {n,m,p} with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

The independent derivation expands the ordered products A[a,b] B[c,d]. In output (i,l), their coefficient must be 1 exactly when a=i, b=c and d=l, and 0 otherwise. Thus matching every coefficient proves the formal non-commutative bilinear identity; it does not rely on substituting sample matrices or commuting A entries past B entries.

Before inspecting author code I specified row-major U and V, and independently tested both usual W conventions. Only the trace convention w[l*n+i] passed; it later matched the author's documented convention exactly. The 4992 mismatches for the alternative output-row-major convention are a rejected interpretation, not a mismatch of the claimed scheme.

Properties checked and how:

- The dimensions are 13,13,15; their maximum is 15, and their sorted tuple avoids both excluded formats.
- The saved object exists, parses as JSON without duplicate keys, declares ring Q and sparse_flat_pairs encoding, and has exactly 1578 rows in each factor. Every coefficient is an exact integer or rational; sparse indices are unique and within the appropriate 169,195,195 coordinate ranges.
- Every term has three nonzero factors. Dropping zero terms leaves exactly 1578 terms. This certifies a decomposition with 1578 products, hence tensor rank at most 1578; it is not a lower-bound claim about optimal rank.
- For each row of each factor I clear its denominators exactly. If the three row denominators for term k multiply to d_k, I use L=lcm_k(d_k)=54400 and multiply its integer outer product by L/d_k. This equals L times the original rational tensor contribution, with no truncation. Direct integer accumulation produces all 6426225 coefficients. All match the scaled target: 2535 coefficients equal L, and the remaining 6423690 equal zero. There are no packed slots, random samples, modular reductions or floating point in this independent check.
- The object's SHA-256 matches INDEX.csv, whose target, format, claimed value and saved baseline also agree. The four recorded source values are 1605,1605,1591,1591, with Perminov's three columns individually 1591. The saved comparisons give 1578 strictly less than each and 13 below their minimum. These are checks of the supplied metadata and arithmetic.
- The ring is Q, so the GF(2)-only condition and partial-win conditions do not apply. The supplied rank is unequal to every rank recorded for this format. No claim about provenance, novelty or exhaustive coverage of historical records is inferred from that observation.
- Repeating the complete independent run and the direct author run produced byte-identical outputs. Both programs use deterministic exact arithmetic. The original object and frozen independent files are unchanged.

The table record explicitly saves metadata only: there are no fetched source bodies or repository snapshots. Their source digests cannot be recomputed or their cell extraction authenticated from this package. Live re-fetches, current minima, the trophy-case absence, and novelty are outside this offline REPRODUCE verdict, as requested. No exhaustive search is claimed; the exhaustive task here is the coefficient identity, and every equation was checked.

Exact independent command (exit 0):

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

Its complete actual output, inserted directly from skeptic/output.txt:

```text
object: object/13x13x15_r1578_Q.json
object sha256: 9a8f254ed5b7e15b8f4157da632c5adc686e46c4f020659b924114c8b7c5a618
format: 13x13x15; ring: Q; encoding: sparse_flat_pairs
format eligibility: PASS (maximum dimension 15; excluded formats avoided)
structure: PASS (row counts, rational coefficients, unique indices, index bounds)
factor nonzeros: u=34650 v=40066 w=37933
terms: declared=1578 active=1578 zero=0
common denominator for tensor coefficients: 54400
exact integer contributions accumulated: 44460676
tensor coefficient equations per convention: 6426225
convention trace: w[l*n+i]: mismatches=0; tensor nonzeros=2535; expected nonzeros=2535
convention output: w[i*p+l]: mismatches=4992; tensor nonzeros=2535; expected nonzeros=2535
first mismatch (w index, u index, v index, scaled actual, scaled expected): (1, 0, 1, 0, 54400)
accepted convention: trace: w[l*n+i]
exhaustive exact bilinear identity: PASS
INDEX object digest, format, value and saved baseline: PASS
saved metadata ranks: Lille digest=1605; Lille page=1605; Perminov ZT/Z/Q=1591/1591/1591; Merlijn=1591
saved metadata comparison: 1578 < 1591 (minimum); difference=13: PASS
source snapshots are absent; metadata extraction and live status are outside this offline check
INDEPENDENT SAVED-OBJECT CHECK PASS
```

Only after that output was saved, I ran the author's checker (exit 0):

```sh
python3 verify-it-yourself/check_fmm_fast.py object/13x13x15_r1578_Q.json --expect-rank 1578 > skeptic/author_output.txt 2>&1
```

Its complete actual output:

```text
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 40 bits, slot width 42 bits, 32955 blocks of 195 slots compared
PASS format=13x13x15 rank=1578
```

The author's denominator scaling and packed-integer proof were also re-derived in skeptic/audit_author.py. The global scales differ from my per-term scaling but represent the same rational equations. The bound follows from the triangle inequality: each scaled coefficient has magnitude at most the sum, over terms, of the three factor maxima multiplied together. With target magnitude at most D, a coefficient difference has magnitude at most B+D. If its packed vector were zero, the lowest nonzero coefficient difference would have to be divisible by base 2^s; its magnitude is strictly smaller than that base, a contradiction. This proves that packed equality checks every slot. The author visits all 32955 input pairs, including untouched pairs; each contains 195 output coefficients.

Exact command (exit 0):

```sh
python3 skeptic/audit_author.py > skeptic/author_proof_output.txt 2>&1
```

Complete actual output:

```text
independently re-derived global denominator scales: DU=5440 DV=40 DW=40
scaled target D: 8704000
coefficient bound B: 721212962720
bound bit length: 40
slot width s: 42
base 2^s: 4398046511104
maximum difference bound B+D: 721221666720
injectivity condition 2^s > B+D: PASS
all 169*195=32955 input pairs, each with 195 output slots: 6426225 equations
proof: each coefficient difference is an integer of absolute value at most B+D;
if a packed difference vanished, its lowest nonzero digit would be a multiple
of base 2^s with absolute value smaller than that base, which is impossible.
AUTHOR PACKING ARGUMENT CONFIRMED
```

I also ran the supplied wrapper, retaining its complete stdout and stderr. TMPDIR keeps its temporary negative-control files inside skeptic/:

```sh
TMPDIR=skeptic sh verify-it-yourself/run_checks.sh > skeptic/author_run_output.txt 2>&1
```

It exited 0. Its complete actual output includes host developer-tool diagnostics; these are preserved verbatim. The direct checker outputs above and below have no such diagnostics and repeat identically.

```text
sha256 matches INDEX.csv (9a8f254ed5b7e15b8f4157da632c5adc686e46c4f020659b924114c8b7c5a618)
== check_fmm_fast.py on object/13x13x15_r1578_Q.json
2026-10-15 03:14:37.050 xcodebuild[11898:73651994]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 03:14:37.506 xcodebuild[11898:73651991] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 40 bits, slot width 42 bits, 32955 blocks of 195 slots compared
PASS format=13x13x15 rank=1578
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x13x15 rank=1577: 76 of 32955 (a, b) blocks differ; first at A[6][4] x B[0][2])
ALL CHECKS PASS
```

A separate sensitivity check adds 1 to the first stored U coefficient and saves skeptic/perturbed.json, retaining all 1578 active terms. It invokes the frozen independent checker on that file and requires rejection specifically at the tensor identity, rather than at a term-count or digest check. The expected 102 failing equations were detected. This intentional negative-control mismatch is not a mismatch of the original object.

Exact command (exit 0 means the negative control was rejected as required):

```sh
python3 skeptic/negative_control.py > skeptic/negative_output.txt 2>&1
```

Complete actual output:

```text
negative control: add 1 to the first stored U coefficient; retain 1578 active terms
object: skeptic/perturbed.json
object sha256: 61708fe26f9a45e3c2e4ecf806f39af16af2eb8aafb27a3379d749360ee83fd7
format: 13x13x15; ring: Q; encoding: sparse_flat_pairs
format eligibility: PASS (maximum dimension 15; excluded formats avoided)
structure: PASS (row counts, rational coefficients, unique indices, index bounds)
factor nonzeros: u=34649 v=40066 w=37933
terms: declared=1578 active=1578 zero=0
common denominator for tensor coefficients: 54400
exact integer contributions accumulated: 44460574
tensor coefficient equations per convention: 6426225
convention trace: w[l*n+i]: mismatches=102; tensor nonzeros=2635; expected nonzeros=2535
first mismatch (w index, u index, v index, scaled actual, scaled expected): (13, 0, 1, 108800, 54400)
convention output: w[i*p+l]: mismatches=5092; tensor nonzeros=2635; expected nonzeros=2535
first mismatch (w index, u index, v index, scaled actual, scaled expected): (1, 0, 1, 0, 54400)
rejection: no unique supported interpretation gives the multiplication tensor
NEGATIVE CONTROL PASS: tensor identity failure detected
```

Repeat commands (all exit 0):

```sh
python3 skeptic/check.py > skeptic/repeat_output.txt 2>&1
cmp skeptic/output.txt skeptic/repeat_output.txt
python3 verify-it-yourself/check_fmm_fast.py object/13x13x15_r1578_Q.json --expect-rank 1578 > skeptic/author_repeat_output.txt 2>&1
cmp skeptic/author_output.txt skeptic/author_repeat_output.txt
```

The complete repeat logs are skeptic/repeat_output.txt and skeptic/author_repeat_output.txt; they are byte-for-byte copies of the corresponding complete outputs pasted above. Additional saved hash and equality assertions produced skeptic/determinism_output.txt:

```text
Frozen independent checker, definition and first output: unchanged
Repeated independent output: byte-for-byte identical
Repeated author checker output: byte-for-byte identical
Both independent runs and both direct author runs exited 0
```

There is no disagreement between the independent checker and the author's checker on the original saved object. Every applicable property checkable from these saved files passed. The verdict below concerns that reproducibility scope.

pass: true
