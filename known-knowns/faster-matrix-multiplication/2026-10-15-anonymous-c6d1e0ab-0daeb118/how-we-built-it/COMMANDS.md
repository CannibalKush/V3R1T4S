# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: built with `cc -O2 -o src/{name} src/{name}.c` (see src/README.md).
The searches are time-capped random searches: re-running a command gives a valid program but not necessarily the same
one (the iteration count depends on machine load). The graph files listed are the actual outputs used; scheme.json is
checkable on its own with check_slp.py and sym_check.py.

## 0. Base scheme (Kronecker product of two Perminov files)
```
python3 tools/kron_scheme.py data/schemes/2x2x2_m7_cr15_cn24_ZT_reduced.json data/schemes/2x3x3_m15_cr43_cn79_ZT_reduced.json work/kron/K466b.json
```
sha256 of work/kron/K466b.json: afe89262f8d7981c

## 1. Map matrices
Written by tools/opt_scheme.py (graphs.maps_of + write_mat): U (r x nm) and V (r x mp) as is, W transposed
(W^T: r x np) for the w_t jobs. Driver command that produced the run directory:
```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py work/kron/K466b.json 100 10 work/kbp_K466b/4x6x6_m105
```
opt_scheme.py starts one process per job; job k gets seed = 10*7 + k, cap 100 s:

## 2. Per-map searches actually used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/kbp_K466b/4x6x6_m105/u_p_bp5b.mat work/kbp_K466b/4x6x6_m105/u_p_bp5b.graph 71 100` | a8b74d1e193c8baa | `best 95 iters 17300 K 105 N 24 D 93` |
| V | `nice -n 19 src/bpopt5 work/kbp_K466b/4x6x6_m105/v_p_bp5a.mat work/kbp_K466b/4x6x6_m105/v_p_bp5a.graph 72 100` | bac0b42e8da376fa | `best 106 iters 4758 K 105 N 36 D 99` |
| W | `nice -n 19 src/bpopt6 work/kbp_K466b/4x6x6_m105/w_t_bp6s.mat work/kbp_K466b/4x6x6_m105/w_t_bp6s.graph 74 100 30 0.8 1 1` | ae98064c43969f0e | `best 91 iters 23600 K 105 N 24 D 90` |

For W the log line is the cost of the W^T program; cost(W) = cost(W^T) + r - n*p after transposition.
For W the graph is a program for W^T; it is transposed back (tools/graphs.py transpose) before assembly.

## 3. Assembly into scheme.json
```
BASE=work/kron/K466b.json RUNGLOB='work/kbp_K466b/%s_m%d' FINALDIR=work/finalK/ python3 tools/combine.py 4x6x6 105
python tools/package.py work/finalK/4x6x6_m105/strict.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor with every
intermediate value ternary (strict), here the three graphs above; package.py writes scheme.json and runs both checkers.

