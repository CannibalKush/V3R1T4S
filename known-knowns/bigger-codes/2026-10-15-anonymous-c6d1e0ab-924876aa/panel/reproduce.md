# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The saved generator passes the independently checked mathematical claim: it generates a binary [213,26,77] code. The complete enumeration has 67,108,863 nonzero words, including exactly 1,170 of weight 77. This verdict concerns reproducibility from the saved files. Live table currency and novelty are left to the other skeptics.

## Quoted definition and criterion

From `CLAIM.md`, the claimed object and value:

> object/code_q2_n213_k26_d77.json is a 26 x 213 generator matrix over GF(2) of rank 26 whose linear code has minimum distance exactly 77, strictly above the codetables.de lower bound of 76 for (q, n, k) = (2, 213, 26).

The bank statement:

> For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256.

The full success criterion (including the clauses outside this skeptic's offline remit):

> Success means a k x n generator matrix over GF(q) with these properties. (1) Rank is exactly k over GF(q), computed independently. (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible (2^k <= ~2^32), or, for large k (or large k with small n-k, via the dual and MacWilliams identities), by two independent exact minimum-distance implementations that agree; never by sampling. (3) d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/ cell for (q,n,k) at verification time, and at most the upper bound. (4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and no newer arXiv claim already reaches that d.

Quote-format note: the Lille URL template, if present, is written as `https://fmm.univ-lille.fr/{n}x{m}x{p}.html`, changing only the brackets. The supplied criterion contains no Lille URL template, so its quoted text needed no such change.

The saved-file clauses checked are the generator's dimensions and field, criterion (1), the full-enumeration branch of criterion (2), and the numerical comparison in criterion (3) against the saved bounds. Criterion (3)'s live-time condition and criterion (4)'s novelty and provenance conditions require outside evidence; neither is adjudicated here. The quantum-code and upper-bound partial wins are not claimed in this package.

## Independence and coverage

I read `CLAIM.md` and the JSON object, then wrote `skeptic/check.py` before inspecting `verify-it-yourself/` or `REPRODUCE.md`. The definition and proof plan are also saved in `skeptic/definition.md`. I completed the independent exhaustive run and saved `skeptic/output.txt` before opening the author's checker. The independent checker uses only Python's standard library and does not import or execute author code. No network was used. Package data and generated artifacts were read and written within this folder.

| Property | Independent check and result |
|---|---|
| Explicit saved object | `object/code_q2_n213_k26_d77.json` parses with duplicate JSON keys rejected. Its SHA-256 matches `INDEX.csv`. |
| Matrix and field | Exactly 26 rows, each exactly 213 entries; every entry has integer type and is 0 or 1. |
| Dimension | Gaussian elimination using highest-bit pivots gives rank 26 over GF(2). |
| Exhaustive coverage | Every one of the 2^26 - 1 = 67,108,863 nonzero messages is visited. None produces the zero codeword. |
| Exact distance | The minimum population count is 77; the full weight distribution is saved and pasted below. |
| Attainment | A weight-77 witness is independently reconstructed coordinate by coordinate from the original matrix entries and message `0x115c`. Its support has 77 positions. |
| Enumeration consistency | The histogram totals 67,108,863. All 213 columns are active. Its first moment is 7,147,094,016 = 213 times 2^25. |
| Determinism | A second complete independent run produces byte-identical output. |
| Author agreement | Both author's complete enumerations give distance 77 and multiplicity 1,170; the author's hash check and rank-deficient negative control pass. |
| Saved table arithmetic | `table-record/README.md` records 76 and 90; 76 is strictly less than 77, which is at most 90. Its cell and timestamp agree with `INDEX.csv`. |

## Re-derived proof steps

Packing coordinate j into bit j identifies GF(2) vector addition with integer XOR. During independent elimination, XORing an existing pivot row preserves the span. Each retained remainder has a previously unused highest pivot. Such remainders are linearly independent: in any nonempty combination, the highest pivot appearing cannot cancel. All original rows reduce into their span, so the 26 retained rows prove rank exactly 26. Consequently the map from 26-bit messages to generated codewords is injective, with 2^26 codewords.

The reflected Gray message g(i) = i XOR (i shifted right by one bit) is invertible: XOR g(i) with all its successive right shifts to recover i. The intermediate shifted terms cancel in pairs, leaving i. It therefore bijects all 26-bit messages. If t is the trailing-zero count of i, then i XOR (i-1) consists of t+1 low bits set. XORing that mask with its right shift leaves only bit t. Applying the Gray definition shows that g(i) XOR g(i-1) is exactly that single bit. Starting at the zero word and XORing the corresponding generator row thus produces precisely the word for g(i). The loop includes every integer i from 1 through 2^26 - 1; it omits only the zero message and is exhaustive. Rank 26 guarantees no duplicates and no zero word in this enumeration.

For a linear code, the difference of two distinct words is a nonzero codeword, and every nonzero word is the difference of itself and zero. Hamming distance is the weight of that difference. Thus the minimum enumerated nonzero weight proves a lower bound of 77 on all pairwise distances. The directly reconstructed witness of weight 77 proves attainment and hence equality. There are 1,170 attaining words.

Every nonzero generator column is a nonzero linear functional of the message. Choose a message where that column is 1; translation by that message pairs inputs where its value is 0 with inputs where its value is 1. Exactly 2^25 messages contribute 1 in each active column. The sum of all enumerated weights must therefore be 213 times 2^25 = 7,147,094,016, as observed. The zero message adds nothing.

The author's checker packs coordinates in the opposite bit order. This is a coordinate permutation, preserving rank and weights. Its rank routine reduces a row by XOR whenever that lowers its integer value, eliminating an existing highest pivot. Later basis rows have all earlier pivot coordinates zero, so subsequent reductions cannot reintroduce eliminated pivots. The number retained is therefore the rank, as above. Its Gray traversal has the coverage proof already given. Its second traversal loops through all ordinary binary messages from 1 through 2^26 - 1 and XORs exactly those rows with a set coefficient bit, so it independently reconstructs each codeword without the Gray recurrence. Both distances and minimum-weight multiplicities agree with my result.

For the author's negative control, row 0 is replaced by row 1 XOR row 2. The original rank-26 result means the remaining 25 original rows are independent. The replacement is in their span, so the modified rank is exactly 25 and rejection is correct. The descriptive Construction X metadata is not a premise of either checker or the distance proof: the generator and exhaustive enumeration establish the claimed code directly.

## Exact commands and real output

All commands below run from this folder. The system `python3 --version` reports Python 3.9.6.

Initial independent invocation:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

That first attempt stopped because my implementation initially used `int.bit_count`, unavailable in Python 3.9. Its complete original output was preserved in `skeptic/output.initial.txt`:

```text
object: object/code_q2_n213_k26_d77.json
sha256: 924876aa988e3a9da62a776f88c297db6aa005b475fe3ad9e76291685851cd12
dimensions: 26 x 213; every entry is an integer in GF(2)
rank over GF(2): 26
enumeration: all 67108863 nonzero messages in reflected Gray order
independent object checks: FAIL: 'int' object has no attribute 'bit_count'
```

I replaced that operation with a version-compatible exact population count before inspecting the author's code. This was a checker compatibility error, not a discrepancy in the saved object. The completed independent run used the same command:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

Exit status: 0. Complete actual `skeptic/output.txt`:

```text
object: object/code_q2_n213_k26_d77.json
sha256: 924876aa988e3a9da62a776f88c297db6aa005b475fe3ad9e76291685851cd12
dimensions: 26 x 213; every entry is an integer in GF(2)
rank over GF(2): 26
enumeration: all 67108863 nonzero messages in reflected Gray order
enumerated nonzero messages: 67108863
zero words among nonzero messages: 0
minimum distance: 77
minimum-weight codewords: 1170
witness message (row 0 is low bit): 0x115c
witness word (column 0 is low bit): 0x6971220249c12282105681a75a6000d38453d9e0d3631a4045244
witness support (zero-based columns): [2, 6, 9, 12, 14, 18, 26, 29, 31, 32, 36, 37, 41, 42, 44, 45, 48, 50, 51, 57, 58, 59, 60, 63, 64, 66, 67, 68, 69, 72, 74, 78, 83, 84, 85, 88, 90, 91, 105, 106, 109, 111, 112, 114, 116, 117, 118, 121, 123, 124, 131, 133, 134, 136, 138, 144, 149, 155, 157, 161, 164, 170, 171, 172, 175, 178, 181, 189, 193, 196, 200, 201, 202, 204, 207, 209, 210]
nonzero weight distribution (weight: count):
77: 1170
78: 2385
79: 1815
80: 3051
81: 12297
82: 18702
83: 13584
84: 16915
85: 59115
86: 102483
87: 75393
88: 81411
89: 259065
90: 422280
91: 305430
92: 267135
93: 790365
94: 1248075
95: 877125
96: 654645
97: 1785735
98: 2808960
99: 1952720
100: 1241835
101: 2974149
102: 4540104
103: 3078978
104: 1695675
105: 3672724
106: 5533590
107: 3720060
108: 1778605
109: 3321585
110: 4901700
111: 3196000
112: 1363905
113: 2248680
114: 3264300
115: 2107200
116: 805020
117: 1116165
118: 1566315
119: 980685
120: 336747
121: 400617
122: 572772
123: 358054
124: 112125
125: 110535
126: 151335
127: 90945
128: 26550
129: 21915
130: 28800
131: 16920
132: 4395
133: 2715
134: 3690
135: 2160
136: 570
137: 330
138: 270
139: 120
140: 15
141: 9
142: 9
143: 3
145: 45
146: 54
147: 24
148: 3
168: 5
active columns: 213
weight sum: 7147094016; expected: 7147094016
independent object checks: PASS
```

The second complete independent invocation was:

```sh
python3 skeptic/check.py > skeptic/output.repeat.txt 2>&1
```

Exit status: 0. Its complete output is byte-identical to the pasted output above; it remains saved separately as `skeptic/output.repeat.txt`.

After the independent run had finished, I inspected and ran the author's wrapper. Its temporary directory was kept within this folder:

```sh
mkdir -p skeptic/tmp
TMPDIR=skeptic/tmp sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
```

Exit status: 0. Complete actual `skeptic/author-output.txt`, including host toolchain diagnostics:

```text
sha256 matches INDEX.csv (924876aa988e3a9da62a776f88c297db6aa005b475fe3ad9e76291685851cd12)
== check_code.py on object/code_q2_n213_k26_d77.json
2026-10-14 18:16:08.652 xcodebuild[13656:72273349]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-14 18:16:14.203 xcodebuild[13656:72273344] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
gray-code walk: d=77 A_d=1170; direct enumeration: d=77 A_d=1170
PASS code=[213,26,77]_2 rank=26 A_d=1170 codewords_enumerated=67108863
== negative control: a rank-deficient copy must FAIL
negative control rejected as expected (FAIL rank over GF(2) is 25, not k = 26)
ALL CHECKS PASS
```

Metadata checks:

```sh
python3 skeptic/check_records.py > skeptic/records-output.txt 2>&1
```

Exit status: 0. Complete actual output:

```text
INDEX.csv: exactly one row; target, cell, value, table value and object path agree
INDEX.csv object sha256 matches: 924876aa988e3a9da62a776f88c297db6aa005b475fe3ad9e76291685851cd12
saved fetch timestamp agrees: 2026-10-15T00:06:08Z
saved-bound arithmetic: 76 < 77 <= 90: PASS
saved metadata consistency: PASS
Fetched table page is absent; its hash and extracted values cannot be independently authenticated.
Live table currency and novelty: not assessed (offline; assigned to other skeptics).
```

Final comparison:

```sh
python3 skeptic/compare.py > skeptic/comparison-output.txt 2>&1
```

Exit status: 0. Complete actual output:

```text
independent complete-run outputs: byte-identical
independent output sha256: 8f78b4611b8e771362c69cb07961e9dba36a6f6b2d2f983b0014a2d81f9042d2
independent / author Gray / author direct: d=77; A_d=1170; nonzero words=67108863
author rank-deficient negative control: rank 25, correctly rejected
comparison: PASS
```

## Mismatches and limits

No mathematical mismatch, missing claimed generator, or differing independent-run output was found. The initial Python API compatibility failure was corrected and both full independent runs completed successfully. Host toolchain diagnostics in the author's transcript did not prevent its successful exit or alter the mathematical results.

The fetched table page is intentionally absent: only metadata is saved. Its page hash and extracted numbers cannot be authenticated from these files; only internal consistency and the recorded-bound arithmetic were checked. No conclusion about table currency, priority, non-derivation from other codes, or novelty is included in this reproducibility verdict.

pass: true
