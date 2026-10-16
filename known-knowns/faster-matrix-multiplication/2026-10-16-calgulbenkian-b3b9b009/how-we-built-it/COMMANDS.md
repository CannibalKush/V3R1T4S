# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: `cc -O2 -o src/{name} src/{source}` (table in src/README.md;
bpopt is built from src/bpopt_v1.c). The searches are time-capped random searches: re-running a command gives a valid
program but not necessarily the same one. The graph files listed are the actual outputs used; scheme.json is checkable
on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/4x5x7_m104_cr400_fv163_cn931_ZT_reduced.json` (sha256 0c4cb3e3de6b9a82...). Every product of scheme.json is a product of this file.

## 1. Driver runs that produced the map programs
tools/opt_scheme.py writes the map matrices (U: r x nm, V: r x mp, W^T: r x np for w_t jobs) and starts
one search process per job; job k gets seed = (sweep seed)*7 + k.

```
python tools/opt_scheme.py data/schemes/4x5x7_m104_cr400_fv163_cn931_ZT_reduced.json 60 1 work/bp60/4x5x7_m104
```

## 2. Per-map programs used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt work/bp60/4x5x7_m104/u_p.mat work/bp60/4x5x7_m104/u_p_bp.graph 7 60` | ddf326a77bcbec29 | `best 91 iters 16407 K 104 N 20 D 85` |
| V | `nice -n 19 src/bpopt work/bp60/4x5x7_m104/v_p.mat work/bp60/4x5x7_m104/v_p_bp.graph 8 60` | 84d473a6029f6aee | `best 113 iters 2275 K 104 N 35 D 90` |
| W | `nice -n 19 src/bpopt work/bp60/4x5x7_m104/w_t.mat work/bp60/4x5x7_m104/w_t_bp.graph 9 60` | 2d8c4bef420ade6a | `best 99 iters 7558 K 104 N 28 D 85` |

Log lines give the search's own count before pruning unused nodes; for W it is the cost of the W^T program,
cost(W) = cost(W^T) + r - n*p after transposition (tools/graphs.py transpose).

## 3. Assembly into scheme.json
```
python3 tools/combine.py 4x5x7 104
python tools/package.py work/final/4x5x7_m104/strict.json work/final/4x5x7_m104/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor whose every intermediate
value is a ternary combination (strict), falling back to Perminov's own program when ours is not strictly better.

