# MLGWSC-1 gravitational-wave search challenge: beat the best published sensitive distance at a false-alarm rate of 1 per month on dataset 3

🌍 **Earth and sky** · standard · tractability ★★☆☆☆ · compute: laptop-days (one month of two-detector simulated Gaussian noise per test set, tens of GB; generation and evaluation scripts in the repository; ML inference on CPU/Apple GPU) · open as of 2026-10-15

## The problem

The first Machine Learning Gravitational-Wave Search Mock Data Challenge (Schafer, Zelenka, Nitz, Wang, Wu, and co-authors; Phys. Rev. D 107, 023021, arXiv:2209.11146) evaluates binary-black-hole searches by sensitive distance versus false-alarm rate on one month of simulated two-detector data. Dataset 3 has simulated Gaussian noise whose PSD is drawn per segment from 20 O3a-derived PSDs per detector (files shipped in the repository), and IMRPhenomXPHM signals with isotropic spins (precession) and higher-order modes, component masses 7-50 Msun; its challenge set was generated with seed 470182217, published in the paper, and generate_data.py plus evaluate.py are public. Table IV at FAR = 1 per month on dataset 3: PyCBC (matched filtering) 1577.18 Mpc, TPI FSU Jena (best machine-learning entry) 1487.67 Mpc, cWB 1252.09 Mpc, Virgo-AUTh 1240.68 Mpc. Datasets 1-3 need no detector data download, so the target is reachable even without the GWOSC strain archive. Open task: a search whose sensitive distance at FAR 1/month on dataset 3 exceeds the best published non-PyCBC entry, and (moonshot) the PyCBC entry.

## What counts as a win

Saved foreground and background trigger files (the challenge HDF5 output format) for the dataset-3 challenge set regenerated with the published seed by the unmodified generate_data.py at the repository's pinned PyCBC version, plus the search code, such that the unmodified evaluate.py gives a sensitive distance at FAR = 1 per month strictly greater (direction: max) than 1487.67 Mpc (main win) by more than the evaluation's Monte-Carlo uncertainty (estimated by re-running evaluate.py on the 5 alternative challenge sets made with seeds 1..5), with the Table IV values in the arXiv/journal version of Schafer et al. and the repository https://github.com/gwastro/ml-mock-data-challenge-1 re-fetched live immediately before claiming, and greater than any dataset-3 FAR-1/month value in later papers (search 'MLGWSC-1 dataset 3'; last 24 months); the search must not be trained or tuned on data generated with the challenge seed. Exceeding PyCBC's 1577.18 Mpc under the same rules is the moonshot win.

## Partial wins

- **p1:** Exceed the Virgo-AUTh dataset-3 value (1240.68 Mpc) at FAR 1/month with a model trained in under 24 laptop-hours.
- **p2:** Beat 1487.67 Mpc on dataset 1 or 2 instead (published bars: dataset 1 ML best 2362.51, dataset 2 ML best 1455.09 Mpc at FAR 1/month).
- **p3:** Match the best ML entry within 2% while analysing the month of data in under 1 hour of wall-clock on a laptop.

## How a win is checked

Skeptic regenerates the dataset-3 challenge set with the published seed, runs the saved search (or checks the saved trigger files hash-match a fresh run), runs evaluate.py, and runs the 5-seed uncertainty check. Laptop-hours to a day.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/gwastro/ml-mock-data-challenge-1>

## Sources

- <https://github.com/gwastro/ml-mock-data-challenge-1>
- <https://arxiv.org/abs/2209.11146>
- <https://doi.org/10.5281/zenodo.5772264>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: 1D CNN on whitened strain with curriculum training on SNR, followed by coincidence and time-slide background estimation.
- Conventional: a hybrid - ML pre-filter feeding a reduced template bank matched filter, keeping matched-filter background statistics.
- Cross-domain import (radar signal processing): constant-false-alarm-rate detection with learned chirp dictionaries, i.e. sparse matched filtering over a compressed template basis (SVD of the bank).
- Cross-domain import (speech recognition): spectrogram transformers with keyword-spotting losses trained on chirps, which handle precession-induced amplitude modulation.
- Cross-domain import (particle physics triggers): train against the background estimate directly (time-slid noise) to optimise the low-FAR tail, not classification accuracy.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Training on noise generated with the challenge seed (or tuning thresholds on the challenge foreground) is test-set contamination.
- Estimating background only from the foreground file inflated some entries' sensitivity in the paper; use the separate background set as evaluate.py expects.
- Different PyCBC versions change waveform and noise generation; use the repository's pinned requirements.
- Sensitive distance at FAR 1/month rests on a handful of loudest background triggers; differences of tens of Mpc can be noise - use the 5-seed check.
- Dataset 4 needs real O3a noise from GWOSC, which did not resolve from this network on 2026-10-15; do not substitute other noise and call it dataset 4.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/earth-and-sky/mlgwsc1-dataset3-sensitive-distance.md
```

Already set up? Say `run V3R1T4S on mlgwsc1-dataset3-sensitive-distance`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `mlgwsc1-dataset3-sensitive-distance`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
