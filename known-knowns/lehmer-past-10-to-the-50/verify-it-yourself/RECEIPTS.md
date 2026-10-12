# Check results (Lehmer 10^50)

## Level 1: `sh verify-it-yourself/run_checks.sh` (2026-10-10T19:34:44Z – 19:37:12Z)

Run on the shipped files on the build machine (macOS, python3 3.9, load average about 80–100). Exit code 0, last line
`ALL CHECKS PASSED`. All numbers are identical to the earlier run of 2026-10-09 (below): 65 647 subtrees in each of the three logs, visited
nodes 2 169 013 803, live nodes 130 205 304, Euler closures 102 312 897 with 0 passes, 0 integral two-prime
completions, 0 events, digests `74e2002af271a197` / `7c1d8e5190f9754f` for the two author runs and for vlrt2; the
three subtree-by-subtree comparisons report `IDENTICAL` (65 647 compared, 0 differences); lbb2 is complete and clean
(41 170 tasks, 10/10 workers, 0 solutions, 0 Euler passes). The shipped logs contain no host-specific fields (no
absolute paths, host names or process ids), so no log was modified for this release and every digest is of the
original data. In the output below, the temporary unpack directory (an absolute path under the system temp dir) is
shown as `$TMP/` and this family's directory as `lehmer/`.

```
2026-10-10T19:34:44Z
== analytic closures (exact rationals)
{"E": 50, "lemma_A_3_divides_N": {"omega_max": 27, "ratio_max": "41986302801436261676558796091323663/14335014864591025495403921408000000", "ratio_float": 2.92893332849949, "ratio_lt_4": true}, "lemma_B_3_not_divides_N": {"omega_max": 30, "ratio_max": "710739494962032881009020595862538715843/240934574033184977247844140318720000000", "ratio_float": 2.949927372665658, "ratio_lt_3": true}, "search_reduces_to_k_eq_2_primes_ge_5": true}
== unpack branch logs
== author run, mode LCRT-4
  nodes_total = 2169013803 
  live_total = 130205304 
  euler_closed_total = 102312897 
  euler_pass_total = 0 
  c2_int_total = 0 
  kfilt_total = 25849618340 
  max_q_seen = 43725458932 
  n_events = 0 
  digest = 74e2002af271a197 
  digest_live = 7c1d8e5190f9754f 
  task_lines = 65647 
  duplicate_conflicts = 0 
== author run, mode LCRT-6
  nodes_total = 2169013803 
  live_total = 130205304 
  euler_closed_total = 102312897 
  euler_pass_total = 0 
  c2_int_total = 0 
  kfilt_total = 25849618340 
  max_q_seen = 43725458932 
  n_events = 0 
  digest = 74e2002af271a197 
  digest_live = 7c1d8e5190f9754f 
  task_lines = 65647 
  duplicate_conflicts = 0 
== independent engine vlrt2, all 65647 subtrees
  nodes_total = 2169013803 
  live_total = 130205304 
  euler_closed_total = 102312897 
  euler_pass_total = 0 
  c2_int_total = 0 
  kfilt_total = 25849618340 
  max_q_seen = 43725458932 
  n_events = 0 
  digest = 74e2002af271a197 
  digest_live = 7c1d8e5190f9754f 
  task_lines = 65647 
  duplicate_conflicts = 0 
== subtree-by-subtree diffs
{"A": "$TMP/lcrt5_1e50", "B": "$TMP/lcrt6_1e50_bigsieve", "tasks_A": 65647, "tasks_B": 65647, "conflicts_A": 0, "conflicts_B": 0, "only_A": 0, "only_B": 0, "compared": 65647, "subtrees_with_difference": 0, "differences_per_field": {}, "compared_fields": ["nodes", "live", "small", "eclosed", "epass", "c2i", "kfilt", "digest", "digest_live", "events", "maxq"], "examples": [], "IDENTICAL": true}
{"A": "lehmer/branch_logs/vlrt2_full50_union.tasks.jsonl.gz", "B": "$TMP/lcrt5_1e50", "tasks_A": 65647, "tasks_B": 65647, "conflicts_A": 0, "conflicts_B": 0, "only_A": 0, "only_B": 0, "compared": 65647, "subtrees_with_difference": 0, "differences_per_field": {}, "compared_fields": ["nodes", "live", "small", "eclosed", "epass", "c2i", "kfilt", "digest", "digest_live", "events"], "examples": [], "IDENTICAL": true}
{"A": "lehmer/branch_logs/vlrt2_full50_union.tasks.jsonl.gz", "B": "$TMP/lcrt6_1e50_bigsieve", "tasks_A": 65647, "tasks_B": 65647, "conflicts_A": 0, "conflicts_B": 0, "only_A": 0, "only_B": 0, "compared": 65647, "subtrees_with_difference": 0, "differences_per_field": {}, "compared_fields": ["nodes", "live", "small", "eclosed", "epass", "c2i", "kfilt", "digest", "digest_live", "events"], "examples": [], "IDENTICAL": true}
== independent engine lbb2, completeness
{
 "dir": "$TMP/e50_S1000000000",
 "ntask": 41170,
 "workers": 10,
 "workers_finished": 10,
 "tasks_done": 41170,
 "missing": 0,
 "prefix_mismatch": 0,
 "nodes_total": 3805754261,
 "m2apcand": 220780104,
 "m2q1": 1713809944,
 "m3euler": 241524181,
 "m1int": 0,
 "m2int": 0,
 "euler_pass": 0,
 "solutions": 0,
 "segq": 0,
 "segchild": 0,
 "maxq1": 164887049,
 "events": {},
 "complete_and_clean": true
}
ALL CHECKS PASSED
sh verify-it-yourself/run_checks.sh  35.25s user 2.25s system 25% cpu 2:27.91 total
2026-10-10T19:37:12Z
```

