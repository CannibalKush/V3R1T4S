# Check results (RobustBench CIFAR-100, Addepalli2022Efficient_RN18)

## Run for this release (quick check)

`N=500 sh verify-it-yourself/run_checks.sh` (python 3.11, numpy 2.4.6, torch 2.14.1, torchvision, robustbench 1.1 at
commit 78fcc9e4; cached CIFAR-100 test set and weights) was run on the shipped files from 2026-10-12T03:46:25Z to
03:47:44Z on the build machine (macOS, CPU, 4 threads, load average about 25 from other jobs). Exit code 0, last line
`ALL CHECKS PASSED`.

| check | result |
|---|---|
| archive sha256 = INDEX.csv | yes (`da17d7c6…7a07`) |
| lossless: zip member, re-saved array, raw bytes | all equal to the original (`.npy` sha256 `4eea7cd6…decb`, raw `aabc97bd…1ee0`) |
| CIFAR-100 test images / labels sha256 | `4cb8e5d9…ee19` / `80031c23…c4ad` |
| weights sha256 | `aafda6c1…8587` (RobustBench download) |
| max L∞ over all 10,000 images (float64) | 0.03137254901960784 = 8/255; 0 coordinates above; 0 outside [0, 1]; all finite |
| images left unchanged | 3,455 (the clean-misclassified ones) |
| images 0–499 | clean-correct 321, robust 146, exact ties 0; robust set = `robust_indices.txt` on these images |

**Not re-run for this release:** the full 10,000-image count (about 10–20 minutes of CPU). It is the claim; run
`rbcheck.py` without `--n` to check it.

## Full counts recorded before release (not with the shipped checker)

| when (UTC) | checker | device | clean | robust |
|---|---|---|---|---|
| 2026-10-11T20:27Z – 22:08Z | the finder's own checker (written from the problem statement) | CPU, 4 threads, batch 200 | 6545 | 2757 (0 ties) |
| 2026-10-11T22:09Z | a second checker written before the search | CPU | 6545 | 2757 |
| 2026-10-11 (quick look) | the same second checker | Apple MPS | 6545 | 2757 |
| 2026-10-11 to 12 | independent reviewer 1, own code (weights re-downloaded, sha256 matched; tie-as-robust rule and plain argmax agree) | CPU | 6545 | 2757 |
| 2026-10-11 to 12 | independent reviewer 2, own code (torch 2.14.1, 4 threads, batch 200, on a byte copy of the tensor) | CPU | 6545 | 2757 |

Near-tie rows (CPU logit margins of the fooled images closest to the boundary): 4129 +1.36e-4, 2137 +3.65e-4,
9693 +4.19e-4; spread at most 4e-6 across CPU batch sizes 1/200/250, 1 and 4 threads, float64 and MPS.

The third independent reviewer re-derived the comparison value (live table, papers, code search) and found nothing
below 27.67 %.

## Raw output

```
2026-10-12T03:46:25Z
== sha256 against INDEX.csv
adversarial-examples/x_adv_Addepalli2022Efficient_RN18.npz: matches INDEX.csv
adversarial-examples/robust_indices.txt: matches INDEX.csv
== lossless restore
archive  x_adv_Addepalli2022Efficient_RN18.npz  45517304 bytes  sha256 da17d7c6bbb4c4fffb6dcdb66711f02223ad5c58a1362973d167248107477a07  ok
members  ['x_adv.npy']; x_adv.npy 122880128 bytes stored as 45517168 (DEFLATE)
member x_adv.npy sha256 4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb  == original
loaded array float32 (10000, 3, 32, 32); numpy.save sha256 4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb  == original
raw float32 bytes sha256 aabc97bd6bb05d9f3a6d0d6793c600f16611ea1688041f3becd892bbcdb81ee0  == original
LOSSLESS: yes, bit-identical to the original tensor
== model check
x_adv: float32 (10000, 3, 32, 32), bit-identical to the original (.npy sha256 4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb)
CIFAR-100 test set: images sha256 4cb8e5d9309da489bf6b19cc10cd96c3ae6f8daf225380b605aaee4c0d6aee19 ok; labels sha256 80031c23f8300724c6fbc588e4bccbe41c6392041782148727bb497b0132c4ad ok
threat model (float64, all 10000 images): max Linf 0.03137254901960784 (8/255 = 0.03137254901960784); coordinates above 8/255: 0; outside [0,1]: 0; all finite: True; images left unchanged: 3455
model Addepalli2022Efficient_RN18 (robustbench 1.1, torch 2.14.1): weights sha256 aafda6c19381b62fdb09aa6905331bcaa0341eac76c5080d2a99a95f8ac18587 ok
images 0..499: clean-correct 321, robust 146, exact ties 0 (26 s clean, 21 s adversarial on 4 CPU threads)
  smallest positive margins among fooled images: [0.0023124217987060547, 0.003156423568725586, 0.0034656524658203125]
  robust set equals robust_indices.txt on these images: True (146 expected)
RBCHECK PASS model=Addepalli2022Efficient_RN18 n=500 clean=321 robust=146 max_linf=0.03137254901960784 runtime=56s
ALL CHECKS PASSED
exit=0
2026-10-12T03:47:44Z
```
