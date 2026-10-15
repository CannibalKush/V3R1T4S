# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, a C compiler; python-sat optional):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected: the family hash matches INDEX.csv; `check_family.py` reports 24 members and no 3-sunflower by three methods;
the CNF header states n=8, r=4, |F| >= 25; `triples_recheck.py` prints MATCH (the ternary clauses are exactly the
3-sunflowers, recomputed by brute force); `card_check.py` prints CARD OK; with python-sat the generator reproduces the CNF;
drat-trim prints `s VERIFIED` on the proof; a truncated proof and a bad family are rejected; last line `ALL CHECKS PASS`.

Alone:

```sh
python3 verify-it-yourself/check_family.py object/family_g8_4_24.json
python3 verify-it-yourself/triples_recheck.py object/nosb.cnf
cc -O2 -o drat-trim verify-it-yourself/drat-trim.c && ./drat-trim object/sb.cnf object/sb.drup -f
python3 verify-it-yourself/gen_cnf.py 8 4 25 regen.cnf --sb alltrans && cmp regen.cnf object/sb.cnf
```

To rebuild the proof: run a DRUP-producing solver (glucose4 was used) on object/sb.cnf; the proof differs by run but
drat-trim must verify it.
