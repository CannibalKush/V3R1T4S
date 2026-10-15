#!/usr/bin/env python3
"""Check the link-lemma chain rows of the exact-values candidate (standard library only).

For each chain_rows/{dir}/derivation.json: the claimed value v must equal
floor(n * g(n-1, r-1) / r) where g(n-1, r-1) is itself a value established in this
candidate (by a checked UNSAT proof in opus_packages/, or by an earlier chain row), and
family.json must contain exactly v distinct r-subsets of [n].  Sunflower-freeness of the
family is checked separately by check_family.py and sfcheck.
Exit 0 iff every chain row checks.  Usage: chain_check.py [candidate_root]
"""
import json
import os
import sys


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proved = {}
    pk = os.path.join(root, "opus_packages")
    for d in sorted(os.listdir(pk)):
        mp = os.path.join(pk, d, "manifest.json")
        if not os.path.exists(mp):
            continue
        m = json.load(open(mp))
        ok = any(isinstance(v, dict) and v.get("drat_trim_verified") and v.get("drup_check_verified")
                 for k, v in m.items() if k not in ("n", "r", "value", "claim"))
        if ok:
            proved[(m["n"], m["r"])] = m["value"]
    print("values with checked UNSAT proofs:", sorted(proved.items()))
    allok = True
    cr = os.path.join(root, "chain_rows")
    pending = sorted(os.listdir(cr))
    progress = True
    done = []
    while pending and progress:
        progress = False
        for d in list(pending):
            der = json.load(open(os.path.join(cr, d, "derivation.json")))
            n, r, v = der["n"], der["r"], der["value"]
            if (n - 1, r - 1) not in proved:
                continue
            g1 = proved[(n - 1, r - 1)]
            bound = (n * g1) // r
            fam = json.load(open(os.path.join(cr, d, "family.json")))
            sets = [frozenset(s) for s in fam["sets"]]
            fam_ok = (fam["n"] == n and fam["r"] == r and len(sets) == v and len(set(sets)) == v
                      and all(len(s) == r and all(isinstance(x, int) and 1 <= x <= n for x in s) for s in sets))
            ok = fam_ok and bound == v and der["upper_bound"]["bound"] == bound
            print("%s: floor(%d*g(%d,%d)/%d) = floor(%d*%d/%d) = %d, family size %d, distinct r-sets in range: %s -> %s"
                  % (d, n, n - 1, r - 1, r, n, g1, r, bound, len(sets), fam_ok, "PASS" if ok else "FAIL"))
            allok &= ok
            if ok:
                proved[(n, r)] = v
            pending.remove(d)
            done.append(d)
            progress = True
    for d in pending:
        print("%s: FAIL (predecessor value not established)" % d)
        allok = False
    print("CHAIN CHECK", "PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
