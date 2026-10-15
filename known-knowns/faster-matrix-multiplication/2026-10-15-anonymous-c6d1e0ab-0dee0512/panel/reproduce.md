# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object is an exact rational bilinear matrix-multiplication scheme for (15,16,16), with 2176 nonzero rank-one terms. All 14,745,600 Brent equations passed independently. The author's checker agrees. The numerical improvement over the minimum recorded in the saved metadata is 4.

This report concerns reproducibility from the saved files. I make no judgment about table currentness or novelty. No network was used and no external claim package or author working tree was read. The supplied Python interpreter was used through its relative path. All generated artifacts are in `skeptic/`.

The definition checked, quoted from `CLAIM.md`:

> Parse the candidate scheme (JSON U, V, W integer/rational matrices, or a Maple-style product list as in the Lille *_raw.mpl files). With exact fractions/sympy, form the r products m_k = (sum_ij U_k,ij A_ij)*(sum_jl V_k,jl B_jl) and check that for every (i,l) sum_k W_k,il m_k equals the symbolic entry (A*B)_il with exact coefficients over the claimed ring (reduce mod p for GF(p)); equivalently check the Brent equations. Count r after dropping zero terms. Re-fetch fmm_sota.json, the Lille per-format page, Perminov's README (all three ZT/Z/Q columns) and MerlijnW70's repo, and compare against the sorted format (rank is invariant under axis permutation/transposition). For p2 also re-fetch COVERAGE.md and the GF(2) schemes. Whole check runs in minutes on a 10-core Mac even for 16x16x16.

The full success criterion, quoted from `CLAIM.md`, so that all clauses and scope limits are explicit. I changed only the brackets: angle brackets around the symbolic format and in the Lille URL template are braces. In particular the URL is https://fmm.univ-lille.fr/{n}x{m}x{p}.html. Inequality signs and all other wording are unchanged.

> Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format {n,m,p} with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

I read `CLAIM.md` and the object metadata, then wrote `skeptic/definition.md` and `skeptic/check_scheme.py` before reading anything in `verify-it-yourself/`. I ran the independent checker to completion and saved its full output before inspecting or running the author code. The independent checker imports no author code. A later correction to `skeptic/definition.md` restored inequality signs affected by its initial bracket substitution; neither the algorithm nor the checker was changed after author inspection.

Properties checked and methods:

- Explicit object and identity: `object/15x16x16_r2176_Q.json` exists, parses, and its SHA256 agrees with `INDEX.csv`. The index contains one matching target, sorted format, rank and file entry.
- Encoding and rational ring: independently decode every `vocab_rle_v1` token; validate every vocabulary index, positive repeat count, row length and term count. Every coefficient is parsed as an exact `Fraction` from an integer or rational string. There are 2176 rows of widths 240, 256 and 240. The declared ring is Q.
- Eligible format: dimensions are (15,16,16), their maximum is 16, and their sorted tuple is neither excluded format.
- Term count: each of all 2176 terms has three nonzero factors, so dropping zero terms leaves 2176. This certifies a scheme of that length, without asserting a lower bound on the minimal tensor rank.
- Complete noncommutative product identity: expand in the ordered basis A[i,j] B[j2,l]. The coefficient in C[i2,l2] must be 1 exactly when j=j2, i=i2 and l=l2, otherwise 0. All 240 output coordinates and all 240*256 ordered input pairs are checked, including all required zeros. Input storage is U[i*16+j] and V[j*16+l]; output storage is W[l*15+i]. Before reading the author's convention I tested both ordinary and transposed output storage. Only transposed storage passes. The rejected alternative is an indexing diagnostic, not a disagreement about the actual object.
- Exactness over Q: let D=2100, the independently computed LCM of every denominator. Scaling each factor by D gives integer coefficients and target D^3. Each integer residual has absolute value at most B=sum_k max|DU_k| max|DV_k| max|DW_k| + D^3 = 3199497484470000. The checker verifies every residual modulo three distinct primes, found by deterministic exhaustive trial division: 16777213, 16777199 and 16777183. Their product M=4722351564707808147821 exceeds B. A residual divisible by M and of magnitude smaller than M must be zero. Thus these are exact rational identities, not probabilistic or finite-field-only evidence. NumPy uses only int64 arithmetic: individual modular products and the dot-product bound 2176*(prime-1)^2 are checked against the int64 limit; no floating-point operations or overflow are used.
- Saved numeric comparison: independently parse `table-record/README.md` and `INDEX.csv`. The saved ranks are digest 2223, Lille 2262, Perminov ZT/Z/Q 2302/2302/2223, and trophy case 2180. Each exceeds 2176 and the saved minimum is 2180. Merlijn metadata reports no scheme; it supplies no numeric rank. These are consistency checks of saved statements, not independent verification of source response bodies.
- Author proof audit: independently recompute DU=60, DV=60, DW=2100, target scaling 7560000, coefficient bound 2611827121200, and slot width 44. In base R=2^44=17592186044416, every residual digit has magnitude at most 2611834681200, smaller than R/2. If a packed residual had a highest nonzero digit at position h, its magnitude contribution would be at least R^h, whereas the combined lower positions would have magnitude smaller than R^h by the geometric-series bound. They cannot cancel. Packed equality therefore implies equality of every slot. The author's loop covers all 61440 input pairs, each with 240 slots, including untouched pairs. This re-derives its packing proof rather than assuming it.
- Controls and determinism: a single U[0,0] change from -2 to -1 preserves all 2176 nonzero terms but fails actual coefficient equations. The author's removed-term control also fails. Repeating the independent checker gives byte-identical full output; repeating the author's run with the supplied interpreter also gives byte-identical output. Both repetitions and both comparisons exited 0. No randomness, sampling, timing-dependent calculation or network enters either mathematical verification.

