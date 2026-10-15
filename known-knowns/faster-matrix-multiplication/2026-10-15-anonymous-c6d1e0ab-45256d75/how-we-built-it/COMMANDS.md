# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: built with `cc -O2 -o src/{name} src/{name}.c` (see src/README.md).
The searches are time-capped random searches: re-running a command gives a valid program but not necessarily the same
one (the iteration count depends on machine load). The graph files listed are the actual outputs used; scheme.json is
checkable on its own with check_slp.py and sym_check.py.

## 0. Base scheme (Kronecker product of two Perminov files)
```
python3 tools/kron_scheme.py data/schemes/2x2x2_m7_cr15_cn24_ZT_reduced.json data/schemes/2x3x4_m20_cr54_fv22_cn90_ZT_reduced.json work/kron/K468.json
```
sha256 of work/kron/K468.json: b0a3a1e456ec5797

## 1. Map matrices
Written by tools/opt_scheme.py (graphs.maps_of + write_mat): U (r x nm) and V (r x mp) as is, W transposed
(W^T: r x np) for the w_t jobs. Driver command that produced the run directory:
```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py work/kron/K468.json 120 7 work/kbp/4x6x8_m140
```
opt_scheme.py starts one process per job; job k gets seed = 7*7 + k, cap 120 s:

## 2. Per-map searches actually used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/kbp/4x6x8_m140/u_p_bp5b.mat work/kbp/4x6x8_m140/u_p_bp5b.graph 50 120` | bd7afd036e4a5f4f | `best 108 iters 46929 K 140 N 24 D 108` |
| V | `nice -n 19 src/bpopt5 work/kbp/4x6x8_m140/v_p_bp5a.mat work/kbp/4x6x8_m140/v_p_bp5a.graph 51 120` | 3085841a256be957 | `best 136 iters 3037 K 140 N 48 D 122` |
| W | `nice -n 19 src/bpopt6 work/kbp/4x6x8_m140/w_t_bp6s.mat work/kbp/4x6x8_m140/w_t_bp6s.graph 53 120 30 0.8 1 1` | 11a0b1392a591470 | `best 124 iters 6233 K 140 N 32 D 122` |

For W the log line is the cost of the W^T program; cost(W) = cost(W^T) + r - n*p after transposition.
For W the graph is a program for W^T; it is transposed back (tools/graphs.py transpose) before assembly.

## 3. Assembly into scheme.json
```
BASE=work/kron/K468.json RUNGLOB='work/kbp/%s_m%d' FINALDIR=work/finalK/ python3 tools/combine.py 4x6x8 140
python tools/package.py work/finalK/4x6x8_m140/strict.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor with every
intermediate value ternary (strict), here the three graphs above; package.py writes scheme.json and runs both checkers.

