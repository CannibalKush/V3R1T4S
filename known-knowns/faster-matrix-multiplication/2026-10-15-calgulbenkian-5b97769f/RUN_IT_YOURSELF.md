# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 verify-it-yourself/check_fmm_fast.py object/13x15x15_r1762_Q.json --expect-rank 1762
```

It checks every Brent equation exactly in integer arithmetic (the scheme is scaled to integers; each W row is packed into one integer with slots wide enough for a proven coefficient bound, so packed equality is slot-by-slot equality; the method is stated in the checker) and counts the terms whose three factors are all nonzero. The run script also checks the sha256 against `INDEX.csv`, and checks that a copy with the last term removed is rejected.

## 2. Rebuild the object from the published parent

`how-we-built-it/REBUILD.md` gives the deterministic recipe: the published LITA parent file (its URL and sha256 are stated there; it is not redistributed in this package), the explicit slice directions and absorption settings for every step, and one command, `rebuild.py`, that regenerates this scheme byte for byte (expected sha256 of the output stated in the recipe) and then runs the exact checker. It needs Python 3.9 or later with `numpy==2.0.2` and `python-flint==0.6.0` and a C++17 compiler; a clean-directory run is recorded in `how-we-built-it/rebuild_test_output.txt`.
