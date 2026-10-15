"""Deterministic one-step rebuild (opus-fmm): parent (SHA-checked) -> slice (axis, f, e) -> absorption trial with a
given seed, exactly as deep.py runs it (seed 0 = supplied greedy order; seed s > 0 = term order shuffled by
random.Random(s), method METHODS[s % 4], start pairing drawn from the same generator) -> compare with a saved
scheme term by term and print the SHA256 of the rebuilt file.

  python rebuild_step.py PARENT --parent-sha SHA --axis A --f JSON --e JSON --seed S --out OUT [--compare SCHEME]
"""
import argparse
import hashlib
import json
import sys

sys.path.insert(0, '[the opus_step folder]')
import deep  # noqa: E402
ca = deep.ca
sa = deep.sa


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def canon(terms):
    return sorted(repr([sorted(f.items()) for f in t]) for t in terms)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('parent')
    ap.add_argument('--parent-sha', required=True)
    ap.add_argument('--axis', type=int, required=True)
    ap.add_argument('--f', required=True)
    ap.add_argument('--e', required=True)
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--compare', default='')
    a = ap.parse_args()
    got = sha(a.parent)
    print('PARENT_SHA256', got, flush=True)
    if got != a.parent_sha:
        raise SystemExit('parent checksum differs')
    n, terms = sa.load(a.parent)
    nr, tr = sa.rotate_to(n, terms, a.axis)
    f = tuple(tuple(x) for x in json.loads(a.f))
    e = tuple(tuple(x) for x in json.loads(a.e))
    ns, ts = sa.slice_dim1(nr, tr, f, e)
    print('slice', sa.fmt(ns), 'raw', len(ts), flush=True)
    t2, ab, method, rot = deep.run_trial(ns, ts, a.seed)
    cn, ct = sa.rotate_to(ns, t2, 3 - a.axis)
    sa.save(a.out, cn, ct, f'opus-fmm rebuild_step: parent sha {got} axis {a.axis} f={a.f} e={a.e} seed {a.seed} '
                           f'method {method} start_rot {rot} raw {len(ts)} absorbed {ab}')
    print('RESULT', sa.fmt(cn), 'rank', len(ct), 'method', method, 'start_rot', rot, 'absorbed', ab, flush=True)
    print('OUT_SHA256', sha(a.out), flush=True)
    if a.compare:
        n2, t3 = sa.load(a.compare)
        same = tuple(n2) == tuple(cn) and canon(t3) == canon(ct)
        print('TERM_IDENTICAL_TO', a.compare, same, flush=True)
        if not same:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
