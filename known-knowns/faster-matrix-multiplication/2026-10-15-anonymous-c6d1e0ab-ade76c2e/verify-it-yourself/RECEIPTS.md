# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (ade76c2eef28cca082e6f87f2ca0294f6a6e5bcdce1e1cb9356fe068bab0dd65)
== check_slp.py on object/4x6x7_m123_cr469_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x6x7_m123_cr469_ZT_reduced.json", "format": "4x6x7", "rank": 123, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 114, "adds_V": 140, "adds_W": 215, "adds_total": 469, "naive_total": 1586, "declared_reduced": 469, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=469, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
