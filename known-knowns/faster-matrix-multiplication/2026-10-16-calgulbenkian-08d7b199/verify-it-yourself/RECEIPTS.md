# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (08d7b199e9ecc9f7254dc46c23ecf2128e83444277b19eac6bbcb678a107f819)
== check_slp.py on object/4x5x5_m76_cr281_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x5x5_m76_cr281_ZT_reduced.json", "format": "4x5x5", "rank": 76, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 75, "adds_V": 84, "adds_W": 122, "adds_total": 281, "naive_total": 530, "declared_reduced": 281, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=281, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
