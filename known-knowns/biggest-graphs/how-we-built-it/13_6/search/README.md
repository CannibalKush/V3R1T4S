# (13,6) search code: N = 535 495

This folder holds the code that searched for the parameters of `G_13_6_n535495`. The parameters are the relaxed cut sets,
the attachments, the random graph Y and the 2 643 shortcut edges. The deterministic rebuild from the certificate lives
one level up, in `../rebuild13.py` and `../compound.py`. This folder adds the steps that produced that certificate.

## Input data (not redistributed)

Rishabh Rajiv, Zenodo record 10.5281/zenodo.23052995 (CC BY 4.0), file `data-and-verification.zip`. Unzip it into a
directory, `./rajiv` by default. Two files are used:

| file | sha256 |
|---|---|
| `graph_d13_k6_n534234.edges.xz` | `c86346b121a6f24591ae12dbf0a9f8dfb4a82f3c8cea25339c11139140b95bae` |
| `witnesses/cs_d13_k6_n534234.json` | `796e0be7453d2437293112c18bfb3f13fb3e5e126f4116e230f9b11d56bce1a9` |

## Scripts

| script | what it does |
|---|---|
| `cutsets.py` | Iterated local search for larger strict cut sets of H(9): pairwise non-collinear points and pairwise non-concurrent lines, in Rajiv's block-0 labels. It is the same file as `../../15_6/search/cutsets.py`. |
| `relax_greedy.py` | Adds "mild" extra cut elements to a strict set: each extra element shares a line (or point) with exactly one cut element, and no line (or point) holds more than two. It runs 12 randomized min-conflict greedy restarts with numpy `default_rng(7)` and keeps the best. |
| `relaxed13.py` | Rebuilds Rajiv's compound with `../compound.py` and cuts it at the relaxed sets. It then adds t new vertices, each with one point and one line of every block at free slots, and joins them by a random 5-regular graph Y, using `default_rng(seed)`. Lemma 5 does not hold for relaxed sets, so the result must be checked all-pairs. |
| `xchk.c` | Exact all-pairs diameter checker in C with pthreads. With `XCHK_DUMP=FILE` it also lists every far pair. |
| `exact_sc.py` | Exact shortcut repair. For each listed far pair (x, y) it runs a BFS from x and from y and picks two free base vertices s1, s2 with d(x,s1) + d(y,s2) <= 5, then adds the edge s1-s2. The pairs are processed in a `default_rng(1)` shuffle of the file order. At the end it re-evaluates all new-new pairs exactly. |
| `newpairs.py` | `bad_new`, the numba BFS over all new-vertex sources, and `csr`, used by `exact_sc.py`. Both are copied without change from the original helper module. |
| `run_search.sh` | All the steps below in one script. |
| `inputs/` | Small intermediate files from the original run (see below). |

## Commands and seeds (as in the original run)

```
sh run_search.sh                                    # RAJIV_DIR=./rajiv OUT=./out_13_6 THREADS=6 by default
FROM_X1=1 USE_SHIPPED_PAIRS=1 sh run_search.sh      # the reproducible part only (about 10 min)
```

| step | command (paths shortened) | seed | original result | original wall time |
|---|---|---|---|---|
| strict points | `cutsets.py --side points --iters 1000000 --seed 77 --init inputs/H9_points_r2.json` | 77 | 3 924 -> 3 928 (`inputs/H9_points_x1.json`) | 1 278 s |
| strict lines | `cutsets.py --side lines --iters 1000000 --seed 77 --init inputs/H9_lines_r1.json` | 77 | 3 940 -> 3 949 (`inputs/H9_lines_x1.json`) | 1 463 s |
| relax points | `relax_greedy.py points H9_points_x1.json SP_relaxed_v1.json 12` | rng 7 | 3 928 + 127 = 4 055 | about 21 s |
| relax lines | `relax_greedy.py lines H9_lines_x1.json SL_relaxed_v1.json 12` | rng 7 | 3 949 + 118 = 4 067 | about 21 s |
| build | `relaxed13.py --sp SP_relaxed_v1.json --sl SL_relaxed_v1.json --kp 0 --kl 0 --seed 1 --t 4055` | 1 | N = 535 495, M = 3 472 571, sha256 `d1ed618b3e777920d89ae335b623c9e7dacf522b837d564ba7ee11c8c3664e49` | 19 s |
| far pairs | `XCHK_DUMP=bad.txt xchk G.edges 13 6 6` | - | INVALID: 3 179 far unordered pairs, all new-new | 197 s |
| shortcuts | `exact_sc.py G.edges 13 531440 G.esc.edges --threads 6 --quiet --rebuild-every 100 --pairs bad.txt` | rng 1 | 536 pairs already fixed by earlier shortcuts, 2 643 added; sha256 `4ed4fc62000b3cbc6c23b08d9db4af383aa28b01e69fc802b5b1bbdbab170e94` | 138 s |
| final check | `xchk G.esc.edges 13 6 6` | - | VALID, all 535 495 eccentricities = 6 | 137 s |

