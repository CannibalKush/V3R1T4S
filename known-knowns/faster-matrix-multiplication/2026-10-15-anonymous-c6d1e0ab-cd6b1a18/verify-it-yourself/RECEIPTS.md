# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (cd6b1a181d857f3e993cc6c15338a7f709bd1119c2745a399cfc02eae9b52f03)
== check_slp.py on object/5x5x8_m144_cr556_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x5x8_m144_cr556_ZT_reduced.json", "format": "5x5x8", "rank": 144, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 133, "adds_V": 161, "adds_W": 262, "adds_total": 556, "naive_total": 1924, "declared_reduced": 556, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=556, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
