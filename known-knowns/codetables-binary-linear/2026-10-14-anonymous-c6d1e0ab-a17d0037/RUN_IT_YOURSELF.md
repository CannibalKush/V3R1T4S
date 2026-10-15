# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 verify-it-yourself/check_code.py object/win_q2_n173_k17_d72.json --expect-d 72
```

It reads the 17 x 173 generator matrix, checks that its rank over GF(2) is 17, and computes the minimum distance twice. Both methods enumerate all 131,071 nonzero codewords: a Gray-code walk, and a direct walk over messages. Both must agree. The run script also checks the object's sha256 against `INDEX.csv`, and checks that a copy with one flipped bit is rejected.

## 2. How the object was built

`how-we-built-it/` holds the search code (`qc_search.c`, `bklc_opt.c`) and the run's pre-registration (`PREREG.md`). The commands below are as the original run recorded them. We did not re-run the search; this claim rests only on the object and the checker above.

```sh
clang -O3 -march=native -Wall -Wextra -o bklc_opt how-we-built-it/bklc_opt.c
./bklc_opt
```

The original run describes `bklc_opt` as deterministic. It builds quasi-cyclic generator matrices from polynomial generators, then evaluates them exactly, punctures them and extends them. `qc_search.c` is the quasi-cyclic / quasi-twisted search used in the same run.
