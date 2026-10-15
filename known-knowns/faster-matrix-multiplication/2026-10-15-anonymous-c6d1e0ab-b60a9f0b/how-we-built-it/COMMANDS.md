# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: built with `cc -O2 -o src/{name} src/{name}.c` (see src/README.md).
The searches are time-capped random searches: re-running a command gives a valid program but not necessarily the same
one (the iteration count depends on machine load). The graph files listed are the actual outputs used; scheme.json is
checkable on its own with check_slp.py and sym_check.py.

## 0. Base scheme (Kronecker product of two Perminov files)
```
python3 tools/kron_scheme.py data/schemes/2x2x2_m7_cr15_cn24_ZT_reduced.json data/schemes/3x3x4_m29_cr88_cn142_ZT_reduced.json work/kron/K668.json
```
sha256 of work/kron/K668.json: 0c21981e2df59b4c

## 1. Map matrices
Written by tools/opt_scheme.py (graphs.maps_of + write_mat): U (r x nm) and V (r x mp) as is, W transposed
(W^T: r x np) for the w_t jobs. Driver command that produced the run directory:
```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py work/kron/K668.json 120 7 work/kbp/6x6x8_m203
```
opt_scheme.py starts one process per job; job k gets seed = 7*7 + k, cap 120 s:

## 2. Per-map searches actually used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/kbp/6x6x8_m203/u_p_bp5b.mat work/kbp/6x6x8_m203/u_p_bp5b.graph 50 120` | 2d1196cf508eae3a | `best 174 iters 2974 K 203 N 36 D 168` |
| V | `nice -n 19 src/bpopt5 work/kbp/6x6x8_m203/v_p_bp5a.mat work/kbp/6x6x8_m203/v_p_bp5a.graph 51 120` | 5a3724e28a7bf9a0 | `best 195 iters 1660 K 203 N 48 D 165` |
| W | `nice -n 19 src/bpopt6 work/kbp/6x6x8_m203/w_t_bp6s.mat work/kbp/6x6x8_m203/w_t_bp6s.graph 53 120 30 0.8 1 1` | 0f3c696bc9b833e0 | `best 195 iters 1679 K 203 N 48 D 165` |

For W the log line is the cost of the W^T program; cost(W) = cost(W^T) + r - n*p after transposition.
For W the graph is a program for W^T; it is transposed back (tools/graphs.py transpose) before assembly.

## 3. Assembly into scheme.json
```
BASE=work/kron/K668.json RUNGLOB='work/kbp/%s_m%d' FINALDIR=work/finalK/ python3 tools/combine.py 6x6x8 203
python tools/package.py work/finalK/6x6x8_m203/strict.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor with every
intermediate value ternary (strict), here the three graphs above; package.py writes scheme.json and runs both checkers.