## Lean formalization: `lake build` in `lean/` (2026-10-10T19:25:32Z – 19:28:22Z)

Built in a copy of `lean/` with Lean `v4.35.0-rc4` and the Mathlib revision pinned in `lake-manifest.json`:
`Build completed successfully (9023 jobs)`. The build emits only linter warnings (6 long lines, 4 unused section
variables, 2 module doc-string placement, 1 `import Mathlib` style note); no `sorry`, no errors. Axioms:

```
'LehmerOracle.reduction' depends on axioms: [propext, Classical.choice, Quot.sound]
'LehmerOracle.node_conditions' depends on axioms: [propext, Classical.choice, Quot.sound]
'LehmerOracle.c1' depends on axioms: [propext, Classical.choice, Quot.sound]
'LehmerOracle.crt' depends on axioms: [propext, Classical.choice, Quot.sound]
'LehmerOracle.euler' depends on axioms: [propext, Classical.choice, Quot.sound]
'LehmerOracle.c4' depends on axioms: [propext, Classical.choice, Quot.sound]
'LehmerOracle.c2_closure' depends on axioms: [propext, Classical.choice, Quot.sound]
```
(The other theorems of `Search.lean` were not printed individually; `node_conditions` bundles them and depends on
nothing beyond these three standard axioms.)

## Not rerun for this release

The engines (Level 2 of `RUN_IT_YOURSELF.md`) were not rerun for this release; the record of their runs follows.

## Earlier check results (2026-10-09), kept for the record

Run on 2026-10-09 01:05Z–01:35Z on the build machine with the python3-only tools in `verify-it-yourself/` on the shipped files
(`sh verify-it-yourself/run_checks.sh` reproduces all of it in about 6 minutes; the numbers below are its output).

### Analytic closures (`closures.py`)

```
E=50: Lemma A (3 | N): omega_max 27, ratio 2.928933328499... < 4 : true
      Lemma B (3 not | N): omega_max 30, ratio 2.949927372665... < 3 : true   -> the search is k = 2 with all primes >= 5
E=56: both still true (2.952136 < 4, 2.993151 < 3)
E=58: Lemma B fails (3.013375 > 3)
```
Exact rationals, own prime table; agrees digit for digit with the author's `certify.py` (which was also rerun on the
two shipped summaries: `"VERDICT": "NO LEHMER NUMBER N <= 10^50"`, summary sha256 90d1d94b…615ab and 943b738c…f893,
equal to the values quoted inside `certificates/certificate_lcrt5_1e50.json` and `certificate_lcrt6_1e50_bigsieve.json`).

### Totals and digests recomputed from the per-subtree logs (`recompute_summary.py`)

