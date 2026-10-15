# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

The explicit matrix and every applicable mathematical property checkable from this package are confirmed. The independent exact determinant agrees with the author. This is a reproduction verdict only; it makes no judgment about the currency of the table value or novelty.

## Quoted definition and criteria

From `CLAIM.md`, the claimed object and value are:

> The file in object/ is a 109 x 109 matrix with entries +1 and -1 whose determinant satisfies |det| / 2^108 = 291 * 27^53 = 2119202655125403624550373680790052808829003860176536932438843923020304438454497, strictly larger than the best known value for order 109.

The complete success criterion is quoted so no file-checkable clause is omitted:

> Success means an explicit n x n +-1 matrix whose exact integer |det| (Bareiss on Python ints, cross-checked with sympy) is STRICTLY GREATER (direction: max) than the max, at verification time, of: the archived MaxDet value (Wayback copy referenced by Math-AI-Caltech), the arXiv:2608.22518 / Math-AI-Caltech CSV value, the EinsteinArena order-51 leaderboard, and any newer arXiv value. It must not exceed the residue-class upper bound (Barba for n = 1 mod 4, Ehlich-Wojtas for n = 2 mod 4, or the Ehlich n = 3 mod 4 bound in the form valid for that n range). The order must be one where the previous record was strictly below that bound.

The specified verification method is:

> Compute |det| with fraction-free Bareiss elimination on Python ints (exact), cross-checked with sympy Matrix(...).det(method='bareiss'). Note that det is divisible by 2^(n-1), so report |det|/2^(n-1) as an integer and compare it exactly to the record value. Confirm all entries are +-1. Also compute the bound for the residue class and confirm det <= bound. Pull the record from the Orrick archive or the Math-AI-Caltech CSVs (the *_prev columns give old benchmarks).

The clauses checkable here are the explicit square sign matrix, exact integer determinant by Python-int Bareiss and SymPy, order and residue class, divisibility and the claimed scaled value, the residue-class upper bound, strict improvement over the saved comparison number, and that the saved comparison number is strictly below the bound. The latter two are arithmetic checks of the saved metadata, conditional on its accuracy. The underlying fetched pages are absent; their hashes alone cannot authenticate their contents. Verification-time maxima across the named sources and newer papers are assigned to the other skeptic and are not judged here.

Neither partial win `p1` nor `p2` is claimed. This package presents an explicit object, not an exhaustive-search or maximality certificate. Every matrix entry and every asserted Gram entry was checked; no sample was used.

## Independence and files

I read `CLAIM.md`, listed the object, examined its first three data rows for format, and read `table-record/README.md`. I then wrote `skeptic/check.py` from the definition and ran it successfully before reading any file under `verify-it-yourself/` or reading `REPRODUCE.md`. Its source quotes the definition and applicable success clauses. Only after that run did I inspect and execute the author's checker. `skeptic/proof_checks.py` subsequently re-derived the additional saved proof steps without importing the author's implementation.

The object is `object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt`. The independent SHA256 matches `INDEX.csv`. The indexed target, order, object name, value, saved benchmark and timestamp are consistent with the other saved files.

`REPRODUCE.md` references `verify-it-yourself/RECEIPTS.md` and `how-we-built-it/`; neither is present. These are unavailable historical receipts and search materials, not missing inputs to the explicit-object proof. No search provenance, search rerun, optimality, or exhaustive enumeration is certified. I initially overlooked `INDEX.csv` when listing subdirectories; a root inventory located it, and it was verified.

## Properties and derivations

