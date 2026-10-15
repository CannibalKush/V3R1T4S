# DNA codes with GC-content and reverse-complement constraint: beat a lower bound in the A_4^GC,RC(n,d,w) table

🦠 **Biology** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Same page as the GC table, second table: A_4^GC,RC(n,d,w) additionally requires Hamming distance >= d between any codeword and the reverse-complement of any codeword (including itself), the constraint that prevents unwanted hybridization in DNA storage/computing. Lower bounds for 4 <= n <= 20 listed; many mid-range 'v' (VNS) and 'c' (linear) entries are not known optimal. Construct a strictly larger code for any unmarked (n,d).

## What counts as a win

A codeword list for some (n,d) whose A_4^GC,RC entry on https://rambutan.umassmed.edu/king/dnacodes.html is not followed by '.' or ':', checked to satisfy: length n, alphabet ACGT, GC count = floor(n/2), pairwise Hamming >= d, Hamming(x, rc(y)) >= d for all x,y including x=y, distinct; size strictly greater than the live table entry re-fetched immediately before claiming and than any post-2010 published value for the same parameters (novelty search, e.g. arXiv 1903.03535 lists GC,RC improvements).

## Partial wins

- **halving-gap:** For an unmarked (n,d), a code of size > half the GC-table entry, beating the GC,RC entry by construction from an RC-closed GC code (checker-confirmed).
- **tie-v-entry-n>=15:** Tie a 'v' entry with n >= 15 using our own search from scratch.

## How a win is checked

Same checker as the GC table plus the reverse-complement constraint (rc = reverse + A<->T, C<->G) applied to all ordered pairs including self-pairs. Seconds.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://rambutan.umassmed.edu/king/dnacodes.html>

## Sources

- <https://rambutan.umassmed.edu/king/dnacodes.html>
- <https://arxiv.org/abs/2108.02033>
- <https://arxiv.org/abs/2403.11551>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Build codes as unions of RC-orbit pairs {x, rc(x)}: search on the quotient graph of orbit pairs with max-clique / VNS.
- Reversible cyclic and quasi-cyclic codes over GF(4) (Gaborit-King linear constructions, reversible G^k codes) restricted to the GC-weight slice, then greedy completion.
- Simulated annealing with tabu over codeword swaps, objective = size with conflict penalty; 10 parallel chains seeded from the page's codes/LinearGCRC.txt.
- Cross-domain import (graph colouring/register allocation): Kempe-chain style recolouring moves on the conflict graph to free room for an extra codeword.
- Cross-domain import (frequency hopping / radar sequence design): use difference-set and Costas-style algebraic constructions with built-in reversal symmetry as seeds.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Self-constraint: Hamming(x, rc(x)) >= d is required; omitting it inflates sizes and is the most common false positive.
- Some authors use the 'Watson-Crick complement' (without reversal) distance instead; that is a different table (Chee-Ling).
- Table is from 2010; novelty must be checked against later literature.
- Some large-n results in recent papers (n=48..160) are outside this table and not comparable.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/dna-codes-gc-rc-king-table.md
```

Already set up? Say `run V3R1T4S on dna-codes-gc-rc-king-table`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `dna-codes-gc-rc-king-table`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
