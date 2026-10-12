#!/usr/bin/env python3
"""taskdiff_r2.py NEW_OUTDIR REF_OUTDIR [--ignore k1,k2]
Compare per-task JSON lines (one line per depth-D0 subtree) of two lcrt/lcrt5 runs.
Every key present in BOTH lines is compared (by default all of them, incl. maxq and events); keys present in only one
(e.g. the r2 diagnostics seg_c2 / seg_ch) are ignored.  Also compares the master.json 'master' record and ntasks.
Prints a JSON summary; exit 0 iff identical."""
import json, sys, glob, os

def load(d):
    out = {}
    conflicts = 0
    for f in sorted(glob.glob(os.path.join(d, 'tasks_w*.jsonl'))):
        for line in open(f):
            if not line.endswith('\n'):
                continue
            t = json.loads(line)
            k = t['task']
            if k in out and out[k] != t:
                conflicts += 1
            out[k] = t
    return out, conflicts

def main():
    a, b = sys.argv[1], sys.argv[2]
    ignore = {"seg_c2", "seg_ch"}   # diagnostics of the prime source (depend on the sieve limit by design)
    if '--ignore' in sys.argv:
        ignore |= set(sys.argv[sys.argv.index('--ignore') + 1].split(','))
    ma = json.load(open(os.path.join(a, 'master.json')))
    mb = json.load(open(os.path.join(b, 'master.json')))
    ta, ca = load(a)
    tb, cb = load(b)
    diffs = []
    master_same = all(ma['master'].get(k) == mb['master'].get(k) for k in set(ma['master']) & set(mb['master']) if k not in ignore)
    for k in sorted(set(ta) | set(tb)):
        if k not in ta or k not in tb:
            diffs.append((k, 'missing in ' + ('new' if k not in ta else 'ref')))
            continue
        x, y = ta[k], tb[k]
        for key in set(x) & set(y):
            if key in ignore:
                continue
            if x[key] != y[key]:
                diffs.append((k, key))
                break
    res = {"new": a, "ref": b, "ntasks_new": ma['ntasks'], "ntasks_ref": mb['ntasks'], "tasks_new": len(ta), "tasks_ref": len(tb),
           "master_same": master_same, "conflicts_new": ca, "conflicts_ref": cb, "n_diff": len(diffs), "first_diffs": diffs[:10],
           "seg_c2_total": sum(t.get('seg_c2', 0) for t in ta.values()), "seg_ch_total": sum(t.get('seg_ch', 0) for t in ta.values()),
           "IDENTICAL": (not diffs and master_same and ma['ntasks'] == mb['ntasks'] and ca == 0 and cb == 0)}
    print(json.dumps(res))
    sys.exit(0 if res['IDENTICAL'] else 1)

if __name__ == '__main__':
    main()
