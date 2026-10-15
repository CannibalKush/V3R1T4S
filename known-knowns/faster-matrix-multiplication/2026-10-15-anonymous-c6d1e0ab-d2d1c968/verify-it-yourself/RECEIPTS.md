# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (d2d1c96812918b46fa34436c66cdd27e51383b12a9686a975d715d69e6480c75)
== check_fmm.py on object/11x13x16_r1445_Q.json
Brent equations hold modulo 1 primes whose product exceeds 2 * D^3 * (S + 1) (D = 8, S = 5595/4); hence exactly over Q
PASS format=11x13x16 rank=1445 max_den=8
== negative control: a copy with one coefficient changed must FAIL
negative control rejected as expected (FAIL 24 Brent equations violated modulo p = 2305843009213693951)
ALL CHECKS PASS
```
