# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: `cc -O2 -o src/{name} src/{source}` (table in src/README.md;
bpopt is built from src/bpopt_v1.c). The searches are time-capped random searches: re-running a command gives a valid
program but not necessarily the same one. The graph files listed are the actual outputs used; scheme.json is checkable
on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/4x4x7_m85_cr319_fv119_cn631_ZT_reduced.json` (sha256 dc7b4ef436d90acd...). Every product of scheme.json is a product of this file.

## 1. Driver runs that produced the map programs
tools/opt_scheme.py writes the map matrices (U: r x nm, V: r x mp, W^T: r x np for w_t jobs) and starts
one search process per job; job k gets seed = (sweep seed)*7 + k.

```
python tools/opt_scheme.py data/schemes/4x4x7_m85_cr319_fv119_cn631_ZT_reduced.json 60 1 work/bp60/4x4x7_m85
```

## 2. Per-map programs used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt work/bp60/4x4x7_m85/u_p.mat work/bp60/4x4x7_m85/u_p_bp.graph 7 60` | 307b87dcc04c017a | `best 72 iters 324497 K 85 N 16 D 71` |
| V | `nice -n 19 src/bpopt work/bp60/4x4x7_m85/v_p.mat work/bp60/4x4x7_m85/v_p_bp.graph 8 60` | c304110108743f8b | `best 83 iters 17492 K 85 N 28 D 68` |
| W | `nice -n 19 src/bpopt work/bp60/4x4x7_m85/w_t.mat work/bp60/4x4x7_m85/w_t_bp.graph 9 60` | 6e77319b3f6cbaeb | `best 82 iters 27853 K 85 N 28 D 68` |

Log lines give the search's own count before pruning unused nodes; for W it is the cost of the W^T program,
cost(W) = cost(W^T) + r - n*p after transposition (tools/graphs.py transpose).

## 3. Assembly into scheme.json
```
python3 tools/combine.py 4x4x7 85
python tools/package.py work/final/4x4x7_m85/strict.json work/final/4x4x7_m85/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor whose every intermediate
value is a ternary combination (strict), falling back to Perminov's own program when ours is not strictly better.

