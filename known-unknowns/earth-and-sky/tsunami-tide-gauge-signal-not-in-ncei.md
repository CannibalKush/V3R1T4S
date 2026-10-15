# Tsunami recorded on open tide-gauge data but absent (as an event or at that gauge) from the NCEI Global Historical Tsunami Database

🌍 **Earth and sky** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours (1-min gauge series are KB-MB per day) · open as of 2026-10-15

## The problem

The NOAA NCEI/WDS Global Historical Tsunami Database (HazEL) lists ~1,600 confirmed events with runup and tide-gauge observations; NCEI's own completeness studies (Wright, Arcos, Varner and Stroker 2021) note that small tsunamis seen only on tide gauges can be missing. The IOC Sea Level Station Monitoring Facility serves 1-min data from 1,000+ gauges openly. Open task: find a tsunami signal (from an earthquake, landslide, volcano or meteotsunami) clearly recorded on >= 2 open tide gauges that NCEI lists neither as an event nor as a runup/gauge observation at those stations.

## What counts as a win

A saved bundle (raw IOC SLSMF series for >= 2 gauges, de-tiding code, source parameters) showing: on each gauge, a band-passed (2-120 min) signal with peak amplitude > 5x the RMS of the preceding 24 h in the same band; arrival times at all gauges consistent within +/- 10 min with shallow-water travel times computed from the source (earthquake from USGS ComCat, or a meteotsunami pressure jump with propagating-front check); signals absent on the same gauges in the same hours on control days; and the NCEI events API (https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events) and runups API, re-fetched live immediately before claiming, have no event within +/- 1 day of the source in that region (main win) or no runup row for those gauges (partial win).

## Partial wins

- **p1:** Gauge observations (amplitude, arrival) for a listed NCEI event at >= 2 gauges where NCEI has no runup rows for those stations.
- **p2:** A meteotsunami (atmospheric pressure jump with matching propagation speed) with > 0.3 m amplitude on >= 2 gauges not in NCEI.
- **p3:** A completeness map: fraction of M >= 6.5 shallow subsea earthquakes 2015-2025 with any tsunami signal on open gauges vs NCEI listing, reproducible from saved code.

## How a win is checked

Skeptic re-downloads the IOC SLSMF series (GET service.php query=data), re-runs de-tiding and band-pass, recomputes travel times with a bathymetry-based or simple shallow-water estimate, and re-queries the NCEI API. Under an hour.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search>

## Sources

- <https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search>
- <https://www.ioc-sealevelmonitoring.org/service.php>
- <https://www.ioc-sealevelmonitoring.org/list.php>
- <https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events>
- <https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/runup-search>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: for every M >= 6.0 shallow offshore earthquake (USGS ComCat) since 2010, pull gauges within 1,500 km, de-tide (UTide), band-pass and test arrivals against travel-time predictions.
- Meteotsunami hunting: match gauge oscillations with pressure jumps in open surface-pressure data and propagation speeds near sqrt(g h).
- Cross-domain import (seismology): STA/LTA triggers and array beamforming across many gauges, treating the gauge network like a seismic array.
- Cross-domain import (audio signal processing): spectrogram ratio against a station's own long-term noise spectrum (as in speech enhancement) to reveal small tsunami energy.
- Cross-domain import (astronomy transient search): difference against a same-time-of-tide 'reference' built from control days, then threshold the residual like difference imaging.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Seiches and harbour resonances ring at similar periods on most days; the control-day test is mandatory.
- Tide-gauge glitches, datum runs and data gaps produce spikes; reject series with level runs.
- Storm surges and infragravity waves during storms mimic small tsunamis; check weather.
- NCEI may list the event under a different source time or as a 'questionable' validity code; search with tolerance and all validity codes.
- Do not report to NCEI or IOC; the claim is a vetted candidate.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/earth-and-sky/tsunami-tide-gauge-signal-not-in-ncei.md
```

Already set up? Say `run V3R1T4S on tsunami-tide-gauge-signal-not-in-ncei`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `tsunami-tide-gauge-signal-not-in-ncei`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
