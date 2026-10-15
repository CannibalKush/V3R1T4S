# Candidate: <4,6,6> rank 105 with 373 reduced additions (Perminov's minimum: 430)

Status: PROMISING (builder opus-add, team addcomp). Not confirmed; the orchestrator's panel decides.

## What it is
`scheme.json` is a straight-line program in Perminov's reduced-scheme layout (`n`, `m`, `u_fresh`, `u`, `v_fresh`, `v`,
`w_fresh`, `w`; fresh variable k of a map gets index (#inputs of that map + k); every form is a list of index/value terms
with values +-1). Its 105 products are NOT those of Perminov's 4x6x6 file: they are the Kronecker (tensor) product of two
of Perminov's own ternary schemes, `2x2x2_m7_cr15_cn24_ZT_reduced.json` (sha256 b374fcc797ea0149...) and `2x3x3_m15_cr43_cn79_ZT_reduced.json`
(sha256 fbbb6d96ba97aa50...), both copied here as component_*.json and both from
schemes/results/addition_reduced_ZT/ (fetched 2026-10-15 ~09:20Z). `kron_scheme.py` rebuilds the naive product scheme:
A index (i1*n2+i2)*(m1*m2)+(j1*m2+j2), B likewise, output C^T index k*n+i with k = k1*p2+k2, i = i1*n2+i2, product
q = q1*r2+q2. The Lille page for 4x6x6 describes its rank-105 algorithm as exactly such a tensor product (the 2x2x2
factor there is Strassen's; Perminov's own 4x6x6 file also has Strassen-type factors (checked: 2x2x2 factor row weights 1,1,2,2,2,2,2), while his 2x2x2 cr15 file is a
Winograd-type variant, which is what makes this product cheaper). The rank is 105 = the Lille best rank (fmm_sota.json).
All coefficients are in {-1,0,1}; all intermediate values are ternary combinations of the inputs.

| map | naive (product scheme) | ours | how |
|---|---|---|---|
| U | 343 | 95 | cancellation search (src/bpopt5) on U |
| V | 483 | 106 | cancellation search (src/bpopt5) on V |
| W | 550 | 172 | cancellation search (src/bpopt6, strict) on W^T, transposed back |
| total | 1376 | 373 | Perminov min cr 430, margin 57 |

Note: the 2x3x3 component is Perminov's cr43_cn79 file (not the cr43_cn77 file listed first); with cr43_cn77 the
product gives 374, with cr44 374, with cr46 385. For comparison, the same search on Perminov's own 4x6x6 tensor reaches 410 (U 101, V 127, W 182) (see sweep.csv); a two-stage
Kronecker-structured program (tools/kron_prog.py) on this product scheme was worse than the direct search.

Program statistics (tools/stats.py): `{"u": {"fresh": 95, "cancelling_steps": 14, "max_abs_coeff": 1}, "v": {"fresh": 106, "cancelling_steps": 9, "max_abs_coeff": 1}, "w": {"fresh": 72, "cancelling_steps": 25, "max_abs_coeff": 1}}`.

## How it was checked (real output in check_output.txt)
- `check_slp.py` (mine): coefficients +-1, straight-line order, exact tensor identity over Z for <4,6,6>
  (C^T layout), evaluation on 50 random integer matrix pairs, reduced count = sum over forms of (length - 1).
- `sym_check.py` (mine, sympy): symbolic run of the program, every output equals the entry of A*B.

```
$ python check_slp.py scheme.json
{"file": "scheme.json", "format": "4x6x6", "rank": 105, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 95, "adds_V": 106, "adds_W": 172, "adds_total": 373, "naive_total": 1376, "declared_reduced": 373, "VALID": true}

$ python sym_check.py scheme.json
{"file": "scheme.json", "format": "4x6x6", "rank": 105, "products": 105, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 373}
```

## What it would beat
- Perminov's live repository (tree fetched 2026-10-15 09:19Z): addition_reduced_ZT files for 4x6x6 rank 105:
  4x6x6_m105_cr430_fv243_cn894_ZT_reduced.json (cr 430). Minimum cr = 430. Nothing lower in reduced_known.json,
  README or CHANGELOG.
- The orchestrator's literature scout (data/literature_bars.md) found no published comparable count below the repository
  for this format and rank; open gap named there: IACR ePrint 2026/849 (unread).
- NOT checked by me: the live Lille page complexity variant and matmulcatalog COVERAGE.md beyond the scout's copies.
- Eligibility note for the panel: this is a different rank-105 ternary scheme from Perminov's 4x6x6 file (a product of
  two of his files); the target text compares against the minimum cr "for that format and rank", which is 430.

## Credits
Base schemes: Perminov (github.com/dronperminov/FastMatrixMultiplication). Map splitting and transposition idea:
PR #149 (DrZuzzjen). Cancellation heuristic after Boyar and Peralta. Code: opus-add.
