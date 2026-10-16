# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: `cc -O2 -o src/{name} src/{source}` (table in src/README.md;
bpopt is built from src/bpopt_v1.c). The searches are time-capped random searches: re-running a command gives a valid
program but not necessarily the same one. The graph files listed are the actual outputs used; scheme.json is checkable
on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/3x4x5_m47_cr161_cn277_ZT_reduced.json` (sha256 d1248a3a32dd03bf...). Every product of scheme.json is a product of this file.

## 1. Driver runs that produced the map programs
tools/opt_scheme.py writes the map matrices (U: r x nm, V: r x mp, W^T: r x np for w_t jobs) and starts
one search process per job; job k gets seed = (sweep seed)*7 + k.

```
python tools/opt_scheme.py data/schemes/3x4x5_m47_cr161_cn277_ZT_reduced.json 60 1 work/bp60/3x4x5_m47
```

## 2. Per-map programs used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt work/bp60/3x4x5_m47/u_p.mat work/bp60/3x4x5_m47/u_p_bp.graph 7 60` | 1867de66ae82c658 | `best 38 iters 870914 K 47 N 12 D 36` |
| V | `nice -n 19 src/bpopt work/bp60/3x4x5_m47/v_p.mat work/bp60/3x4x5_m47/v_p_bp.graph 8 60` | cdf75a323f2659e1 | `best 44 iters 162095 K 47 N 20 D 33` |
| W | none: Perminov's own program from the base file, copied unchanged (`w_fresh`, `w`) | - | - |

Log lines give the search's own count before pruning unused nodes; for W it is the cost of the W^T program,
cost(W) = cost(W^T) + r - n*p after transposition (tools/graphs.py transpose).

## 3. Assembly into scheme.json
```
python3 tools/combine.py 3x4x5 47
python tools/package.py work/final/3x4x5_m47/strict.json work/final/3x4x5_m47/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor whose every intermediate
value is a ternary combination (strict), falling back to Perminov's own program when ours is not strictly better.

