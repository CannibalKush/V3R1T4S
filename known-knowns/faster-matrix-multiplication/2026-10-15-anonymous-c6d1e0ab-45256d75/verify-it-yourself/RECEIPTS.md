# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (45256d75a05660145a239129ba59524edf864bbda68bcf5297be8fdf7c38158e)
== check_slp.py on object/4x6x8_m140_cr476_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x6x8_m140_cr476_ZT_reduced.json", "format": "4x6x8", "rank": 140, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 108, "adds_V": 136, "adds_W": 232, "adds_total": 476, "naive_total": 1620, "declared_reduced": 476, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=476, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
