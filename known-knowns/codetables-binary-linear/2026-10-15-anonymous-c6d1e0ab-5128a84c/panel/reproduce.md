# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: all properties that can be checked from this saved package are confirmed. This is a reproduction verdict. The current table value and novelty are left to the other skeptic, as instructed.

## Quoted definition and success criterion

> object/code_q2_n175_k25_d61.json is a 25 x 175 generator matrix over GF(2) of rank 25 whose linear code has minimum distance exactly 61, strictly above the codetables.de lower bound of 60 for (q, n, k) = (2, 175, 25).

> For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256.

> Success means a k x n generator matrix over GF(q) with these properties. (1) Rank is exactly k over GF(q), computed independently. (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible (2^k <= ~2^32), or, for large k (or large k with small n-k, via the dual and MacWilliams identities), by two independent exact minimum-distance implementations that agree; never by sampling. (3) d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/ cell for (q,n,k) at verification time, and at most the upper bound. (4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and no newer arXiv claim already reaches that d.

CLAIM.md contains no Lille URL template. The requested bracket-only spelling for such a template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only the angle brackets have been changed to braces in that spelling. No other quoted wording has been changed.

The operational definition checked is C = {uG : u in GF(2)^25}, with all arithmetic modulo 2. Hamming weight counts the coordinates equal to 1. For a linear code, the minimum distance equals the least weight of a nonzero codeword: the difference of any two distinct codewords is a nonzero codeword, and each nonzero codeword is its own difference from zero.

The applicable local requirements are the matrix dimensions and field, clause (1), the feasible exhaustive-enumeration branch of clause (2), and the numerical inequalities in clause (3) using the saved metadata. Clauses about the live table and prior or newer claims are not judged here. Neither partial-win alternative is claimed by this package.

## Independence and scope

I read CLAIM.md and the saved object, recorded the quoted definition in skeptic/definition.md, and wrote skeptic/check.py before opening any file in verify-it-yourself/. The independent checker completed its successful exhaustive run before I opened REPRODUCE.md or the author's checker. All package data read and artifacts written stayed in this folder; no network was used.

An initial checker attempt failed because I omitted the x term from the final polynomial factor when transcribing the object, and because this python3 has no int.bit_count. I corrected the transcription and added a standard-library population-count fallback before inspecting the author's code. The failed attempt is preserved in skeptic/initial_output.txt. Those were errors in my first checker, not disagreements with the object. The successful full output is skeptic/output.txt.

## Properties and proof steps checked

1. Shape and field: require exactly 25 lists of length 175, with every entry an integer 0 or 1. The descriptive q, n, k and d fields must match 2, 175, 25 and 61. Binary packed integers preserve coordinate order with coordinate j at bit j.
2. Rank: independently perform GF(2) Gaussian elimination with XOR and highest-bit pivots. Each surviving pivot adds an independent row; removing existing pivots preserves the span. The generator and its first 170 columns both have rank 25. Thus distinct messages produce distinct codewords.
3. Exhaustiveness: enumerate t = 1 through 2^25 - 1, using message Gray(t) = t XOR (t >> 1). This map is a bijection: starting at the highest bit, its triangular bit equations uniquely recover t from Gray(t). Zero maps only to zero. Consecutive Gray messages differ at the lowest set bit of t, so XORing that generator row maintains the exact codeword. Every nonzero message, hence every nonzero codeword, is visited once. Both full histogram totals are checked against 33,554,431. No sampling is used.
4. Exact distance and claimed value: compute weights of every extended and base word, retain both complete weight distributions, and check that no nonzero message gives zero. The extended minimum is 61, and exactly 95 words attain it, matching A_d. Direct multiplication of an explicit witness using the original unpacked entries independently confirms a word of weight 61. Exhaustiveness proves the lower bound; the witness proves equality.
5. Polynomial construction: multiply the four stated factors by carryless polynomial arithmetic over GF(2), obtaining h = 0x36a5431 of degree 25. Polynomial long division of x^85 + 1 by h gives g = 0x1c33559d105fa131 with zero remainder. In characteristic two, x^85 - 1 = x^85 + 1. For each basis message a = x^i, compute (g*a, g*(a*f mod h)) with f = 0xe600fc. Both blocks fit 85 coordinates. Append the five parity functionals given in the object. Every reconstructed row equals the saved row exactly. Polynomial multiplication, reduction and parity functionals are linear, so checking all basis rows establishes the construction for all messages. The quasi-cyclic description also follows: simultaneous cyclic shifting of the two length-85 blocks is multiplication by x modulo x^85 + 1, which corresponds to replacing a by x*a modulo h because g*h = x^85 + 1. Reduction commutes with multiplication by f. Thus the base row space is invariant under this blockwise shift; interleaving the blocks gives the usual index-2 coordinate convention.
6. Extension argument: the exhaustive base minimum is 60, attained by 680 words. Every one of those 680 words has a nonzero five-coordinate extension. Appending coordinates cannot lower weight. Each base word of weight 60 therefore has extended weight at least 61; every other nonzero base word already has weight greater than 60. The enumerated witness attains 61. This re-derives the claimed improvement from the saved base construction.
7. Saved records: independently parse INDEX.csv, check its single row, cell, value, fetch time, object path and SHA-256, and compare the recorded bounds with table-record/README.md and the object metadata. The saved arithmetic is 60 strictly less than 61, and 61 at most 72. The third-party page is explicitly not saved, so its reported page hash and live status cannot be independently verified here; no current-table conclusion is drawn.
8. Author comparison: run the author's checker only after the independent exhaustive run. Its Gray walk and direct binary-message enumeration each cover all 33,554,431 nonzero messages and agree on d = 61 and A_d = 95. The author's integer encoding reverses coordinate order relative to mine, which preserves both weight and rank. The independent and author results agree.
9. Negative control: replace row 0 by row 1 XOR row 2, save the control within skeptic/, and independently find rank 24. The original other 24 rows are independent, and the replacement is in their span, proving the expected rank. The author's checker rejects it with exit status 1 and the expected rank-24 message.
10. Reproducibility: repeat my entire exhaustive run, not a sample. Both complete outputs are byte-for-byte identical. Recheck the original object's hash after all runs. No disagreement, missing claimed object, or non-determinism was observed.

## Exact commands and verbatim output

All commands below were run from this folder. The four positive checker/comparison commands and the repeat command returned exit status 0. The intended author negative-control rejection returned exit status 1, as included in the records output. The author's wrapper was read but not executed; its hash check and negative-control step were independently performed within this folder.

### Independent full enumeration

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

Verbatim saved output from skeptic/output.txt:

```text
Independent checker: GF(2) row space, Hamming weight, exhaustive Gray walk
object: object/code_q2_n175_k25_d61.json
sha256: 5128a84caf064a0c4b0b6bd46d4c8d26e02cddac4bbc988437a72c947859e17c
25 x 175 matrix, integer entries in GF(2): PASS
rank over GF(2): 25
rank exactly 25: PASS
saved q,n,k,d agree with claimed 2,175,25,61: PASS
product of stated h factors: 0x36a5431; degree: 25
stated h factorization and degree 25: PASS
g = (x^85 + 1)/h: 0x1c33559d105fa131; remainder: 0
h divides x^85 - 1 over GF(2): PASS
construction row 0: both polynomial blocks have length at most 85: PASS
construction row 1: both polynomial blocks have length at most 85: PASS
construction row 2: both polynomial blocks have length at most 85: PASS
construction row 3: both polynomial blocks have length at most 85: PASS
construction row 4: both polynomial blocks have length at most 85: PASS
construction row 5: both polynomial blocks have length at most 85: PASS
construction row 6: both polynomial blocks have length at most 85: PASS
construction row 7: both polynomial blocks have length at most 85: PASS
construction row 8: both polynomial blocks have length at most 85: PASS
construction row 9: both polynomial blocks have length at most 85: PASS
construction row 10: both polynomial blocks have length at most 85: PASS
construction row 11: both polynomial blocks have length at most 85: PASS
construction row 12: both polynomial blocks have length at most 85: PASS
construction row 13: both polynomial blocks have length at most 85: PASS
construction row 14: both polynomial blocks have length at most 85: PASS
construction row 15: both polynomial blocks have length at most 85: PASS
construction row 16: both polynomial blocks have length at most 85: PASS
construction row 17: both polynomial blocks have length at most 85: PASS
construction row 18: both polynomial blocks have length at most 85: PASS
construction row 19: both polynomial blocks have length at most 85: PASS
construction row 20: both polynomial blocks have length at most 85: PASS
construction row 21: both polynomial blocks have length at most 85: PASS
construction row 22: both polynomial blocks have length at most 85: PASS
construction row 23: both polynomial blocks have length at most 85: PASS
construction row 24: both polynomial blocks have length at most 85: PASS
all saved rows equal the stated construction for a = x^i: PASS
base generator rank: 25
base rank exactly 25: PASS
nonzero messages enumerated: 33554431
extended weight distribution: {"61": 95, "62": 420, "63": 1176, "64": 3036, "65": 6660, "66": 12475, "67": 20017, "68": 29847, "69": 42812, "70": 61518, "71": 88668, "72": 126517, "73": 176932, "74": 243484, "75": 332687, "76": 446392, "77": 581876, "78": 731437, "79": 894814, "80": 1065322, "81": 1246605, "82": 1435750, "83": 1609798, "84": 1764686, "85": 1884106, "86": 1963876, "87": 2006290, "88": 2005118, "89": 1965762, "90": 1884232, "91": 1763840, "92": 1610844, "93": 1433345, "94": 1247758, "95": 1064870, "96": 894249, "97": 732264, "98": 581287, "99": 447415, "100": 332627, "101": 244106, "102": 176678, "103": 126154, "104": 88781, "105": 61194, "106": 42836, "107": 29865, "108": 20019, "109": 12444, "110": 6729, "111": 2988, "112": 1168, "113": 407, "114": 128, "115": 26, "172": 1}
base weight distribution: {"60": 680, "62": 6120, "64": 30430, "66": 66470, "68": 135320, "70": 282880, "72": 538050, "74": 999515, "76": 1612960, "78": 2297040, "80": 3068670, "82": 3707360, "84": 4031720, "86": 4031720, "88": 3707360, "90": 3068670, "92": 2297040, "94": 1612960, "96": 999515, "98": 538050, "100": 282880, "102": 135320, "104": 66470, "106": 30430, "108": 6120, "110": 680, "170": 1}
full enumeration count and both histogram totals equal 2^25 - 1: PASS
no nonzero message gives zero in either code: PASS
exact extended minimum distance: 61
exact base minimum distance: 60
extended words of weight 61: 95
base words of weight 60: 680; covered by extension: 680
exact minimum distance 61: PASS
claimed A_d = 95: PASS
base distance 60 and every minimum word receives a nonzero extension: PASS
minimum-weight witness message (bit i selects row i): 0x3a879
witness codeword integer (bit j is coordinate j): 0x125a51148924402cd0184c20292e10558604b1a0f9c9
minimum witness checked by direct matrix multiplication: PASS
saved descriptive table bounds: lower=60; upper=72
numeric comparison with saved metadata: 60 < 61 <= 72: PASS
Live-table currency and novelty: outside this offline reproduction review
independent result: PASS
```

### Independent repeat, also exhaustive

```sh
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
```

Verbatim saved output from skeptic/output-repeat.txt:

```text
Independent checker: GF(2) row space, Hamming weight, exhaustive Gray walk
object: object/code_q2_n175_k25_d61.json
sha256: 5128a84caf064a0c4b0b6bd46d4c8d26e02cddac4bbc988437a72c947859e17c
25 x 175 matrix, integer entries in GF(2): PASS
rank over GF(2): 25
rank exactly 25: PASS
saved q,n,k,d agree with claimed 2,175,25,61: PASS
product of stated h factors: 0x36a5431; degree: 25
stated h factorization and degree 25: PASS
g = (x^85 + 1)/h: 0x1c33559d105fa131; remainder: 0
h divides x^85 - 1 over GF(2): PASS
construction row 0: both polynomial blocks have length at most 85: PASS
construction row 1: both polynomial blocks have length at most 85: PASS
construction row 2: both polynomial blocks have length at most 85: PASS
construction row 3: both polynomial blocks have length at most 85: PASS
construction row 4: both polynomial blocks have length at most 85: PASS
construction row 5: both polynomial blocks have length at most 85: PASS
construction row 6: both polynomial blocks have length at most 85: PASS
construction row 7: both polynomial blocks have length at most 85: PASS
construction row 8: both polynomial blocks have length at most 85: PASS
construction row 9: both polynomial blocks have length at most 85: PASS
construction row 10: both polynomial blocks have length at most 85: PASS
construction row 11: both polynomial blocks have length at most 85: PASS
construction row 12: both polynomial blocks have length at most 85: PASS
construction row 13: both polynomial blocks have length at most 85: PASS
construction row 14: both polynomial blocks have length at most 85: PASS
construction row 15: both polynomial blocks have length at most 85: PASS
construction row 16: both polynomial blocks have length at most 85: PASS
construction row 17: both polynomial blocks have length at most 85: PASS
construction row 18: both polynomial blocks have length at most 85: PASS
construction row 19: both polynomial blocks have length at most 85: PASS
construction row 20: both polynomial blocks have length at most 85: PASS
construction row 21: both polynomial blocks have length at most 85: PASS
construction row 22: both polynomial blocks have length at most 85: PASS
construction row 23: both polynomial blocks have length at most 85: PASS
construction row 24: both polynomial blocks have length at most 85: PASS
all saved rows equal the stated construction for a = x^i: PASS
base generator rank: 25
base rank exactly 25: PASS
nonzero messages enumerated: 33554431
extended weight distribution: {"61": 95, "62": 420, "63": 1176, "64": 3036, "65": 6660, "66": 12475, "67": 20017, "68": 29847, "69": 42812, "70": 61518, "71": 88668, "72": 126517, "73": 176932, "74": 243484, "75": 332687, "76": 446392, "77": 581876, "78": 731437, "79": 894814, "80": 1065322, "81": 1246605, "82": 1435750, "83": 1609798, "84": 1764686, "85": 1884106, "86": 1963876, "87": 2006290, "88": 2005118, "89": 1965762, "90": 1884232, "91": 1763840, "92": 1610844, "93": 1433345, "94": 1247758, "95": 1064870, "96": 894249, "97": 732264, "98": 581287, "99": 447415, "100": 332627, "101": 244106, "102": 176678, "103": 126154, "104": 88781, "105": 61194, "106": 42836, "107": 29865, "108": 20019, "109": 12444, "110": 6729, "111": 2988, "112": 1168, "113": 407, "114": 128, "115": 26, "172": 1}
base weight distribution: {"60": 680, "62": 6120, "64": 30430, "66": 66470, "68": 135320, "70": 282880, "72": 538050, "74": 999515, "76": 1612960, "78": 2297040, "80": 3068670, "82": 3707360, "84": 4031720, "86": 4031720, "88": 3707360, "90": 3068670, "92": 2297040, "94": 1612960, "96": 999515, "98": 538050, "100": 282880, "102": 135320, "104": 66470, "106": 30430, "108": 6120, "110": 680, "170": 1}
full enumeration count and both histogram totals equal 2^25 - 1: PASS
no nonzero message gives zero in either code: PASS
exact extended minimum distance: 61
exact base minimum distance: 60
extended words of weight 61: 95
base words of weight 60: 680; covered by extension: 680
exact minimum distance 61: PASS
claimed A_d = 95: PASS
base distance 60 and every minimum word receives a nonzero extension: PASS
minimum-weight witness message (bit i selects row i): 0x3a879
witness codeword integer (bit j is coordinate j): 0x125a51148924402cd0184c20292e10558604b1a0f9c9
minimum witness checked by direct matrix multiplication: PASS
saved descriptive table bounds: lower=60; upper=72
numeric comparison with saved metadata: 60 < 61 <= 72: PASS
Live-table currency and novelty: outside this offline reproduction review
independent result: PASS
```

### Author full enumerations

```sh
python3 verify-it-yourself/check_code.py object/code_q2_n175_k25_d61.json --expect-d 61 > skeptic/author-output.txt 2>&1
```

Verbatim saved output from skeptic/author-output.txt:

```text
gray-code walk: d=61 A_d=95; direct enumeration: d=61 A_d=95
PASS code=[175,25,61]_2 rank=25 A_d=95 codewords_enumerated=33554431
```

### Saved records and author negative control

```sh
python3 skeptic/check_records.py > skeptic/records-output.txt 2>&1
```

Verbatim saved output from skeptic/records-output.txt:

```text
INDEX.csv: one record; target, cell, value, saved lower bound, fetch time, object path and sha256 agree: PASS
table-record/README.md: saved cell, fetch time and bounds agree with INDEX.csv and object metadata: PASS
Saved-bound arithmetic: 60 < 61 <= 72: PASS
The third-party page was not saved; its hash and live status are not verified here.
Independent rank of saved negative control skeptic/negative-object.json: 24: PASS
Author negative-control output:
FAIL rank over GF(2) is 24, not k = 25
Author negative-control exit status: 1
Author rejects independently confirmed rank-24 control: PASS
Saved-record and negative-control result: PASS
```

### Completed-run comparison

```sh
python3 skeptic/compare.py > skeptic/comparison-output.txt 2>&1
```

Verbatim saved output from skeptic/comparison-output.txt:

```text
Two independent-checker exhaustive runs: byte-for-byte identical: PASS
Sha256 of each independent output: 9486cb12849545699e368d8d2ec507a2ac941390e6e0cde0aec8a9cb50b038ad
Author Gray walk and direct full enumeration agree with independent rank, distance, count and A_d: PASS
Object hash still matches INDEX.csv after all runs: PASS
Mismatch or observed non-determinism: none
Comparison result: PASS
```

The additional exact command `cmp skeptic/output.txt skeptic/output-repeat.txt` returned exit status 0 and produced no output.

## Mismatches and disposition

There is no mismatch between the saved object, independently computed properties, saved numerical records and the author's computed results. Every locally checkable property and construction step listed above is confirmed. This verdict does not establish current-table status or novelty.

pass: true
