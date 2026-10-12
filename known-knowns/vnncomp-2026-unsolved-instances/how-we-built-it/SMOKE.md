# Smoke run of the generating code (2026-10-11)

Run from a scratch working directory with the scripts taken from this repository copy (`how-we-built-it/`).
Environment: Python 3.12.13, the versions in `requirements.txt`, Apple M5 (10 cores), macOS, `nice -n 10`,
`OMP_NUM_THREADS=2`, load average about 20 to 35 from other jobs. Benchmark files: the three files of the pinned
commit (sha256 `baeca5c8…8a83`, `5e4318e8…590a`, `3b690c29…e20e`, checked) in the `downloads/` layout that
`verify-it-yourself/vnncheck.py --cache downloads` produces. Paths below are relative to that working directory;
`H` is this `how-we-built-it/` directory.

## 1. Regenerate the published witnesses from the checkpoints (deterministic)

```sh
sh $H/regenerate_from_checkpoints.sh downloads regen
```
```
pw 10 target 25 argmax 22 ... margin 0.9999091625213623 n changed coords 1826 min dist to bound 0.0009765625
pw 9 target 13 argmax 15 ... margin 0.9640275239944458 n changed coords 1692 min dist to bound 0.0009765625
idx_1703 witness_plain.txt: identical to published (80f4b5a8284931dd0f970d61f1289db47b62a46856edbcb9f19c76334c5580f8)
idx_1703 witness_v2.txt: identical to published (c0a0e2177da623d49fadb5d1971fdb3cbd7eac1fa357445602c49469f79a17fb)
idx_178 witness_plain.txt: identical to published (83c8b41e31f7f44ada880ffd67de003e06891d9b3994a18a49154af36f35ac98)
idx_178 witness_v2.txt: identical to published (281aba6d70b19ce536c41eef4d82e4eb508accadf7247e31204d631cb863bb8f)
REGENERATED: all four witness files byte-identical
real 8.30
```
Matches expectation (the same result was obtained with the original, uncleaned scripts).

## 2. Exactness of the integer model

```sh
python3 -I $H/check_surrogate.py
```
```
model_30_idx_1703_eps_1.00000: target 25, centre L_t=2492, best other class 22 at 1542, gap 950, layer1 |a|<=26: 481, ... ort-vs-int max dev 0.00e+00, ort y_t=1.000000
model_30_idx_178_eps_1.00000: target 13, centre L_t=2814, best other class 15 at 1874, gap 940, layer1 |a|<=26: 629, ... ort-vs-int max dev 0.00e+00, ort y_t=1.000000
max |ort MatMul - surrogate logits| over all tests: 0.0
real 4.38
```
Matches the original run's output line for line.

## 3. Short CP-SAT search on idx 1703 (60 s limit, 2 workers)

Warm start from the saved hint, as in the original run but with 2 workers and 60 s instead of 4 workers and 900 s:
```sh
python3 -I $H/cpsat_bnn30.py --vnnlib downloads/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib/model_30_idx_1703_eps_1.00000.vnnlib.gz \
  --cls 22 --pw 10 --time 60 --workers 2 --hint $H/checkpoints/hint_idx_1703_cls22.json --out smoke_1703.json
```
```
model built in 14.1s: {'n_unst1': 481, 'n_strict_rule': 0, 'n_pix': 2496, 'n_unst2': 6546, 'centre_D': -950, 'obj_const': -658, 'n_obj_terms': 3363} target 25 pw 10
[   18.2s] solution obj=-706 surrogate D=-706 argmax=25 ...
[   18.3s] solution obj=-10 surrogate D=-10 argmax=25 ...
[   18.5s] solution obj=-6 surrogate D=-6 argmax=25 ...
[   20.2s] solution obj=2 surrogate D=2 argmax=22 L_cls=2054 L_t=2052 n_pix_changed=1834 min|a1|=0.0000 ymargin=0.7616
*** PROPERTY-SATISFYING SOLUTION FOUND (surrogate): D=2 softmax margin 0.7616 ***
status FEASIBLE obj 2.0 bound 1918.0 wall 20.2s
real 27.06
```
The model statistics equal those in the original run log (481, 2,496, 6,546, −950, −658, 3,363). A counterexample was
found within the limit (a different one from the published witness, as expected for a parallel solver).
`make_witness.py --ckpt smoke_1703.json --pw 10 ...` then `verify-it-yourself/vnncheck.py --cache downloads --instance 1703 --witness <it>`:
```
  input box, exact rationals, strict: True; smallest distance to a bound = 1/1024 = 0.0009765625
  onnxruntime 1.31.0 CPU float32: output assertion holds at zero tolerance: True; margin 0.76159412; argmax 22
  onnx.reference 1.23.2: output assertion holds at zero tolerance: True; margin 0.76159411; argmax 22
VNNCHECK PASS instance=3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_1703_eps_1.00000 margin=0.76159412 min_input_slack=0.0009765625
```

Same search **without** the hint (from the box centre), 60 s, 2 workers:
```
model built in 13.2s: {... same statistics ...} target 25 pw 10
[   16.4s] solution obj=-982 ...
[   59.8s] solution obj=-10 ...
[   60.0s] solution obj=-2 ...
[   60.2s] solution obj=6 surrogate D=6 argmax=22 L_cls=2048 L_t=2042 n_pix_changed=1872 min|a1|=0.0000 ymargin=0.9951
*** PROPERTY-SATISFYING SOLUTION FOUND (surrogate): D=6 softmax margin 0.9951 ***
status FEASIBLE obj 6.0 bound 1906.0 wall 60.2s
real 66.78
```
Found right at the time limit, so a 60-second cold run may as well end without one; its witness also gives
`VNNCHECK PASS` (margin 0.99505480, onnxruntime and onnx.reference identical). The idx 178 search (351 s on 4 workers
originally) was not repeated.
