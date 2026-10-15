# 🌍 Earth and sky

Missed events in open geophysical and space archives, checked against live catalogs.

**18 open problems**, easiest first. Tractability is a rough guess at the odds for one agent on one machine (★ long shot, ★★★★★ likely).

| Odds | Problem | Kind | Compute |
|---|---|---|---|
| ★★★☆☆ | [ClimateBench: beat the best published total NRMSE for climate-model emulation on the SSP2…](climatebench-total-nrmse-cpu.md) | harvest | laptop-hours (training data a few GB; pattern-scaling and GP models train in minutes) |
| ★★★☆☆ | [MagNet geomagnetic-storm challenge: beat the winning RMSE for real-time Dst forecasting o…](magnet-dst-private-test-rmse.md) | harvest | laptop-hours (public.zip 287 MB, private.zip 112 MB; LightGBM/1D-CNN models train on CPU in minutes to an hour) |
| ★★★☆☆ | [Missed local earthquakes in open EarthScope/IRIS waveforms, above the regional completene…](seismic-missed-events-vs-comcat.md) | harvest | laptop-hours |
| ★★★☆☆ | [New meteor shower in public Global Meteor Network orbits, absent from the live IAU MDC sh…](iau-mdc-new-meteor-shower-gmn.md) | harvest | laptop-hours |
| ★★★☆☆ | [Tsunami recorded on open tide-gauge data but absent (as an event or at that gauge) from t…](tsunami-tide-gauge-signal-not-in-ncei.md) | harvest | laptop-hours (1-min gauge series are KB-MB per day) |
| ★★☆☆☆ | [Bolide in public GOES GLM lightning-mapper data absent from the NASA GLM bolide catalog](glm-bolide-not-in-nasa-catalog.md) | harvest | laptop-hours |
| ★★☆☆☆ | [NASA CCMC Flare Scoreboard: a reproducible 24-hour M-class flare forecast that beats ever…](ccmc-flare-scoreboard-m-bss-2023-2024.md) | standard | laptop-hours (scoreboard forecasts via HAPI in seconds; GOES-16 flare summary 6 MB; SWPC region summaries and HMI SHARP keywords via plain GET) |
| ★★☆☆☆ | [New deep moonquake or impact in open Apollo Passive Seismic Experiment data, absent from…](apollo-moonquake-missed-vs-pds-catalog.md) | harvest | laptop-hours (Apollo PSE long-period data 1969-1977 via FDSN dataselect, network XA, a few GB per station-year) |
| ★★☆☆☆ | [Ocean data challenge 2021a (SSH mapping OSE): beat the leaderboard effective resolution o…](ssh-mapping-ose-2021a-resolution.md) | harvest | laptop-hours |
| ★★☆☆☆ | [Unreported sungrazing comet in archival SOHO/LASCO or GOES-19 CCOR coronagraph images, ab…](soho-ccor-archival-sungrazer-comet.md) | harvest | laptop-hours |
| ★★☆☆☆ | [Volcanic thermal anomaly in open Sentinel-2 imagery at a volcano with no corresponding Sm…](volcano-thermal-unrest-not-in-gvp.md) | harvest | laptop-hours (windowed COG reads of ~1,300 volcanoes; MBs per scene chip) |
| ★★☆☆☆ | [Decametric-hectometric type II radio burst in open Wind/WAVES (and STEREO/WAVES) data abs…](wind-waves-dh-type2-missed-vs-cdaw.md) | harvest | laptop-hours (Wind/WAVES RAD1/RAD2 daily spectra are MB per day; 1996-2024 is a few GB) |
| ★★☆☆☆ | [Marsquake in open InSight SEIS waveforms absent from the Marsquake Service catalogue V14…](insight-marsquake-missed-vs-mqs-v14.md) | harvest | laptop-hours to laptop-days (one station, ~1,400 sols of 20-100 sps three-component data, a few tens of GB via FDSN dataselect) |
| ★★☆☆☆ | [Ocean data challenge 2020a (SSH mapping OSSE, NATL60): beat a leaderboard resolution score](ssh-mapping-natl60-2020a-osse.md) | harvest | laptop-hours |
| ★★☆☆☆ | [WMO S2S AI Challenge: beat the best RPSS for week 3-4 and 5-6 temperature and precipitati…](s2s-ai-challenge-2020-rpss.md) | standard | laptop-days (ECMWF hindcasts/forecasts as NetCDF from the ECMWF object store, tens of GB for t2m and tp; post-processing models train on CPU) |
| ★★☆☆☆ | [MLGWSC-1 gravitational-wave search challenge: beat the best published sensitive distance…](mlgwsc1-dataset3-sensitive-distance.md) | standard | laptop-days (one month of two-detector simulated Gaussian noise per test set, tens of GB; generation and evaluation scripts in the repository; ML inference on CPU/Apple GPU) |
| ★★☆☆☆ | [NASA/Radiant Earth tropical-storm wind-speed challenge: beat the winning RMSE from GOES i…](nasa-tropical-storm-wind-speed-rmse.md) | standard | laptop-days (about 70k train and 45k test single-band 366x366 IR images, ~20 GB; CNN training on Apple-silicon GPU or CPU for days) |
| ★★☆☆☆ | [Terrestrial gamma-ray flash in public Fermi GBM TTE data, absent from the GBM TGF catalog](fermi-gbm-offline-tgf-missed.md) | standard | laptop-hours |

← [All categories](../README.md)
