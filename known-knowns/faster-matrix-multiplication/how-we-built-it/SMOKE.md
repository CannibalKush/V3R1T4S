# Smoke run of the cleaned code (2026-10-11; section 4 added 2026-10-12)

Run from the repository copy of this folder, with outputs in a scratch directory `$S` (not in the repository).
Environment: Apple M5 (10 cores, other jobs running, load ~15), macOS, Python 3.12.13, numpy 2.5.3,
`nice -n 10`, `OMP_NUM_THREADS=2`. `$HWB` is this folder, `$FMM` the family folder.

## 0. Inputs

The four LITA files cached by the original run (downloaded 2026-10-09 UTC) were copied to `$S/lita/`; `fetch_lita.sh`
found them present (so no download) and confirmed the pinned sha256 of all four:
```
$ sh $HWB/fetch_lita.sh lita
OK   15x15x15_r1977.npz
OK   14x14x14_r1593.npz
OK   16x16x16_r2236.npz
OK   13x13x13_r1379.npz
```
Their git blob hashes equal those listed for `schemes/` in the tree of LITA commit 472a79fb… (recorded during the run).

## 1. One LITA peel: <14,15,15>:1843 from 15x15x15_r1977.npz

```
$ python3 -I $HWB/make_scheme.py lita/15x15x15_r1977.npz n "1 1 1 1 1 1 1 -5 1 1 1 1 1 1 1" \
      "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0" regen/14x15x15_r1843_Q.json
 "source_terms": 1977, "projected_format": [14, 15, 15], "projected_terms_nonzero": 1843, ...   (real 39.6 s)
$ shasum -a 256 regen/14x15x15_r1843_Q.json
c86dba238db8a26bef6a4e8f5e224e8524e5d61cd0b89625fe34b43e27813ac3      (= INDEX.csv)
$ python3 -I $FMM/verify-it-yourself/fmmcheck.py regen/14x15x15_r1843_Q.json | tail -2
  checked 210*225*210 = 9922500 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 32.9
FMMCHECK PASS file=14x15x15_r1843_Q.json format=<14,15,15> sorted=<14,15,15> terms=1843 rank_nonzero_terms=1843 sha256=c86dba23...3ac3   (real 36.8 s)
```

## 2. The sweep picks the same direction pair

```
$ python3 -I $HWB/sweep.py --axes n --out sweep/peel_15n.csv --candidates sweep/candidates --force lita/15x15x15_r1977.npz
[CANDIDATE] sweep/candidates/14x15x15_r1843_from_15x15x15_r1977.npz_n.json: 1843 terms < bar 1848 for 14x15x15 (ring Q)
15x15x15_r1977.npz: fmt 15x15x15 ring Q r=1977 16.0s
```
CSV row: `coord_best_z=30 coord_best_idx=7 gen_best_z=134 e="1 1 1 1 1 1 1 -5 1 1 1 1 1 1 1" f="1 0 … 0" n_e_rank1=377
n_f_rank1=377 est_rank=1843`, the same values as the original run's row; the candidate file has sha256 c86dba23…3ac3.
The third-stage sweep on `$FMM/schemes/14x14x15_r1716_Q.json` (45 s, all axes) also reproduced the original rows
(n: coordinate 29, generalised 39 → 1677; m: 37 / 38 → 1678; p: 22 / 120 → <14,14,14> 1596, not built since the bar is 1593)
and wrote the 1677 candidate with sha256 4230f61d…d6bc (= INDEX.csv).

## 3. All five schemes

```
$ sh $HWB/regenerate_all.sh lita regen_all
 projected_terms_nonzero 1843 (13.8 s), 1558 (26.2 s), 2196 (40.0 s), 1716 (34.3 s), 1677 (20.4 s)
IDENTICAL 14x15x15_r1843_Q.json
IDENTICAL 13x14x14_r1558_Q.json
IDENTICAL 15x16x16_r2196_Q.json
IDENTICAL 14x14x15_r1716_Q.json
IDENTICAL 13x14x15_r1677_Q.json
real 158.3 s   (exit 0)
$ python3 -I $FMM/verify-it-yourself/fmmcheck.py regen_all/13x14x15_r1677_Q.json | tail -1
FMMCHECK PASS file=13x14x15_r1677_Q.json format=<13,14,15> sorted=<13,14,15> terms=1677 rank_nonzero_terms=1677 sha256=4230f61d...d6bc
```

**Result: as expected.** All five regenerated files are byte-identical to `../schemes/` (sha256 as in `../INDEX.csv`),
and the two that were re-checked here pass `fmmcheck.py` with the claimed ranks (the other three are byte-identical
to files whose check is recorded in `../verify-it-yourself/RECEIPTS.md`).

## 4. Absorption: 1843 → 1842 and 2196 → 2180 (2026-10-12)

