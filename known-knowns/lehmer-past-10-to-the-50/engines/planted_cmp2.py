#!/usr/bin/env python3
"""Planted completeness test for lbb2.c: fake-prime variant vs ref_fake.py, many engine settings (dedup by set)."""
import subprocess, sys
from ref_fake import run
HERE = __file__.rsplit('/', 1)[0]

def engine(E, pmin, R, K2, K3, T3, S):
    out = subprocess.run([f"{HERE}/lbb2", "-fake", "-pmin", str(pmin), "-R", str(R), "-X", f"1e{E}", "-K2", str(K2), "-K3", str(K3), "-T3", str(T3), "-S", str(S)],
                         capture_output=True, text=True, check=True).stdout
    sols = set(); tot = None; raw = 0
    for line in out.splitlines():
        if line.startswith("SOLUTION m1"):
            continue   # redundant m1 cross-check: excluded so it cannot mask a failure of the real closures
        if line.startswith("SOLUTION"):
            raw += 1
            left, right = line.split("|")
            pre = left.split("prefix")[1].split()
            r = right.split()
            if "N" in r: r = r[:r.index("N")]
            sols.add(tuple(int(v) for v in pre + r))
        if line.startswith("TOTAL"): tot = line
        if line.startswith("FATAL") or line.startswith("WARN"): print(line)
    return sorted(sols), raw, tot

if __name__ == "__main__":
    ok = True
    cases = [(10, 3, 1), (12, 3, 1), (14, 3, 1), (16, 3, 1), (14, 3, 3), (16, 3, 3), (16, 5, 1)]
    if len(sys.argv) > 1: cases.append((int(sys.argv[1]), 3, 1))
    settings = [(0.0, 0.0, 0), (100.0, 0.0, 0), (0.0, 50.0, 64), (0.1, 0.5, 2), (1.0, 2.0, 4), (100.0, 50.0, 64), (0.01, 0.05, 0)]
    for (E, pmin, R) in cases:
        ref, nodes = run(10 ** E, pmin, R)
        for (K2, K3, T3) in settings:
            if K3 >= 50 and E > 16: continue   # fake_check on huge AP closures is too slow
            got, raw, tot = engine(E, pmin, R, K2, K3, T3, 2_000_000)
            same = got == ref; ok &= same
            print(f"E={E} pmin={pmin} R={R} K2={K2} K3={K3} T3={T3}: ref {len(ref)} engine {len(got)} (raw {raw}) {'MATCH' if same else 'MISMATCH'} | {tot.split(' euler_pass')[0] if tot else ''}", flush=True)
            if not same:
                print("  only ref:", sorted(set(ref) - set(got))[:5]); print("  only engine:", sorted(set(got) - set(ref))[:5])
        print("  ref solutions:", ref, flush=True)
    print("ALL_MATCH" if ok else "SOME_MISMATCH")
