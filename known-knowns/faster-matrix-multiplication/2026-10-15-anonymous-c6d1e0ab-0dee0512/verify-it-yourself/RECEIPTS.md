# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (0dee0512255d74595673fd8bfa0df20b0ab0a87785b2d11cbb2a94f6dbd5d57c)
== check_fmm_fast.py on object/15x16x16_r2176_Q.json
exact integer check: D=7560000 (DU=60, DV=60, DW=2100), coefficient bound 42 bits, slot width 44 bits, 61440 blocks of 240 slots compared
PASS format=15x16x16 rank=2176
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=15x16x16 rank=2175: 4147 of 61440 (a, b) blocks differ; first at A[0][0] x B[0][0])
ALL CHECKS PASS
```
