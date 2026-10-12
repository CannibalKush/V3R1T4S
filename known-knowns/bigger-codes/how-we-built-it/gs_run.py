#!/usr/bin/env python3
"""Rebuild the largest Graham-Sloane class for A(n,6,w) and list the words that can be added to it.

usage: gs_run.py N W {bose|singer} Q [--top K] [--out DIR]

For each of the K largest classes g it writes DIR/A{n}_6_{w}_{kind}{q}_g{g}_class.npy (the class code) and
..._free.npy (the weight-w words outside the class at distance >= 6 from every class word), plus a summary JSON.
The published A(29,6,11) and A(29,6,12) codes are class + free words (the free words were pairwise compatible):
    write_code.py OUT.txt N DIR/<tag>_class.npy DIR/<tag>_free.npy
"""
import sys, time, json, os
import numpy as np
from math import comb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sidon, gslib

OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "gs_out"
os.makedirs(OUT, exist_ok=True)


def main():
    n, w, kind, q = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 1
    A, m = (sidon.bose(q) if kind == "bose" else sidon.singer(q))
    assert len(A) >= n
    a = np.array(A[:n], dtype=np.int64)
    assert sidon.is_sidon(list(a), m)
    t0 = time.time()
    cc = gslib.class_counts(n, w, a, m, 64)
    assert cc.sum() == comb(n, w)
    order = np.argsort(-cc)
    print(f"A({n},6,{w}) {kind} q={q} m={m}: C(n,w)={comb(n,w)} avg={comb(n,w)/m:.2f} "
          f"max={cc[order[0]]} at g={order[0]}  top10={[int(cc[g]) for g in order[:10]]}  ({time.time()-t0:.1f}s)",
          flush=True)
    one_i, one_j, ptr, I, J = gslib.swap_tables(list(a), m)
    res = []
    for g in order[:top]:
        g = int(g)
        t0 = time.time()
        buf, cnt = gslib.class_words(n, w, a, m, g, 64, int(cc[g]) // 8 + 10000)
        cw = gslib.gather(buf, cnt)
        assert len(cw) == cc[g]
        buf, cnt = gslib.free_words(n, w, a, m, g, one_i, one_j, ptr, I, J, 64, 200000)
        fw = gslib.gather(buf, cnt)
        # class distribution of free words
        sums = np.array([sum(int(a[i]) for i in range(n) if (int(x) >> i) & 1) % m for x in fw], dtype=np.int64)
        u, c = np.unique(sums, return_counts=True)
        best = int(c.max()) if len(c) else 0
        print(f"  g={g}: class={len(cw)} free={len(fw)} in {len(u)} classes, max per class={best} "
              f"({time.time()-t0:.1f}s)", flush=True)
        tag = f"A{n}_6_{w}_{kind}{q}_g{g}"
        np.save(os.path.join(OUT, tag + "_class.npy"), cw)
        np.save(os.path.join(OUT, tag + "_free.npy"), fw)
        res.append({"g": g, "class": int(len(cw)), "free": int(len(fw)), "free_classes": int(len(u)),
                    "free_max_per_class": best})
    with open(os.path.join(OUT, f"A{n}_6_{w}_{kind}{q}_summary.json"), "w") as f:
        json.dump({"n": n, "w": w, "kind": kind, "q": q, "m": m, "a": [int(v) for v in a],
                   "max_class": int(cc[order[0]]), "avg": comb(n, w) / m, "results": res}, f, indent=1)


if __name__ == "__main__":
    main()
