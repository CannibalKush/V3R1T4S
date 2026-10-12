# Smoke runs of the cleaned code (2026-10-11)

All runs used the scripts in this folder (not the original working copies), from a scratch directory, on the same
machine as the original runs (Apple M5, macOS, CPython 3.12.13, numpy 2.5.3, numba 0.68.0, scipy 1.18.1), under
`nice -n 10` with

```sh
export NUMBA_NUM_THREADS=2 OMP_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 NUMBA_CACHE_DIR=<scratch>/numba_cache
K=<repo>/known-knowns/bigger-codes; H=$K/how-we-built-it      # commands run from the scratch directory
```

Times include numba compilation (about 30–60 s per engine on a cold cache). The seed files were local copies of the
archive files with the sha256 values in `SEEDS.sha256`.

## 1. A(34,8,7) = 602 from the archive seed: identical to the published file

```sh
python3 $H/convert_seed.py a34.8.7.601H 34 7 A34_8_7_seed.npy      # a34.8.7.601H sha256 5fad3b52...8528
python3 $H/lb_lns_gen.py A34_8_7_seed.npy 34 8 7 walk_d8_34_7 --seed 31 --rounds 2
python3 $H/write_code.py A34_8_7_602.txt 34 walk_d8_34_7_best.npy
shasum -a 256 A34_8_7_602.txt
python3 $K/verify-it-yourself/cwcheck.py A34_8_7_602.txt 34 8 7
```
```
A34_8_7_seed.npy 601 hex
start A34_8_7_seed.npy M=601 n=34 d=8 w=7 rmax=8 KB=3 seed=31
  analyse: 3671 low-blocked words, by #blockers [0, 51, 627, 2993] (38s)
  moves: 6320 removal sets, 5330 MIS solved, improving=0 plateau=2049 (27s)
round 0: M=601 gain=0 applied=27 best=601 t=65s
  analyse: 3023 low-blocked words, by #blockers [0, 46, 526, 2451] (8s)
  moves: 5774 removal sets, 4879 MIS solved, improving=8 plateau=2026 (5s)
round 1: M=602 gain=1 applied=1 best=602 t=78s
done best=602
real 80.89
A34_8_7_602.txt 602
1a1d0958047e78b8d29752ccb0210518b170663b6862f84d57669c7b0c02d81e  A34_8_7_602.txt
A all-pairs: words=602 pairs=180901 expected=180901 min_distance=8 need>=8 histogram={8: 32414, 10: 44914, 12: 75763, 14: 27810}
B packing: t=4 subsets=21070 distinct=21070 collisions=0
VERDICT: VALID  A(34,8,7) >= 602
```
**Matches** `codes/A34_8_7_602.txt` (sha256 in `../INDEX.csv`). The blocker histograms and move counts are the same
numbers as in the original 2026-10-06 log, round for round.

## 2. Five Delsarte certificates: identical to the published files

```sh
for c in "31 12 10" "31 12 11" "32 12 10" "32 12 15" "32 12 16"; do python3 $H/delsarte/make_certs.py ${=c} certs; done   # zsh
python3 $K/verify-it-yourself/delsarte_check.py certs/cert_A*.json
```
```
A(31,12,10): float 197.341463  exact LP optimum 8091/41 = 197.341463  -> U = 197
A(31,12,11): float 380.255875  exact LP optimum 145638/383 = 380.255875  -> U = 380
A(32,12,10): float 245.724771  exact LP optimum 26784/109 = 245.724771  -> U = 245
A(32,12,15): float 2511.307517  exact LP optimum 1102464/439 = 2511.307517  -> U = 2511
A(32,12,16): float 2652.347682  exact LP optimum 801009/302 = 2652.347682  -> U = 2652
ALL CERTIFICATES VALID
```
Each regenerated JSON has the same sha256 as `../certificates/cert_A*.json` (**byte-identical**). A few seconds in total.

## 3. A(29,6,12) = 61823, Graham–Sloane class + free words: identical

```sh
python3 $H/gs_run.py 29 12 bose 29 --top 1 --out gs_out
python3 $H/write_code.py A29_6_12_61823.txt 29 gs_out/A29_6_12_bose29_g400_class.npy gs_out/A29_6_12_bose29_g400_free.npy
shasum -a 256 A29_6_12_61823.txt
```
```
A(29,6,12) bose q=29 m=840: C(n,w)=51895935 avg=61780.88 max=61820 at g=400  top10=[61820, 61820, 61815, ...]  (47.4s)
  g=400: class=61820 free=3 in 3 classes, max per class=1 (97.9s)
real 150.18
A29_6_12_61823.txt 61823
d467400b0827c8db81a1c9348317ca1d645c049d6cb54fdf5b927964490e4d2f  A29_6_12_61823.txt
```
**Matches** `codes/A29_6_12_61823.txt`.

## 4. One `lb_lns_fast3.py` step (determinism of the faster engines)

Input: the intermediate 1736-word A(27,8,10) code written by the first-day walk (sha256 of the `.npy`
`b9f1496f...e1`; it is not shipped, it is step 1 of the A(27,8,10) chain in `README.md`).

```sh
python3 $H/lb_lns_fast3.py A27_8_10_1736_intermediate.npy 27 8 10 t_d8_27_10 --rounds 2 --rmax 12 --kb 4 \
    --clusters 20000 --max4 50000 --verify-every 100 --seed 52
python3 $H/write_code.py A27_8_10_1737.txt 27 t_d8_27_10_best.npy; shasum -a 256 A27_8_10_1737.txt
```
```
  analyse(inc): 11614 low-blocked words, by #blockers [0, 604, 1887, 3461, 5662] (18.2s); 30365 removal sets (17.2s); ...
round 0: M=1736 gain=0 applied=165 best=1736 t=116s
  analyse(inc): 11074 low-blocked words, by #blockers [0, 600, 1701, 3387, 5386] (0.1s); 29920 removal sets (0.7s); ...
round 1: M=1737 gain=1 applied=1 best=1737 t=118s
real 122.90
5a9ef07f5d958179ac069f546c43914147ac041f0c10e80a2229ea3d1287a05f  A27_8_10_1737.txt
VERDICT: VALID  A(27,8,10) >= 1737          (cwcheck.py)
```
**Matches** `codes/A27_8_10_1737.txt`; the counts equal those of the original 2026-10-08 log.

## 5. One round of `lb_lns.py` (the d = 6 engine)

```sh
python3 $H/convert_seed.py a26.6.11.12206H 26 11 A26_6_11_seed.npy
python3 $H/lb_lns.py A26_6_11_seed.npy 26 11 walk_26_11 --seed 5 --rounds 1
```
```
  moves: 18870 removal sets, 18147 MIS solved, improving=7 plateau=4855 (31s)
round 0: M=12210 gain=4 applied=4 best=12210 t=64s
real 77.13
```
Same counts and size as round 0 of the original walk that produced `codes/A26_6_11_12222.txt` (15 rounds); the
remaining 14 rounds were not rerun.

## Not rerun

The long chains (up to six steps and about 2 hours each in the original runs), and the five A(n,8,7) walks of
`xwalk.py`, whose original random streams cannot be recovered (see `README.md`).
