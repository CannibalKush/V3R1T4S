#!/usr/bin/env python3
"""Re-verify the whole exact-values candidate from a clean copy (standard library + a C compiler).

Usage: verify_all.py [candidate_root] [--no-regen] [--pysat PYTHON]
  PYTHON with python-sat is needed only to regenerate the CNFs (--pysat, default: $PYSAT or python3).
Steps, all outputs under {root}/verify_out/:
  1. compile tools/drat-trim.c, tools/drup_check2.c, tools/sfcheck.c into verify_out/bin/
  2. every family.json (opus_packages/ and chain_rows/): tools/check_family.py (three methods) and sfcheck
  3. every proof variant: its ternary clauses are recomputed from the definition by brute force over
     all triples of r-sets (tools/triples_recheck.py); drat-trim and drup_check2 must both print 's VERIFIED'
  4. every CNF regenerated with tools/gen_cnf.py from (n, r, k, sb, deg) in its header and compared byte-for-byte
  4b. case-split packages (ARGUMENT.md + cases/): brute-force clause recheck, drat-trim and drup_check2 on every
     case proof and classification-completeness proof; the package's regenerate.sh must rebuild every CNF identical
  5. negative controls (truncated proof, foreign proof, a family with a sunflower) must be rejected
  6. second method: tools/exact_bb.py exhaustive maxima for (7,3), (7,4), (8,3) (--bb-all adds (9,3), (8,4))
  7. tools/chain_check.py and tools/build_index.py --check
Prints one line per check and a final PASS/FAIL; exit 0 iff everything passed.  Runs single-threaded.
"""
import os
import re
import subprocess
import sys
import time


def sh(cmd, out, timeout=7200):
    with open(out, "w") as fh:
        try:
            p = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, timeout=timeout)
            return p.returncode
        except subprocess.TimeoutExpired:
            fh.write("\nTIMEOUT\n")
            return "timeout"


