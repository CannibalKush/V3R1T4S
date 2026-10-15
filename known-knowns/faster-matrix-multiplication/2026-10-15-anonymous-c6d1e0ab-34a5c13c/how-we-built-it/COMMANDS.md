# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: built with `cc -O2 -o src/{name} src/{name}.c` (see src/README.md).
The searches are time-capped random searches: re-running a command gives a valid program but not necessarily the same
one (the iteration count depends on machine load). The graph files listed are the actual outputs used; scheme.json is
checkable on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/6x6x7_m183_cr769_fv370_cn2502_ZT_reduced.json` (sha256 bc960780454fc916...).

## 1. Map matrices
Written by tools/opt_scheme.py (graphs.maps_of + write_mat): U (r x nm) and V (r x mp) as is, W transposed
(W^T: r x np) for the w_t jobs. Driver command that produced the run directory:
```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py data/schemes/6x6x7_m183_cr769_fv370_cn2502_ZT_reduced.json 300 4 work/top300/6x6x7_m183
```
opt_scheme.py starts one process per job; job k gets seed = 4*7 + k, cap 300 s:

## 2. Per-map searches actually used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/top300/6x6x7_m183/u_p_bp5a.mat work/top300/6x6x7_m183/u_p_bp5a.graph 28 300` | 584072dfb666bfeb | `best 184 iters 5286 K 183 N 36 D 160` |
| V | `nice -n 19 src/bpopt5 work/top300/6x6x7_m183/v_p_bp5a.mat work/top300/6x6x7_m183/v_p_bp5a.graph 30 300` | e388ba7cb0c380f0 | `best 182 iters 3220 K 183 N 42 D 156` |
| W | `nice -n 19 src/bpopt6 work/top300/6x6x7_m183/w_t_bp6s.mat work/top300/6x6x7_m183/w_t_bp6s.graph 32 300 30 0.8 1 1` | 90beff97fe673a39 | `best 188 iters 4185 K 183 N 42 D 159` |

For W the log line is the cost of the W^T program; cost(W) = cost(W^T) + r - n*p after transposition.
For W the graph is a program for W^T; it is transposed back (tools/graphs.py transpose) before assembly.

## 3. Assembly into scheme.json
```
python3 tools/combine.py 6x6x7 183
python tools/package.py work/final/6x6x7_m183/strict.json work/final/6x6x7_m183/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor with every
intermediate value ternary (strict), here the three graphs above; package.py writes scheme.json and runs both checkers.

