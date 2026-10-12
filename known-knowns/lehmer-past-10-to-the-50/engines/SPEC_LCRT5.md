# Spec LCRT5 (revision 2): what changed relative to SPEC_LCRT_r1.md (revision 1)

Read `SPEC_LCRT_r1.md` (revision 1) and `SPEC_LCAP1.md` (10-06) first. The tree, the
CRT prune, the four modes LCRT-1..4, the canonical output and the certificate (`certify.py`) are **unchanged**. Revision 2
changes three things, and nothing else.

1. The prime source no longer has a hard ceiling. This is needed: the revision-1 engine aborted at 10^48.
2. There is a new optional mode, LCRT-5, which only changes how the m = 2 completions of some nodes are found.
3. There is a new optional mode, LCRT-6, which adds a trial-division prefilter in front of the Euler closure.

Engine: `lcrt5.c` (C + GMP). Usage: `lcrt5 X SIEVE D0 WORKERS OUTDIR [SIGMA] [PMIN] [CRT] [KMAX] [FILT] [CQMODE] [EULER] [C2CAND] [TDIV]`.
With `C2CAND` and `TDIV` omitted or 0 it is LCRT-4 exactly as in revision 1 (argument meanings unchanged).

## 1. Why the revision-1 engine could not reach 10^48
In revision 1 every prime came from one sieve stored as u32, so the limit L had to be below 2^32. The engine aborted
("never truncate") whenever a C2 range or a children scan needed a prime above L. The revision-1 job at X = 10^48
(L = 4*10^9) died with `FATAL: sieve too small for a C2 range`. The node responsible is

    prefix 5 7 13 17 19 23 37 59 67 163 173 199 6823 (depth 13), A = 2 Phi - P = 945,464,631,607,

a near miss with 2 Phi/A ~ 2.0*10^10. Its C2 interval is [qa, qb] = [20,021,216,264, 40,042,128,696], which holds
830,579,601 primes. Near misses like this have C2 intervals of about [2 Phi/A, 4 Phi/A], and they grow by about 100x
per two decades of X: the largest q is 3.1*10^8 at 10^46 and 4.0*10^10 at 10^48.

## 2. The exact segmented sieve (all modes)
- **Main sieve.** `PR[]` holds the primes from 3 up to L, with L < 2^32.
- **Primes above `PR[NPR-1]`.** These are produced segment by segment. A segment covers the odd numbers in [a, b] and is
  crossed off with the base primes p <= isqrt(b) taken from `PR`, starting at max(p^2, the first odd multiple of
  p >= a). If isqrt(b) > `PR[NPR-1]` the engine **aborts**. With L = 10^9 it can therefore produce every prime below
  10^18.
- **C2 at a node.** The primes of [qa, qb] that are <= `PR[NPR-1]` come from `PR`, exactly as in revision 1. The rest are
  streamed from consecutive segments. The per-prime work (admissibility, then integrality u | n) is unchanged.
- **Children scan.** In revision 1 the stop of the (c3)/(c4) scan was found by galloping plus bisection over `PR`
  indices. The engine still does that while it stays at least 80 primes below the end of `PR` (index
  `SAFE = NPR - 81`). If (c3) and (c4) still hold at `SAFE`, or if lo is already beyond `SAFE`, the scan continues as a
  **linear** scan over a prime stream with a lookahead of 128 primes. It stops at the first q that fails (c3) or (c4).
  That is the same stop as the galloping search, because the predicate is monotone in q (10-06 SPEC section 5). The
  m-loop of (c3)/(c4) reads the next primes after q from the lookahead buffer, and the engine aborts if more than 127
  would be needed.
- **Rule (c2): no prefix prime divides q - 1.** For q - 1 < 2^32 it is the revision-1 Lemire test. For q - 1 >= 2^32 it
  is the exact `%` test. The Lemire test is exact only for 32-bit numerators, and every prefix prime is < q.
- **Removed aborts.** "lo beyond sieve" no longer aborts. The only requirement is lo < 2^62, and lo < (2X)^(1/3)
  < 6*10^18 for X <= 10^56.
- **New diagnostics.** Each task line gains `seg_c2` and `seg_ch`, the numbers of primes the segmented path delivered
  to C2 ranges and to children scans. They depend on L by design and are **not canonical**. `merge_lcrt.py` (r2) sums
  them as `seg_c2_primes` and `seg_children_primes`.

**Claim (checked, section 5):** at any L that does not abort, every canonical field of every task line equals the
revision-1 output, `maxq` included.

## 3. Mode LCRT-5 (`C2CAND = c > 0`; FILT = 1 and CRT = 1 required)
Take a live large-regime node, that is K > KMAX candidates, with its C2 interval [qa, qb] computed exactly as before
(`maxq` is updated with qb as before). If

    K * c < qb - qa + 1        (exact integer comparison; K is the exact candidate count),

the m = 2 completions of the node are found by the **candidate closure** instead of the C2 prime loop. For each
candidate Q = Q1 + k*8*Phi (0 <= k < K) the closure computes

