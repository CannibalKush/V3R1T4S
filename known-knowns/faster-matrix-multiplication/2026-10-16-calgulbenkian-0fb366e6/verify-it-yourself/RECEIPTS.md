# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (0fb366e6a2a5cc6bc6fd0b31334b1d859df86c180c0fc30759cbbd41c4867501)
== check_slp.py on object/5x8x8_m230_cr929_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x8x8_m230_cr929_ZT_reduced.json", "format": "5x8x8", "rank": 230, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 205, "adds_V": 327, "adds_W": 397, "adds_total": 929, "naive_total": 2747, "declared_reduced": 929, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=929, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
