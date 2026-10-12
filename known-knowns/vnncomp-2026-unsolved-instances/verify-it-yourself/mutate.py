#!/usr/bin/env python3
"""
mutate.py -- write three broken variants of a witness that vnncheck.py must reject.

  python3 mutate.py PROPERTY.vnnlib.gz witness_plain.txt OUTDIR
    on_bound.txt : the coordinate closest to a bound is moved exactly onto that bound (not strictly inside)
    outside.txt  : the first coordinate is moved 1/1024 beyond its upper bound
    centre.txt   : every coordinate at the centre of its interval (the unperturbed image; the network is right there)
"""
import gzip, os, re, sys
from fractions import Fraction

vnn, wit, out = sys.argv[1:4]
txt = gzip.open(vnn, 'rt').read()
lo, hi = {}, {}
for op, h, w, c, v in re.findall(r'\(assert \((<=|>=) X\[0,(\d+),(\d+),(\d+)\] ([-+0-9.eE]+)\)\)', txt):
    i = (int(h) * 30 + int(w)) * 3 + int(c)
    (hi if op == '<=' else lo)[i] = Fraction(v)
x = [Fraction(l.strip()) for l in open(wit) if l.strip()]
assert len(x) == 2700 and len(lo) == len(hi) == 2700
os.makedirs(out, exist_ok=True)


def write(name, vals):
    with open(os.path.join(out, name), 'w') as f:
        f.write(''.join(repr(float(v)) + '\n' for v in vals))


d = [(min(x[i] - lo[i], hi[i] - x[i]), i) for i in range(2700)]
_, j = min(d)
m = list(x); m[j] = lo[j] if x[j] - lo[j] <= hi[j] - x[j] else hi[j]; write('on_bound.txt', m)
m = list(x); m[0] = hi[0] + Fraction(1, 1024); write('outside.txt', m)
write('centre.txt', [(lo[i] + hi[i]) / 2 for i in range(2700)])
print('wrote on_bound.txt outside.txt centre.txt')
