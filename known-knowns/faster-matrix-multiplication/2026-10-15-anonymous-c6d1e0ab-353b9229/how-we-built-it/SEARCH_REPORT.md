# Candidate: <6,8,8> rank 266 with 993 reduced additions (Perminov's minimum: 1161)

Status: PROMISING (builder opus-add, team addcomp). Not confirmed; the orchestrator's panel decides.

## What it is
`scheme.json` is a straight-line program in Perminov's reduced-scheme layout (`n`, `m`, `u_fresh`, `u`, `v_fresh`, `v`,
`w_fresh`, `w`; fresh variable k of a map gets index (#inputs of that map + k); every form is a list of index/value terms
with values +-1). Its 266 products are NOT those of Perminov's 6x8x8 file: they are the Kronecker (tensor) product of two
of Perminov's own ternary schemes, `2x2x2_m7_cr15_cn24_ZT_reduced.json` (sha256 b374fcc797ea0149...) and `3x4x4_m38_cr125_cn224_ZT_reduced.json`
(sha256 96529b323ade49d0...), both copied here as component_*.json and both from
schemes/results/addition_reduced_ZT/ (fetched 2026-10-15 ~09:20Z). `kron_scheme.py` rebuilds the naive product scheme:
A index (i1*n2+i2)*(m1*m2)+(j1*m2+j2), B likewise, output C^T index k*n+i with k = k1*p2+k2, i = i1*n2+i2, product
q = q1*r2+q2. The Lille page for 6x8x8 describes its rank-266 algorithm as exactly such a tensor product (the 2x2x2
factor there is Strassen's; Perminov's own 6x8x8 file also has Strassen-type factors, while his 2x2x2 cr15 file is a
Winograd-type variant, which is what makes this product cheaper). The rank is 266 = the Lille best rank (fmm_sota.json).
All coefficients are in {-1,0,1}; all intermediate values are ternary combinations of the inputs.

| map | naive (product scheme) | ours | how |
|---|---|---|---|
| U | 1078 | 255 | cancellation search (src/bpopt5) on U |
| V | 1470 | 274 | cancellation search (src/bpopt5) on V |
| W | 1240 | 464 | cancellation search (src/bpopt6, strict) on W^T, transposed back |
| total | 3788 | 993 | Perminov min cr 1161, margin 168 |

For comparison, the same search on Perminov's own 6x8x8 tensor reaches 1040 (U 249/250, V 319, W 471) (see sweep.csv); a two-stage
Kronecker-structured program (tools/kron_prog.py) on this product scheme was worse than the direct search.

Program statistics (tools/stats.py): `{"u": {"fresh": 255, "cancelling_steps": 61, "max_abs_coeff": 1}, "v": {"fresh": 274, "cancelling_steps": 53, "max_abs_coeff": 1}, "w": {"fresh": 160, "cancelling_steps": 29, "max_abs_coeff": 1}}`.

## How it was checked (real output in check_output.txt)
- `check_slp.py` (mine): coefficients +-1, straight-line order, exact tensor identity over Z for <6,8,8>
  (C^T layout), evaluation on 50 random integer matrix pairs, reduced count = sum over forms of (length - 1).
- `sym_check.py` (mine, sympy): symbolic run of the program, every output equals the entry of A*B.

```
$ python check_slp.py scheme.json
{"file": "scheme.json", "format": "6x8x8", "rank": 266, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 255, "adds_V": 274, "adds_W": 464, "adds_total": 993, "naive_total": 3788, "declared_reduced": 993, "VALID": true}

$ python sym_check.py scheme.json
{"file": "scheme.json", "format": "6x8x8", "rank": 266, "products": 266, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 993}
```

## What it would beat
- Perminov's live repository (tree fetched 2026-10-15 09:19Z): addition_reduced_ZT files for 6x8x8 rank 266:
  6x8x8_m266_cr1161_fv654_cn2780_ZT_reduced.json (cr 1161). Minimum cr = 1161. Nothing lower in reduced_known.json,
  README or CHANGELOG.
- The orchestrator's literature scout (data/literature_bars.md) found no published comparable count below the repository
  for this format and rank; open gap named there: IACR ePrint 2026/849 (unread).
- NOT checked by me: the live Lille page complexity variant and matmulcatalog COVERAGE.md beyond the scout's copies.
- Eligibility note for the panel: this is a different rank-266 ternary scheme from Perminov's 6x8x8 file (a product of
  two of his files); the target text compares against the minimum cr "for that format and rank", which is 1161.

## Credits
Base schemes: Perminov (github.com/dronperminov/FastMatrixMultiplication). Map splitting and transposition idea:
PR #149 (DrZuzzjen). Cancellation heuristic after Boyar and Peralta. Code: opus-add.
