# How the codes and certificates were generated

This folder holds the code that produced the 30 files in `../codes/` and the 5 files in `../certificates/`, the
exact commands and random seeds for every one of them, and a manifest of the seed codes from A. E. Brouwer's archive
that the searches started from. The scripts are the ones that ran; they were copied from our working folders and
cleaned (comments and labels, file paths made command-line arguments). Algorithms, constants and random seeds are
unchanged. `SMOKE.md` records a rerun of the cleaned code: it reproduced three published codes (one from a stored
intermediate) and all five certificates byte for byte.

The checkers in `../verify-it-yourself/` share no code with anything here.

## Files

| file | what it does |
|---|---|
| `SEEDS.sha256`, `fetch_seeds.sh` | sha256 of the 28 archive seed files we used; `sh fetch_seeds.sh [DIR]` downloads them from `https://aeb.win.tue.nl/codes/cwc/<d>/<file>` (one GET per file, 1 s apart) and checks them |
| `convert_seed.py` | archive `$BASE=16` file → sorted `int64` array (`.npy`), the input of every engine (bit i of the integer = coordinate i) |
| `lb_lns.py` | plateau-walk exact LNS for d = 6 (the first engine) |
| `lb_lns_gen.py` | the same for any even d (two words conflict iff they share a (w − d/2 + 1)-subset) |
| `lb_lns_deep.py` | `lb_lns_gen.py` with deeper neighbourhoods: candidates with ≤ 4 blockers (`--kb 4`), removal sets up to 12 words, a sample of the 4-blocker sets as extra removal sets (`--max4`) |
| `lb_lns_inc.py`, `lb_lns_inc2.py` | the same neighbourhood with blocker counts kept incrementally instead of re-enumerating all C(n,w) words each round (`inc2`: faster table-driven subset ranks) |
| `lb_lns_fast.py`, `lb_lns_fast2.py`, `lb_lns_fast3.py` | `inc` + the move phase in numba (`fast`), + removal-set generation in numba (`fast2`), on `inc2` (`fast3`); same neighbourhood definition, only faster |
| `lns6.py`, `gslib.py` | shared numba helpers (subset ranks, owner array, exact bitset maximum-independent-set solver; colex enumeration) |
| `xwalk.py` | multi-seed screen + walk driver around `lb_lns_gen.py` (used for the five A(n,8,7), n = 52..56, codes) |
| `sidon.py`, `gs_run.py` | Graham–Sloane construction: Bose S2 set, all class sizes, the largest classes and their free words |
| `write_code.py` | union of one or more `.npy` word arrays → the published text format (sorted 0/1 strings, `format(x, '0nb')`) |
| `delsarte/make_certs.py`, `delsarte/cwlp.py` | exact Delsarte LP certificate for one cell (float HiGHS LP to guess the optimal basis, then exact rational solve and exact feasibility checks) |
| `requirements.txt` | Python package versions used |

### What one walk round does

1. One pass over all C(n,w) weight-w words lists every non-code word with at most KB *blockers* (codewords at
   distance < d from it).
2. Removal sets R: every blocker set of size 1..3 (`deep`/`inc`/`fast*`: plus a random sample of `--max4` blocker
   sets of size 4), and `--clusters` random connected clusters of up to `--rmax` codewords in the co-blocking graph.
3. For each R: the exact maximum independent set (bitset branch and bound) of {low-blocked words whose blockers all
   lie in R} ∪ R.
4. All disjoint improving moves (|MIS| > |R|) are applied; if there is none, a random 30 % (`--plateau-frac`) of the
   disjoint plateau moves (|MIS| = |R|, different words) is applied. The code is re-validated every round and
   `<out>_best.npy` is written whenever the size grows.

Every engine takes `SEED.npy N [D] W OUT_PREFIX [--rounds R] [--seconds S] [--seed X] [...]` (`lb_lns.py` has no
D argument) and writes `OUT_PREFIX.log`, `OUT_PREFIX_cur.npy`, `OUT_PREFIX_best.npy` and `OUT_PREFIX_best.json`.
The random choices come only from `--seed`, so a step is **deterministic**: the same input, seed and number of rounds
give the same output; the parallel loops write per-chunk results in a fixed order, so the thread count does not
matter (the A(34,8,7) rerun on 2 threads in `SMOKE.md` matched a run made with the numba default thread
count). The original runs were stopped by wall clock; to replay a step, pass `--rounds R` with the R given below (the round in which the published size was first
reached, plus one) and continue from `OUT_PREFIX_best.npy`.

