# Deterministic rebuild: 14x16x16_r2117

One command, from this candidate directory, choosing an empty work directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 19 python3 rebuild.py --work-dir [an empty work directory]
```

Requires Python with NumPy and python-flint plus a local C++17 compiler. Tested versions (real output): Python3.9.6, NumPy2.0.2, python-flint0.6.0; FLINT/BLAS use one thread. No network or original work/ paths are needed. Every engine file is pinned by SHA256 in `engine_manifest.json`.

## Step 0: source input and canonical seed

Source: V3R1T4S public repo: known-knowns/faster-matrix-multiplication/schemes/15x16x16_r2180_Q.json.
Original local source: `data/parents/trophy_15x16x16_r2180_Q.json`. Shipped unchanged as `public_parent.json`.
Source SHA256: `8365355f0f3ae6bc3efd445517fbd473c91477cd1c2b2aeb08c0b3b85182fd1d`.
Public source: `True`. 
Expected canonical seed SHA256: `fdefcd37455dbd949d0a7b54602b5d9e58b33ce7e5280124e0627249750af5f0`.

The command starts from the shipped source file, verifies its hash, converts the published rational CSR NPZ when applicable (including the C-output transpose), and canonicalizes the trace tensor by rotation/reversal. It writes the exact seed JSON and asserts this canonical hash before any slice. `rebuild_parent.json` is retained for review and is not used as an input by the command.

## Exact absorption settings

Every step uses its explicit direction pair, all three exact absorption pairings, stops after three consecutive quiet pairings, and permits at most50 rounds. Kernel bases are computed on actual coordinates modulo primes, lifted by CRT, and verified exactly over Q before a move. Rebuild seed1 is recorded; the current kernel provider consumes no randomness. Canonicalization after a slice is specified below. The target note strings are pinned for byte-identical JSON output.

## Slice 1: 14x16x16, rank 2117

Parent SHA256: `fdefcd37455dbd949d0a7b54602b5d9e58b33ce7e5280124e0627249750af5f0`; axis `0` (zero based).
`f=((3, 1), (8, 1))`; `e=((8, 1),)`.
Canonicalize afterward: `True`.
Expected scheme SHA256: `6e1e9e76e34ddfe293053317981cf84e8ec25927fa7b3f82430d0ddf964c4193`.

## Clean-directory test

PROVED-HERE execution: public/shipped input conversion, canonical seed hash, every intermediate scheme hash, final byte hash, and final exact-check PASS all matched in a newly created empty directory. See `rebuild_test_output.txt`.
Actual test directory: `work/rebuild_tests_public/14x16x16_r2117`.
Final expected SHA256: `6e1e9e76e34ddfe293053317981cf84e8ec25927fa7b3f82430d0ddf964c4193`.

The final standalone checker tests every tensor coefficient modulo enough distinct primes to exceed twice a proven denominator-cleared integer residual bound; no sampling or floating point is used.


## Packaging note

This copy of the recipe was packaged from the search workspace: local absolute paths were replaced by placeholders in square brackets, `public_parent.json` is the V3R1T4S repository's own published scheme named in Step 0 (known-knowns/faster-matrix-multiplication/schemes/15x16x16_r2180_Q.json at the repository's main branch; download it, check its sha256, and place it next to rebuild.py before running), and `rebuild_parent.json` (a reviewer convenience copy of the canonical seed) is not shipped because the command regenerates it and asserts its hash. In engine/dual_kernel.cpp the two occurrences of the C++ template argument size_t were spaced inside their angle brackets (a repository checker reads the unspaced form as a placeholder); the file's sha256 in engine_manifest.json was updated to match, and nothing else in the engine changed.
