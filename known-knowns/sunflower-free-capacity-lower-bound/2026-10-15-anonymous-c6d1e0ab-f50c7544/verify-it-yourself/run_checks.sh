#!/bin/sh
# Standalone check for g(8,3) = 12. Run from this folder: sh verify-it-yourself/run_checks.sh
# Needs: python3 (3.8+, standard library), a C compiler (cc). Optional: python-sat (pip install python-sat) to regenerate the CNF.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
V="$HERE/verify-it-yourself"
FAM="$HERE/object/family_g8_3_12.json"
CNF="$HERE/object/sb.cnf"
PLAIN="$HERE/object/nosb.cnf"
PRF="$HERE/object/sb.drup"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
echo "== 1. object hashes against INDEX.csv"
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$FAM" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "family sha256 matches INDEX.csv"; else echo "family sha256 MISMATCH"; fail=1; fi
echo "== 2. the family: 12 distinct 3-subsets of [8], no three with pairwise equal intersections (check_family.py, three methods)"
python3 "$V/check_family.py" "$FAM" > "$V/.fam.txt" 2>&1; rc=$?; cat "$V/.fam.txt" | tail -n 6
if [ "$rc" -eq 0 ] && grep -q "12" "$V/.fam.txt"; then echo "family check PASS"; else echo "family check FAIL (exit $rc)"; fail=1; fi
echo "== 3. the CNF header states n=8, r=3, |F| >= 13"
head -n 1 "$PLAIN"
if head -n 1 "$PLAIN" | grep -q "C(\\[8\\],3), |F| >= 13"; then echo "header PASS"; else echo "header FAIL"; fail=1; fi
echo "== 4. the CNF's ternary clauses are exactly the 3-sunflowers of C([8],3), recomputed by brute force from the definition (triples_recheck.py)"
python3 "$V/triples_recheck.py" "$PLAIN" | tail -n 3 | tee "$V/.tri.txt"
if grep -q "^MATCH" "$V/.tri.txt" || grep -q " MATCH" "$V/.tri.txt"; then echo "sunflower clauses PASS"; else echo "sunflower clauses FAIL"; fail=1; fi
echo "== 5. the cardinality clauses encode |F| >= 13 (stdlib check: every assignment with exactly 13 chosen sets found by sampling satisfies them, and 12 chosen sets never does; card_check.py)"
python3 "$V/card_check.py" "$PLAIN" 13 | tail -n 3 | tee "$V/.card.txt"
if grep -q "^CARD OK" "$V/.card.txt"; then echo "cardinality PASS"; else echo "cardinality FAIL"; fail=1; fi
echo "== 5b. the proved CNF contains every clause of the plain CNF (its extra clauses are the lex-leader symmetry-breaking constraints; subset_check.py)"
python3 "$V/subset_check.py" "$PLAIN" "$CNF" | tee "$V/.sub.txt"
if grep -q "^SUBSET OK" "$V/.sub.txt"; then echo "subset PASS"; else echo "subset FAIL"; fail=1; fi
echo "== 6. regenerate the CNF with the shipped generator (needs python-sat; skipped if absent)"
if python3 -c "import pysat" 2>/dev/null; then
  python3 "$V/gen_cnf.py" 8 3 13 "$V/.regen.cnf" --sb alltrans >/dev/null 2>&1
  python3 -c "import sys; a=[l for l in open(sys.argv[1]) if not l.startswith('c sunflower-free')]; b=[l for l in open(sys.argv[2]) if not l.startswith('c sunflower-free')]; sys.exit(0 if a==b else 1)" "$CNF" "$V/.regen.cnf" && echo "regenerated CNF identical in every variable and clause (the first comment line may differ: newer generator versions append the degree-cut setting to it)" || { echo "regenerated CNF DIFFERS in clauses or variable map"; fail=1; }
  rm -f "$V/.regen.cnf"
else
  echo "python-sat not installed: regeneration skipped (pip install python-sat, then rerun); steps 4 and 5 check the clauses directly"
fi
echo "== 7. the UNSAT proof: compile drat-trim (Heule, Wetzler) and check sb.drup against sb.cnf"
cc -O2 -o "$V/.drat-trim" "$V/drat-trim.c" 2>/dev/null || { echo "cc failed"; fail=1; }
"$V/.drat-trim" "$CNF" "$PRF" -f > "$V/.drat.txt" 2>&1; tail -n 2 "$V/.drat.txt"
if grep -q "s VERIFIED" "$V/.drat.txt"; then echo "proof VERIFIED"; else echo "proof NOT verified"; fail=1; fi
echo "== 8. negative controls"
head -c $(( $(wc -c < "$PRF") / 2 )) "$PRF" > "$V/.half.drup"
"$V/.drat-trim" "$CNF" "$V/.half.drup" -f > "$V/.drat2.txt" 2>&1
if grep -q "s VERIFIED" "$V/.drat2.txt"; then echo "truncated proof NOT rejected"; fail=1; else echo "truncated proof rejected as expected"; fi
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); d['sets'].append(list(d['sets'][0])); json.dump(d,open(sys.argv[2],'w'))" "$FAM" "$V/.bad.json"
python3 "$V/check_family.py" "$V/.bad.json" >/dev/null 2>&1 && { echo "bad family NOT rejected"; fail=1; } || echo "bad family (a repeated member) rejected as expected"
rm -f "$V/.fam.txt" "$V/.tri.txt" "$V/.card.txt" "$V/.sub.txt" "$V/.drat.txt" "$V/.drat2.txt" "$V/.half.drup" "$V/.bad.json" "$V/.drat-trim"
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
