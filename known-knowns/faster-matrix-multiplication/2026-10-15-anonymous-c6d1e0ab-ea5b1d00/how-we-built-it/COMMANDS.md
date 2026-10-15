# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: built with `cc -O2 -o src/{name} src/{name}.c` (see src/README.md).
The searches are time-capped random searches: re-running a command gives a valid program but not necessarily the same
one (the iteration count depends on machine load). The graph files listed are the actual outputs used; scheme.json is
checkable on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json` (sha256 8f899e560b2d2976...).

## 1. Map matrices
Written by tools/opt_scheme.py (graphs.maps_of + write_mat): U (r x nm) and V (r x mp) as is, W transposed
(W^T: r x np) for the w_t jobs. Driver command that produced the run directory:
```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py data/schemes/5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json 150 5 work/top150/5x6x6_m130
```
opt_scheme.py starts one process per job; job k gets seed = 5*7 + k, cap 150 s:

## 2. Per-map searches actually used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/top150/5x6x6_m130/u_p_bp5b.mat work/top150/5x6x6_m130/u_p_bp5b.graph 36 150` | 9583a8884dded1c5 | `best 129 iters 9561 K 130 N 30 D 115` |
| V | `nice -n 19 src/bpopt5 work/top150/5x6x6_m130/v_p_bp5a.mat work/top150/5x6x6_m130/v_p_bp5a.graph 37 150` | dad7d427e00c7882 | `best 147 iters 3138 K 130 N 36 D 117` |
| W | `nice -n 19 src/bpopt6 work/top150/5x6x6_m130/w_t_bp6t.mat work/top150/5x6x6_m130/w_t_bp6t.graph 40 150 30 0.8 1 1` | 0be7c1f1f05da835 | `best 126 iters 5444 K 130 N 30 D 112` |

For W the log line is the cost of the W^T program; cost(W) = cost(W^T) + r - n*p after transposition.
For W the graph is a program for W^T; it is transposed back (tools/graphs.py transpose) before assembly.

## 3. Assembly into scheme.json
```
python3 tools/combine.py 5x6x6 130
python tools/package.py work/final/5x6x6_m130/strict.json work/final/5x6x6_m130/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor with every
intermediate value ternary (strict), here the three graphs above; package.py writes scheme.json and runs both checkers.