1. **Dimensions and entries.** Parse every line as integers, require exactly 109 rows and 109 columns in each row, and test all 11,881 entries for membership in {-1,+1}. The order is at least 23 and is 1 modulo 4.
2. **Exact determinant.** Independently implement Bareiss on Python integers with pivot row swaps and determinant sign tracking. The recurrence is `(pivot*a[i,j] - a[i,k]*a[k,j])/previous_pivot`. Sylvester's determinant identity gives this fraction-free recurrence between successive elimination minors; each actual division is checked for zero remainder. Triangular elimination and the tracked row-swap sign give the final determinant. All 425,754 divisions are exact. Repeat the complete elimination and require equality. Cross-check the original full matrix using `sympy.Matrix(...).det(method='bareiss')`.
3. **Divisibility and normalized value.** Subtract the first row from each of the other 108 rows, preserving determinant. Every resulting entry in those rows is even. Divide each such row by two, giving `det M = 2^108 * det reduced`. Compute that reduced determinant in a further full Bareiss run. Its absolute value, the decimal claim, and `291 * 27^53` are equal.
4. **Barba bound.** For order 109, the required bound is `sqrt(217) * 108^54`. Dividing by `2^108` gives `sqrt(217) * 27^54`. Squaring nonnegative quantities and cancelling `27^106` reduces the claimed-value comparison to `291^2 <= 217 * 27^2`, namely `84681 <= 158193`. Also compare the complete integer determinant square against `217 * 108^108`, without floating-point decisions. The saved comparison number is strictly below this same bound, and the object strictly exceeds that number by the exact difference printed below.
5. **Bordered Hadamard proof.** Check the corner is -1 and every other border entry is +1. For the 108-square inner block H, compute all 11,664 inner products and require `H H^T = 108 I`. Thus `H^-1 = H^T/108`, and taking determinants gives `abs(det H) = 108^54`; also compute `det H` independently. Sum every entry of H to get `s = 1056`. Eliminating the border with this inverse gives the Schur complement `-1 - s/108`, hence `det M = det H * (-1 - s/108)`. Check this signed identity as an integer equality after multiplying by 108. Consequently `abs(det M) = 108^54 * (1 + 1056/108) = 1164 * 108^53 = 2^108 * 291 * 27^53`, since `1164 = 4*291` and `108 = 4*27`.
6. **CRT proof.** Independently generate the author's twelve distinct prime moduli and certify primality by trying every possible divisor up to the integer square root. Compute full determinants over each prime field, with a separately written elimination that normalizes pivot rows. Check each residue against the independent signed integer determinant. Assemble CRT using modular inverses, and check the centered representative equals that signed determinant. Each sign row has Euclidean norm `sqrt(109)`, so Hadamard's inequality bounds `abs(det M)` by `109^(109/2)`. The modulus product squared exceeds `4 * 109^109`, so the product exceeds twice this bound. Two integers within that interval with the same residues differ by a multiple of the product; only zero is possible. This proves exact CRT reconstruction, rather than a probabilistic modular spot check.
7. **Negative control and determinism.** Independently flip the corner sign and recompute the entire determinant; its Schur complement becomes `1 - s/108` and its scaled absolute determinant differs from the claim. The author's wrapper rejects this same change. Two complete independent-checker invocations give byte-identical output, and the original object bytes remain unchanged during checking.

## Exact commands and actual output

All commands were run from this folder. The relative interpreter path below selects the dependency-equipped Python interpreter explicitly permitted in the task. The system `python3` initially lacked SymPy; that environment failure is retained in `skeptic/system-python-output.txt`. It is not a determinant disagreement. The successful independent run used:

```sh
../../../.venv/bin/python -u skeptic/check.py > skeptic/output.txt 2>&1
```

Exit status: 0. The following is pasted directly from `skeptic/output.txt`:

```text
object: object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt
sha256: 0108345c2f3cbffdd58f23eef8aba73546583f02062a013a5b64ab95e198faa6
dimensions: 109 x 109
entries: all 11881 entries are +1 or -1
order: 109 >= 23; 109 mod 4 = 1
Bareiss exact divisions: 425754
signed determinant: 687720580550393685384435488623154547762327053849477344513207580440243395287690372410950406599169376107974623232
repeat full Bareiss: identical
SymPy version: 1.14.0
SymPy signed determinant: 687720580550393685384435488623154547762327053849477344513207580440243395287690372410950406599169376107974623232
SymPy comparison: equal
row-difference reduced determinant: 2119202655125403624550373680790052808829003860176536932438843923020304438454497
reduced Bareiss exact divisions: 425754
divisibility by 2^108: verified by exact row operations
absolute scaled determinant: 2119202655125403624550373680790052808829003860176536932438843923020304438454497
291 * 27^53: 2119202655125403624550373680790052808829003860176536932438843923020304438454497
claimed formula and decimal: both equal the computed value
Barba bound: |det| <= sqrt(217) * 108^54
scaled Barba bound: sqrt(217) * 27^54
exact reduced squared comparison: 84681 <= 158193
exact determinant-squared <= Barba-bound-squared: True
saved benchmark metadata (unauthenticated): 1877483841834222713683125485573890072927341503771574105042244268774869908324352
scaled determinant minus saved benchmark: 241718813291180910867248195216162735901662356404962827396599654245434530130145
saved benchmark arithmetic: strictly exceeded; strictly below Barba bound
table authentication/currentness/novelty: outside this check
object bytes unchanged during run: true
independent file checks: PASS
```

The complete repeat and comparison commands were:

```sh
../../../.venv/bin/python -u skeptic/check.py > skeptic/output-repeat.txt 2>&1
cmp skeptic/output.txt skeptic/output-repeat.txt
```

Both exited 0. `cmp` produced no output.

Additional independently re-derived proof checks:

```sh
../../../.venv/bin/python -u skeptic/proof_checks.py > skeptic/proof-output.txt 2>&1
```