The GF(2)-only condition and enumerated partial wins do not apply: the scheme is certified over Q and its maximum dimension is 16. The saved metadata numerically supports a smaller rank rather than an equal-rank ring or addition-count change. Whether a construction or an earlier source already attained this rank, repository completeness, the authenticity of recorded source digests, and the required live fetches cannot be established from metadata-only records. Those are left to the other skeptic as instructed. The parent object named in the object's provenance note is not supplied; the claimed final scheme is self-contained and its identity does not depend on trusting that provenance or a construction history. There is no claimed exhaustive search to reproduce; the algebraic verification itself is exhaustive.

Exact independent command (exit 0); the relative executable is the user-supplied interpreter:

```sh
../../../.venv/bin/python skeptic/check_scheme.py object/15x16x16_r2176_Q.json > skeptic/output.txt 2>&1
```

Full captured `skeptic/output.txt`:

```text
Independent exhaustive rational matrix-multiplication checker
object: object/15x16x16_r2176_Q.json
sha256: 0dee0512255d74595673fd8bfa0df20b0ab0a87785b2d11cbb2a94f6dbd5d57c
dimensions: (15, 16, 16) ; ring: Q; encoding: vocab_rle_v1
stored terms: 2176 ; nonzero rank-one terms: 2176
nonzero coefficients U,V,W: (66132, 73799, 46470)
common denominator D: 2100
integer residual absolute bound B: 3199497484470000
coefficient equations per prime: 14745600
prime 16777213 ; mismatched equations: {'row-major output': 7616, 'transposed output': 0}
prime 16777199 ; mismatched equations: {'row-major output': 7616, 'transposed output': 0}
prime 16777183 ; mismatched equations: {'row-major output': 7616, 'transposed output': 0}
distinct-prime product M: 4722351564707808147821
M > B: True ; primes: 3
valid output storage: transposed output
input storage: U[i*m+j]=A[i,j], V[j*p+l]=B[j,l]
output storage: W[l*n+i] contributes to C[i,l]
ALL rational Brent equations certified exactly; no sampling.
claim term comparison: 2176 < 2180 = True
algebra_pass: true
```

Exact repeat and comparison command (exit 0, comparison emits no output):

```sh
../../../.venv/bin/python skeptic/check_scheme.py object/15x16x16_r2176_Q.json > skeptic/output-repeat.txt 2>&1 && cmp skeptic/output.txt skeptic/output-repeat.txt
```

Exact metadata command (exit 0):

```sh
python3 skeptic/check_metadata.py > skeptic/metadata-output.txt 2>&1
```

Full captured `skeptic/metadata-output.txt`:

```text
INDEX.csv: one row; target, sorted format, rank, object path and SHA256 agree
fmm_sota.json digest (createdAt 2026-10-09T11:45:48): 2223
Lille per-format page: 2262
Perminov README status table: 2302, 2302, 2223
MerlijnW70 fmm-schemes (repository tree): saved metadata reports no scheme
V3R1T4S TROPHY_CASE.md: 2180
minimum of saved numeric values: 2180
2176 < each saved numeric rank: True; improvement over saved minimum: 4
Saved response bodies are absent; HTTP/digest/cell provenance and live freshness are not verified.
metadata_consistency_pass: true
```

