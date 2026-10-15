#!/bin/sh
# Standalone check for object/G_14_3_N1117.edges. Run from the package folder: sh verify-it-yourself/run_checks.sh
# Checks (1) the object's sha256 against INDEX.csv, (2) a simple graph with maximum degree 14 and diameter 3 by breadth-first search from all 1117 vertices with check_dd.py (Python standard library),
# and (3) that a corrupted copy of the object is rejected. Last line: ALL CHECKS PASS, or FAIL.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/G_14_3_N1117.edges"
CHK="$HERE/verify-it-yourself/check_dd.py"
fail=0
if [ ! -f "$OBJ" ]; then echo "FAIL missing object/G_14_3_N1117.edges"; exit 1; fi
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_dd.py on object/G_14_3_N1117.edges"
python3 "$CHK" "$OBJ" --delta 14 --diameter 3 --expect-n 1117 || fail=1
echo "== negative control: a corrupted copy must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
awk '$1 != 0 && $2 != 0' "$OBJ" > "$TMP/G_14_3_N1117.edges" 
if python3 "$CHK" "$TMP/G_14_3_N1117.edges" --delta 14 --diameter 3 --expect-n 1117 >"$TMP/neg.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected ($(tail -n 1 "$TMP/neg.txt"))"; fi
rm -f "$TMP/G_14_3_N1117.edges" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
