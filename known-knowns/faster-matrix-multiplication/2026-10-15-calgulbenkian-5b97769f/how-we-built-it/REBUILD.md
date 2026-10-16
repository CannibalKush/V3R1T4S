# Deterministic rebuild: 13x15x15_r1762

One command, from this candidate directory, choosing an empty work directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 19 python3 rebuild.py --work-dir [an empty work directory]
```

Requires Python with NumPy and python-flint plus a local C++17 compiler. Tested versions (real output): Python3.9.6, NumPy2.0.2, python-flint0.6.0; FLINT/BLAS use one thread. No network or original work/ paths are needed. Every engine file is pinned by SHA256 in `engine_manifest.json`.

## Step 0: source input and canonical seed

Source: LITA published 15x15x15_r1977.npz (https://github.com/khoruzhii/lita).
Original local source: `public_parent.npz (the LITA release file 15x15x15_r1977.npz, downloaded as REBUILD.md states)`. Shipped unchanged as `public_parent.npz`.
Source SHA256: `94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33`.
Public source: `True`. 
Expected canonical seed SHA256: `29f4ff55f2ccbd7bfd2228030a028e52d368fa80d4ee7a892f8b721a13844b0e`.

The command starts from the shipped source file, verifies its hash, converts the published rational CSR NPZ when applicable (including the C-output transpose), and canonicalizes the trace tensor by rotation/reversal. It writes the exact seed JSON and asserts this canonical hash before any slice. `rebuild_parent.json` is retained for review and is not used as an input by the command.

## Exact absorption settings

Every step uses its explicit direction pair, all three exact absorption pairings, stops after three consecutive quiet pairings, and permits at most50 rounds. Kernel bases are computed on actual coordinates modulo primes, lifted by CRT, and verified exactly over Q before a move. Rebuild seed1 is recorded; the current kernel provider consumes no randomness. Canonicalization after a slice is specified below. The target note strings are pinned for byte-identical JSON output.

## Slice 1: 14x15x15, rank 1842

Parent SHA256: `29f4ff55f2ccbd7bfd2228030a028e52d368fa80d4ee7a892f8b721a13844b0e`; axis `0` (zero based).
`f=((0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, -5), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1))`; `e=((4, 1),)`.
Canonicalize afterward: `True`.
Expected scheme SHA256: `cc2909b34c7280c0a3cc940ef1309c546c5c9acabc2a6c61812436b257ca62df`.

## Slice 2: 13x15x15, rank 1762

Parent SHA256: `cc2909b34c7280c0a3cc940ef1309c546c5c9acabc2a6c61812436b257ca62df`; axis `0` (zero based).
`f=((0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, -5), (7, 1), (8, 1), (9, 1), (10, 1), (12, 1), (13, 1))`; `e=((3, 1), (11, -1))`.
Canonicalize afterward: `True`.
Expected scheme SHA256: `5b97769fb1c3115c7195f0c508e0cae9ded013ef2543a7f0d5aa4147410e1647`.

## Clean-directory test

PROVED-HERE execution: public/shipped input conversion, canonical seed hash, every intermediate scheme hash, final byte hash, and final exact-check PASS all matched in a newly created empty directory. See `rebuild_test_output.txt`.
Actual test directory: `work/rebuild_tests_public/13x15x15_r1762`.
Final expected SHA256: `5b97769fb1c3115c7195f0c508e0cae9ded013ef2543a7f0d5aa4147410e1647`.

The final standalone checker tests every tensor coefficient modulo enough distinct primes to exceed twice a proven denominator-cleared integer residual bound; no sampling or floating point is used.


## Packaging note

This copy of the recipe was packaged from the search workspace: local absolute paths were replaced by placeholders in square brackets, `public_parent.npz` is the LITA release file named in Step 0 (download it from https://github.com/khoruzhii/lita, check its sha256, and place it next to rebuild.py before running), and `rebuild_parent.json` (a reviewer convenience copy of the canonical seed) is not shipped because the command regenerates it and asserts its hash. In engine/dual_kernel.cpp the two occurrences of the C++ template argument size_t were spaced inside their angle brackets (a repository checker reads the unspaced form as a placeholder); the file's sha256 in engine_manifest.json was updated to match, and nothing else in the engine changed.
