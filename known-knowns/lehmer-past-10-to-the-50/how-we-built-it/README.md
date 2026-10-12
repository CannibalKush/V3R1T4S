# How the 10^50 objects were built (end-to-end pipeline)

The three search engines and the summing / certificate scripts already ship in [`../engines/`](../engines/) and are the
reference code; this directory adds only what was missing to regenerate every published object: the job driver of the
certified run, the exact engine revision that run used (as a patch), the lbb2 parallel driver, and the merge/union
steps that assembled the independent engine's 65 647-subtree log. Every command below is the one recorded in the run
logs; times are wall-clock on the build machine (Apple M5, 10 cores, 32 GB, macOS, often at load average 20-60 from
other jobs). Paths are relative to `known-knowns/lehmer-past-10-to-the-50/`. `X=$(python3 -c 'print(10**50)')`.

| file | what it is |
|---|---|
| `run_lcrt5_job.sh` | driver of the certified LCRT-4 run: lcrt5 -> `merge_lcrt.py` -> `certify.py` (resumable) |
| `lcrt5_v1_LCRT4.patch` | turns `engines/lcrt5.c` into the revision that produced `lcrt5_1e50_LCRT4_tasks.tar.gz` |
| `merge_lcrt_v1.patch` | turns `engines/merge_lcrt.py` into the revision that produced `certificates/lcrt5_1e50.summary.json` |
| `run_lbb2_parallel.sh` | one lbb2 generator + W workers (the lbb2 10^50 run) |
| `vlrt2_union.py` | task-list / merge / union steps between the three vlrt2 runs (python3 only) |
| `requirements.txt` | sympy version (for `certify.py`, `xcheck_segc2.py`), compiler and GMP version |
| `SMOKE.md` | a tiny end-to-end rerun of this pipeline at X = 10^30 |

## 0. Build

```sh
cd engines
cc -O3 -o lcrt5 lcrt5.c -lgmp                     # final author engine (modes LCRT-4/5/6); macOS+Homebrew: add -I/opt/homebrew/include -L/opt/homebrew/lib
mkdir -p ../scratch/v1/engines && cp lcrt5.c merge_lcrt.py certify.py ../scratch/v1/engines/
(cd ../scratch/v1 && patch -p1 < ../../how-we-built-it/lcrt5_v1_LCRT4.patch && patch -p1 < ../../how-we-built-it/merge_lcrt_v1.patch)
cc -O3 -DORPHAN_EXIT=1 -o lcrt5_v1 ../scratch/v1/engines/lcrt5.c -lgmp   # the revision of the certified LCRT-4 run
cc -O3 -o vlrt2 vlrt2.c -lgmp -lpthread
cc -O3 -o lbb2 lbb2.c -lgmp -lm
```
The patched `lcrt5.c` has sha256 `c4ec83c1…` here; the file that actually ran (sha256
`b60bdb1982926bad6d34d259c570382631c2cd067c12445a8b9986e34b854d12`) differs from it only in a two-line comment that we
reworded. The revision adds nothing new: the final `engines/lcrt5.c` adds modes LCRT-5/6 (arguments 13 and 14) and two
output fields (`c2k`, `tdrej`) but gives the same mode-independent output in LCRT-4 mode. The v1 patch is needed only
to regenerate the LCRT-4 task lines and summary **byte for byte** (they lack the `c2k`/`tdrej`/`c2cand` fields).

## 1. Author engine, LCRT-4 (certified run) -> `branch_logs/lcrt5_1e50_LCRT4_tasks.tar.gz`, `certificates/lcrt5_1e50.*`

