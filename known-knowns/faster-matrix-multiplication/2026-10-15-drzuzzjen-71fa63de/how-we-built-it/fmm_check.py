#!/usr/bin/env python3
"""Exact checker for Perminov-format reduced FMM straight-line programs (standard library only).

Format (JSON): n=[n1,n2,n3], m=rank, u_fresh/u, v_fresh/v, w_fresh/w.
 - A inputs are indices 0..n1*n2-1 (row-major), u_fresh[i] defines variable n1*n2+i
   as a signed sum of earlier variables; u[k] is product k's left factor.
 - B likewise with n2*n3 inputs.
 - w_fresh[i] defines variable m+i over products 0..m-1 and earlier fresh vars;
   w[c] is output c. Perminov's README documents w as "the linear form of C^T"
   with n3*n1 rows (README lines 574 and 679 of the 2026-10-14 snapshot), i.e.
   output row c = k*n1 + i holds C[i][k]; confirmed on 113/113 published files
   (0/113 verify under plain C row-major; the addition count does not depend on it).
Verification is an exact integer tensor identity (equivalent to symbolic equality,
since every form is linear in A and in B).
Count: each form costs len(form)-1 (one binary +/- per extra term); negation is
free; coefficients must be exactly +1 or -1 and the EXPANDED linear form must
stay in {-1,0,1} (ternary SLP). A form must be non-empty, must not repeat an
index, must not reference itself or a later variable, and must not expand to
zero; any violation makes the scheme invalid (never a lower count).
Usage: fmm_check.py FILE [FILE...]   -> one JSON line per file.
"""
import json, sys


def _int(x, what):
    if isinstance(x, bool) or not isinstance(x, int):
        raise ValueError("%s is not an integer: %r" % (what, x))
    return x


def forms(n_in, fresh, final):
    """Expand fresh and final forms to dense integer vectors over the n_in base variables.
    Returns (final_vectors, additions, bad) where bad lists every non-ternary observation.
    Raises ValueError on a malformed form (empty, duplicate index, forward/self reference, zero form)."""
    vecs = [[1 if j == i else 0 for j in range(n_in)] for i in range(n_in)]
    adds, bad = 0, []

    def ev(form, what):
        nonlocal adds
        if not isinstance(form, list) or len(form) == 0:
            raise ValueError("%s is empty or not a list" % what)
        seen = set()
        v = [0] * n_in
        for t in form:
            c, i = _int(t["value"], what + " value"), _int(t["index"], what + " index")
            if c not in (1, -1):
                bad.append(c)
            if not (0 <= i < len(vecs)):
                raise ValueError("%s: forward/invalid reference %d (have %d vars)" % (what, i, len(vecs)))
            if i in seen:
                raise ValueError("%s: duplicate index %d in one form" % (what, i))
            seen.add(i)
            for j, x in enumerate(vecs[i]):
                if x:
                    v[j] += c * x
        adds += len(form) - 1
        if any(x not in (-1, 0, 1) for x in v):
            bad.append("expanded:%d" % max(abs(x) for x in v))
        if not any(v):
            raise ValueError("%s expands to the zero form" % what)
        return v

    for k, f in enumerate(fresh):
        vecs.append(ev(f, "fresh[%d]" % k))
    out = [ev(f, "final[%d]" % k) for k, f in enumerate(final)]
    return out, adds, bad


def check(d):
    """Full record for one scheme dict. Never raises on a malformed scheme: it returns
    exact_over_Z=False, valid_ternary_slp=False, reduced_additions=None and an 'error' string."""
    res = {"format": None, "rank": None, "adds_U": None, "adds_V": None, "adds_W": None,
           "reduced_additions": None, "nonternary_coeffs": [], "exact_over_Z": False, "valid_ternary_slp": False,
           "stated_reduced": None, "count_matches_stated": None, "error": None}
    try:
        n1, n2, n3 = (_int(x, "n") for x in d["n"])
        r = _int(d["m"], "m")
        res["format"], res["rank"] = "%dx%dx%d" % (n1, n2, n3), r
        res["stated_reduced"] = (d.get("complexity") or {}).get("reduced")
        U, au, bu = forms(n1 * n2, d.get("u_fresh", []), d["u"])
        V, av, bv = forms(n2 * n3, d.get("v_fresh", []), d["v"])
        W, aw, bw = forms(r, d.get("w_fresh", []), d["w"])
    except (ValueError, KeyError, TypeError, IndexError) as e:
        res["error"] = str(e) or repr(e)
        return res
    res.update({"adds_U": au, "adds_V": av, "adds_W": aw, "reduced_additions": au + av + aw,
                "nonternary_coeffs": sorted(set(map(str, bu + bv + bw)))})
    ok = len(U) == r and len(V) == r and len(W) == n1 * n3
    if not ok:
        res["error"] = "row counts: U %d V %d W %d, expected %d %d %d" % (len(U), len(V), len(W), r, r, n1 * n3)
    # C[i][k] = sum_j A[i][j] B[j][k]; Perminov stores outputs as C^T row-major: c = k*n1+i
    # (README lines 574/679 of the saved snapshot; confirmed on 113/113 published files)
    if ok:
        for i in range(n1):
            for k in range(n3):
                c = k * n1 + i
                for a in range(n1 * n2):
                    ua = [U[q][a] for q in range(r)]
                    for b in range(n2 * n3):
                        s = 0
                        for q in range(r):
                            if ua[q] and W[c][q]:
                                s += ua[q] * V[q][b] * W[c][q]
                        ai, aj = divmod(a, n2)
                        bj, bk = divmod(b, n3)
                        want = 1 if (ai == i and aj == bj and bk == k) else 0
                        if s != want:
                            ok = False
                            break
                    if not ok: break
                if not ok: break
            if not ok: break
    res["exact_over_Z"] = ok
    res["valid_ternary_slp"] = ok and not res["nonternary_coeffs"]
    stated = res["stated_reduced"]
    res["count_matches_stated"] = stated == res["reduced_additions"] if stated is not None else None
    return res


if __name__ == "__main__":
    for f in sys.argv[1:]:
        try:
            r = check(json.load(open(f, encoding="utf-8")))
        except Exception as e:
            r = {"error": repr(e), "exact_over_Z": False, "valid_ternary_slp": False, "reduced_additions": None}
        r["file"] = f.replace("\\", "/").split("/")[-1]
        print(json.dumps(r))
