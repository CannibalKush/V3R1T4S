# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (49ee1c4f6642d1245e5af697eeb2f342024d04f06a0cc9113501ce8f45177144)
== check_fmm_fast.py on object/13x14x15_r1645_Q.json
exact integer check: D=8704000 (DU=40, DV=40, DW=5440), coefficient bound 40 bits, slot width 42 bits, 38220 blocks of 195 slots compared
PASS format=13x14x15 rank=1645
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x14x15 rank=1644: 840 of 38220 (a, b) blocks differ; first at A[3][4] x B[0][0])
ALL CHECKS PASS
```
