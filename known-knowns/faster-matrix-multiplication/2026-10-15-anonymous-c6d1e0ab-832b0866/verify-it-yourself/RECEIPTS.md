# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (832b08667df7d72d5c12f78f7073168f43dd50e323aaaf547290f0533d2585f3)
== check_slp.py on object/5x6x7_m150_cr582_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x6x7_m150_cr582_ZT_reduced.json", "format": "5x6x7", "rank": 150, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 147, "adds_V": 171, "adds_W": 264, "adds_total": 582, "naive_total": 2039, "declared_reduced": 582, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=582, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
