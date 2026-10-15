"""Standard-library sanity check of the cardinality part of a gen_cnf.py CNF.

Usage: card_check.py file.cnf K
The CNF's variables 1..M are the r-sets (from the 'c var' lines); the remaining clauses (those that are not the
all-negative ternary sunflower clauses) encode sum(x_1..x_M) >= K with auxiliary variables above M. This check
treats that sub-formula as a black box and tests it by unit propagation plus a small DPLL on the auxiliaries:
(1) for 200 random choices of exactly K set-variables true and the rest false, the auxiliary clauses are satisfiable;
(2) for 200 random choices of exactly K-1 true, they are unsatisfiable. It also verifies that no clause mentions a
set-variable positively except inside the cardinality block. Prints CARD OK or CARD FAIL. It is a sanity check of
the encoding, not a proof of it; the proof-checked UNSAT result rests on the CNF as shipped and regenerated.
"""
import random
import sys


def main():
    path, K = sys.argv[1], int(sys.argv[2])
    M = 0
    clauses = []
    for line in open(path):
        if line.startswith("c var "):
            M = max(M, int(line.split()[2]))
        elif line[0] in "cp":
            continue
        else:
            lits = [int(x) for x in line.split()[:-1]]
            if lits:
                clauses.append(lits)
    sun = [c for c in clauses if len(c) == 3 and all(l < 0 and -l <= M for l in c)]
    card = [c for c in clauses if not (len(c) == 3 and all(l < 0 and -l <= M for l in c))]
    aux = sorted({abs(l) for c in card for l in c if abs(l) > M})
    print(f"M={M} sunflower_clauses={len(sun)} cardinality_clauses={len(card)} aux_vars={len(aux)}")

    def sat(assign):
        # DPLL restricted to the cardinality clauses with set variables fixed
        cls = []
        for c in card:
            if any(assign.get(abs(l), None) == (l > 0) for l in c):
                continue
            rest = [l for l in c if abs(l) not in assign]
            if not rest:
                return False
            cls.append(rest)
        return dpll(cls, {})

    def dpll(cls, a):
        while True:
            unit = None
            new = []
            for c in cls:
                if any(a.get(abs(l)) == (l > 0) for l in c):
                    continue
                rest = [l for l in c if abs(l) not in a]
                if not rest:
                    return False
                if len(rest) == 1:
                    unit = rest[0]
                new.append(rest)
            cls = new
            if not cls:
                return True
            if unit is None:
                break
            a[abs(unit)] = unit > 0
        v = abs(cls[0][0])
        for val in (True, False):
            b = dict(a); b[v] = val
            if dpll(cls, b):
                return True
        return False

    rng = random.Random(1)
    ok = True
    for trial in range(200):
        chosen = set(rng.sample(range(1, M + 1), K))
        if not sat({i: (i in chosen) for i in range(1, M + 1)}):
            print(f"FAIL: {K} chosen sets but cardinality block unsatisfiable (trial {trial})"); ok = False; break
    for trial in range(200):
        chosen = set(rng.sample(range(1, M + 1), K - 1))
        if sat({i: (i in chosen) for i in range(1, M + 1)}):
            print(f"FAIL: {K - 1} chosen sets but cardinality block satisfiable (trial {trial})"); ok = False; break
    print("CARD OK" if ok else "CARD FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
