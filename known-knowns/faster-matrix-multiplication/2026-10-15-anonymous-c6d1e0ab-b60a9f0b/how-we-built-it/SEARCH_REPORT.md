# Candidate: <6,6,8> rank 203 with 719 reduced additions (Perminov's minimum: 836)

Status: PROMISING (builder opus-add, team addcomp). Not confirmed; the orchestrator's panel decides.

## What it is
`scheme.json` is a straight-line program in Perminov's reduced-scheme layout (`n`, `m`, `u_fresh`, `u`, `v_fresh`, `v`,
`w_fresh`, `w`; fresh variable k of a map gets index (#inputs of that map + k); every form is a list of index/value terms
with values +-1). Its 203 products are NOT those of Perminov's 6x6x8 file: they are the Kronecker (tensor) product of two
of Perminov's own ternary schemes, `2x2x2_m7_cr15_cn24_ZT_reduced.json` (sha256 b374fcc797ea0149...) and `3x3x4_m29_cr88_cn142_ZT_reduced.json`
(sha256 e34d3afa84ac8726...), both copied here as component_*.json and both from
schemes/results/addition_reduced_ZT/ (fetched 2026-10-15 ~09:20Z). `kron_scheme.py` rebuilds the naive product scheme:
A index (i1*n2+i2)*(m1*m2)+(j1*m2+j2), B likewise, output C^T index k*n+i with k = k1*p2+k2, i = i1*n2+i2, product
q = q1*r2+q2. The Lille page for 6x6x8 describes its rank-203 algorithm as exactly such a tensor product (the 2x2x2
factor there is Strassen's; Perminov's own 6x6x8 file also has Strassen-type factors, while his 2x2x2 cr15 file is a
Winograd-type variant, which is what makes this product cheaper). The rank is 203 = the Lille best rank (fmm_sota.json).
All coefficients are in {-1,0,1}; all intermediate values are ternary combinations of the inputs.

| map | naive (product scheme) | ours | how |
|---|---|---|---|
| U | 749 | 174 | cancellation search (src/bpopt5) on U |
| V | 805 | 195 | cancellation search (src/bpopt5) on V |
| W | 960 | 350 | cancellation search (src/bpopt6, strict) on W^T, transposed back |
| total | 2514 | 719 | Perminov min cr 836, margin 117 |

For comparison, the same search on Perminov's own 6x6x8 tensor reaches 759 (U 183, V 208, W 368) (see sweep.csv); a two-stage
Kronecker-structured program (tools/kron_prog.py) on this product scheme was worse than the direct search.

Program statistics (tools/stats.py): `{"u": {"fresh": 174, "cancelling_steps": 24, "max_abs_coeff": 1}, "v": {"fresh": 195, "cancelling_steps": 46, "max_abs_coeff": 1}, "w": {"fresh": 144, "cancelling_steps": 66, "max_abs_coeff": 1}}`.

## How it was checked (real output in check_output.txt)
- `check_slp.py` (mine): coefficients +-1, straight-line order, exact tensor identity over Z for <6,6,8>
  (C^T layout), evaluation on 50 random integer matrix pairs, reduced count = sum over forms of (length - 1).
- `sym_check.py` (mine, sympy): symbolic run of the program, every output equals the entry of A*B.

```
$ python check_slp.py scheme.json
{"file": "scheme.json", "format": "6x6x8", "rank": 203, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 174, "adds_V": 195, "adds_W": 350, "adds_total": 719, "naive_total": 2514, "declared_reduced": 719, "VALID": true}

$ python sym_check.py scheme.json
{"file": "scheme.json", "format": "6x6x8", "rank": 203, "products": 203, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 719}
```

## What it would beat
- Perminov's live repository (tree fetched 2026-10-15 09:19Z): addition_reduced_ZT files for 6x6x8 rank 203:
  6x6x8_m203_cr836_fv454_cn1994_ZT_reduced.json (cr 836). Minimum cr = 836. Nothing lower in reduced_known.json,
  README or CHANGELOG.
- The orchestrator's literature scout (data/literature_bars.md) found no published comparable count below the repository
  for this format and rank; open gap named there: IACR ePrint 2026/849 (unread).
- NOT checked by me: the live Lille page complexity variant and matmulcatalog COVERAGE.md beyond the scout's copies.
- Eligibility note for the panel: this is a different rank-203 ternary scheme from Perminov's 6x6x8 file (a product of
  two of his files); the target text compares against the minimum cr "for that format and rank", which is 836.

## Credits
Base schemes: Perminov (github.com/dronperminov/FastMatrixMultiplication). Map splitting and transposition idea:
PR #149 (DrZuzzjen). Cancellation heuristic after Boyar and Peralta. Code: opus-add.