Offset 531440 is the number of base vertices, 2 · 4 · 66 430. Hardware: a 10-core Apple-silicon Mac that was shared with
many other jobs at the time (load around 125), so the times are only rough. The relax_greedy command line was not logged.
It is inferred from its log and from the `base_file` field in its output JSON, and the rerun below matches it.

### Where the warm starts came from (earlier runs of the same `cutsets.py`, Rajiv's H(9) data)

| file | how it was made | result |
|---|---|---|
| `H9_points_test.json` (not shipped) | Rajiv's 3 875 points, `--iters 200000 --seed 1`, 1 round, 359 s | 3 906 |
| `inputs/H9_points_r2.json` | `--init H9_points_test.json --iters 300000 --rounds 3 --seed 11` (round r uses seed 11 + 1000 r), 1 654 s | 3 924 |
| `inputs/H9_lines_r1.json` | Rajiv's 3 878 lines, `--iters 300000 --rounds 3 --seed 21`, 1 820 s | 3 940 |

The `--stall` value is not recorded for any H(9) run: not for these three and not for the two seed-77 runs.
`run_search.sh` uses the script default (200 000). `H9_points_test.json` came from an earlier version of `cutsets.py`;
its JSON lacks the `start_size` field that the final version writes.

## What was confirmed and what was not

Reruns made for this release used the repo copies, from a scratch directory, single-threaded, with the shipped
`inputs/` and Rajiv's files listed above:

- `relax_greedy.py points` and `lines`, about 14 s each, gave the same restart logs and the same 127 / 118 extras. The
  sets are element-for-element identical to `../SP_relaxed_t4055.json` and `../SL_relaxed_t4055.json`.
- `relaxed13.py ... --seed 1 --t 4055` reproduced sha256 `d1ed618b…4e49` exactly, in 9 s.
- `exact_sc.py` on that graph with `inputs/far_pairs_t4055.txt` and `--threads 1` took 77 s. It reported 536 pairs
  already fixed, 2 643 shortcuts added (the same array as the original run) and 0 far new-new pairs. It wrote sha256
  `4ed4fc62000b3cbc6c23b08d9db4af383aa28b01e69fc802b5b1bbdbab170e94`, the published graph, byte for byte.

So steps 2 to 5 are confirmed to regenerate `G_13_6_n535495` from `inputs/H9_*_x1.json` and Rajiv's files.

Not rerun: the seed-77 cut-set searches (20 to 25 minutes each) and the xchk runs.

Not recoverable or not deterministic:
- The `--stall` values of the H(9) cut-set runs (see above). Numba's random stream can also change between versions. A
  rerun of step 1 may therefore not give exactly 3 928 / 3 949. The shipped `inputs/H9_*_x1.json` are the files the
  original run wrote (`FROM_X1=1` starts from them).
- The order of the XCHK_DUMP far-pair list depends on thread scheduling, but the set of pairs does not. `exact_sc.py`
  shuffles the pairs in that file order, so a fresh dump can give different shortcuts and a different final sha256.
  The graph should still be valid; that is checked by the final xchk. `inputs/far_pairs_t4055.txt` (3 179 lines, sha256
  `659e8c8a76ab0a59c68fcd820e2c3ac63035ce91c8cccd3e0b36723a00d99299`) is the list from the original run. Use it
  (`USE_SHIPPED_PAIRS=1`) to reproduce the published graph byte for byte.

## Requirements

`requirements.txt`: Python 3.12.13 (macOS arm64) with numpy 2.5.3, pandas 2.3.3, numba 0.68.0 and llvmlite 0.50.0.
`xchk.c` needs a C11 compiler with pthreads; the original run used Apple clang 21.0.0 with `cc -O3 -march=native -lpthread`.

## Credits

The construction, the base graph and the witness files are by Rishabh Rajiv (Zenodo 10.5281/zenodo.23052995,
CC BY 4.0): the compound H_q(T_m), Definition 3, Lemmas 4 and 5, and the Theorem 3 surgery. The local-search moves in
`cutsets.py` follow Andrade, Resende and Werneck's iterated local search for maximum independent set. The relaxed cut
sets, the exact shortcut repair and the code were made by agents during the search (Oct 2026) and only cleaned
for this release; there is no third-party code.
