#!/bin/sh
# Standalone check for object/code_q2_n175_k25_d61.json. Run from the package folder: sh verify-it-yourself/run_checks.sh
# Checks (1) the object's sha256 against INDEX.csv, (2) rank 25 over GF(2) and the exact minimum distance 61 by two
# full enumerations of all 33,554,431 nonzero codewords with check_code.py (Python standard library), and (3) that a
# corrupted copy of the object (row 0 replaced by the sum of rows 1 and 2, so rank 24) is rejected.
# Last line: ALL CHECKS PASS, or FAIL.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/code_q2_n175_k25_d61.json"
CHK="$HERE/verify-it-yourself/check_code.py"
fail=0
if [ ! -f "$OBJ" ]; then echo "FAIL missing object/code_q2_n175_k25_d61.json"; exit 1; fi
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_code.py on object/code_q2_n175_k25_d61.json"
python3 "$CHK" "$OBJ" --expect-d 61 || fail=1
echo "== negative control: a rank-deficient copy must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); G=d['G']; G[0]=[a^b for a,b in zip(G[1],G[2])]; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
if python3 "$CHK" "$TMP/neg.json" --expect-d 61 >"$TMP/neg.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected ($(tail -n 1 "$TMP/neg.txt"))"; fi
rm -f "$TMP/neg.json" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