Run from a scratch directory `$S` holding copies of `$FMM/schemes/14x15x15_r1843_Q.json` and
`$FMM/schemes/15x16x16_r2196_Q.json` (same names). Environment: the same machine (load ~3), Python 3.12.13,
numpy 2.5.3, numba 0.68.0 (`NUMBA_CACHE_DIR` in `$S`, cold cache), `nice -n 10`, `OMP_NUM_THREADS=2`.
2026-10-12T18:07:50Z to 18:18:51Z.

```
$ python3 -I -B $HWB/absorb_exact.py 14x15x15_r1843_Q.json regen_14x15x15_r1842.json
{"round": 0, "pairing": "vw", "r": 1843, "nullity": 1, "pivot_terms": [1628], "exact_ok": true, "max_den": 1, "max_num": 1, "r_new": 1842, "sec": 158.7}
{"round": 0, "pairing": "uw", "r": 1842, "rank_modp": [1842, 1842, 1842], "nullity": 0, "sec": 40.3}
{"round": 0, "pairing": "uv", "r": 1842, "rank_modp": [1842, 1842, 1842], "nullity": 0, "sec": 41.1}
{"round": 1, "pairing": "vw", "r": 1842, "rank_modp": [1842, 1842, 1842], "nullity": 0, "sec": 40.4}
{"round": 1, "pairing": "uw", "r": 1842, "rank_modp": [1842, 1842, 1842], "nullity": 0, "sec": 40.9}
{"round": 1, "pairing": "uv", "r": 1842, "rank_modp": [1842, 1842, 1842], "nullity": 0, "sec": 41.9}
{"final_r": 1842, "out": "regen_14x15x15_r1842.json"}
real 365.6 s
$ python3 -I -B $HWB/maxkill.py 15x16x16_r2196_Q.json uv regen_15x16x16_r2180.json regen_2180_cert.json
{"src": "15x16x16_r2196_Q.json", "pairing": "uv", "r": 2196, "rank_modp": [2188, 2188, 2188], "nullity": 8,
 "rref_pivots": [0, 4, 19, 34, 49, 64, 79, 94], "blocks": {"0": 55, "1": 76, ..., "7": 88}, "hubs": [1344, 1349, 2009, 2012],
 "killed": [1348, 1350, 1474, 1476, 1491, 1493, 1508, 1510, 1525, 1527, 1542, 1544, 1559, 1561, 1998, 2003],
 "n_killed": 16, "r_new": 2180, ...}
real 270.4 s
$ shasum -a 256 regen_14x15x15_r1842.json regen_15x16x16_r2180.json
c3e9a07824ea5e7e0128a481a32ab86ca7aab7900237242bd25db6bb3df703a2  regen_14x15x15_r1842.json
7be47d819f764bbb78156d7ef04bde2da9213f567eaae0ab9f018af73cc38637  regen_15x16x16_r2180.json
$ python3 -c "... all(A[k]==B[k] for k in 'uvw') ..."      # against $FMM/schemes/*_r1842_Q.json, *_r2180_Q.json
regen_14x15x15_r1842.json u,v,w identical term-for-term to 14x15x15_r1842_Q.json: True 1842 1842 n True
regen_15x16x16_r2180.json u,v,w identical term-for-term to 15x16x16_r2180_Q.json: True 2180 2180 n True
$ python3 -I -B $FMM/verify-it-yourself/fmmcheck.py regen_14x15x15_r1842.json | tail -1      (4.7 s)
FMMCHECK PASS file=regen_14x15x15_r1842.json format=<14,15,15> sorted=<14,15,15> terms=1842 rank_nonzero_terms=1842 sha256=c3e9a078...03a2
$ python3 -I -B $FMM/verify-it-yourself/fmmcheck.py regen_15x16x16_r2180.json | tail -1      (19.7 s)
FMMCHECK PASS file=regen_15x16x16_r2180.json format=<15,16,16> sorted=<15,16,16> terms=2180 rank_nonzero_terms=2180 sha256=7be47d81...8637
```
(each `fmmcheck.py` run also printed `violated Brent equations = 0` for all four primes.)

**Result: as expected, term for term.** The two tools are deterministic, and their outputs have exactly the u, v, w
arrays (same terms, same order, same coefficient strings) and `n` of the shipped `14x15x15_r1842_Q.json` (sha256
bb313b87…c6b5) and `15x16x16_r2180_Q.json` (sha256 8365355f…fd1d). The **file** sha256 differs because the header
fields differ: the shipped files carry the `note` (2180) or `source`/`method`/`dependency` (1842) fields written by the
tools that first produced them (see "Lineage" in `README.md`). Both regenerated files pass `fmmcheck.py` with ranks
1842 and 2180.
