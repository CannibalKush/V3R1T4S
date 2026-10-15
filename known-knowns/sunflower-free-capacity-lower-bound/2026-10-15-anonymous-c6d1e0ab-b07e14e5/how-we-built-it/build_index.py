#!/usr/bin/env python3
"""Build index.json and INDEX.md for the exact-values candidate from the artifacts on disk
(standard library only).  Usage: build_index.py [candidate_root] [--check]

Each opus_packages/g_{n}_{r}_{v}/ row: family.json (size v), one or more proof variants
{variant}.cnf + {variant}.drup with drat-trim and drup_check outputs; the CNF header line
states the symmetry breaking (sb=none|alltrans) and the degree cut (deg<=D or none).
Each chain_rows/g_{n}_{r}_{v}/ row: family.json plus derivation.json (link lemma, core size 1).

Proof basis of a row (strongest available):
  plain      : a variant with sb=none whose degree cut (if any) is justified by plain rows / base values
  lex-leader : a variant with lex-leader symmetry breaking (soundness: SOUNDNESS.md section 3)
  chain      : floor(n g(n-1,r-1)/r) with the predecessor established, plus a family of that size
A degree cut deg(x) <= D is valid iff D >= g(n-1,r-1); g(m,1)=2 (m>=2) and g(m,2)=6 (m>=6) are the
base values (SOUNDNESS.md section 4), other predecessors must be rows of this candidate.
--check exits 1 if any referenced file is missing, any verifier output lacks 's VERIFIED', a
family size disagrees with the claimed value, or a degree cut is not justified.
"""
import json
import os
import re
import sys

BASE = {1: 2, 2: 6}  # g(m,1)=2 for m>=2, g(m,2)=6 for m>=6


def base_value(m, r):
    if r == 1 and m >= 2:
        return 2
    if r == 2 and m >= 6:
        return 6
    return None


def parse_header(cnf):
    with open(cnf) as fh:
        line = fh.readline().strip()
    m = re.search(r"C\(\[(\d+)\],(\d+)\), \|F\| >= (\d+); triples=(\d+); sb=(\w+)", line)
    n, r, k, trip, sb = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5)
    dm = re.search(r"deg<=(\d+)", line)
    deg = int(dm.group(1)) if dm else None
    return {"n": n, "r": r, "k": k, "triples": trip, "sb": sb, "deg": deg, "header": line}


def verified(path):
    if not os.path.exists(path):
        return None
    txt = open(path, errors="replace").read().replace("\r", "\n")
    return "s VERIFIED" in txt


