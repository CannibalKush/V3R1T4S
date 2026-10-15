# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (5128a84caf064a0c4b0b6bd46d4c8d26e02cddac4bbc988437a72c947859e17c)
== check_code.py on object/code_q2_n175_k25_d61.json
gray-code walk: d=61 A_d=95; direct enumeration: d=61 A_d=95
PASS code=[175,25,61]_2 rank=25 A_d=95 codewords_enumerated=33554431
== negative control: a rank-deficient copy must FAIL
negative control rejected as expected (FAIL rank over GF(2) is 24, not k = 25)
ALL CHECKS PASS
```
