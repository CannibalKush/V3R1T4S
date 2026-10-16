# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: `cc -O2 -o src/{name} src/{source}` (table in src/README.md;
bpopt is built from src/bpopt_v1.c). The searches are time-capped random searches: re-running a command gives a valid
program but not necessarily the same one. The graph files listed are the actual outputs used; scheme.json is checkable
on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/5x6x8_m170_cr720_fv345_cn2312_ZT_reduced.json` (sha256 d448e0b5c4977193...). Every product of scheme.json is a product of this file.

## 1. Driver runs that produced the map programs
tools/opt_scheme.py writes the map matrices (U: r x nm, V: r x mp, W^T: r x np for w_t jobs) and starts
one search process per job; job k gets seed = (sweep seed)*7 + k.

```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py data/schemes/5x6x8_m170_cr720_fv345_cn2312_ZT_reduced.json 150 5 work/top150/5x6x8_m170
```

## 2. Per-map programs used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/top150/5x6x8_m170/u_p_bp5b.mat work/top150/5x6x8_m170/u_p_bp5b.graph 36 150` | 2fb6df013bc9b1c3 | `best 159 iters 3613 K 170 N 30 D 149` |
| V | `nice -n 19 src/bpopt5 work/top150/5x6x8_m170/v_p_bp5a.mat work/top150/5x6x8_m170/v_p_bp5a.graph 37 150` | e7708703e616bfc1 | `best 196 iters 1626 K 170 N 48 D 157` |
| W | `nice -n 19 src/bpopt6 work/top150/5x6x8_m170/w_t_bp6s.mat work/top150/5x6x8_m170/w_t_bp6s.graph 39 150 30 0.8 1 1` | 812e57fb31fe3338 | `best 182 iters 1470 K 170 N 40 D 157` |

Log lines give the search's own count before pruning unused nodes; for W it is the cost of the W^T program,
cost(W) = cost(W^T) + r - n*p after transposition (tools/graphs.py transpose).

## 3. Assembly into scheme.json
```
python3 tools/combine.py 5x6x8 170
python tools/package.py work/final/5x6x8_m170/strict.json work/final/5x6x8_m170/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor whose every intermediate
value is a ternary combination (strict), falling back to Perminov's own program when ours is not strictly better.

