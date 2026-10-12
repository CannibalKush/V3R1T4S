# Reproduce: constant-weight codes

All commands are relative to the `known-knowns/bigger-codes/` directory. Requirements: `python3` with `numpy` (any version; `numpy >= 2.0` is faster for the popcounts). No network access
is needed except for step 3.

## 1. Check every code (about 10 minutes single-threaded; the largest, A(29,6,12) with 1.9·10^9 pairs, takes a few minutes)

```sh
cd codes
for f in A*.txt; do
  set -- $(echo "$f" | sed 's/^A//; s/\.txt$//; s/_/ /g')     # n d w M
  python3 ../verify-it-yourself/cwcheck.py "$f" "$1" "$2" "$3" || echo "FAILED $f"
done
```
Each run prints the sha256, the format/weight/distinctness tests, the full pairwise-distance histogram, the t-subset
packing test and `VERDICT: VALID  A(n,d,w) >= M`. The expected sha256 of every file is in `INDEX.csv`;
`verify-it-yourself/RECEIPTS.md` has the complete output at release time.

Controls: duplicate a line, flip one bit, or change `M` in the file name; every such file is reported INVALID
(exit code 1).

## 2. Check the five Delsarte certificates (seconds, pure python)

```sh
python3 verify-it-yourself/delsarte_check.py certificates/cert_A*.json
```
Expected: five lines ending in `VALID` with the bounds 197, 380, 245, 2511, 2652 and the exact optima 8091/41,
145638/383, 26784/109, 1102464/439, 801009/302, then `ALL CERTIFICATES VALID`. Changing `U` or any `y_k` in a copy of
a certificate makes the checker report the violated constraint.

`sh verify-it-yourself/run_checks.sh` runs steps 1 and 2 and compares the sha256 values with `INDEX.csv`.

## 3. Compare with today's table

```sh
curl -sS -D headers.txt -o Andw.html https://aeb.win.tue.nl/codes/Andw.html     # one GET, default client
sha256sum Andw.html                                   # 0f1b51bf...1cee was the version recorded on 2026-10-10
python3 the-record-we-beat/parse_brouwer_table.py Andw.html the-record-we-beat/claims.csv
```
`the-record-we-beat/claims.csv` lists our 35 cells (`n,d,w,value,lb|ub`); the parser prints each cell's current text and a verdict
(STRICT_BEAT / TIE / BELOW for codes, STRICT_BELOW_UB for the Delsarte values). Any code whose cell now prints a lower
bound ≥ our size is no longer an improvement (see Corrections in `READ_BEFORE_CITING.md` at the repository root).

## 4. Rebuilding the codes

The codes are the output of a randomised local search and are not rebuilt deterministically; the files themselves
are the claim. To see how far each is from its seed, download the seed file named in `INDEX.csv` from Brouwer's code
archive (directory `cwc/` next to the table; files such as `a26.6.9.5761H` hold one hex word per line) and compare
the word sets; our own measurement is quoted in the README (1 %–17 % of the words changed).
