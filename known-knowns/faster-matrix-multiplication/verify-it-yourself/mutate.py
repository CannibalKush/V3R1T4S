#!/usr/bin/env python3
"""mutate.py SCHEME.json OUTDIR -- write three guaranteed-invalid variants of a scheme (negative controls):
  drop_term.json   the last term removed
  bump_coeff.json  one nonzero coefficient of u in term 0 increased by 1
  swap_vw.json     the v rows of terms 0 and 1 exchanged (only if they differ)
fmmcheck.py must report FAIL on every one of them."""
import json, os, sys
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
d = json.load(open(src))
a = dict(d); a["u"], a["v"], a["w"] = d["u"][:-1], d["v"][:-1], d["w"][:-1]
json.dump(a, open(os.path.join(out, "drop_term.json"), "w"))
b = json.loads(json.dumps(d)); k = next(i for i, x in enumerate(b["u"][0]) if x not in (0, "0"))
x = b["u"][0][k]; b["u"][0][k] = (x + 1) if isinstance(x, int) else f"{x}+1"
if isinstance(x, str):
    from fractions import Fraction
    f = Fraction(x) + 1; b["u"][0][k] = str(f) if f.denominator != 1 else f.numerator
json.dump(b, open(os.path.join(out, "bump_coeff.json"), "w"))
c = json.loads(json.dumps(d)); c["v"][0], c["v"][1] = c["v"][1], c["v"][0]
assert c["v"][0] != c["v"][1]
json.dump(c, open(os.path.join(out, "swap_vw.json"), "w"))
print("wrote", out)
