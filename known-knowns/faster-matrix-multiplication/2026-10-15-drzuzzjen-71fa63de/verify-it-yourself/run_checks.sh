#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
PY=""
for c in python3 python; do
  if "$c" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then PY="$c"; break; fi
done
[ -z "$PY" ] && { echo "no working python3/python found"; echo FAIL; exit 1; }
OUT=$("$PY" -I verify-it-yourself/indep_check.py object/5x5x5_m93_cr358_ZT_reduced.json) || true
echo "$OUT"
echo "$OUT" | "$PY" -I -c '
import json, sys
r = json.loads(sys.stdin.read().strip().splitlines()[-1])
ok = (r.get("pass") is True and r.get("format") == "5x5x5" and r.get("rank") == 93 and r.get("total") == 358
      and r.get("tensor_CT_mismatches") == 0 and r.get("random_fail_CT") == 0)
print("format %s rank %s additions %s exact %s" % (r.get("format"), r.get("rank"), r.get("total"), r.get("tensor_CT_mismatches") == 0))
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
'
