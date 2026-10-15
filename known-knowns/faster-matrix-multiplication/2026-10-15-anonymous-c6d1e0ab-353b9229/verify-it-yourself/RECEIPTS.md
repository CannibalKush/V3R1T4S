# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (353b922983ecc35f13d03a9e7136407be941d5a3282630c9eb9c13af94c236ec)
== check_slp.py on object/6x8x8_m266_cr993_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "6x8x8_m266_cr993_ZT_reduced.json", "format": "6x8x8", "rank": 266, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 255, "adds_V": 274, "adds_W": 464, "adds_total": 993, "naive_total": 3788, "declared_reduced": 993, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=993, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
