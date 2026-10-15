context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Independent offline reproduction of `object/14x16x16_r2117_Q.json`.

Definition and criterion quoted from `CLAIM.md` follow. In angle-bracketed format notation and the Lille URL template I changed only the brackets to braces; in particular the template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html. All other wording is unchanged.

> Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format {n,m,p} with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

The bank's exact verification definition is:

> Parse the candidate scheme (JSON U, V, W integer/rational matrices, or a Maple-style product list as in the Lille *_raw.mpl files). With exact fractions/sympy, form the r products m_k = (sum_ij U_k,ij A_ij)*(sum_jl V_k,jl B_jl) and check that for every (i,l) sum_k W_k,il m_k equals the symbolic entry (A*B)_il with exact coefficients over the claimed ring (reduce mod p for GF(p)); equivalently check the Brent equations. Count r after dropping zero terms. Re-fetch fmm_sota.json, the Lille per-format page, Perminov's README (all three ZT/Z/Q columns) and MerlijnW70's repo, and compare against the sorted format (rank is invariant under axis permutation/transposition). For p2 also re-fetch COVERAGE.md and the GF(2) schemes. Whole check runs in minutes on a 10-core Mac even for 16x16x16.

I read `CLAIM.md`, the object, `INDEX.csv`, and `table-record/` first. I wrote `skeptic/check.py` and completed its first successful exhaustive run before opening any file in `verify-it-yourself/` or `REPRODUCE.md`. The checker was derived from the coefficient definition of matrix multiplication. It does not import or call the author's code. Its optimization from direct rational expansion to exact integer matrix multiplication was also completed before reading the author's code.

Properties checked and proof re-derived:

- Explicit object and decoding: JSON has no duplicate keys; every vocabulary coefficient is an integer or rational string parsed with `Fraction`; all RLE tokens, indices, repeat counts, expanded widths and row counts are validated. There are 2,117 rows in each of U, V and W, with widths 224, 256 and 224. The declared ring is Q. All terms have three nonzero factors, so dropping zero terms leaves exactly 2,117 rank-one terms.
- Eligible format: dimensions are exactly (14,16,16), their maximum is 16, and their sorted tuple is neither excluded tuple. The object agrees with the stated format and term count.
- Bilinear and non-commutative identity: for independent symbols A[i,j] and B[h,l], the coefficient of the ordered product A[i,j] B[h,l] in output C[s,t] must equal 1 precisely when i=s, j=h and l=t, and must otherwise equal 0. Expanding the ordered products preserves A before B, so coefficient equality also proves the non-commutative bilinear identity over Q.
- Exact scaling: the least common multiple of all nonzero coefficient denominators is 50,400. Multiplying each factor by this integer multiplies every tensor coefficient by 50,400 cubed, namely 128,024,064,000,000. This scaling is reversible over Q. For each output coordinate, the checker forms the full matrix U times the diagonal matrix of its W coefficients times V, restricted only to terms with nonzero W at that output. It uses `flint.fmpz_mat` arbitrary-precision integer multiplication, with no rounding, fixed-width overflow, modular test or sampling. This is exactly the sum of the original rank-one outer products after scaling.
- Exhaustive identity: all 224 output contractions are computed and every entry of each 224-by-256 contraction is inspected. The entire tensor has exactly 3,584 nonzero coefficients, each equal to the required scaled unit coefficient, and all remaining 12,841,472 coefficients are zero. Thus all 12,845,056 Brent equations hold, including zero targets. No inference is made from a sample or from the author's packed representation.
- Flattening: because `CLAIM.md` refers to the author's code for its convention, the independent checker initially considers all eight row/column-major choices for A, B and C. Exactly one satisfies the full identity: A row-major, B row-major, C column-major. After the independent run, the author's convention was read and confirmed to be exactly U[i*16+j], V[j*16+l], W[l*14+i]. The seven rejected coordinate interpretations are reported diagnostics, not discrepancies in the claimed convention.
- Saved identity and value: the SHA-256 matches `INDEX.csv`, as do its target id, format, object filename, claimed value and recorded bound. The rank-one term count 2,117 is strictly below the saved bound 2,128 by 11. `table-record/` reports 2,128 for both Lille sources and Q, and 2,170 for each of ZT and Z; the arithmetic minimum of these numerical metadata values is 2,128. It reports no matching Merlijn scheme and no trophy-case row.
- Scope: raw table responses are not saved, only fetch metadata and hashes. I do not authenticate those responses, judge whether any table value is current, decide novelty, or verify the live-refetch requirement; those are the other skeptic's remit. This verdict covers the explicit object, exact mathematical identity and saved-file consistency. The GF(2)-only and partial-win clauses do not apply to this Q object. No construction or provenance assertion is needed as a proof premise: the complete tensor identity is checked directly.
- Determinism: a second complete independent execution produced byte-for-byte identical output. Both executions exited 0. The checker uses no randomness, network, parallel scheduling assumptions or machine-sized coefficient arithmetic.

