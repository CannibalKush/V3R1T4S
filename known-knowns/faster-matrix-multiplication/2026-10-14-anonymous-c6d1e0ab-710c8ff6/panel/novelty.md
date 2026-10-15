# Novelty skeptic report (fmm-catalogue-small-format-rank)

role: novelty
context: subagent (fresh executor context, only brief + claim/ read)
target_id: fmm-catalogue-small-format-rank

Claim (claim/CLAIM.md): (13, 15, 15) rank 1763 over Q (beats 1776); object 13x15x15_r1763_Q.json. status_source: https://fmm.univ-lille.fr/
Object check: JSON keys n,m,ring,encoding,note,u,v,w; len(u)=len(v)=len(w)=1763 (rank count only; correctness belongs to the verifier role).

Live fetches (single attempt each, curl UA "V3R1T4S-novelty-skeptic"), started Wed Oct 14 13:53:23 UTC 2026:
- 200 https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json -> {"format": [13, 15, 15], "rank": 1776, "exponent": 2.812457}
- 200 https://fmm.univ-lille.fr/13x15x15.html -> "Description of fast matrix multiplication algorithm: <13x15x15:1797>"
- 200 https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md ->
  line 287: | `13x15x15` |  1803 (`Z`)   |   [1776](schemes/results/Q/13x15x15_m1776_Q.json) (`Q`)    |
  line 1434: | `13x15x15` |  1797 (?)   | 1797 (1803)  | 1776 (1803)  |   -> min(ZT,Z,Q) = 1776
  grep -c '1763' README.md -> 0
- MerlijnW70/fmm-schemes git tree (GitHub API, 200, 39 paths, not truncated): no 13x15x15 file (closest: 13x13x15_m1591_ZT.json, 12x13x15_m1464_ZT.json).
- Minimum over all four sources: 1776. 1763 < 1776 strictly.

Prior-art checks:
- TROPHY_CASE.md (raw main): grep for "13.15.15|1763" -> no match.
- V3R1T4S open PRs: #78 thomson, #31, #30, #28 constant-weight-codes, #9, #8 A(34,8,7), #1 -> none on 13x15x15.
- Perminov open PRs: #6 (3x4x5 additions) only.
- Web search "13x15x15 matrix multiplication rank 1763": only Perminov repo hit; its live README lists 1776 (Q) and contains no 1763. No 2024-2026 paper found reporting <= 1763 for <13,15,15>.
- Not a composition at an already-listed rank (1763 is below every listed value).

Conclusion: 1763 strictly beats the best known rank 1776 for <13,15,15> across all four live scoreboards; no earlier claim of this rank found. Novelty confirmed (conditional on exact-arithmetic verification by the verifier role).

pass: true
