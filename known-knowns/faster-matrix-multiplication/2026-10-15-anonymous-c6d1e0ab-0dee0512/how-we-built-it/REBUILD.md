# Deterministic rebuild: 15x16x16_r2176

One command, from this candidate directory, choosing an empty work directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 19 python3 rebuild.py --work-dir [an empty work directory]
```

Requires Python with NumPy and python-flint plus a local C++17 compiler. Tested versions (real output): Python3.9.6, NumPy2.0.2, python-flint0.6.0; FLINT/BLAS use one thread. No network or original work/ paths are needed. Every engine file is pinned by SHA256 in `engine_manifest.json`.

## Step 0: source input and canonical seed

Source: LITA published 17x17x17_r2723.npz (https://github.com/khoruzhii/lita).
Original local source: `data/lita/17x17x17_r2723.npz`. Shipped unchanged as `public_parent.npz`.
Source SHA256: `dc041354b5d9c0709aa06372f47f50422e5e027b63644f13be32715c3250683b`.
Public source: `True`. 
Expected canonical seed SHA256: `22018645c44d46ad9b855ee2bf30df18a1188f0d4eb6435c4484b2f8679d3f95`.

The command starts from the shipped source file, verifies its hash, converts the published rational CSR NPZ when applicable (including the C-output transpose), and canonicalizes the trace tensor by rotation/reversal. It writes the exact seed JSON and asserts this canonical hash before any slice. `rebuild_parent.json` is retained for review and is not used as an input by the command.

## Exact absorption settings

Every step uses its explicit direction pair, all three exact absorption pairings, stops after three consecutive quiet pairings, and permits at most50 rounds. Kernel bases are computed on actual coordinates modulo primes, lifted by CRT, and verified exactly over Q before a move. Rebuild seed1 is recorded; the current kernel provider consumes no randomness. Canonicalization after a slice is specified below. The target note strings are pinned for byte-identical JSON output.

## Slice 1: 16x17x17, rank 2553

Parent SHA256: `22018645c44d46ad9b855ee2bf30df18a1188f0d4eb6435c4484b2f8679d3f95`; axis `0` (zero based).
`f=((0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, -6), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1))`; `e=((0, 1),)`.
Canonicalize afterward: `False`.
Expected scheme SHA256: `f5dca3b437c4bec43077dbe10178f5d82ffe89b4fb5d66078a352c4929556f87`.

## Slice 2: 15x17x17, rank 2463

Parent SHA256: `f5dca3b437c4bec43077dbe10178f5d82ffe89b4fb5d66078a352c4929556f87`; axis `0` (zero based).
`f=((8, 1),)`; `e=((8, 1),)`.
Canonicalize afterward: `True`.
Expected scheme SHA256: `9ebf1dd0a32bd9b49f29386ad49bf74f01a613a69159b48a40b4cf248803a5be`.

## Slice 3: 15x16x17, rank 2313

Parent SHA256: `9ebf1dd0a32bd9b49f29386ad49bf74f01a613a69159b48a40b4cf248803a5be`; axis `2` (zero based).
`f=((0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, -6), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1))`; `e=((5, 1),)`.
Canonicalize afterward: `True`.
Expected scheme SHA256: `5d8085edc06740bcedbcfa7bbb3f92da85eb374774b340b1204b5ccdd835d419`.

## Slice 4: 15x16x16, rank 2176

Parent SHA256: `5d8085edc06740bcedbcfa7bbb3f92da85eb374774b340b1204b5ccdd835d419`; axis `2` (zero based).
`f=((10, 1),)`; `e=((0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, -6), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1))`.
Canonicalize afterward: `True`.
Expected scheme SHA256: `2095186e1215bd90009436c122d8f6cc78b89b0fe1f1943234ad02d8f9d1bd3e`.

## Clean-directory test

PROVED-HERE execution: public/shipped input conversion, canonical seed hash, every intermediate scheme hash, final byte hash, and final exact-check PASS all matched in a newly created empty directory. See `rebuild_test_output.txt`.
Actual test directory: `work/rebuild_tests_public/15x16x16_r2176`.
Final expected SHA256: `2095186e1215bd90009436c122d8f6cc78b89b0fe1f1943234ad02d8f9d1bd3e`.

The final standalone checker tests every tensor coefficient modulo enough distinct primes to exceed twice a proven denominator-cleared integer residual bound; no sampling or floating point is used.


## Packaging note

This copy of the recipe was packaged from the search workspace: local absolute paths were replaced by placeholders in square brackets, `public_parent.npz` is the LITA release file named in Step 0 (download it from https://github.com/khoruzhii/lita, check its sha256, and place it next to rebuild.py before running), and `rebuild_parent.json` (a reviewer convenience copy of the canonical seed) is not shipped because the command regenerates it and asserts its hash. In engine/dual_kernel.cpp the two occurrences of the C++ template argument size_t were spaced inside their angle brackets (a repository checker reads the unspaced form as a placeholder); the file's sha256 in engine_manifest.json was updated to match, and nothing else in the engine changed.
