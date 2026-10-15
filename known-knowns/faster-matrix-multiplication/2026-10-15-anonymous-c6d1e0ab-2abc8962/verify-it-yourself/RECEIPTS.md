# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (2abc89623e051336de20440c1e68300d56656b98733b8df7e66808bbd60174be)
== check_slp.py on object/5x7x7_m176_cr699_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x7x7_m176_cr699_ZT_reduced.json", "format": "5x7x7", "rank": 176, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 179, "adds_V": 206, "adds_W": 314, "adds_total": 699, "naive_total": 2605, "declared_reduced": 699, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=699, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
