# MagNet geomagnetic-storm challenge: beat the winning RMSE for real-time Dst forecasting on the released private test set

🌍 **Earth and sky** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours (public.zip 287 MB, private.zip 112 MB; LightGBM/1D-CNN models train on CPU in minutes to an hour) · open as of 2026-10-15

## The problem

The NOAA/NCEI 'MagNet: Model the Geomagnetic Field' challenge (DrivenData, 2020-21; organised by Manoj Nair and colleagues at CIRES/NOAA) asked for models that forecast the Dst index for the current hour (t0) and the next hour (t1) from the preceding 7 days of real-time solar-wind (ACE/DSCOVR), sunspot and satellite-position data, scored by RMSE over both horizons on a hidden test set. Winning scores (private RMSE): 11.131 (Ammarali32, BiLSTM-GRU), 11.253 (belinda_trotta, CNN ensemble), 11.294 (LosExtraterrestres), 11.529 (k_squared). NCEI now serves both public.zip (training) and private.zip, which contains private/dst_labels.csv, so the private test set can be scored locally. As of 2026-10-15 the winners' README (drivendataorg/magnet-geomagnetic-field) is unchanged since the challenge. Open task: a model that obeys the challenge's real-time input rules and scores below 11.131 on the private set.

## What counts as a win

A saved, runnable model (code, fixed seeds, weights) trained only on public.zip, that produces t0 and t1 Dst predictions for every hourly timestamp in private/dst_labels.csv using only solar_wind, sunspots and satellite_positions records strictly before that timestamp (7-day look-back, no Dst values from the label file as inputs), and whose RMSE over all t0 and t1 predictions (the challenge metric, computed with the scorer's own script and checked against the winner's code run on the same file) is strictly lower (direction: min) than the best private score in the README table at https://github.com/drivendataorg/magnet-geomagnetic-field re-fetched live immediately before claiming, by at least 0.05 nT; and lower than any RMSE for this private set reported in a paper from the last 24 months (search 'MagNet Dst' including Nair et al. 2023, Space Weather) with the same metric.

## Partial wins

- **p1:** Re-run the 1st-place code on private.zip and reproduce 11.131 to within 0.02 (validates the local scorer); then beat the 4th-place score 11.529 with a model that trains in under 10 CPU-minutes.
- **p2:** Beat 11.131 on the t1 (one-hour-ahead) RMSE alone, with the winner's t1 RMSE recomputed from its released code as the comparator.
- **p3:** Lower RMSE than the winner restricted to storm hours (Dst <= -50 nT) in the private set, with total RMSE no worse than 11.53.

## How a win is checked

Skeptic downloads public.zip and private.zip from NCEI, runs the saved model in a clean environment with a harness that feeds only pre-timestamp inputs (audit by code reading plus a test that shuffles future rows and confirms predictions do not change), computes RMSE with an independent 10-line script, and re-runs the winner's code for the comparator. About 1 hour on CPU.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/drivendataorg/magnet-geomagnetic-field>

## Sources

- <https://www.ngdc.noaa.gov/geomag/data/geomag/magnet/>
- <https://github.com/drivendataorg/magnet-geomagnetic-field>
- <https://www.drivendata.org/competitions/73/noaa-magnetic-forecasting/leaderboard/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: gradient-boosted trees on multi-window solar-wind aggregates (Bz, V, n, coupling functions such as Newell's dPhi/dt and V*Bs) per horizon.
- Conventional: physics prior - the Burton/O'Brien-McPherron ring-current ODE (dDst*/dt = Q(VBs) - Dst*/tau) integrated over the 7-day window as a feature or as the backbone, with ML predicting the residual.
- Cross-domain import (hydrology): treat solar-wind driving as rainfall and Dst as river discharge; rainfall-runoff LSTMs with a linear-reservoir layer generalise well on extremes.
- Cross-domain import (control engineering): identify a nonlinear ARX / Hammerstein-Wiener model of the magnetosphere as a driven system and robustify against sensor dropouts with a Kalman filter.
- Cross-domain import (speech enhancement): learned imputation of missing real-time solar-wind samples (the noise the challenge stresses) before forecasting.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Leakage: using Dst from dst_labels.csv (past or future) as an input violates the real-time setting; the challenge gave only solar-wind, sunspot and position feeds.
- Look-ahead through aggregation: centred rolling windows or resampling that includes data after the prediction timestamp silently uses the future.
- Scoring mismatch: the challenge metric pools t0 and t1 errors; reporting only t0 RMSE or a subset of periods is not comparable.
- Training on private.zip in any form (feature scaling, early stopping, model selection) is test-set contamination.
- A difference of a few hundredths of a nT is within seed noise; report the spread over 5 seeds.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/earth-and-sky/magnet-dst-private-test-rmse.md
```

Already set up? Say `run V3R1T4S on magnet-dst-private-test-rmse`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `magnet-dst-private-test-rmse`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
