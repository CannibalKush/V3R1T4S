# Volcanic thermal anomaly in open Sentinel-2 imagery at a volcano with no corresponding Smithsonian GVP eruption record

🌍 **Earth and sky** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours (windowed COG reads of ~1,300 volcanoes; MBs per scene chip) · open as of 2026-10-15

## The problem

The Smithsonian Global Volcanism Program (GVP) Volcanoes of the World database records Holocene eruptions with dates; it is served openly through a GeoServer WFS. Sentinel-2 L2A imagery (open on AWS via the Element 84 Earth Search STAC API) detects hot surfaces (lava, domes, vents) in SWIR bands at 20 m; MIROVA (Coppola et al.) monitors many volcanoes but not all. Remote volcanoes in Melanesia, the Kurils, the Aleutians, South Sandwich and Andes can have unreported low-level activity. Open task: find thermal anomalies at a GVP Holocene volcano during a period with no GVP eruption record covering those dates.

## What counts as a win

A saved bundle (Sentinel-2 L2A scene IDs, SWIR band 11/12 chips, detection code) showing a hot-pixel cluster (normalized thermal index or B12 radiance > 5 sigma above the volcano's own clear-sky baseline) within 2 km of a GVP Holocene volcano vent in >= 3 separate clear acquisitions spanning >= 10 days; the same detector run on a null set (the same scenes at >= 300 randomly placed non-volcanic control points of similar terrain, and the volcano's own scenes with dates permuted) gives an expected false count < 0.05 for >= 3-scene detections over the searched span; not explained by wildfires, sun-glint or cloud artefacts (morphology confined to crater/vent); at dates outside every eruption interval for that volcano in the GVP WFS layer GVP-VOTW:Smithsonian_VOTW_Holocene_Eruptions (re-queried live immediately before claiming; open-ended eruptions treated as continuing); and with no GVP Weekly/Bulletin report covering that activity found by text search.

## Partial wins

- **p1:** A reproducible thermal time series that extends a GVP eruption's end date (activity persisting >= 30 days beyond the listed stop date) in >= 3 clear scenes.
- **p2:** A first satellite thermal detection at a volcano whose GVP record has no eruption in the last 50 years, even if later found reported by a local observatory.
- **p3:** A reproducible global screening over all GVP Holocene volcanoes for one year with a documented false-positive rate.

## How a win is checked

Skeptic queries the STAC API for the listed scene IDs, downloads SWIR cloud-optimized GeoTIFF windows (MB), recomputes the thermal index and baseline, overlays the vent location, and re-queries the GVP WFS. Under an hour.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows?service=WFS&request=GetCapabilities>

## Sources

- <https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows?service=WFS&request=GetCapabilities>
- <https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a>
- <https://www.mirovaweb.it/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: per-volcano time series of a SWIR hot-pixel index (e.g. Massimetti et al. 2020 NHI) over 2017-2026 with volcano-specific baselines.
- Prioritise volcanoes absent from MIROVA's monitored list and remote island arcs with little ground observation.
- Cross-domain import (manufacturing quality control): Shewhart/EWMA control charts per volcano flag sustained deviation rather than single hot pixels.
- Cross-domain import (astronomy): treat each acquisition like an image in a transient survey - reference stack, difference, PSF-matched detection - to suppress static bright rock.
- Cross-domain import (ecology occupancy models): model detection probability under cloud cover to estimate true activity periods from patchy observations.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Wildfires and agricultural burning near volcano flanks look identical in SWIR; require vent confinement.
- Sun-glint off crater lakes and bright fumarole-free rock in high-sun scenes produce false hot pixels; use night or low-glint tests and baseline per season.
- GVP records may lag but local observatories (e.g. PHIVOLCS, KVERT, SERNAGEOMIN) may have reported it; the novelty claim is relative to GVP only and must say so.
- GVP eruption dates can be uncertain ('continuing'); treat open-ended eruptions as covering the present.
- The GVP website pages may block scripts; use only the WFS service and do not contact GVP.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/earth-and-sky/volcano-thermal-unrest-not-in-gvp.md
```

Already set up? Say `run V3R1T4S on volcano-thermal-unrest-not-in-gvp`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `volcano-thermal-unrest-not-in-gvp`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
