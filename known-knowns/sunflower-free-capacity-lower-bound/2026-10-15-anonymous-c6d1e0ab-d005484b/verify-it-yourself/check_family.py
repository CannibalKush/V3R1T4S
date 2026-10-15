#!/usr/bin/env python3
"""Standalone checker for uniform 3-sunflower-free families (standard library only).

Definition checked: three DISTINCT sets A, B, C form a 3-sunflower when
A & B == A & C == B & C (empty core allowed, so three pairwise disjoint sets
are a sunflower).  A family is sunflower-free when no three distinct members
form a sunflower.

Input JSON: {"n": int, "r": int, "sets": [[elements...], ...]}
  Elements must all lie in 1..n or all lie in 0..n-1 (either labelling of an
  n-point ground set is accepted; the checker reports which).

Checks:
  1. structure: ints, every member a set (no repeated element), size exactly r,
     elements inside the ground set, members pairwise distinct;
  2. sunflower test, method A: for every pair (A, B) the third member C must
     satisfy C contains A&B and C misses A^B; candidates are found with
     per-point column bitsets over the member index (big-int AND/OR);
  3. sunflower test, method B (independent formulation): for every member A,
     group the other members by their trace B&A; inside a trace class the
     residuals B\\A must be pairwise intersecting (a disjoint pair B, C in
     the class means A&B == A&C == B&C == trace);
  4. method C (literal definition on Python frozensets, all triples), run when
     the family is small enough (C(N,3) <= --brute-limit);
  5. exact rate comparison with integers only:
       |F| * 10^(4n) > 15545^n        (the 1.5545 success bar)
     plus the same comparison for 1.551 and 1.554, and the exact smallest size
     that clears 1.5545 at this n.

Exit status 0 = structurally valid and sunflower-free under every method run.
"""
import argparse
import itertools
import json
import sys
import time