def has_verified(path):
    return "s VERIFIED" in open(path, errors="replace").read().replace("\r", "\n")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    regen = "--no-regen" not in sys.argv
    pysat = os.environ.get("PYSAT", sys.executable)
    if "--pysat" in sys.argv:
        pysat = sys.argv[sys.argv.index("--pysat") + 1]
        args = [a for a in args if a != pysat]
    root = os.path.abspath(args[0]) if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tools = os.path.join(root, "tools")
    out = os.path.join(root, "verify_out")
    bin_ = os.path.join(out, "bin")
    os.makedirs(bin_, exist_ok=True)
    results = []
    t0 = time.time()

    def rec(name, ok, extra=""):
        results.append((name, bool(ok)))
        print("%-70s %s %s" % (name, "PASS" if ok else "FAIL", extra), flush=True)

    for src, exe in (("drat-trim.c", "drat-trim"), ("drup_check2.c", "drup_check2"), ("sfcheck.c", "sfcheck")):
        rc = sh(["cc", "-O2", "-o", os.path.join(bin_, exe), os.path.join(tools, src)], os.path.join(out, exe + ".build.txt"))
        rec("compile " + src, rc == 0)
    dt, dc, sf = (os.path.join(bin_, x) for x in ("drat-trim", "drup_check2", "sfcheck"))
    dirs = []
    for sub in ("opus_packages", "chain_rows"):
        for d in sorted(os.listdir(os.path.join(root, sub))):
            if os.path.isdir(os.path.join(root, sub, d)):
                dirs.append((sub, d))
    for sub, d in dirs:
        pd = os.path.join(root, sub, d)
        fam = os.path.join(pd, "family.json")
        o1 = os.path.join(out, "%s__family_check.txt" % d)
        rc = sh([sys.executable, os.path.join(tools, "check_family.py"), fam], o1)
        txt = open(o1).read()
        rec("%s family check_family.py (A,B,C)" % d, rc == 0 and '"verdict": "SUNFLOWER-FREE' in txt)
        o2 = os.path.join(out, "%s__sfcheck.txt" % d)
        rc = sh([sf, fam], o2)
        rec("%s family sfcheck" % d, rc == 0 and "PASS" in open(o2).read())
        for f in sorted(os.listdir(pd)):
            if not f.endswith(".cnf") or f.endswith(".regen.cnf"):
                continue
            var = f[:-4]
            cnf, drup = os.path.join(pd, f), os.path.join(pd, var + ".drup")
            if not os.path.exists(drup):
                rec("%s/%s proof present" % (d, var), False)
                continue
            o = os.path.join(out, "%s__%s_triples.txt" % (d, var))
            rc = sh([sys.executable, os.path.join(tools, "triples_recheck.py"), cnf], o)
            rec("%s/%s sunflower clauses = brute-force triples" % (d, var), rc == 0 and "MATCH" in open(o).read())
            o = os.path.join(out, "%s__%s_drat_trim.txt" % (d, var))
            t = time.time()
            rc = sh([dt, cnf, drup], o)
            rec("%s/%s drat-trim" % (d, var), has_verified(o), "%.1fs" % (time.time() - t))
            o = os.path.join(out, "%s__%s_drup_check2.txt" % (d, var))
            t = time.time()
            rc = sh([dc, cnf, drup], o)
            rec("%s/%s drup_check2" % (d, var), has_verified(o), "%.1fs" % (time.time() - t))
            if regen:
                h = open(cnf).readline()
                m = re.search(r"C\(\[(\d+)\],(\d+)\), \|F\| >= (\d+); .*sb=(\w+)", h)
                dm = re.search(r"deg<=(\d+)", h)
                cmd = [pysat, os.path.join(tools, "gen_cnf.py"), m.group(1), m.group(2), m.group(3),
                       os.path.join(out, "%s__%s.regen.cnf" % (d, var)), "--sb", m.group(4)]
                if dm:
                    cmd += ["--deg", dm.group(1)]
                o = os.path.join(out, "%s__%s_regen.txt" % (d, var))
                rc = sh(cmd, o)
                a, b = open(cnf, "rb").read(), open(cmd[5], "rb").read() if rc == 0 else b""
                same = rc == 0 and a == b
                # CNFs generated before the --deg option have no 'deg<=none' field in their first comment
                # line; the clause body (everything after the first line) must still be byte-identical.
                body_same = rc == 0 and a.split(b"\n", 1)[1] == b.split(b"\n", 1)[1] and \
                    a.split(b"\n", 1)[0].rstrip(b" ") + b"; deg<=none" == b.split(b"\n", 1)[0]
                rec("%s/%s CNF regenerated byte-identical" % (d, var), same or body_same,
                    "" if same else ("(header comment differs only by the field 'deg<=none'; clauses identical)" if body_same else ""))
                if same or body_same:
                    os.remove(cmd[5])
    # case-split packages (ARGUMENT.md + cases/): every case proof and every classification completeness proof
    for sub, d in dirs:
        pd = os.path.join(root, sub, d)
        cdir = os.path.join(pd, "cases")
        if not (os.path.isdir(cdir) and os.path.exists(os.path.join(pd, "ARGUMENT.md"))):
            continue
        todo = [os.path.join(cdir, f) for f in sorted(os.listdir(cdir)) if f.endswith(".cnf") and not f.startswith("base")]
        cl = os.path.join(pd, "classify")
        if os.path.isdir(cl):
            todo += [os.path.join(cl, f) for f in sorted(os.listdir(cl)) if f.endswith("_complete.cnf")]
        for cnf in todo:
            var = os.path.basename(cnf)[:-4]
            drup = cnf[:-4] + ".drup"
            tmp_gz = None
            if not os.path.exists(drup) and os.path.exists(drup + ".gz"):
                import gzip, shutil
                tmp_gz = os.path.join(out, "%s__%s.drup" % (d, var))
                with gzip.open(drup + ".gz", "rb") as fi, open(tmp_gz, "wb") as fo:
                    shutil.copyfileobj(fi, fo)
                drup = tmp_gz
            if not os.path.exists(drup):
                rec("%s/%s proof present" % (d, var), False)
                continue
            if "/cases/" in cnf:
                o = os.path.join(out, "%s__%s_triples.txt" % (d, var))
                rc = sh([sys.executable, os.path.join(tools, "triples_recheck.py"), cnf], o)
                rec("%s/%s sunflower clauses = brute-force triples" % (d, var), rc == 0 and "MATCH" in open(o).read())
            o = os.path.join(out, "%s__%s_drat_trim.txt" % (d, var))
            t = time.time()
            sh([dt, cnf, drup], o)
            rec("%s/%s drat-trim" % (d, var), has_verified(o), "%.1fs" % (time.time() - t))
            o = os.path.join(out, "%s__%s_drup_check2.txt" % (d, var))
            t = time.time()
            sh([dc, cnf, drup], o)
            rec("%s/%s drup_check2" % (d, var), has_verified(o), "%.1fs" % (time.time() - t))
            if tmp_gz:
                os.remove(tmp_gz)
        if regen and os.path.exists(os.path.join(pd, "regenerate.sh")):
            o = os.path.join(out, "%s__regenerate.txt" % d)
            env = dict(os.environ)
            t = time.time()
            with open(o, "w") as fh:
                try:
                    p_ = subprocess.run(["zsh", "./regenerate.sh"], cwd=pd, stdout=fh, stderr=subprocess.STDOUT, timeout=3600, env=env)
                except subprocess.TimeoutExpired:
                    fh.write("TIMEOUT\n")
            txt = open(o).read()
            nid = txt.count("identical")
            ncnf = len([f for f in os.listdir(cdir) if f.endswith(".cnf")]) + (len([f for f in os.listdir(cl) if f.endswith(".cnf")]) if os.path.isdir(cl) else 0)
            rec("%s regenerate.sh: all %d CNFs rebuilt identical" % (d, ncnf), nid == ncnf, "%.0fs (%d identical)" % (time.time() - t, nid))
            rg = os.path.join(pd, "regen")
            if os.path.isdir(rg):
                for f in os.listdir(rg):
                    os.remove(os.path.join(rg, f))
                os.rmdir(rg)
    # negative controls: the verifiers must reject a truncated proof, a proof of another formula,
    # and the family checker must reject a family containing a sunflower
    ctl = os.path.join(root, "opus_packages", "g_7_3_12")
    cnf, drup = os.path.join(ctl, "sb.cnf"), os.path.join(ctl, "sb.drup")
    if os.path.exists(cnf) and os.path.exists(drup):
        lines = open(drup).read().splitlines()
        trunc = os.path.join(out, "control_truncated.drup")
        open(trunc, "w").write("\n".join(lines[: len(lines) // 2]) + "\n")
        o = os.path.join(out, "control_truncated_drat_trim.txt")
        sh([dt, cnf, trunc], o)
        rec("control: drat-trim rejects truncated proof", not has_verified(o))
        o = os.path.join(out, "control_truncated_drup_check2.txt")
        sh([dc, cnf, trunc], o)
        rec("control: drup_check2 rejects truncated proof", not has_verified(o))
        other = os.path.join(root, "opus_packages", "g_7_4_15", "sb.drup")
        if os.path.exists(other):
            o = os.path.join(out, "control_foreign_drat_trim.txt")
            sh([dt, cnf, other], o)
            rec("control: drat-trim rejects proof of another formula", not has_verified(o))
            o = os.path.join(out, "control_foreign_drup_check2.txt")
            sh([dc, cnf, other], o)
            rec("control: drup_check2 rejects proof of another formula", not has_verified(o))
    bad = os.path.join(out, "control_sunflower_family.json")
    open(bad, "w").write('{"n": 9, "r": 3, "sets": [[1,2,3],[4,5,6],[7,8,9],[1,2,4]]}')
    o = os.path.join(out, "control_sunflower_family_check.txt")
    rc = sh([sys.executable, os.path.join(tools, "check_family.py"), bad], o)
    rec("control: check_family.py rejects three disjoint sets", rc != 0 and "SUNFLOWER-FREE" not in open(o).read())
    o = os.path.join(out, "control_sunflower_family_sfcheck.txt")
    rc = sh([sf, bad], o)
    rec("control: sfcheck rejects three disjoint sets", rc != 0 or "FAIL" in open(o).read())
    # second method: exhaustive branch-and-bound from the definition (fast cases by default)
    cases = [(7, 3, 12), (7, 4, 15), (8, 3, 12)] + ([(9, 3, 14), (8, 4, 24)] if "--bb-all" in sys.argv else [])
    for n, r, v in cases:
        o = os.path.join(out, "bb_%d_%d.txt" % (n, r))
        t = time.time()
        rc = sh([sys.executable, os.path.join(tools, "exact_bb.py"), str(n), str(r)], o)
        txt = open(o).read()
        rec("second method exact_bb.py (%d,%d) max = %d" % (n, r, v), rc == 0 and ("'max': %d," % v) in txt, "%.1fs" % (time.time() - t))
    o = os.path.join(out, "chain_check.txt")
    rc = sh([sys.executable, os.path.join(tools, "chain_check.py"), root], o)
    rec("chain_check.py", rc == 0 and "CHAIN CHECK PASS" in open(o).read())
    o = os.path.join(out, "build_index.txt")
    rc = sh([sys.executable, os.path.join(tools, "build_index.py"), root, "--check"], o)
    rec("build_index.py --check", rc == 0)
    nfail = sum(1 for _, ok in results if not ok)
    print("TOTAL %d checks, %d failed, %.0f s -> %s" % (len(results), nfail, time.time() - t0, "PASS" if nfail == 0 else "FAIL"))
    with open(os.path.join(out, "SUMMARY.txt"), "w") as fh:
        for name, ok in results:
            fh.write("%s %s\n" % ("PASS" if ok else "FAIL", name))
        fh.write("TOTAL %d checks, %d failed\n" % (len(results), nfail))
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
