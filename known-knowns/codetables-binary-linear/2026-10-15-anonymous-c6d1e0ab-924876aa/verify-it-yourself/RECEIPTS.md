# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (924876aa988e3a9da62a776f88c297db6aa005b475fe3ad9e76291685851cd12)
== check_code.py on object/code_q2_n213_k26_d77.json
gray-code walk: d=77 A_d=1170; direct enumeration: d=77 A_d=1170
PASS code=[213,26,77]_2 rank=26 A_d=1170 codewords_enumerated=67108863
== negative control: a rank-deficient copy must FAIL
negative control rejected as expected (FAIL rank over GF(2) is 25, not k = 26)
ALL CHECKS PASS
```
