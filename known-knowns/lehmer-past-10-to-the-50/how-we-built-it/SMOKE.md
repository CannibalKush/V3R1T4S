# Smoke run of the pipeline (2026-10-11)

Run from this repository's files (engines/, how-we-built-it/, verify-it-yourself/) in a scratch directory outside the
repository, on the build machine: Apple M5 (10 cores), macOS, Apple clang 21.0.0, GMP 6.3.0 (Homebrew), python3 for
the helper scripts, python 3.12.13 + sympy 1.14.0 for `certify.py`. Everything under `nice -n 10`, at most 2 workers /
threads, load average 55-69 from other jobs. Tiny bound X = 10^30 with task depth D0 = 8 (108 subtrees).

## A. Every stage end to end at X = 10^30

```sh
R=<this family directory>; I="-I/opt/homebrew/include -L/opt/homebrew/lib"
mkdir -p v1/engines && cp $R/engines/* v1/engines/
(cd v1 && patch -p1 < $R/how-we-built-it/lcrt5_v1_LCRT4.patch && patch -p1 < $R/how-we-built-it/merge_lcrt_v1.patch)
cc -O3 $I -o lcrt5 $R/engines/lcrt5.c -lgmp
cc -O3 $I -DORPHAN_EXIT=1 -o lcrt5_v1 v1/engines/lcrt5.c -lgmp
cc -O3 $I -o vlrt2 $R/engines/vlrt2.c -lgmp -lpthread
cc -O3 $I -o lbb2 $R/engines/lbb2.c -lgmp -lm
X=$(python3 -c 'print(10**30)')

# 1. certified-run driver (LCRT-4 engine revision + its merge + certify)
mkdir job && cd job && PY=<python with sympy> SIEVE=1000000 WORKERS=2 D0=8 nice -n 10 sh $R/how-we-built-it/run_lcrt5_job.sh ../lcrt5_v1 ../v1/engines 30 && cd ..
# 2. final engine, LCRT-6, then diff against step 1
nice -n 10 ./lcrt5 $X 1000000 8 2 o30m6 1 5 1 32 1 0 1 1024 1000 2> o30m6.log
python3 $R/engines/merge_lcrt.py o30m6 > s30m6.json && python3 $R/engines/certify.py s30m6.json 30 | grep VERDICT
python3 $R/verify-it-yourself/diff_runs.py o30m6 job/out_1e30
# 3. vlrt2 in two pieces, as for the 10^50 log: a subset, then the remaining prefixes, then the union
mkdir v && cd v
VSTRIDE=3 VOFF=0 nice -n 10 ../vlrt2 $X 10000000 8 2 1 5 1 32 1 1 partA 1024 1000
python3 $R/how-we-built-it/vlrt2_union.py remaining ../job/out_1e30 partA.tasks.jsonl > rem.txt
VSEL=rem.txt nice -n 10 ../vlrt2 $X 10000000 8 2 1 5 1 32 1 1 partB 1024 1000
python3 $R/how-we-built-it/vlrt2_union.py merge partA.tasks.jsonl > partA_merged.jsonl
python3 $R/how-we-built-it/vlrt2_union.py union partA_merged.jsonl partB.tasks.jsonl > union.tasks.jsonl
python3 $R/verify-it-yourself/recompute_summary.py union.tasks.jsonl --top partB.summary.json --expect-ntasks 108
python3 $R/verify-it-yourself/diff_runs.py union.tasks.jsonl ../job/out_1e30
cd ..
# 4. lbb2 with the parallel driver, then its aggregator
nice -n 10 bash $R/how-we-built-it/run_lbb2_parallel.sh ./lbb2 runs 30 2 8 10000000
python3 $R/verify-it-yourself/lbb2_aggregate.py runs/e30_S10000000
# 5. packaging round trip
(cd job && tar czf ../lcrt5_1e30_LCRT4_tasks.tar.gz out_1e30) && mkdir tx && cd tx && tar xzf ../lcrt5_1e30_LCRT4_tasks.tar.gz \
  && python3 $R/verify-it-yourself/recompute_summary.py out_1e30
```