Exact independent command (the variable selects the Python interpreter authorized in the task without writing an absolute pathname):

```sh
PYTHON=$(python3 - <<'PY'
from pathlib import Path
print(Path.home() / 'v3r1t4s' / '.venv' / 'bin' / 'python')
PY
)
"$PYTHON" -u skeptic/check.py object/14x16x16_r2117_Q.json > skeptic/output.txt 2>&1
```

The same checker was run to `skeptic/output_repeat.txt`. The exact comparison command was:

```sh
cmp skeptic/output.txt skeptic/output_repeat.txt
```

The comparison exited 0 and printed nothing. The complete independent output below is inserted directly from `skeptic/output.txt`:

```text
object: object/14x16x16_r2117_Q.json
sha256: 9d6ef02f8162d9d5a53e56ecff6821459727c32d5a5fecb24283bd0c716fdf10
format: 14x16x16 ; ring: Q; encoding: vocab_rle_v1
rows decoded: 2117 2117 2117 ; widths: 224 256 224
nonzero rank-one terms: 2117 ; zero terms: 0
coefficient domain: exact fractions; vocabulary size: 496
nonzero factor entries: 160039 191929 157940
exact scalar contributions to expand: 6041804545
common denominator: 50400 ; tensor scale: 128024064000000
exact output contractions: 16 / 224
exact output contractions: 32 / 224
exact output contractions: 48 / 224
exact output contractions: 64 / 224
exact output contractions: 80 / 224
exact output contractions: 96 / 224
exact output contractions: 112 / 224
exact output contractions: 128 / 224
exact output contractions: 144 / 224
exact output contractions: 160 / 224
exact output contractions: 176 / 224
exact output contractions: 192 / 224
exact output contractions: 208 / 224
exact output contractions: 224 / 224
expanded tensor nonzero coefficients: 3584
layout A/B/C: row-major/row-major/row-major ; required entries wrong: 3552 ; unexpected nonzeros: 3552
layout A/B/C: row-major/row-major/column-major ; required entries wrong: 0 ; unexpected nonzeros: 0
layout A/B/C: row-major/column-major/row-major ; required entries wrong: 3582 ; unexpected nonzeros: 3582
layout A/B/C: row-major/column-major/column-major ; required entries wrong: 3360 ; unexpected nonzeros: 3360
layout A/B/C: column-major/row-major/row-major ; required entries wrong: 3582 ; unexpected nonzeros: 3582
layout A/B/C: column-major/row-major/column-major ; required entries wrong: 3552 ; unexpected nonzeros: 3552
layout A/B/C: column-major/column-major/row-major ; required entries wrong: 3568 ; unexpected nonzeros: 3568
layout A/B/C: column-major/column-major/column-major ; required entries wrong: 3582 ; unexpected nonzeros: 3582
verified ALL 12845056 tensor coefficients: 3584 unit coefficients and 12841472 zero coefficients
valid A/B/C layout: row-major/row-major/column-major
INDEX: target, format, object path, sha256, rank and recorded bound agree
saved bound comparison: 2117 < 2128; difference: 11
live record status and novelty: outside this offline reproduction review
INDEPENDENT EXACT OBJECT CHECK: PASS
```

Only after that first successful independent run, I read `REPRODUCE.md` and the author's checker. I re-derived its packed-integer argument: clearing denominators gives integer equations with target scale DU*DV*DW. Its bound is the sum over terms of the product of each factor's maximum absolute coefficient, so the triangle inequality bounds every resulting tensor coefficient. Its base is greater than twice both that bound and the target scale. If two bounded coefficient vectors packed to the same integer, their difference would have each coefficient strictly smaller in absolute value than the base; reducing modulo the base forces the lowest coefficient to be zero, and division followed by induction forces every coefficient to be zero. Consequently its packed comparison checks every slot exactly. Its loops cover every A/B index pair, including pairs absent from its accumulator. This independently justifies the proof steps used by the author rather than assuming its PASS message is sufficient.

I initially started the author's shell wrapper, then interrupted it before completion because its later negative-control branch uses temporary files outside this folder. I used the direct checker command below for the completed comparison. No result from the interrupted wrapper is used.

Exact completed author command:

```sh
python3 verify-it-yourself/check_fmm_fast.py object/14x16x16_r2117_Q.json --expect-rank 2117 > skeptic/author_output.txt 2>&1
```

The completed author command exited 0. Its full real output, inserted directly from `skeptic/author_output.txt`, is:

```text
exact integer check: D=26127360000 (DU=25200, DV=720, DW=1440), coefficient bound 49 bits, slot width 51 bits, 57344 blocks of 224 slots compared
PASS format=14x16x16 rank=2117
```

There is no mismatch between the independent exact result and the author's result. Both establish the same ordered bilinear tensor and the same nonzero term count. No missing object or nondeterminism was found. The differing denominator scales are harmless: the independent checker uses one common LCM for all factors, whereas the author uses a separate LCM for each factor.

pass: true
