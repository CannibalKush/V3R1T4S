REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved object independently reproduces an exact 11 x 13 by 13 x 16 bilinear matrix multiplication scheme over Q with 1,445 nonzero rank-one terms. All 5,234,944 tensor equations match. No mismatch or mathematical nondeterminism was found.

Scope and order: I read CLAIM.md and the object, recorded the definition in skeptic/definition.txt, and wrote skeptic/check_independent.py before reading any file in verify-it-yourself/ or REPRODUCE.md. The first exhaustive run completed successfully and was saved to skeptic/output.txt before those files were opened. Only this folder was used as evidence; no network was used. No external code or source scheme was imported. The checker uses Python's standard library. The input object and author's files were not modified.

The full success criterion is quoted below. I changed only the brackets in symbolic angle-bracket notation to braces, including the Lille URL template https://fmm.univ-lille.fr/{n}x{m}x{p}.html. The inequality <= is unchanged.

> Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format {n,m,p} with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

The verification definition quoted from CLAIM.md:

> Parse the candidate scheme (JSON U, V, W integer/rational matrices, or a Maple-style product list as in the Lille *_raw.mpl files). With exact fractions/sympy, form the r products m_k = (sum_ij U_k,ij A_ij)*(sum_jl V_k,jl B_jl) and check that for every (i,l) sum_k W_k,il m_k equals the symbolic entry (A*B)_il with exact coefficients over the claimed ring (reduce mod p for GF(p)); equivalently check the Brent equations. Count r after dropping zero terms. Re-fetch fmm_sota.json, the Lille per-format page, Perminov's README (all three ZT/Z/Q columns) and MerlijnW70's repo, and compare against the sorted format (rank is invariant under axis permutation/transposition). For p2 also re-fetch COVERAGE.md and the GF(2) schemes. Whole check runs in minutes on a 10-core Mac even for 16x16x16.

Properties checked and the independent derivation:

| Property | Check and result |
|---|---|
| Explicit saved scheme | object/11x13x16_r1445_Q.json exists, parses as JSON, and supplies all u, v, w rows. No required candidate object is missing. |
| Eligible format | Dimensions equal [11, 13, 16], are positive integers, have maximum 16, and the sorted tuple is neither excluded format. |
| Encoding and coefficient validity | sparse_flat_pairs; even row lengths; integer indices in bounds; no duplicate index in a row; exact integer or rational values; nonzero denominators. Floats and Boolean coefficients are rejected. |
| Claimed ring | ring is Q. Arithmetic uses Python integers and Fraction, with no floating point or numerical tolerance. There are 7,657 nonintegral coefficients. |
| Flattening | Independently selected u[i*13+j], v[j*16+l], w[l*11+i], then verified that the author specifies exactly the same convention. |
| Claimed value | All three matrices have 1,445 rows. Every term has three nonzero factors. Dropping zero terms therefore leaves r=1,445. This counts the explicit decomposition; it does not claim a lower bound on minimum tensor rank. |
| Every bilinear equation | Expand all 3,951,738 sparse triple contributions, then visit all 143*208*176=5,234,944 possible coefficients, including zeros. Exactly 2,288 equal 1; all others equal 0. No sample or random evaluation was used. |
| Noncommutative bilinearity | Each product keeps the A linear form first and the B linear form second. The exhaustive comparison checks ordered monomials A[i,j]B[t,l]. No commutation assumption is used. |
| File identity | Object SHA-256 agrees with INDEX.csv. INDEX target, format, file, rank, saved table value, and fetch timestamp agree with the saved metadata. |
| Saved comparison arithmetic | Digest 1,446; Lille 1,446; Perminov ZT/Z/Q 1,458/1,458/1,446. Their saved numerical minimum is 1,446, and 1,445 is strictly below each. Saved CHANGELOG value is also 1,446. Merlijn metadata says no scheme for this format. |
| GF(2) condition and partial wins | GF(2)-only condition is inapplicable: the identity is proved over Q. The format is within 16, so p1 is inapplicable; this is not a p2 claim. |
| Existing-rank and additions-only exclusions | The saved rank is one below every saved numeric baseline, rather than equal to a saved baseline. The checked claim concerns multiplication terms, not addition counts. Historical completeness and whether any construction was already listed require source evidence and belong to the table/novelty skeptic. |
| Determinism and agreement | Independent exhaustive runs have byte-identical output. Author direct runs have byte-identical output. Both confirm the same format and value. The author's altered-coefficient negative control is rejected. |

