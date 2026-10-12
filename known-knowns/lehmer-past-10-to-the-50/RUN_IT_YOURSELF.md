# Reproduce: Lehmer's totient problem, N > 10^50

All paths below are relative to the `known-knowns/lehmer-past-10-to-the-50/` directory of this repository. Three levels. Level 1 (minutes, python3 only) re-derives every number in the README from the shipped branch logs and
checks that the three engines' logs agree. Level 2 (about an hour of CPU per engine) rebuilds the engines from
source and reruns the whole 10^50 search. Nothing accesses the network except the optional Lean build (Level 1b), which downloads Mathlib.

## Level 1: verify the shipped logs (python3, no packages)

```sh
cd known-knowns/lehmer-past-10-to-the-50               # from the repository root
python3 verify-it-yourself/closures.py 50 56 58
#   E=50: Lemma A omega_max 27 ratio 2.928933... < 4;  Lemma B omega_max 30 ratio 2.949927... < 3  -> search is k=2, primes >= 5
#   E=56 still true; E=58 Lemma B fails (3.013 > 3)

L=$(pwd)                         # the known-knowns/lehmer-past-10-to-the-50/ directory of this repository
mkdir -p scratch && cd scratch   # any empty scratch directory (known-knowns/lehmer-past-10-to-the-50/scratch/ is not part of the release)
tar xzf $L/branch_logs/lcrt5_1e50_LCRT4_tasks.tar.gz
tar xzf $L/branch_logs/lcrt6_1e50_bigsieve_LCRT6_tasks.tar.gz
tar xzf $L/branch_logs/lbb2_e50_S1000000000_tasks.tar.gz

python3 $L/verify-it-yourself/recompute_summary.py lcrt5_1e50
#   task_lines 65647, duplicate_conflicts 0, missing_tasks 0, DONE_marker true,
#   nodes_total 2169013803, live_total 130205304, euler_closed_total 102312897, euler_pass_total 0, c2_int_total 0,
#   kfilt_total 25849618340, max_q_seen 43725458932, n_events 0, digest 74e2002af271a197, digest_live 7c1d8e5190f9754f
python3 $L/verify-it-yourself/recompute_summary.py lcrt6_1e50_bigsieve                       # same totals and digests
python3 $L/verify-it-yourself/recompute_summary.py $L/branch_logs/vlrt2_full50_union.tasks.jsonl.gz \
        --top $L/branch_logs/vlrt2_r50c.summary.json --expect-ntasks 65647     # same totals and digests from the independent engine

python3 $L/verify-it-yourself/diff_runs.py lcrt5_1e50 lcrt6_1e50_bigsieve --maxq            # IDENTICAL, 65647 compared
python3 $L/verify-it-yourself/diff_runs.py $L/branch_logs/vlrt2_full50_union.tasks.jsonl.gz lcrt5_1e50          # IDENTICAL
python3 $L/verify-it-yourself/diff_runs.py $L/branch_logs/vlrt2_full50_union.tasks.jsonl.gz lcrt6_1e50_bigsieve # IDENTICAL
python3 $L/verify-it-yourself/lbb2_aggregate.py e50_S1000000000
#   ntask 41170, workers 10/10 finished, tasks_done 41170, missing 0, prefix_mismatch 0, solutions 0, euler_pass 0,
#   m1int 0, m2int 0, events {}, complete_and_clean true
```
`sh verify-it-yourself/run_checks.sh` does all of this. The author's own certificate script can be rerun on the shipped
summaries with `python3 engines/certify.py certificates/lcrt5_1e50.summary.json 50` (needs sympy; prints
`"VERDICT": "NO LEHMER NUMBER N <= 10^50"` and the summary's sha256, which must match the one quoted in
`certificates/certificate_lcrt5_1e50.json`).

Controls: `diff_runs.py` reports the subtree and field of any change (alter one digest in a copy of a log file);
`recompute_summary.py` reports missing tasks if a task line is deleted.

## Level 1b: build the Lean formalization (optional)

```sh
cd lean && lake build          # Lean v4.35.0-rc4 + Mathlib v4.35.0-rc4 (pinned in lean-toolchain / lake-manifest.json)
```
Expected: `Build completed successfully`, no `sorry`; `#print axioms LehmerOracle.reduction` (and the other
theorems) lists only `propext`, `Classical.choice`, `Quot.sound`. What this does and does not cover: `lean/README.md`.

## Level 2: rebuild the engines and rerun the search

