# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (9d6ef02f8162d9d5a53e56ecff6821459727c32d5a5fecb24283bd0c716fdf10)
== check_fmm_fast.py on object/14x16x16_r2117_Q.json
exact integer check: D=26127360000 (DU=25200, DV=720, DW=1440), coefficient bound 49 bits, slot width 51 bits, 57344 blocks of 224 slots compared
PASS format=14x16x16 rank=2117
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=14x16x16 rank=2116: 3712 of 57344 (a, b) blocks differ; first at A[0][0] x B[0][0])
ALL CHECKS PASS
```
