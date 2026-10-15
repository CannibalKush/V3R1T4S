#!/bin/sh
# Standalone verification script for object/13x15x15_r1763_Q.json.
# Verifies: (1) SHA-256 against INDEX.csv, (2) exact Brent equations over Q via CRT,
# (3) claimed rank 1763, and (4) negative control rejection on a mutated copy.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/13x15x15_r1763_Q.json"
CHK="$HERE/verify-it-yourself/verify_brent.py"

if [ ! -f "$OBJ" ]; then
  echo "FAIL missing object/13x15x15_r1763_Q.json"
  exit 1
fi

if command -v sha256sum >/dev/null 2>&1; then
  SHA="sha256sum"
else
  SHA="shasum -a 256"
fi

fail=0
echo "== Checking object/13x15x15_r1763_Q.json"
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | cut -d, -f7)
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then
  echo "sha256 matches INDEX.csv ($got_sha)"
else
  echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"
  fail=1
fi

exp_rank=$(tail -n 1 "$HERE/INDEX.csv" | cut -d, -f3)
out=$(python3 "$CHK" "$OBJ") || fail=1
echo "$out"
echo "$out" | tail -n 1 | grep -q "rank=$exp_rank " && echo "rank $exp_rank matches INDEX.csv" || {
  echo "RANK MISMATCH (expected $exp_rank)"
  fail=1
}

echo "== Running negative control (mutated coefficient must FAIL)"
neg_ok=$(python3 -c '
import json, os, subprocess, sys, tempfile
obj_path, chk_path = sys.argv[1], sys.argv[2]
with open(obj_path, "r", encoding="utf-8") as f:
    d = json.load(f)
d["u"][0][1] = int(d["u"][0][1]) + 1
with tempfile.TemporaryDirectory(prefix="neg_ctrl_") as tmp:
    neg_path = os.path.join(tmp, "neg.json")
    with open(neg_path, "w", encoding="utf-8") as f:
        json.dump(d, f)
    r = subprocess.run([sys.executable, chk_path, neg_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print("REJECTED" if r.returncode != 0 else "ACCEPTED")
' "$OBJ" "$CHK")

if [ "$neg_ok" = "REJECTED" ]; then
  echo "negative control rejected as expected"
else
  echo "negative control PASSED (BAD)"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASS"
  exit 0
else
  echo "CHECK FAIL"
  exit 1
fi