All three engines need GMP (`libgmp`) and a C compiler; on macOS with Homebrew add
`-I/opt/homebrew/include -L/opt/homebrew/lib`. X is written out in decimal: `X=$(python3 -c 'print(10**50)')`.

**Author engine lcrt5** (8 worker processes; mode LCRT-6 is the fast one, ~13 min on a 10-core laptop; needs ~3 GB RAM
for the 2^32 sieve). Arguments: `X SIEVE D0 WORKERS OUTDIR SIGMA PMIN CRT KMAX FILT CQMODE EULER [C2CAND] [TDIV]`.
```sh
cd engines && cc -O3 -o lcrt5 lcrt5.c -lgmp
./lcrt5 $X 4294967291 11 8 out50 1 5 1 32 1 0 1 1024 1000        # LCRT-6 (as certificates/lcrt6_1e50_bigsieve)
# ./lcrt5 $X 1000000000 11 8 out50b 1 5 1 32 1 0 1               # LCRT-4 with segmented sieve (as certificates/lcrt5_1e50), ~25 min
python3 merge_lcrt.py out50 > s50.json && python3 certify.py s50.json 50     # certify.py needs sympy
python3 ../verify-it-yourself/diff_runs.py out50 ../scratch/lcrt5_1e50          # IDENTICAL (add --maxq when comparing two lcrt5 runs)
```
**Independent engine 1, vlrt2** (pthreads; ~12 min on 8 threads). Arguments:
`X SIEVE D0 THREADS SIGMA PMIN CRT KMAX FILT EULER outprefix [CC] [TDB]`; it writes `outprefix.tasks.jsonl`,
`outprefix.summary.json`, `outprefix.events.jsonl`.
```sh
cc -O3 -o vlrt2 vlrt2.c -lgmp -lpthread
./vlrt2 $X 4294967295 11 8 1 5 1 32 1 1 v50 1024 1000
python3 ../verify-it-yourself/recompute_summary.py v50.tasks.jsonl --top v50.summary.json --expect-ntasks 65647
python3 ../verify-it-yourself/diff_runs.py v50.tasks.jsonl ../scratch/lcrt5_1e50               # IDENTICAL
```
(`VSEL=prefixes.txt` restricts a run to the listed depth-11 prefixes, which is how the 62 061-subtree run was made.)

**Independent engine 2, lbb2** (one generator process, then W workers; ~25 min with 10 workers).
```sh
cc -O3 -o lbb2 lbb2.c -lgmp -lm
mkdir e50 && cd e50
../lbb2 -X 1e50 -S 1000000000 -D 11 -gen > gen.out                                  # 41170 TASK lines + TOTAL for the top
for w in 0 1 2 3 4 5 6 7 8 9; do ../lbb2 -X 1e50 -S 1000000000 -tasks gen.out -w $w 10 > w$w.out & done; wait
python3 ../../verify-it-yourself/lbb2_aggregate.py .                                             # complete_and_clean true, solutions 0
../lbb2 -S 1000000000 -selftest 20000000000 20010000000                             # segmented sieve vs table: 421348 primes
```
Positive controls described in the README (companion equation N + 1 = 2φ(N) with SIGMA = −1 and PMIN = 3 for lcrt5 /
vlrt2; `-fake -R` planted mode for lbb2) are documented in the engine headers and in `engines/SPEC_LCRT5.md` §5.

## Regenerate the shipped objects

[`how-we-built-it/README.md`](how-we-built-it/README.md) gives the exact commands and runtimes that produced every file in
`branch_logs/` and `certificates/`, including the engine revision of the certified LCRT-4 run (a patch to
`engines/lcrt5.c`) and the steps that assembled `vlrt2_full50_union.tasks.jsonl.gz` from its two runs. The main command
(certified run, then summary and certificate; ~25 min on 8 workers, needs sympy):
```sh
mkdir -p scratch/job && cd scratch/job
sh ../../how-we-built-it/run_lcrt5_job.sh ../../engines/lcrt5_v1 ../v1/engines 50   # build lcrt5_v1 first: how-we-built-it/README.md §0
```
A tiny version of the whole pipeline (X = 10^30, seconds) is in `how-we-built-it/SMOKE.md`.

## What a different result would mean

Any `SOLUTION` event, any Euler pass, any integral two-prime completion, a digest mismatch between engines, or a
missing subtree would invalidate the theorem as stated and must be reported (see Corrections in
`READ_BEFORE_CITING.md` at the repository root). A run that merely differs in `maxq` or in the mode-dependent diagnostics (`c2p`, `c2a`, `cand`,
`sqhit`, `tdrej`, `seg_*`) is expected when the mode or prime source differs.
