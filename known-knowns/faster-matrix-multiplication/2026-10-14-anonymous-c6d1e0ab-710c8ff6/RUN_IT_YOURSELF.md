# Run It Yourself

## 1. Verify the Shipped Object (`object/13x15x15_r1763_Q.json`)

From a fresh shell inside this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
== Checking object/13x15x15_r1763_Q.json
sha256 matches INDEX.csv (710c8ff6593f7c6e578a9ae83b4d7083ed5381db72fd734e614a3108d7c87465)
PASS file=13x15x15_r1763_Q.json format=13x15x15 rank=1763 primes=2 log2_bound=48
rank 1763 matches INDEX.csv
== Running negative control (mutated coefficient must FAIL)
negative control rejected as expected
ALL CHECKS PASS
```

You can also run the standalone verifier directly:
```sh
python3 verify-it-yourself/verify_brent.py object/13x15x15_r1763_Q.json
```

## 2. How to Rebuild `object/13x15x15_r1763_Q.json` from `14x15x15_r1842_Q.json`

From the V3R1T4S workspace root (where `repo/known-knowns/faster-matrix-multiplication/schemes/14x15x15_r1842_Q.json` and `repo/known-knowns/faster-matrix-multiplication/how-we-built-it/peel.py` are present):

```sh
python3 runs/2026-10-14-0004/attempts/representation-absorber/code/make_result_13x15x15.py
```

This executes the two exact algebraic steps:
1. Generalised one-slice peel of `14x15x15_r1842_Q.json` along `axis=0` with $e = e_1 + e_7, f = e_7$, annihilating $46$ terms ($1842 \to 1796$).
2. Exact 20-dimensional $(V \otimes W)$ left-nullspace extraction over $\mathbb{Q}$ and Rado–Edmonds matroid max-kill $U$-factor shifting (`how-we-built-it/screen_all.py`), annihilating $33$ terms ($1796 \to 1763$) and producing `13x15x15_r1763_Q.json` with exact SHA-256 `710c8ff6593f7c6e578a9ae83b4d7083ed5381db72fd734e614a3108d7c87465`.