For the independent proof, write C[h,s] = sum_k w[k,s*11+h] (sum_i,j u[k,i*13+j] A[i,j]) (sum_t,l v[k,t*16+l] B[t,l]). Distributing gives the coefficient sum_k u[k,i*13+j]v[k,t*16+l]w[k,s*11+h] for each ordered monomial. Matrix multiplication requires that coefficient to equal 1 exactly when i=h, j=t, and l=s, and 0 otherwise. The independent checker computes those sums exactly and checks every possible index combination. This is a direct proof of the entire identity and needs no assumption about how the object was constructed.

The author's modular proof was re-derived independently in skeptic/audit_saved_evidence.py, without importing the author's code. The denominator lcm is D=8 and S=sum_k max|u_k| max|v_k| max|w_k|=5595/4. For any tensor coefficient residual R, D^3 R is an integer and |D^3 R| is at most D^3(S+1)=716672. The single modulus is P=2305843009213693951=2^61-1. Trial division proves 61 prime; 59 Lucas-Lehmer iterations give residue zero, proving P prime. gcd(P,D)=1, so all rational coefficients reduce unambiguously modulo P. The author's exhaustive coefficient calculation reports zero residuals modulo P, so each D^3 R is divisible by P. Since P exceeds 2*716672, the only possible such integer is zero. Thus the modular proof is exact. The independent rational expansion separately confirms the result without relying on that modular calculation.

The object's note attributes its construction to slicing and absorbing a 12x13x16 rank-1509 scheme. That parent scheme and a derivation transcript are not saved, so I do not reproduce that provenance assertion. Neither is needed for the direct exhaustive proof of the supplied object's identity and term count. No candidate search or exhaustive-search claim is supplied; the exhaustive claim here is the verification of every tensor equation, which was fully reproduced.

The saved table-record/README.md explicitly contains metadata only. It does not contain fetched pages, a repository tree, or the Lille construction column. I confirm arithmetic and internal consistency of the saved assertions only. I make no judgment about table currency, completeness, whether GETs happened at the stated times, absence of a Merlijn scheme, construction history, or novelty. The other skeptic must evaluate those source assertions. This pass is the REPRODUCE verdict on properties checkable from the saved package, not a verdict that the overall target is a current record.

Exact commands, run from this folder:

```sh
python3 skeptic/check_independent.py object/11x13x16_r1445_Q.json > skeptic/output.txt 2>&1
python3 skeptic/check_independent.py object/11x13x16_r1445_Q.json > skeptic/output_repeat.txt 2>&1
TMPDIR=skeptic sh verify-it-yourself/run_checks.sh > skeptic/author_output.txt 2>&1
python3 verify-it-yourself/check_fmm.py object/11x13x16_r1445_Q.json --expect-rank 1445 > skeptic/author_direct_output.txt 2>&1
python3 verify-it-yourself/check_fmm.py object/11x13x16_r1445_Q.json --expect-rank 1445 > skeptic/author_direct_repeat.txt 2>&1
python3 skeptic/audit_saved_evidence.py > skeptic/audit_output.txt 2>&1
```

Every command exited 0. The author shell run creates its temporary negative-control copy inside skeptic/ because TMPDIR is set to that relative directory; it removes that copy afterward. The independent first run occurred before the author shell run. The independent repeat and author shell run were independent concurrent operations after author inspection. The last audit was run after the direct repeats.