```sh
mkdir -p scratch/job && cd scratch/job                  # needs sympy for certify.py (PY=... to choose the python)
PY=python3 nice -n 10 sh ../../how-we-built-it/run_lcrt5_job.sh ../../engines/lcrt5_v1 ../v1/engines 50
#   = ./lcrt5_v1 $X 1000000000 11 8 out_1e50 1 5 1 32 1 0 1 2>> run_1e50.err
#     merge_lcrt.py out_1e50 > summary_1e50.json ; certify.py summary_1e50.json 50 > certificate_1e50.json
```
Original run: 08:25:52 -> 08:50:22 PDT on 2026-10-08, 1 468 s of search on 8 workers (`certificates/lcrt5_1e50.log` is
`run_1e50.err`; `out_1e50/` is the tarball's `lcrt5_1e50/`, renamed). The worker file names carry worker PIDs, so file
names differ between reruns; the task lines do not. `certify.py` writes the sha256 of the summary file it reads and the
file name exactly as passed on the command line; the certificate was produced with the name `summary_1e50.json`, and
the summary was later copied to `certificates/lcrt5_1e50.summary.json` unchanged.

Confirmed on the shipped files: `scratch/v1/engines/merge_lcrt.py lcrt5_1e50 > summary_1e50.json` reproduces
`certificates/lcrt5_1e50.summary.json` (sha256 `90d1d94b…15ab`) byte for byte, and `certify.py summary_1e50.json 50`
then reproduces `certificates/certificate_lcrt5_1e50.json` (sha256 `4f827108…dc86`) byte for byte.

Side checks of this run (section 5 of the family README), started 08:52 PDT:
```sh
python3 engines/xcheck_segc2.py scratch/job/run_1e50.err 50           > xcheck_segc2_1e50.jsonl          # needs sympy
python3 engines/xcheck_segc2.py scratch/job/run_1e50.err 50 --primepi > xcheck_segc2_1e50_primepi.jsonl  # last line {"E": 50, "ranges": 60, "ALL_OK": true}
```

## 2. Author engine, LCRT-6 cross-run -> `branch_logs/lcrt6_1e50_bigsieve_LCRT6_tasks.tar.gz`, `certificates/lcrt6_1e50_bigsieve.*`

```sh
cd engines
./lcrt5 $X 4294967291 11 8 lcrt6_1e50_bigsieve 1 5 1 32 1 0 1 1024 1000 2> lcrt6_1e50_bigsieve.log    # 784 s, ~3 GB RAM
python3 merge_lcrt.py lcrt6_1e50_bigsieve > lcrt6_1e50_bigsieve.summary.json
python3 certify.py lcrt6_1e50_bigsieve.summary.json 50 > certificate_lcrt6_1e50_bigsieve.json
```
Original run 08:53 -> 09:06 PDT. Confirmed: the shipped `engines/merge_lcrt.py` and `certify.py` reproduce
`certificates/lcrt6_1e50_bigsieve.summary.json` (`943b738c…f893`) and `certificate_lcrt6_1e50_bigsieve.json`
(`36dcd993…b020`) byte for byte from the tarball's task lines.

## 3. Independent engine 1, vlrt2 -> `branch_logs/vlrt2_*`

The 10^50 vlrt2 log was assembled from three runs of the same binary (`engines/vlrt2.c`; the file that ran differs only
in comment wording) because of a 20-minute rerun cap at the time:

```sh
cd engines
# part 1 (09:18 PDT): a full run, 10 threads, stopped by hand after ~4 min -> 286 complete task lines (v6_50.tasks.jsonl)
./vlrt2 $X 4294967295 11 10 1 5 1 32 1 1 v6_50 1024 1000
# part 2 (09:22-09:30): the tasks holding the 60 beyond-sieve C2 ranges of the LCRT-4 log not already in part 1,
#                       plus every task with index == 7 (mod 20); 3 315 tasks, 500 s wall, 10 threads
python3 ../how-we-built-it/vlrt2_union.py segc2 ../certificates/lcrt5_1e50.log > sel50_segc2.txt           # 39 prefixes
python3 ../how-we-built-it/vlrt2_union.py minus sel50_segc2.txt v6_50.tasks.jsonl | LC_ALL=C sort > sel50_remaining.txt   # 34
VSEL=sel50_remaining.txt VSTRIDE=20 VOFF=7 ./vlrt2 $X 4294967295 11 10 1 5 1 32 1 1 v6_50s 1024 1000
python3 ../how-we-built-it/vlrt2_union.py merge v6_50.tasks.jsonl v6_50s.tasks.jsonl > v6_50_merged.tasks.jsonl  # 3 586 lines
# part 3 (09:36-09:46): everything else, 8 threads, 600.9 s wall / 4 094 s CPU
python3 ../how-we-built-it/vlrt2_union.py remaining ../scratch/lcrt5_1e50 v6_50_merged.tasks.jsonl > rem50.txt     # 62 061 prefixes
VSEL=rem50.txt ./vlrt2 $X 4294967295 11 8 1 5 1 32 1 1 r50c 1024 1000 2> r50c.log
python3 ../how-we-built-it/vlrt2_union.py union v6_50_merged.tasks.jsonl r50c.tasks.jsonl > full50_union.tasks.jsonl  # 65 647
gzip -c v6_50_merged.tasks.jsonl > vlrt2_verifier_v6_50_merged.tasks.jsonl.gz   # likewise r50c, full50_union (gzip level not recorded)
```
(`../scratch/lcrt5_1e50` is the unpacked LCRT-4 tarball, as in `../RUN_IT_YOURSELF.md` Level 1, or any directory/tasks file with all 65 647 prefixes.)
`r50c.summary.json` is shipped as `vlrt2_r50c.summary.json` (it carries the top-tree record used by
`recompute_summary.py --top`); `r50c.log` is `vlrt2_r50c.log` (the `real/user/sys` lines come from `time`).

Confirmed with `vlrt2_union.py` on the original intermediate files (sha256 of the uncompressed outputs):

| output | sha256 | reproduced |
|---|---|---|
| `sel50_segc2.txt` (39 prefixes) | same prefix set as the original (line order of the original file not recoverable; irrelevant to VSEL) | set-identical |
| `sel50_remaining.txt` | `192ca02df3946ad7de75f785841c9d51dfcc2824745a04bb2b80420210d092fc` | byte-identical |
| `v6_50_merged.tasks.jsonl` | `c286ee3456c143a71c8a5b46ba5993a089db54b6d2705ae8da2bf0f7c3e3dec3` | byte-identical |
| `rem50.txt` | `a37e070fe30f23a4d436b46190a1423d785160ed737a1c36d8abeb6d5a135c9d` | byte-identical (from either author run) |
| `full50_union.tasks.jsonl` | `5bf42b3e2e9e8668d3800dd74a27366c8d6f686ebd8691606f7026ca74689f61` | byte-identical (also from the two shipped `.gz` parts) |

Determinism: every task line is a deterministic function of (X, prefix, arguments) (part 1 and part 2 overlapped on 15
tasks with byte-identical lines), but vlrt2 writes lines in thread-completion order and part 1 depends on when it was
stopped, so a rerun reproduces the **set** of task lines, not the byte order of `r50c.tasks.jsonl`. The simplest
regeneration is one full run (`./vlrt2 $X 4294967295 11 8 1 5 1 32 1 1 v50 1024 1000`, ~12 min on 8 threads),
compared with `verify-it-yourself/diff_runs.py` (as in `../RUN_IT_YOURSELF.md`, Level 2).

## 4. Independent engine 2, lbb2 -> `branch_logs/lbb2_*`

```sh
cd engines
bash ../how-we-built-it/run_lbb2_parallel.sh ./lbb2 runs 50 10 11 1000000000      # 10:17:42 -> 10:41:55 PDT, 41 170 tasks
python3 ../verify-it-yourself/lbb2_aggregate.py runs/e50_S1000000000 > lbb2_agg_e50.json
(cd runs && tar czf lbb2_e50_S1000000000_tasks.tar.gz e50_S1000000000)
```
Confirmed: `lbb2_aggregate.py runs/e50_S1000000000` on the unpacked tarball reproduces `branch_logs/lbb2_agg_e50.json`
(`0ce7cefd…d0cf`) byte for byte (the `"dir"` field records the path given, so it must be `runs/e50_S1000000000`).
`lbb2_planted_final.out` is the output of `python3 engines/planted_cmp2.py 18` run next to the `lbb2` binary (49 of 49
configurations MATCH; the optional extra E = 18 case was stopped unfinished, so the file has no final ALL_MATCH line).
`lbb2_selftest.log` comes from `lbb2 -S 1000000000 -selftest LO HI` on [2·10^10, 2·10^10 + 10^7] and
[43 720 000 000, 43 725 000 000], plus a sympy `primerange` count of the second interval; the exact invocations and the
sympy one-liner were not recorded (the counts can be rechecked with the command in `../RUN_IT_YOURSELF.md`).

## 5. Packaging

The two author tarballs are `tar czf` of the run directories (`lcrt5_1e50/`, `lcrt6_1e50_bigsieve/`: `master.json`,
8 `tasks_w*_<pid>.jsonl`, `DONE`); their unpacked contents were checked file by file against the original run
directories. The vlrt2 `.gz` files are plain gzip of the task files (decompressed sha256 values in section 3).
The archive bytes themselves (gzip timestamps, member order) are not reproducible and do not matter:
compare unpacked contents, or use `verify-it-yourself/recompute_summary.py` and `diff_runs.py`.

## Not recoverable / not included

- The original part-2 and part-3 task-list and union steps were short inline Python; `vlrt2_union.py` is a
  re-implementation, verified byte for byte against every original file it replaces (table above).
- The exact `lbb2 -selftest` invocations and the sympy check line in `lbb2_selftest.log` (see section 4).
- Earlier engine generations (the 10^34-10^46 engines `lcap.c` and `lcrt.c`, and vlrt2's predecessor `vlrt.c`) are not
  needed for any shipped object and are not included.
