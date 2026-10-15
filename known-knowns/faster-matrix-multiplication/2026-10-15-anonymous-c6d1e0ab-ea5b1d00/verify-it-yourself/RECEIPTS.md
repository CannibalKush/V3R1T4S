# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (ea5b1d00e3702536a57a8598f0f09040f99b503e844d5018556128ac81d0a097)
== check_slp.py on object/5x6x6_m130_cr502_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x6x6_m130_cr502_ZT_reduced.json", "format": "5x6x6", "rank": 130, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 129, "adds_V": 147, "adds_W": 226, "adds_total": 502, "naive_total": 1716, "declared_reduced": 502, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=502, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
