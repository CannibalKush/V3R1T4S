#!/usr/bin/env python3
"""recompute_summary.py RUN [--top TOP.json] [--expect-ntasks N]

Recompute the totals and the 64-bit digests of a branch log from its per-task lines (pure python3), so that the
numbers quoted in the certificates can be re-derived from the shipped logs rather than trusted.

RUN is either
  * a directory holding master.json and tasks_w*.jsonl (the author engine lcrt5; use `tar xzf` on the shipped
    tarball first), or
  * a .jsonl or .jsonl.gz file of task lines (the independent engine vlrt2 writes this format).
--top gives the record of the top of the tree (depths 0..D0-1, which is not part of any task): master.json
  (key "master") or a vlrt2 summary JSON (key "top").  For a directory RUN the top record is read from master.json
  automatically.

Every task line describes one depth-D0 subtree (a prefix of D0 primes) and carries per-depth counters.  The engines
use different names for one counter (lcrt5 "kfilt" = vlrt2 "kfb"); everything else compared here has the same name.
Reported: number of tasks and distinct prefixes, duplicate lines that disagree, visited nodes (total and by depth),
live nodes, small-regime nodes, Euler closures and passes, integral two-prime completions (c2i), kfilt, maximum q,
events, and the digests  digest = (top digest + sum of task digests) mod 2^64  (likewise digest_live).
For a directory RUN it also checks that every task index 0..ntasks-1 is present and that the DONE marker exists.
"""
import glob
import gzip
import json
import os
import sys

FIELDS = ("nodes", "pruned", "live", "small", "eclosed", "epass", "c2i", "kfilt")
MASK = (1 << 64) - 1


def addv(acc, v):
    for i, x in enumerate(v):
        while len(acc) <= i:
            acc.append(0)
        acc[i] += int(x)


def norm_line(t):
    """Map a task line to a common dictionary (vlrt2's kfb is lcrt5's kfilt)."""
    u = dict(t)
    if "kfilt" not in u and "kfb" in u:
        u["kfilt"] = u["kfb"]
    if "events" not in u:
        u["events"] = [] if not u.get("nev") else ["%d events (vlrt2 writes them to a separate .events file)" % u["nev"]]
    return u


def iter_lines(path):
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                yield json.loads(ln)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    run = sys.argv[1]
    top = None
    expect_ntasks = None
    if "--top" in sys.argv:
        tj = json.load(open(sys.argv[sys.argv.index("--top") + 1]))
        top = tj.get("master", tj.get("top"))
    if "--expect-ntasks" in sys.argv:
        expect_ntasks = int(sys.argv[sys.argv.index("--expect-ntasks") + 1])
    files, ntasks_declared, done = [], None, None
    if os.path.isdir(run):
        m = json.load(open(os.path.join(run, "master.json")))
        top = m["master"] if top is None else top
        ntasks_declared = m["ntasks"]
        done = os.path.exists(os.path.join(run, "DONE"))
        files = sorted(glob.glob(os.path.join(run, "tasks_w*.jsonl")))
    else:
        files = [run]
    tot = {k: [] for k in FIELDS}
    dig = int(top["digest"], 16) if top else 0
    digl = int(top.get("digest_live", "0"), 16) if top else 0
    if top:
        for k in FIELDS:
            addv(tot[k], top.get(k if k != "kfilt" else ("kfilt" if "kfilt" in top else "kfb"), []))
    seen = {}
    conflicts = 0
    maxq = int(top.get("maxq", 0)) if top else 0
    events = list(top.get("events", [])) if top else []
    for f in files:
        for t in iter_lines(f):
            key = tuple(t["prefix"])
            if key in seen:
                if seen[key] != t:
                    conflicts += 1
                continue
            seen[key] = t
            u = norm_line(t)
            for k in FIELDS:
                addv(tot[k], u.get(k, []))
            dig = (dig + int(u["digest"], 16)) & MASK
            digl = (digl + int(u.get("digest_live", "0"), 16)) & MASK
            maxq = max(maxq, int(u.get("maxq", 0)))
            events.extend(u["events"])
    task_ids = sorted(t["task"] for t in seen.values())
    missing = None
    if ntasks_declared is not None:
        missing = ntasks_declared - len(set(task_ids))
    out = {"run": run, "task_lines": len(seen), "duplicate_conflicts": conflicts,
           "ntasks_declared": ntasks_declared, "missing_tasks": missing, "DONE_marker": done,
           "expect_ntasks_ok": (expect_ntasks is None or expect_ntasks == len(seen)),
           "top_included": top is not None,
           "nodes_total": sum(tot["nodes"]), "nodes_by_depth": tot["nodes"],
           "live_total": sum(tot["live"]), "live_by_depth": tot["live"],
           "small_total": sum(tot["small"]), "euler_closed_total": sum(tot["eclosed"]),
           "euler_pass_total": sum(tot["epass"]), "c2_int_total": sum(tot["c2i"]), "kfilt_total": sum(tot["kfilt"]),
           "max_q_seen": maxq, "events": events, "n_events": len(events),
           "digest": "%016x" % dig, "digest_live": "%016x" % digl}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
