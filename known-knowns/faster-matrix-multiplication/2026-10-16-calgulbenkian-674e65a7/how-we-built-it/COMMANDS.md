# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: `cc -O2 -o src/{name} src/{source}` (table in src/README.md;
bpopt is built from src/bpopt_v1.c). The searches are time-capped random searches: re-running a command gives a valid
program but not necessarily the same one. The graph files listed are the actual outputs used; scheme.json is checkable
on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/2x8x8_m100_cr424_cn608_ZT_reduced.json` (sha256 215daedef7b298b3...). Every product of scheme.json is a product of this file.

## 1. Driver runs that produced the map programs
tools/opt_scheme.py writes the map matrices (U: r x nm, V: r x mp, W^T: r x np for w_t jobs) and starts
one search process per job; job k gets seed = (sweep seed)*7 + k.

```
python tools/opt_scheme.py data/schemes/2x8x8_m100_cr424_cn608_ZT_reduced.json 60 1 work/bp60/2x8x8_m100
```

## 2. Per-map programs used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt work/bp60/2x8x8_m100/u_p.mat work/bp60/2x8x8_m100/u_p_bp.graph 7 60` | c5f5fcc562b2d478 | `best 90 iters 122259 K 100 N 16 D 90` |
| V | none: Perminov's own program from the base file, copied unchanged (`v_fresh`, `v`) | - | - |
| W | `nice -n 19 src/bpopt work/bp60/2x8x8_m100/w_t.mat work/bp60/2x8x8_m100/w_t_bp.graph 9 60` | 534998f5be93a0ca | `best 90 iters 121967 K 100 N 16 D 90` |

Log lines give the search's own count before pruning unused nodes; for W it is the cost of the W^T program,
cost(W) = cost(W^T) + r - n*p after transposition (tools/graphs.py transpose).

## 3. Assembly into scheme.json
```
python3 tools/combine.py 2x8x8 100
python tools/package.py work/final/2x8x8_m100/strict.json work/final/2x8x8_m100/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor whose every intermediate
value is a ternary combination (strict), falling back to Perminov's own program when ours is not strictly better.

