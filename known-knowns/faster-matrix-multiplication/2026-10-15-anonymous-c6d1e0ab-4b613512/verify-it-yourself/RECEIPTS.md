# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (4b613512756bdb5c0303dc17236ad63b3b8a4e931d898e75e863d95d6dd9ab9e)
== check_fmm_fast.py on object/13x14x14_r1538_Q.json
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 42 bits, slot width 44 bits, 35672 blocks of 182 slots compared
PASS format=13x14x14 rank=1538
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x14x14 rank=1537: 729 of 35672 (a, b) blocks differ; first at A[0][0] x B[0][0])
ALL CHECKS PASS
```
