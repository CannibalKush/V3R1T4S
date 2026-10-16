# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (a6655488fc692a5a552aed8c46ae58eff2a384d66f33966f3a53c0a33b3fec2e)
== check_slp.py on object/4x4x7_m85_cr294_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x4x7_m85_cr294_ZT_reduced.json", "format": "4x4x7", "rank": 85, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 72, "adds_V": 83, "adds_W": 139, "adds_total": 294, "naive_total": 631, "declared_reduced": 294, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=294, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
