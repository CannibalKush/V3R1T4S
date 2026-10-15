# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0; local absolute paths in the output replaced by a placeholder):

```text
== 1. object hashes against INDEX.csv
family sha256 matches INDEX.csv
== 2. the family: 24 distinct 4-subsets of [8], no three with pairwise equal intersections (check_family.py, three methods)
  "min_size_to_beat_1.554": 35,
  "min_size_to_beat_1.551": 34,
  "rate_floor_10dp": "1.4877378261"
 },
 "verdict": "SUNFLOWER-FREE; does not clear 1.5545 bar"
}
family check PASS
== 3. the CNF header states n=8, r=4, |F| >= 25
c sunflower-free F in C([8],4), |F| >= 25; triples=980; sb=none; card=seqcounter; deg<=none
header PASS
== 4. the CNF's ternary clauses are exactly the 3-sunflowers of C([8],4), recomputed by brute force from the definition (triples_recheck.py)
[workspace path] M=70 sets of size [4]; sunflower triples by brute force 980; ternary negative clauses in CNF 980; MATCH
sunflower clauses PASS
== 5. the cardinality clauses encode |F| >= 25 (stdlib check: every assignment with exactly 25 chosen sets found by sampling satisfies them, and 24 chosen sets never does; card_check.py)
M=70 sunflower_clauses=980 cardinality_clauses=2230 aux_vars=1125
CARD OK
cardinality PASS
== 5b. the proved CNF contains every clause of the plain CNF (its extra clauses are the lex-leader symmetry-breaking constraints; subset_check.py)
plain clauses 3210, proved clauses 6514, extra in proved 3304, var maps equal True
SUBSET OK
subset PASS
== 6. regenerate the CNF with the shipped generator (needs python-sat; skipped if absent)
python-sat not installed: regeneration skipped (pip install python-sat, then rerun); steps 4 and 5 check the clauses directly
== 7. the UNSAT proof: compile drat-trim (Heule, Wetzler) and check sb.drup against sb.cnf

s VERIFIED

c verification time: 0.149 seconds
proof VERIFIED
== 8. negative controls
truncated proof rejected as expected
bad family (a repeated member) rejected as expected
ALL CHECKS PASS
```
