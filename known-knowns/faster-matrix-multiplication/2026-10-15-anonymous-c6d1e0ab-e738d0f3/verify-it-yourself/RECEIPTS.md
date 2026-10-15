# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (e738d0f367b67ba740109db2687b58811da516ee74f67c42ccb934eab382548d)
== check_fmm_fast.py on object/13x13x14_r1479_Q.json
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 41 bits, slot width 43 bits, 30758 blocks of 182 slots compared
PASS format=13x13x14 rank=1479
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x13x14 rank=1478: 833 of 30758 (a, b) blocks differ; first at A[5][0] x B[0][0])
ALL CHECKS PASS
```
