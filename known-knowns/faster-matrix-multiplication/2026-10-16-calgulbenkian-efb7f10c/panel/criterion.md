# Criterion skeptic report: add-5x6x8-cr667

I wrote my own checker (criterion_ws/chk.py) before reading the author's. It was run on the claim object and on null models (criterion_ws/nulls.py). Fetched sources were kept in criterion_ws (per.json, sota.json, tree.json, lille.html, cov.md), one GET each, with the honest User-Agent and no retries. I did not refetch reduced_known.json, README or CHANGELOG; the clause on them rests on the author's table-record, which I did not independently check.

## My checker, on the claim object (claim/object/5x6x8_m170_cr667_ZT_reduced.json)

Checks: every coefficient is +1 or -1; every reference is to an input or an earlier fresh variable (index below inputs plus position, asserted); every fresh variable and final form is expanded to exact integers over the inputs; every expanded coefficient is in {-1,0,1}; the 170 product factors and 40 outputs are tested against the full Brent identity for 5x6 times 6x8 (all 30*48*40 index triples, output k*5+i read as C[i][k]); 20 random integer matrix pairs are evaluated.

Real output:
`adds U,V,W 159 196 312 total 667 | nonternary 0 0 0 | brent bad 0 | ok True []`

Per-map additions: U 159, V 196, W 312, total 667 (sum over all fresh and final forms of terms minus 1; negation free). Straight-line order held and no coefficient outside +/-1 occurred. No expanded intermediate had a coefficient outside {-1,0,1} in any of the three maps.

## Calibration on Perminov's file

File: 5x6x8_m170_cr720_fv345_cn2312_ZT_reduced.json (HTTP 200).
My counter output: `adds U,V,W 177 218 325 total 720 | nonternary 0 0 0 | brent bad 0 | ok True`. The counter gives 720 and Perminov's scheme passes the same identity.
The expanded U, V and W rows (the 170 products) are identical between his file and the claim: U identical True, V identical True, W identical True. Only the programs differ. No map's program is identical to his: u_fresh 74 vs 159 forms, v_fresh 92 vs 196, w_fresh 179 vs 109; final lists also differ. The claim's file records complexity reduced 667 and naive 2312; his records reduced 720 and naive 2312.

## Clauses

1. "explicit straight-line program ... for a format with max(n,m,p) <= 8": MET. Format 5x6x8, max 8, n = [5,6,8], z2 false.
2. "rank r equal to the best rank listed in fmm_sota.json (re-fetched live)": MET. Live fmm_sota.json has the single entry for this format: format [5,6,8], rank 170. The object has m = 170.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": MET. Exact Brent identity with 0 violations, plus 20 random integer evaluations, over Z with ternary expanded forms.
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository, counted under the reduced convention": MET. The live git tree (not truncated, 6637 entries, HTTP 200) has exactly one file for 5x6x8 in addition_reduced_ZT, with cr 720, so the minimum cr over files for this format and rank is 720. 667 < 720. Under my counter his file is 720, so the conventions agree. The tree also lists two 5x6x8 entries in naive_addition_reduced_ZT (c2312, .json and .m). Those are naive counts, nz(U)+nz(V)+nz(W) minus the trivial subtraction under another convention. They count every non-shared linear form expanded, with no common-subexpression sharing, so they are about 2312 and do not compare with the reduced count; the claim's own naive figure is also 2312. Not a lower reduced count. The reduced_known.json, README and CHANGELOG clause rests on the author's record (5x6x8-170: None; no lower count stated), unverified by me.
5. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant": MET vacuously. The live page https://fmm.univ-lille.fr/5x6x8.html (HTTP 200) lists the algorithm type polynomial for rank 170 (taken from Kauers and Wood, arXiv 2510.19787) and download encodings only. It has no Commentaries section, and the words complexity, addition, operation and best-known do not occur. No count is cited, so no lower count exists.
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": MET. The row for 5,6,8 reads "+2410" in the adds column. The legend defines adds as nz(U)+nz(V)+nz(W) - 2r - n*p, a naive count. For the claim's own expanded rows I get nz = 2692, giving 2312 under that formula (the table's 2410 is for a different scheme or convention). The column is naive, not comparable to reduced counts, and in any case far above 667. No cell is lower than 667.
7. "If the Lille rank is attained only with non-ternary coefficients ...": not triggered. The object is ternary and no count is cited.
8. "The reference count is the MINIMUM cr over all files for that format and rank": one file, 720.
9. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": the rank equals the live best (170); no rank is lowered. Not triggered. The scheme is Perminov's own product set (identical U, V, W rows).

Hidden quantifier note: the win is on the straight-line program only, over his exact products, in the single-file reduced class. It is a genuine reduction of the program from 720 to 667 (7.4 percent), and no other source compared supplies a reduced count.

## Null models (my checker rejects each)

- Flip the sign of one term of one U factor: ok False (Brent violations).
- Drop one term of one output (W form 3, count becomes 311): ok False.
- Shift one index in one V factor: ok False.
- Swap two outputs (C-layout error): ok False.
- Forward reference (a fresh form points to a later variable): rejected by the order assertion.
- Coefficient 2 in a term: rejected by the coefficient assertion.
- A duplicate term inside a fresh form (expanded coefficient 2, count 160): ok False, with a non-ternary expanded form.

## Verdicts

Full criterion: met on every clause I can check from the named sources (reduced_known.json, README and CHANGELOG on the author's record only).
p1 (as the brief defines it: strictly fewer than Perminov's live 5x6x8 count, same convention): met, 667 < 720. The bank's own enumerated p1 (rank-23 for 3x3x3) is not what this claim addresses, and p3 (three formats) is not met; the claim stands on the full criterion, so the partial win is subsumed.

confirmed_scope: The file claim/object/5x6x8_m170_cr667_ZT_reduced.json (sha256 efb7f10c7e3a5dcd2481aacbd72ae5e308550dd825927d1c1114574354447c80) is a ternary straight-line program that exactly computes the full 5x6 times 6x8 product over Z at rank 170 (Brent identity verified, every expanded coefficient in {-1,0,1}) using 667 reduced additions (U 159, V 196, W 312), strictly below the 720 of the only addition_reduced_ZT file for 5x6x8 rank 170, on the same products as that file, and no source checked (the live Lille page, COVERAGE.md) gives a comparable lower count.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
