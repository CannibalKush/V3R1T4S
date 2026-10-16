# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (e5731a01ecf58de14b5fc4a6e9a0de880b11146aeeeef4df6844dd83bfbb83a8)
== check_slp.py on object/3x4x5_m47_cr156_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "3x4x5_m47_cr156_ZT_reduced.json", "format": "3x4x5", "rank": 47, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 38, "adds_V": 44, "adds_W": 74, "adds_total": 156, "naive_total": 277, "declared_reduced": 156, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=156, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
