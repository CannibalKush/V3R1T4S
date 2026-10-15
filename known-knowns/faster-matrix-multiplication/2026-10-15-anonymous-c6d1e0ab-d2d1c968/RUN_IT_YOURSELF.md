# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 verify-it-yourself/check_fmm.py object/11x13x16_r1445_Q.json --expect-rank 1445
```

It checks every Brent equation exactly. It works modulo primes near 2^61 whose product exceeds the bound stated in the checker, which makes the result exact over Q. It also counts the terms whose three factors are all nonzero. The run script additionally checks the sha256 against `INDEX.csv`, and checks that a copy with one coefficient changed is rejected.

## 2. Rebuild the object from Perminov's scheme

The build is deterministic; this command reproduces the shipped file byte for byte (sha256 d2d1c96812918b46fa34436c66cdd27e51383b12a9686a975d715d69e6480c75). It needs Python 3.9 or later with `numpy==2.0.2` and `python-flint==0.6.0`, and takes a few minutes on one core.

```sh
curl -sO https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/Q/12x13x16_m1509_Q.json
python3 how-we-built-it/sweep.py 12x13x16_m1509_Q.json --depth 1 --top 4 --save-all --out rebuilt
shasum -a 256 rebuilt/11x13x16_r1445_Q.json
```

`sweep.py` slices the parent along each axis. For axis 0 it removes 31 terms (1509 to 1478) and then absorbs 33 more (to 1445). It saves each child after an exact Brent check.
