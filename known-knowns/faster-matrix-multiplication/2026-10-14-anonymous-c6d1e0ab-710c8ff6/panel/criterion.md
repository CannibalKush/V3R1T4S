# Criterion skeptic report (fmm-catalogue-small-format-rank)

role: criterion
context: subagent (fresh executor context, saw only the brief and claim/)
target_id: fmm-catalogue-small-format-rank
confirmed_scope: claim/13x15x15_r1763_Q.json (sha256 710c8ff6593f7c6e578a9ae83b4d7083ed5381db72fd734e614a3108d7c87465) is an exactly verified bilinear scheme over Q for the format <13,15,15> with 1763 non-zero rank-one terms, which is strictly less than the minimum rank 1776 across the four live criterion sources fetched 2026-10-14T13:54:59Z-13:55:00Z.

## Criterion read literally
Full success needs: (a) an explicit bilinear scheme, (b) max(n,m,p) <= 16 and sorted format not (3,3,3)/(4,4,4), (c) r STRICTLY LESS than every one of: fmm_sota.json, the Lille per-format page, min over Perminov ZT/Z/Q, the lowest MerlijnW70 rank, all re-fetched live, (d) exact verification over the claimed ring, (e) not a composition/padding equal to an already-listed value, and not a ternary re-derivation or additions-only result.
"Strictly less" (Merriam-Webster, "less": "of lower rank, degree, or importance"/smaller; "strictly" excludes equality) means 1763 < bar with no ties allowed. Nothing in the criterion is stretched here: the claim is the full win, not a partial (p1 needs max dim 17-32; p2 is GF(2)-only; this is Q with max dim 15).

## Format/ring
JSON: n=[13,15,15], ring="Q", encoding sparse_flat_pairs, len(u)=len(v)=len(w)=1763. sorted=(13,15,15), max=15 <= 16, not excluded.

## Independent exact check (my own script, not the shipped one)
Dense U,V,W from sparse pairs, coefficients parsed as Fraction; Brent equations sum_k u_k[a]v_k[b]w_k[c] = delta (a=i*15+j, b=j*15+l, c=l*13+i) checked over all 195*225*195 index triples modulo three primes:
```
r 1763 denoms [1, 2, 5, 10, 16, 17, 20, 25, 34, 50] max|num| 11142
nonzero terms 1763
p 1048573 mismatches 0
p 1048571 mismatches 0
p 1048559 mismatches 0
```
Shipped CRT verifier (deterministic proof with bound) also run:
```
$ python3 verify-it-yourself/verify_brent.py 13x15x15_r1763_Q.json
PASS file=13x15x15_r1763_Q.json format=13x15x15 rank=1763 primes=2 log2_bound=48
```
(run_checks.sh fails only on its package path `object/...`, as CLAIM.md warns; not a defect of the object.)

## Live bar (curl -sS, 2026-10-14T13:54:59Z to 13:55:00Z UTC, all HTTP 200)
- fmm_sota.json (sha256 d0da2c36...244c1): `[{'format': [13, 15, 15], 'rank': 1776, 'exponent': 2.812457}]`
- https://fmm.univ-lille.fr/13x15x15.html (sha256 ce3fdb83...68ee7): `&lang;13&times;15&times;15:1797&rang;`
- Perminov README (sha256 7b0761ec...78341): line 1434 `| 13x15x15 | 1797 (?) | 1797 (1803) | 1776 (1803) |` -> min 1776
- MerlijnW70/fmm-schemes git tree (39 entries, truncated:false): no 13x15x15 in any permutation (only schemes/13x13x15_m1591_ZT.json, a different format).
Bar = min(1776, 1797, 1776) = 1776. 1763 < 1776 (margin 13). Hashes match the claim's table-record fetches.

## Null models / exclusions
- Composition/padding: 1763 is not any listed value (Lille 1797, Q 1776); Lille page lists no lower construction. The derivation (peel of a 14x15x15 r1842 scheme + term elimination) yields a rank not previously listed, so the composition exclusion does not apply.
- Not a ternary re-derivation (rank is new, ring Q), not additions-only, not GF(2)-only.
- Rank counted after dropping zero terms: 1763 nonzero.
- Residual caveat: I did not check unindexed sources beyond the four named (e.g. preprints); the criterion names only these four.

pass: true
