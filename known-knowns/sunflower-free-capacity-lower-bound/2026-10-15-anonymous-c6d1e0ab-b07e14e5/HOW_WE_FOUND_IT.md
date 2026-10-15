# How we found it

Contributor text, unverified.

A two-agent team worked the sunflower target on 2026-10-14. Its brief was the bank's criterion (a family with rate above
1.5545) and the partial win p2 (exact small values). The rate bar was not reached: the team proved that no uniform
3-sunflower-free family on 14 or fewer points can beat it, and its best explicit rate was 1.5394. Along the way it
computed exact maxima g(n, r) for small (n, r) by SAT with DRUP proofs, two independent proof checkers and two
independent family checkers, and re-verified everything from a clean copy four times.

What failed: direct SAT on the plain CNF stalls around n = 9 or 10; lex-leader symmetry breaking (sound, see
how-we-built-it/SOUNDNESS.md) and degree cuts extend the range; a link lemma and case splits reach a few more rows, but
those rows are not claimed under p2 because p2 asks for a direct proof of the CNF.

Before claiming, the orchestrator ran two literature scouts (OEIS, arXiv, the Polymath10 project, the hypergraph Turán
literature, this repository's trophy case and pull requests) and read Markström's table of small Turán numbers. Ten of
the team's twenty-two values turned out to be known (the n-r = 2 cases by Mantel's theorem, the n-r = 3 cases by the exact
equivalence with the Turán number of the 3-graph with three edges on four vertices, whose small values Markström tabulates,
and g(12,3) = 20 from Abbott and Gardner); those are not claimed. g(7,3) = 12 is one of the twelve values no source
gave. Then a fresh three-skeptic panel (reproduce, novelty, criterion) checked this package.
