# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: `cc -O2 -o src/{name} src/{source}` (table in src/README.md;
bpopt is built from src/bpopt_v1.c). The searches are time-capped random searches: re-running a command gives a valid
program but not necessarily the same one. The graph files listed are the actual outputs used; scheme.json is checkable
on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json` (sha256 7a273fbb34339b61...). Every product of scheme.json is a product of this file.

## 1. Driver runs that produced the map programs
tools/opt_scheme.py writes the map matrices (U: r x nm, V: r x mp, W^T: r x np for w_t jobs) and starts
one search process per job; job k gets seed = (sweep seed)*7 + k.

```
JOBSET=w:t:bp6s,w:t:bp6t,u:p:bp5a,v:p:bp5a,v:p:bp5b,u:p:bp5b python tools/opt_scheme.py data/schemes/4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json 150 8 work/strictW/4x5x8_m118
```

## 2. Per-map programs used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/strictW/4x5x8_m118/u_p_bp5b.mat work/strictW/4x5x8_m118/u_p_bp5b.graph 61 150` | 6976f5e11e4d72f2 | `best 102 iters 59884 K 118 N 20 D 98` |
| V | `nice -n 19 src/bpopt5 work/strictW/4x5x8_m118/v_p_bp5a.mat work/strictW/4x5x8_m118/v_p_bp5a.graph 59 150` | f8cc24fde61aa26d | `best 146 iters 3165 K 118 N 40 D 107` |
| W | `nice -n 19 src/bpopt6 work/strictW/4x5x8_m118/w_t_bp6s.mat work/strictW/4x5x8_m118/w_t_bp6s.graph 56 150 30 0.8 1 1` | 739d1536dfae8938 | `best 136 iters 5547 K 118 N 32 D 109` |

Log lines give the search's own count before pruning unused nodes; for W it is the cost of the W^T program,
cost(W) = cost(W^T) + r - n*p after transposition (tools/graphs.py transpose).

## 3. Assembly into scheme.json
```
python3 tools/combine.py 4x5x8 118
python tools/package.py work/final/4x5x8_m118/strict.json work/final/4x5x8_m118/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor whose every intermediate
value is a ternary combination (strict), falling back to Perminov's own program when ours is not strictly better.

