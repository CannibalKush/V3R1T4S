# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (0daeb11814025acb716cc2cb7432d358a83e8bff7985faec2ef73e5efad21bda)
== check_slp.py on object/4x6x6_m105_cr373_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x6x6_m105_cr373_ZT_reduced.json", "format": "4x6x6", "rank": 105, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 95, "adds_V": 106, "adds_W": 172, "adds_total": 373, "naive_total": 1376, "declared_reduced": 373, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=373, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