Real first independent output, inserted directly from skeptic/output.txt:

```text
object: object/11x13x16_r1445_Q.json
sha256: d2d1c96812918b46fa34436c66cdd27e51383b12a9686a975d715d69e6480c75
format: 11 x 13 x 16; sorted format: (11, 13, 16)
dimension bound and excluded-format checks: PASS
ring: Q; all coefficients parsed as exact integers or fractions
encoding, row counts, index bounds, and unique sparse indices: PASS
flattening: u[i*13+j], v[j*16+l], w[l*11+i]
declared terms: 1445; nonzero rank-one terms: 1445; zero terms: 0
nonzero coefficient counts: u=15901, v=17058, w=15143
nonintegral coefficients: 7657
exact expanded triple contributions: 3951738
exhaustively checked tensor equations: 5234944
expected nonzero coefficients: 2288; actual nonzero coefficients: 2288
coefficient mismatches: 0
ordered bilinear identity over Q, including every zero coefficient: PASS
claimed value r=1445: PASS
independent object check: PASS
```

Real author shell output, inserted directly from skeptic/author_output.txt:

```text
sha256 matches INDEX.csv (d2d1c96812918b46fa34436c66cdd27e51383b12a9686a975d715d69e6480c75)
== check_fmm.py on object/11x13x16_r1445_Q.json
2026-10-14 11:23:57.496 xcodebuild[1846:69979266]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-14 11:23:57.931 xcodebuild[1846:69979265] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
Brent equations hold modulo 1 primes whose product exceeds 2 * D^3 * (S + 1) (D = 8, S = 5595/4); hence exactly over Q
PASS format=11x13x16 rank=1445 max_den=8
== negative control: a copy with one coefficient changed must FAIL
negative control rejected as expected (FAIL 24 Brent equations violated modulo p = 2305843009213693951)
ALL CHECKS PASS
```

The two Xcode diagnostics above were emitted by the system launcher during the shell run. They are preserved unedited. They did not affect either checker's mathematical result or exit status; the repeated direct checker outputs below are identical.

Real author direct output, inserted directly from skeptic/author_direct_output.txt:

```text
Brent equations hold modulo 1 primes whose product exceeds 2 * D^3 * (S + 1) (D = 8, S = 5595/4); hence exactly over Q
PASS format=11x13x16 rank=1445 max_den=8
```

Real independent evidence-audit output, inserted directly from skeptic/audit_output.txt:

```text
independently recomputed denominator lcm D: 8
independently recomputed coefficient bound S: 5595/4
2 * D^3 * (S + 1): 1433344
prime: 2305843009213693951; exponent 61 trial-division primality: PASS
Lucas-Lehmer iterations: 59; final residue: 0; prime proof: PASS
gcd(prime, D): 1; prime exceeds residual uniqueness threshold: PASS
author arithmetic bound, format, rank, and negative-control run agree: PASS
independent exhaustive run repeated: byte-for-byte identical output, PASS
author direct checker repeated: byte-for-byte identical output, PASS
INDEX.csv target, format, object path, rank, and object SHA-256: PASS
saved numeric metadata: digest=1446, Lille=1446, Perminov ZT/Z/Q=(1458, 1458, 1446), changelog=1446
saved minimum=1446; claimed rank=1445; strict improvement=1: PASS
Merlijn metadata asserts no scheme; repository tree and source pages are not saved
table-source currency, completeness, construction history, and novelty: delegated, no judgment
saved-evidence and proof audit: PASS
```

Mismatch assessment: none for the unchanged object, format, term count, exact coefficient tensor, hash, saved numerical comparison, or proof bound. The deliberately modified author negative control has 24 violated equations, as expected. The metadata-only limitations above are explicitly outside this reproduction verdict.

pass: true
