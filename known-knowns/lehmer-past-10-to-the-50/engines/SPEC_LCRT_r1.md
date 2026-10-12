# Spec LCRT: LCAP-1 plus the cofactor CRT prune (C engine `lcrt.c`, the predecessor of `lcrt5.c`)

This page plus `SPEC_LCAP1.md` (shipped in this directory,
sections 1-3) is enough to reimplement the search and diff the canonical output, without reading the engine's code.
The same lemma was found independently, and first, by a separate formalization effort on the same problem
("Lemma CQ"). Its Euler-test closure is reused in mode LCRT-4.

## 0. What a run proves
With SIGMA = +1, PMIN = 5 and cap X: no C-sequence of primes 5 <= p_1 < ... < p_w (w >= 2) with P <= X satisfies
P - 2*Phi = 1. With `certify.py` (3 | N impossible, k >= 3 impossible, both for X <= 10^56), this means:
**no Lehmer number N <= X**.

## 1. Lemma CRT (cofactor congruence) [PROVED-HERE]
Let pi = (p_1 < ... < p_j) be a C-sequence of odd primes, P = prod p_i, Phi = prod (p_i - 1). Suppose
N = P * r_1 * ... * r_m with distinct odd primes r_i > p_j, m >= 2, and N - sigma = 2 phi(N) (sigma odd). Put
Q = prod r_i. Then

    Q == sigma * P^{-1}  (mod 8*Phi).

Proof. N is squarefree, so phi(N) = Phi * prod (r_i - 1) and N - sigma = 2*Phi*prod(r_i - 1). Each r_i - 1 is even and
m >= 2, so 4 | prod(r_i - 1) and N == sigma (mod 8*Phi). gcd(P, 8*Phi) = 1: P is odd, and no p_i divides any p_k - 1
(C-sequence; p_i does not divide p_i - 1). So P is a unit mod 8*Phi and P*Q = N == sigma gives the claim. []

For the same completion (LCAP-1 notation lo = max(p_j + 1, floor(2*Phi/A) + 1), A = 2*Phi - P > 0):
* Q <= floor(X/P) when N <= X;
* Q >= lo*(lo+2): r_1 >= lo by LCAP-1 rule (c1) (pi + (r_1) is a proper prefix, so its P < 2*Phi), and r_2 >= r_1 + 2.

The candidate set of a node is the arithmetic progression C(pi) = { Q == sigma*P^{-1} (mod 8 Phi) : lo(lo+2) <= Q <= X/P },
written Q1 + k*8*Phi, 0 <= k < K. A node is LIVE iff it passes LCAP-1's shortcut (lo <= isqrt(floor(X/P))) and K >= 1.

The lemma also holds for integral LCAP-1 C2 "events" with N <= X whose r is composite (the identity
P q r - 2 Phi (q-1)(r-1) = sigma only needs r odd), so a prune by Lemma CRT never removes any LCAP-1 event with N <= X.

## 2. Modes (all exact; integers via GMP; doubles only as filters with a 1e-9 relative margin, exact fallback)
* **LCAP-1** (`CRT=0`): the 10-06 tree, reproduced exactly (canonical output identical to the 10-06 logs).
* **LCRT-1** (`CRT=1 KMAX=0 FILT=0`): LCAP-1, except that a visited node that is not LIVE is PRUNED (no C2, no children).
* **LCRT-2** (`KMAX=32 FILT=0`): a LIVE node with K <= KMAX is closed by the candidate closure:
  - m = 2: for each candidate Q, Psi = (P*Q - sigma)/(2*Phi) must equal (r1-1)(r2-1) with r1*r2 = Q, so
    r1 + r2 = Q - Psi + 1 and (Q - Psi + 1)^2 - 4Q must be a positive perfect square (exact);
  - m >= 3: only the LCAP-1 children q that divide some candidate are visited (necessary, by Lemma CRT at the child
    q: its candidate times q is a candidate of the parent).
* **LCRT-3** (`KMAX=32 FILT=1`): additionally, at EVERY live node a child q is visited only if q divides some
  Q1 + k*8*Phi with k < K, i.e. k0 = (-Q1) * (8*Phi)^{-1} mod q < K (always true when K >= q). q is coprime to 8*Phi.
* **LCRT-4** (`KMAX=32 FILT=1 EULER=1`, production): a small-regime node (K <= 32) first tests every candidate
  N = P*Q with 2^((N - sigma)/2) mod N. A genuine completion has N - sigma = 2*phi(N), so 2^((N - sigma)/2) == 1 (mod N)
  (Euler; N odd). If every candidate fails, the node is closed for every m >= 2. If any candidate passes, the node falls
  back to the exact LCRT-3 treatment (perfect-square m=2 closure + filtered children). (Euler closure: credit
  to that separate formalization effort, its mode LCAP-CQ2.)
