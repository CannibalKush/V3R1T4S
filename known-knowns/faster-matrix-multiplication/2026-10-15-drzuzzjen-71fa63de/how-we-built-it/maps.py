"""Dense maps of a Perminov scheme: U (r x n1n2), V (r x n2n3), W (n1n3 x r), and rebuild a scheme JSON."""
import json, numpy as np, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fmm_check as F

def load(path):
    d = json.load(open(path, encoding="utf-8"))
    n1, n2, n3 = d["n"]; r = d["m"]
    U, _, _ = F.forms(n1 * n2, d.get("u_fresh", []), d["u"])
    V, _, _ = F.forms(n2 * n3, d.get("v_fresh", []), d["v"])
    W, _, _ = F.forms(r, d.get("w_fresh", []), d["w"])
    return d, np.array(U, np.int8), np.array(V, np.int8), np.array(W, np.int8)

def scheme_json(d, parts):
    """parts: dict name->(fresh, final) for 'u','v','w'; other parts copied from d."""
    out = {"n": d["n"], "m": d["m"], "z2": False}
    for k in ("u", "v", "w"):
        fr, fi = parts.get(k, (d.get(k + "_fresh", []), d[k]))
        out[k + "_fresh"] = fr; out[k] = fi
    for k in ("u", "v", "w"):
        for f in out[k + "_fresh"] + out[k]:
            if not f:
                raise ValueError("empty linear form in %s" % k)
    tot = sum(len(f) - 1 for k in ("u", "v", "w") for f in out[k + "_fresh"] + out[k])
    out["complexity"] = {"reduced": tot}
    return out
