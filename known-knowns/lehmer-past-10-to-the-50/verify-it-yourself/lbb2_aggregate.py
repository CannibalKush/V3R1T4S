#!/usr/bin/env python3
"""lbb2_aggregate.py DIR  --  aggregate a parallel lbb2 run (pure python3).

DIR holds gen.out (the serial generator: TASK lines with the depth-D0 prefixes and a TOTAL line for the top of the
tree) and w*.out (one file per worker: a DONE line per finished task, echoing its prefix, and a TOTAL line).
The run is complete and clean iff every worker finished, every task index 0..ntask-1 is DONE exactly once with the
matching prefix, and there is no SOLUTION, EULERPASS, FATAL or WARN line anywhere.  Totals are summed over the
generator and all workers.  Exit code 0 iff complete_and_clean.
"""
import glob
import json
import os
import sys

BAD = ("SOLUTION", "EULERPASS", "FATAL", "WARN", "M1INT", "M2INT")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    d = sys.argv[1]
    gen = open(os.path.join(d, "gen.out")).read().splitlines()
    tasks = [l for l in gen if l.startswith("TASK")]
    events = {"gen": [l for l in gen if l.startswith(BAD)]}
    tot = {}

    def addtot(line):
        f = line.split()
        for i in range(1, len(f) - 1, 2):
            try:
                tot[f[i]] = tot.get(f[i], 0) + float(f[i + 1])
            except ValueError:
                pass

    gen_total = [l for l in gen if l.startswith("TOTAL")]
    assert len(gen_total) == 1, "generator did not finish (no single TOTAL line)"
    addtot(gen_total[0])
    done, finished = {}, 0
    wfiles = sorted(glob.glob(os.path.join(d, "w*.out")))
    for wf in wfiles:
        for l in open(wf).read().splitlines():
            if l.startswith("DONE"):
                idx = int(l.split()[1])
                pre = l.split(":", 1)[1].split()
                assert idx not in done, "duplicate task %d" % idx
                done[idx] = pre
            if l.startswith(BAD):
                events.setdefault(os.path.basename(wf), []).append(l)
            if l.startswith("TOTAL"):
                finished += 1
                addtot(l)
    missing = [i for i in range(len(tasks)) if i not in done]
    mismatch = [i for i in done if done[i] != tasks[i].split()[1:]]
    maxq1 = max([int(l.split("maxq1")[1].split()[0]) for f in [os.path.join(d, "gen.out")] + wfiles
                 for l in open(f) if l.startswith("TOTAL")] or [0])
    res = {"dir": d, "ntask": len(tasks), "workers": len(wfiles), "workers_finished": finished, "tasks_done": len(done),
           "missing": len(missing), "prefix_mismatch": len(mismatch),
           "nodes_total": int(tot.get("nodes", 0)), "m2apcand": int(tot.get("m2apcand", 0)), "m2q1": int(tot.get("m2q1", 0)),
           "m3euler": int(tot.get("m3euler", 0)), "m1int": int(tot.get("m1int", 0)), "m2int": int(tot.get("m2int", 0)),
           "euler_pass": int(tot.get("euler_pass", 0)), "solutions": int(tot.get("solutions", 0)),
           "segq": int(tot.get("segq", 0)), "segchild": int(tot.get("segchild", 0)), "maxq1": maxq1,
           "events": {k: v for k, v in events.items() if v}}
    res["complete_and_clean"] = (finished == len(wfiles) and not missing and not mismatch and res["solutions"] == 0
                                 and res["euler_pass"] == 0 and not res["events"])
    print(json.dumps(res, indent=1))
    sys.exit(0 if res["complete_and_clean"] else 1)


if __name__ == "__main__":
    main()
