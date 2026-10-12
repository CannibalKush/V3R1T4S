# How we found it: no Lehmer number up to 10^50

## The task
An AI agent was asked to turn the best *claimed* lower bound for Lehmer's totient problem (Pinch's uncertified
N > 10^30) into a *certified* one and then push the cap: a capped, logged, exhaustive search over prime factor
sequences for k = 2, with the cases 3 | N and k ≥ 3 closed separately, an exact two-prime closure at every node
("once two primes remain, q can be enumerated directly and r forced"), and every closure logged so that someone else
could check it. The suggested speed-up for the second session, splitting by the smallest prime (5 | N), was to be
measured before being built.

## What was tried, what failed, what worked
- **First session (2026-10-06, from 17:03 PDT).** A C + GMP engine of the plain capped search (spec LCAP-1 in
  `engines/SPEC_LCAP1.md`) with an independent Python implementation reached N > 10^34 in the session and 10^35 and
  10^36 in an overnight background job. Its cost was dominated by the two-prime closure (one divisibility test per
  prime q), growing about 4x per decade, so 10^38 would have taken more than a day.
- **The slated 5 | N split failed on measurement.** The branch with smallest prime ≥ 7 was already pruned to almost
  nothing (1 task of 11 107 at 10^35), so the split saved about 0%. It was not built.
- **What worked: a congruence prune (second session, 2026-10-08 from 04:59 PDT).** If at least two primes remain,
  their product Q satisfies Q ≡ P⁻¹ (mod 8Φ) and lies in a known interval; a node with no such Q is cut with its
  whole subtree (Lemma CRT, `engines/SPEC_LCRT_r1.md`). Together with a candidate closure and Euler's criterion as a
  closure for nodes with few candidates, this took the certified cap to 10^46 by about 06:50.
- **Failure and fix.** The 10^48 job aborted: a two-prime interval needed primes beyond the in-memory sieve. The
  engine got an exact segmented sieve beyond the main sieve (lcrt5), which certified 10^48 and then 10^50 (08:25-08:50,
  1 468 s on 8 workers). Two faster modes (candidate closure instead of the prime loop; trial division before Euler)
  then reran 10^50 in 784 s with identical mode-independent output (09:06). The 60 intervals scanned beyond the main
  sieve were closed a second way by factoring (side check).
- **Independent reruns.** A reviewer agent that never read the author's code wrote vlrt/vlrt2 from the specification
  documents alone. Under a 20-minute rerun cap it covered 3 586 of the 65 647 subtrees (09:13-09:30); a second reviewer
  agent ran the other 62 061 with the same binary (09:36-09:46), and the union matched both author runs subtree by
  subtree. A third reviewer agent wrote lbb2 from the definition with a different tree and different closures, found
  and fixed a bug in its own segmented sieve (it surfaced as a hard error, not a silent pass), validated it on planted
  solutions, and ran 10^50 in 24 minutes (10:17-10:42): complete, no solution.
- **Separately,** a Lean 4 formalization of the reduction and of each pruning rule was added (`lean/`), and the
  release checks in `verify-it-yourself/` were written and run on the shipped logs.

## How long it took
About two hours of agent work on 2026-10-06 plus an overnight job, then about 6 hours on 2026-10-08 (04:59 to 10:42 PDT)
from the first congruence-prune engine to the last independent 10^50 run. Each full 10^50 search takes 10-25 minutes
of wall clock on a 10-core laptop.

## Credits
- Problem: D. H. Lehmer (1932). Reductions and earlier bounds: Lieuwens (1970), Kishore (1977), Cohen and Hagis
  (1980), Hagis (1988), Renze (2004), Pinch (2006), Burcsi, Czirbusz and Farkas (2011); survey by Yamada; recent ω ≥ 16
  work by Mandal, Bhattacharjee and Bhattacharya (see README references).
- Engines, specifications and certificates: an AI agent (author engine lcrt5 and its predecessors).
- Independent engines and reruns: independent reviewer agents (vlrt2 written from the spec only; the 62 061-subtree
  completion run; lbb2 with a different algorithm).
- Libraries: GMP; sympy (certificate and side checks); Lean 4 + Mathlib (formalization).
- Not peer reviewed; see the Limitations section of `README.md`.
