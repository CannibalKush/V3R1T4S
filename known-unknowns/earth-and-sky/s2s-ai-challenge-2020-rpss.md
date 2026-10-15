# WMO S2S AI Challenge: beat the best RPSS for week 3-4 and 5-6 temperature and precipitation tercile forecasts in 2020

🌍 **Earth and sky** · standard · tractability ★★☆☆☆ · compute: laptop-days (ECMWF hindcasts/forecasts as NetCDF from the ECMWF object store, tens of GB for t2m and tp; post-processing models train on CPU) · open as of 2026-10-15

## The problem

The WMO Prize Challenge to improve subseasonal-to-seasonal predictions using AI (2021; organised by Andrew Robertson, Frederic Vitart, Aaron Spring and colleagues) scored probabilistic tercile forecasts of 2 m temperature and biweekly precipitation for weeks 3-4 and 5-6, for all 2020 forecast start dates, by RPSS relative to climatology, averaged over the globe land grid. The archived leaderboard (github.com/aaronspring/s2s-ai-challenge-leaderboard, last automated update 2022-11-07) has the best score RPSS = 0.0459475 by the CRIM team (submission-methods-7, Jordan Gierschendorf et al.); the next teams are near 0.0 or negative. Data remain downloadable from the ECMWF object store by plain GET (S2S data licence terms apply; no registration). Open task: a forecast for 2020 built only from the allowed training period that beats 0.0459 with the challenge's scorer.

## What counts as a win

A saved submission NetCDF in the challenge format (t2m and tp, lead_time weeks 3-4 and 5-6, all 53 2020 start dates, tercile probabilities) plus code, trained only on hindcast/observation data allowed by the challenge rules (no 2020 observations), whose RPSS computed by the challenge's own scoring code (s2s-ai-challenge-template RPSS_verification notebook / scorer, unmodified) against the 2020 terciled observations is strictly greater (direction: max) than the best RPSS on the leaderboard README at https://github.com/aaronspring/s2s-ai-challenge-leaderboard re-fetched live immediately before claiming, by at least 0.002, and greater than any RPSS for the same 2020 test reported in papers of the last 24 months (search 'S2S AI challenge RPSS', including Horat and Lerch's subseasonal post-processing work and the challenge overview by Vitart et al.).

## Partial wins

- **p1:** Reproduce the CRIM score within 0.002 from their released code (github.com/crim-ca/crims2s) and then beat it on one of the two variables alone.
- **p2:** RPSS > 0 for both variables and both lead windows simultaneously (no negative component), which no 2021 entry except CRIM achieved.
- **p3:** A no-neural-network method (e.g. EMOS with spatial smoothing) with RPSS >= 0.040.

## How a win is checked

Skeptic downloads the needed ECMWF forecast, hindcast and observation files from the object store, runs the unmodified scorer from the template repository on the saved NetCDF, checks that the training code never opens 2020 observation files (sandbox run without them), and compares to the live leaderboard. A few hours.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/aaronspring/s2s-ai-challenge-leaderboard>

## Sources

- <https://s2s-ai-challenge.github.io/>
- <https://github.com/aaronspring/s2s-ai-challenge-leaderboard>
- <https://github.com/aaronspring/s2s-ai-challenge-template>
- <https://github.com/ecmwf-lab/climetlab-s2s-ai-challenge>
- <https://github.com/crim-ca/crims2s>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: ensemble model output statistics on ECMWF tercile probabilities with spatial smoothing and shrinkage toward climatology where hindcast skill is low.
- Conventional: combine ECMWF, NCEP and ECCC ensembles (all in the challenge data) with weights learned per region and lead from hindcasts.
- Cross-domain import (finance): Bayesian shrinkage of predictive signals with low signal-to-noise (James-Stein toward climatology) - the main lesson of S2S is that most of the grid has no skill.
- Cross-domain import (epidemiology forecast hubs): quantile/probability ensembling with trimmed means, which reliably beats individual models under scoring rules like WIS and RPS.
- Cross-domain import (image restoration): treat the global probability fields as images and use a small U-Net on anomaly maps conditioned on MJO/ENSO indices.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Using 2020 observations (directly or via climatology recomputed with 2020) is leakage.
- RPSS is averaged in a specific way (by the scorer revised on 2021-10-22); a home-made RPSS will not match - use the template's code.
- Forecasts that are overconfident score badly in RPS; many entries were negative because they beat the raw ECMWF on hindcasts but not out of sample.
- Precipitation tercile edges come from the challenge files; recomputing them changes the categories.
- One test year (2020) is a small sample with La Nina; gains of 0.001-0.002 are within noise.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/earth-and-sky/s2s-ai-challenge-2020-rpss.md
```

Already set up? Say `run V3R1T4S on s2s-ai-challenge-2020-rpss`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `s2s-ai-challenge-2020-rpss`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
