# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: built with `cc -O2 -o src/{name} src/{name}.c` (see src/README.md).
The searches are time-capped random searches: re-running a command gives a valid program but not necessarily the same
one (the iteration count depends on machine load). The graph files listed are the actual outputs used; scheme.json is
checkable on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/5x5x8_m144_cr620_fv281_cn1924_ZT_reduced.json` (sha256 f8da82de3400cfbf...).

## 1. Map matrices
Written by tools/opt_scheme.py (graphs.maps_of + write_mat): U (r x nm) and V (r x mp) as is, W transposed
(W^T: r x np) for the w_t jobs. Driver command that produced the run directory:
```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py data/schemes/5x5x8_m144_cr620_fv281_cn1924_ZT_reduced.json 150 5 work/top150/5x5x8_m144
```
opt_scheme.py starts one process per job; job k gets seed = 5*7 + k, cap 150 s:

## 2. Per-map searches actually used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/top150/5x5x8_m144/u_p_bp5b.mat work/top150/5x5x8_m144/u_p_bp5b.graph 36 150` | b89fa3381593432e | `best 133 iters 8245 K 144 N 25 D 125` |
| V | `nice -n 19 src/bpopt5 work/top150/5x5x8_m144/v_p_bp5b.mat work/top150/5x5x8_m144/v_p_bp5b.graph 38 150` | df8cccb74f334d39 | `best 161 iters 1821 K 144 N 40 D 127` |
| W | `nice -n 19 src/bpopt6 work/top150/5x5x8_m144/w_t_bp6s.mat work/top150/5x5x8_m144/w_t_bp6s.graph 39 150 30 0.8 1 1` | 8550ac616d1ba8a2 | `best 158 iters 2874 K 144 N 40 D 128` |

For W the log line is the cost of the W^T program; cost(W) = cost(W^T) + r - n*p after transposition.
For W the graph is a program for W^T; it is transposed back (tools/graphs.py transpose) before assembly.

## 3. Assembly into scheme.json
```
python3 tools/combine.py 5x5x8 144
python tools/package.py work/final/5x5x8_m144/strict.json work/final/5x5x8_m144/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor with every
intermediate value ternary (strict), here the three graphs above; package.py writes scheme.json and runs both checkers.

