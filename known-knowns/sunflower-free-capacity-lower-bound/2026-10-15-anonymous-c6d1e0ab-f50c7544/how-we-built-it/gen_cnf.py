#!/usr/bin/env python3
"""DIMACS CNF: 'there is a 3-sunflower-free F in C([n],r) with |F| >= k'.

  gen_cnf.py n r k out.cnf [--sb none|adj|alltrans] [--card seqcounter|totalizer]

Variables 1..M are the r-subsets of [n] in colex order (the order is written as
comments 'c var {i} {elements}').  Clauses:
  (a) for every unordered sunflower triple {A,B,C}:  -A -B -C
  (b) cardinality sum x >= k (pysat CardEnc, auxiliary variables above M)
  (c) optional lex-leader symmetry breaking: for each point permutation sigma in the
      chosen set, x <=_lex x o sigma (variables compared in index order).  Sound because
      the lexicographically least member of the S_n-orbit of any solution satisfies
      every such constraint, and (a), (b) are S_n-invariant.
"""
import argparse
import itertools
import sys

from pysat.card import CardEnc, EncType


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("r", type=int)
    ap.add_argument("k", type=int)
    ap.add_argument("out")
    ap.add_argument("--sb", default="alltrans", choices=["none", "adj", "alltrans"])
    ap.add_argument("--card", default="seqcounter", choices=["seqcounter", "totalizer", "sortnetwrk", "kmtotalizer"])
    ap.add_argument("--deg", type=int, default=0,
                    help="add, for every point x, sum of members containing x <= DEG (valid when DEG >= g(n-1,r-1))")
    args = ap.parse_args()
    n, r, k = args.n, args.r, args.k
    subsets = sorted(itertools.combinations(range(n), r), key=lambda c: sum(1 << p for p in c))
    masks = [sum(1 << p for p in c) for c in subsets]
    var = {m: i + 1 for i, m in enumerate(masks)}
    M = len(masks)
    clauses = []
    ntrip = 0
    for t in range(r):
        s = r - t
        if 3 * s > n - t:
            continue
        for K in itertools.combinations(range(n), t):
            km = sum(1 << p for p in K)
            rest = [p for p in range(n) if not (km >> p) & 1]
            pets = [sum(1 << p for p in c) for c in itertools.combinations(rest, s)]
            L = len(pets)
            for i in range(L):
                a = pets[i]
                for j in range(i + 1, L):
                    b = pets[j]
                    if a & b:
                        continue
                    for l in range(j + 1, L):
                        c = pets[l]
                        if c & (a | b):
                            continue
                        clauses.append([-var[km | a], -var[km | b], -var[km | c]])
                        ntrip += 1
    top = M
    enc = {"seqcounter": EncType.seqcounter, "totalizer": EncType.totalizer,
           "sortnetwrk": EncType.sortnetwrk, "kmtotalizer": EncType.kmtotalizer}[args.card]
    card = CardEnc.atleast(lits=list(range(1, M + 1)), bound=k, top_id=top, encoding=enc)
    clauses.extend(card.clauses)
    top = max([top] + [abs(l) for c in card.clauses for l in c])
    if args.deg:
        for x in range(n):
            lits = [var[m] for m in masks if (m >> x) & 1]
            dc = CardEnc.atmost(lits=lits, bound=args.deg, top_id=top, encoding=enc)
            clauses.extend(dc.clauses)
            top = max([top] + [abs(l) for c in dc.clauses for l in c])
    perms = []
    if args.sb == "adj":
        perms = [(i, i + 1) for i in range(n - 1)]
    elif args.sb == "alltrans":
        perms = list(itertools.combinations(range(n), 2))
    nsb = 0
    for (a, b) in perms:
        def sw(m):
            ba, bb = (m >> a) & 1, (m >> b) & 1
            if ba != bb:
                m ^= (1 << a) | (1 << b)
            return m
        # x <=lex y with y_i = x_{sigma(i)}; only positions where sigma moves the variable matter
        pairs = []
        for m in masks:
            m2 = sw(m)
            if m2 != m:
                pairs.append((var[m], var[m2]))
        # chain: e_0 = true; e_{i-1} & x_i -> y_i ; e_{i-1} & (x_i == y_i) -> e_i
        prev = None
        for idx, (xi, yi) in enumerate(pairs):
            if prev is None:
                clauses.append([-xi, yi])
            else:
                clauses.append([-prev, -xi, yi])
            if idx == len(pairs) - 1:
                break
            top += 1
            e = top
            if prev is None:
                clauses.append([xi, yi, e])      # (x=0,y=0) -> e
                clauses.append([-xi, -yi, e])    # (x=1,y=1) -> e
            else:
                clauses.append([-prev, xi, yi, e])
                clauses.append([-prev, -xi, -yi, e])
            prev = e
            nsb += 1
    with open(args.out, "w") as fh:
        fh.write("c sunflower-free F in C([%d],%d), |F| >= %d; triples=%d; sb=%s; card=%s; deg<=%s\n"
                 % (n, r, k, ntrip, args.sb, args.card, args.deg or "none"))
        for i, c in enumerate(subsets):
            fh.write("c var %d %s\n" % (i + 1, " ".join(str(p + 1) for p in c)))
        fh.write("p cnf %d %d\n" % (top, len(clauses)))
        for c in clauses:
            fh.write(" ".join(map(str, c)) + " 0\n")
    print("vars=%d clauses=%d triples=%d sb_aux=%d" % (top, len(clauses), ntrip, nsb))


if __name__ == "__main__":
    main()