Exact author command using the supplied interpreter (exit 0). TMPDIR keeps its temporary control inside `skeptic/`:

```sh
PATH="../../../.venv/bin:$PATH" TMPDIR=skeptic sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
```

Full captured `skeptic/author-output.txt`:

```text
sha256 matches INDEX.csv (0dee0512255d74595673fd8bfa0df20b0ab0a87785b2d11cbb2a94f6dbd5d57c)
== check_fmm_fast.py on object/15x16x16_r2176_Q.json
exact integer check: D=7560000 (DU=60, DV=60, DW=2100), coefficient bound 42 bits, slot width 44 bits, 61440 blocks of 240 slots compared
PASS format=15x16x16 rank=2176
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=15x16x16 rank=2175: 4147 of 61440 (a, b) blocks differ; first at A[0][0] x B[0][0])
ALL CHECKS PASS
```

Exact author repeat and comparison command (exit 0, comparison emits no output):

```sh
PATH="../../../.venv/bin:$PATH" TMPDIR=skeptic sh verify-it-yourself/run_checks.sh > skeptic/author-repeat-output.txt 2>&1 && cmp skeptic/author-output.txt skeptic/author-repeat-output.txt
```

Exact independent packing-audit and coefficient-control command (exit 0):

```sh
../../../.venv/bin/python skeptic/check_controls.py > skeptic/control-output.txt 2>&1
```

Full captured `skeptic/control-output.txt` (the embedded negative object's exit 1 is the intended rejection):

```text
Independently re-derived author packing constants:
DU,DV,DW: (60, 60, 2100)
D: 7560000 ; coefficient bound: 2611827121200 ; bound bits: 42 ; slot width: 44
base R: 17592186044416 ; residual coefficient bound: 2611834681200
Residual bound < R/2: True. Highest nonzero digit cannot be cancelled by lower digits.
61440 input pairs x 240 output slots = 14745600 coefficient equations.
Independent checker repeated: byte-identical full output.
Negative control: change U[0,0] from -2 to -1 ; preserve dimensions and all 2176 nonzero terms.
Independent exhaustive rational matrix-multiplication checker
object: skeptic/negative-coefficient.json
sha256: d93e1bab174ea451b1d27fb5361b012b39ebf1aa336eb711a548554e0e5509c4
dimensions: (15, 16, 16) ; ring: Q; encoding: vocab_rle_v1
stored terms: 2176 ; nonzero rank-one terms: 2176
nonzero coefficients U,V,W: (66132, 73799, 46470)
common denominator D: 2100
integer residual absolute bound B: 3199497484470000
coefficient equations per prime: 14745600
prime 16777213 ; mismatched equations: {'row-major output': 8013, 'transposed output': 399}
first mismatches (prime,a,b,c,actual,expected): {'row-major output': (16777213, 0, 0, 1, 16755637, 0), 'transposed output': (16777213, 0, 0, 1, 16755637, 0)}
FAIL: ValueError: neither tested indexing convention satisfies all equations
algebra_pass: false
Coefficient-corruption control rejected on actual Brent equations: True
control_pass: true
```

For completeness, the first author run used system `python3` and emitted timestamped host Xcode startup diagnostics on stderr. Its mathematical output agreed. These host diagnostics are absent with the supplied interpreter; both controlled author runs are byte-identical. The initial command was:

```sh
TMPDIR=skeptic sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
```

That original capture was preserved as `skeptic/author-system-output.txt` before the controlled rerun. Its full actual output is:

```text
sha256 matches INDEX.csv (0dee0512255d74595673fd8bfa0df20b0ab0a87785b2d11cbb2a94f6dbd5d57c)
== check_fmm_fast.py on object/15x16x16_r2176_Q.json
2026-10-15 03:15:00.580 xcodebuild[12251:73653398]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 03:15:00.880 xcodebuild[12251:73653397] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
exact integer check: D=7560000 (DU=60, DV=60, DW=2100), coefficient bound 42 bits, slot width 44 bits, 61440 blocks of 240 slots compared
PASS format=15x16x16 rank=2176
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=15x16x16 rank=2175: 4147 of 61440 (a, b) blocks differ; first at A[0][0] x B[0][0])
ALL CHECKS PASS
```

No disagreement between the independent and author checkers was found. No claimed final object is missing. All object properties checkable here and the internal saved-value comparisons pass; live-source and novelty judgments are outside this report's scope.

pass: true
