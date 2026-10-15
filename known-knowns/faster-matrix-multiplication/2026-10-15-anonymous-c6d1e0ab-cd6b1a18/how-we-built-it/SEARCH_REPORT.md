# Candidate: <5,5,8> rank 144 with 556 reduced additions (Perminov's minimum: 620)

Status: PROMISING (builder opus-add, team addcomp). Not confirmed; the orchestrator's panel decides.

## What it is
`scheme.json` is a straight-line program in Perminov's reduced-scheme layout (`n`, `m`, `u_fresh`, `u`, `v_fresh`, `v`,
`w_fresh`, `w`; fresh variable k of a map gets index (#inputs of that map + k); every form is a list of index/value terms
with values +-1, so his own counter can recount it). It uses exactly the 144 products of Perminov's ternary scheme
`schemes/results/addition_reduced_ZT/5x5x8_m144_cr620_fv281_cn1924_ZT_reduced.json` (fetched 2026-10-15 ~09:20Z): the expanded U, V, W matrices are
unchanged; only the programs that compute the three linear maps are new. All intermediate values are ternary
combinations of the inputs (no other scalars anywhere).

| map | Perminov | ours | how ours was found |
|---|---|---|---|
| U | 151 | 133 | cancellation search (src/bpopt*.c) on the map (`work/top150/5x5x8_m144/u_p_bp5b.graph`) |
| V | 182 | 161 | cancellation search (src/bpopt*.c) on the map (`work/top150/5x5x8_m144/v_p_bp5b.graph`) |
| W | 287 | 262 | cancellation search (src/bpopt*.c) on W^T, transposed back (transposition principle) (`work/top150/5x5x8_m144/w_t_bp6s.graph`) |
| total | 620 | 556 | margin 64 |

Program statistics (tools/stats.py): `{"u": {"fresh": 133, "cancelling_steps": 35, "max_abs_coeff": 1}, "v": {"fresh": 161, "cancelling_steps": 30, "max_abs_coeff": 1}, "w": {"fresh": 98, "cancelling_steps": 33, "max_abs_coeff": 1}}` (cancelling_steps = forms whose terms overlap and partly cancel;
max_abs_coeff = largest coefficient of any intermediate value over the map's inputs; 1 means every intermediate is a
ternary combination). Perminov's own programs have no cancelling steps.


## How it was checked (real output in check_output.txt)
- `check_slp.py` (mine, standard library): coefficients all +-1, straight-line order, exact expansion of every map over Z
  and the full tensor identity sum_q U_q (x) V_q (x) W_q = <5,5,8> (output C[i][k] at index k*n+i,
  Perminov's layout), plus evaluation of the program on 50 random integer matrix pairs; count = sum over all forms of
  (length - 1), Perminov's 'reduced' convention.
- `sym_check.py` (mine, sympy): runs the program on symbolic matrices, expands each output and compares it with A*B.
- Counter calibration: the same counter reproduces the `cr` of all 49 addition_reduced_ZT files at the Lille best rank
  with max side <= 8 (NOTES.md).

```
$ python check_slp.py scheme.json
{"file": "scheme.json", "format": "5x5x8", "rank": 144, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 133, "adds_V": 161, "adds_W": 262, "adds_total": 556, "naive_total": 1924, "declared_reduced": 556, "VALID": true}

$ python sym_check.py scheme.json
{"file": "scheme.json", "format": "5x5x8", "rank": 144, "products": 144, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 556}
```

## What it would beat
- Perminov's live repository (tree fetched 2026-10-15 09:19Z), addition_reduced_ZT files for 5x5x8 rank 144: 5x5x8_m144_cr620_fv281_cn1924_ZT_reduced.json (cr 620).
  Minimum cr = 620. reduced_known.json, README and CHANGELOG (fetched 09:20Z) list nothing lower for this format and rank.
- Rank 144 is the best rank for 5x5x8 in fmm_sota.json (fetched 09:19Z).
- The orchestrator's literature scout (data/literature_bars.md, 2026-10-15) found no published comparable count below
  Perminov's repository for this format and rank (sources: Perminov arXiv:2512.13365 Tables 1-6, Martensson-Wagner ACDA25,
  matmulcatalog COVERAGE.md naive counts, Lille page without commentary). Open gap named there: IACR ePrint 2026/849
  could not be read.
- NOT checked by me (my brief allows no other fetches): the Lille per-format page's complexity variant and matmulcatalog's
  COVERAGE.md 'adds' column. The orchestrator must re-fetch those and Perminov's tree before any claim.

## How it was found
tools/opt_scheme.py splits the scheme into its three maps and runs, per map, (a) a Boyar-Peralta-style distance-guided
search with cancellation over ternary vectors (src/bpopt.c) on the tall maps U, V and W^T (the W program is then obtained
by the transposition principle, cost(W) = cost(W^T) + r - n*p), and (b) randomized iterated pair-greedy CSE on the
transposed maps (src/slpopt.c), keeping Perminov's own program for any map where ours is not strictly better.

## Credits
Splitting into three maps and optimising the transposed map (transposition principle) is from another contributor's
PR #149 on the V3R1T4S repo (DrZuzzjen, <4,6,7> 503 vs 517). The cancellation heuristic follows Boyar and Peralta's
shortest-linear-program heuristic. The base scheme is Perminov's (github.com/dronperminov/FastMatrixMultiplication).
All code here is opus-add's own.
