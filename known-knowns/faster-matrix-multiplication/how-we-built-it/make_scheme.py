#!/usr/bin/env python3
"""make_scheme.py -- deterministic regeneration of one peeled scheme from a source scheme and a direction pair.

Usage:
    python3 make_scheme.py SOURCE AXIS "e0 e1 ..." "f0 f1 ..." OUT.json

  SOURCE  LITA .npz or Perminov-style .json scheme
  AXIS    n, m or p (the dimension that shrinks by one)
  e, f    the two direction vectors (rationals, length = that dimension), <e,f> != 0, e and f each normalised with
          first nonzero entry 1 (as printed in the sweep CSV)

The projected scheme is built by peel.project, zero terms are dropped, and the result is written as Perminov-style
JSON with the same `note` field as the published files, so OUT.json is byte-identical to the file in ../schemes/
when SOURCE has the same file name as the source named in that note.  Verify OUT.json with
../verify-it-yourself/fmmcheck.py.
"""
import argparse
import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import peel  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("axis", choices=["n", "m", "p"])
    ap.add_argument("e")
    ap.add_argument("f")
    ap.add_argument("out")
    args = ap.parse_args()

    t0 = time.time()
    fmt, u, v, w, meta = peel.load_scheme(args.source)
    axis = "nmp".index(args.axis)
    F = peel.Field(None)
    e = tuple(Fraction(x) for x in args.e.split())
    f = tuple(Fraction(x) for x in args.f.split())
    assert len(e) == len(f) == fmt[axis], "direction length must equal the peeled dimension"
    assert peel.dot(e, f, F) != 0, "<e,f> must be nonzero"
    fmt2, u2, v2, w2 = peel.project(fmt, u, v, w, F, axis, e, f)
    note = peel.note_for(os.path.basename(args.source), args.axis, e, f)
    json.dump(peel.to_json(fmt2, u2, v2, w2, F, note=note), open(args.out, "w"))
    print(json.dumps({"source": os.path.basename(args.source), "source_format": list(fmt), "source_terms": len(u),
                      "axis": args.axis, "e": args.e, "f": args.f, "projected_format": list(fmt2),
                      "projected_terms_nonzero": len(u2), "out": args.out,
                      "seconds": round(time.time() - t0, 1)}, indent=1))


if __name__ == "__main__":
    main()
