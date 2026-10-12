# (9,4), N = 1700: voltage search

These scripts produce the plain-text inputs of [`../rebuild_1700.py`](../rebuild_1700.py):
[`../voltage_q7_Z2.txt`](../voltage_q7_Z2.txt), [`../spread_q7.txt`](../spread_q7.txt),
[`../W7_points.txt`](../W7_points.txt) and [`../W7_lines.txt`](../W7_lines.txt). They also write the edge list
directly.

## Files

| file | what it does |
|---|---|
| `gq4.py` | Builds the incidence graph of the generalized quadrangle W(7) in the GF(7^4) model, with the symplectic form B(x,y) = Tr(delta x y^(q^2)). It also builds the cyclic automorphism omega = theta^48 (order 50 in GF(7^4)^*; it acts semiregularly on points, lines and flags, with orbits of size 25) and the regular spread of 50 lines. `python gq4.py 7` runs a self-test that uses `gq.py`. |
| `gq.py` | An independent coordinate model of W(q). Only the `gq4.py` self-test uses it. |
| `vsearch.py` | Numba helpers: geodesic enumeration on the incidence graph and `count_bad`, which counts the opposite pairs that break the covering condition (C4). The functions are verbatim from the original file. The plain WalkSAT search in that file served another table cell and is omitted. |
| `symsearch.py` | The search that was actually run. Z_2 voltages are held constant on the 128 omega-orbits of flags. WalkSAT works on the reduced instance: 10,976 constraints, one for each pair (u, w) where u is an orbit representative and w is opposite u. The script expands the best solution to all 3,200 incidences and re-checks it on all 137,200 opposite pairs. It writes an `.npz` (alpha, orbits, lines, spread, adjacency). |
| `lam.py` | Builds the graph from the `.npz`. The graph is the K_2-fibre lift with the point fibres deleted, plus twins of the line copies over the spread, plus twin fibres. Order 4*400 + 2*50 = 1700, 9-regular. |
| `export_txt.py` | **Written for this release, not part of the original run.** The original run did not keep the script that wrote the four `.txt` files. This converter writes them from the `.npz`, and it reproduces all four shipped files byte for byte (checked on both the published `.npz` and the rerun one). |

## Commands (seed 1)

```bash
pip install -r requirements.txt
python symsearch.py --q 7 --n 2 --seed 1 --steps 100000 --restarts 10 --out sym_q7_n2_s1.npz
python lam.py sym_q7_n2_s1.npz G_9_4_n1700.edges
python export_txt.py sym_q7_n2_s1.npz --outdir txt     # voltage_q7_Z2.txt spread_q7.txt W7_points.txt W7_lines.txt
shasum -a 256 sym_q7_n2_s1.npz G_9_4_n1700.edges txt/*
```

Numba caches compiled code next to the scripts (`__pycache__/`) unless `NUMBA_CACHE_DIR` is set.

Expected log: `q=7 n=2 flag orbits 128, reps 32, reduced constraints 10976`, then `restart 0 reduced bad 0`,
`full check: violated opposite pairs = 0`, `done best 0`.

| output | sha256 |
|---|---|
| `sym_q7_n2_s1.npz` | `de4b89aeb9c827de6787fcc2499dae7e29a3d9913b55b34dbc7901c02b7cebe1` |
| `G_9_4_n1700.edges` (= [`graphs/G_9_4_n1700.edges`](../../../graphs/G_9_4_n1700.edges)) | `d271a1e84aa9539ba47f8d036cd15e4a5a9ccc5a4752d0dacc94a9d35f17eebd` |
| `txt/voltage_q7_Z2.txt` | `80985e8d25ed81f7b27216b7dba3cf0fbed32c7d3651eb91a5aaa381ad024172` |
| `txt/spread_q7.txt` | `8d9d9f727d6975868f6b3773c1cab5f1bbabc35da42a44d29cfba8b89addda13` |
| `txt/W7_points.txt` | `8dab91849f30b4e74bd2b717d755054eb5cfd535e352f2f872c9cc196673114d` |
| `txt/W7_lines.txt` | `f3a6efe49c3c26b2f6b72f2f604476a61f599f5c0a1505517bb8dc27f23ee487` |

**Determinism.** Restart r seeds the numba WalkSAT with `1000*seed + r`, and its starting point comes from `numpy.random.default_rng(seed)`. The walk stops as soon as no constraint is violated. Seed 1 solves the instance in restart 0, inside the 100,000-step limit. A larger `--steps` value, such as the default 200,000 in the script, therefore gives the same output.

The original run took about 100 s. A rerun from these repo copies used one thread (`NUMBA_NUM_THREADS=1`), Python 3.12.13 and the versions below on an Apple M5 Mac. It took 47 s wall-clock, including about 16 s of numba compilation and instance setup. It reproduced the `.npz` byte for byte and gave the same arrays. The edge list and all four `.txt` files had the sha256 values above.

## Packages

Python 3.12.13; `numpy==2.5.3`, `numba==0.68.0` (with `llvmlite==0.50.0`), `galois==0.4.11` (see `requirements.txt`).

## Third-party credits

- **galois**, by M. Hostetter. MIT license. Used for GF(7^4) arithmetic in `gq4.py` and `export_txt.py`, and for GF(q) in `gq.py`.
- **Numba**: BSD-2-Clause. **llvmlite**: BSD-2-Clause, with the Apache-2.0 LLVM exception for the bundled LLVM. **NumPy**: BSD-3-Clause.
- W(q) and its regular spread are classical (Payne and Thas, *Finite Generalized Quadrangles*).
