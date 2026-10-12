# Fast matrix multiplication: five rational schemes of record rank

A *scheme* of rank r for the format <n1,n2,n3> is a list of r rank-one bilinear products from which the product of
an n1×n2 matrix and an n2×n3 matrix can be read off, i.e. a decomposition of the matrix multiplication tensor into r
rank-one terms (the *Brent equations*). Smaller r is better; the current best ranks are collected in a few public
catalogues.

**Claim (exact scope), as of 2026-10-10, updated 2026-10-12.** The five record files in `schemes/` are schemes with
rational coefficients that satisfy the Brent equations exactly over Q, with the ranks below, and each rank is
**strictly smaller than the smallest value listed for that format by any of the four criterion sources** as fetched
on 2026-10-10 between 19:25:52Z and 19:25:53Z (one GET per source with an honest User-Agent, no retries;
`the-record-we-beat/sources_2026-10-10T19-25-52Z.json`):

- `fmm_sota.json` of the Lille catalogue digest (github.com/sedoglavic/fmm_digest; `createdAt` 2026-10-09T11:45:48),
- the "Research Findings & Status" table of Perminov's README (github.com/dronperminov/FastMatrixMultiplication;
  columns ZT / Z / Q),
- the scheme list (`SHA256SUMS`) of github.com/MerlijnW70/fmm-schemes,
- `generated/COVERAGE.md` of github.com/solven-eu/matmulcatalog (F2 and R/Q/Z columns).

| format (sorted) | our rank | fmm_sota | Perminov ZT / Z / Q | MerlijnW70 | matmulcatalog F2 / R,Q,Z | bar (min) | margin | file |
|---|---|---|---|---|---|---|---|---|
| <14,15,15> | **1842** | 1848 | 1905 / 1895 / 1848 | — | 1895 / 1890 | 1848 | −6 | `schemes/14x15x15_r1842_Q.json` |
| <13,14,14> | **1558** | 1582 | 1614 / 1614 / 1582 | — | 1614 / 1614 | 1582 | −24 | `schemes/13x14x14_r1558_Q.json` |
| <15,16,16> | **2180** | 2223 | 2302 / 2302 / 2223 | — | 2302 / 2302 | 2223 | −43 | `schemes/15x16x16_r2180_Q.json` |
| <14,14,15> | **1716** | 1789 | 1798 / 1798 / 1790 | — | 1798 / 1798 | 1789 | −73 | `schemes/14x14x15_r1716_Q.json` |
| <13,14,15> | **1677** | 1681 | 1681 / 1681 / 1681 | — | 1681 / 1681 | 1681 | −4 | `schemes/13x14x15_r1677_Q.json` |

**Update 2026-10-12.** The first release (2026-10-10) had <14,15,15> at **1843** (margin −5) and <15,16,16> at
**2196** (margin −27). Both are **superseded by our own 1842 and 2180**, obtained from them by absorbing linear
dependencies (below). The files `schemes/14x15x15_r1843_Q.json` and `schemes/15x16x16_r2196_Q.json` are kept: they are
valid schemes, the parents of the new ones, and the 1843 is also the parent of the <14,14,15>:1716; `INDEX.csv`
marks them "superseded by our own 1842" / "2180". The public minimum was re-checked on 2026-10-12: <14,15,15> at
10:22Z, 1848; <15,16,16> at 12:41Z, 2223 (fmm_sota.json 2223, Lille page 2262, Perminov Q 2223, MerlijnW70 none).
Same-day fetches of the four criterion sources were byte-identical to the 2026-10-10 snapshot
(`the-record-we-beat/live_recheck_2026-10-12.json`). The other three formats are unchanged.

The same five bars (1848, 1582, 2223, 1789, 1681) were found by our agents's own comparisons on 2026-10-09 and
2026-10-10T06:16Z, except that on 2026-10-09T01:49Z the <14,14,15> bar was 1790 (fmm_sota.json has listed 1789 since
its 2026-10-09T11:45 rebuild). The per-format pages of the Lille catalogue (fmm.univ-lille.fr) lag behind the digest
and are not a criterion source; LITA's README lists square formats only.

