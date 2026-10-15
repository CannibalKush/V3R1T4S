# CRITERION skeptic report: fmm-15x16x16-r2176

Object checked: claim/object/15x16x16_r2176_Q.json, sha256 0dee0512255d74595673fd8bfa0df20b0ab0a87785b2d11cbb2a94f6dbd5d57c (all seven entries of claim.SHA256SUMS verified OK with shasum -a 256 -c before reading anything).

Method note: I decoded the vocab_rle_v1 encoding from the CLAIM.md description, wrote my own checker before opening the author's code, and only then compared conventions. My checker (criterion_ws/scripts/brent_check.py) scales every row to integers, forms the integer tensor L times the sum over terms of u (x) v (x) w exactly with python-flint fmpz_mat (arbitrary-precision integers, no modular reduction, no sampling), one slice per A-entry, and compares it entry by entry against L times the 15x16x16 matrix multiplication tensor under two candidate C-index conventions. Angle-bracket format notation from the bank text is rewritten below as (n,m,p) or 15x16x16 to satisfy the repo checker; nothing else in the quotes is changed.

## My checker's real output (run under nice -n 19, 6.3 s)

```
sha256: 0dee0512255d74595673fd8bfa0df20b0ab0a87785b2d11cbb2a94f6dbd5d57c bytes: 735805
declared n,m,p = (15, 16, 16)  declared m (terms) = 2176  ring = Q  encoding = vocab_rle_v1
terms listed: 2176  terms with all three factors nonzero (rank): 2176  degenerate terms: 0
global scale L = 50400  max |integer coeff| u,v,w: 11948 18686 23886
nonzeros in U: 66132  in V: 73799  in W: 46470
convention C_rowmajor   : Brent equations checked = 14745600, violated = 7616  (first bad A-slice, count) = (0, 30)
convention C_transposed : Brent equations checked = 14745600, violated = 0
RESULT: EXACT over Q under convention(s) ['C_transposed']; rank (nonzero terms) = 2176
```

C_transposed means w[l*15 + i] is the coefficient of C[i][l]; this is exactly the convention the author's checker docstring states (Perminov's), read after my run. All 240 x 256 x 240 = 14,745,600 Brent equations hold exactly over Q. Rank counted as terms with all three factors nonzero: 2176 (no degenerate terms, so the listed count is not padded).

Negative controls through my checker (criterion_ws/scripts/negative_controls_output.txt): dropping the last term gives 128,557 violated equations; changing one single w coefficient gives 627 violated equations. The checker is sensitive to a one-coefficient change.

Author's own script (sh verify-it-yourself/run_checks.sh, run by me): "PASS format=15x16x16 rank=2176", negative control rejected, "ALL CHECKS PASS". Agrees with mine but my verdict rests on my checker.

## Clause-by-clause

1. Format clause. Quoted: "a format (n,m,p) with max(n,m,p) at most 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}". Object declares n = [15, 16, 16]; row lengths decode to 240 = 15*16 (u), 256 = 16*16 (v), 240 = 15*16 (w), consistent. max = 16, sorted format 15x16x16 is not an excluded one. MET.

2. Explicit scheme clause. Quoted: "an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) ... whose number of rank-one terms r". The file holds 2176 explicit rank-one terms with rational coefficients; r = 2176 after dropping zero terms (none to drop). MET.

3. Exact verification over the claimed ring. Quoted: "The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims". Ring field says Q; coefficients have denominators dividing 50400 = 2^5 3^2 5^2 7, so the scheme is over Q (not Z, not ZT) and the claim says Q only. My exact integer check above: 0 violations. MET. The GF(2)-only clause does not apply (this is a characteristic-0 scheme, and over GF(2) it is not even defined because of the denominators).

4. Strictly below all four live sources, each fetched once by me on 2026-10-15 with curl, User-Agent "V3R1T4S-research (honest client; curl)", no retries (criterion_ws/fetch/fetch_log.txt). Quoted: "STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in ... fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in ... README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes".
   - fmm_sota.json (HTTP 200, sha256 d0da2c36...b9bd244c1, createdAt 2026-10-09T11:45:48): entry {"format": [15, 16, 16], "rank": 2223}. 2176 is less. MET.
   - Lille page https://fmm.univ-lille.fr/15x16x16.html (HTTP 200, sha256 ec9909c1...acbedb139f0b2): title "15x16x16:2262"; construction column: 8x8x8:336 + 7x8x8:306 + 8x8x8:336 + 7x8x8:306 + 7x8x8:306 + 8x8x8:336 + 8x8x8:336 = 2262. 2176 is less. MET.
   - Perminov README (HTTP 200, sha256 7b0761ec...8ebba7e78341): status table row for 15x16x16: ZT 2302 (?), Z 2302 (?), Q 2223 (2262); the only other 15x16x16 row (CHANGELOG-style improvement table) says 2262 to 2223 over Q. Minimum over ZT/Z/Q = 2223. 2176 is less. MET.
   - MerlijnW70 fmm-schemes tree (api.github.com git/trees/main?recursive=1, HTTP 200, sha256 f25a290f...807da335e8c37, truncated: false, 39 paths): 33 scheme files, none for 15x16x16 (nearest: 11x16x16_m1749_ZT, 8x16x16_m1256_ZT, 9x14x16_m1260_ZT). No value to beat; the source does not constrain. MET (vacuously for this source; the "ALL of" quantifier is satisfied because the other three are beaten).
   All five of my fetch hashes equal the author's table-record hashes byte for byte, so the author's claimed cells are reproduced, not merely asserted. Minimum over the four sources: 2223; margin 47.

