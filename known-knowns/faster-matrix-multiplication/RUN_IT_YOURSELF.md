# Reproduce: fast matrix multiplication schemes

All commands are relative to the `known-knowns/faster-matrix-multiplication/` directory. Requirements: `python3` with `numpy`.

## 1. Integrity

```sh
sha256sum schemes/*.json      # macOS: shasum -a 256; expected values in INDEX.csv
```

## 2. Brent equations and rank (the proof)

```sh
python3 verify-it-yourself/fmmcheck.py schemes/14x15x15_r1843_Q.json schemes/13x14x14_r1558_Q.json \
        schemes/15x16x16_r2196_Q.json schemes/14x14x15_r1716_Q.json schemes/13x14x15_r1677_Q.json
```
Expected, per scheme: `mod p: violated Brent equations = 0` for each prime, the line comparing log2 of the product of
the primes with log2(2·L·(S+1)), and a last line
`FMMCHECK PASS ... rank_nonzero_terms=<rank> sha256=<as in INDEX.csv>` with ranks 1843, 1558, 2196, 1716, 1677.
Runtime: seconds to a few minutes per scheme (the <15,16,16> scheme is the slowest).

Negative controls:
```sh
mkdir -p mutants && python3 verify-it-yourself/mutate.py schemes/13x14x15_r1677_Q.json mutants
for m in drop_term bump_coeff swap_vw; do python3 verify-it-yourself/fmmcheck.py mutants/$m.json | tail -1; done   # each FMMCHECK FAIL
```
`sh verify-it-yourself/run_checks.sh` does all of the above and compares sha256 and rank with `INDEX.csv`.

## 3. Compare with today's catalogues

One GET per source, with a User-Agent that says who you are, and no retries:
```sh
mkdir -p today && cd today
UA="your-name-or-project (single GET)"
curl -sS -A "$UA" -o fmm_sota.json             https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json
curl -sS -A "$UA" -o perminov_README.md        https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md
curl -sS -A "$UA" -o merlijn_SHA256SUMS        https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS
curl -sS -A "$UA" -o matmulcatalog_COVERAGE.md https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md
cd ..
python3 the-record-we-beat/parse_sources.py today 14x15x15=1843 13x14x14=1558 15x16x16=2196 14x14x15=1716 13x14x15=1677
```
Each format prints the value listed by each source, the minimum (`bar_min_of_four_sources`) and
`strictly_below_bar`. If a source has since listed a rank ≤ ours, that format is no longer an improvement (see the
Corrections in `READ_BEFORE_CITING.md` at the repository root). The values recorded for this release are in
`the-record-we-beat/sources_2026-10-10T19-25-52Z.json`.

## 4. Regenerating the schemes

The schemes are restrictions of LITA's public square schemes (github.com/khoruzhii/lita, `schemes/15x15x15_r1977.npz`
sha256 94515288…2a33, `14x14x14_r1593.npz` e8039025…1110, `16x16x16_r2236.npz` af5fd100…67da as fetched by our agents)
along the direction pairs listed in `README.md`. The peel code is not part of this release; the five files and the
checker are the claim.
