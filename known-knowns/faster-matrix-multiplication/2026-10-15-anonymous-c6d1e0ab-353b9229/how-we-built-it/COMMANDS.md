# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: built with `cc -O2 -o src/{name} src/{name}.c` (see src/README.md).
The searches are time-capped random searches: re-running a command gives a valid program but not necessarily the same
one (the iteration count depends on machine load). The graph files listed are the actual outputs used; scheme.json is
checkable on its own with check_slp.py and sym_check.py.

## 0. Base scheme (Kronecker product of two Perminov files)
```
python3 tools/kron_scheme.py data/schemes/2x2x2_m7_cr15_cn24_ZT_reduced.json data/schemes/3x4x4_m38_cr125_cn224_ZT_reduced.json work/kron/K688.json
```
sha256 of work/kron/K688.json: 56015f3e99f25647

## 1. Map matrices
Written by tools/opt_scheme.py (graphs.maps_of + write_mat): U (r x nm) and V (r x mp) as is, W transposed
(W^T: r x np) for the w_t jobs. Driver command that produced the run directory:
```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py work/kron/K688.json 120 7 work/kbp/6x8x8_m266
```
opt_scheme.py starts one process per job; job k gets seed = 7*7 + k, cap 120 s:

## 2. Per-map searches actually used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/kbp/6x8x8_m266/u_p_bp5b.mat work/kbp/6x8x8_m266/u_p_bp5b.graph 50 120` | e974cd8d3466f3e2 | `best 255 iters 606 K 266 N 48 D 234` |
| V | `nice -n 19 src/bpopt5 work/kbp/6x8x8_m266/v_p_bp5a.mat work/kbp/6x8x8_m266/v_p_bp5a.graph 51 120` | a92e71587f874d6c | `best 274 iters 133 K 266 N 64 D 236` |
| W | `nice -n 19 src/bpopt6 work/kbp/6x8x8_m266/w_t_bp6s.mat work/kbp/6x8x8_m266/w_t_bp6s.graph 53 120 30 0.8 1 1` | 73bcfe1b4c68f4b8 | `best 246 iters 644 K 266 N 48 D 242` |

For W the log line is the cost of the W^T program; cost(W) = cost(W^T) + r - n*p after transposition.
For W the graph is a program for W^T; it is transposed back (tools/graphs.py transpose) before assembly.

## 3. Assembly into scheme.json
```
BASE=work/kron/K688.json RUNGLOB='work/kbp/%s_m%d' FINALDIR=work/finalK/ python3 tools/combine.py 6x8x8 266
python tools/package.py work/finalK/6x8x8_m266/strict.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor with every
intermediate value ternary (strict), here the three graphs above; package.py writes scheme.json and runs both checkers.

