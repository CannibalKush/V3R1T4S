# 🔭 Sky archives

New vetted candidates in public astronomy archives (never 'a planet', only 'a candidate').

**7 open problems**, easiest first. Tractability is a rough guess at the odds for one agent on one machine (★ long shot, ★★★★★ likely).

| Odds | Problem | Kind | Compute |
|---|---|---|---|
| ★★★★☆ | [New periodic variable stars / eclipsing binaries absent from VSX, confirmed in two indepe…](new-periodic-variables-not-in-vsx.md) | harvest | laptop-hours (ZTF light curves are fetched per cone query, a few hundred KB each; TESScut 5x5-pixel cutouts are ~1 MB per sector; the CDS vsx.dat dump is 2.2 GB; Gaia and Chen+2020 catalogs are queried, not downloaded in full) |
| ★★★☆☆ | [New vetted transit candidate in archival Kepler or K2 light curves (not in KOI/K2 candida…](kepler-k2-new-vetted-transit-candidate.md) | harvest | laptop-hours (do NOT fetch the full Kepler or K2 light-curve sets; restrict to a defined sub-sample under 200 GB, e.g. one K2 campaign (~20k targets, ~10 GB) or Kepler M dwarfs; pip install lightkurve transitleastsquares wotan triceratops astroquery) |
| ★★★☆☆ | [New vetted transiting-planet candidate in public TESS light curves (not in TOI/CTOI/Archi…](tess-new-vetted-transit-candidate.md) | harvest | laptop-hours (one sector of 2-min SPOC light curves is ~20,000 files / ~40 GB; keep any sub-sample under 200 GB, e.g. Tmag < 12 M dwarfs or a single sector; pip install lightkurve transitleastsquares wotan triceratops astroquery into a virtual environment first) |
| ★★★☆☆ | [Precovery of known asteroids in public ZTF / Pan-STARRS / DECam images, extending the obs…](asteroid-precovery-arc-extension.md) | harvest | laptop-hours (cutouts are ~1-10 MB each; orbit propagation is seconds; the limiting step is choosing objects whose back-propagated positions fall in archive coverage; MPCORB.DAT is 319 MB, NEA.txt is small) |
| ★★☆☆☆ | [New single-/duo-transit long-period candidate in Kepler or TESS light curves](kepler-tess-single-transit-long-period-candidate.md) | harvest | laptop-hours (single-event search is cheap; the cost is downloading: use the tesscurl sector scripts for a defined bright sub-sample or Kepler PDCSAP for Teff < 6000 K dwarfs, well under 200 GB) |
| ★★☆☆☆ | [New circumbinary transit candidate in a Kepler eclipsing binary (Villanova EB catalog)](kepler-eb-circumbinary-transit-candidate.md) | standard | laptop-hours to laptop-days (2878 EB light curves ~ 1.5 GB; the N-body stacking search is CPU-heavy, so restrict to detached EBs with morph < 0.5 and P_bin 5-60 d, ~ 700 systems) |
| ★☆☆☆☆ | [MOONSHOT - Planet Nine or a new extreme distant TNO candidate in public archival survey i…](planet-nine-distant-tno-archival-moonshot.md) | moonshot | laptop-hours to laptop-days (DECam frames are ~0.5-1 GB each; restrict to < 200 GB by selecting fields with >= 3 public epochs in the predicted Planet Nine region or ecliptic-latitude bands; shift-and-stack on 10 cores is feasible for a few square degrees per day) |

← [All categories](../README.md)
