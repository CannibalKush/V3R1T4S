#!/usr/bin/env python3
"""Independent recomputation of the sunflower clauses of a CNF from the literal definition.

Usage: triples_recheck.py file.cnf
Reads the 'c var i e1 e2 ...' map, enumerates ALL triples of distinct r-sets of [n] (brute
force, no core enumeration), keeps those with pairwise equal intersections (A&B == A&C == B&C,
empty allowed), and compares the resulting set of variable triples with the set of ternary
all-negative clauses over the original variables in the CNF.  Prints MATCH or MISMATCH.
This is a different enumeration from the generator's (which enumerates core + three disjoint
petals), so agreement shows the CNF forbids exactly the 3-sunflowers and nothing else among
the ternary clauses.  Standard library only; runs in well under a minute for M <= ~200 sets.
"""
import itertools
import sys


def main():
    path = sys.argv[1]
    names = {}
    clauses = []
    nvars = None
    with open(path) as fh:
        for line in fh:
            if line.startswith("c var "):
                p = line.split()
                names[int(p[2])] = frozenset(map(int, p[3:]))
            elif line.startswith("p cnf"):
                nvars = int(line.split()[2])
            elif line.startswith("c"):
                continue
            else:
                lits = list(map(int, line.split()))
                if lits and lits[-1] == 0:
                    lits.pop()
                clauses.append(lits)
    M = len(names)
    cnf_triples = set()
    for c in clauses:
        if len(c) == 3 and all(l < 0 and -l <= M for l in c):
            cnf_triples.add(frozenset(-l for l in c))
    mine = set()
    ids = sorted(names)
    for a, b, c in itertools.combinations(ids, 3):
        A, B, C = names[a], names[b], names[c]
        ab = A & B
        if ab == A & C and ab == B & C:
            mine.add(frozenset((a, b, c)))
    ok = mine == cnf_triples
    sizes = sorted({len(s) for s in names.values()})
    print("%s: M=%d sets of size %s; sunflower triples by brute force %d; ternary negative clauses in CNF %d; %s"
          % (path, M, sizes, len(mine), len(cnf_triples), "MATCH" if ok else "MISMATCH"))
    if not ok:
        print("only in brute force:", len(mine - cnf_triples), "only in CNF:", len(cnf_triples - mine))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
