#!/usr/bin/env python3
"""apply_diff.py NEAR_MISS DIFF GRAPH -- apply the 5-edge switch in DIFF to the near-miss edge list and check that the
resulting edge SET equals the edge set of GRAPH (the shipped G_13_4_n6630.edges).  python3 only.
The byte order of the shipped file comes from the annealing program and is not reproduced; the edge set is."""
import sys

def edges(path):
    s = set()
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        u, v = map(int, line.split()[:2])
        s.add((min(u, v), max(u, v)))
    return s

near, diff, graph = sys.argv[1:4]
E = edges(near)
rem, add = set(), set()
for line in open(diff):
    if line[:2] in ("- ", "+ "):
        u, v = map(int, line[2:].split())
        (rem if line[0] == "-" else add).add((min(u, v), max(u, v)))
assert rem <= E, "an edge to remove is not in the near-miss graph"
assert not (add & E), "an edge to add is already present"
R = (E - rem) | add
G = edges(graph)
print(f"near-miss edges {len(E)}, removed {len(rem)}, added {len(add)}, result {len(R)}, shipped graph {len(G)}")
print("EDGE SETS IDENTICAL" if R == G else "EDGE SETS DIFFER")
sys.exit(0 if R == G else 1)
