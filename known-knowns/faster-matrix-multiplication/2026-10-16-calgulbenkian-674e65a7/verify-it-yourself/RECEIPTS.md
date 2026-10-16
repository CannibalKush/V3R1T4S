# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (674e65a792736a9bf4930d7e529fb901990cafa22ddf52baaf6c2ed0d256a87f)
== check_slp.py on object/2x8x8_m100_cr418_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "2x8x8_m100_cr418_ZT_reduced.json", "format": "2x8x8", "rank": 100, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 90, "adds_V": 154, "adds_W": 174, "adds_total": 418, "naive_total": 608, "declared_reduced": 418, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=418, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
