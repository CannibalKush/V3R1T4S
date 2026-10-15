# Verification Receipts (`2026-10-14-anonymous-c6d1e0ab-710c8ff6`)

Command run from package root (`2026-10-14T01:30:09Z` to `2026-10-14T01:30:15Z`, macOS, Python 3.9.6, Apple clang):

```sh
sh verify-it-yourself/run_checks.sh
```

Output:
```text
== Checking object/13x15x15_r1763_Q.json
sha256 matches INDEX.csv (710c8ff6593f7c6e578a9ae83b4d7083ed5381db72fd734e614a3108d7c87465)
PASS file=13x15x15_r1763_Q.json format=13x15x15 rank=1763 primes=2 log2_bound=48
rank 1763 matches INDEX.csv
== Running negative control (mutated coefficient must FAIL)
negative control rejected as expected
ALL CHECKS PASS
```

| File | Format | Brent Equations Checked | Primes ($p \approx 2^{30}$) | $\log_2(\prod p)$ | $\log_2(2 L (S + 1))$ | Violations | Nonzero Rank-1 Terms | SHA-256 Matches `INDEX.csv` | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| `object/13x15x15_r1763_Q.json` | `(13, 15, 15)` | $195 \times 225 \times 195 = 8,555,625$ | $2$ | $60.0$ | $48$ | $0$ | $1763$ | yes | `PASS` |
