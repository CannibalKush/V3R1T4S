# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (efb7f10c7e3a5dcd2481aacbd72ae5e308550dd825927d1c1114574354447c80)
== check_slp.py on object/5x6x8_m170_cr667_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x6x8_m170_cr667_ZT_reduced.json", "format": "5x6x8", "rank": 170, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 159, "adds_V": 196, "adds_W": 312, "adds_total": 667, "naive_total": 2312, "declared_reduced": 667, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=667, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
