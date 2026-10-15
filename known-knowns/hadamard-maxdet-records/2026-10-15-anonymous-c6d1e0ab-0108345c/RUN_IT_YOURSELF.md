# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 verify-it-yourself/check_maxdet.py object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt --expect-norm 2119202655125403624550373680790052808829003860176536932438843923020304438454497
```

It reads the 109 x 109 matrix and checks that every entry is +1 or -1. It computes |det| exactly in two independent ways: fraction-free Bareiss elimination on Python integers, and determinants modulo twelve primes combined by the Chinese remainder theorem. The primes' product exceeds twice the Hadamard bound, so the CRT value is exact. The two values must agree. It also checks divisibility by 2^108 and that the value is below the Barba bound. The run script additionally checks the sha256 against `INDEX.csv`, and checks that a copy with one sign flipped is rejected.

## 2. How the object was built

`how-we-built-it/` holds the original run's search code (`maxdet_search.c`, `run_maxdet_campaign.py`) and its pre-registration (`PREREG.md`). We did not re-run the search; this claim rests only on the object and the checker above.

The structure can be read off the object itself. Row 0 and column 0 are a border: the corner is -1 and the other 216 border entries are +1. The remaining 108 x 108 block H is a Hadamard matrix (H H^T = 108 I). With u the border, |det| = 108^54 (1 + s/108), where s = 1056 is the excess the search reached. That gives |det| = 1164 · 108^53 = 2^108 · 291 · 27^53.
