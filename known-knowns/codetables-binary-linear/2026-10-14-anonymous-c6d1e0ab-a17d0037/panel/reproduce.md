# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

## Definition and success criterion checked

The claimed definition, quoted exactly from `CLAIM.md`:

> object/win_q2_n173_k17_d72.json is a 17 x 173 generator matrix over GF(2) of rank 17 whose linear code has minimum distance exactly 72, strictly above the codetables.de lower bound of 70 for (q, n, k) = (2, 173, 17).

The bank statement, quoted:

> For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256.

The complete success criterion, quoted so that its applicable clauses and scope are explicit:

> Success means a k x n generator matrix over GF(q) with these properties. (1) Rank is exactly k over GF(q), computed independently. (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible (2^k <= ~2^32), or, for large k (or large k with small n-k, via the dual and MacWilliams identities), by two independent exact minimum-distance implementations that agree; never by sampling. (3) d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/ cell for (q,n,k) at verification time, and at most the upper bound. (4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and no newer arXiv claim already reaches that d.

The prescribed verification method, quoted:

> Use an independent script. Compute rank by Gaussian elimination over GF(2) with numpy uint8 or bitset ints. For k <= 32, compute weights with a Gray-code walk over all codewords using XOR of packed rows (2^k * n/64 ops; k=22 takes seconds). For larger k, use two independent minimum-distance implementations (e.g. a custom Brouwer-Zimmermann plus pip 'galois' or 'ldpc' style tools) and require agreement. Look up the live table cell at codetables.de/BKLC/... for (n,k) and confirm the strict improvement. Then check arXiv for newer claims.

I checked the classical generator claim: the format and field, exact dimensions, exact rank, exhaustive exact minimum distance, and the arithmetic against the saved lower and upper bounds. I also checked the saved minimum-weight multiplicity, object digest, and agreement of saved index metadata. The alternative large-dimension, quantum-code, and non-existence criteria do not apply to this object.

I interpret a binary generator matrix as defining C = {uG : u in GF(2)^17}. Hamming weight counts its nonzero coordinates. For a linear code, differences of distinct codewords run through its nonzero codewords, so its minimum distance is the least nonzero Hamming weight. This is the operational mathematical definition used by my checker.

The live-table condition in clause (3) and the provenance/literature condition in clause (4) cannot be established from this package offline. I make no judgment about table currency or novelty, as instructed. The saved metadata comparison alone is 72 > 70 and 72 <= 77. Metadata and page hashes without their source pages do not independently authenticate those pages.

## Independence and proof reconstruction

I read `CLAIM.md`, the saved object, and `table-record/README.md`; then wrote `skeptic/check.py` before reading anything in `verify-it-yourself/` or the author's `REPRODUCE.md`. My completed exhaustive independent run was saved before I opened the author's code. No network was used and no files outside this package were inspected. Python runtime execution is implicit in the requested python3 command. Runtime version: Python 3.9.6. All artifacts and temporary data I created are within this folder.

1. Format and dimensions: strict JSON parsing rejects duplicate keys; the checker confirms the claimed metadata, 17 rows, 173 entries per row, and integer entries exclusively in {0,1}. Thus every row is in GF(2)^173 and every binary row combination is also in that vector space.
2. Rank: list-based Gaussian elimination swaps rows and XORs a pivot row into rows below. Each operation is invertible over GF(2), so it preserves rank. The 17 distinct pivot columns are 0 through 16. Therefore the row span has dimension exactly 17, and the coefficient-to-codeword map is injective.
3. Coverage: the independent checker visits every integer mask from 1 through 131071, exactly the 2^17 - 1 nonzero binary coefficient vectors. Each codeword is freshly formed by XORing its selected rows; no sample, probabilistic step, or early distance cutoff is used. The set contains 131071 distinct words and excludes zero, agreeing with the independent rank proof.
4. Coordinate cross-check: for every message and every one of the 173 columns, a second representation computes the binary dot product of the message and that column. All 131071 entire words agree with the independently assembled row sums. This cross-check covers all messages and coordinates, not a subset.
5. Exact distance: the exhaustive nonzero weight distribution is 72:6341, 80:39440, 88:59586, 96:23885, 104:1785, 112:34. It sums to 131071 and has no weight below 72. The word for message mask 7 (rows 0,1,2) has weight 72, providing an attaining witness; its full coordinates are in the pasted output. Thus the lower bound and attaining upper bound establish d = 72 exactly. Its multiplicity is 6341, equal to saved `A_d`.
6. Saved table arithmetic: the checker extracts the unique [173,17] GF(2) cell from `table-record/README.md`, with saved bounds 70 and 77. Exact integer comparison establishes the claimed strict saved improvement and upper-bound compatibility. `skeptic/check_index.py` separately parses `INDEX.csv`, verifies all its fields and the object's SHA-256, and checks agreement of its saved fetch timestamp.
7. Author comparison: after the independent exhaustive run, I inspected and ran the author's code. Its Gray-code update flips the row at the least-significant set bit of the step index: successive reflected binary Gray masks differ in exactly that bit. This visits every nonzero message once. Its second method reconstructs each word directly from each binary message. Both methods give d=72 and A_d=6341, agreeing with my enumeration. Its rank reduction uses XOR with previously stored pivot rows to remove a leading bit when doing so decreases the integer; those operations preserve span and yield 17 independent pivots. The wrapper also confirms the saved object digest and rejects its one-bit-altered copy because that copy has distance 71.
8. Determinism: my final checker was run twice, the author's standalone checker twice, and the complete author wrapper three times. My outputs and the standalone author's outputs are byte-identical within their respective repeated pairs. The second and third complete wrapper outputs are also byte-identical. The first wrapper includes two extra Xcode platform diagnostics, recorded below; removing exactly those two lines gives the same complete verification output. These are platform log messages, not changed enumeration results, random codewords, or changed object data. Every mathematical result agrees across all runs.

## Exact commands and actual output

All commands were executed from this package folder. The final independent checker and its repeat each exited 0:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
```

The full output below is inserted directly from `skeptic/output.txt`:

```text
object: object/win_q2_n173_k17_d72.json
sha256: a17d00378317979d9fe0acb452d3cce805f55cb17595a8407acb9b56b7b51a76
PASS metadata type: saved='classical', expected='classical'
PASS metadata q: saved=2, expected=2
PASS metadata n: saved=173, expected=173
PASS metadata k: saved=17, expected=17
PASS metadata d: saved=72, expected=72
PASS metadata d_lo_codetables: saved=70, expected=70
PASS metadata d_up_codetables: saved=77, expected=77
PASS metadata A_d: saved=6341, expected=6341
PASS matrix dimensions: rows=17, row_lengths=[173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173]
PASS GF(2) entries: invalid_entries=[]
PASS rank: rank=17, pivot_columns_zero_based=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
PASS exhaustive coverage: coefficient_vectors=131071, required=131071
PASS distinct nonzero codewords: distinct=131071, zero_generated=False
PASS independent column evaluation: full_word_disagreements=0, compared=131071
PASS exact minimum distance: computed=72, claimed=72
PASS minimum weight multiplicity: computed=6341, saved=6341
weight_distribution_nonzero_messages: {"72":6341,"80":39440,"88":59586,"96":23885,"104":1785,"112":34}
minimum_witness_message_mask: 7
minimum_witness_coefficients_row_order: 11100000000000000
minimum_witness_codeword_column_order: 11110110011110000001100000000111010011000101000110110100111001100000010100000000000001110111011101000001010111111011110010001001000011010110010110100001110011000001000000000
PASS saved table cell: extracted=[('70', '77')]
PASS strict saved lower-bound improvement: 72 > 70
PASS saved upper-bound compatibility: 72 <= 77
scope: live table currency and novelty excluded; saved metadata only
failed_properties: []
verdict: PASS
```

The author wrapper was run only after the independent checker completed. `TMPDIR` keeps its altered-object temporary files within this package:

```sh
mkdir -p skeptic/tmp
TMPDIR=skeptic/tmp sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
TMPDIR=skeptic/tmp sh verify-it-yourself/run_checks.sh > skeptic/author-output-repeat.txt 2>&1
TMPDIR=skeptic/tmp sh verify-it-yourself/run_checks.sh > skeptic/author-output-third.txt 2>&1
```

All three wrapper invocations exited 0. Full first-wrapper output, inserted directly from `skeptic/author-output.txt`:

```text
sha256 matches INDEX.csv (a17d00378317979d9fe0acb452d3cce805f55cb17595a8407acb9b56b7b51a76)
== check_code.py on object/win_q2_n173_k17_d72.json
2026-10-14 10:44:04.684 xcodebuild[65550:69761657]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-14 10:44:05.613 xcodebuild[65550:69761656] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
gray-code walk: d=72 A_d=6341; direct enumeration: d=72 A_d=6341
PASS code=[173,17,72]_2 rank=17 A_d=6341 codewords_enumerated=131071
== negative control: a corrupted copy must FAIL
negative control rejected as expected (FAIL minimum distance 71 != expected 72)
ALL CHECKS PASS
```

Full second-wrapper output, inserted directly from `skeptic/author-output-repeat.txt`; the third run is byte-identical:

```text
sha256 matches INDEX.csv (a17d00378317979d9fe0acb452d3cce805f55cb17595a8407acb9b56b7b51a76)
== check_code.py on object/win_q2_n173_k17_d72.json
gray-code walk: d=72 A_d=6341; direct enumeration: d=72 A_d=6341
PASS code=[173,17,72]_2 rank=17 A_d=6341 codewords_enumerated=131071
== negative control: a corrupted copy must FAIL
negative control rejected as expected (FAIL minimum distance 71 != expected 72)
ALL CHECKS PASS
```

The author's standalone checker was separately repeated; both commands exited 0:

```sh
python3 verify-it-yourself/check_code.py object/win_q2_n173_k17_d72.json --expect-d 72 > skeptic/author-checker-output.txt 2>&1
python3 verify-it-yourself/check_code.py object/win_q2_n173_k17_d72.json --expect-d 72 > skeptic/author-checker-output-repeat.txt 2>&1
```

Full standalone output, inserted directly from `skeptic/author-checker-output.txt`:

```text
gray-code walk: d=72 A_d=6341; direct enumeration: d=72 A_d=6341
PASS code=[173,17,72]_2 rank=17 A_d=6341 codewords_enumerated=131071
```

Supplementary saved-file consistency check (exit 0):

```sh
python3 skeptic/check_index.py > skeptic/index-output.txt 2>&1
```

Actual output inserted directly from `skeptic/index-output.txt`:

```text
PASS INDEX.csv: one row; target, cell, claimed value, saved lower bound, fetch timestamp and object filename agree with package metadata.
PASS INDEX.csv object sha256: a17d00378317979d9fe0acb452d3cce805f55cb17595a8407acb9b56b7b51a76
PASS saved table timestamp agrees with INDEX.csv; no live source consulted.
Documentation reference verify-it-yourself/RECEIPTS.md: present=False
Documentation reference how-we-built-it: present=False
The claimed generator object and both checker source files are present.
```

The byte comparisons and cross-check assertions were captured in `skeptic/comparison.txt`. Actual output:

```text
skeptic/output.txt == skeptic/output-repeat.txt: True
output sha256: 7bdaa3de472cac181ead770819ab2313440cae53a6794f1668f846b69ff5bc8e
skeptic/author-checker-output.txt == skeptic/author-checker-output-repeat.txt: True
output sha256: fe213fcec9bea2775c19fc894e5cf4a83cf83caa315c97c5c46250e1af400f53
skeptic/author-output-repeat.txt == skeptic/author-output-third.txt: True
output sha256: f6ad8eafb7f48c7d2cef1095445e7bde4e52d94b2938d0fa78d3497ec3007ab1
Initial wrapper extra platform diagnostics:
2026-10-14 10:44:04.684 xcodebuild[65550:69761657]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-14 10:44:05.613 xcodebuild[65550:69761656] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
Initial wrapper differs only by these two platform diagnostics; all verification result lines agree.
Independent and author results agree: n=173, k=17, q=2, rank=17, d=72, A_d=6341, nonzero codewords=131071.
Determinism: independent checker, author checker, and two subsequent complete wrapper runs are byte-identical within each repeated pair.
```

## Initial checker correction and documentation gaps

My initial invocation was the same independent command shown above, but initially used `int.bit_count()`, which Python 3.9.6 does not provide. It exited 1 before enumeration. Before reading the author's code, I replaced that operation with the exact equivalent `bin(value).count("1")` and reran the entire checker successfully. The initial failed output is preserved in `skeptic/output-initial-python3.txt`, pasted directly here:

```text
object: object/win_q2_n173_k17_d72.json
sha256: a17d00378317979d9fe0acb452d3cce805f55cb17595a8407acb9b56b7b51a76
PASS metadata type: saved='classical', expected='classical'
PASS metadata q: saved=2, expected=2
PASS metadata n: saved=173, expected=173
PASS metadata k: saved=17, expected=17
PASS metadata d: saved=72, expected=72
PASS metadata d_lo_codetables: saved=70, expected=70
PASS metadata d_up_codetables: saved=77, expected=77
PASS metadata A_d: saved=6341, expected=6341
PASS matrix dimensions: rows=17, row_lengths=[173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173]
PASS GF(2) entries: invalid_entries=[]
PASS rank: rank=17, pivot_columns_zero_based=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
FAIL exception: AttributeError: 'int' object has no attribute 'bit_count'
verdict: FAIL
```

The author's `REPRODUCE.md` refers to `verify-it-yourself/RECEIPTS.md` and `how-we-built-it/`, which are absent. Those documentation references are not evidence of construction reproducibility, and I have not reproduced the discovery search or validated the construction/provenance label. The package explicitly says its claim rests on the saved object and checker; the claimed generator object is present and its defining mathematical properties are established without search-history files. This report supplies fresh verification receipts. None of those absent references is required to enumerate this generator's entire code.

There is no disagreement about the generator's dimensions, rank, minimum distance, multiplicity, or saved-bound arithmetic. No mathematical non-determinism was observed; the first wrapper's platform diagnostic difference is fully disclosed. The pass below is limited to the requested saved-object reproduction scope and does not certify the live table or novelty.

pass: true
