# Reproduce skeptic report (fmm-catalogue-small-format-rank)

role: reproduce
context: subagent (fresh executor context, Grok Bot)
target_id: fmm-catalogue-small-format-rank

## Definition (quoted from CLAIM.md)
"form the r products m_k = (sum_ij U_k,ij A_ij)*(sum_jl V_k,jl B_jl) and check that for every (i,l) sum_k W_k,il m_k equals the symbolic entry (A*B)_il with exact coefficients over the claimed ring ... equivalently check the Brent equations. Count r after dropping zero terms."
Bar: rank strictly below min over fmm_sota.json, Lille page, Perminov ZT/Z/Q, MerlijnW70.

## Integrity
`sha256sum -c ../claim.SHA256SUMS` (run inside claim/): all files OK.
13x15x15_r1763_Q.json sha256 = 710c8ff6593f7c6e578a9ae83b4d7083ed5381db72fd734e614a3108d7c87465

## Own checker (written before reading verify-it-yourself/)
Parsed sparse_flat_pairs (index,value) with Python Fractions; built the full trilinear tensor sum_k U_k ⊗ V_k ⊗ W_k exactly and compared to the <13,15,15> matmul tensor (A index i*15+j, B index j*15+l, C index tried both i*15+l and l*13+i).
Output:
```
lens 1763 1763 1763 r 1763
nonzero terms 1763
maxidx 194 224 194
nonint 19516
W[i*p+l] exact match: False diff count 5760
W[l*n+i] exact match: True diff count 0
```
=> exact Brent equations hold over Q (W stored transposed, C^T convention, which is standard); 1763 nonzero rank-one terms; non-integer rational coefficients present, so the claim is over Q (consistent with ring=Q). Exhaustive full-tensor check, not a sample.

## Author's checker (run afterwards)
`python3 verify-it-yourself/verify_brent.py 13x15x15_r1763_Q.json`
```
PASS file=13x15x15_r1763_Q.json format=13x15x15 rank=1763 primes=2 log2_bound=48
```
Agrees with my exact result. (run_checks.sh not run: it expects package layout object/ + INDEX.csv absent from claim/.)

## Live bar re-fetch (2026-10-14T13:54:31Z)
- fmm_sota.json: `{ "format": [13,15,15], "rank": 1776, "exponent": 2.812457 }`
- https://fmm.univ-lille.fr/13x15x15.html: `13×15×15:1797`
- Perminov README: `| 13x15x15 | 1797 (?) | 1797 (1803) | 1776 (1803) |` (min 1776, Q)
- MerlijnW70 SHA256SUMS: 0 lines matching 13x15x15
Minimum bar = 1776; claimed 1763 < 1776 (margin 13). Matches table-record/.

Caveat: I did not independently audit whether 1763 equals a composition rank listed in Lille's construction column; the live Lille page lists 1797 as best, so no listed construction reaches 1763.

pass: true
