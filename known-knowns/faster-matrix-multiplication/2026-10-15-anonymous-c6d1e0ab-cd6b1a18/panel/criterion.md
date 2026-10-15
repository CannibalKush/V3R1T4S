# Criterion skeptic report: add-5x5x8-cr556

Hash list: every file in claim/ matches claim.SHA256SUMS (sha256sum -c, all OK).

## My own checker (criterion_ws/chk.py, written before reading the author's)

Run on claim/object/5x5x8_m144_cr556_ZT_reduced.json:

    dims (5,5,8), rank 144, adds per map (U,V,W) = (133, 161, 262), total 556,
    declared complexity {naive 1924, reduced 556}
    straight-line order + every coefficient in {+1,-1}: True
    every expanded fresh variable and every expanded final form has coefficients in {-1,0,1}: True
    full Brent tensor identity for <5,5,8> (A index i*5+j, B index j*8+l, output index l*5+i, i.e. C transposed), exact integers, 144 factors, 40 outputs: True
    20 random integer matrix products (entries -50..49) equal A*B exactly: True

Count rule: sum over all fresh and final forms of (terms - 1); negation free. Total 133+161+262 = 556.

## Calibration

Fetched once (HTTP 200) Perminov's 5x5x8_m144_cr620_fv281_cn1924_ZT_reduced.json (sha256 f8da82de3400cfbf57d0061a47567ef05c1c241cb6a0dea9c250b5083e910a33, same as the author recorded). My counter gives 151+182+287 = 620, matching its declared cr620; it also passes my ternary, straight-line, tensor and random checks. Its expanded U, V, W rows equal the claim's rows exactly, in the same order (identical multiset and identical sequence; nonzeros 660/809/783 both). So the claim is Perminov's own rank-144 scheme with a new, shorter straight-line program. The criterion compares counts at the best rank, not schemes, so this is allowed.

## Clauses

1. "explicit straight-line program ... for a format with max(n,m,p) <= 8": MET. Format 5x5x8, max 8.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": MET. Fetched once (HTTP 200); the entry for format [5,5,8] is rank 144 (exponent 2.813995); the claim has 144 products.
3. "(1) verified symbolically to compute the full product A*B exactly over Z": MET. Exact integer tensor identity plus random evaluation (above). Ternary condition also holds on every expanded intermediate.
4. "(2) STRICTLY LESS than the smallest reduced addition count for that format and rank in Perminov's live repository": MET. Fetched the git tree once (HTTP 200, not truncated). addition_reduced_ZT contains exactly one 5x5x8 file, 5x5x8_m144_cr620_fv281_cn1924_ZT_reduced.json, so the minimum cr is 620; 556 < 620 (64 fewer). Files under naive_addition_reduced_ZT (5x5x8_m144_c1872, c1908) and the c-prefixed names without "cr" count a naive nonzero-based total (additions without shared subexpressions, a different convention; their values are above 1900, far from any reduced count), so they do not compare with the reduced convention and do not lower the reference. I did not fetch reduced_known.json, the README or the CHANGELOG (outside my named sources); the author's table-record shows no 5x5x8-144 entry in them. That part is unverified by me.
5. "AND below any lower count published on the live Lille per-format page's cited complexity variant": MET vacuously. Fetched https://fmm.univ-lille.fr/5x5x8.html once (HTTP 200): rank 144, algorithm from Kauers and Wood (arXiv 2510.19787), a polynomial "algorithm type" line, links to Maple encodings; no commentaries section, no complexity variant and no operation count cited for this rank.
6. "and in matmulcatalog's live COVERAGE.md 'adds' column": MET. Fetched once (HTTP 200). Row for <5,5,8> shows 144 and "+1908" adds. The column is a naive count nz(U)+nz(V)+nz(W) - 2r - n*p (stated in the file); here 660+809+783 - 288 - 40 = 1924 for Perminov's/claim rows, and 1908 is the catalogue's own scheme count. Not the same convention, and both are far above 556, so nothing lower exists there.
7. "If the Lille rank is attained only with non-ternary coefficients, compare in the same coefficient class": not triggered; the rank 144 scheme is ternary (Perminov's ZT file).
8. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": MET. Rank is unchanged at 144.
9. Hidden quantifiers: the reference is the minimum over all files for this format and rank (one file); the comparison is on the exact same format, rank and convention. No stretched definition found. Caveat: a program with fewer additions than a published one at the same products is a CSE improvement; the criterion asks only for that.

## Null models (my checker must reject each)

- flipped sign of one term in u[5]: tensor False, random False (rejected)
- dropped a term in w[7]: total 555 but tensor False, random False (rejected)
- swapped indices between v[10] and v[11]: tensor False, random False (rejected)
- shifted an index in v[10]: tensor False, random False (rejected)
- coefficient 2 in a fresh variable: ternary/straight False (rejected)
- forward reference in u_fresh: ternary/straight False (rejected)
- fresh variable = fresh0 + fresh0 (non-ternary expansion): ternary/straight False (rejected)

## Verdicts

Full criterion: met for 5x5x8 at rank 144 (556 reduced additions, strictly below Perminov's live minimum of 620, same convention; calibration reproduces 620).

Partial win p1 as enumerated is about rank-23 <3,3,3> with fewer than 58 additions. The claim is a different format, so the enumerated p1 is not what it meets. (The kit's loose reading of p1, strictly fewer than Perminov's live count for the claimed format under the same convention, is true: 556 < 620.)

p1: true

confirmed_scope: claim/object/5x5x8_m144_cr556_ZT_reduced.json (sha256 cd6b1a181d857f3e993cc6c15338a7f709bd1119c2745a399cfc02eae9b52f03) is a ternary straight-line program for the Perminov rank-144 scheme of the 5x5x8 format that computes A*B exactly over Z with 556 additions under the reduced convention, versus 620 for the only 5x5x8 file in Perminov's live addition_reduced_ZT, with no operation count for this rank on the Lille page and only a different naive count in COVERAGE.md; it shows no rank improvement and no evidence for any other format.

context: Claude Code subagent (Fable 5.1), fresh context
pass: true
