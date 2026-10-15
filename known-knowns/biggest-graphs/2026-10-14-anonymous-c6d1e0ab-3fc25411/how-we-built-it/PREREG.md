# Step 3 Run-Level Pre-Registration (`runs/2026-10-14-0615`)

## 1. Falsifiable Hypotheses
- **Hypothesis 1 (`symmetry-orbit-join`)**: Algebraic lift constructions (mixed-degree route-chart lifts over $\mathbb{F}_3^3$ / $\mathbb{F}_4^3$, Delorme polarity quotients over $\mathbb{F}_3^4$, or twin-packing extensions with inter-twin edges) can produce a simple graph $G$ on $N$ vertices with maximum degree $\le \Delta$ and all-pairs diameter $\le D$ strictly exceeding the live Comellas entry on at least one of `(12, 3)`, `(13, 3)`, `(14, 3)`, `(16, 3)`, `(11, 4)`, or `(12, 4)`.
- **Hypothesis 2 (`c-evaluator-optimizer`)**: Starting from live record graphs in `adjD2`, `adjD3`, and `adjD4` that possess unused degree slack (such as `(13, 3)` at $N=873$ with 117 free degree slots, `(14, 3)` at $N=1,116$, `(11, 4)` at $N=3,444$, `(15, 2)` at $N=190$, or `(11, 2)` at $N=106$), edge pruning + slack-vertex insertion + bit-parallel simulated annealing over 2-switches and single-edge rewires will close all distance-$ above  D$ pairs for $N_{\text{new}} \ge N_{\text{live}} + 1$.

## 2. Exact Verification Protocol
Every candidate graph $G$ must pass `verify_dd.py` (and compiled C checker `ddcheck`):
1. Parse 0-indexed edge list; verify 0 unparsable lines, 0 self-loops, 0 duplicate edges, and 0 isolated/unused vertex labels in $0 \dots N-1$.
2. Verify $\max_{v \in V} \deg(v) \le \Delta$.
3. Verify exact all-pairs shortest-path diameter $\le D$ via exhaustive bitset BFS from all $N$ vertices (`ordered_pairs_at_distance_gt_D == 0`).
4. Run negative control at $D - 1$ (`verify_dd.py` confirms `ordered_pairs_at_distance_gt_{D-1}  above  0`, proving true diameter is $D$ and the checker is not vacuously passing).
5. Verify $N \le M(\Delta, D)$ (Moore bound) and $N  above  \max(N_{\text{live}}(\Delta, D), N_{\text{trophy}}(\Delta, D))$.
6. Verify uncompressed edge-list artifact size $ under  1,000,000$ bytes.
null_test: not needed because degree-diameter-table is in category graphs-games-automata (exact deterministic graph degree and diameter verification)
