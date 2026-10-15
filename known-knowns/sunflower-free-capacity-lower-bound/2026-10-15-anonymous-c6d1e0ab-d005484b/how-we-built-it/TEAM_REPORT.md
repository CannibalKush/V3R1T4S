# Candidate (partial win p2): twenty-two exact values g(n,r) with machine-checked proofs

Status: PROMISING (team sunflower: opus-sun computed the families and the proofs; fable-sun reviewed the
pipeline, re-verified independently and wrote the soundness note). Only the orchestrator's panel can confirm.
Labels: the values are NUMERICAL (machine-checked UNSAT proofs + checked families); the lemmas used are
PROVED-HERE (SOUNDNESS.md); novelty is UNCHECKED (see section 4).

## 1. What is claimed
g(n,r) = maximum size of an r-uniform 3-sunflower-free family on [n] (no three distinct members with pairwise
equal intersections; three pairwise disjoint members count). Twenty-two exact values:

| n \ r | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| 6 | 10 | | | | | |
| 7 | 12 | 15 | 12 | | | |
| 8 | 12 | 24 | 22 | 16 | | |
| 9 | 14 | 27 | 42 | 32 | 20 | |
| 10 | 16 | 31 | | 70 | 44 | 25 |
| 11 | 16 | | | | 110 | |
| 12 | 20 | | | | | 165 |

The authoritative, machine-generated list with the proof basis of every row is `INDEX.md` / `index.json`
(`tools/build_index.py --check`). Proof basis: 9 rows have proofs of the plain CNF (no symmetry breaking);
7 rows have proofs with lex-leader symmetry breaking, three of them also with a valid degree cut
((9,3), (9,5), (9,6), (10,3), (10,8), (11,3), (12,3)); 4 rows follow from a proved predecessor by the link lemma
g(n,r) <= floor(n g(n-1,r-1)/r) together with a family of exactly that size ((9,4) from (8,3); (10,6) from
(9,5); (11,7) from (10,6); (12,8) from (11,7)); 2 rows, (10,4) = 31 and (10,7) = 44, are proved by a case split on the link of a
maximum-degree point (17 and 6 UNSAT case proofs, all verified; `opus_packages/g_10_4_31/ARGUMENT.md`,
`opus_packages/g_10_7_44/ARGUMENT.md`, SOUNDNESS.md section 10). Caution: g(10,7) = 44 is probably a known
value (in the complement view g(n,n-3) is the Turan number ex(n, K4^-) of 3-graphs with no three edges on four
vertices; not checked here). In addition `opus_packages/bound_g_11_4_le38/` proves the upper bound g(11,4) <= 38
(not an exact value; a 36-family is known) by the same method, which is what kills n = 15 for the bar. The PSL(2,11)-invariant family of 110 seven-sets on 11 points is
therefore provably optimal for (11,7); its rate 110^(1/11) = 1.5331 is the best among all exact values.

## 2. Artifacts (everything a panel needs is inside this folder)
- `opus_packages/g_{n}_{r}_{v}/` (17 rows, opus-sun; g_10_4_31 is a case-split package: ARGUMENT.md, cases/, classify/): `family.json`; `family_check.txt` and `family_sfcheck.txt`
  (two independent family checkers); for each proof variant `{variant}.cnf`, `{variant}.drup`,
  `{variant}_drat_trim.txt`, `{variant}_drup_check.txt` (two independent proof checkers, both `s VERIFIED`);
  `manifest.json`; `regenerate.sh`. Variant names: `nosb` = plain CNF, `sb` = lex-leader symmetry breaking over
  all point transpositions, `sb_degD` = lex-leader plus the degree cut deg(p) <= D. The CNF's first line states
  (n, r, k, sb, deg); the variable-to-set map is in its `c var` lines.