Exit status: 0. Pasted directly from `skeptic/proof-output.txt`:

```text
border: corner -1; all other 216 border entries +1
Hadamard inner block: all 11664 entries of H H^T equal 108 I
excess s = sum of all H entries: 1056
signed det H: -63809126030448898643916694820705061132587046233456660831122352824352479975146529398954161437036333865688367104
H inverse = H^T / 108 follows from the fully checked Gram identity
Schur complement: det M = det H * (-1 - s/108); exact equality verified
absolute determinant identities: 108^54 * (1 + 1056/108) = 1164 * 108^53 = 2^108 * 291 * 27^53
CRT primes (trial-division certified): [2147483647, 2147483629, 2147483587, 2147483579, 2147483563, 2147483549, 2147483543, 2147483497, 2147483489, 2147483477, 2147483423, 2147483399]
CRT modulus product: 9619624174635069841772211428052709599486115124032323136969363097616412141543659987229343641984267061780616937463
product^2 > 4 * 109^109: True
det M mod 2147483647: 1332424771
det M mod 2147483629: 825081487
det M mod 2147483587: 1367437667
det M mod 2147483579: 766278987
det M mod 2147483563: 1790849131
det M mod 2147483549: 468257410
det M mod 2147483543: 1054268015
det M mod 2147483497: 576084035
det M mod 2147483489: 1715665301
det M mod 2147483477: 575222050
det M mod 2147483423: 1296750623
det M mod 2147483399: 699397858
CRT centered signed determinant: 687720580550393685384435488623154547762327053849477344513207580440243395287690372410950406599169376107974623232
exactness: Hadamard gives |det M| <= 109^(109/2); product exceeds twice that bound, so the centered CRT representative is unique
negative control (corner sign flipped), absolute scaled determinant: 1725948554174297797314221863736228576262796958288107398584213091944371656060879
negative control differs from the claim: true
INDEX.csv: target, order, object path, SHA256, claimed value, saved benchmark, and saved timestamp all consistent
all additional saved proof steps: PASS
```

Author's standalone checker, run only after the initial independent success:

```sh
../../../.venv/bin/python -u verify-it-yourself/check_maxdet.py object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt --expect-norm 2119202655125403624550373680790052808829003860176536932438843923020304438454497 > skeptic/author-output.txt 2>&1
```

Exit status: 0. Pasted directly from `skeptic/author-output.txt`:

```text
n=109 bareiss |det| and CRT |det| (12 primes) agree
sympy bareiss cross-check agrees
|det| / 2^108 = 2119202655125403624550373680790052808829003860176536932438843923020304438454497
ratio to the Barba bound = 0.731643
PASS n=109 norm_det=2119202655125403624550373680790052808829003860176536932438843923020304438454497
```

Author's advertised wrapper, with its temporary negative-control files kept inside this folder:

```sh
mkdir -p skeptic/tmp
TMPDIR=skeptic/tmp sh verify-it-yourself/run_checks.sh > skeptic/author-wrapper-output.txt 2> skeptic/author-wrapper-stderr.txt
```

Exit status: 0. Pasted directly from `skeptic/author-wrapper-output.txt`:

```text
sha256 matches INDEX.csv (0108345c2f3cbffdd58f23eef8aba73546583f02062a013a5b64ab95e198faa6)
== check_maxdet.py on object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt
n=109 bareiss |det| and CRT |det| (12 primes) agree
sympy not installed: two exact methods used
|det| / 2^108 = 2119202655125403624550373680790052808829003860176536932438843923020304438454497
ratio to the Barba bound = 0.731643
PASS n=109 norm_det=2119202655125403624550373680790052808829003860176536932438843923020304438454497
== negative control: a corrupted copy must FAIL
negative control rejected as expected (FAIL normalized determinant 1725948554174297797314221863736228576262796958288107398584213091944371656060879 != expected 2119202655125403624550373680790052808829003860176536932438843923020304438454497)
ALL CHECKS PASS
```

The wrapper's system Python does not have SymPy; the independent checker and the separate author invocation above both did execute the required SymPy cross-check. The wrapper also emitted these host diagnostics on stderr; pasted directly from `skeptic/author-wrapper-stderr.txt`:

```text
2026-10-14 10:50:54.227 xcodebuild[69609:69797100]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-14 10:50:54.560 xcodebuild[69609:69797099] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
```

## Comparison and verdict

No mathematical disagreement, missing claimed matrix, changed object bytes, hash mismatch, or non-deterministic result was found. The author's determinant, CRT claim, Barba comparison and negative-control result agree with the independent calculations. Missing historical receipts and construction code are explicitly recorded above. Authentication and currency of table sources and novelty remain outside this reproduction verdict.

pass: true
