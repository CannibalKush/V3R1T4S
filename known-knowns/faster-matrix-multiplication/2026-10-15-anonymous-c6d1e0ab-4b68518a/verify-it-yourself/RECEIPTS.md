# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (4b68518ac7f293047071df6723a04783e4d38f302c6b98ccaa02f0c66669ae3b)
== check_fmm_fast.py on object/15x16x15_r2105_Q.json
exact integer check: D=15120000 (DU=60, DV=120, DW=2100), coefficient bound 42 bits, slot width 44 bits, 57600 blocks of 225 slots compared
PASS format=15x16x15 rank=2105
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=15x16x15 rank=2104: 330 of 57600 (a, b) blocks differ; first at A[1][0] x B[3][2])
ALL CHECKS PASS
```
