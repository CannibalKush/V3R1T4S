# How we found it: bigger constant-weight codes and five Delsarte bounds

**The brief.** An AI agent was pointed at A. E. Brouwer's table of bounds for binary constant-weight codes, with a
fresh copy of the table, all 713 explicit codes linked from it, the recent literature (Rosin, Lysenstøen, Echols,
Gippini, Gangl, Boisclair) and a checker, and asked to beat a printed lower bound with an explicit, checkable code.
Its assigned angle was, in short, an *exact large-neighbourhood search*: "remove r codewords, re-insert r+1 by an
exact MIS/clique solve over the words compatible with the kept code", seeded from the record codes.
Two days later three more agents were briefed to (a) re-verify and push those codes further, (b) try seed families
the first search never touched, and (c) look for exact upper-bound certificates.

**What worked.**
- *Plateau walks from the archive codes* (first agent, 2026-10-06, about 2 hours). The first design (random removal
  sets around a random codeword) was too slow and found nothing. The second one, `lb_lns.py`, lists once per round
  every outside word blocked by at most 3 codewords, builds removal sets from that blocker hypergraph, solves each
  re-insertion exactly, and when no move gains it applies a random batch of *equal-size* moves. Record codes looked
  exchange-dry at first, but after 0–6 plateau rounds the walks started to gain: 22 archive codes grew, the softest
  being Boisclair's (A(26,6,9) +213 at that point). A general-d version (`lb_lns_gen.py`) extended this to d = 8.
- *Graham–Sloane classes are not maximal* (same agent). Rebuilding the Bose S2-set construction for A(29,6,11) and
  A(29,6,12) reproduced the table's 41216 and 61820 exactly; an exhaustive scan found 4 and 3 words that can be added
  to one of the largest classes. These are the weakest claims here (the table itself says gs codes are not always
  maximal).
- *Faster engines, deeper neighbourhoods* (second agent, 2026-10-08, about 1.6 hours plus background walks).
  Profiling showed the time went into re-enumerating all C(n,w) words and into Python loops; four rewrites
  (incremental blocker counts, numba move phase, numba removal sets, table-driven ranks) made rounds 10–20 times
  faster, and larger neighbourhoods (≤ 4 blockers, removal sets up to 12) let 17 cells grow further. Independent
  restarts from the original archive seeds sometimes beat the warm-started walks (A(28,8,9): 1406 vs 1402).
- *Untouched seeds* (third agent, 2026-10-08). A one-round screen of the archive's A(n,8,7) codes, n = 46..63
  (mostly Boisclair's), showed n = 52..56 soft (improving moves in the first round) and n >= 58 rigid; 5-minute
  walks gave the five A(n,8,7) codes.
- *Delsarte LP certificates* (fourth agent, 2026-10-08, about 20 minutes for the certificates). For n > 28 the table
  prints the Johnson bound unless marked; the plain Delsarte LP, solved exactly over the rationals, is lower in five
  cells. The agent that prepared the data had already flagged these five cells with its own certificates; the
  published certificates are an independent exact recomputation. Routine bounds that nobody had printed, offered
  as table entries only.

**What failed.** Random-removal LNS (too slow, uninformative neighbourhoods); Graham–Sloane polishing for
A(29,6,13), A(29,6,14) and against the Jin–Xing cells (no free words); walks on group codes (no plateau moves at all);
crossing two walked codes by bipartite matching (gain 0); a fixed-size tabu search (diverges); second-moment and
local-cap LP constraints (slack at the Delsarte optimum); a three-point SDP (double-precision solvers returned values
below known lower bounds, so nothing from it is used). Several cells reached by the walks were later overtaken by
other contributors or are not claimed (see `README.md`).

**How long.** About 2 h of agent time on 2026-10-06 and about 2 h on 2026-10-08, plus background walks of a few
hours; the longest single code chain (A(26,6,13)) is about 2 h of wall clock on a shared 10-core machine. Every
command, seed and time is in `how-we-built-it/README.md`.

**Credits.** The seed codes are the work of J. Boisclair, D. Gangl, A. Gippini, C. Lysenstøen, W. Echols and the
contributors of Brouwer's archive; the table and archive are A. E. Brouwer's; the construction is Graham and Sloane's
(1980) with Bose's S2 sets; the LP bound is Delsarte's (1973). The searches, engines and certificates were written
and run by AI agents; independent reviewer agents re-checked every code with their own checkers, re-fetched the table
and searched the literature before release.
