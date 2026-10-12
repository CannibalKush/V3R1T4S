# Check results (fast matrix multiplication)

`sh verify-it-yourself/run_checks.sh` was run on the shipped files from 2026-10-10T19:30:51Z to 19:37:03Z on the build machine
(macOS, python3 3.9, numpy 2.0.2, load average about 80–100 from other jobs). Exit code 0, last line
`ALL CHECKS PASSED`.

| scheme | Brent equations checked | primes (p < 2^20) | log2 ∏p | log2 2L(S+1) | violations | rank (nonzero terms) | sha256 = INDEX.csv | verdict |
|---|---|---|---|---|---|---|---|---|
| <14,15,15> `14x15x15_r1843_Q.json` | 9 922 500 | 4 | 80.0 | 32.9 | 0 | 1843 | yes | PASS |
| <13,14,14> `13x14x14_r1558_Q.json` | 6 492 304 | 4 | 80.0 | 36.8 | 0 | 1558 | yes | PASS |
| <15,16,16> `15x16x16_r2196_Q.json` | 14 745 600 | 4 | 80.0 | 39.5 | 0 | 2196 | yes | PASS |
| <14,14,15> `14x14x15_r1716_Q.json` | 8 643 600 | 4 | 80.0 | 33.7 | 0 | 1716 | yes | PASS |
| <13,14,15> `13x14x15_r1677_Q.json` | 7 452 900 | 4 | 80.0 | 33.7 | 0 | 1677 | yes | PASS |

Because ∏p exceeds 2·L·(S+1) in every case, "0 violations modulo every prime" implies every Brent equation holds
exactly over Q (see the docstring of `verify-it-yourself/fmmcheck.py`). Negative controls (`verify-it-yourself/mutate.py` on the <13,14,15>
scheme): a dropped term, a coefficient increased by 1, and two swapped v-factors are each reported
`FMMCHECK FAIL`.

Comparison with the criterion sources (2026-10-10T19:25:52Z, `the-record-we-beat/sources_2026-10-10T19-25-52Z.json`): every rank
is strictly below the minimum of the four sources (bars 1848, 1582, 2223, 1789, 1681; margins −5, −24, −27, −73, −4).

Earlier independent checks (not shipped): the author's exact big-integer checker (clears denominators, no modular
arithmetic), an independent reviewer's checker in exact Fraction mode and in CRT-bounded modular mode, and a final
pre-release modular Brent check over 4 primes, all with 0 violations and the same ranks.

## Raw output

```
2026-10-10T19:30:51Z
== 13x14x14_r1558_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 182*196*182 = 6492304 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 36.8
FMMCHECK PASS file=13x14x14_r1558_Q.json format=<13,14,14> sorted=<13,14,14> terms=1558 rank_nonzero_terms=1558 sha256=15e46337bdca5a92090021dbd11a6fcb9d57f352a396ea6b34e1f32888fe0702
rank 1558 as claimed
== 13x14x15_r1677_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 182*210*195 = 7452900 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 33.7
FMMCHECK PASS file=13x14x15_r1677_Q.json format=<13,14,15> sorted=<13,14,15> terms=1677 rank_nonzero_terms=1677 sha256=4230f61d432b627d0624105deb004451e8332ccca32c1834746cff2e11c7d6bc
rank 1677 as claimed
== 14x14x15_r1716_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 196*210*210 = 8643600 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 33.7
FMMCHECK PASS file=14x14x15_r1716_Q.json format=<14,14,15> sorted=<14,14,15> terms=1716 rank_nonzero_terms=1716 sha256=83e880a0ecbab4bc6af7c0105365e9ee69aac2c2dc0ac272073249e856f34a56
rank 1716 as claimed
== 14x15x15_r1843_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 210*225*210 = 9922500 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 32.9
FMMCHECK PASS file=14x15x15_r1843_Q.json format=<14,15,15> sorted=<14,15,15> terms=1843 rank_nonzero_terms=1843 sha256=c86dba238db8a26bef6a4e8f5e224e8524e5d61cd0b89625fe34b43e27813ac3
rank 1843 as claimed
== 15x16x16_r2196_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 240*256*240 = 14745600 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 39.5
FMMCHECK PASS file=15x16x16_r2196_Q.json format=<15,16,16> sorted=<15,16,16> terms=2196 rank_nonzero_terms=2196 sha256=11c2649664a1d8d4386b225bb0ba62f3a5f1c819b575f50ce9830c478fb67113
rank 2196 as claimed
== negative controls on the smallest scheme (each must FAIL)
control drop_term: FMMCHECK FAIL file=drop_term.json format... (expected)
control bump_coeff: FMMCHECK FAIL file=bump_coeff.json forma... (expected)
control swap_vw: FMMCHECK FAIL file=swap_vw.json format=<... (expected)
ALL CHECKS PASSED
sh verify-it-yourself/run_checks.sh  90.84s user 1.47s system 24% cpu 6:12.03 total
2026-10-10T19:37:03Z
```
