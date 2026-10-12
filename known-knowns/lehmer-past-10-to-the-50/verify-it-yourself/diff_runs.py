#!/usr/bin/env python3
"""diff_runs.py RUN_A RUN_B [--allow-subset] [--maxq]

Subtree-by-subtree comparison of two branch logs of the 10^50 search (pure python3).  Each run is a directory with
tasks_w*.jsonl (lcrt5) or a .jsonl/.jsonl.gz file (vlrt2).  Task lines are matched by their prime prefix, not by
task index, so logs written by different engines can be compared.

Compared per subtree (trailing zeros of per-depth lists ignored): the per-depth counts of visited nodes, live
nodes, small-regime nodes, Euler closures and Euler passes, integral two-prime completions (c2i), kfilt (= vlrt2
kfb), the two 64-bit digests of the visited and live node sets, and the presence of events.  These are the fields
the search's correctness rests on: identical digests mean both engines visited exactly the same prefixes.
Not compared: mode-dependent diagnostics (c2p, c2a, cand, sqhit, tdrej, seg_*), which legitimately differ between
modes and prime sources, and maxq (the largest two-prime bound scanned), which the two engines record differently;
pass --maxq to compare it as well (meaningful between two runs of the same engine).

IDENTICAL means: same set of prefixes (unless --allow-subset lets A be a subset of B), no duplicate lines that
disagree, and no field difference in any common subtree.  The output also counts differences per field.
Exit code 0 iff IDENTICAL.
"""
import glob
import gzip
import json
import os
import sys

FIELDS = ("nodes", "live", "small", "eclosed", "epass", "c2i", "kfilt")


def norm(a):
    a = [int(x) for x in a]
    while a and a[-1] == 0:
        a.pop()
    return a


def load(run):
    files = sorted(glob.glob(os.path.join(run, "tasks_w*.jsonl"))) if os.path.isdir(run) else [run]
    out, conflicts = {}, 0
    for f in files:
        opener = gzip.open if f.endswith(".gz") else open
        with opener(f, "rt") as fh:
            for ln in fh:
                ln = ln.strip()
                if not ln:
                    continue
                t = json.loads(ln)
                if "kfilt" not in t and "kfb" in t:
                    t["kfilt"] = t["kfb"]
                k = tuple(t["prefix"])
                if k in out and out[k] != t:
                    conflicts += 1
                out[k] = t
    return out, conflicts


def has_events(t):
    return bool(t.get("events")) or bool(t.get("nev"))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    A, ca = load(sys.argv[1])
    B, cb = load(sys.argv[2])
    only_a, only_b = set(A) - set(B), set(B) - set(A)
    ndiff, examples, per_field = 0, [], {}
    for k in set(A) & set(B):
        a, b = A[k], B[k]
        diffs = [f for f in FIELDS if norm(a.get(f, [])) != norm(b.get(f, []))]
        if a.get("digest") != b.get("digest"):
            diffs.append("digest")
        if a.get("digest_live") != b.get("digest_live"):
            diffs.append("digest_live")
        if "--maxq" in sys.argv and int(a.get("maxq", 0)) != int(b.get("maxq", 0)):
            diffs.append("maxq")
        if has_events(a) != has_events(b):
            diffs.append("events")
        if diffs:
            ndiff += 1
            for f in diffs:
                per_field[f] = per_field.get(f, 0) + 1
            if len(examples) < 5:
                examples.append({"prefix": list(k), "fields": diffs})
    identical = (ndiff == 0 and ca == 0 and cb == 0 and not only_a and (not only_b or "--allow-subset" in sys.argv))
    out = {"A": sys.argv[1], "B": sys.argv[2], "tasks_A": len(A), "tasks_B": len(B), "conflicts_A": ca, "conflicts_B": cb,
           "only_A": len(only_a), "only_B": len(only_b), "compared": len(set(A) & set(B)), "subtrees_with_difference": ndiff,
           "differences_per_field": per_field, "compared_fields": list(FIELDS) + ["digest", "digest_live", "events"] +
           (["maxq"] if "--maxq" in sys.argv else []), "examples": examples, "IDENTICAL": identical}
    print(json.dumps(out))
    sys.exit(0 if identical else 1)


if __name__ == "__main__":
    main()
