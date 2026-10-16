# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (1e59f08cf1870f4ade6b3ab5efc2d004e5bb1a0edb455b7e250ed4a7cfc6a65a)
== check_slp.py on object/5x5x7_m127_cr483_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x5x7_m127_cr483_ZT_reduced.json", "format": "5x5x7", "rank": 127, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 116, "adds_V": 137, "adds_W": 230, "adds_total": 483, "naive_total": 1607, "declared_reduced": 483, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=483, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
