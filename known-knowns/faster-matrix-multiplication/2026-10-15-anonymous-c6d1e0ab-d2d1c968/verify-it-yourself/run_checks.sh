#!/bin/sh
# Standalone check for object/11x13x16_r1445_Q.json. Run from this folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/11x13x16_r1445_Q.json"
CHK="$HERE/verify-it-yourself/check_fmm.py"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_fmm.py on object/11x13x16_r1445_Q.json"
python3 "$CHK" "$OBJ" --expect-rank 1445 || fail=1
echo "== negative control: a copy with one coefficient changed must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); r=d['u'][0]; r[1]=(r[1]+1) if isinstance(r[1],int) else 2; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
if python3 "$CHK" "$TMP/neg.json" --expect-rank 1445 >"$TMP/neg.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected ($(tail -n 1 "$TMP/neg.txt"))"; fi
rm -f "$TMP/neg.json" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
