# Criterion skeptic report: add-6x6x6-cr588

Own checker: criterion_ws/chk.py (pure Python, exact integers), written before reading the author's checker (which I did not run).
Claim file hashes verified against claim.SHA256SUMS (all 8 OK).

## Evidence
1. Parse: every form references only inputs or earlier fresh variables (forward reference raises); every coefficient is +1 or -1. Sizes: u_fresh 159, v_fresh 157, w_fresh 98; 153 u/v factors; 36 w outputs.
2. Expansion: every fresh variable and every final form expanded to an integer vector over the inputs; all expanded coefficients lie in {-1,0,1} (asserted for every intermediate, none failed).
3. Tensor identity: sum over r of U[r,a] V[r,b] W[o,r] equals exactly 1 at (a=i*6+j, b=j*6+k, o=k*6+i) and 0 elsewhere (C-transposed output layout), exact. Also 20 random integer 6x6 matrix pairs: output k*6+i equals C[i][k] every time.
4. Count (reduced convention, sum of terms-1 over all fresh and final forms): U 159, V 157, W 272, total 588; matches the declared complexity.reduced 588.
5. Calibration: the same counter on Perminov's 6x6x6_m153_cr655_fv329_cn2182_ZT_reduced.json (fetched once) gives U 180, V 179, W 296, total 655, passing all the same checks. His 153 products (expanded U and V rows, in order) are identical to the claim's, as are the expanded W rows; the claim is the same scheme with a better addition program (same naive count 2182).
6. Null models, all rejected by my checker: flipped sign in a fresh term (non-ternary expansion); dropped term from a final V form (72 differing tensor cells); swapped two output rows (24 cells); forward reference; coefficient 2; x+x doubling; shifted input index (86 cells).

## Clauses
- "explicit SLP for a format with max dim <= 8": met, 6x6x6.
- "rank equal to best rank in fmm_sota.json (live)": met. Live fetch lists [6,6,6] rank 153; the claim has 153.
- "(1) verified symbolically to compute A*B exactly over Z": met (exact tensor identity plus random evaluation above).
- "(2) strictly less than the minimum reduced count for that format and rank in Perminov's live addition_reduced_ZT": met. The live tree (not truncated) holds exactly one addition_reduced_ZT file for 6x6x6, cr655, so the minimum is 655; 588 < 655. Files in naive_addition_reduced_ZT named c2171 (no "cr") are naive counts nz(U)+nz(V)+nz(W)-2r-np, a different convention that does not compare with SLP counts. reduced_known.json (in schemes/) has no 6x6x6 entry; README lists 6x6x6 only in a rank table; CHANGELOG has no 6x6x6 mention.
- "below any lower count on the live Lille per-format page": met vacuously. fmm.univ-lille.fr/6x6x6.html gives rank 153 (Moosbauer and Poole), a polynomial type, and encodings; it cites no complexity variant or operation count.
- "below COVERAGE.md adds column": met. The 6x6x6 row shows +2171 (Dronperminov c2171_ZT), the naive count; 588 is lower, though under a different convention, and the column is the only count published there.
- "same coefficient class": ternary SLP, Z; no non-ternary rank issue (rank 153 attained over Z).
- "each scheme claimed once; not a rank target": met; rank stays 153.

Limit: not a new scheme or rank; products are Perminov's. The win is the addition program only, under the reduced convention. Literature novelty not judged here.

## Verdicts
Full criterion: met. p1 as defined in this brief (strictly fewer than Perminov's live 6x6x6 count, same convention): met, 588 < 655. (The bank's own p1 names <3,3,3> rank 23, which this claim does not address.)

confirmed_scope: claim/object/6x6x6_m153_cr588_ZT_reduced.json (sha256 4abbbac3ec7576e4a03ff6ab7110dd4c99e8c564724a8c2eba3b26c4e2231a47) is an exact ternary straight-line program for the rank-153 6x6x6 scheme with Perminov's own 153 products, using 588 additions under the reduced convention versus 655 in his only live 6x6x6 addition_reduced_ZT file, as checked on 2026-10-15.
context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
