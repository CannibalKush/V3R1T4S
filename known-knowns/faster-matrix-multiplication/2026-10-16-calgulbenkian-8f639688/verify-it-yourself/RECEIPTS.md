# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (8f63968828f21bb5d9ac3954a4424a742a68f22c641afbd4c507d26d3f7e3a2f)
== check_slp.py on object/4x5x8_m118_cr470_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x5x8_m118_cr470_ZT_reduced.json", "format": "4x5x8", "rank": 118, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 102, "adds_V": 146, "adds_W": 222, "adds_total": 470, "naive_total": 1521, "declared_reduced": 470, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=470, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
