#!/usr/bin/env python3
"""merge_lcrt.py OUTDIR  (r2: also sums the lcrt5 diagnostics seg_c2 / seg_ch; nothing else changed)
 -> summary JSON on stdout (binds X, sigma, pmin, crt flag from master.json).

Checks: every task id 0..ntasks-1 present; duplicate lines for one task (resume overlap) must be identical apart from
nothing; the prefix of every task line must be unique.  Sums per-depth arrays, digest mod 2^64, collects events.
"""
import json, sys, glob, os

def addv(acc, v):
    for i, x in enumerate(v):
        while len(acc) <= i: acc.append(0)
        acc[i] += x

def main():
    d = sys.argv[1]
    m = json.load(open(os.path.join(d, 'master.json')))
    nt = m['ntasks']
    KEYS = ('nodes', 'pruned', 'c2p', 'c2a', 'c2i', 'live', 'small', 'cand', 'sqhit', 'kfilt', 'eclosed', 'epass', 'c2k')
    tot = {k: [] for k in KEYS}
    dig = int(m['master']['digest'], 16)
    digl = int(m['master'].get('digest_live', '0'), 16)
    for k in tot: addv(tot[k], m['master'].get(k, []))
    crt_tests, crt_skip, maxq = m['master']['crt_tests'], m['master']['crt_skip'], m['master']['maxq']
    seg_c2, seg_ch = m['master'].get('seg_c2', 0), m['master'].get('seg_ch', 0)   # r2 diagnostics (lcrt5 only)
    events = list(m['master']['events'])
    seen = {}
    dup_conflicts = 0
    for f in sorted(glob.glob(os.path.join(d, 'tasks_w*.jsonl'))):
        for line in open(f):
            if not line.endswith('\n'): continue
            t = json.loads(line)
            k = t['task']
            if k in seen:
                if seen[k] != line: dup_conflicts += 1
                continue
            seen[k] = line
            for key in tot: addv(tot[key], t.get(key, []))
            dig = (dig + int(t['digest'], 16)) % (1 << 64)
            digl = (digl + int(t.get('digest_live', '0'), 16)) % (1 << 64)
            crt_tests += t['crt_tests']; crt_skip += t['crt_skip']; maxq = max(maxq, t['maxq'])
            seg_c2 += t.get('seg_c2', 0); seg_ch += t.get('seg_ch', 0)
            events.extend(t['events'])
    missing = [k for k in range(nt) if k not in seen]
    prefixes = [tuple(json.loads(seen[k])['prefix']) for k in seen]
    out = {
        "X": m['X'], "sigma": m['sigma'], "pmin": m['pmin'], "crt": m['crt'], "kmax": m.get("kmax", 0), "filt": m.get("filt", 0),
        "sieve": m['sieve'], "D0": m['D0'],
        "live_total": sum(tot['live']), "live_by_depth": tot['live'], "digest_live": "%016x" % digl,
        "small_total": sum(tot['small']), "cand_total": sum(tot['cand']), "sqhit_total": sum(tot['sqhit']),
        "kfilt_total": sum(tot['kfilt']), "euler_closed_total": sum(tot['eclosed']), "euler_pass_total": sum(tot['epass']),
        "cqmode": m.get("cqmode", 0), "euler": m.get("euler", 0), "c2cand": m.get("c2cand", 0),
        "c2k_total": sum(tot['c2k']), "c2k_by_depth": tot['c2k'],
        "nodes_total": sum(tot['nodes']), "nodes_by_depth": tot['nodes'], "pruned_total": sum(tot['pruned']),
        "pruned_by_depth": tot['pruned'], "digest": "%016x" % dig,
        "c2_primes": sum(tot['c2p']), "c2_adm": sum(tot['c2a']), "c2_int": sum(tot['c2i']),
        "c2_primes_by_depth": tot['c2p'], "crt_tests": crt_tests, "crt_skip": crt_skip, "max_q_seen": maxq,
        "seg_c2_primes": seg_c2, "seg_children_primes": seg_ch,
        "events": events, "solutions": [e for e in events if e.get('reason') == 'SOLUTION'],
        "ntasks": nt, "tasks_found": len(seen), "missing_tasks": len(missing),
        "duplicate_conflicts": dup_conflicts, "unique_prefixes": len(set(prefixes)) == len(prefixes),
        "complete": os.path.exists(os.path.join(d, 'DONE')) and not missing and dup_conflicts == 0,
    }
    print(json.dumps(out))

if __name__ == '__main__':
    main()
