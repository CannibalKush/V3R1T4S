# Bolide in public GOES GLM lightning-mapper data absent from the NASA GLM bolide catalog

🌍 **Earth and sky** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

NASA's neo-bolide.ndc.nasa.gov publishes a curated catalogue of bolides detected by the GOES-16/17/18/19 Geostationary Lightning Mappers (public JSON API: 11,611 published events on 2026-10-15, latest event 2026-10-06, published 2026-10-12). GLM L2 LCFA files are public on the NOAA open-data S3 buckets (noaa-goes16/17/18/19). The pipeline uses classifiers on GLM group data plus human vetting, so faint, short or stereo-ambiguous bolides can be missed. Open task: a bolide in public GLM data, older than 2 months, that is absent from the live catalogue.

## What counts as a win

A saved candidate (UTC time, lat/lon, GLM file names, group/event IDs, extracted light curve, detection code) such that: the light curve lasts >= 100 ms with a smooth single- or multi-peaked meteor shape and a spatial track of >= 3 pixels moving consistently; there is NO co-located lightning (no other GLM flashes within 50 km and +/- 2 min); the same detector run on a null set (one month of data in a lightning-active region, plus the candidate month with group times shuffled within flashes) gives an expected false count < 0.05 at the candidate's score over the searched span; ideally stereo detection by two GLMs; and no event within +/- 2 min / 200 km in the bolide JSON API and the CNEOS fireball API, both re-fetched live immediately before claiming.

## Partial wins

- **p1:** A stereo (two-GLM) candidate whose triangulated altitude is 20-90 km and whose ground track is non-lightning-like, absent from the catalog.
- **p2:** A blind detector run over one month of GLM-16 data that recovers >= 90% of the catalog's events for that month, with the residual non-catalog detections listed and hand-vetted.

## How a win is checked

Skeptic downloads the cited GLM L2 files from the NOAA S3 bucket, re-extracts the groups, plots the light curve and track, checks for nearby lightning flashes in the same and adjacent files, and queries both catalogs live. Under 30 minutes.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://neo-bolide.ndc.nasa.gov/>

## Sources

- <https://neo-bolide.ndc.nasa.gov/>
- <https://neo-bolide.ndc.nasa.gov/service/event/public>
- <https://noaa-goes16.s3.amazonaws.com/?list-type=2&prefix=GLM-L2-LCFA/>
- <https://noaa-goes18.s3.amazonaws.com/?list-type=2&prefix=GLM-L2-LCFA/&max-keys=1>
- <https://noaa-goes19.s3.amazonaws.com/?list-type=2&prefix=GLM-L2-LCFA/&max-keys=1>
- <https://ssd-api.jpl.nasa.gov/fireball.api>
- <https://cneos.jpl.nasa.gov/fireballs/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: re-implement the published GLM bolide features (group duration, track linearity, energy ratio) with a random forest trained on catalog events vs lightning.
- Conventional: search overlap regions of GOES-East/West for stereo coincidences that single-satellite classifiers down-weight.
- Cross-domain import (particle physics triggers): a two-level trigger with a loose online cut and an offline likelihood ratio, estimating the false-positive rate on time-shifted data.
- Cross-domain import (exoplanet transit search): treat each pixel's group-energy time series like a light curve and apply matched filters (box/Gaussian templates) for meteor-shaped pulses.
- Cross-domain import (sports/ball tracking): RANSAC line fitting on event centroids to separate straight bolide tracks from branching lightning.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Lightning is the dominant false positive; isolated 'bolt from the blue' flashes and sprites can be linear and short.
- Glint and instrument artefacts (sun glint over oceans, South Atlantic Anomaly hits, GLM 'blooming') create bright compact events.
- Catalog publication lags detection by days; candidates from the last 2 weeks may simply be unpublished - restrict to windows older than 2 months.
- Do not report to NASA; claim only the saved verified candidate.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/earth-and-sky/glm-bolide-not-in-nasa-catalog.md
```

Already set up? Say `run V3R1T4S on glm-bolide-not-in-nasa-catalog`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `glm-bolide-not-in-nasa-catalog`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
