# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 verify-it-yourself/check_code.py object/code_q2_n175_k25_d61.json --expect-d 61
```

It reads the 25 x 175 generator matrix, checks that its rank over GF(2) is 25, and computes the minimum distance twice. Both methods enumerate all 33,554,431 nonzero codewords: a Gray-code walk, and a direct walk over messages. Both must agree. The run script also checks the object's sha256 against `INDEX.csv`, and checks that a rank-deficient copy is rejected.

## 2. Rebuild the object from its parameters

The generator matrix is fully determined by six numbers. This standard-library script rebuilds it and compares it with the shipped object entry by entry:

```sh
python3 how-we-built-it/rebuild.py object/code_q2_n175_k25_d61.json
```

Expected output ends with `IDENTICAL to the object's G`. The construction, stated in the script: a quasi-cyclic index-2 code of length 170 with circulant size 85, check polynomial h = 0x36a5431 (a degree-25 divisor of x^85 - 1, product of x + 1 and three octics) and multiplier f = 0xe600fc, which has minimum distance 60 with 680 words of weight 60; then five added columns, each a linear functional on the messages (0x1e80373, 0xa194c, 0x1fefae8, 0x19cf5ed, 0x16091f4), chosen so that every weight-60 word gets a 1 in at least one new column.
