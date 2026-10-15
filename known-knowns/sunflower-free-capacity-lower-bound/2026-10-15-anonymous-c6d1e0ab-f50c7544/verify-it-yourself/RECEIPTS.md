# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0; local absolute paths in the output replaced by a placeholder):

```text
== 1. object hashes against INDEX.csv
family sha256 matches INDEX.csv
== 2. the family: 12 distinct 3-subsets of [8], no three with pairwise equal intersections (check_family.py, three methods)
  "min_size_to_beat_1.554": 35,
  "min_size_to_beat_1.551": 34,
  "rate_floor_10dp": "1.3642616018"
 },
 "verdict": "SUNFLOWER-FREE; does not clear 1.5545 bar"
}
family check PASS
== 3. the CNF header states n=8, r=3, |F| >= 13
c sunflower-free F in C([8],3), |F| >= 13; triples=1400; sb=none; card=seqcounter; deg<=none
header PASS
== 4. the CNF's ternary clauses are exactly the 3-sunflowers of C([8],3), recomputed by brute force from the definition (triples_recheck.py)
[workspace path] M=56 sets of size [3]; sunflower triples by brute force 1400; ternary negative clauses in CNF 1400; MATCH
sunflower clauses PASS
== 5. the cardinality clauses encode |F| >= 13 (stdlib check: every assignment with exactly 13 chosen sets found by sampling satisfies them, and 12 chosen sets never does; card_check.py)
M=56 sunflower_clauses=1400 cardinality_clauses=1088 aux_vars=559
CARD OK
cardinality PASS
== 5b. the proved CNF contains every clause of the plain CNF (its extra clauses are the lex-leader symmetry-breaking constraints; subset_check.py)
plain clauses 2488, proved clauses 4952, extra in proved 2464, var maps equal True
SUBSET OK
subset PASS
== 6. regenerate the CNF with the shipped generator (needs python-sat; skipped if absent)
python-sat not installed: regeneration skipped (pip install python-sat, then rerun); steps 4 and 5 check the clauses directly
== 7. the UNSAT proof: compile drat-trim (Heule, Wetzler) and check sb.drup against sb.cnf

s VERIFIED

c verification time: 0.108 seconds
proof VERIFIED
== 8. negative controls
truncated proof rejected as expected
bad family (a repeated member) rejected as expected
ALL CHECKS PASS
```
