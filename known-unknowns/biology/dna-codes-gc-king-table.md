# DNA codes with constant GC-content: beat a lower bound in the Gaborit-King A_4^GC(n,d,w) table

🦠 **Biology** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Oliver King's table (rambutan.umassmed.edu/king/dnacodes.html, last updated June 23, 2010) lists best-known lower bounds for A_4^GC(n,d,w): the maximum size of a quaternary (A,C,G,T) code of length n, minimum Hamming distance d, with every codeword containing exactly w = floor(n/2) G/C letters, for 4 <= n <= 20, 3 <= d <= 20. Entries marked '.' or ':' are proven optimal. Construct an explicit code strictly larger than the table entry for an unmarked (n,d). These codes are used for DNA data storage address/primer design and microarray probes.

## What counts as a win

A plain-text list of codewords for some (n,d) whose table entry on https://rambutan.umassmed.edu/king/dnacodes.html is NOT followed by '.' or ':' such that a checker confirms all words have length n over {A,C,G,T}, exactly the table's GC-content w (w = floor(n/2), confirm from King 2003), pairwise Hamming distance >= d, are distinct, and the count is strictly greater than the table entry re-fetched live immediately before claiming, AND strictly greater than any value for the same (n,d,w) found by a novelty search of post-2010 literature (e.g. Limbachiya-Gupta-Rao altruistic-algorithm papers, Montemanni-Smith, arXiv 1903.03535, 2108.02033).

## Partial wins

- **tie-unmarked-mid:** Reproduce (tie) an unmarked 'v' (variable-neighbourhood-search) entry with n >= 14 from scratch with our own search, checker-confirmed.
- **new-optimality-proof:** Prove an unmarked entry optimal via exact max-clique with symmetry breaking, producing a checkable certificate (e.g. clique-solver log + upper-bound LP).

## How a win is checked

Python checker: read codewords, assert alphabet, length, GC count, uniqueness, all-pairs Hamming distance >= d (n<=20 and sizes <= ~10^5 is seconds with numpy bit tricks), compare size to live table cell. Run on a code file from the page's codes/ directory first.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://rambutan.umassmed.edu/king/dnacodes.html>

## Sources

- <https://rambutan.umassmed.edu/king/dnacodes.html>
- <https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r33>
- <https://arxiv.org/abs/2403.11551>
- <https://arxiv.org/abs/2108.02033>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Max-clique search on the GC-constrained Hamming graph with automorphism (coordinate permutation x base-swap A<->T, C<->G) orbit reduction, then clique solvers (e.g. MoMC / cliquer) on quotient graphs.
- Variable-neighbourhood search / tabu with conflict-driven replacement, starting from the table's own linear codes in codes/LinearGC.txt.
- Linear and additive codes over GF(4)/Z4 with GC-weight selection: search quasi-cyclic generator matrices and take the largest constant-GC coset slice.
- Cross-domain import (constant-weight binary codes): map A/T vs G/C to a weight constraint and lift known record constant-weight codes from Brouwer's tables (our bank already confirmed wins there) via product/concatenation constructions.
- Cross-domain import (SAT/SMT scheduling): encode 'size >= table+1' as a SAT instance with symmetry-breaking predicates and run kissat/cadical for small n (n<=12).
- Cross-domain import (sphere packing/lattice codes): Construction A from quaternary lattices and spherical-code style greedy-with-repulsion annealing.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The table is stale (2010); later papers (Limbachiya et al. 2016-2018, Montemanni-Smith, Smith-Aboluion-Montemanni-Perkins) may already exceed some cells - a 'win' versus the page alone is not novel.
- GC-content w: the table fixes w = floor(n/2); a code with mixed or different GC weights is not admissible.
- Do not confuse with the GC,RC table directly below it on the same page (different, stricter constraint).
- Entries ending in '.' or ':' are proven optimal; exceeding one indicates a checker bug.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/dna-codes-gc-king-table.md
```

Already set up? Say `run V3R1T4S on dna-codes-gc-king-table`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `dna-codes-gc-king-table`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
