# Smoke runs of the (13,4) search code (2026-10-11)

Run from the repository copies in `13_4/search/`, working directory `how-we-built-it/13_4/`, outputs in a scratch
directory (written `$OUT` below). Machine: Apple M5 laptop (10 cores, shared with other jobs, load 20–40), macOS 27.0,
Python 3.12.13 with numpy 2.5.3, numba 0.68.0, llvmlite 0.50.0, scipy 1.18.1, networkx 3.7. Every run single-threaded
under `nice -n 10` with

```sh
export NUMBA_CACHE_DIR=$OUT/numba_cache PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
```

The searches for the other cells were rerun from their repo copies as well; the commands and results are in
`15_4/search/README.md`, `15_3/search/README.md`, `14_4/search/README.md` and `9_4/search/README.md` (all
byte-identical to the shipped parameters).

## 1. Tiny case: two insertions into the Petersen graph, as a (4,2) search (seconds)

`$OUT/petersen.edges` is the Petersen graph (outer 5-cycle 0–4, spokes i–(i+5), inner pentagram), 15 edges.

```sh
python3 search/insert_step.py $OUT/petersen.edges --delta 4 --diam 2 --k 2 --iters 20000 --seed 1 --out $OUT/out1 --tag pet
#  {"n": 12, "seed": 1, "init": 2, "best": 0, "best_recheck": 0, "acc": 4, "nfull": 3, "nscreen": 10, "verified_diam": 2, "maxdeg": 4, ...}
#  real 1.2 s;  sa2hit_pet_4_2_N12_s1.edges sha256 3985b96f109bbb91ab31b3702a412af900cd1b4c9467877bc49df8ee68226db1

# spec: [{"seed": "$OUT/petersen.edges", "delta": 4, "diam": 2, "tag": "t42", "iters": 2e4, "retries": 3, "seed0": 0}]
python3 search/chain.py --spec $OUT/spec.json --out $OUT/chain
#  chain_t42.log: 10 -> 11 (seed 1) -> 12 (seed 2) -> 13 -> 14 -> 15 (seed 5, valid_t42_4_2_N15.edges sha256 1a0d28dd...8bde8),
#  then 3 near-misses at N=16 with 2 far pairs each and "STUCK at N=15 after 3 consecutive failures";  real 2.5 s
```
15 is the proven maximum for (4,2) (bold in the table), so stopping there is the expected behaviour. A second run
into a fresh directory gave byte-identical `valid_*` files and identical near-miss edge lines (near-miss headers
contain the output path).

## 2. The real (13,4) chain: three steps rerun against the original files

| step | command | runtime | result |
|---|---|---|---|
| seed decode | `python3 search/decode_sage.py 6611_rishabhrajiv_SageMath.txt 6611 $OUT/G_13_4_n6611_rajiv.edges` (input sha256 `c0859737…c467`) | 5 s | `f6953f1a…d936`, identical to the original decode |
| loader check | `ddlib.load_graph` vs the original checker's parser on the 6 611, 6 612, 6 629-pruned and Petersen files | seconds | same N and identical edge arrays |
| 6 611 -> 6 612 | `python3 search/insert_step.py $OUT/G_13_4_n6611_rajiv.edges --delta 13 --diam 4 --k 1 --iters 100000 --T0 0.6 --T1 0.05 --seed 1 --out $OUT/step1 --tag t6611` | 84 s | init 77, best 0, acc 78, nfull 85; `sa2hit_t6611_13_4_N6612_s1.edges` sha256 `48a2f7d929da424f625ac8ab4b4c6192d68ec2ef08bc10f85f578257db70b7b5`, **byte-identical** to the original 6 612 graph |
| near-miss attempt | `python3 search/chain_step.py valid_c134_13_4_N6629_pruned.edges --delta 13 --diam 4 --seed 13064 --iters 2e5 --T0 0.6 --out $OUT/near_s13064.edges` (input: the original chain file, identical to `valid_c134_13_4_N6629_pruned.edges.gz` decompressed, sha256 `46ce5e24…ca53`) | 976 s wall, 403 s CPU | `N->6630 seed 13064: init 126 best 2 acc 94 full 273 screened 159655`, the original log line; edge lines **identical** to `near_miss_N6630_cost2.edges` |
| final step | `python3 search/sa2_resume.py $OUT/near_c134_N6630_s13064_c2.edges 13 4 $OUT/sa2c2 --iters 250000 --T0 0.12 --T1 0.02 --seeds 101` (input: `near_miss_N6630_cost2.edges` copied to that name) | 205 s wall, 53 s CPU | `seed 101: sa2 best 0 (fresh re-eval 0) acc 3 full 13 screened 9559`; `sa2c2_s101_c0.edges` sha256 `7c44e128901d6dd6b64e0574b90ff8aa21872462338fd267bab466cb268e10a4`, **byte-identical** to `graphs/G_13_4_n6630.edges` |
| edge-set check | `python3 apply_diff.py near_miss_N6630_cost2.edges G_13_4_n6630.diff_vs_near_miss.txt ../../graphs/G_13_4_n6630.edges` | < 1 s | `near-miss edges 43086, removed 5, added 5, result 43086, shipped graph 43086` / `EDGE SETS IDENTICAL` |

All outputs matched expectation. Not rerun: the two chains as a whole (6 612 -> 6 614, about 20 minutes; 6 614 ->
6 629 plus 30 near-miss attempts, about 17 hours originally).
