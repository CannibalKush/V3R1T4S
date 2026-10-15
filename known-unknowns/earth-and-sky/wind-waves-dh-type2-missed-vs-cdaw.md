# Decametric-hectometric type II radio burst in open Wind/WAVES (and STEREO/WAVES) data absent from the CDAW type II list

🌍 **Earth and sky** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours (Wind/WAVES RAD1/RAD2 daily spectra are MB per day; 1996-2024 is a few GB) · open as of 2026-10-15

## The problem

The CDAW list of Wind and STEREO WAVES decametric-hectometric (DH) type II bursts and associated CMEs (Gopalswamy, Makela and Yashiro, Sun and Geosphere 2019) catalogues slowly drifting radio emission from CME-driven shocks starting at or above 1 MHz, from 1996-05-15 to 2024-12-29 on 2026-10-15, with flare and CME associations from the CDAW SOHO/LASCO CME catalog. The list is human-curated from dynamic spectra, so faint, short or overlapping bursts can be missed. Open task: a DH type II burst in public Wind/WAVES data with a supporting CME that the list does not contain.

## What counts as a win

A saved candidate (start/end UT, frequency range, drift rate, Wind/WAVES RAD1/RAD2 file names, extracted dynamic spectrum, detection code) such that: an emission lane with negative drift consistent with a shock speed of 300-3000 km/s in a standard coronal density model persists >= 10 min at >= 3 sigma above the frequency-channel background and is seen in both Wind and (after 2006-10) at least one STEREO/WAVES receiver or with fundamental-harmonic structure; the same detector run on time-reversed spectra (positive drifts) and on the full 1996-2024 data gives an estimated false-alarm count below 0.05 at the candidate's statistic; a CME in the CDAW SOHO/LASCO catalog launched within 2 h before the burst with speed >= 400 km/s; and no entry overlapping the burst time in https://cdaw.gsfc.nasa.gov/CME_list/radio/waves_type2.html re-fetched live immediately before claiming, including 'uncertain' rows.

## Partial wins

- **p1:** A listed burst whose end time or end frequency is wrong by > 1 h or a factor 2 in frequency, demonstrated with the same detection and null test.
- **p2:** A blind detector that recovers >= 90% of the list's 2011-2014 bursts with fewer than 1 false lane per month, saved and re-runnable.
- **p3:** A candidate after 2024-12-29 (beyond the list's current end) meeting all criteria, labelled 'not yet catalogued' rather than 'missed'.

## How a win is checked

Skeptic downloads the cited Wind and STEREO WAVES files from SPDF, recomputes background-normalised dynamic spectra, re-fits the drift, reruns the time-reversed null, checks the CDAW CME catalog and the type II list. Under 45 minutes.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://cdaw.gsfc.nasa.gov/CME_list/radio/waves_type2.html>

## Sources

- <https://cdaw.gsfc.nasa.gov/CME_list/radio/waves_type2.html>
- <https://cdaw.gsfc.nasa.gov/CME_list/>
- <https://spdf.gsfc.nasa.gov/pub/data/wind/waves/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: Hough/Radon transform of background-subtracted log-frequency spectra to find straight drifting lanes in log f vs log t.
- Conventional: start from every fast (>= 900 km/s) CDAW CME without a listed type II and inspect the 2 h after launch.
- Cross-domain import (gravitational-wave chirp searches): matched filtering with a bank of drift templates derived from shock-speed and density-model grids.
- Cross-domain import (marine bioacoustics): whale-call contour trackers that follow tonal drifts through noisy spectrograms.
- Cross-domain import (pulsar searches): dedispersion-like stacking along predicted drift paths to raise faint lanes above noise.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Type III bursts (fast drift) and their storms dominate the spectra; require drift rates in the type II range.
- Terrestrial auroral kilometric radiation and interference lines mimic narrow-band features; check frequency range and spacecraft geometry.
- Overlapping events: the list merges complex periods into single rows; check all rows overlapping in time.
- Associating a burst with an unrelated CME by timing alone is easy; require speed and position consistency.
- Do not contact CDAW; claim only the saved candidate.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/earth-and-sky/wind-waves-dh-type2-missed-vs-cdaw.md
```

Already set up? Say `run V3R1T4S on wind-waves-dh-type2-missed-vs-cdaw`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `wind-waves-dh-type2-missed-vs-cdaw`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
