# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (b3b9b009a9de20414ff66a9309bc4092c31b6ad74a3aec0e235e470cd5d07335)
== check_slp.py on object/4x5x7_m104_cr379_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x5x7_m104_cr379_ZT_reduced.json", "format": "4x5x7", "rank": 104, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 91, "adds_V": 113, "adds_W": 175, "adds_total": 379, "naive_total": 931, "declared_reduced": 379, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=379, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
