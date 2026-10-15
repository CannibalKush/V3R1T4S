# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (34a5c13ccfa01ac91606b8899c53be5f1facf7f62f1e06e9ddf5f9ec6bf82ea5)
== check_slp.py on object/6x6x7_m183_cr695_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "6x6x7_m183_cr695_ZT_reduced.json", "format": "6x6x7", "rank": 183, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 184, "adds_V": 182, "adds_W": 329, "adds_total": 695, "naive_total": 2502, "declared_reduced": 695, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=695, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
