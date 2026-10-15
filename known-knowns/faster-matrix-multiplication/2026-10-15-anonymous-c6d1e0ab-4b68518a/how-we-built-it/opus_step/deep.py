"""Deepen the best pairs of a scan: for each chosen (f, e), slice, then run T absorption trials, each with a random
term order, a random absorption method (greedy, rgreedy, rflat, beam) and a random starting pairing. Every trial is
recorded (JSONL); the best schemes are saved with their recipe (pair, seed, method, start_rot, permutation seed)."""
import argparse
import json
import os
import random
import signal
import sys
import time

sys.path.insert(0, '[the opus_step folder]')
import ca  # noqa: E402
sa = ca.sa

METHODS = ['greedy', 'rgreedy', 'rflat', 'beam']


def run_trial(ns, ts, seed):
    rng = random.Random(seed)
    perm = list(range(len(ts)))
    if seed:
        rng.shuffle(perm)
    method = METHODS[seed % len(METHODS)] if seed else 'greedy'
    rot = rng.randrange(3) if seed else 0
    tt = [ts[i] for i in perm]
    t2, ab = ca.absorb_all(ns, tt, method, random.Random(seed + 1), start_rot=rot)
    return t2, ab, method, rot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('parent')
    ap.add_argument('--axis', type=int, required=True)
    ap.add_argument('--scan', required=True, help='scan JSONL')
    ap.add_argument('--top', type=int, default=8)
    ap.add_argument('--trials', type=int, default=24)
    ap.add_argument('--cap', type=int, default=1800)
    ap.add_argument('--out', default='work/r2/deep')
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    signal.alarm(a.cap)
    os.makedirs(a.out, exist_ok=True)
    print('PID', os.getpid(), flush=True)
    recs = [json.loads(x) for x in open(a.scan)]
    recs = [r for r in recs if r['status'] == 'ok']
    recs.sort(key=lambda r: (r['rank'], r['raw'], r['idx']))
    seen = set()
    pick = []
    for r in recs:
        key = (json.dumps(r['f']), json.dumps(r['e']))
        if key in seen:
            continue
        seen.add(key)
        pick.append(r)
        if len(pick) >= a.top:
            break
    n, terms = sa.load(a.parent)
    nr, tr = sa.rotate_to(n, terms, a.axis)
    ck = f'{a.out}/deep_{a.tag or os.getpid()}.jsonl'
    best = None
    for r in pick:
        f = tuple(tuple(x) for x in r['f'])
        e = tuple(tuple(x) for x in r['e'])
        ns, ts = sa.slice_dim1(nr, tr, f, e)
        for s in range(a.trials):
            t0 = time.time()
            try:
                t2, ab, method, rot = run_trial(ns, ts, s)
                status = 'ok'
            except Exception as ex:
                t2, ab, method, rot, status = ts, 0, '?', 0, f'fail {ex!r}'[:200]
            cn, ct = sa.rotate_to(ns, t2, 3 - a.axis)
            rec = dict(idx=r['idx'], f=r['f'], e=r['e'], raw=len(ts), seed=s, method=method, rot=rot,
                       absorbed=ab, rank=len(ct), fmt=sa.fmt(cn), sec=round(time.time() - t0, 1), status=status)
            with open(ck, 'a') as fh:
                fh.write(json.dumps(rec) + '\n')
            print('DEEP', rec, flush=True)
            if status == 'ok' and (best is None or len(ct) < best):
                best = len(ct)
                path = f'{a.out}/{sa.fmt(cn)}_r{len(ct)}_{a.tag}_i{r["idx"]}_s{s}.json'
                sa.save(path, cn, ct, f'opus-fmm deep: {a.parent} axis {a.axis} f={r["f"]} e={r["e"]} '
                                      f'seed {s} method {method} start_rot {rot} raw {len(ts)} absorbed {ab}')
                print('SAVED', path, flush=True)
    print('DONE best', best, flush=True)


if __name__ == '__main__':
    main()
