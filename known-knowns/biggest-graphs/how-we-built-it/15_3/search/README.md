# (15,3), N = 1620: search code for the controller and the route chart

This folder holds the search that produced `../controller_own_k5_n60.adj` and `../G_15_3_n1620.params.json`, from
which `../rebuild_route_chart.py` builds the graph.

## Scripts

| file | role |
|---|---|
| `vsa5.py` | Step 1. Simulated annealing for a 5-regular "W3 controller" on 60 vertices: every non-adjacent ordered pair (u, v), u = v included, must be joined by a walk of length exactly 3. The controller is a Z_15-voltage lift of a 4-vertex base multigraph; base edges and voltages are annealed. Writes `prefix.json` (base data, voltages, edge list). |
| `k5sat.py` | Step 2. Exact SAT model (CaDiCaL via python-sat): chooses a perfect matching M of the controller and, on every M-edge, which turns are singular, so that every non-adjacent ordered pair keeps a usable 3-walk. Then realises the transports T, builds the lift over F_3^3 and checks it by exact all-pairs bitset BFS. Writes `prefix.k5sat.json` and, if the lift has diameter 3, `prefix.edges.txt`. Deterministic. |
| `make_params.py` | Step 3. Converts the two outputs into the published `.adj` and `.params.json` files (adds w = T d mod 3 and the voltage data). |
| `w3sa.py` | `w3_cost` (W3 deficit, numba). |
| `vlift_w3.py` | `make_group` (multiplication tables, here Z15). |
| `rcl3.py` | F_q arithmetic, pencils, lift construction, bitset BFS. |
| `typed_chart.py` | `TransportFinder` (transport matrices with prescribed singular turns). |

`w3sa.py`, `vlift_w3.py` and `typed_chart.py` keep only the functions used here; the rest of the original modules
(annealers and drivers for other designs) was removed. In `k5sat.py` the output field `controller_source` now holds
the file name instead of an absolute path. Algorithms, constants and seeds are unchanged.

Step 3 was done by hand when the graph was found; no script for it was saved. `make_params.py` was written for this
release; it reproduces both published files byte for byte (checked on the original search outputs and on the rerun
below). The description text inside the params file is copied verbatim from the published file.

## Commands (run from this folder)

```bash
pip install -r requirements.txt
export NUMBA_CACHE_DIR=/some/scratch/dir   # numba's cache=True would otherwise write __pycache__ here
# step 1: controller (deficit 0 at restart 1)
python vsa5.py --b 4 --group Z15 --k 5 --iters 1000000 --restarts 30 --seed 5 --out c60
# step 2: route chart (exact SAT) and the lift
python k5sat.py c60.json --out k5
#   n=60: 2550 variables, 14760 clauses (3300 pair clauses)  SAT: True
#   lift: N=1620, edges=12150, degree 15..15, ordered pairs at distance > 3: 0   SUCCESS
shasum -a 256 k5.edges.txt
#   da9faa8c8a875ac789506ca3f91a45db37b3f1f3952b729c88199557caa792ce  (= ../../../graphs/G_15_3_n1620.edges.txt)
# step 3: published parameter files
python make_params.py c60.json k5.k5sat.json --adj controller_own_k5_n60.adj --params G_15_3_n1620.params.json
shasum -a 256 controller_own_k5_n60.adj G_15_3_n1620.params.json
#   83db2c54d0d764f9bc20f7e1498edda882441fbeafa0ab57c9ee84913e094de2  controller_own_k5_n60.adj
#   ccbecf951e9e4cc8d3847317a975e71dfa8dafebb461054a293a9f5d97c12ea2  G_15_3_n1620.params.json
```

## Rerun check (from these copies)

Apple M5, Python 3.12.13, `NUMBA_NUM_THREADS=1`, cold numba cache:

| step | runtime | result |
|---|---|---|
| `vsa5.py --seed 5` | 16 s | deficit 0 at restart 1; `c60.json` byte-identical to the original search output |
| `k5sat.py` | 1.2 s | SAT; same chart as the original (all fields equal except `controller_source`); edge list sha256 `da9faa8c...92ce` |
| `make_params.py` | < 1 s | both published files reproduced byte for byte (sha256 above) |

The original controller search took about 75 s per restart (deficit 0 at restart 1, about 150 s in total).

## Packages

Python 3.12.13; numpy 2.5.3, numba 0.68.0 (llvmlite 0.50.0), networkx 3.7, python-sat 1.9.dev15. See
`requirements.txt`.

## Credits

- Route-chart lifts over a controller graph follow the method of R. Mizuno, arXiv:2606.15860. The code here is an
  independent implementation; no code from Mizuno's repository (github.com/rmizuno42/ddp) is included.
- SAT solving: python-sat (PySAT) by A. Ignatiev, J. Marques-Silva and A. Morgado, MIT license (from the installed
  package metadata), using its bundled CaDiCaL 1.5.3 solver (`Cadical153`) by A. Biere et al. PySAT is a dependency
  only; none of its code is copied here.
