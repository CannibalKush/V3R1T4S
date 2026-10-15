# Hadamard maximal determinant, order 109: |det| / 2^108 = 291 · 27^53

## What

The 109 x 109 {+1,-1} matrix in claim/object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt (sha256 0108345c2f3cbffdd58f23eef8aba73546583f02062a013a5b64ab95e198faa6) has exact |det| = 2^108 * 291 * 27^53 = 2^108 * 2119202655125403624550373680790052808829003860176536932438843923020304438454497 (Bareiss, 8-prime CRT and 120-digit mpmath agree), which is strictly below the Barba bound for n = 109 (ratio 0.731643) and strictly above the only n = 109 value carried by the criterion's enumerated sources at verification time on 2026-10-14 16:16-16:23 UTC, Rokicki's 2005 two-circulant record 1877483841834222713683125485573890072927341503771574105042244268774869908324352 (= 1.877483842E78 in the Archive-It copy of Orrick's MaxDet table, itself strictly below the bound at ratio 0.648191, reproduced exactly from Rokicki's published first rows), while the arXiv:2608.22518v3 / Math-AI-Caltech CSV and EinsteinArena order-51 sources carry no n = 109 value and an arXiv search found no newer n = 109 value.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only. If `sympy` is installed, the checker adds a third determinant method.
- **Rough laptop time**: about 3 seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

All values are |det| / 2^108, the normalization used by Orrick's table.

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Orrick's MaxDet table, Archive-It copy (orders 80-119) | N = 109 | 1.877483842E78, marked not proved maximal; matrix found by Tomas Rokicki (page dated 12 April 2005) | 2.119202656E78 | https://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/page3.shtml | 2026-10-14T16:16:58Z |
| Same record, exact value | N = 109 | 1877483841834222713683125485573890072927341503771574105042244268774869908324352 (rebuilt by the criterion skeptic from Rokicki's published circulant rows) | 2119202655125403624550373680790052808829003860176536932438843923020304438454497 | https://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/d109.html | 2026-10-14T16:17:39Z |
| Math-AI-Caltech/hadamard-maxdet `maxdet_records.csv` | n = 109 | no row (covers 51, 103, 107, 111, 115, 119) | | https://raw.githubusercontent.com/Math-AI-Caltech/hadamard-maxdet/main/maxdet_records.csv | 2026-10-14T16:16:11Z |
| arXiv:2608.22518 v3 (1 Oct 2026) | n = 109 | no value | | https://arxiv.org/abs/2608.22518 | 2026-10-14T16:18:09Z |
| Barba bound, sqrt(2n - 1) (n - 1)^((n-1)/2) / 2^108 | n = 109 | about 2.896497E78 | ratio 0.731643 (old record: 0.648191) | | |

Our value is 1.1287 times the old record. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Maximality is not claimed. The value is 73% of the Barba bound, so the order stays open.
- Orders 105 and 117, found in the same run, are separate cells and are not claimed here.
- No new method is claimed. The matrix borders a Hadamard matrix of order 108 (Paley's construction from the prime 107). The determinant depends on the core's "excess", 1056 here. Bordering a Hadamard matrix is a standard construction, and we did not trace its first appearance.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **W. P. Orrick and B. Solomon**, *The Hadamard maximal determinant problem* (archived): https://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/. This is the table the result is compared against.
- **Tomas Rokicki**, the previous order-109 record (archived page dated 12 April 2005): http://tomas.rokicki.com/newrec.html.
- **R. E. A. C. Paley**, "On Orthogonal Matrices", *J. Math. Phys.* 12 (1933), 311-320 (https://mathworld.wolfram.com/PaleysTheorem.html). His construction gives the order-108 Hadamard core.
- **G. Butbaia et al.**, Math-AI-Caltech/hadamard-maxdet and arXiv:2608.22518. Compared against; they carry no order-109 value.
- Contributor credit: `anonymous-c6d1e0ab`.