| log | task lines | missing / conflicting | visited nodes | live nodes | Euler closures (passes) | c2i | kfilt | max q | events | digest | digest_live |
|---|---|---|---|---|---|---|---|---|---|---|---|
| author, LCRT-4 (`lcrt5_1e50`) | 65 647 | 0 / 0, DONE marker present | 2 169 013 803 | 130 205 304 | 102 312 897 (0) | 0 | 25 849 618 340 | 43 725 458 932 | 0 | 74e2002af271a197 | 7c1d8e5190f9754f |
| author, LCRT-6 (`lcrt6_1e50_bigsieve`) | 65 647 | 0 / 0, DONE | 2 169 013 803 | 130 205 304 | 102 312 897 (0) | 0 | 25 849 618 340 | 43 725 458 932 | 0 | 74e2002af271a197 | 7c1d8e5190f9754f |
| independent engine vlrt2, all subtrees (`vlrt2_full50_union` + top record from `vlrt2_r50c.summary.json`) | 65 647 | 0 / 0 | 2 169 013 803 | 130 205 304 | 102 312 897 (0) | 0 | 25 849 618 340 | 43 725 458 932 | 0 | 74e2002af271a197 | 7c1d8e5190f9754f |

Per-depth profiles of the vlrt2 union equal the author's:
`nodes_by_depth = [1, 3, 7, 17, 29, 57, 129, 341, 986, 3005, 11736, 65647, 662953, 80450857, 2061050747, 26767283, 5]`,
`live_by_depth = [1, 3, 7, 17, 29, 57, 129, 341, 986, 3005, 11736, 65647, 662953, 31403462, 97992813, 64118]`.
The 62 061-subtree vlrt2 run alone (`vlrt2_r50c`) has 1 443 345 623 visited nodes, 109 898 530 live nodes, 0 Euler
passes, 0 c2i, 0 events; together with the 3 586 subtrees of an earlier partial run of the same engine (`vlrt2_verifier_v6_50_merged`,
disjoint from it) it covers exactly the 65 647 prefixes of the author's run.

### Subtree-by-subtree comparison (`diff_runs.py`)

| A | B | compared | differences | verdict |
|---|---|---|---|---|
| author LCRT-4 | author LCRT-6 (`--maxq` included) | 65 647 | 0 | IDENTICAL |
| vlrt2 union | author LCRT-4 | 65 647 | 0 | IDENTICAL |
| vlrt2 union | author LCRT-6 | 65 647 | 0 | IDENTICAL |
| vlrt2 r50c (62 061) | author LCRT-4 (`--allow-subset`) | 62 061 | 0 | IDENTICAL on the subset |
| vlrt2 earlier partial run (3 586) | author LCRT-4 (`--allow-subset`) | 3 586 | 0 | IDENTICAL on the subset |

Fields compared: per-depth visited, live, small-regime, Euler-closed and Euler-passed node counts, integral two-prime
completions, kfilt, both 64-bit digests, presence of events. `maxq` is excluded for cross-engine comparisons because
vlrt2 records it differently (with it included, 65 595 of 65 647 subtrees differ in `maxq` only and in nothing else).
Negative control: altering one digest in a copy of the union log is reported as 1 subtree with a `digest` difference.

### Independent engine lbb2 (`lbb2_aggregate.py` on `lbb2_e50_S1000000000_tasks.tar.gz`)

```
ntask 41170, workers 10 (10 finished), tasks_done 41170, missing 0, prefix_mismatch 0,
nodes_total 3805754261, m2apcand 220780104, m2q1 1713809944, m3euler 241524181,
m1int 0, m2int 0, euler_pass 0, solutions 0, segq 0, segchild 0, maxq1 164887049, events {},
complete_and_clean true
```

### Not rerun for this release

The three engines were not rebuilt and rerun for this release (each full 10^50 run is 10–25 minutes on 8–10 cores;
the exact commands are in `RUN_IT_YOURSELF.md`). The shipped logs are the ones produced on 2026-10-08 by the author
(08:25–08:50 PDT and 08:53–09:06 PDT), by an independent reviewer (09:18–09:30 PDT, partial vlrt2 run) and by two
further independent reviewers (09:36–09:46 PDT for vlrt2; 10:17–10:41 PDT for lbb2). The side checks in `certificates/xcheck_segc2_1e50*.jsonl`
(algebraic closure of the 60 beyond-sieve intervals, `ALL_OK: true` on all 60; prime counts equal to sympy's
`primepi` on all 60) were produced by the author with `engines/xcheck_segc2.py` and were not rerun.