5. Repository's own prior. The V3R1T4S TROPHY_CASE.md (fetched live, HTTP 200, sha256 b4f3ad52...2042cdcc412) row 46 lists 15x16x16 rank 2180 over Q (and the summary row says 2180, updated 2026-10-12). 2176 is strictly below 2180, so this is a genuine 4-term improvement on the project's own best, not a re-submission of an already-held rank. MET.

6. Composition clause. Quoted: "A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations)." 2176 equals no value listed in any of the five sources for 15x16x16 (2223, 2262, 2302, 2302, 2223, 2180). Null model (criterion_ws/scripts/null_model_compositions.py, input the live fmm_sota.json only): the best bound for 15x16x16 obtainable by any single-axis block split, padding to any larger listed format up to 16, or iterated combinations thereof is 2223 (the catalogue entry itself); the best single split is 6x16x16 + 9x16x16 = 2352. Catalogue neighbours: 15x15x16 2132, 14x16x16 2128, 16x16x16 2236, 15x16x17 2448. So no trivial composition of public values reaches 2176 or anything near it. The file's own note says it was derived from a 15x16x17 scheme of rank 2313 (far below the public 2448, so a non-public parent) by restriction along axis 2 plus absorption of 7 terms; that is a derivation, but the clause excludes derivations only when the rank equals a listed value, which it does not. MET.

7. Scope splits. Quoted: "Ternary/integer re-derivations of a rank already attained over Q are NOT this target ...; fewer additions at an existing rank is NOT this target". The object sets a new rank over Q (2176 was attained nowhere), so it is neither a ring upgrade of an existing rank nor an addition-count result. Not excluded. MET.

8. Live re-fetch clause. Quoted: "every one re-fetched live immediately before claiming". Author's table-record timestamps are 2026-10-14T18:44:39Z to 18:44:46Z, one minute before INDEX.csv's fetch time, and my 2026-10-15 fetches return byte-identical pages, so the sources have not moved since. MET.

## Hidden quantifiers and stretched definitions hunted

- Rank inflation by zero terms: none (0 degenerate terms; author's stated m = 2176 = my count).
- Wrong index convention making a wrong scheme look right: ruled out; exactly one of the two conventions passes, with 0 violations, and the failing convention fails on only 7616 equations (consistent with a correct scheme read with C transposed, not a random tensor).
- Ring stretch: the scheme needs 1/2, 1/3, 1/5, 1/7 so it is Q-only; the claim says Q only and the target accepts "over ANY ring". Consistent.
- Sorted-format lookup: all sources are indexed by sorted format; 15x16x16 is already sorted and the object's axes are (15,16,16).
- Source staleness: Perminov's bracketed "(2262)" and "(?)" cells are previous ranks, not open marks; minimum taken over the actual values.

## Partial wins considered

p1 (17 to 32 side) and p2 (GF(2)-only) do not apply: the format has max side 16 and the scheme is over Q with a new overall rank. No partial win is needed; the full criterion is met.

## Verdict

The object is an exact rank-2176 bilinear scheme for 15x16x16 over Q, verified by my own independent exact check (0 of 14,745,600 Brent equations violated), strictly below the minimum 2223 of the four live criterion sources (fmm_sota.json 2223, Lille 2262, Perminov ZT/Z/Q 2302/2302/2223, MerlijnW70 none) and below the repository's own 2180. Full success criterion met; genuine, non-subsumed win.

confirmed_scope: claim/object/15x16x16_r2176_Q.json (sha256 0dee0512255d74595673fd8bfa0df20b0ab0a87785b2d11cbb2a94f6dbd5d57c) is an exact bilinear scheme over Q for the 15x16x16 matrix multiplication format with 2176 rank-one terms, all nonzero, satisfying all 14,745,600 Brent equations in exact integer arithmetic, and 2176 is strictly below 2223, the minimum rank for 15x16x16 in the four live sources fetched 2026-10-15 (fmm_sota.json 2223, Lille page 2262, Perminov README ZT 2302 / Z 2302 / Q 2223, MerlijnW70 tree no entry), and below the V3R1T4S trophy case entry of 2180.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
