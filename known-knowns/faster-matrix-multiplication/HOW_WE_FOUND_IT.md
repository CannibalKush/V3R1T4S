# How we found it

## The brief

The target was the public record tables of fast matrix multiplication: find an explicit bilinear scheme for some
format <n,m,p> with max(n,m,p) ≤ 16 (not <3,3,3> or <4,4,4>) with strictly fewer rank-one terms than every live
record source, verified in exact arithmetic. A preliminary survey by an AI agent had pinned the four record sources,
written an exact checker, and flagged that LITA (github.com/khoruzhii/lita) had pushed new square schemes on
2026-10-07, <14,14,14>:1593 and <16,16,16>:2236, below every table, so they had to be treated as a fifth bar.

The AI agent that found these schemes was asked to *extend* a published technique rather than invent a new one;
its chosen angle was a "generalised one-slice peel" of public larger-format record schemes.

## What was tried

1. A census of the catalogue: for each format, how many terms a one-slice restriction of the next-larger record
   scheme would have to remove to beat the bar. This pointed at <13,14,14> and <15,16,16> (needing 12 and 14
   removals from LITA's new 1593 and 2236).
2. Coordinate peels (deleting one row or column, the projection step of Perminov's meta flip graph and of
   Kauers–Wood) of about 1,200 public record schemes (Perminov, MerlijnW70, Lille, LITA). None reached a bar;
   on LITA's schemes they remove 0 (even sizes) or 30 (size 15) terms.
3. The generalisation: restrict along an arbitrary pair of directions (e, f) with ⟨e, f⟩ ≠ 0. A term disappears
   exactly when its relevant factor is rank one with fiber direction e (or f), so the best pair is found exactly by
   grouping the terms by those directions (`how-we-built-it/peel.py`). The restricted scheme is then rebuilt in
   exact rational arithmetic and checked.
4. A pair-factor linear-dependency test (a dependency among u_k⊗v_k lets one term be absorbed), a GF(3) flip-graph
   walk on the new 1843-term scheme (7-minute cap), and a top-2 multi-step peel-chain search.

## What failed

- Coordinate peels: no format reached its bar. With the best direction pair, 33 restrictions of non-LITA schemes
  landed exactly on a bar (equal, not better).
- The dependency test found no reducible record scheme among about 1,140 integer ones (it found one on a
  non-record scheme, as a positive control). An early version mis-scaled rational rows and raised two false alarms;
  this was found and fixed during the run.
- The GF(3) walk found nothing within its cap. Near misses: <12,13,13> 1276 from LITA 13³ (bar 1274), and
  <14,14,14> 1596 by a three-step chain (LITA has 1593). Second peels of 1558 and 2196 did not reach any bar.

## What worked

The generalised peel of LITA's squares along the first axis: 15³:1977 → <14,15,15>:1843 (134 terms removed), 14³:1593 →
<13,14,14>:1558 (35), 16³:2236 → <15,16,16>:2196 (40). Peeling the new 1843 scheme again gave <14,14,15>:1716 (127 removed)
and peeling that gave <13,14,15>:1677 (39 removed). Exact commands: `how-we-built-it/README.md`.

## Later: absorbing linear dependencies (1843 → 1842, 2196 → 2180; confirmed 2026-10-12)

A peeled scheme can carry linear dependencies among its *pair factors*. If ∑_k c_k v_k ⊗ w_k = 0 with c_j ≠ 0, then
term j can be removed by adding −(c_k/c_j)·u_j to the u-factor of every other term in the dependency, without changing
the tensor (the same works for the u⊗w and u⊗v pairings). This elementary move generalises the "reduction" step of
flip-graph searches (Kauers–Moosbauer), where two terms share two factors. On the 1843 an agent found one exact 7-term
zero sum in the v⊗w pairing (all coefficients 1; found on the night of 2026-10-08 with a float-guided search, packaged
and re-derived exactly on 2026-10-12); absorbing term 1628 gives <14,15,15>:**1842**. The 2196 has an 8-dimensional
nullspace in its u⊗v pairing. Absorbing it one pivot per dependency (canonical row-reduced basis) gives 2188. But here
the free factor can be shifted, w_k → w_k − ∑_s c^(s)_k ζ_s for *any* vectors ζ_s, and a term dies when its new w is
zero. Choosing each ζ_s as the normalised w-factor that occurs most often among the terms of that dependency kills two
terms per dependency, 16 in all: <15,16,16>:**2180**. Afterwards all three pairings of the 2180 have full rank, so no
further one-step absorption exists, and 16 is the most this move class can remove from the 2196. The nullspaces are
computed modulo three primes, lifted by CRT and rational reconstruction, and every null vector is checked exactly over
Q before it is used. Code and commands: `how-we-built-it/README.md` ("Absorption").

## How long it took

On 2026-10-08 (US Pacific time): the agent started at 17:45, wrote its plan by 17:52, and the census was done at 17:58.
The three single peels were written at 18:02–18:08, <14,14,15>:1716 at 18:38 and <13,14,15>:1677 at 18:53; the
write-up was finished at 19:00. That is about 1 h 15 min of wall-clock time, on a shared Apple M5 laptop.

## Checks and credits

- The agent checked the schemes with exact checkers (its own big-integer one; the survey's fraction and CRT modes).
- An independent reviewer agent, 19:00–19:20 the same evening, re-verified all five with its own code (CRT-modular
  and random big-integer evaluation), rebuilt them from LITA's files, re-checked the restriction lemma, and re-fetched
  every source. Further reviewer agents checked novelty, reproduction and the success criterion. The release checker
  `verify-it-yourself/fmmcheck.py` was written later from the definition.
- The 1842 and the 2180 were each checked on 2026-10-12 by three separate reviewer agents with their own exact
  checkers; the derivation of each from its parent (1843, 2196) was also certified in exact arithmetic.
- **Seed schemes:** Kirill Khoruzhii, Luzian Serafin, Patrick Gelß and Sebastian Pokutta (LITA), building on Victor Pan's
  trilinear aggregation. **Projection idea:** Perminov (arXiv:2606.02480) and Kauers–Wood (arXiv:2510.19787). **Reductions in flip graphs:**
  Kauers and Moosbauer (arXiv:2212.01175).
  **Record tables:** Sedoglavic (Lille catalogue), Perminov, MerlijnW70, solven-eu/matmulcatalog.
