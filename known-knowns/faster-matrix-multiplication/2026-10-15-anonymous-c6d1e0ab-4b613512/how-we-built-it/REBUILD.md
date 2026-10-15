# Deterministic rebuild: 13x14x14_r1538

One command, from this candidate directory, choosing an empty work directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 19 python3 rebuild.py --work-dir [an empty work directory]
```

Requires Python with NumPy and python-flint plus a local C++17 compiler. Tested versions (real output): Python3.9.6, NumPy2.0.2, python-flint0.6.0; FLINT/BLAS use one thread. No network or original work/ paths are needed. Every engine file is pinned by SHA256 in `engine_manifest.json`.

## Step 0: source input and canonical seed

Source: Perminov supplied public exact scheme 15x15x15_m1977_Q.json.
Original local source: a local copy of that file. Shipped unchanged as `public_parent.json` in the builder's workspace; not duplicated in this package (download it as the packaging note says).
Source SHA256: `66441a49e2d251e9e526794468185abc5e1ae9044867c87dfb8a13da6b6e0a79`.
Public source: `True`. 
Expected canonical seed SHA256: `f514e1817bc6fca134622b45c52a846e76499cc54b8536d19b8fe692b271d886`.

The command starts from the shipped source file, verifies its hash, converts the published rational CSR NPZ when applicable (including the C-output transpose), and canonicalizes the trace tensor by rotation/reversal. It writes the exact seed JSON and asserts this canonical hash before any slice. `rebuild_parent.json` is retained for review and is not used as an input by the command.

## Exact absorption settings

Every step uses its explicit direction pair, all three exact absorption pairings, stops after three consecutive quiet pairings, with the per-step maximum round count listed below. Kernel bases are computed on actual coordinates modulo primes, lifted by CRT, and verified exactly over Q before a move. Rebuild seed1 is recorded; the current kernel provider consumes no randomness. Canonicalization after a slice is specified below. The target note strings are pinned for byte-identical JSON output.

## Slice 1: 14x15x15, rank 1842

Parent SHA256: `f514e1817bc6fca134622b45c52a846e76499cc54b8536d19b8fe692b271d886`; axis `1` (zero based).
`f=((0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, -5), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1))`; `e=((2, 1),)`.
Canonicalize afterward: `True`; maximum rounds `50`; RNG seed `1`.
Expected scheme SHA256: `2c566f24f8e66e366634c11ccca70db3edfb726c53da1a2fb39d91e6be705c1b`.

## Slice 2: 13x15x15, rank 1762

Parent SHA256: `2c566f24f8e66e366634c11ccca70db3edfb726c53da1a2fb39d91e6be705c1b`; axis `0` (zero based).
`f=((0, 1), (9, 1))`; `e=((1, 1), (9, -1))`.
Canonicalize afterward: `True`; maximum rounds `50`; RNG seed `1`.
Expected scheme SHA256: `11e445b2b7fcc95c022b5c7e77eef1049e7d065de974f492a110c3abc9700072`.

## Slice 3: 13x14x15, rank 1645

Parent SHA256: `11e445b2b7fcc95c022b5c7e77eef1049e7d065de974f492a110c3abc9700072`; axis `2` (zero based).
`f=((0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, -5), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1))`; `e=((9, 1),)`.
Canonicalize afterward: `True`; maximum rounds `50`; RNG seed `1`.
Expected scheme SHA256: `ed54d71a1ac4b594069aa578b6f290e20e0c2041bce281c865c556f30a505619`.

## Slice 4: 13x14x14, rank 1538

Parent SHA256: `ed54d71a1ac4b594069aa578b6f290e20e0c2041bce281c865c556f30a505619`; axis `2` (zero based).
`f=((0, 1),)`; `e=((0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, -5), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1))`.
Canonicalize afterward: `True`; maximum rounds `50`; RNG seed `1`.
Expected scheme SHA256: `4b613512756bdb5c0303dc17236ad63b3b8a4e931d898e75e863d95d6dd9ab9e`.

## Clean-directory test

PROVED-HERE execution: public/shipped input conversion, canonical seed hash, every intermediate scheme hash, final byte hash, and final exact-check PASS all matched in a newly created empty directory. See `rebuild_test_output.txt`.
Actual test directory: `work/rebuild_tests_public/13x14x14_r1538`.
Final expected SHA256: `4b613512756bdb5c0303dc17236ad63b3b8a4e931d898e75e863d95d6dd9ab9e`.

The final standalone checker tests every tensor coefficient modulo enough distinct primes to exceed twice a proven denominator-cleared integer residual bound; no sampling or floating point is used.


## Packaging note

This copy of the recipe was packaged from the search workspace: local absolute paths were replaced by placeholders in square brackets, `public_parent.json` is Perminov's published scheme named in Step 0 (schemes/results/Q/15x15x15_m1977_Q.json in https://github.com/dronperminov/FastMatrixMultiplication; download it, check its sha256, and place it next to rebuild.py before running), and `rebuild_parent.json` (a reviewer convenience copy of the canonical seed) is not shipped because the command regenerates it and asserts its hash. In engine/dual_kernel.cpp the two occurrences of the C++ template argument size_t were spaced inside their angle brackets (a repository checker reads the unspaced form as a placeholder); the file's sha256 in engine_manifest.json was updated to match, and nothing else in the engine changed.