- Psi = (P*Q - sigma)/(2 Phi),
- W1 = Q - Psi + 1,
- Disc = W1^2 - 4Q.

If Disc > 0 is a perfect square with W1 - sqrt(Disc) even, then r1 = (W1 - sqrt Disc)/2 and r2 = (W1 + sqrt Disc)/2.
r1 must be >= lo, > p_last, prime, and admissible (no prefix prime divides r1 - 1). If it is, the pair is recorded as
an event with the same reason logic as C2 (`record_event`). The children (m >= 3) are handled exactly as in LCRT-4.

**Lemma (events identical to the C2 prime loop) [PROVED-HERE].**
- **A C2 event is a candidate.** Let (q, r) be a C2 event of the node: q prime in [qa, qb], admissible, u = Aq - 2 Phi
  divides n = 2 Phi (q - 1) - sigma, and r = n/u.
  - n is odd (sigma is odd), so r is odd, and so 4 | (q-1)(r-1).
  - The identity P q r - 2 Phi (q-1)(r-1) = sigma then gives Q = q r == sigma P^{-1} (mod 8 Phi).
  - h(q) < 0 is equivalent to r > q, so r >= q + 2 and Q >= lo(lo+2). The cap gives Q <= X/P.
  - So Q is one of the K candidates.
  - (q-1)(r-1) = Psi, so q and r are the roots of t^2 - W1 t + Q. Hence r1 = q (the smaller root), and the closure
    records the same (q, r).
- **A closure event is a C2 event.** Conversely, every event of the closure has r1 = q prime >= lo, admissible, with
  r2 > r1 and P r1 r2 <= X. The real function r(q) = n/u satisfies r(r1) = r2 > r1, which is equivalent to h(r1) < 0,
  and cap(r1) holds. So r1 lies in [qa, qb] and u | n.
- **Conclusion.** The two event sets are equal.

**Canonical output of LCRT-5** compared with LCRT-4 at the same X:
- `nodes`, `digest`, `live`, `digest_live`, `pruned`, `small`, `eclosed`, `epass`, `kfilt`, `c2i`, `maxq`, `events`
  are **identical**.
- `c2p`, `c2a`, `cand` and `sqhit` differ: the closure's candidates go to `cand` and its square hits to `sqhit`.
- The new per-depth counter `c2k` counts the nodes that used the closure.
- Events carry `"via": "c2" | "c2cand" | "small"` when C2CAND > 0.

## 3b. Mode LCRT-6 (`TDIV = B > 0`, argv[14]; used with EULER = 1)
In the Euler closure of a small-regime node (K <= KMAX), a candidate Q is first tested by trial division: if some odd
prime p < min(lo, B) divides Q, the candidate is **rejected** (counted in the new per-depth counter `tdrej`) and is
not Euler-tested. Otherwise the Euler test runs as in LCRT-4. The node is closed iff no candidate survives both tests.
If some candidate survives, the node takes the exact LCRT-4 fallback.

**Soundness [PROVED-HERE].** A genuine completion has Q = r_1 ... r_m with every prime r_i >= r_1 >= lo (rule (c1)).
So no prime p < lo divides it, and it is never rejected. It also passes the Euler test, so the node is never closed
wrongly.

**Canonical output.** Wherever the LCRT-4 run has `epass = 0` (true for every Lehmer run so far), the visited set and
every mode-independent counter equal LCRT-4. The reason is that a node LCRT-4 closes, LCRT-6 also closes. Only `tdrej`
is new. If a candidate with a small factor passed the Euler test, LCRT-4 would fall back and LCRT-6 would close the
node. In that case LCRT-6 visits a subset of the nodes, and its events would still be complete.

**Speed.** At 1e46 (B = 1000, C2CAND = 1024) it used 169.5 s of user CPU against 362.3 s for LCRT-4 on the same
machine, a factor of 2.1. A sample profile of LCRT-4 at 1e48 shows mpz_powm (the Euler test) at about 60% of the
samples. B = 1000 rejects about 84% of random odd candidates (the product over 3 <= p < 1000 of (1 - 1/p) is about
0.16).

## 4. Reference values (sigma = +1, PMIN = 5, D0 = 11, KMAX = 32, FILT = 1, EULER = 1; all with 0 events)
| X | mode | tasks | visited / digest | live / digest_live | Euler closures (passes) | C2 primes (int) | max q |
|---|---|---|---|---|---|---|---|
| 1e48 | LCRT-4 | 54,115 | 451,329,471 / 0b55adec1f853ea7 | 25,563,734 / 499f7d4846b16101 | 12,842,300 (0) | 4,009,531,122 (0) | 40,042,128,696 |
| 1e48 | LCRT-5, c = 1024 | 54,115 | identical | identical | identical | 1,175,781,160 (0); 31,930 nodes by candidates | identical |
| 1e50 | LCRT-4 | 65,647 | 2,169,013,803 / 74e2002af271a197 | 130,205,304 / 7c1d8e5190f9754f | 102,312,897 (0) | 26,727,509,182 (0) | 43,725,458,932 |
| 1e50 | LCRT-6 (c = 1024, B = 1000), L = 4,294,967,291 | 65,647 | identical | identical | identical | 7,238,774,634 (0); 191,717 nodes by candidates | identical |

