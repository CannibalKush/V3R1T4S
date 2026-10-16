# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (760a6fabaf3fef7778e29b48d9b96dca9ae9dc8686afa84060805ac3be723354)
== check_slp.py on object/5x5x6_m110_cr413_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x5x6_m110_cr413_ZT_reduced.json", "format": "5x5x6", "rank": 110, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 108, "adds_V": 114, "adds_W": 191, "adds_total": 413, "naive_total": 1215, "declared_reduced": 413, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=413, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
