# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: built with `cc -O2 -o src/{name} src/{name}.c` (see src/README.md).
The searches are time-capped random searches: re-running a command gives a valid program but not necessarily the same
one (the iteration count depends on machine load). The graph files listed are the actual outputs used; scheme.json is
checkable on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/6x6x6_m153_cr655_fv329_cn2182_ZT_reduced.json` (sha256 1fcee02b8d2d456f...).

## 1. Map matrices
Written by tools/opt_scheme.py (graphs.maps_of + write_mat): U (r x nm) and V (r x mp) as is, W transposed
(W^T: r x np) for the w_t jobs. Driver command that produced the run directory:
```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py data/schemes/6x6x6_m153_cr655_fv329_cn2182_ZT_reduced.json 150 5 work/top150/6x6x6_m153
```
opt_scheme.py starts one process per job; job k gets seed = 5*7 + k, cap 150 s:

## 2. Per-map searches actually used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/top150/6x6x6_m153/u_p_bp5b.mat work/top150/6x6x6_m153/u_p_bp5b.graph 36 150` | b7cd112193d62a0a | `best 159 iters 3739 K 153 N 36 D 138` |
| V | `nice -n 19 src/bpopt5 work/top150/6x6x6_m153/v_p_bp5b.mat work/top150/6x6x6_m153/v_p_bp5b.graph 38 150` | 026482b2ca2db366 | `best 157 iters 3449 K 153 N 36 D 137` |
| W | `nice -n 19 src/bpopt6 work/top150/6x6x6_m153/w_t_bp6s.mat work/top150/6x6x6_m153/w_t_bp6s.graph 39 150 30 0.8 1 1` | 4b9defc32031e710 | `best 155 iters 3698 K 153 N 36 D 137` |

For W the log line is the cost of the W^T program; cost(W) = cost(W^T) + r - n*p after transposition.
For W the graph is a program for W^T; it is transposed back (tools/graphs.py transpose) before assembly.

## 3. Assembly into scheme.json
```
python3 tools/combine.py 6x6x6 153
python tools/package.py work/final/6x6x6_m153/strict.json work/final/6x6x6_m153/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor with every
intermediate value ternary (strict), here the three graphs above; package.py writes scheme.json and runs both checkers.