## Environment of the original runs

macOS on an Apple M5 (10 cores, 32 GB), CPython 3.12.13 with `requirements.txt`. The machine was shared with other
jobs (load average 6 to 360), so the times below are wall clock under load, not benchmarks. The steps with
`--clusters` set ran with `NUMBA_NUM_THREADS=2`; the thread count of the first-day runs (`lb_lns.py`,
`lb_lns_gen.py`, `xwalk.py`) was not recorded (numba default = all cores). No GPU.

## Lineage of every published object

Every published code was traced by content: its sha256 (`../INDEX.csv`) equals `write_code.py` applied to the
`_best.npy` of the last step below, and each step's input equals, as a set of words, the output of the step before.
The first input is the archive file named in the seed column, converted with `convert_seed.py` (byte-identical to
the arrays the runs used, checked for all 23 seed files of these chains).

Argument presets: **D** = engine defaults (`--rmax 8 --kb 3 --clusters 3000 --plateau-frac 0.3`; these runs did not
log clusters/plateau-frac, but defaults reproduce the logged runs exactly, see `SMOKE.md`);
**P6k** = `--rmax 12 --kb 4 --clusters 6000 --max4 20000`; **P20k** = `--rmax 12 --kb 4 --clusters 20000 --max4 50000`;
**P50k** = `--rmax 12 --kb 4 --clusters 50000 --max4 50000`. The P20k/P50k steps also passed `--verify-every 100`
(`200` for A(28,8,9)), a periodic consistency recount that does not change the trajectory.
Step notation: `engine preset sS rR (t s)` = `engine IN.npy n [d] w OUT preset --seed S --rounds R`, which took t
seconds in the original run. `gen` = `lb_lns_gen.py`, `lns` = `lb_lns.py`, `deep`/`inc`/`fast`/`fast2`/`fast3` =
`lb_lns_deep.py`/`lb_lns_inc.py`/`lb_lns_fast*.py`.