- `chain_rows/g_{n}_{r}_{v}/` (4 rows, fable-sun): `family.json` and `derivation.json` (predecessor value, the
  integer computation, the family's origin).
- `tools/`: `check_family.py` (stdlib, three sunflower tests + exact integer rate), `sfcheck.c`, `gen_cnf.py` (the
  CNF generator), `triples_recheck.py` (brute-force recomputation of all sunflower clauses from the definition),
  `drat-trim.c` (Heule-Wetzler), `drup_check2.c` (opus-sun's forward RUP checker), `chain_check.py`,
  `build_index.py`, `exact_bb.py` (fable-sun's exhaustive branch-and-bound, the SAT-free second method),
  `verify_all.py`.
- `verify_all.sh`: re-verifies everything from a clean copy (see section 3).
- `SOUNDNESS.md`: the referee-facing argument (CNF completeness, cardinality encoding, lex-leader soundness,
  degree cuts, the link-lemma chain, proof checking, controls, limits).
- `bounds/g_10_4_le32/`: the supporting bound g(10,4) <= 32 (CNFs, three verified DRUP proofs, classification of the
  extremal (9,3)-families, scripts, fable-sun's independent checks, README with the argument).
- `second_method/`: outputs of the exhaustive branch-and-bound for (7,3), (7,4), (8,3), (8,4), (9,3) (same maxima).
- `g_{n}_{r}/` (12 folders) and `verification_summary.json`: fable-sun's earlier independent re-check of the first
  twelve rows (sunflower-clause sets recomputed and compared, drat-trim re-run); kept as a record. For (9,4) the
  folder holds the CNF and the drat-trim VERIFIED output of a 437 MB lex-leader proof that was deleted afterwards
  (size rule); the row now rests on the link lemma.

## 3. How to re-check (what was run, and what a panel should run)
    cp -R candidates/exact_small_values /some/clean/place/ && cd /some/clean/place/exact_small_values
    PYSAT=/path/to/python-with-pysat ./verify_all.sh            # add --bb-all for the two long B&B cases
It compiles the C tools, checks all 21 families with both checkers, recomputes the sunflower clauses of all 27 row
CNFs and 17 case CNFs by brute force (all MATCH), runs both proof checkers on all 27 + 19 proofs, regenerates all CNFs and compares
them with the proved files, runs the negative controls (a truncated proof and a foreign proof must be rejected
by both checkers; a family with three disjoint sets must be rejected by both family checkers), re-runs the
exhaustive second method on (7,3), (7,4), (8,3), and finally `chain_check.py` and `build_index.py --check`.
Single-threaded; about 15 minutes (4 minutes without the case-split package).

Clean-copy runs by fable-sun on 2026-10-14 (work/fable/clean_regen/):
- run 1 (19 rows, 22:54 UTC): 143 checks, 122 PASS; the 21 'FAIL' lines were all the regeneration comparison of
  CNFs written before the generator gained its `--deg` option: their first comment line lacks the field
  `deg<=none`, the clause bodies are byte-identical. The comparison now checks the body and the parsed header.
- run 2 (20 rows, 22:59 UTC, after the fix and with the controls and second-method steps added):
  RESULT: 158 checks, 0 failed, 232 s -> PASS (log: verify_runs/run2_clean_copy_20rows.log; run 1 log alongside).
- run 4 (21 rows including the case-split row (10,4) = 31, 23:55 UTC): 216 checks, 0 failed, 865 s -> PASS
  (log: verify_runs/run4_clean_copy_21rows.log); it re-ran both proof checkers and the brute-force clause recheck on
  all 17 case proofs and 2 classification-completeness proofs and rebuilt the package's 24 CNFs identical.
  The 21 header-only regeneration differences are reported as PASS with the note 'header comment differs only by
  the field deg<=none; clauses identical'.
- run 3 (20 rows, 23:08 UTC, `--bb-all`, i.e. the exhaustive second method also re-run on (9,3) and (8,4)):
  TOTAL 160 checks, 0 failed, 1499 s -> PASS; second method exact_bb.py (9,3) max = 14 PASS 117.0s; second method exact_bb.py (8,4) max = 24 PASS 1178.4s (log: verify_runs/run3_clean_copy_20rows_bb_all.log).

## 4. Why it matters / what it would beat
No table of g(n,r) appears in the sources we were allowed to read (Naslund-Sawin 2017, Frankl-Pach-Palvolgyi
2024, Tang-Zhang 2025, the bank page). Whether these values are published elsewhere could NOT be checked (web
access was restricted); in particular g(12,3) = 20 may coincide with a classical result of Abbott, Hanson and
Sauer on 3-uniform families (SPECULATION, unverified memory). The partial win p2 requires "not previously
published", so the panel must check the literature.

Consequences used by the team (NUMERICAL, link-lemma recursion seeded with these values; NOTES.md section 4
and 11): no uniform family on n <= 13 points can clear the bank's 1.5545 bar, none on n <= 12 can beat 1.551,
g(14,7) <= floor(1001*16/35) = 457 < 482, and with the bound g(10,4) <= 32 (`bounds/g_10_4_le32/`, a case split on an
extremal (9,3)-link; not an exact value, g(10,4) is 31 or 32) also g(14,8) <= 457 < 482, and with the exact row g(10,4) = 31 even g(14,8) <= 443: no uniform family on at most
14 points can clear the bar; with g(11,4) <= 38 the same holds for 15 points (max over r of the recursive bound at
n = 15 is 738 < 748, recomputed independently by fable-sun). First open cells: (16,8) <= 1238, (16,9) <= 1312,
(16,10) <= 1176 against 1163.

## 5. Corrections since the first version of this report
- 2026-10-14 19:30 UTC: twelve values. 19:56: seventeen (g(9,5)=42 and its chain). 22:51: g(10,3)=16, g(11,3)=16
  (opus-sun). 22:57: g(12,3)=20 (opus-sun). 23:51: g(10,4)=31 (opus-sun, case split). 00:20: g(10,7)=44 (opus-sun,
  case split; twenty-two values) and the bound g(11,4) <= 38.
- fable-sun's earlier NOTES claim "g(10,3) = 20 via the stars of K5" was WRONG (that family contains three
  pairwise disjoint triples) and was withdrawn when opus-sun's UNSAT proof of (10,3)@17 appeared.
- The 437 MB lex-leader proof of (9,4)@28 and the 1.07 GB plain proof of (9,5)@43 were both verified by drat-trim
  and then deleted under the "no proof files over 100 MB kept" rule; the verifier outputs are kept (g_9_4/ and
  opus_packages/g_9_5_42/plain_deg24_record/, the latter with the proof's SHA-256). With the plain proof of (9,5),
  the rows (9,5), (10,6), (11,7), (12,8) no longer depend on symmetry breaking.
