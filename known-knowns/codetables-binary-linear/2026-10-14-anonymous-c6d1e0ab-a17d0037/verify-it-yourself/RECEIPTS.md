# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (a17d00378317979d9fe0acb452d3cce805f55cb17595a8407acb9b56b7b51a76)
== check_code.py on object/win_q2_n173_k17_d72.json
gray-code walk: d=72 A_d=6341; direct enumeration: d=72 A_d=6341
PASS code=[173,17,72]_2 rank=17 A_d=6341 codewords_enumerated=131071
== negative control: a corrupted copy must FAIL
negative control rejected as expected (FAIL minimum distance 71 != expected 72)
ALL CHECKS PASS
```
