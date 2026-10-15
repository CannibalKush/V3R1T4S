"""Usage: subset_check.py plain.cnf proved.cnf
Checks that every clause of plain.cnf (as a set of literals) occurs in proved.cnf, that both have the same 'c var' map,
and reports how many extra clauses proved.cnf has (the symmetry-breaking constraints). Prints SUBSET OK or SUBSET FAIL."""
import sys


def load(p):
    cl, varmap = set(), []
    for line in open(p):
        if line.startswith("c var "):
            varmap.append(line.strip())
        if line[0] in "cp":
            continue
        t = tuple(sorted(int(x) for x in line.split()[:-1]))
        if t:
            cl.add(t)
    return cl, varmap


a, va = load(sys.argv[1])
b, vb = load(sys.argv[2])
ok = a <= b and va == vb and len(va) > 0
print(f"plain clauses {len(a)}, proved clauses {len(b)}, extra in proved {len(b - a)}, var maps equal {va == vb}")
print("SUBSET OK" if ok else "SUBSET FAIL")
sys.exit(0 if ok else 1)
