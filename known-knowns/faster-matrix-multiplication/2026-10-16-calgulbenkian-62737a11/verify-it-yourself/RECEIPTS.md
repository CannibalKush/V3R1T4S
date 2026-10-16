# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (62737a117df29bc9dc6194509ed47f95a6f763ea3ca21fca84f79a78c44e6e1a)
== check_slp.py on object/2x5x5_m40_cr147_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "2x5x5_m40_cr147_ZT_reduced.json", "format": "2x5x5", "rank": 40, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 31, "adds_V": 54, "adds_W": 62, "adds_total": 147, "naive_total": 283, "declared_reduced": 147, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=147, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
