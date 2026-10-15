# CRITERION skeptic report: maxdet-109 (`hadamard-maxdet-records`, cell n = 109)

Inputs read: the claim folder (`CLAIM.md`, `REPRODUCE.md`, `object/`, `table-record/`, `verify-it-yourself/`) and `claim.SHA256SUMS`. All seven listed hashes verify (`shasum -a 256 -c`: 7 OK). Object: `claim/object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt`, sha256 `0108345c2f3cbffdd58f23eef8aba73546583f02062a013a5b64ab95e198faa6`.

The author's shipped checker cannot run from the package: `run_checks.sh` needs `INDEX.csv` and `verify-it-yourself/maxdet_table.json`, neither of which is in the claim folder. Every check below is therefore my own (scripts written fresh in my workspace; Python 3 with numpy/mpmath; no sympy available).

## Live fetches (one honest GET each, User-Agent `V3R1T4S-research (honest client; curl)`, no retries), 2026-10-14 16:16-16:23 UTC

| Source | HTTP | sha256 of fetched bytes | What it says about n = 109 |
|---|---|---|---|
| raw.githubusercontent.com Math-AI-Caltech/hadamard-maxdet `README.md` | 200 | `a445d967…4abd` (2,146 B) | Covers orders 51, 103, 107, 111, 115, 119 only. No n = 109 row. Points to the Archive-It copy of the MaxDet database. |
| same repo, `maxdet_records.csv` | 200 | `884d99a5…f2c9` (7 data rows) | No n = 109 row. |
| arxiv.org/abs/2608.22518 | 200 | `8aa955ce…9a7a` | Latest version is v3 (1 Oct 2026). |
| arxiv.org/html/2608.22518v3 | 200 | `ed31ecc9…0bb6` (570,907 B) | "109" occurs once, as a journal volume number in a citation; no table cell or formula alt-text contains 109. No n = 109 value. |
| archive.org Wayback availability API for `www.indiana.edu/~maxdet/` | 200 | `0e01cccc…7083` | `archived_snapshots: {}` (no archive.org snapshot returned). |
| wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/ (the copy the README references) | 200 (served 20190314205221) | `5408c439…fa5e` | Orrick's "The Hadamard maximal determinant problem" index; links `page3.shtml` for orders 80-119 and `d109.html`. |
| archived `page3.shtml` (orders 80-119) | 200 (served 20190315055615) | `f73ec1ed…7f27` | Row 109: Det `1.877483842E78`, flagged `??` (not known maximal), R = `.65`. |
| archived `d109.html` | 200 (served 20190316001217) | `31d88ca8…bc6c` | "Matrix found by Tomas Rokicki", linking tomas.rokicki.com/newrec.html. |
| tomas.rokicki.com/newrec.html (live) | 200 | `35007699…083a` | Row `108 A 1.87748e+78` (N is the 0/1 size; 0/1 size 108 = ±1 order 109) with the two 54-character circulant first rows; `matresults/best108.html` is its detail page, which is the `rokicki_best108.html` the author's expected output cites. |
| einsteinarena.com | 200 | `5f383832…773d` | Only Hadamard entry: "Hadamard Maximal Determinant (order 51)". No 109. |
| export.arxiv.org API, `all:"maximal determinant"`, newest first, max 40 | 200 | `81d22a95…c770` | 36 results total; newest relevant is 2608.22518v3 itself; no other 2026 paper on ±1 maximal determinants. |
| arxiv.org/pdf/1208.1805 (Brent-Osborn, bordered-Hadamard lower bounds) | 200 | `a285e7ee…3836` | pdftotext: no "108"/"109" as numbers; one asymptotic table only. |
| arxiv.org/pdf/1402.6817 (Brent-Osborn-Smith, probabilistic lower bounds) | 200 | `61a29245…dfd1` | pdftotext: no "108"/"109" as numbers; tables are for h = 664 and h = 996. |
| maths-people.anu.edu.au/~brent/maxdet/ | 200 | `22fbf3f7…6f88` | Papers and talks list; no record table for n = 109. |

