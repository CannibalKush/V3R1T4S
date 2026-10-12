# How we built it: generalised one-slice peels of LITA's square schemes, then absorption

This folder holds the code that produced the seven scheme files in `../schemes/`: five by peeling (below), and the two
2026-10-12 records <14,15,15>:1842 and <15,16,16>:2180 by absorbing linear dependencies of the peeled 1843 and 2196
(section "Absorption"). It is the code the AI agents ran, cleaned (paths made relative, command-line paths to helper
modules replaced by the script's own folder, internal labels removed, unused experiments dropped); the algorithms,
their tie-breaking and seeds, and the JSON output format are unchanged. Rerunning the peels gives files that are
**byte-identical** to the published ones; rerunning the absorptions gives the published 1842 and 2180 **term for
term** (identical u, v, w; only the JSON header fields differ). Checked: see "Lineage" below and `SMOKE.md`.

## Files

| file | what it does |
|---|---|
| `peel.py` | Library: loaders for LITA `.npz` and Perminov-style `.json` schemes, `peel_census` (finds the direction pair (e, f) that kills the most terms on one axis), `project` (builds the restricted scheme for a given (e, f), exact rational arithmetic), JSON writer. The docstring states the restriction lemma. |
| `sweep.py` | For each input scheme and each axis: best coordinate peel, best generalised peel, estimated rank r − z; builds the restriction when it is within `--margin` of the bar and writes it if it is below. This is how the direction pairs were chosen. |
| `make_scheme.py` | Rebuilds one scheme from a source file, an axis and a given direction pair (no search). |
| `fetch_lita.sh` | Downloads the four LITA input files at a pinned commit and checks their sha256 (they are not redistributed here). |
| `regenerate_all.sh` | Runs `make_scheme.py` five times (three single peels, then the two-step chain 1843 → 1716 → 1677) and compares each output's sha256 with `../INDEX.csv`. |
| `bars_2026-10-08.csv` | The bars `sweep.py` compared against: the smallest rank listed by the four criterion sources as pinned on 2026-10-08T23:42Z, and LITA's ranks for the four squares. Only used to decide what to build. |
| `absorb_exact.py` | Iterated exact absorption: for each pairing (v⊗w, u⊗w, u⊗v), computes the left nullspace of the pair factors (modulo three primes, CRT, rational reconstruction, every null vector checked exactly over Q), removes one pivot term per dependency, and repeats until all three pairings have full rank. Made 1843 → 1842. |
| `maxkill.py` | Exact absorption of one pairing's nullspace with the best shift per dependency (the normalised free factor that occurs most often), so that more than one term per dependency can die; also writes a certificate (null rows, shifts, killed terms). Made 2196 → 2180. |
| `pairtools.py` | Library for the two above: modular matrix product and row reduction (numba), Khatri-Rao projected pairing matrix. |
| `requirements.txt` | numpy (for the `.npz` loader and the absorption tools) and numba (absorption tools only); everything else is the Python standard library. |

## Inputs (not included: LITA's repository states no license)

github.com/khoruzhii/lita at commit `472a79fbc8248423a97bebb3aacbc89e769b9b3e` (2026-10-07T19:22:13Z), folder `schemes/`:

| file | sha256 | used for |
|---|---|---|
| `15x15x15_r1977.npz` | `94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33` | <14,15,15>:1843, then 1716 and 1677 |
| `14x14x14_r1593.npz` | `e80390259e0b7f58192f6167595e3da9b57142402665de44e489338a26941110` | <13,14,14>:1558 |
| `16x16x16_r2236.npz` | `af5fd100931c22721b7f60277325a430d92b63e60e59a95dc2dd132a7b8767da` | <15,16,16>:2196 |
| `13x13x13_r1379.npz` | `9df0b464793e3c9584c9e95e48dc748a4774afa07bd1b7aa7e6d4421570b40eb` | swept only (near miss, see below) |

The agent fetched these files from the `main` branch on 2026-10-09 (UTC); their git blob hashes equal those of the
pinned commit, which was `main` at the time. `sh fetch_lita.sh lita` downloads them (one GET each) and checks the sha256.

## Regenerate the five schemes

From this folder (python3 with numpy):
```sh
sh fetch_lita.sh lita                 # 4 files, 0.6 MB
sh regenerate_all.sh lita regen       # writes regen/*.json, prints IDENTICAL/DIFFERENT per scheme
python3 ../verify-it-yourself/fmmcheck.py regen/*.json
```
Expected: `IDENTICAL` for all five (sha256 as in `../INDEX.csv`) and `FMMCHECK PASS` with ranks 1843, 1558, 2196,
1716, 1677. The individual commands (exactly those in `regenerate_all.sh`):

| scheme | command |
|---|---|
| <14,15,15>:1843 | `python3 make_scheme.py lita/15x15x15_r1977.npz n "1 1 1 1 1 1 1 -5 1 1 1 1 1 1 1" "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0" regen/14x15x15_r1843_Q.json` |
| <13,14,14>:1558 | `python3 make_scheme.py lita/14x14x14_r1593.npz n "0 1 0 0 0 0 0 0 1 0 0 0 0 0" "1 -1 0 0 0 0 0 0 0 0 0 0 0 0" regen/13x14x14_r1558_Q.json` |
| <15,16,16>:2196 | `python3 make_scheme.py lita/16x16x16_r2236.npz n "0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0" "1 -1 0 0 0 0 0 0 0 0 0 0 0 0 0 0" regen/15x16x16_r2196_Q.json` |
| <14,14,15>:1716 | `python3 make_scheme.py regen/14x15x15_r1843_Q.json m "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0" "1 1 1 1 1 1 1 -5 1 1 1 1 1 1 1" regen/14x14x15_r1716_Q.json` |
| <13,14,15>:1677 | `python3 make_scheme.py regen/14x14x15_r1716_Q.json n "0 1 0 0 0 0 0 0 0 1 0 0 0 0" "0 1 0 0 0 0 0 0 0 0 0 0 0 0" regen/13x14x15_r1677_Q.json` |

The `note` field written into each file names the source file by its base name, so the outputs are byte-identical
only when the inputs keep the names above (for the chained steps: the published names `14x15x15_r1843_Q.json` and
`14x14x15_r1716_Q.json`; you can equally pass `../schemes/14x15x15_r1843_Q.json` etc.).

## Absorption: 1843 → 1842 and 2196 → 2180

Needs numpy and numba (`requirements.txt`). Both tools are deterministic (fixed seeds; the canonical row-reduced
nullspace basis does not depend on them). From this folder:
```sh
python3 absorb_exact.py ../schemes/14x15x15_r1843_Q.json regen/14x15x15_r1842.json
python3 maxkill.py ../schemes/15x16x16_r2196_Q.json uv regen/15x16x16_r2180.json regen/15x16x16_r2180_cert.json
python3 ../verify-it-yourself/fmmcheck.py regen/14x15x15_r1842.json regen/15x16x16_r2180.json
```
(`regen/14x15x15_r1843_Q.json` and `regen/15x16x16_r2196_Q.json` from `regenerate_all.sh` work equally, since they are
byte-identical to the shipped parents.) Expected output:

- `absorb_exact.py`: round 0, pairing `vw`: `"nullity": 1, "pivot_terms": [1628], "exact_ok": true, "r_new": 1842`; then
  every pairing reports `"nullity": 0` and the last line is `"final_r": 1842`.
- `maxkill.py`: `"nullity": 8`, `"n_killed": 16`, `"r_new": 2180`.
- `fmmcheck.py`: `FMMCHECK PASS` with `rank_nonzero_terms=1842` and `rank_nonzero_terms=2180`.

The outputs are **term-for-term identical** (same u, v, w, same order) to `../schemes/14x15x15_r1842_Q.json` and
`../schemes/15x16x16_r2180_Q.json`, but not byte-identical: the shipped files carry the header fields (`note`, or
`source`/`method`/`dependency`) written by the tools that first produced them (see "Lineage"), so compare the u, v, w
arrays, e.g.
```sh
python3 -c "import json,sys; a,b=(json.load(open(f)) for f in sys.argv[1:]); print(all(a[k]==b[k] for k in 'nuvw'))" \
    regen/15x16x16_r2180.json ../schemes/15x16x16_r2180_Q.json
```
Runtime: a few minutes each (several eliminations of a ~2000 × ~2000 matrix modulo three primes); `SMOKE.md` has
a recorded run.

## Find the direction pairs (the sweep)

```sh
python3 sweep.py --out sweep/lita.csv --candidates sweep/candidates \
    lita/13x13x13_r1379.npz lita/15x15x15_r1977.npz lita/14x14x14_r1593.npz lita/16x16x16_r2236.npz
python3 sweep.py --out sweep/stage2.csv --candidates sweep/candidates ../schemes/14x15x15_r1843_Q.json
python3 sweep.py --out sweep/stage3.csv --candidates sweep/candidates ../schemes/14x14x15_r1716_Q.json
```
`peel_census` is deterministic (groups terms by the exact rational direction of their rank-one factors, ties broken
by term order), so the CSV columns `e`, `f`, `gen_best_z` and the candidate files are reproducible. What the sweep
reported in the original run (n-axis rows; the other axes were equal or worse):

| source | axis | best coordinate slice kills | best (e, f) kills | result | bar used |
|---|---|---|---|---|---|
| LITA 15x15x15_r1977 | n | 30 | 134 | 1843 | 1848 |
| LITA 14x14x14_r1593 | n | 0 | 35 | 1558 (m: 1573, p: 1564) | 1582 |
| LITA 16x16x16_r2236 | n | 0 | 40 | 2196 (m: 2214, p: 2203) | 2223 |
| LITA 13x13x13_r1379 | n, m, p | 26 | 103 | 1276 (near miss) | 1274 |
| our 14x15x15_r1843 | m | 23 | 127 | 1716 (p: 1716 too; n: 1797 vs 1776) | 1790 |
| our 14x14x15_r1716 | n | 29 | 39 | 1677 (m: 1678; p: <14,14,14> 1596 vs LITA 1593) | 1681 |

For the n-axis of the three LITA squares the sweep row printed here is exactly the published direction pair; the
1716 and 1677 rows were taken from the second and third sweeps. Add `--verify` to run `../verify-it-yourself/fmmcheck.py`
on every candidate written.

## Runtime and environment

Original run: Apple M5 (10 cores, shared with other jobs, load 100+), Python 3.12.13, numpy 2.5.3, single thread.
Sweep of the four LITA squares, all three axes, including the original exact verification of every built
restriction: 37 s (13³), 102 s (15³), 166 s (14³), 451 s (16³). Re-run of the cleaned code (load ~15, `nice -n 10`):
`make_scheme.py` takes 14–40 s per scheme; all of `regenerate_all.sh` took 158 s (`SMOKE.md`).
Nothing is random: no seeds are involved.

## Lineage (how we know this is the code that made the published files)

Absorption (the 1842 and the 2180):

- The 1842 was first produced on 2026-10-08 by a different agent, with a float-guided search for an integer dependency
  in the v⊗w pairing of the 1843, verified exactly. `absorb_exact.py` is a later, exact re-implementation (written on
  2026-10-12 while the 1842 was being packaged); run on the 1843 it finds the same single dependency, removes the same
  term and returns the shipped 1842 term for term.
- The 2180 was first built in two steps (an exact null basis of the 2196's u⊗v pairing, then a builder applying the
  best shift per dependency). `maxkill.py` is the same algorithm in one command, and returns the shipped 2180 term for
  term from the 2196. Its certificate lists the 16 removed parent terms
  (1348, 1350, 1474, 1476, 1491, 1493, 1508, 1510, 1525, 1527, 1542, 1544, 1559, 1561, 1998, 2003), the same list as in
  the `note` of the shipped 2180, which names its parent by the file name of a byte-identical working copy of
  `15x16x16_r2196_Q.json`.

Peels (the other five files):

- The published files are byte-identical (sha256) to the candidate files the original sweep wrote,
  `14x15x15_r1843_from_15x15x15_r1977.npz_n.json`, `13x14x14_r1558_from_14x14x14_r1593.npz_n.json`,
  `15x16x16_r2196_from_16x16x16_r2236.npz_n.json`, `14x14x15_r1716_from_14x15x15_r1843_Q.json_m.json`,
  `13x14x15_r1677_from_14x14x15_r1716_Q.json_n.json`, and their `note` fields are the sweep's.
- The cleaned code, rerun on the cached LITA inputs (sha256 above), reproduces those files byte for byte, and the
  cleaned sweep reproduces the original CSV row for LITA 15x15x15 axis n (`SMOKE.md`).
- An independent reviewer agent rebuilt all five schemes with the original `project` function and found them identical
  as exact rational matrices, before release.

## What was dropped from the original code

- The verification inside the original sweep used a separate exact checker written during the run; here the
  checker shipped in `../verify-it-yourself/` is used instead (`--verify`). It only gated what was saved and did not
  change any coefficient.
- A pair-factor linear-dependency test (`--dep`, run on public schemes; the absorption of our own 1843 and 2196 is
  done by `absorb_exact.py` and `maxkill.py` above), a top-K multi-step peel-chain search, a census of composition
  bounds, and a GF(3) flip-graph walk. None of them produced a published object (see `../HOW_WE_FOUND_IT.md`).
- GF(2) input handling (the sweep over public integer schemes); all inputs here are rational.
