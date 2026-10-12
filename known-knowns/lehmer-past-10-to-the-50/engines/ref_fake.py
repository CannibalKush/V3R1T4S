#!/usr/bin/env python3
"""Plain reference search for the planted ("fake prime") variant used to test lbb.c's completeness.

Fake problem: increasing sequences x1 < ... < xr (r >= 2) of ODD integers >= 5 (primality NOT required),
pairwise 'admissible' (x_j mod x_i != 1 for i < j), with  prod x - 1 = 2 * prod (x - 1)  and prod x <= X.
This has solutions (unlike the real problem), so it tests the tree logic (m=1 formula, branching,
feasibility bound, cube fast path, 8F-congruence closure) for completeness.
Reference = exhaustive DFS with only the most basic, obviously valid pruning:
  * continue only while P < 2F (ratio only grows);   * x*(x+2) <= X/P for a non-final element;
  * crude ratio bound (x/(x-1))^M > 2F/P with x^M <= X/P (monotone in x) -> stop.
No lower bound on x other than x > previous, no congruence closure.
"""
import sys

def run(X, pmin=5, R=1):
    sols = []
    nodes = 0
    def adm(x, pre):
        return all(x % p != 1 for p in pre)
    def dfs(pre, P, F):
        nonlocal nodes
        nodes += 1
        a = 2 * F; g = a - P
        assert g > 0
        Qmax = X // P
        plast = pre[-1] if pre else pmin - 2
        if pre and (a - R) % g == 0:
            x = (a - R) // g
            if x > plast and x <= Qmax and x % 2 == 1 and adm(x, pre):
                sols.append(tuple(pre + [x]))
        x = plast + 2
        while x * (x + 2) <= Qmax:
            if adm(x, pre):
                P2, F2 = P * x, F * (x - 1)
                M = 0; t = 1
                while t * x <= Qmax:
                    t *= x; M += 1
                if x ** M * P <= (x - 1) ** M * a:
                    break
                if P2 < 2 * F2:
                    dfs(pre + [x], P2, F2)
            x += 2
    dfs([], 1, 1)
    return sorted(sols), nodes

if __name__ == "__main__":
    E = int(sys.argv[1]); pmin = int(sys.argv[2]) if len(sys.argv) > 2 else 5; R = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    sols, nodes = run(10 ** E, pmin, R)
    for s in sols:
        P = 1; F = 1
        for x in s: P *= x; F *= x - 1
        assert P - R == 2 * F
        print("SOL", P, " ".join(map(str, s)))
    print("REF nodes", nodes, "solutions", len(sols))
