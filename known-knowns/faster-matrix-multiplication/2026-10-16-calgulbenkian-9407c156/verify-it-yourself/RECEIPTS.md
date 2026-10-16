# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (9407c156647ed8a24fbd9e29d7f644e1fd6281aabc4eaa317bb5cb3a3a9b5b23)
== check_slp.py on object/3x5x5_m58_cr211_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "3x5x5_m58_cr211_ZT_reduced.json", "format": "3x5x5", "rank": 58, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 48, "adds_V": 69, "adds_W": 94, "adds_total": 211, "naive_total": 357, "declared_reduced": 211, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=211, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
