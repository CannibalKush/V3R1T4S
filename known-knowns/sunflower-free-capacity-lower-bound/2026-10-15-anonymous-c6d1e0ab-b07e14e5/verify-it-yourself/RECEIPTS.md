# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0; local absolute paths in the output replaced by a placeholder):

```text
== 1. object hashes against INDEX.csv
family sha256 matches INDEX.csv
== 2. the family: 12 distinct 3-subsets of [7], no three with pairwise equal intersections (check_family.py, three methods)
  "min_size_to_beat_1.554": 22,
  "min_size_to_beat_1.551": 22,
  "rate_floor_10dp": "1.4261616352"
 },
 "verdict": "SUNFLOWER-FREE; does not clear 1.5545 bar"
}
family check PASS
== 3. the CNF header states n=7, r=3, |F| >= 13
c sunflower-free F in C([7],3), |F| >= 13; triples=315; sb=none; card=seqcounter; deg<=none
header PASS
== 4. the CNF's ternary clauses are exactly the 3-sunflowers of C([7],3), recomputed by brute force from the definition (triples_recheck.py)
[workspace path] M=35 sets of size [3]; sunflower triples by brute force 315; ternary negative clauses in CNF 315; MATCH
sunflower clauses PASS
== 5. the cardinality clauses encode |F| >= 13 (stdlib check: every assignment with exactly 13 chosen sets found by sampling satisfies them, and 12 chosen sets never does; card_check.py)
M=35 sunflower_clauses=315 cardinality_clauses=563 aux_vars=286
CARD OK
cardinality PASS
== 5b. the proved CNF contains every clause of the plain CNF (its extra clauses are the lex-leader symmetry-breaking constraints; subset_check.py)
plain clauses 878, proved clauses 878, extra in proved 0, var maps equal True
SUBSET OK
subset PASS
== 6. regenerate the CNF with the shipped generator (needs python-sat; skipped if absent)
python-sat not installed: regeneration skipped (pip install python-sat, then rerun); steps 4 and 5 check the clauses directly
== 7. the UNSAT proof: compile drat-trim (Heule, Wetzler) and check nosb.drup against nosb.cnf

s VERIFIED

c verification time: 0.075 seconds
proof VERIFIED
== 8. negative controls
truncated proof rejected as expected
bad family (a repeated member) rejected as expected
ALL CHECKS PASS
```
