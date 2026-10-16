# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (feea5fbcfd07fd3416d280a9a3d8af5e49c916171b9771d614e51e7a43f98b85)
== check_slp.py on object/4x4x6_m73_cr256_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x4x6_m73_cr256_ZT_reduced.json", "format": "4x4x6", "rank": 73, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 66, "adds_V": 71, "adds_W": 119, "adds_total": 256, "naive_total": 540, "declared_reduced": 256, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=256, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