1e50 LCRT-4:
- live_by_depth = [1, 3, 7, 17, 29, 57, 129, 341, 986, 3005, 11736, 65647, 662953, 31403462, 97992813, 64118, 0]
- nodes_by_depth = [1, 3, 7, 17, 29, 57, 129, 341, 986, 3005, 11736, 65647, 662953, 80450857, 2061050747, 26767283, 5]
- kfilt 25,849,618,340
- segmented primes: 5,462,744,549 in C2 ranges and 128,247,667 in children scans (main sieve L = 10^9)

1e48 LCRT-4 by depth:
- live_by_depth = [1, 3, 7, 17, 28, 49, 116, 298, 834, 2566, 9845, 54115, 555162, 20402898, 4537586, 209]
- nodes_by_depth = [1, 3, 7, 17, 28, 49, 116, 298, 834, 2566, 9845, 54115, 555162, 66864447, 383740035, 101948]
- kfilt total 3,535,452,488
- C2 primes from the segmented sieve: 1,221,455,326 (main sieve L = 10^9)

## 5. Checks done for revision 2 (working notes and regression data are not shipped; the 1e50 runs are)
- **Tiny main sieve against the revision-1 logs.** Every task line was identical to the revision-1 logs on every common
  field: 1e42 with L = 2e5, 1e44 with L = 1e6 and 1e46 with L = 3e6. An independent reviewer had diffed those
  revision-1 logs against a separately written engine. At 1e46, 55,132,065 C2 primes and 98,840,576 children-scan primes came from the
  segmented path.
- **Independent algebraic closure of every C2 range the engine streamed beyond the main sieve at 1e48** (8 ranges,
  `xcheck_segc2.py`). This check uses no prime enumeration.
  - Since A n = 2 Phi u + D with D = 4 Phi^2 - 2 Phi A - A sigma, u | n implies u | D.
  - D (45-46 digits) was factored completely, and every factor was proven prime.
  - No divisor of D lies in [A qa - 2 Phi, A qb - 2 Phi] with d == -2 Phi (mod A), so there are 0 integral completions
    in every range.
  - [qa, qb] was recomputed from the definitions and matches.
  - The engine's segmented prime counts equal sympy.primepi differences for all 8 ranges, for example 830,579,601 primes
    in [20,021,216,264, 40,042,128,696].
- **LCRT-5 against LCRT-4.** The mode-independent fields are identical at 1e42 and 1e44 (against the revision-1 logs) and
  at 1e48 (against the revision-2 LCRT-4 run).
- **1e50 cross-run.** The 1e50 run in LCRT-6 with main sieve L = 4,294,967,291 is identical to the LCRT-4 1e50 run
  (L = 10^9) on every mode-independent field of all 65,647 task lines. The LCRT-6 run took **no** primes from the
  segmented path. The LCRT-4 run took 5.46e9 C2 primes and 1.28e8 children-scan primes from it, so the stream is
  cross-checked in (10^9, 4.29*10^9]. The 60 beyond-sieve C2 ranges of the LCRT-4 1e50 run were closed algebraically,
  and their prime counts equal sympy.primepi (all OK).
- **Positive controls.**
  - The companion run (sigma = -1, pmin 3, 1e20) finds all six known solutions and both spoofs, with L = 3e4, both
    modes, KMAX = 0 or 32.
  - Planted C-sequences were found 30/30 at each of 1e24, 1e30 and 1e36. With L = 2e4 some go through the segmented
    path.
  - With KMAX = 0 and C2CAND = 1, 30/30 were found at 1e24 and 30/30 at 1e30. Of these, 51 came **through the
    candidate closure** ("via": "c2cand").

## 6. Shortest path for an independent reimplementation
With LCRT-5 (and optionally LCRT-6) and a u32 main sieve near 2^32, the 1e48 and 1e50 runs need no segmented primes
at all (`seg_c2 = seg_ch = 0`). An engine that already implements LCRT-4 (for example `vlrt.c`, the independent
revision-1 engine that `vlrt2.c` extends) therefore only needs:
- the candidate rule of section 3;
- optionally the trial-division rule of section 3b.

It can then diff the mode-independent fields against the shipped 1e50 logs
(`../branch_logs/lcrt5_1e50_LCRT4_tasks.tar.gz`, LCRT-4; `../branch_logs/lcrt6_1e50_bigsieve_LCRT6_tasks.tar.gz`,
LCRT-6). To check the segmented path itself, diff an LCRT-4 run with a small main sieve against one with a large main
sieve at 1e42-1e46 (section 5).
