# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (4abbbac3ec7576e4a03ff6ab7110dd4c99e8c564724a8c2eba3b26c4e2231a47)
== check_slp.py on object/6x6x6_m153_cr588_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "6x6x6_m153_cr588_ZT_reduced.json", "format": "6x6x6", "rank": 153, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 159, "adds_V": 157, "adds_W": 272, "adds_total": 588, "naive_total": 2182, "declared_reduced": 588, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=588, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