def iroot_floor(x, k):
    """floor(x ** (1/k)) for integers x >= 0, k >= 1, exactly."""
    if x < 2:
        return x
    lo, hi = 1, 1 << ((x.bit_length() + k - 1) // k + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** k <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def popcount(x):
    return bin(x).count("1")


def load(path):
    with open(path) as fh:
        data = json.load(fh)
    return data


def structural_check(data):
    errs = []
    n = data.get("n")
    r = data.get("r")
    sets = data.get("sets")
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        errs.append("n must be a positive integer")
        return errs, None
    if not isinstance(r, int) or isinstance(r, bool) or r < 0 or r > n:
        errs.append("r must be an integer with 0 <= r <= n")
        return errs, None
    if not isinstance(sets, list):
        errs.append("sets must be a list")
        return errs, None
    allel = []
    for idx, s in enumerate(sets):
        if not isinstance(s, list):
            errs.append("member %d is not a list" % idx)
            continue
        for e in s:
            if not isinstance(e, int) or isinstance(e, bool):
                errs.append("member %d has a non-integer element %r" % (idx, e))
        allel.extend(e for e in s if isinstance(e, int) and not isinstance(e, bool))
        if len(set(s)) != len(s):
            errs.append("member %d repeats an element" % idx)
        if len(set(s)) != r:
            errs.append("member %d has size %d, not r=%d" % (idx, len(set(s)), r))
    if errs:
        return errs, None
    if allel:
        lo, hi = min(allel), max(allel)
    else:
        lo, hi = 1, 1
    if lo >= 1 and hi <= n:
        base = 1
    elif lo >= 0 and hi <= n - 1:
        base = 0
    else:
        errs.append("elements span %d..%d, not inside 1..%d or 0..%d" % (lo, hi, n, n - 1))
        return errs, None
    fsets = [frozenset(s) for s in sets]
    if len(set(fsets)) != len(fsets):
        seen = {}
        for idx, fs in enumerate(fsets):
            if fs in seen:
                errs.append("members %d and %d are equal" % (seen[fs], idx))
                if len(errs) > 5:
                    break
            else:
                seen[fs] = idx
        return errs, None
    masks = []
    for s in sets:
        m = 0
        for e in s:
            m |= 1 << (e - base)
        masks.append(m)
    return errs, {"n": n, "r": r, "base": base, "masks": masks, "fsets": fsets}


def method_a(n, masks):
    """Pairs + column bitsets.  Returns a sunflower triple of indices or None."""
    N = len(masks)
    col = [0] * n
    for idx, m in enumerate(masks):
        p = 0
        mm = m
        while mm:
            if mm & 1:
                col[p] |= 1 << idx
            mm >>= 1
            p += 1
    allmask = (1 << N) - 1
    bits = [[p for p in range(n) if (m >> p) & 1] for m in masks]
    for i in range(N):
        ai = masks[i]
        for j in range(i + 1, N):
            aj = masks[j]
            k = ai & aj
            d = ai ^ aj
            cand = allmask
            kk = k
            p = 0
            while kk:
                if kk & 1:
                    cand &= col[p]
                kk >>= 1
                p += 1
            if not cand:
                continue
            dd = d
            p = 0
            while dd and cand:
                if dd & 1:
                    cand &= ~col[p]
                dd >>= 1
                p += 1
            if cand:
                c = (cand & -cand).bit_length() - 1
                return (i, j, c)
    return None


def method_b(n, r, masks):
    """Per-member trace classes; residuals within a class must pairwise meet."""
    N = len(masks)
    for i in range(N):
        a = masks[i]
        classes = {}
        for j in range(N):
            if j == i:
                continue
            b = masks[j]
            classes.setdefault(b & a, []).append(j)
        for trace, members in classes.items():
            if len(members) < 2:
                continue
            res = [masks[j] & ~a for j in members]
            s = r - popcount(trace)
            if 2 * s > n - r:
                continue  # two s-subsets of an (n-r)-set must meet (pigeonhole)
            L = len(res)
            for x in range(L):
                rx = res[x]
                for y in range(x + 1, L):
                    if rx & res[y] == 0:
                        return (i, members[x], members[y])
    return None


def method_c(fsets):
    """Literal definition on frozensets over all triples."""
    N = len(fsets)
    for i, j, k in itertools.combinations(range(N), 3):
        a, b, c = fsets[i], fsets[j], fsets[k]
        ab = a & b
        if ab == (a & c) and ab == (b & c):
            return (i, j, k)
    return None


def is_sunflower(fs3):
    a, b, c = fs3
    return len({a, b, c}) == 3 and (a & b) == (a & c) == (b & c)


def rate_report(N, n):
    out = {}
    out["size"] = N
    out["n"] = n
    out["beats_1.5545"] = N * 10 ** (4 * n) > 15545 ** n
    out["beats_1.554"] = N * 1000 ** n > 1554 ** n
    out["beats_1.551"] = N * 1000 ** n > 1551 ** n
    out["min_size_to_beat_1.5545"] = 15545 ** n // 10 ** (4 * n) + 1
    out["min_size_to_beat_1.554"] = 1554 ** n // 1000 ** n + 1
    out["min_size_to_beat_1.551"] = 1551 ** n // 1000 ** n + 1
    digits = 10
    fl = iroot_floor(N * 10 ** (digits * n), n)  # floor(N^(1/n) * 10^digits)
    out["rate_floor_10dp"] = "%d.%0*d" % (fl // 10 ** digits, digits, fl % 10 ** digits)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("family", help="JSON file with n, r, sets")
    ap.add_argument("--brute-limit", type=int, default=3 * 10 ** 7,
                    help="run method C when C(N,3) is at most this (default 3e7)")
    ap.add_argument("--skip", default="", help="comma list of methods to skip (A,B,C)")
    args = ap.parse_args()
    skip = set(x.strip().upper() for x in args.skip.split(",") if x.strip())
    data = load(args.family)
    errs, fam = structural_check(data)
    report = {"file": args.family}
    if errs:
        report["structure"] = "FAIL"
        report["errors"] = errs[:20]
        print(json.dumps(report, indent=1))
        return 1
    n, r, masks, fsets = fam["n"], fam["r"], fam["masks"], fam["fsets"]
    N = len(masks)
    report["structure"] = "PASS (n=%d, r=%d, N=%d distinct %d-sets, labels %d-based)" % (n, r, N, r, fam["base"])
    ok = True
    for name, fn in (("A", lambda: method_a(n, masks)), ("B", lambda: method_b(n, r, masks)),
                     ("C", lambda: method_c(fsets))):
        if name in skip:
            report["method_" + name] = "SKIPPED (by request)"
            continue
        if name == "C":
            ntrip = N * (N - 1) * (N - 2) // 6
            if ntrip > args.brute_limit:
                report["method_C"] = "SKIPPED (C(N,3)=%d > brute limit %d)" % (ntrip, args.brute_limit)
                continue
        t0 = time.time()
        res = fn()
        dt = time.time() - t0
        if res is None:
            report["method_" + name] = "PASS: no sunflower (%.2fs)" % dt
        else:
            trip = [sorted(x + fam["base"] for x in range(n) if (masks[t] >> x) & 1) for t in res]
            confirm = is_sunflower(tuple(fsets[t] for t in res))
            report["method_" + name] = "FAIL: sunflower at members %s = %s (literal re-check: %s) (%.2fs)" % (
                list(res), trip, "sunflower" if confirm else "NOT a sunflower -- checker bug", dt)
            ok = False
    report["rate"] = rate_report(N, n)
    report["verdict"] = ("SUNFLOWER-FREE" if ok else "HAS A SUNFLOWER") + (
        "; clears 1.5545 bar" if ok and report["rate"]["beats_1.5545"] else "; does not clear 1.5545 bar")
    print(json.dumps(report, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
