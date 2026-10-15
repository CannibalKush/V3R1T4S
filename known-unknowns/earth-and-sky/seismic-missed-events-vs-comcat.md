# Missed local earthquakes in open EarthScope/IRIS waveforms, above the regional completeness magnitude, absent from USGS ComCat

🌍 **Earth and sky** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

USGS ComCat (live FDSN event service) is the authoritative US catalog; open continuous waveforms are served by the EarthScope/IRIS FDSN dataselect service. Template matching and ML pickers routinely find 2-10x more events than standard catalogs, mostly below completeness. The open, non-trivial task: an earthquake at or above the regional magnitude of completeness that ComCat (and ISC) do not list, in a region/time where no published enhanced catalog covers it.

## What counts as a win

A saved event package (origin time, location, depth, local magnitude with method, >= 8 P/S picks on >= 4 public stations, FDSN request URLs on service.earthscope.org, detection code) such that: the skeptic's independent re-location (e.g. NonLinLoc/HypoInverse-style grid search) gives RMS <= 0.3 s and horizontal error <= 5 km; the detector run on a null set (the same continuous data with station traces circularly time-shifted against each other by >= 10 min, or time-reversed) yields an expected false count < 0.05 over the searched span at the candidate's statistic; the magnitude is >= the regional ComCat completeness magnitude Mc computed by the skeptic (maximum curvature + 0.2) from a live ComCat query for that region over the 5 surrounding years; not a quarry blast (daytime-cluster and S/P amplitude checks; ComCat eventtype filters); and a live ComCat query (and the ISC bulletin if reachable) re-fetched immediately before claiming returns no event within +/- 30 s and 50 km. Must not be inside the space-time window of a published enhanced catalogue (e.g. QTM Southern California, Ross et al. 2019) unless absent there too.

## Partial wins

- **p1:** A missed event of magnitude >= Mc - 0.3 with the same location-quality requirements, in a ComCat-authoritative network region (not offshore).
- **p2:** A template-matching catalogue for one sparse-network region and year that recovers >= 95% of ComCat events there and adds >= 3x more detections, each with CC >= 0.6 on >= 3 stations, saved and re-runnable.
- **p3:** A ComCat event demonstrably mislocated by > 20 km (re-location with >= 8 picks and RMS <= 0.3 s), saved with picks.

## How a win is checked

Skeptic fetches the listed waveforms from the FDSN dataselect URLs (minutes), hand-checks picks on band-passed traces, re-locates with a 1D regional model, recomputes ML from Wood-Anderson-simulated amplitudes, recomputes Mc from a live ComCat query, and runs the live ComCat absence query. Under 1 hour.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://earthquake.usgs.gov/fdsnws/event/1/>

## Sources

- <https://earthquake.usgs.gov/fdsnws/event/1/>
- <https://service.earthscope.org/fdsnws/dataselect/1/>
- <https://service.earthscope.org/fdsnws/station/1/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: EQcorrscan template matching from ComCat templates in sparse-network regions (Basin and Range, Great Plains induced-seismicity areas, Alaska interior).
- Conventional: PhaseNet/EQTransformer via SeisBench on CPU followed by GaMMA association.
- Cross-domain import (radio astronomy/pulsar search): matched filtering with a dedispersion-like moveout stack (beamforming across stations) to detect coherent arrivals below single-station SNR.
- Cross-domain import (gravitational-wave data analysis): chi-square signal-consistency veto and time-slide background estimation to control false detections.
- Cross-domain import (speech recognition): spectrogram fingerprinting (FAST, locality-sensitive hashing) to find repeating events without templates.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Most detections are below Mc and trivially 'missed'; the Mc criterion is mandatory.
- Quarry/mining blasts and noise bursts (wind, traffic) mimic events - check time-of-day patterns and S/P amplitude ratios; ComCat often lists blasts separately (eventtype=quarry blast).
- Teleseismic phases or aftershock coda can be mis-associated as local events.
- ComCat updates with delay; very recent windows may be missing events that will appear - use windows older than 6 months.
- Never report to USGS or any agency.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/earth-and-sky/seismic-missed-events-vs-comcat.md
```

Already set up? Say `run V3R1T4S on seismic-missed-events-vs-comcat`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `seismic-missed-events-vs-comcat`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
