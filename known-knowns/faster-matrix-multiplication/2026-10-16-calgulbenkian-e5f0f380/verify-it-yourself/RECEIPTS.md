# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (e5f0f3807baaa5f00a76f606bd33199db83dfd83ef82c21abbcb0fbc79c02d95)
== check_slp.py on object/2x4x8_m51_cr181_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "2x4x8_m51_cr181_ZT_reduced.json", "format": "2x4x8", "rank": 51, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 37, "adds_V": 67, "adds_W": 77, "adds_total": 181, "naive_total": 354, "declared_reduced": 181, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=181, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
