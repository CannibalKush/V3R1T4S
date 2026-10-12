# Spec LCAP-1: capped, omega-free exhaustive search for Lehmer numbers N <= X

This spec is written so that anyone can reimplement the search from scratch and diff the canonical output
(per-depth node counts, a digest, the per-depth C2 counts and the event list) without reading our code.
Two independent implementations of it exist: a pure-Python reference (exact integers) and a C engine
(128-bit integers with exact 256-bit cross-products). They agree exactly at every cap tested.

## 0. What a run proves
With SIGMA = +1 and PMIN = 5, a run with cap X shows that **no C-sequence of primes 5 <= p_1 < ... < p_w (w >= 2)
satisfies P <= X and P - 2*Phi = 1**. Here P = prod p_i and Phi = prod (p_i - 1).
A certificate script (here `certify.py`) closes the other cases (3 | N, and k >= 3). Together these give: **no Lehmer
number N <= X**. The lemmas are Lemmas A and B of `../README.md`.

## 1. Notation
- For a prefix pi = (p_1, ..., p_j) (j >= 0): P = prod p_i, Phi = prod (p_i - 1), A = 2*Phi - P.
- Every node has A > 0, which is the invariant P < 2*Phi.
- p_last = p_j, or PMIN - 1 for the empty prefix.
- lo = max(p_last + 1, floor(2*Phi / A) + 1).
- pi_i(q) is the i-th prime strictly greater than q, over ALL primes (no admissibility filter).
- sigma = +1 for the Lehmer equation P - 2*Phi = 1. sigma = -1 gives the companion equation P - 2*Phi = -1, which
  is used only for regressions.

## 2. Nodes (the tree)
The root is the empty prefix. A prime q is a **child** of node pi (the prefix pi + (q) is a node) iff all of the
following hold:
- **(c1)** q >= lo.
- **(c2)** gcd(q - 1, P) = 1.
- **(c3)** P * q * pi_1(q) * pi_2(q) <= X.
- **(c4)** P q prod_{i<=m} pi_i(q) > (2 Phi (q-1) - [sigma = -1]) prod_{i<=m} (pi_i(q) - 1), where
  m = max{ m : P q prod_{i<=m} pi_i(q) <= X } (m >= 2 by (c3)).

Children are scanned in increasing q, starting at the first prime >= lo. The scan **stops** at the first prime q
(admissible or not) that fails (c3) or (c4). Both conditions are non-increasing in q.

The following two shortcuts are implied by (c3) and do not change the tree:
- If P*lo*(lo+2)*(lo+4) > X, the node has no children.
- If lo > isqrt(floor(X/P)), the node has neither children nor a C2 interval.

## 3. Two-prime closure C2 (done at every node, including the root)
Find all (q, r) with p_last < q < r, P q r <= X and P q r - 2 Phi (q-1)(r-1) = sigma. Define:
- u(q) = A q - 2 Phi
- n(q) = 2 Phi (q-1) - sigma

Then r = n(q) / u(q). The C2 interval is the set of integers q with:
- q >= lo;
- h(q) := A q^2 - 4 Phi q + 2 Phi + sigma < 0 (equivalent to r(q) > q over the reals);
- cap(q) := P * q * n(q) <= X * u(q) (equivalent to P q r(q) <= X over the reals).

For q >= lo the set {h < 0} is an interval [lo, qb]. P q r(q) is strictly decreasing on it (as a function of
u = A q - 2 Phi it is (2 Phi u + D + 4 Phi^2 + 2 Phi D / u) / A^2 with D = 4 Phi^2 - A(2 Phi + sigma) > 0, and
h < 0 <=> u^2 < D). So {cap} restricted to [lo, qb] is a final segment [qa, qb]. Either qa or qb may not exist,
in which case the interval is empty.

For every **prime** q in [qa, qb]:
- **admissible:** gcd(q - 1, P) = 1;
- **integral:** admissible and u(q) | n(q).

Every integral q is an **EVENT** (prefix, q, r = n/u). Its reason is the first of these that applies:
- `r<=q`;
- `cap` (P q r > X);
- `C-violation` (gcd(r - 1, P q) > 1);
- `r composite`;
- `SOLUTION`.

## 4. Canonical output (what to diff)
- `nodes_by_depth[j]`: the number of nodes with j primes.
- `digest` = sum over all nodes of H(P) mod 2^64, where
  - H(P) = splitmix64( (P mod 2^64) XOR splitmix64(floor(P / 2^64)) ), and
  - splitmix64(x): x += 0x9E3779B97F4A7C15; x = (x ^ (x>>30)) * 0xBF58476D1CE4E5B9; x = (x ^ (x>>27)) *
    0x94D049BB133111EB; return x ^ (x>>31), all mod 2^64.
  - P determines the prefix (unique factorisation), so the digest is an order-free fingerprint of the node set.
- `c2_primes_by_depth[j]`, `c2_adm`, `c2_int`: summed over nodes of depth j. These are the number of primes in the
  C2 interval, how many of them are admissible, and how many are integral.
- `events`: the full list. **Every solution would appear here as a `SOLUTION` event.**
- The per-task logs (`tasks_w*.jsonl`) give these quantities for each depth-D0 subtree, together with the subtree's
  prefix. `master.json` holds the nodes above depth D0. A spot check re-ran a random sample of subtrees with the
  pure-Python reference.

## 5. Why the tree is complete
Take any solution (p_1, ..., p_w) with w >= 2 and N = P_w <= X.
- **Every prefix of length j <= w-2 is a node.** Argue by induction on j. Each of (c1)-(c4) is a necessary
  condition for a prefix that is followed by at least 2 more primes of a solution:
  - (c1): every proper prefix has P < 2 Phi. If P >= 2 Phi then P - 2 Phi >= 1, since P is odd. Then
    P/Phi >= 2 + 1/Phi > 2 + 1/Phi_final, which contradicts monotone growth of the product.
  - (c2): C-sequence.
  - (c3): p_{j+1} >= pi_1(q) and p_{j+2} >= pi_2(q).
  - (c4): the remaining m' primes satisfy r_i >= pi_i(q), so m' <= m, and the final product
    2 + sigma/Phi_final is at most the bound. For sigma = -1, 2 - 1/Phi_final > 2 - 1/(Phi(q-1)).

  The scan stops correctly because of monotonicity: as q grows, pi_i(q) and q/(q-1) and m behave monotonically.
- **The pair (p_{w-1}, p_w) is examined by C2 at the length-(w-2) prefix, and it is integral.** It lies in the C2
  interval: q >= lo by (c1), r > q gives h < 0, and P q r <= X gives cap. So it is recorded as an event. It is a
  `SOLUTION` exactly when it is a genuine solution.

## 6. Arithmetic notes for reimplementers
- Never use floating point in a decision. Our C code uses doubles only to seed exact searches, and in a pre-filter
  that decides only when the estimate is at least 1e-9 (relative) away from X.
- Restricting q to q <= isqrt(floor(X/P)) in C2 is exact: cap together with r > q implies P q^2 < X.
- Primes >= 3 up to the sieve limit. Abort, never truncate, if a range runs past the sieve.
- The companion regression is SIGMA=-1, PMIN=3. It must find exactly 15, 255, 65535, 83623935, 4294967295 and
  6992962672132095 up to X = 1e17 or 1e20. It also finds spoof events with composite r, for example
  3*5*17*257*65537*(2^32+1).
