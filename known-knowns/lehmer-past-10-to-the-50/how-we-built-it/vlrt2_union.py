#!/usr/bin/env python3
"""vlrt2_union.py -- task-list and merge helpers used to assemble branch_logs/vlrt2_full50_union.tasks.jsonl.gz.

The independent engine vlrt2 was run on 10^50 in three pieces (see README.md in this directory):
  part 1  a full run stopped by hand after ~4 min           -> 286 task lines
  part 2  VSEL=<34 prefixes> VSTRIDE=20 VOFF=7               -> 3 315 task lines
  part 3  VSEL=<the 62 061 prefixes not yet covered>         -> 62 061 task lines (vlrt2_r50c.tasks.jsonl.gz)
These subcommands are the steps between the runs.  The original steps were short inline Python; this file re-implements
them and was checked to reproduce the original files byte for byte (sha256 values in README.md).

  segc2      LCRT4_LOG                     prefixes (depth D0) of the tasks holding a "SEGC2" line of an lcrt5 LCRT-4 log
  minus      PREFIXES TASKS.jsonl...       the PREFIXES lines whose prefix is not in any TASKS file (input order kept)
  remaining  RUN TASKS.jsonl...            prefixes of all tasks of RUN (an lcrt5 output dir or a tasks .jsonl) that
                                           are not in any TASKS file, sorted, one "p1,p2,...,p11" per line (VSEL format)
  merge      TASKS.jsonl...                union of task files keyed by prefix; duplicate prefixes must give identical
                                           records; written sorted by prefix with json.dumps (= v6_50_merged.tasks.jsonl)
  union      TASKS.jsonl...                plain concatenation after checking the prefix sets are disjoint
                                           (= full50_union.tasks.jsonl = merged part1+2 followed by part 3, as-is)
All output goes to stdout.  python3 only, no packages.
"""
import argparse, glob, gzip, json, os, sys


def opn(fn):
    return gzip.open(fn, 'rt') if fn.endswith('.gz') else open(fn)


def task_lines(fn):
    """Complete JSON task lines of a vlrt2 tasks file or an lcrt5 output directory (partial last lines skipped)."""
    files = sorted(glob.glob(os.path.join(fn, 'tasks_w*.jsonl'))) if os.path.isdir(fn) else [fn]
    for f in files:
        with opn(f) as h:
            for line in h:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                yield line, d


def prefixes_of(files):
    s = set()
    for fn in files:
        for _, d in task_lines(fn):
            s.add(tuple(d['prefix']))
    return s


def fmt(p):
    return ','.join(map(str, p))


def cmd_segc2(a):
    seen = []
    for line in open(a.log):
        if line.startswith('SEGC2'):
            t = tuple(int(v) for v in line.split('prefix')[1].split('qa')[0].split()[:a.d0])
            if t not in seen:
                seen.append(t)
    for t in seen:
        print(fmt(t))


def cmd_minus(a):
    have = prefixes_of(a.tasks)
    for line in open(a.prefixes):
        line = line.strip()
        if line and tuple(int(v) for v in line.split(',')) not in have:
            print(line)


def cmd_remaining(a):
    allp = prefixes_of([a.run])
    have = prefixes_of(a.tasks)
    for t in sorted(allp - have):
        print(fmt(t))


def cmd_merge(a):
    m = {}
    for fn in a.tasks:
        for _, d in task_lines(fn):
            k = tuple(d['prefix'])
            if k in m:
                assert m[k] == d, ('nondeterministic duplicate', k)
            m[k] = d
    out = sys.stdout
    for k in sorted(m):
        out.write(json.dumps(m[k]) + '\n')


def cmd_union(a):
    seen = set()
    out = sys.stdout
    for fn in a.tasks:
        for line, d in task_lines(fn):
            k = tuple(d['prefix'])
            assert k not in seen, ('overlap', k)
            seen.add(k)
            out.write(line if line.endswith('\n') else line + '\n')
    print(len(seen), 'task lines', file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('segc2'); p.add_argument('log'); p.add_argument('--d0', type=int, default=11); p.set_defaults(f=cmd_segc2)
    p = sp.add_parser('minus'); p.add_argument('prefixes'); p.add_argument('tasks', nargs='*'); p.set_defaults(f=cmd_minus)
    p = sp.add_parser('remaining'); p.add_argument('run'); p.add_argument('tasks', nargs='*'); p.set_defaults(f=cmd_remaining)
    p = sp.add_parser('merge'); p.add_argument('tasks', nargs='+'); p.set_defaults(f=cmd_merge)
    p = sp.add_parser('union'); p.add_argument('tasks', nargs='+'); p.set_defaults(f=cmd_union)
    a = ap.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()
