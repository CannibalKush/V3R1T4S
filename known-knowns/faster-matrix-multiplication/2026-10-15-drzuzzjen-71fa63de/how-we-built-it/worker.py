#!/usr/bin/env python3
"""One worker job: improve the SLP of one scheme with a given lens until the deadline.

usage: worker.py --lens LENS --file SCHEME.json --ref REFCOUNT --eligibility data_eligibility.md
                 --deadline EPOCH --out DIR [--seed S]
--ref must equal the 'perminov min cr' of the file's format+rank in the eligibility table and that row must be
eligible (rank == fmm_sota rank); otherwise the worker refuses to start (exit 2).
Writes DIR/<jobname>.ckpt.json (atomic) and, whenever a full scheme strictly below REF is produced AND passes
tools/fmm_check.py (independent of the generator), DIR/candidates/<format>_m<r>_cr<N>_ref<REF>_<lens>_s<seed>_<t>.json.
"""
import argparse, json, os, re, sys, time, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fmm_check as F
import lens_ops


def eligibility_row(path, fmt, rank):
    for line in open(path, encoding="utf-8"):
        p = [x.strip() for x in line.split("|")]
        if len(p) > 6 and p[1] == fmt and p[2].isdigit() and int(p[2]) == rank:
            return {"eligible": p[4] == "yes", "min_cr": int(p[5])}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lens", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--ref", type=int, required=True)
    ap.add_argument("--eligibility", required=True)
    ap.add_argument("--deadline", type=float, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    m = re.match(r"(\d+x\d+x\d+)_m(\d+)_", os.path.basename(a.file))
    row = eligibility_row(a.eligibility, m.group(1), int(m.group(2))) if m else None
    if not row or not row["eligible"] or row["min_cr"] != a.ref:
        print("refusing: file %s eligibility row %r does not match --ref %d" % (a.file, row, a.ref), file=sys.stderr)
        sys.exit(2)
    # cells already beaten upstream (written by tools/claim_watch.py): do not spend CPU on them
    run_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(a.out))))
    skip = os.path.join(run_dir, "SKIP_FORMATS")
    if m and os.path.exists(skip) and m.group(1) in open(skip, encoding="utf-8").read().split():
        print("skipping %s: listed in SKIP_FORMATS (beaten upstream)" % m.group(1), file=sys.stderr)
        sys.exit(0)
    os.makedirs(os.path.join(a.out, "candidates"), exist_ok=True)
    rng = random.Random(a.seed)
    name = "%s_%s_s%d" % (os.path.basename(a.file).split("_ZT")[0], a.lens, a.seed)
    ck = os.path.join(a.out, name + ".ckpt.json")
    state = {"lens": a.lens, "file": os.path.basename(a.file), "ref": a.ref, "seed": a.seed, "pid": os.getpid(),
             "started": time.time(), "deadline": a.deadline, "best_total": None, "best_maps": None,
             "candidates": 0, "rejected_invalid": 0, "yielded": 0, "updated": time.time(), "error": None}

    def save():
        state["updated"] = time.time()
        tmp = ck + ".tmp"
        with open(tmp, "w") as f:
            json.dump(state, f)
        os.replace(tmp, ck)

    save()
    fn = getattr(lens_ops, "lens_" + a.lens.replace("-", "_"))
    try:
        for scheme, total in fn(a.file, rng, a.deadline, state, save):
            state["yielded"] += 1
            # every yielded scheme is re-verified independently of the generator
            try:
                r = F.check(scheme)
            except Exception as e:  # malformed object: count it, never crash the job
                r = {"valid_ternary_slp": False, "error": repr(e)}
            if not r.get("valid_ternary_slp"):
                state["rejected_invalid"] += 1
                state["last_rejection"] = r.get("error") or "invalid"
                save()
                continue
            if state["best_total"] is None or r["reduced_additions"] < state["best_total"]:
                state["best_total"] = r["reduced_additions"]
                state["best_maps"] = [r["adds_U"], r["adds_V"], r["adds_W"]]
                save()
            if r["reduced_additions"] < a.ref:
                state["candidates"] += 1
                p = os.path.join(a.out, "candidates", "%s_m%d_cr%d_ref%d_%s_s%d_%d.json" % (
                    r["format"], r["rank"], r["reduced_additions"], a.ref, a.lens, a.seed, int(time.time())))
                with open(p, "w") as f:
                    json.dump(scheme, f)
                save()
    except Exception as e:
        state["error"] = repr(e)
    state["finished"] = time.time()
    save()


if __name__ == "__main__":
    main()
