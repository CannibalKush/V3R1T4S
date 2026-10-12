# (15,4), N = 13365: search code for the construction data

This folder holds the search that produced `../state_Z11x2Z30.json` (the group, the three generators and the
matrices A_t, vectors b_t over F_3^4). The (15,4) graph itself is then built from that file by
`../gen_G_15_4_direct.py` (quotient of the 26,730-vertex lift by the automorphism described in that script).

## Scripts

| file | role |
|---|---|
| `exh_bip.py` | Step 1. Exhaustive scan of generator triples (a, b, c) of the group Z_11 x\|_2 Z_30 (c an involution, all three outside the index-2 subgroup). For each triple it counts the group elements that the alphabet {a, a^-1, b, b^-1, c} cannot reach with reduced words of the right parity and length (2 or 4 for even elements, 1, 3 or 5 for odd ones). Prints the best triples. Deterministic (numba, parallel loop over a). |
| `bip_proxy_search.py` | Step 2. Simulated annealing over the matrices A_t and vectors b_t for fixed generators. Each restart anneals a fast rank score (`rankproxy.py`); the result is then checked by an exact bitset BFS from the 81 sources (e, x), cap 5. Stops at the first chart with exact defect 0 and writes the state JSON. |
| `rcl.py` | Linear algebra mod q, random invertible matrices / involutions, bitset BFS defect (numba). |
| `rcl2.py` | Group parsing (`meta:m,k,r` etc.), the `Lift` class (chart sampling, tweaks, neighbour table, state export). |
| `rankproxy.py` | Reduced words, their endpoints in the group, and the rank of each word's controllability matrix over F_q. |
| `rcl_bip.py` | Parity homomorphism of the group (colour of the bipartite lift). |
| `groups.py` | Finite groups as multiplication tables. |

`rcl2.py` and `rcl_bip.py` are library copies; their own command-line drivers (not used for this graph) were removed.
Nothing else was changed apart from docstrings; algorithms, constants and seeds are as in the original run.

## Commands (run from this folder)

```bash
pip install -r requirements.txt
export NUMBA_CACHE_DIR=/some/scratch/dir   # numba's cache=True would otherwise write __pycache__ here
# step 1: generator scan (deterministic)
python exh_bip.py --group meta:11,30,2 --top 10 --out scan.jsonl
#   {"group": "meta:11,30,2", "n": 330, "min_hard": 0, "n_ok": 110, "best": [[0, 3, 35, 195], [0, 3, 65, 45], ...]}
# step 2: chart search on the first triple, seed 77
python bip_proxy_search.py --group meta:11,30,2 --gens '[3,35,195]' --minutes 40 --seed 77 --out state.json
#   {"restart": 0, "proxy": 0, "exact": 0}  {"FOUND": true, "N": 26730}  {"final": 0}
shasum -a 256 state.json
#   4d70ce9be3bb26bfbb4dc76906d425008f5b3b6893ec9c059be12637c4a8c4a0  (= ../state_Z11x2Z30.json)
# step 3: the (15,4) graph
python ../gen_G_15_4_direct.py state.json G_15_4.edges
```

`--minutes` is only a time limit; the search stops as soon as it finds a defect-0 chart (restart 0 for seed 77).
`--spec` defaults to `pair3,pair3,inv3` (each letter pair contributes 3+3 edges, the involution 3; degree 15).

## Rerun check (from these copies)

Apple M5, Python 3.12.13, `NUMBA_NUM_THREADS=1`, cold numba cache:

| step | runtime | result |
|---|---|---|
| `exh_bip.py` | 9 s | same `best` list as the original run (first triple [3, 35, 195]) |
| `bip_proxy_search.py --seed 77` (run with `--minutes 5`) | 25 s | found at restart 0; output byte-identical to `../state_Z11x2Z30.json` (sha256 above) |

The original run used 2 to 3 numba threads; step 1 took about 10 s and step 2 found the chart at restart 0 within
about 2.5 minutes. The result does not depend on the thread count. Other numpy versions could in principle change the
random stream of `numpy.random.default_rng`; the versions used are pinned in `requirements.txt`.

## Packages

Python 3.12.13; numpy 2.5.3, numba 0.68.0 (llvmlite 0.50.0). See `requirements.txt`.

## Credits

The construction is a route-chart lift of a Cayley graph, following the method of R. Mizuno,
arXiv:2606.15860, Appendix A.4. The code here is an independent reimplementation; no code from Mizuno's
repository (github.com/rmizuno42/ddp) is included.
