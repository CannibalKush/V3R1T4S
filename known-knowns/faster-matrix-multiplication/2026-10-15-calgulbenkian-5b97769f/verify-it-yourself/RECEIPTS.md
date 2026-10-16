# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (5b97769fb1c3115c7195f0c508e0cae9ded013ef2543a7f0d5aa4147410e1647)
== check_fmm_fast.py on object/13x15x15_r1762_Q.json
exact integer check: D=8704000 (DU=5440, DV=40, DW=40), coefficient bound 40 bits, slot width 42 bits, 43875 blocks of 195 slots compared
PASS format=13x15x15 rank=1762
== negative control: a copy with the last term removed must FAIL
negative control rejected as expected (FAIL format=13x15x15 rank=1761: 8550 of 43875 (a, b) blocks differ; first at A[0][1] x B[0][0])
ALL CHECKS PASS
```
