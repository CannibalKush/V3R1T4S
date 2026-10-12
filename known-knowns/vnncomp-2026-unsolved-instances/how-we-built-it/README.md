# How we built the two witnesses

The code that found the two counterexamples in `../witnesses/`: an exact integer model of the binarized network
`3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30`, a CP-SAT (Google OR-Tools) search over pixel perturbations, and the
script that turns a CP-SAT solution into the witness files. All commands are run from the family directory
`known-knowns/vnncomp-2026-unsolved-instances/`.

## Files

| file | what it does |
|---|---|
| `bnn.py` | Reads the ONNX model (weights all ±1), and evaluates the network exactly in integers: conv 16×3×3×3 → sign → conv 32×16×2×2 → sign → dense 23,328×43 (sign means +1 if the pre-activation is ≥ 0, which is what the graph's Sign → +0.1 → Sign does). Parses the input box and true class from the VNN-LIB file. `pixel_map` defines the search space: x = v + off + m·d with v = floor((lo+hi)/2), integer d in [lo−v, hi−v], m = 1 − 2^-pw, and a half-step offset only for pixels whose box is clipped at 0 or 255. Every such x lies strictly inside the box and is exact in float32. |
| `check_surrogate.py` | Checks the integer model against onnxruntime: the pre-softmax MatMul output must equal the integer logits exactly at the box centres, 20 random integer points and 20 random real points per box (numpy seed 0). |
| `cpsat_bnn30.py` | Builds the CP-SAT model: one integer variable per pixel that can affect an unstable first-layer neuron, one Boolean per unstable first-layer and second-layer neuron (neurons whose sign cannot change over the box are fixed by interval bounds), and the exact integer logit difference L_cls − L_true as the objective to maximise. Each new solution is replayed through `bnn.py` and saved as a JSON checkpoint (`d` vector, NHWC order); the search stops when the difference is ≥ 2 and the softmax margin is ≥ 1e-5. |
| `make_witness.py` | Turns a checkpoint into `witness_plain.txt` (2,700 values, X[0,h,w,c] row-major) and `witness_v2.txt` (VNN-LIB 2.0 assignment, with the Y block replayed by onnxruntime, CPU, one thread). Asserts that every value is float32-exact and strictly inside the box. |
| `regenerate_from_checkpoints.sh` | Rebuilds both published witnesses from the saved solutions and compares sha256 with `../witnesses/`. |
| `checkpoints/` | The CP-SAT solutions that produced the published witnesses (`ckpt_idx_1703_cls22.json`, `ckpt_idx_178_cls15.json`) and the warm-start hint used for idx 1703 (`hint_idx_1703_cls22.json`, the best solution of an earlier 60-second run, logit difference −10). |
| `requirements.txt` | Pinned versions of the environment that ran it (Python 3.12.13). |

## Inputs

The benchmark files are **not** included. They are the unmodified files of
github.com/VNN-COMP/vnncomp2026_benchmarks at commit `303f2327a8e8411efc4457da03d2016ce42733cf`,
directory `benchmarks/traffic_signs_recognition_2023/2.0/`, fetched and sha256-checked by the release checker:

```sh
python3 verify-it-yourself/vnncheck.py --cache downloads
```

| file | sha256 (gz, as stored in git) |
|---|---|
| `onnx/3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.onnx.gz` | `baeca5c8bcf58a9b8bf8a22cf59fffd2fc5e2baac0fd1e5be467dbb716f78a83` |
| `vnnlib/model_30_idx_1703_eps_1.00000.vnnlib.gz` | `5e4318e8e9320325f0d03f110439f1febe8b34a407bafd4e737359cb958f590a` |
| `vnnlib/model_30_idx_178_eps_1.00000.vnnlib.gz` | `3b690c291a9f43f4a47ad1987d92abc301c9075fa7567418a1599fe142c3b20e` |

These are the same files (same sha256) as the ones the search used on 2026-10-10.

```sh
pip install -r how-we-built-it/requirements.txt
```

## Regenerate the published witnesses (deterministic, seconds)

```sh
sh how-we-built-it/regenerate_from_checkpoints.sh downloads regenerated
```
Expected: four lines `identical to published (...)` with the sha256 values of `INDEX.csv`
(plain `80f4b5a8…80f8`, v2 `c0a0e217…17fb` for idx 1703; plain `83c8b41e…ac98`, v2 `281aba6d…bb8f` for idx 178), then
`REGENERATED: all four witness files byte-identical`. Equivalent single command for one instance:
```sh
python3 -I how-we-built-it/make_witness.py --ckpt how-we-built-it/checkpoints/ckpt_idx_1703_cls22.json --pw 10 \
  --vnnlib downloads/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib/model_30_idx_1703_eps_1.00000.vnnlib.gz \
  --onnx downloads/benchmarks/traffic_signs_recognition_2023/2.0/onnx/3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.onnx.gz \
  --out regenerated/model_30_idx_1703_eps_1
```

## Re-run the search (not deterministic)

```sh
B=downloads/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib
# idx 1703 (true class 25, target class 22), as run: pw 10, 4 workers, 900 s cap, warm start from the hint
python3 -I how-we-built-it/cpsat_bnn30.py --vnnlib $B/model_30_idx_1703_eps_1.00000.vnnlib.gz --cls 22 --pw 10 \
  --time 900 --workers 4 --hint how-we-built-it/checkpoints/hint_idx_1703_cls22.json --out ckpt_1703.json
# idx 178 (true class 13, target class 15), as run: pw 9 (default), 4 workers, 900 s cap, no hint
python3 -I how-we-built-it/cpsat_bnn30.py --vnnlib $B/model_30_idx_178_eps_1.00000.vnnlib.gz --cls 15 \
  --time 900 --workers 4 --out ckpt_178.json
# then make_witness.py --ckpt ckpt_<idx>.json --pw <10|9> ... as above, and check with verify-it-yourself/vnncheck.py --witness
```
The target class is the runner-up class at the box centre (`check_surrogate.py` prints it). The solver uses OR-Tools'
default random seed (`random_seed = 1`); with several workers CP-SAT is not reproducible across machines or thread
timings, so a rerun finds *a* counterexample (usually a different one), not these exact files.

| instance | model size (unstable layer-1 / layer-2 neurons, pixel variables) | logit gap at centre | original run | result |
|---|---|---|---|---|
| idx 1703 | 481 / 6,546, 2,496 | −950 | 4 workers, nice 10, warm start; model built in 25 s; solution at 72.5 s | difference +10, class 22, softmax margin 0.99991 |
| idx 178 | 626 / 8,423, 2,469 (35 neurons use the strict rule for clipped pixels) | −940 | 4 workers, nice 10, no hint; model built in 23 s; solution at 350.4 s (351.3 s wall) | difference +4, class 15, softmax margin 0.96403 |

Hardware: Apple M5 laptop (10 cores, 32 GB, macOS), heavily shared with other jobs at the time (load average in the
hundreds). Expected output: a checkpoint whose logit difference is ≥ 2 and a witness that `vnncheck.py` reports as
`VNNCHECK PASS`; the published witnesses themselves are reproduced only through the checkpoints above.

## What is and is not the exact original code

- `make_witness.py` and `bnn.py` are the final versions from the run (comments edited; the idx 178 witness was
  written with them, the idx 1703 witness a few minutes earlier with their previous revision). With them the
  regeneration above reproduces all four published files byte for byte, for idx 1703 as well.
- `cpsat_bnn30.py` is the version that ran the idx 178 search; only the hard-coded ONNX path was replaced by `--onnx`
  (and the docstring extended).
  The idx 1703 search (and the 60-second run that produced its hint) ran on an **earlier revision of the same script**
  that was overwritten a few minutes later, when the pixel map was generalised for boxes clipped at 255 (idx 178 has
  315 such coordinates, boxes of width 1; idx 1703 has none). That earlier revision is not preserved. It used
  m = 1 − 2^-10 with no offsets, which is exactly `--pw 10` on the idx 1703 box, and the current script with `--pw 10` builds a model with
  the same statistics as the original run log (481 / 2,496 / 6,546 / centre −950 / objective constant −658 / 3,363
  objective terms); see `SMOKE.md`. The exact command line of the 60-second run that produced the hint was not recorded.
- `check_surrogate.py` is the original exactness check restricted to the two published instances (a side analysis of a
  third image was dropped).
