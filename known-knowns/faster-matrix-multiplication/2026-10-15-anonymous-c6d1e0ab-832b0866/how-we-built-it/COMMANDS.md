# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: built with `cc -O2 -o src/{name} src/{name}.c` (see src/README.md).
The searches are time-capped random searches: re-running a command gives a valid program but not necessarily the same
one (the iteration count depends on machine load). The graph files listed are the actual outputs used; scheme.json is
checkable on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/5x6x7_m150_cr664_fv310_cn2039_ZT_reduced.json` (sha256 ee197c7c8fa4d02a...).

## 1. Map matrices
Written by tools/opt_scheme.py (graphs.maps_of + write_mat): U (r x nm) and V (r x mp) as is, W transposed
(W^T: r x np) for the w_t jobs. Driver command that produced the run directory:
```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py data/schemes/5x6x7_m150_cr664_fv310_cn2039_ZT_reduced.json 150 5 work/top150/5x6x7_m150
```
opt_scheme.py starts one process per job; job k gets seed = 5*7 + k, cap 150 s:

## 2. Per-map searches actually used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/top150/5x6x7_m150/u_p_bp5b.mat work/top150/5x6x7_m150/u_p_bp5b.graph 36 150` | 01671542581209a1 | `best 147 iters 3191 K 150 N 30 D 129` |
| V | `nice -n 19 src/bpopt5 work/top150/5x6x7_m150/v_p_bp5a.mat work/top150/5x6x7_m150/v_p_bp5a.graph 37 150` | 73475d7055988fc0 | `best 171 iters 1646 K 150 N 42 D 136` |
| W | `nice -n 19 src/bpopt6 work/top150/5x6x7_m150/w_t_bp6s.mat work/top150/5x6x7_m150/w_t_bp6s.graph 39 150 30 0.8 1 1` | eca5c4f73235949c | `best 149 iters 2817 K 150 N 35 D 132` |

For W the log line is the cost of the W^T program; cost(W) = cost(W^T) + r - n*p after transposition.
For W the graph is a program for W^T; it is transposed back (tools/graphs.py transpose) before assembly.

## 3. Assembly into scheme.json
```
python3 tools/combine.py 5x6x7 150
python tools/package.py work/final/5x6x7_m150/strict.json work/final/5x6x7_m150/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor with every
intermediate value ternary (strict), here the three graphs above; package.py writes scheme.json and runs both checkers.