**Status.** Found by AI agents (see `READ_BEFORE_CITING.md` at the repository root) on 2026-10-08 (the 1842 and 2180
confirmed on 2026-10-12, each by three separate reviewers), checked internally and by the checker shipped here,
**not peer reviewed and not yet submitted** to the catalogue maintainers at the time of this release. These are rank
bounds for specific formats over Q; they do not change the asymptotic exponent of matrix multiplication. The schemes
use non-integer rational coefficients (denominators such as 2, 4, 5, 8, 17, 350, 1088), so they say nothing about the
ZT or Z columns, where other values apply.

## How the schemes were made, and whose work they build on

All five are **derived from the square schemes of LITA** (Kirill Khoruzhii, Luzian Serafin, Patrick Gelß and
Sebastian Pokutta, *Local Improvements to Trilinear Aggregation*, github.com/khoruzhii/lita, schemes pushed
2026-10-07, building on Victor Pan's trilinear aggregation): <15,15,15> rank 1977, <14,14,14> rank 1593 and
<16,16,16> rank 2236. **Please credit them**; the schemes here are derived objects.

Restricting <n,m,p> to <n,m,p−1> ("peeling a slice") turns a scheme into a scheme for the smaller format; the
published projection step (Perminov's meta flip graph, arXiv:2606.02480, and Kauers–Wood, arXiv:2510.19787) deletes
one coordinate row or column. Our agents used a *generalised one-slice peel*: restrict along an arbitrary direction
pair (e, f) with ⟨e, f⟩ ≠ 0 instead of a coordinate; a term disappears exactly when its relevant factor is
proportional to e (or to f), so choosing (e, f) to match the factors of many terms removes many terms at once.

| scheme | obtained from | step |
|---|---|---|
| <14,15,15>:1843 (superseded) | LITA <15,15,15>:1977, n-axis | peel, e = (1,1,1,1,1,1,1,−5,1,1,1,1,1,1,1), f = e_0 |
| **<14,15,15>:1842** | our <14,15,15>:1843 | absorption of one exact 7-term v⊗w dependency (term 1628 removed) |
| <13,14,14>:1558 | LITA <14,14,14>:1593, n-axis | peel, e = e_1 + e_8, f = e_0 − e_1 |
| <15,16,16>:2196 (superseded) | LITA <16,16,16>:2236, n-axis | peel, e = e_1 + e_9, f = e_0 − e_1 |
| **<15,16,16>:2180** | our <15,16,16>:2196 | absorption of the 8-dimensional u⊗v nullspace with max-kill w-shifts (16 terms removed) |
| <14,14,15>:1716 | our <14,15,15>:1843, m-axis | peel, e = e_0, f = (1,1,1,1,1,1,1,−5,1,1,1,1,1,1,1) |
| <13,14,15>:1677 | our <14,14,15>:1716, n-axis | peel, e = e_1 + e_9, f = e_1 |

*Absorption.* If the pair factors of a scheme are linearly dependent, ∑_k c_k v_k ⊗ w_k = 0 (or the same for u⊗w,
u⊗v), the free factors can be shifted, u_k → u_k − c_k ζ for any vector ζ, without changing the tensor; a term whose
new factor is zero disappears. With one dependency and ζ = u_j/c_j this removes term j (1843 → 1842). With the
8-dimensional u⊗v nullspace of the 2196, one shift per dependency chosen to match two w-factors at once removes 16
terms (2196 → 2180; one term per dependency would give 2188). All three pairings of the 2180 then have full rank.

The best *coordinate* slice of the three LITA squares removes 30, 0 and 0 terms, which would not reach any of the bars.
The sweep, peel and absorption code is in [`how-we-built-it/`](how-we-built-it/README.md) (it regenerates the five
peeled files byte for byte from LITA's files, and the 1842 and 2180 term for term from the 1843 and 2196); the story of
the search is in [`HOW_WE_FOUND_IT.md`](HOW_WE_FOUND_IT.md). The claim rests on the scheme files and the checker.

## Please cite

Our schemes are all derived from LITA's public square schemes. The LITA repository (https://github.com/khoruzhii/lita)
has no license; we will remove or relicense the derived schemes on request. If you use these schemes, please cite LITA
as its README asks (an associated manuscript is in preparation):

```bibtex
@misc{khoruzhii2026lita,
  author = {Kirill Khoruzhii and Luzian Serafin and Patrick Gel{\ss} and Sebastian Pokutta},
  title = {Local Improvements to Trilinear Aggregation},
  year = {2026},
  url = {https://github.com/khoruzhii/lita}
}
```

## File format

JSON as in Perminov's repository: `n = [n1, n2, n3]`, `u` (r rows of length n1·n2, index i·n2+j ↔ A_ij), `v`
(r rows of length n2·n3, index j·n3+l ↔ B_jl), `w` (r rows of length n3·n1, index l·n1+i ↔ coefficient of the
product in C_il); coefficients are integers or strings `"p/q"`; `ring` is `Q`; `note` records the peel.

## Checking

`verify-it-yourself/fmmcheck.py` (python3 + numpy, written for this release from the definition) checks every Brent equation,
∑_k u_k[a] v_k[b] w_k[c] = δ, for all (n1n2)(n2n3)(n3n1) index triples, and counts the rank as the number of terms
whose three factors are all nonzero. It computes the residual modulo several primes p < 2^20 (exact in float64 BLAS
products) and adds primes until their product exceeds 2·L·(S+1), where L clears all denominators and S bounds the
size of any residual; a zero residual modulo all of them is therefore a **proof** that the residual is zero over Q
(Chinese remainder theorem), not a probabilistic test. `verify-it-yourself/mutate.py` writes three broken variants (a dropped term,
a changed coefficient, two swapped factors) that the checker must reject. `sh verify-it-yourself/run_checks.sh` runs everything;
output at release time, and of the checks of the 1842 and 2180 on 2026-10-12, in `verify-it-yourself/RECEIPTS.md`. Before release the schemes had also passed the author's
exact big-integer checker and an independent reviewer's Fraction and modular-CRT checkers.

## Limitations

- Internal verification only; no outside expert has looked at the schemes yet.
- Margins of −4 (<13,14,15>) and −6 (<14,15,15>) are small; the catalogues change often (fmm_sota.json changed on 2026-10-09).
- Rank over Q only. Nothing is claimed for integer or F2 schemes of these formats.
- The schemes are derived from LITA's published schemes; LITA's repository stated no license at fetch time. We
  redistribute only our derived decompositions, with credit, and will remove or relicense them on request.

## Files

```
README.md, RUN_IT_YOURSELF.md, INDEX.csv, HOW_WE_FOUND_IT.md
schemes/             the five record schemes and the superseded 1843 and 2196 (JSON, 3–8 MB each)
how-we-built-it/     peel.py, sweep.py, make_scheme.py, fetch_lita.sh, regenerate_all.sh (peels);
                     absorb_exact.py, maxkill.py, pairtools.py (absorption)
verify-it-yourself/  fmmcheck.py, mutate.py, run_checks.sh, RECEIPTS.md
the-record-we-beat/  sources_2026-10-10T19-25-52Z.json (fetch times, ETags, sha256 and parsed values of the criterion sources),
                     parse_sources.py (the parser), live_recheck_2026-10-12.json (re-check for the 1842 and 2180)
```

## References

- K. Khoruzhii, L. Serafin, P. Gelß, S. Pokutta, *Local Improvements to Trilinear Aggregation*, github.com/khoruzhii/lita (2026).
- V. Y. Pan, trilinear aggregation, FOCS 1978 (doi:10.1109/SFCS.1978.34) and Comput. Math. Appl. 8 (1982).
- Perminov, arXiv:2606.02480 (2026), and github.com/dronperminov/FastMatrixMultiplication.
- Kauers and Wood, arXiv:2510.19787.
- M. Kauers and J. Moosbauer, *Flip graphs for matrix multiplication*, arXiv:2212.01175 (reductions).
- A. Sedoglavic, catalogue of fast matrix multiplication algorithms, fmm.univ-lille.fr, digest github.com/sedoglavic/fmm_digest.
- R. P. Brent, *Algorithms for matrix multiplication*, Stanford report STAN-CS-70-157 (1970) (the Brent equations).