## The success criterion, clause by clause

**Clause 1.** "Success means an explicit n x n +-1 matrix"
Met. The file parses as 109 rows of 109 whitespace-separated integers (11,881 tokens: 6,576 of `1`, 5,305 of `-1`; no other characters). n = 109 is not divisible by 4 (bank scope) and 109 = 1 mod 4.

**Clause 2.** "whose exact integer |det| (Bareiss on Python ints, cross-checked with sympy)"
Met in substance; the named cross-check tool was substituted. My own fraction-free Bareiss on Python ints gives det = +687720580550393685384435488623154547762327053849477344513207580440243395287690372410950406599169376107974623232. An independently written Gaussian elimination modulo 8 primes just below 2^61 (product about 2^488, above the Hadamard bound 109^54.5 of about 2^369) with CRT reconstruction gives the identical integer; mpmath at 120 digits agrees to relative error 6.8e-121. |det| is divisible by 2^108 and |det| / 2^108 = 2119202655125403624550373680790052808829003860176536932438843923020304438454497 = 291 * 27^53, equal to the claim sentence, the filename and the author's expected output. sympy is not installed, so the literal "cross-checked with sympy" token is not satisfied; the kit instruction to this skeptic authorises an exact modular determinant as the second method, and that is what was used.

**Clause 3.** "is STRICTLY GREATER (direction: max) than the max, at verification time, of: the archived MaxDet value (Wayback copy referenced by Math-AI-Caltech), the arXiv:2608.22518 / Math-AI-Caltech CSV value, the EinsteinArena order-51 leaderboard, and any newer arXiv value."
Met. At verification time (table above) the only n = 109 value carried by any enumerated source is the archived MaxDet value `1.877483842E78` (Orrick's table, Archive-It copy referenced by the Math-AI-Caltech README), attributed to Tomas Rokicki. Rokicki's live page still lists it as `1.87748e+78`. I reconstructed his matrix from the two published 54-character first rows a, b as the 0/1 matrix [[A, B], [B^T, J - A^T]] (A, B circulant) and got det exactly 1877483841834222713683125485573890072927341503771574105042244268774869908324352, which is the author's `D_prev` to the digit (a 108 x 108 0/1 determinant equals the ±1 order-109 determinant divided by 2^108). Claim / record = 1.128746, strictly greater, with a margin far beyond the table's 10 significant digits. The arXiv:2608.22518v3 paper and the Math-AI-Caltech README/CSV carry no n = 109 value (they cover 51, 103, 107, 111, 115, 119). EinsteinArena lists only order 51, so it carries no n = 109 value. The arXiv search found no newer paper with an n = 109 value; the natural older home for a bordered-Hadamard value at n = 108 + 1 (Brent-Osborn 1208.1805, Brent-Osborn-Smith 1402.6817) contains none. Limit: an arXiv paper that avoids the phrase "maximal determinant" would escape the search; within the sources the criterion enumerates the max is 1.877483842E78.

Provenance defect in the claim package (does not change the comparison): `table-record/` says the n = 109 record was "extracted" from the Math-AI-Caltech README with page sha256 `7b6160e3…3463`. The live README has sha256 `a445d967…4abd` and contains no n = 109 row at all; the Math-AI-Caltech repo never covered n = 109. The number the author compared against is correct, but its stated source is not reproducible; the author's own expected output names the real source (`rokicki_best108.html`).

**Clause 4.** "It must not exceed the residue-class upper bound (Barba for n = 1 mod 4, Ehlich-Wojtas for n = 2 mod 4, or the Ehlich n = 3 mod 4 bound in the form valid for that n range)."
Met. 109 = 1 mod 4, so the Barba bound applies: |det|^2 <= (2n - 1)(n - 1)^(n - 1) = 217 * 108^108. Exact integer comparison: |det|^2 < 217 * 108^108, strictly. |det| / Barba = 0.731643. floor(Barba / 2^108) = 2896497323385832583622927428277996632836928103583147613858951575196511441468179, matching the author's `B_norm`.

**Clause 5.** "The order must be one where the previous record was strictly below that bound."
Met, two ways. Numerically: (1877483841834222713683125485573890072927341503771574105042244268774869908324352 * 2^108)^2 < 217 * 108^108, ratio to the bound 0.648191; the archive itself flags n = 109 with `??` and R = .65. Structurally: 2n - 1 = 217 is not a perfect square, and Barba's bound is attained only when the Gram matrix is (n-1)I + J, whose determinant (2n-1)(n-1)^(n-1) must then be a perfect square; so no ±1 matrix of order 109 can reach the bound, and the previous record was necessarily strictly below it.

## Null models and definition checks

- Random 109 x 109 ±1 matrix: |det| is of order sqrt(109!) ~ 1e88 before the 2^108 scaling, i.e. a normalised value around 1e56, 22 orders of magnitude below both record and claim. Not a null-model artefact.
- The object is a bordered Hadamard matrix: row 0 and column 0 are the border (corner -1, the other 216 border entries +1) and the 108 x 108 minor H is a Hadamard matrix (Gram = 108 I). With u the border column, |Hu|_1 = (Hu).v = 1056, so |det| = 108^54 * (1 + 1056/108) = 1164 * 108^53 = 2^108 * 291 * 27^53, exactly. A random border gives an expected factor 1 + sqrt(2*108/pi) = 9.29, i.e. about 251 * 27^53 = 1.83e78, which would NOT beat Rokicki's 1.877e78; the claimed border reaches 10.78 (|Hu|_1 = 1056 against the Cauchy-Schwarz ceiling 108^1.5 = 1122.4, 94 percent of it). The construction type is classical, but no published value at or above 291 * 27^53 for n = 109 exists in the enumerated sources or in the bordered-Hadamard papers checked, and generic published bounds on |Hu|_1 (Best, Brent-Osborn) give smaller factors. The criterion asks for a strictly larger explicit matrix, not a new method.
- Hidden quantifier "at verification time": satisfied by the fetches listed above, all on 2026-10-14 between 16:16 and 16:23 UTC.
- "best known value" in the claim sentence and "live target" in the bank statement: n = 109 is a 1 mod 4 order above 22 with archive ratio .65 and no learning-method result, exactly the class the bank names as live.

## Partial wins considered

- `p1` (maximality certificate): not claimed and not applicable; the result is a new lower bound, not a proof of maximality.
- `p2` (frozen Gram target): not claimed. Not needed: a full explicit matrix beating the record meets the full criterion and strictly dominates a Gram target for the same order.

## Verdict

The claim meets every clause of the full success criterion as written, with one method substitution (an exact 8-prime CRT determinant in place of sympy, as the kit allows this skeptic) and one bookkeeping defect in the claim package (the stated README provenance of the record is not reproducible, though the record value itself is confirmed exactly from the archived MaxDet table and Rokicki's live page). The win is genuine and not subsumed by any published value found. PASS.

confirmed_scope: The 109 x 109 {+1,-1} matrix in claim/object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt (sha256 0108345c2f3cbffdd58f23eef8aba73546583f02062a013a5b64ab95e198faa6) has exact |det| = 2^108 * 291 * 27^53 = 2^108 * 2119202655125403624550373680790052808829003860176536932438843923020304438454497 (Bareiss, 8-prime CRT and 120-digit mpmath agree), which is strictly below the Barba bound for n = 109 (ratio 0.731643) and strictly above the only n = 109 value carried by the criterion's enumerated sources at verification time on 2026-10-14 16:16-16:23 UTC, Rokicki's 2005 two-circulant record 1877483841834222713683125485573890072927341503771574105042244268774869908324352 (= 1.877483842E78 in the Archive-It copy of Orrick's MaxDet table, itself strictly below the bound at ratio 0.648191, reproduced exactly from Rokicki's published first rows), while the arXiv:2608.22518v3 / Math-AI-Caltech CSV and EinsteinArena order-51 sources carry no n = 109 value and an arXiv search found no newer n = 109 value.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
