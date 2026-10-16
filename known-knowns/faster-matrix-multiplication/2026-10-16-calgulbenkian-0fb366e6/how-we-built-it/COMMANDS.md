# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: `cc -O2 -o src/{name} src/{source}` (table in src/README.md;
bpopt is built from src/bpopt_v1.c). The searches are time-capped random searches: re-running a command gives a valid
program but not necessarily the same one. The graph files listed are the actual outputs used; scheme.json is checkable
on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/5x8x8_m230_cr974_fv447_cn2747_ZT_reduced.json` (sha256 733a0bd327e5015d...). Every product of scheme.json is a product of this file.

## 1. Driver runs that produced the map programs
tools/opt_scheme.py writes the map matrices (U: r x nm, V: r x mp, W^T: r x np for w_t jobs) and starts
one search process per job; job k gets seed = (sweep seed)*7 + k.

```
JOBSET=w:t:bp6s,w:t:bp6t,u:p:bp5a,v:p:bp5a,v:p:bp5b,u:p:bp5b python tools/opt_scheme.py data/schemes/5x8x8_m230_cr974_fv447_cn2747_ZT_reduced.json 150 8 work/strictW/5x8x8_m230
```

## 2. Per-map programs used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/strictW/5x8x8_m230/u_p_bp5b.mat work/strictW/5x8x8_m230/u_p_bp5b.graph 61 150` | 09c487fa11f6e385 | `best 205 iters 2076 K 230 N 40 D 191` |
| V | `nice -n 19 src/bpopt5 work/strictW/5x8x8_m230/v_p_bp5a.mat work/strictW/5x8x8_m230/v_p_bp5a.graph 59 150` | c069b7fcf042de6a | `best 327 iters 91 K 230 N 64 D 205` |
| W | `nice -n 19 src/bpopt6 work/strictW/5x8x8_m230/w_t_bp6s.mat work/strictW/5x8x8_m230/w_t_bp6s.graph 56 150 30 0.8 1 1` | a8f645d4f8e3ee28 | `best 207 iters 1894 K 230 N 40 D 187` |

Log lines give the search's own count before pruning unused nodes; for W it is the cost of the W^T program,
cost(W) = cost(W^T) + r - n*p after transposition (tools/graphs.py transpose).

## 3. Assembly into scheme.json
```
python3 tools/combine.py 5x8x8 230
python tools/package.py work/final/5x8x8_m230/strict.json work/final/5x8x8_m230/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor whose every intermediate
value is a ternary combination (strict), falling back to Perminov's own program when ours is not strictly better.