* children scan: LCAP-1 rules (c1)-(c4); the scan stop (first q failing (c3) or (c4)) is located by an exact
  galloping + bisection search, which equals the linear scan's stop because (c3), (c4) are monotone in q
  (SPEC_LCAP1 section 5, independently re-derived on 10-06).

## 3. Completeness [PROVED-HERE, given LCAP-1 completeness (SPEC_LCAP1 section 5, independently re-derived on 10-06)]
Let N <= X be a solution, prefixes pi_0 (root), pi_1, ..., pi_{w-2}. LCAP-1: each pi_j (j <= w-2) is an LCAP-1 node
and the last pair is found by C2 at pi_{w-2}. Each pi_j has m = w - j >= 2 remaining primes, so by Lemma CRT its
remaining product Q is in C(pi_j): every pi_j is LIVE. Hence:
* LCRT-1 visits every pi_j (a node is pruned only when not live) and runs C2 at pi_{w-2}.
* LCRT-2/3: at a large-regime live node the child pi_{j+1} passes the AP filter (its q = p_{j+1} divides the
  candidate Q of pi_j); at a small-regime live node the m = 2 completion is found by the perfect-square test and the
  m >= 3 completions through the child dividing the candidate.
* LCRT-4: at a small-regime node the genuine candidate N passes the Euler test, so the node takes the exact fallback.
So every solution is reported as a SOLUTION event. All four modes visit every LIVE node whose ancestors were not
closed by an earlier rule; LCRT-1, -2, -3 have the SAME live set (a child that fails the filter is provably not live),
which is the canonical object to diff (section 4). LCRT-4 visits a subset of it.

## 4. Canonical output (per task line and merged summary; `merge_lcrt.py`)
* `live_by_depth`, `digest_live` = sum of H(P) mod 2^64 over LIVE nodes (H as in LCAP-1 section 4) -- identical for
  LCRT-1, LCRT-2, LCRT-3 at the same X (diff this);
* `events` (N <= X) -- identical for LCAP-1, LCRT-1..3 (Lehmer: none);
* diagnostics (mode dependent): `nodes` (visited) and `digest` (over visited), `pruned`, C2 counts, `small`, `cand`,
  `sqhit`, `kfilt`, `eclosed`, `epass`, `crt_tests`, `maxq`;
* the summary binds `X`, `sigma`, `pmin`, `crt`, `kmax`, `filt`, `euler`; `certify.py` requires X = 10^E, sigma = 1,
  pmin = 5, crt = 1, complete = true (DONE marker, every task present, no conflicting duplicate lines), no SOLUTION.

## 5. Reference values (sigma = +1, pmin = 5; all with 0 events)
| X | LCAP-1 nodes | LCRT-1 visited | live | digest_live | LCRT-3 visited | LCRT-4 visited |
|---|---|---|---|---|---|---|
| 1e30 | 4,462,332 | 6,199 | 1,374 | b270d41143bd0193 | 1,893 | 1,678 |
| 1e36 | 6,365,120,065 (10-06) | 204,383 | 17,005 | 294856e93f2736bc | 112,343 | 112,079 |
| 1e38 | -- | 3,124,158 | 60,285 | b30ab4f38bbf9cd6 | 219,426 | 216,605 |
| 1e40 | -- | 15,770,261 | 260,810 | c387f554f2a7bcb1 | 561,379 | 508,697 |
| 1e42 | -- | (aborts: lo beyond sieve) | 409,579 | 6bef94e18e5176c3 | 6,543,475 | 6,536,690 (live 409,572) |
| 1e44 | -- | -- | 2,658,749 | 7b797b512220b9e2 | 18,264,911 | 18,017,886 (live 2,658,392, baa654254c6457e9) |
| 1e46 | -- | -- | -- | -- | -- | 54,945,185 (live 10,865,780, c59aa49428d3c222) |
LCRT-4 live counts are a subset of the LCRT-1..3 live set (Euler-closed nodes are not expanded).
LCRT-1 visited digests: 1e30 5ceeaf3d2aa17cec, 1e36 6d1b0f3b902e4dff, 1e38 bf59e8011099ef52, 1e40 62abb7337c834c22
(= a pure-Python prototype at every cap 1e16..1e40).

## 6. Arithmetic and limits
* GMP throughout, so there is no word-size limit on X. Primes come from a sieve (u32 storage, limit < 2^32); the
  program aborts (never truncates) when a needed prime is beyond the sieve.
* The analytic closures in `certify.py` hold for X <= 10^56 (B: N/phi(N) <= 2.9932 < 3 at 10^56, 3.0134 at 10^58).
