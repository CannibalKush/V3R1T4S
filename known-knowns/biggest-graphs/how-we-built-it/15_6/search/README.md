# (15,6) search code: N = 1 424 896

This folder holds the code that searched for the parameters of `G_15_6_n1424896`. The parameters are the two cut sets
and the 9 shortcut edges. The deterministic rebuild from those parameters lives one level up, in `../rebuild.py` and
`../compound.py`. This folder adds the steps that found the parameters.

## Input data (not redistributed)

Rishabh Rajiv, Zenodo record 10.5281/zenodo.23052995 (CC BY 4.0), file `data-and-verification.zip`. Unzip it into a
directory, `./rajiv` by default. Two files are used:

| file | sha256 |
|---|---|
| `graph_d15_k6_n1424472.edges.xz` | `5bbd5327f49631a94f41b3dea3b0d933f440c2bdb8e1db235c49a5e3be2c390f` |
| `witnesses/cs_d15_k6_n1424472.json` | `1d621e2b7be945ac11cf5ea2f85eaad83a1db1cdd1623b39334c818fd987baa9` |

## Scripts

| script | what it does |
|---|---|
| `cutsets.py` | Reads the H(11) incidence graph from block 0 of Rajiv's edge file, so it uses his labels. It then grows his cut sets by an iterated local search: (1,c)-swaps in the style of Andrade, Resende and Werneck for maximum independent set, random perturbation, and a restart from the best set after a stall. A point cut set must be pairwise non-collinear and a line cut set pairwise non-concurrent. The packing property is re-checked on output. |
| `../compound.py` | Rebuilds Rajiv's compound C(I;T,H) (his Definition 3) and self-tests it: with his own cut sets it must reproduce his published edge set exactly. It then cuts at the new sets, adds t new vertices (one point and one line per block) and joins them by a random 7-regular graph Y. This file is shared with the rebuild and is not duplicated here. |
| `assign_generic.py` | Runs an exact bit-parallel BFS from every new vertex to list the new-new pairs at distance > 6. For each such pair it adds one shortcut edge between two base vertices with free degree, using greedy placement plus WalkSAT-style ejections. It then re-evaluates exactly and writes the graph only if no far pair is left. |
| `toppairs.py` | `csr` and the numba BFS kernel `bad_pairs` used by `assign_generic.py`, copied without change from the original helper modules. |
| `run_search.sh` | All the steps below in one script. |

## Commands and seeds (as in the original run)

```
sh run_search.sh                          # RAJIV_DIR=./rajiv OUT=./out_15_6 PYTHON=python3 by default
USE_SHIPPED_CUTSETS=1 sh run_search.sh    # skip the cut-set search and use ../H11_points_s5.json, ../H11_lines_s1.json
```

| step | command (paths shortened) | seed | original result | original wall time |
|---|---|---|---|---|
| points | `cutsets.py --side points --iters 100000 --rounds 1 --stall 40000 --seed 5` | 5 | 7 679 points (Rajiv: 7 369) | 586 s |
| lines | `cutsets.py --side lines --iters 300000 --rounds 1 --stall 60000 --seed 1` | 1 | 7 648 lines (Rajiv: 7 226) | 2 048 s |
| build | `../compound.py --sp H11_points_s5.json --sl H11_lines_s1.json --t 7648 --seed 1` | 1 | N = 1 424 896, base sha256 `7ff1c677…8c36` | 257 s |
| shortcuts | `assign_generic.py --delta 15 --off 1417248 --t 7648 --D 6 --seed 1 --iters 3000000 --hours 0.5 --write_partial` | 1 | 9 far pairs, 9 shortcuts, final sha256 `554149b59ffe151197dff3ae48ae315596d9c618924d25db4775b1315ab47a75` | 355 s |

Both cut-set runs started from Rajiv's witness sets. The `--stall` values come from the original attempt's reproduction
notes; they are not in the run logs. `cutsets.py` uses numba's random stream: `np.random.seed` is called inside the
jitted kernel. The search was single-threaded; the BFS in `assign_generic.py` is multi-threaded. Hardware: a 10-core
Apple-silicon Mac that was shared with many other jobs at the time (load far above the core count), so the times are
only rough.

The pipeline's fallback stage (a re-attachment repair when shortcuts alone do not close every pair) was not needed for
this graph, so it is not included.

## What was confirmed and what was not

- Lineage: the shipped cut sets `../H11_points_s5.json` and `../H11_lines_s1.json` are byte-identical to the files
  these runs wrote. The original pipeline log shows compound.py writing base sha256 `7ff1c677…8c36`, then
  assign_generic finding 9 far pairs, placing 9 shortcuts, re-evaluating to 0 far pairs and writing the published
  sha256 `554149b5…7a75`. The shortcut list `../G_15_6_n1424896.shortcuts.npy` is the one from that run.
- Not rerun for this release: the cut-set searches take 10 to 35 minutes, and the build and shortcut steps need
  Rajiv's 1.4M-vertex graph. Only `py_compile` and `sh -n` were checked on these files. The cleaned copies change only
  comments, the usage text and one import line. `toppairs.py` holds the two helper functions verbatim.
- Not fully recoverable: the lines run (`H11_lines_s1.json`) started about 30 s before the last edit of `cutsets.py`
  was saved. Its log and JSON use an older output format, without `start_size` or the `--init` option. Whether the
  search kernel itself changed in that edit is not recorded. The shipped `cutsets.py` is the final version, which
  produced the points set. A rerun may therefore not give exactly 7 648 lines, and numba versions may differ too. The
  JSON files in `..` are the certificate. Any cut sets with at least 7 648 elements on each side work with
  `--t 7648`.
- Expected when `USE_SHIPPED_CUTSETS=1`: compound.py and assign_generic.py are deterministic for fixed inputs and
  seeds, so the run should end with sha256 `554149b5…7a75`. This end-to-end run was not repeated for this release.
  `../rebuild.py`, which uses the shipped shortcuts, was confirmed byte-identical at the time.

## Requirements

`requirements.txt`: Python 3.12.13 (macOS arm64) with numpy 2.5.3, pandas 2.3.3, numba 0.68.0 and llvmlite 0.50.0.

## Credits

The construction, the base graph and the witness files are by Rishabh Rajiv (Zenodo 10.5281/zenodo.23052995,
CC BY 4.0): the compound H_q(T_m), Definition 3, Lemmas 4 and 5, and the Theorem 3 surgery. The local-search moves follow
Andrade, Resende and Werneck's iterated local search for maximum independent set. The code was written by agents
during the search (Oct 2026) and only cleaned for this release; it contains no third-party code.
