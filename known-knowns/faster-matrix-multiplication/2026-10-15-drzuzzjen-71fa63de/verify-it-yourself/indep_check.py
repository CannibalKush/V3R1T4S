#!/usr/bin/env python3
"""Independent verifier for addition-reduced ternary (ZT) matrix-multiplication schemes.

Written from the README definition only (see ../output/definition_quotes.md).

Format: {"n":[n1,n2,n3], "m":rank, "z2":false, "complexity":{"naive":x,"reduced":y},
         "u_fresh","v_fresh","w_fresh","u","v","w"}  -- every form a list of {"index":i,"value":c}.
  A is n1 x n2 (flat i*n2+p), B is n2 x n3 (flat q*n3+j), w row r = j*n1+i encodes C^T.
  Fresh entry k of map X gets index base_X + k (base_U=n1*n2, base_V=n2*n3, base_W=m).

Counting: each form (fresh or final) with t terms costs t-1 additions (negation is free).

Usage:
  python indep_check.py FILE [FILE ...] [--trials N] [--seed S] [--bank DIR]
Prints one JSON line per file.  With --bank, also reports the minimum published
complexity.reduced for the same (n, m) (and for the transposed format) computed from the bank files.
"""
import json
import os
import random
import sys

MAPS = ("u", "v", "w")


class Reject(Exception):
    pass