| cell | M | seed (archive file) | steps (each continues from the previous `_best.npy`) | replay |
|---|---|---|---|---|
| A(25,6,11) | 8718 | `d6/a25.6.11.8698H` | lns D s5 r102 (2192 s) → fast P20k s51 r24 (144 s) | deterministic |
| A(25,6,12) | 9895 | `d6/a25.6.12.9880H` | lns D s3 r61 (1475 s) | deterministic |
| A(26,6,8) | 3603 | `d6/a26.6.8.3602H` | gen D s21 r3 (63 s) | deterministic |
| A(26,6,9) | 5986 | `d6/a26.6.9.5761H` | lns D s5 r138 (2164 s) → deep P6k s13 r46 (623 s) → fast3 P50k s103 r501 (1957 s) → fast3 P50k s204 r178 (960 s) | deterministic |
| A(26,6,11) | 12222 | `d6/a26.6.11.12206H` | lns D s5 r15 (437 s) | deterministic |
| A(26,6,13) | 16225 | `d6/a26.6.13.16117H` | lns D s3 r25 (2204 s) → deep P6k s12 r20 (1114 s) → fast P20k s32 r17 (242 s) → fast2 P50k s62 r58 (561 s) → fast3 P50k s102 r169 (1918 s) → fast3 P50k s202 r59 (992 s) | deterministic |
| A(27,6,9) | 8325 | `d6/a27.6.9.8324H` | lns D s5 r188 (879 s) | deterministic |
| A(27,8,10) | 1737 | `d8/a27.8.10.1728H` | gen D s43 r20 (566 s) → fast3 P20k s52 r2 (13 s) | deterministic |
| A(27,8,11) | 2421 | `d8/a27.8.11.2404H` | gen D s31 r5 (200 s) → fast3 P20k s52 r31 (112 s) → fast3 P50k s205 r154 (1003 s) | deterministic |
| A(28,8,9) | 1406 | `d8/a28.8.9.1376H` | fast3 P50k s141 r157 (843 s) | deterministic |
| A(28,8,11) | 3785 | `d8/a28.8.11.3773H` | gen D s21 r19 (1236 s) → fast P20k s51 r4 (154 s) | deterministic |
| A(28,8,12) | 4962 | `d8/a28.8.12.4927H` | gen D s21 r13 (1385 s) → inc P6k s22 r13 (260 s) → fast P20k s42 r6 (210 s) → fast2 P50k s72 r13 (454 s) → fast3 P50k s112 r157 (1643 s) → fast3 P50k s212 r40 (630 s) | deterministic |
| A(28,8,14) | 6359 | `d8/a28.8.14.6218H` | gen D s21 r6 (1414 s) → inc P6k s21 r5 (312 s) → fast P20k s41 r7 (240 s) → fast2 P50k s71 r20 (577 s) → fast3 P50k s111 r156 (1987 s) → fast3 P50k s211 r47 (900 s) | deterministic |
| A(29,6,10) | 25974 | `d6/a29.6.10.25896H` | lns D s9 r73 (2725 s) → fast P20k s34 r18 (233 s) → fast2 P50k s64 r26 (388 s) → fast3 P50k s104 r161 (1974 s) → fast3 P50k s203 r63 (1031 s) | deterministic |
| A(29,6,11) | 41219 | Graham–Sloane, Bose S2 set q = 29 in Z_840 | `gs_run.py 29 11 bose 29 --top 3` (the third-largest class, g = 825, 41215 words, has 4 free words, pairwise compatible; about 4 min in the original run) → `write_code.py A29_6_11_41219.txt 29 <out>/A29_6_11_bose29_g825_class.npy <out>/A29_6_11_bose29_g825_free.npy` | deterministic (exhaustive) |
| A(29,6,12) | 61823 | Graham–Sloane, Bose S2 set q = 29 in Z_840 | `gs_run.py 29 12 bose 29 --top 2` (the largest class, g = 400, 61820 words, has 3 free words; `--top 1` suffices, 2.5 min on 2 threads) → `write_code.py A29_6_12_61823.txt 29 <out>/A29_6_12_bose29_g400_class.npy <out>/A29_6_12_bose29_g400_free.npy` | **rerun in `SMOKE.md`: identical** |
| A(30,8,8) | 1166 | `d8/a30.8.8.1163H` | gen D s31 r4 (80 s) → gen D s41 r12 (166 s) | deterministic |
| A(33,8,8) | 1809 | `d8/a33.8.8.1800H` | gen D s31 r1 (76 s) → gen D s41 r14 (400 s) → fast P20k s51 r3 (101 s) → fast3 P50k s214 r45 (746 s) | deterministic |
| A(34,8,7) | 602 | `d8/a34.8.7.601H` | gen D s31 r2 (48 s) | **rerun in `SMOKE.md`: identical** |
| A(34,8,8) | 1965 | `d8/a34.8.8.1949H` | gen D s31 r1 (121 s) → gen D s41 r15 (571 s) → deep P6k s16 r12 (613 s) → fast P20k s44 r5 (157 s) → fast2 P50k s74 r11 (342 s) → fast3 P50k s114 r73 (962 s) | deterministic |
| A(35,6,6) | 2217 | `d6/a35.6.6.2209H` | gen D s31 r4 (86 s) → gen D s41 r20 (288 s) → fast3 P20k s52 r50 (149 s) | deterministic |
| A(45,8,7) | 1907 | `d8/a45.8.7.1904H` | gen D s43 r10 (501 s) → fast3 P20k s52 r9 (106 s) | deterministic |
| A(51,6,5) | 1785 | `d6/a51.6.5.1783H` | gen D s31 r4 (51 s) | deterministic |
| A(51,6,6) | 11184 | `d6/a51.6.6.11156H` | gen D s31 r2 (78 s) → gen D s41 r22 (607 s) → deep P6k s14 r19 (682 s) | deterministic |
| A(52,8,7) | 3799 | `d8/a52.8.7.3797H` | xwalk screen (1 round) → xwalk walk, reached in round 7 (93 s) | **not byte-reproducible** (see below) |
| A(53,8,7) | 3987 | `d8/a53.8.7.3980H` | xwalk screen → xwalk walk, round 23 (263 s) | not byte-reproducible |
| A(54,8,7) | 4193 | `d8/a54.8.7.4173H` | xwalk screen → xwalk walk, round 20 (294 s) | not byte-reproducible |
| A(55,8,7) | 4426 | `d8/a55.8.7.4417H` | xwalk screen → xwalk walk, round 16 (266 s) | not byte-reproducible |
| A(56,8,7) | 4685 | `d8/a56.8.7.4674H` | xwalk screen → xwalk walk, round 17 (299 s) | not byte-reproducible |
| A(58,6,5) | 2684 | `d6/a58.6.5.2678H` | gen D s31 r3 (84 s) → gen D s41 r13 (217 s) → fast3 P20k s52 r17 (66 s) | deterministic |

