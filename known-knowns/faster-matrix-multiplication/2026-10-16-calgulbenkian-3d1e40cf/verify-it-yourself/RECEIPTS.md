# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (3d1e40cf65f343ad2edfe3735c1d4eccd1fd4aeaca82b31980779e38a059dcc1)
== check_slp.py on object/2x5x6_m47_cr179_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "2x5x6_m47_cr179_ZT_reduced.json", "format": "2x5x6", "rank": 47, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 38, "adds_V": 65, "adds_W": 76, "adds_total": 179, "naive_total": 332, "declared_reduced": 179, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=179, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