Results (trimmed):

| step | runtime | output |
|---|---|---|
| build (4 binaries) | ~10 s | no warnings shown; the patches apply cleanly; patched `lcrt5.c` sha256 `c4ec83c1…`, patched `merge_lcrt.py` sha256 `57aa39c2…` (= the merge that produced the certified summary) |
| 1. LCRT-4 driver | 44 s search + merge/certify | `master: 108 tasks at depth 8`, `1e30 certify exit 0`; summary: complete, 1 678 visited nodes (digest `6a39fd0c4d728743`), 1 374 live (`b270d41143bd0193`), 845 Euler closures / 0 passes, c2_int 0, events []; `"VERDICT": "NO LEHMER NUMBER N <= 10^30"` |
| 2. LCRT-6 | 3 s | same VERDICT; `diff_runs.py`: 108 compared, `"IDENTICAL": true` |
| 3. vlrt2 pieces + union | < 1 s each | `task subset: 36 of 108`, then 72 remaining prefixes, `task subset: 72 of 108`; union `108 task lines`; `recompute_summary.py`: nodes 1 678, digest `6a39fd0c4d728743`, live 1 374, digest_live `b270d41143bd0193`, euler_pass 0, events []; `diff_runs.py` vs step 1: `"IDENTICAL": true` |
| 4. lbb2 | 10 s | 44 tasks, 2/2 workers finished, 44 done, missing 0, prefix_mismatch 0, solutions 0, euler_pass 0, `"complete_and_clean": true` |
| 5. tar round trip | < 1 s | 108 task lines, missing 0, DONE marker, same totals |

Matches expectation: the three engines agree (lcrt5 in two modes and vlrt2 subtree by subtree; lbb2 complete and
clean), and the max q differs only between modes (1 489 in LCRT-4, 1 487 in vlrt2's candidate-closure mode), which is
the expected mode-dependent field.

## B. Byte-exact regeneration of shipped 10^50 objects from their inputs

From the shipped tarballs (unpacked) and the original intermediate files, with the repository scripts:

| command | reproduces (sha256) | result |
|---|---|---|
| `v1/engines/merge_lcrt.py lcrt5_1e50 > summary_1e50.json` (21 s) | `certificates/lcrt5_1e50.summary.json` `90d1d94b…` | identical |
| `engines/certify.py summary_1e50.json 50` | `certificates/certificate_lcrt5_1e50.json` `4f827108…` | identical |
| `engines/merge_lcrt.py lcrt6_1e50_bigsieve` | `certificates/lcrt6_1e50_bigsieve.summary.json` `943b738c…` | identical |
| `engines/certify.py lcrt6_1e50_bigsieve.summary.json 50` | `certificates/certificate_lcrt6_1e50_bigsieve.json` `36dcd993…` | identical |
| `vlrt2_union.py union` on the two shipped vlrt2 `.gz` parts | `vlrt2_full50_union.tasks.jsonl` `5bf42b3e…` | identical |
| `vlrt2_union.py merge` / `remaining` / `minus … \| LC_ALL=C sort` on the original part files | `v6_50_merged` `c286ee34…`, `rem50.txt` `a37e070f…`, `sel50_remaining.txt` `192ca02d…` | identical |
| `verify-it-yourself/lbb2_aggregate.py runs/e50_S1000000000` | `branch_logs/lbb2_agg_e50.json` `0ce7cefd…` | identical |
| unpacked `lcrt5_1e50/`, `lcrt6_1e50_bigsieve/`, `e50_S1000000000/` | the original run directories | identical, file by file |
| `engines/xcheck_segc2.py certificates/lcrt5_1e50.log 50` | `certificates/xcheck_segc2_1e50.jsonl` | first 14 of 60 lines identical; the rest of the rerun (sympy factorisations of numbers of up to 48 digits) was still running under load when this was written |

The 10^50 searches themselves (13-25 min each on 8-10 cores) were not rerun for this smoke test; see
`../RUN_IT_YOURSELF.md` Level 2.
