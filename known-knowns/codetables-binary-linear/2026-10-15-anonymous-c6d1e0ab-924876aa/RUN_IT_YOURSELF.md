# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 verify-it-yourself/check_code.py object/code_q2_n213_k26_d77.json --expect-d 77
```

It reads the 26 x 213 generator matrix, checks that its rank over GF(2) is 26, and computes the minimum distance twice. Both methods enumerate all 67,108,863 nonzero codewords: a Gray-code walk, and a direct walk over messages. Both must agree. The run script also checks the object's sha256 against `INDEX.csv`, and checks that a rank-deficient copy is rejected.

## 2. Rebuild the object from its parameters

The generator matrix is determined by a handful of polynomials over GF(2). This standard-library script rebuilds it and compares it with the shipped object entry by entry:

```sh
python3 how-we-built-it/rebuild.py object/code_q2_n213_k26_d77.json
```

Expected output ends with `IDENTICAL to the object's G`. The construction, stated in the script: an index-2 quasi-cyclic code of length 210 with circulant size m = 105, check polynomial h = (x+1)(x^3+x^2+1)(x^4+x^3+x^2+x+1)(x^6+x^4+x^2+x+1)(x^12+x^8+x^6+x^5+x^3+x^2+1) (degree 26, a divisor of x^105 - 1) and multiplier f = 0x2d547, which has minimum distance 76; its submodule subcode {a : (x^3+x^2+1) divides a} has dimension 23 and minimum distance 77; appending three columns that hold a mod (x^3+x^2+1) (Construction X with the trivial [3,3,1] auxiliary code) gives the [213, 26, 77] code.
