#!/bin/sh
# Standalone check for object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt. Run from the package folder: sh verify-it-yourself/run_checks.sh
# Checks (1) the object's sha256 against INDEX.csv, (2) the exact determinant by Bareiss and by a multi-prime CRT, and the Barba bound with check_maxdet.py (Python standard library),
# and (3) that a corrupted copy of the object is rejected. Last line: ALL CHECKS PASS, or FAIL.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt"
CHK="$HERE/verify-it-yourself/check_maxdet.py"
fail=0
if [ ! -f "$OBJ" ]; then echo "FAIL missing object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt"; exit 1; fi
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_maxdet.py on object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt"
python3 "$CHK" "$OBJ" --expect-norm 2119202655125403624550373680790052808829003860176536932438843923020304438454497 || fail=1
echo "== negative control: a corrupted copy must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
awk 'NR==1{ $1 = -$1 } { print }' "$OBJ" > "$TMP/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt" 
if python3 "$CHK" "$TMP/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt" --expect-norm 2119202655125403624550373680790052808829003860176536932438843923020304438454497 >"$TMP/neg.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected ($(tail -n 1 "$TMP/neg.txt"))"; fi
rm -f "$TMP/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
