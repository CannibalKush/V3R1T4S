#!/usr/bin/env python3
"""parse_sources.py DIR fmt=rank ...  -- read the four criterion sources saved in DIR and print, per format, the
value each source lists and the minimum (the "bar").  Formats are sorted triples, e.g. 14x15x15=1843.
Files expected in DIR (one plain GET each, see RUN_IT_YOURSELF.md):
  fmm_sota.json              https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json
  perminov_README.md         https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md
  merlijn_SHA256SUMS         https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS
  matmulcatalog_COVERAGE.md  https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md
Output: one JSON object.  python3 standard library only.
"""
import json, os, re, sys

def main():
    d = sys.argv[1]
    rd = lambda f: open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
    sota = json.loads(rd("fmm_sota.json")); perm = rd("perminov_README.md")
    merl = rd("merlijn_SHA256SUMS"); cov = rd("matmulcatalog_COVERAGE.md")
    if "## Research Findings" in perm:
        perm = perm[perm.index("## Research Findings"):]
    out = {"fmm_sota_createdAt": sota.get("createdAt"), "formats": {}}
    for a in sys.argv[2:]:
        f, r = a.split("="); fmt = tuple(sorted(int(x) for x in f.split("x"))); n, m, p = fmt; ours = int(r)
        res = {"ours": ours}
        res["fmm_sota"] = next((e["rank"] for e in sota["entries"] if tuple(sorted(e["format"])) == fmt), None)
        row = None
        for line in perm.splitlines()[1:]:
            if line.startswith("## "):
                break
            if re.match(rf"\|\s*`{n}x{m}x{p}`\s*\|", line):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                row = []
                for c in cells[1:4]:
                    mm = re.match(r"\[?(\d+)", c.replace("*", ""))
                    row.append(int(mm.group(1)) if mm else None)
                res["perminov_row_raw"] = line.strip(); break
        res["perminov_ZT_Z_Q"] = row
        best = None
        for mm in re.finditer(r"schemes/(\d+)x(\d+)x(\d+)_m(\d+)_", merl):
            if tuple(sorted(int(x) for x in mm.groups()[:3])) == fmt:
                best = min(best or 10**9, int(mm.group(4)))
        res["merlijn_lowest"] = best
        f2 = rqz = None
        for line in cov.splitlines():
            if line.startswith(f"| `⟨{n},{m},{p}⟩`"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                mm = re.search(r"(\d+)", cells[1].replace("**", "")); f2 = int(mm.group(1)) if mm else None
                mm = re.search(r"(\d+)", cells[2].replace("**", "")); rqz = int(mm.group(1)) if mm else None
                res["matmulcatalog_row_raw"] = line.strip()
        res["matmulcatalog_F2"], res["matmulcatalog_RQZ"] = f2, rqz
        vals = [v for v in [res["fmm_sota"], best, f2, rqz] + (row or []) if isinstance(v, int)]
        res["bar_min_of_four_sources"] = min(vals) if vals else None
        res["strictly_below_bar"] = bool(vals) and ours < min(vals)
        res["margin"] = ours - min(vals) if vals else None
        out["formats"][f"{n}x{m}x{p}"] = res
    print(json.dumps(out, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main()
