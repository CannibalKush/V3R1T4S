# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (df14df3c1a01189e540ab5a0eedebc331cd08e12714d795df0884481da292366)
== check_slp.py on object/4x4x5_m61_cr222_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x4x5_m61_cr222_ZT_reduced.json", "format": "4x4x5", "rank": 61, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 59, "adds_V": 61, "adds_W": 102, "adds_total": 222, "naive_total": 452, "declared_reduced": 222, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=222, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