"deterministic" means: the scripts and arguments above define the output uniquely, and the step type was shown to
replay exactly (`lb_lns_gen.py` and `gs_run.py` end to end, `lb_lns_fast3.py` for one step, `lb_lns.py` for one
round, see `SMOKE.md`; `lb_lns_deep/inc/fast/fast2.py` use the same seeded construction but were not rerun); the long chains themselves were not rerun (hours of CPU). If a replay drifts (e.g. a different numba
or numpy version), a walk with the same arguments and a few more rounds is still expected to reach the same size or
more, as the independent restarts in our runs did, but not necessarily the same file.

### Example: A(35,6,6) from the archive seed

```sh
export NUMBA_NUM_THREADS=2
sh fetch_seeds.sh seeds
python3 convert_seed.py seeds/d6/a35.6.6.2209H 35 6 s0.npy
python3 lb_lns_gen.py s0.npy 35 6 6 st1 --seed 31 --rounds 4
python3 lb_lns_gen.py st1_best.npy 35 6 6 st2 --seed 41 --rounds 20
python3 lb_lns_fast3.py st2_best.npy 35 6 6 st3 --rmax 12 --kb 4 --clusters 20000 --max4 50000 --verify-every 100 --seed 52 --rounds 50
python3 write_code.py A35_6_6_2217.txt 35 st3_best.npy
shasum -a 256 A35_6_6_2217.txt        # expected 3bc77f117eb9...1459 (../INDEX.csv)
python3 ../verify-it-yourself/cwcheck.py A35_6_6_2217.txt 35 6 6
```

### The five A(n,8,7) codes, n = 52..56 (`xwalk.py`)

1. Screen (one round of `lb_lns_gen` moves on each archive file, KB = 3, |R| ≤ 8, defaults otherwise):
   `xwalk.py screen LIST1 screen/`, where `LIST1` has lines `seeds/d8/a52.8.7.3797H 52 8 7` etc.; this writes
   `screen/A52_8_7_a52.8.7.3797H_cur.npy` (3798, 3982, 4174, 4418, 4676 words for n = 52..56).
2. Walk: `xwalk.py walk LIST2 walk/ --per-seed 300 --kb 3 --rmax 8 --plateau-frac 0.6 --seed 7`, where `LIST2` has
   lines `screen/A52_8_7_a52.8.7.3797H_cur.npy 52 8 7 A52_8_7_Bo_walk` etc. The published codes are the
   `walk/<tag>_best.npy` states at the end of this first 300-second pass (rounds above), written out with
   `write_code.py`. The walk kept running afterwards and found larger codes (e.g. 3802 for n = 52), which were not
   verified or published.

`xwalk.py` seeds each cell's random generator with `--seed` plus Python's `hash()` of the tag string, and string
hashing is randomised per process unless `PYTHONHASHSEED` is set; the original runs did not set it. So the exact
trajectories of these five codes are **not recoverable**; a rerun (with any `PYTHONHASHSEED`) runs the same
algorithm and is expected to reach codes of similar size in similar time, not the same files. What we have is the
original logs: sizes 3797 → 3798 → 3799 (n = 52), 3980 → 3982 → 3987, 4173 → 4174 → 4193, 4417 → 4418 → 4426,
4674 → 4676 → 4685.

### The five Delsarte certificates

```sh
cd delsarte
for c in "31 12 10" "31 12 11" "32 12 10" "32 12 15" "32 12 16"; do python3 make_certs.py $c out; done
```
(in zsh write `${=c}`). Seconds in total; the output files are byte-identical to `../certificates/` (`SMOKE.md`).

## What is not here

- The seed codes themselves (other people's work; fetch them with `fetch_seeds.sh`). If the archive has replaced a
  file since 2026-10-08, the copy we used is identified only by its sha256 in `SEEDS.sha256`.
- Experiments that did not contribute to any published file (a random-removal LNS, bipartite crossover of two
  codes, a tabu search at fixed size, a second-moment / SDP upper-bound line, Johnson-composition seeds).
- Job launchers, harvesting and reporting scripts: they only moved files between folders and ran the checkers.