def family_size(path, n, r):
    d = json.load(open(path))
    sets = [frozenset(s) for s in d["sets"]]
    ok = d["n"] == n and d["r"] == r and len(set(sets)) == len(sets) and \
        all(len(s) == r and all(isinstance(x, int) and 1 <= x <= n for x in s) for s in sets)
    return len(sets), ok


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    root = args[0] if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    problems = []
    rows = []
    pk = os.path.join(root, "opus_packages")
    for d in sorted(os.listdir(pk)):
        mp = os.path.join(pk, d, "manifest.json")
        cdir = os.path.join(pk, d, "cases")
        if not os.path.exists(mp) and os.path.isdir(cdir) and os.path.exists(os.path.join(pk, d, "ARGUMENT.md")):
            rows.append(casesplit_row(pk, d, problems))
            continue
        if not os.path.exists(mp):
            continue
        m = json.load(open(mp))
        n, r, v = m["n"], m["r"], m["value"]
        row = {"n": n, "r": r, "value": v, "dir": "opus_packages/" + d, "kind": "sat", "variants": []}
        fs, ok = family_size(os.path.join(pk, d, "family.json"), n, r)
        row["family_size"] = fs
        if not ok or fs != v:
            problems.append("%s: family.json invalid or size %d != %d" % (d, fs, v))
        for f in sorted(os.listdir(os.path.join(pk, d))):
            if f.endswith(".cnf") and not f.endswith(".regen.cnf"):
                var = f[:-4]
                h = parse_header(os.path.join(pk, d, f))
                if (h["n"], h["r"], h["k"]) != (n, r, v + 1):
                    problems.append("%s/%s: header (%d,%d,%d) does not match claim" % (d, f, h["n"], h["r"], h["k"]))
                drup = os.path.join(pk, d, var + ".drup")
                ent = {"variant": var, "cnf": f, "proof": var + ".drup", "sb": h["sb"], "deg": h["deg"],
                       "triples": h["triples"], "proof_bytes": os.path.getsize(drup) if os.path.exists(drup) else None,
                       "drat_trim_verified": verified(os.path.join(pk, d, var + "_drat_trim.txt")),
                       "drup_check_verified": verified(os.path.join(pk, d, var + "_drup_check.txt"))}
                if ent["proof_bytes"] is None:
                    problems.append("%s/%s: proof missing" % (d, var))
                if not (ent["drat_trim_verified"] and ent["drup_check_verified"]):
                    problems.append("%s/%s: verifier output missing or not VERIFIED" % (d, var))
                row["variants"].append(ent)
        if not row["variants"]:
            problems.append("%s: no proof variant" % d)
        for f in ("regenerate.sh", "family_check.txt", "family_sfcheck.txt"):
            if not os.path.exists(os.path.join(pk, d, f)):
                problems.append("%s: %s missing" % (d, f))
        # fable-sun's independent re-check directory, if present
        fd = os.path.join(root, "g_%d_%d" % (n, r))
        if os.path.isdir(fd):
            row["fable_recheck_dir"] = "g_%d_%d" % (n, r)
            row["fable_drat_trim_verified"] = verified(os.path.join(fd, "drat_trim_output.txt"))
        rows.append(row)
    cr = os.path.join(root, "chain_rows")
    for d in sorted(os.listdir(cr)):
        der = json.load(open(os.path.join(cr, d, "derivation.json")))
        n, r, v = der["n"], der["r"], der["value"]
        fs, ok = family_size(os.path.join(cr, d, "family.json"), n, r)
        if not ok or fs != v:
            problems.append("%s: family.json invalid or size %d != %d" % (d, fs, v))
        rows.append({"n": n, "r": r, "value": v, "dir": "chain_rows/" + d, "kind": "chain", "family_size": fs,
                     "derivation": der["upper_bound"]})
    # fable's verification_summary (independent triple-clause recomputation)
    vs = os.path.join(root, "verification_summary.json")
    tm = {}
    if os.path.exists(vs):
        for e in json.load(open(vs)):
            tm[(e["n"], e["r"])] = e.get("triples_match")
    # establish values: iterate until stable
    est = {}
    ub = {}
    basis = {}
    changed = True
    while changed:
        changed = False
        for row in rows:
            key = (row["n"], row["r"])
            if key in est:
                continue
            n, r, v = row["n"], row["r"], row["value"]
            pred = base_value(n - 1, r - 1)
            if pred is None:
                pred = est.get((n - 1, r - 1))
            if pred is None and (n - 1, r - 1) in est:
                pred = None
            if row["kind"] == "casesplit":
                if not any(pr.startswith(row["dir"].split("/")[-1]) for pr in problems):
                    if row.get("upper_bound_only"):
                        ub[key] = v
                        basis[key] = ("case-split upper bound", "g(%d,%d) <= %d: %d cases at |F|>=%d, see ARGUMENT.md (not an exact value)" % (n, r, v, row["n_cases_at_v_plus_1"], v + 1))
                        est[key] = None  # mark handled
                    else:
                        est[key] = v
                        basis[key] = ("case-split", "%d cases at |F|>=%d, see ARGUMENT.md (completeness of the case list is argued there, not machine-checked by this index)" % (row["n_cases_at_v_plus_1"], v + 1))
                    changed = True
                continue
            if row["kind"] == "chain":
                if pred is not None and (n * pred) // r == v:
                    est[key] = v
                    basis[key] = ("chain", "g(%d,%d)=%d" % (n - 1, r - 1, pred))
                    changed = True
                continue
            best = None
            for ent in row["variants"]:
                if not (ent["drat_trim_verified"] and ent["drup_check_verified"]):
                    continue
                if ent["deg"] is not None and (pred is None or ent["deg"] < pred):
                    ent["degree_cut_justified"] = False if pred is not None else None
                    continue
                if ent["deg"] is not None:
                    ent["degree_cut_justified"] = True
                    ent["degree_cut_uses"] = "g(%d,%d)=%d" % (n - 1, r - 1, pred)
                kind = "plain" if ent["sb"] == "none" else "lex-leader"
                if best is None or (kind == "plain" and best[0] != "plain"):
                    best = (kind, ent["variant"])
            if best is not None:
                est[key] = v
                basis[key] = best
                changed = True
    for row in rows:
        key = (row["n"], row["r"])
        if key in est:
            row["proof_basis"] = basis[key][0]
            row["proof_basis_detail"] = basis[key][1]
        else:
            row["proof_basis"] = "UNESTABLISHED"
            problems.append("%s: value not established (missing verified variant or predecessor)" % row["dir"])
        if key in tm:
            row["fable_triples_match"] = tm[key]
        row["rate_floor_6dp"] = "%d.%06d" % divmod(int((row["value"] * 10 ** (6 * row["n"])) ** (1.0 / row["n"])) if False else irootf(row["value"], row["n"]), 10 ** 6)
    rows.sort(key=lambda x: (x["n"], x["r"]))
    bound_rows = [x for x in rows if x.get("upper_bound_only")]
    rows = [x for x in rows if not x.get("upper_bound_only")]
    out = {"claim": "exact values g(n,r) of the maximum r-uniform 3-sunflower-free family on [n]",
           "rows": rows, "count": len(rows), "upper_bounds": bound_rows, "problems": problems}
    json.dump(out, open(os.path.join(root, "index.json"), "w"), indent=1)
    lines = ["# Index of exact values (generated by tools/build_index.py; do not edit by hand)", "",
             "| (n,r) | g(n,r) | proof basis | detail | artifacts | fable re-check |", "|---|---|---|---|---|---|"]
    for row in rows:
        if row["kind"] == "casesplit":
            det = "%d case CNFs at |F|>=%d (sb=none), all proofs present, both checkers VERIFIED per solve_log.txt; argument in %s/ARGUMENT.md" % (row["n_cases_at_v_plus_1"], row["value"] + 1, row["dir"])
        elif row["kind"] == "sat":
            det = "; ".join("%s: sb=%s deg=%s %s B drat-trim %s drup_check %s" % (
                e["variant"], e["sb"], e["deg"] if e["deg"] is not None else "none", e["proof_bytes"],
                "OK" if e["drat_trim_verified"] else "NO", "OK" if e["drup_check_verified"] else "NO") for e in row["variants"])
        else:
            det = row["derivation"]["computation"] + " using " + row["derivation"]["uses"]
        fr = []
        if row.get("fable_triples_match") is not None:
            fr.append("triples match" if row["fable_triples_match"] else "TRIPLES DIFFER")
        if row.get("fable_drat_trim_verified") is not None:
            fr.append("drat-trim re-run OK" if row["fable_drat_trim_verified"] else "drat-trim re-run NOT OK")
        lines.append("| (%d,%d) | %d | %s | %s | %s | %s |" % (row["n"], row["r"], row["value"], row["proof_basis"],
                                                              det, row["dir"], ", ".join(fr) or "-"))
    if bound_rows:
        lines += ["", "Upper bounds proved by case split (not exact values):", "",
                  "| (n,r) | bound | detail | artifacts |", "|---|---|---|---|"]
        for row in bound_rows:
            lines.append("| (%d,%d) | g <= %d | %s | %s |" % (row["n"], row["r"], row["value"], row.get("proof_basis_detail", ""), row["dir"]))
    lines += ["", "%d exact rows, %d bound rows. Problems: %s" % (len(rows), len(bound_rows), "none" if not problems else "; ".join(problems))]
    open(os.path.join(root, "INDEX.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 1 if (check and problems) else 0


def casesplit_row(pk, d, problems):
    """A package proved by a case split (ARGUMENT.md): every cases/case_*.cnf has a .drup, and solve_log.txt
    records 's VERIFIED' from both drat-trim and drup_check2 for it; headers must claim |F| >= v+1 with no
    symmetry breaking (the unit clauses fix a labelling, so lex-leader clauses would be unsound here)."""
    m = re.match(r"g_(\d+)_(\d+)_(\d+)$", d)
    mb = re.match(r"bound_g_(\d+)_(\d+)_le(\d+)$", d)
    if m:
        n, r, v = int(m.group(1)), int(m.group(2)), int(m.group(3))
        row = {"n": n, "r": r, "value": v, "dir": "opus_packages/" + d, "kind": "casesplit", "variants": [], "cases": []}
        fs, ok = family_size(os.path.join(pk, d, "family.json"), n, r)
        row["family_size"] = fs
        if not ok or fs != v:
            problems.append("%s: family.json invalid or size %d != %d" % (d, fs, v))
    elif mb:
        # an upper bound g(n,r) <= v proved by a case split; no family of size v is claimed
        n, r, v = int(mb.group(1)), int(mb.group(2)), int(mb.group(3))
        row = {"n": n, "r": r, "value": v, "upper_bound_only": True, "dir": "opus_packages/" + d, "kind": "casesplit", "variants": [], "cases": []}
        if os.path.exists(os.path.join(pk, d, "family.json")):
            fs, ok = family_size(os.path.join(pk, d, "family.json"), n, r)
            row["family_size"] = fs
            if not ok or fs > v:
                problems.append("%s: family.json invalid or larger than the bound" % d)
    else:
        problems.append("%s: unrecognised case-split package name" % d)
        return {"n": 0, "r": 0, "value": 0, "dir": "opus_packages/" + d, "kind": "casesplit", "variants": [], "cases": [], "n_cases_at_v_plus_1": 0}
    log = open(os.path.join(pk, d, "solve_log.txt"), errors="replace").read() if os.path.exists(os.path.join(pk, d, "solve_log.txt")) else ""
    cdir = os.path.join(pk, d, "cases")
    ncase = 0
    for f in sorted(os.listdir(cdir)):
        if not (f.endswith(".cnf") and not f.startswith("base")):
            continue
        var = f[:-4]
        h = parse_header(os.path.join(cdir, f))
        drup = os.path.join(cdir, var + ".drup")
        if not os.path.exists(drup) and os.path.exists(drup + ".gz"):
            drup = drup + ".gz"
        ent = {"case": var, "k": h["k"], "sb": h["sb"], "deg": h["deg"], "proof_bytes": os.path.getsize(drup) if os.path.exists(drup) else None,
               "gzipped": drup.endswith(".gz")}
        lines = [l for l in log.splitlines() if l.strip().startswith(var + " drat-trim")]
        ent["log_verified"] = bool(lines) and all("drat-trim: s VERIFIED" in l and "drup_check2: s VERIFIED" in l for l in lines)
        if (h["n"], h["r"]) != (n, r) or h["k"] < v + 1:
            problems.append("%s/%s: header does not claim |F| >= %d" % (d, f, v + 1))
        if h["sb"] != "none":
            problems.append("%s/%s: symmetry breaking combined with fixed labelling" % (d, f))
        if ent["proof_bytes"] is None:
            problems.append("%s/%s: proof missing" % (d, var))
        if not ent["log_verified"]:
            problems.append("%s/%s: no 's VERIFIED' from both checkers in solve_log.txt" % (d, var))
        if h["k"] == v + 1:
            ncase += 1
        row["cases"].append(ent)
    row["n_cases_at_v_plus_1"] = ncase
    req = ("regenerate.sh", "ARGUMENT.md") if row.get("upper_bound_only") else ("regenerate.sh", "family_check.txt", "family_sfcheck.txt", "ARGUMENT.md")
    for f in req:
        if not os.path.exists(os.path.join(pk, d, f)):
            problems.append("%s: %s missing" % (d, f))
    if ncase == 0:
        problems.append("%s: no case CNF at |F| >= %d" % (d, v + 1))
    return row


def irootf(v, n):
    """floor(10^6 * v^(1/n)) as an integer, exact integer arithmetic."""
    x = v * 10 ** (6 * n)
    lo, hi = 1, 1 << ((x.bit_length() + n - 1) // n + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** n <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


if __name__ == "__main__":
    sys.exit(main())
