# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (b60a9f0b2339bc2927201b903c73b030905b0b39cc6a12b3a3b53fc65da014cf)
== check_slp.py on object/6x6x8_m203_cr719_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "6x6x8_m203_cr719_ZT_reduced.json", "format": "6x6x8", "rank": 203, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 174, "adds_V": 195, "adds_W": 350, "adds_total": 719, "naive_total": 2514, "declared_reduced": 719, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=719, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