def _no_dup_keys(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise Reject("duplicate JSON key %r" % k)
        d[k] = v
    return d


def _bad_const(c):
    raise Reject("non-finite JSON constant %s" % c)


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    return json.loads(txt, object_pairs_hook=_no_dup_keys, parse_constant=_bad_const)


def parse_form(form, where, limit):
    """Validate one sparse form; return list of (index, value). Indices must be < limit."""
    if not isinstance(form, list):
        raise Reject("%s: form is not a list" % where)
    if len(form) == 0:
        raise Reject("%s: empty form" % where)
    seen = set()
    out = []
    for t, term in enumerate(form):
        if not isinstance(term, dict) or set(term.keys()) != {"index", "value"}:
            raise Reject("%s term %d: must be an object with exactly keys index,value" % (where, t))
        i, c = term["index"], term["value"]
        if not _is_int(i):
            raise Reject("%s term %d: non-integer index %r" % (where, t, i))
        if not _is_int(c):
            raise Reject("%s term %d: non-integer coefficient %r" % (where, t, c))
        if c not in (1, -1):
            raise Reject("%s term %d: coefficient %r not in {-1,+1}" % (where, t, c))
        if i < 0:
            raise Reject("%s term %d: negative index %d" % (where, t, i))
        if i >= limit:
            raise Reject("%s term %d: index %d is a self/forward/out-of-range reference (limit %d)"
                         % (where, t, i, limit))
        if i in seen:
            raise Reject("%s: duplicate index %d in one form" % (where, i))
        seen.add(i)
        out.append((i, c))
    return out


def parse_scheme(obj):
    if not isinstance(obj, dict):
        raise Reject("top level is not an object")
    required = {"n", "m", "z2", "complexity", "u_fresh", "v_fresh", "w_fresh", "u", "v", "w"}
    missing = required - set(obj)
    if missing:
        raise Reject("missing keys %s" % sorted(missing))
    warnings = []
    extra = set(obj) - required
    if extra:
        warnings.append("extra top-level keys %s" % sorted(extra))
    n = obj["n"]
    if not (isinstance(n, list) and len(n) == 3 and all(_is_int(x) and x >= 1 for x in n)):
        raise Reject("bad n %r" % (n,))
    m = obj["m"]
    if not (_is_int(m) and m >= 1):
        raise Reject("bad m %r" % (m,))
    if obj["z2"] is not False:
        raise Reject("z2 must be false for a ZT scheme over Z (got %r)" % (obj["z2"],))
    cx = obj["complexity"]
    deviations = []
    if not (isinstance(cx, dict) and "reduced" in cx and _is_int(cx["reduced"])
            and set(cx) <= {"naive", "reduced"}):
        raise Reject("bad complexity field %r" % (cx,))
    if "naive" not in cx:
        # README L641 specifies {"naive": x, "reduced": y}; a missing naive is a format deviation
        # that does not affect correctness or the addition count, so it is reported, not fatal.
        deviations.append("complexity.naive missing (README format requires it)")
        cx = {"naive": None, "reduced": cx["reduced"]}
    elif not _is_int(cx["naive"]):
        raise Reject("bad complexity.naive %r" % (cx["naive"],))
    n1, n2, n3 = n
    base = {"u": n1 * n2, "v": n2 * n3, "w": m}
    rows_expected = {"u": m, "v": m, "w": n3 * n1}
    S = {"n": n, "m": m, "complexity": cx, "base": base, "fresh": {}, "final": {}}
    for X in MAPS:
        fr = obj[X + "_fresh"]
        if not isinstance(fr, list):
            raise Reject("%s_fresh is not a list" % X)
        fresh = []
        for k, form in enumerate(fr):
            fresh.append(parse_form(form, "%s_fresh[%d]" % (X, k), base[X] + k))
        rows = obj[X]
        if not isinstance(rows, list):
            raise Reject("%s is not a list" % X)
        if len(rows) != rows_expected[X]:
            raise Reject("%s has %d rows, expected %d" % (X, len(rows), rows_expected[X]))
        final = []
        for r, form in enumerate(rows):
            final.append(parse_form(form, "%s[%d]" % (X, r), base[X] + len(fresh)))
        S["fresh"][X] = fresh
        S["final"][X] = final
    S["warnings"] = warnings
    S["deviations"] = deviations
    return S


def expand(S, X):
    """Expand fresh and final forms of map X into dense integer vectors over the originals."""
    b = S["base"][X]
    vecs = []  # expansion of fresh var k
    for form in S["fresh"][X]:
        v = [0] * b
        for i, c in form:
            if i < b:
                v[i] += c
            else:
                src = vecs[i - b]
                for j in range(b):
                    if src[j]:
                        v[j] += c * src[j]
        vecs.append(v)
    rows = []
    for form in S["final"][X]:
        v = [0] * b
        for i, c in form:
            if i < b:
                v[i] += c
            else:
                src = vecs[i - b]
                for j in range(b):
                    if src[j]:
                        v[j] += c * src[j]
        rows.append(v)
    return vecs, rows


def check_expansions(S, reasons, warnings):
    exp = {}
    for X in MAPS:
        vecs, rows = expand(S, X)
        for k, v in enumerate(vecs):
            if not any(v):
                reasons.append("%s_fresh[%d] expands to the zero form" % (X, k))
            bad = [c for c in v if c not in (-1, 0, 1)]
            if bad:
                reasons.append("%s_fresh[%d] expands to non-ternary coefficients %s" % (X, k, sorted(set(bad))))
        for r, v in enumerate(rows):
            if not any(v):
                reasons.append("%s[%d] expands to the zero form" % (X, r))
            bad = [c for c in v if c not in (-1, 0, 1)]
            if bad:
                reasons.append("%s[%d] expands to non-ternary coefficients %s" % (X, r, sorted(set(bad))))
        exp[X] = rows
        # usage of fresh vars
        b = S["base"][X]
        used = set()
        for form in S["fresh"][X] + S["final"][X]:
            for i, _ in form:
                if i >= b:
                    used.add(i - b)
        unused = [k for k in range(len(S["fresh"][X])) if k not in used]
        if unused:
            warnings.append("%s_fresh unused entries %s (still counted)" % (X, unused[:10]))
    # products whose output column in W is identically zero -> effective rank lower
    m = S["m"]
    W = exp["w"]
    dead = [k for k in range(m) if all(W[r][k] == 0 for r in range(len(W)))]
    if dead:
        warnings.append("products never used in any output: %s (effective rank %d)" % (dead, m - len(dead)))
    return exp


def tensor_check(S, exp, transpose_out=True):
    """Exact check of sum_k U[k][a] V[k][b] W[r][k] == delta over all (a, b, r).
    transpose_out=True: r = j*n1+i (C^T, the definition). False: r = i*n3+j (plain C)."""
    n1, n2, n3 = S["n"]
    m = S["m"]
    U, V, W = exp["u"], exp["v"], exp["w"]
    wcols = [[(r, W[r][k]) for r in range(len(W)) if W[r][k]] for k in range(m)]
    T = {}
    for k in range(m):
        su = [(a, c) for a, c in enumerate(U[k]) if c]
        sv = [(b, c) for b, c in enumerate(V[k]) if c]
        for a, ca in su:
            for b, cb in sv:
                cab = ca * cb
                for r, cw in wcols[k]:
                    key = (a, b, r)
                    T[key] = T.get(key, 0) + cab * cw
    target = {}
    for i in range(n1):
        for p in range(n2):
            for j in range(n3):
                r = j * n1 + i if transpose_out else i * n3 + j
                target[(i * n2 + p, p * n3 + j, r)] = 1
    bad = 0
    first = None
    for key in set(T) | set(target):
        if T.get(key, 0) != target.get(key, 0):
            bad += 1
            if first is None:
                first = (key, T.get(key, 0), target.get(key, 0))
    return bad, first


def run_slp(S, A, B):
    """Execute the SLP literally (fresh vars in order, no expansion); return C^T-indexed outputs."""
    n1, n2, n3 = S["n"]
    m = S["m"]

    def lin(vals, base, forms):
        x = list(vals)
        for form in forms:  # fresh
            x.append(sum(c * x[i] for i, c in form))
        return x

    a = [A[i][p] for i in range(n1) for p in range(n2)]
    b = [B[q][j] for q in range(n2) for j in range(n3)]
    xa = lin(a, n1 * n2, S["fresh"]["u"])
    xb = lin(b, n2 * n3, S["fresh"]["v"])
    left = [sum(c * xa[i] for i, c in form) for form in S["final"]["u"]]
    right = [sum(c * xb[i] for i, c in form) for form in S["final"]["v"]]
    prods = [left[k] * right[k] for k in range(m)]
    xp = lin(prods, m, S["fresh"]["w"])
    return [sum(c * xp[i] for i, c in form) for form in S["final"]["w"]]


def random_check(S, trials, seed):
    n1, n2, n3 = S["n"]
    rng = random.Random(seed)
    fails_ct = 0
    fails_c = 0
    for _ in range(trials):
        A = [[rng.randint(-1000, 1000) for _ in range(n2)] for _ in range(n1)]
        B = [[rng.randint(-1000, 1000) for _ in range(n3)] for _ in range(n2)]
        C = [[sum(A[i][p] * B[p][j] for p in range(n2)) for j in range(n3)] for i in range(n1)]
        out = run_slp(S, A, B)
        ok_ct = all(out[j * n1 + i] == C[i][j] for i in range(n1) for j in range(n3))
        ok_c = all(out[i * n3 + j] == C[i][j] for i in range(n1) for j in range(n3))
        fails_ct += not ok_ct
        fails_c += not ok_c
    return fails_ct, fails_c


def count_adds(S):
    per = {}
    for X in MAPS:
        per[X + "_fresh"] = sum(len(f) - 1 for f in S["fresh"][X])
        per[X] = sum(len(f) - 1 for f in S["final"][X])
    per_map = {X.upper(): per[X + "_fresh"] + per[X] for X in MAPS}
    return per, per_map, sum(per.values())


def naive_count(exp):
    """Additions of the unreduced scheme: every expanded form evaluated on its own."""
    return sum(sum(1 for c in row if c) - 1 for X in MAPS for row in exp[X])


def check_file(path, trials=24, seed=20261014):
    rec = {"file": os.path.abspath(path), "pass": False, "pass_substantive": False,
           "reasons": [], "warnings": [], "format_deviations": []}
    try:
        obj = load_json(path)
        S = parse_scheme(obj)
    except Reject as e:
        rec["reasons"].append("parse: " + str(e))
        return rec
    except (ValueError, OSError) as e:
        rec["reasons"].append("parse: %s: %s" % (type(e).__name__, e))
        return rec
    n1, n2, n3 = S["n"]
    rec["format"] = "%dx%dx%d" % (n1, n2, n3)
    rec["rank"] = S["m"]
    rec["warnings"].extend(S["warnings"])
    per, per_map, total = count_adds(S)
    rec["counts"] = per
    rec["per_map"] = per_map
    rec["total"] = total
    rec["declared_reduced"] = S["complexity"]["reduced"]
    rec["declared_naive"] = S["complexity"]["naive"]
    rec["n_fresh"] = {X: len(S["fresh"][X]) for X in MAPS}
    reasons = rec["reasons"]
    exp = check_expansions(S, reasons, rec["warnings"])
    rec["naive_recomputed"] = naive_count(exp)
    bad_ct, first_ct = tensor_check(S, exp, True)
    rec["tensor_CT_mismatches"] = bad_ct
    if bad_ct:
        reasons.append("tensor identity (C^T convention) fails at %d entries, first %s" % (bad_ct, first_ct))
        bad_c, _ = tensor_check(S, exp, False)
        rec["tensor_C_mismatches"] = bad_c
        if bad_c == 0:
            reasons.append("scheme is correct only under the plain-C (non-transposed) output convention")
    f_ct, f_c = random_check(S, trials, seed)
    rec["random_trials"] = trials
    rec["random_fail_CT"] = f_ct
    rec["random_fail_C"] = f_c
    if f_ct:
        reasons.append("random evaluation (C^T) failed on %d/%d integer pairs" % (f_ct, trials))
    if bad_ct == 0 and f_ct:
        reasons.append("INTERNAL: tensor check and SLP evaluation disagree")
    if total != S["complexity"]["reduced"]:
        reasons.append("declared complexity.reduced=%d but counted %d" % (S["complexity"]["reduced"], total))
    if S["complexity"]["naive"] is not None and rec["naive_recomputed"] != S["complexity"]["naive"]:
        rec["warnings"].append("declared complexity.naive=%d but recomputed %d"
                               % (S["complexity"]["naive"], rec["naive_recomputed"]))
    rec["format_deviations"] = S["deviations"]
    # pass_substantive: parses, ternary, exact product (tensor + random), honest count.
    # pass (strict): additionally no deviation from the README field layout.
    rec["pass_substantive"] = not reasons
    rec["pass"] = not reasons and not S["deviations"]
    return rec


def bank_index(bank_dir):
    """(n1,n2,n3,m) -> list of (declared reduced, recounted total, pass, file) from the bank files."""
    idx = {}
    for name in sorted(os.listdir(bank_dir)):
        p = os.path.join(bank_dir, name)
        if not os.path.isfile(p):
            continue
        r = check_file(p, trials=20)
        if "format" not in r:
            continue
        key = (r["format"], r["rank"])
        idx.setdefault(key, []).append((r["declared_reduced"], r["total"], r["pass"], name))
    return idx


def main(argv):
    trials, seed, bank = 24, 20261014, None
    files = []
    it = iter(argv)
    for a in it:
        if a == "--trials":
            trials = int(next(it))
        elif a == "--seed":
            seed = int(next(it))
        elif a == "--bank":
            bank = next(it)
        else:
            files.append(a)
    if trials < 20:
        print("refusing: need at least 20 random trials", file=sys.stderr)
        return 2
    idx = bank_index(bank) if bank else None
    allpass = True
    for f in files:
        rec = check_file(f, trials, seed)
        if idx is not None and "format" in rec:
            n1, n2, n3 = (int(x) for x in rec["format"].split("x"))
            same = idx.get((rec["format"], rec["rank"]), [])
            good = [e for e in same if e[2]]
            rec["published_same_format_rank"] = len(same)
            if good:
                pmin = min(e[0] for e in good)
                rec["published_min_reduced"] = pmin
                rec["published_min_recounted"] = min(e[1] for e in good)
                rec["published_min_file"] = min(good)[3]
                rec["strictly_below_published"] = bool(rec.get("total") is not None and rec["total"] < pmin)
            else:
                rec["published_min_reduced"] = None
                rec["strictly_below_published"] = None
            tfmt = "%dx%dx%d" % (n3, n2, n1)
            tgood = [e for e in idx.get((tfmt, rec["rank"]), []) if e[2]]
            rec["published_min_transposed_format"] = (tfmt, min(e[0] for e in tgood)) if tgood else (tfmt, None)
            anyrank = [e for (fm, _r), lst in idx.items() if fm == rec["format"] for e in lst if e[2]]
            rec["published_min_same_format_any_rank"] = min(e[0] for e in anyrank) if anyrank else None
        allpass &= rec["pass"]
        print(json.dumps(rec, sort_keys=True))
        sys.stdout.flush()
    return 0 if allpass else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
