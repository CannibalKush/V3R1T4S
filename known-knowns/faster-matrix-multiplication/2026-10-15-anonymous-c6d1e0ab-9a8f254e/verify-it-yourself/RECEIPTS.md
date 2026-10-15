# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (9a8f254ed5b7e15b8f4157da632c5adc686e46c4f020659b924114c8b7c5a618)
== check_fmm_fast.py on object/13x13x15_r1578_Q.json
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 40 bits, slot width 42 bits, 32955 blocks of 195 slots compared
PASS format=13x13x15 rank=1578
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x13x15 rank=1577: 76 of 32955 (a, b) blocks differ; first at A[6][4] x B[0][2])
ALL CHECKS PASS
```
