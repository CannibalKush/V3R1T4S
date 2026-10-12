# VNN-COMP 2026: counterexamples for two instances that no verifier resolved

The International Verification of Neural Networks Competition (VNN-COMP) gives neural-network verifiers a set of
*instances*: an ONNX network plus a VNN-LIB property ("for every input in this box, the output satisfies ..."). A tool
either proves the property, finds a counterexample (an input in the box that violates it), or times out. The 2026
results table, `SCORING/results.txt` in github.com/VNN-COMP/vnncomp2026_results, lists 127 of its 3,618 instances as
resolved by **no** participating tool.

**Claim (exact scope), as of 2026-10-12T03:36:49Z.** The two files `witnesses/*/witness_plain.txt` are counterexamples
for these two instances of the benchmark `traffic_signs_recognition_2023` (version directory 2.0), used unmodified:

| network | property | true class | satisfied disjunct | output margin | live row in results.txt |
|---|---|---|---|---|---|
| `3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30` | `model_30_idx_1703_eps_1.00000` | 25 | `(>= Y[0,22] Y[0,25])` | 0.99990918 | `timeout, -, timeout` |
| `3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30` | `model_30_idx_178_eps_1.00000` | 13 | `(>= Y[0,15] Y[0,13])` | 0.96402755 | `timeout, -, timeout` |

For each witness:

- every one of the 5,400 input constraints holds **strictly** (exact rational arithmetic, no tolerance): each pixel is
  at least 2^-10 = 0.0009765625 inside its interval, and every value is exactly representable in float32;
- the output assertion holds at **zero tolerance** under onnxruntime (CPU, float32) and under `onnx.reference`, which
  agree exactly (maximum difference 0.0). The network ends in a softmax; at the box centre (the unperturbed image) the
  true class has probability 1, at the witness another class has probability above 0.96;
- the competition's own validator, `SCORING/counterexamples_v2.py`, run unmodified, returns `correct` ("all assertions
  hold with input_tolerance=0.0, output_tolerance=0.0"), both with the competition's tolerance 1e-4 and with 0.

**The record we beat.** In `results.txt` (fetched 2026-10-12T03:36:49Z, sha256 `ec1b6fcb…eb26f`, byte-identical to
copies fetched on 10 and 11 Oct; the results repository was last pushed on 2026-08-03) both rows read
`['…', 'timeout', '-', 'timeout']` for the three tools of this category (alpha_beta_crown, pyrat, vibecheck). The
results tree at commit `eea564f5` (27,250 entries) contains no counterexample file for either instance. The published
counterexamples for the same two images are for the larger radii eps = 3, 5, 10 and 15; none of those 16 files lies
inside the eps = 1 box (each has 2,136 to 2,612 of its 2,700 coordinates outside it), and a smaller box is not implied
by a larger one. Earlier editions (2023 to 2025) used other image indices for this network. Details and hashes:
`the-record-we-beat/sources_2026-10-12T03-36-49Z.json`.

**Status.** Found by AI agents (see `READ_BEFORE_CITING.md` at the repository root) on 2026-10-11; verified internally
by three independent reviewers with their own code; **not yet reported to the maintainers** (the VNN-COMP organisers)
at the time of this release.

## How the witnesses were found

The traffic-sign networks of this benchmark are binarized: weights in {−1, +1}, sign activations, integer pixel
inputs. Gradient attacks get no useful signal from them, which may be one reason no tool resolved these instances. Our agents
wrote an exact integer model of the 3_30_30 network (checked against onnxruntime: maximum deviation 0.0) and searched
with the CP-SAT constraint solver of Google OR-Tools over pixel perturbations of ±(1 − 2^-10), so that every
coordinate stays strictly inside its interval and is exact in float32, maximising the gap between a wrong class and
the true class. The gap closed from −950 to +10 (idx 1703, 73 s) and from −940 to +4 (idx 178, 351 s) on 4 CPU cores.
The search code is not part of this release; the claim rests on the two witness files and the checkers.

## Credits (please cite)

- **VNN-COMP 2026** and its organisers, who publish every benchmark, every tool's results and the validator. The
  latest competition report is for 2025: K. Kaulen, T. Ladner, S. Bak, C. Brix, H. Duong, T. Flinkow, T. T. Johnson,
  L. Koller et al., *The 6th International Verification of Neural Networks Competition (VNN-COMP 2025): Summary and
  Results*, arXiv:2512.19007.
- **The benchmark `traffic_signs_recognition_2023`** is by Andreea Postovan and Mădălina Eraşcu (source repository
  github.com/apostovan21/vnncomp2023, commit 3587d3b1, as recorded in the benchmark's README; paper: A. Postovan and
  M. Eraşcu, *Benchmarking Local Robustness of High-Accuracy Binary Neural Networks for Enhanced Traffic Sign
  Recognition*, arXiv:2310.03033). The networks classify
  30×30 colour images into 43 traffic-sign classes.
- The competing tools in this category: alpha-beta-CROWN, PyRAT and vibecheck.

## Limitations

- "Unsolved" means that no tool resolved the instance within the competition's 480-second limit. It is not a
  long-standing open problem. These are 2 of the 127 such instances; 7 more traffic-sign instances (on the larger
  48×48 and 64×64 networks) remain unresolved.
- The witnesses move pixels by fractional amounts (±(1 − 2^-10)), so they are not integer-valued images. VNN-LIB uses
  real-valued boxes and the official validator accepts them; they are not claimed as integer-pixel adversarial images.
- Our onnxruntime (1.31.0) is newer than the competition's pin (1.26.0). The reference evaluator gives identical
  outputs and the margins are about 1, so a version-dependent change is implausible but has not been tested on 1.26.0.
- Internal verification only; the organisers have not seen these witnesses.

## Files

```
README.md, RUN_IT_YOURSELF.md, INDEX.csv
witnesses/model_30_idx_1703_eps_1/   witness_plain.txt (2700 values, X[0,h,w,c] row-major), witness_v2.txt (VNN-LIB 2.0 assignment)
witnesses/model_30_idx_178_eps_1/    the same for the second instance
verify-it-yourself/  vnncheck.py (standalone checker), mutate.py (negative controls), official_validate.py (runs the
                     competition's validator unmodified), run_checks.sh, RECEIPTS.md
the-record-we-beat/  sources_2026-10-12T03-36-49Z.json (fetch times, HTTP headers, sha256, extracted rows), parse_results.py
```

The ONNX model and the VNN-LIB properties are **not** redistributed here; the checkers download them from the
official benchmark repository at commit `303f2327a8e8411efc4457da03d2016ce42733cf` and check their sha256.
