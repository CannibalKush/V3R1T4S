# CDC FluSight emergency-department visits: beat the FluSight-ensemble's season WIS on the newer ED-visit target

🧬 **Disease research** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

The CDC FluSight hub added a second prediction target - the weekly proportion of emergency-department visits attributed to influenza, from the National Syndromic Surveillance Program - alongside its long-running hospital-admissions target, and publishes a separate end-of-season evaluation for it (reports/'Flu_ED_Visit_Forecasts_WIS_27 May 2026.html' in github.com/cdcepi/FluSight-forecast-hub, directory fetched 2026-10-15; model-output holds every team's submissions through 2026-10-17, and target-data holds oracle-output.csv, 17 MB, plus the 89 MB time-series.csv with as-of values). The ED-visit target is young: fewer teams have tuned models for a bounded proportion with its own reporting artefacts, the series is revised, and the ensemble's lead over the baseline is correspondingly less entrenched than on admissions. The scoring rule is the open hubverse weighted interval score, so a stranger can rescore everything on a laptop.

## What counts as a win

Success means saved quantile forecasts, in the hub's submission format for the ED-visit target, covering every reference date, location and horizon of ONE completed season for which FluSight-ensemble submitted, produced by a released deterministic pipeline that at each reference date uses only data available then (the hub's as-of target data or an archived snapshot; no final revised series, no oracle-output, no other team's submissions, no parameter tuned on later weeks of that season), whose season-average WIS, computed with public hubverse scoring code against the hub's oracle-output for that season under the hub's exclusion rules, is STRICTLY LOWER (direction: min) than the FluSight-ensemble's for the same target, season, locations, horizons and reference dates as published in the hub's ED-visit evaluation report in https://github.com/cdcepi/FluSight-forecast-hub/tree/main/reports , re-fetched live immediately before claiming, by at least 3% relative AND outside a stationary-bootstrap 90% interval over reference dates. The scorer must first reproduce the ensemble's published value for that season to within 1%.

## Partial wins

- **p1:** Strictly lower season-average WIS than the FluSight-baseline AND than the median submitted model on the ED-visit target for one completed season, under the as-of discipline and the hub's scorer.
- **p2:** Beat the ensemble at horizons 2-3 weeks ahead on the ED-visit target across all locations of one completed season, reported as a horizon-restricted result.
- **p3:** A transfer result: show that a single model fitted jointly on the admissions and ED-visit targets beats the same model fitted on ED visits alone, by a margin with an interval, quantifying how much the older target's history is worth.

## How a win is checked

Skeptic clones the hub at a pinned commit, validates the attacker's files against hub-config task-ids for the ED-visit target, recomputes WIS for the attacker, the ensemble and the baseline with public hubverse code (first reproducing the published report value), bootstraps over reference dates, and audits look-ahead by rerunning the pipeline on truncated snapshots and by grepping for reads of oracle-output, of future weeks or of model-output. Under a gigabyte, CPU-only.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/cdcepi/FluSight-forecast-hub/tree/main/reports>

## Sources

- <https://github.com/cdcepi/FluSight-forecast-hub/tree/main/reports>
- <https://github.com/cdcepi/FluSight-forecast-hub>
- <https://github.com/cdcepi/FluSight-forecast-hub/tree/main/target-data>
- <https://github.com/hubverse-org>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Respect the support: the target is a bounded proportion, so logit-scale modelling with heteroscedastic, horizon-dependent spread and back-transformed quantiles avoids the crossing and tail problems that cost WIS on count-style models.
- CROSS-DOMAIN (signal processing / control): a state-space model on logit-proportion with a time-varying growth state and revisions treated as observation noise produces calibrated intervals without hand-tuned spread.
- CROSS-DOMAIN (econometrics of mixed-frequency data): ED visits lead admissions, so a leading-indicator regression (MIDAS-style) exploits the two targets' different timing instead of modelling each in isolation.
- CROSS-DOMAIN (ecology / nonlinear dynamics): analogue forecasting across jurisdictions as replicate trajectories handles season-shape variation that parametric curves miss, especially at turning points.
- Backfill first: the most recent weeks of NSSP proportions are revised, so an explicit revision model for the last two weeks is probably the largest single WIS gain.
- Hierarchical pooling across jurisdictions and the two targets, with shrinkage of growth-rate volatility toward a national mean - the ensemble averages models, not information.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Look-ahead through revisions: the ED-visit series is revised after first report; fitting on the final series while claiming a retrospective forecast is the classic false positive here.
- Target confusion: the hub scores two targets with different units and different reports; comparing against the hospital-admissions ensemble value, or mixing the targets' rows, invalidates the claim.
- Mismatched task sets: the ensemble's published score covers specific locations, horizons and dates with exclusion rules; dropping low-volume jurisdictions is the commonest fake win.
- Hindsight tuning: choosing the transform, window or spread multiplier after seeing the season's scores must be excluded by freezing parameters on earlier seasons with commit evidence.
- Ensemble contamination: consuming other teams' submissions for the scored season makes the result a combination, not a forecast.
- A WIS improvement is a forecasting-method result and is not public-health guidance.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/flusight-ed-visits-beat-ensemble-wis.md
```

Already set up? Say `run V3R1T4S on flusight-ed-visits-beat-ensemble-wis`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `flusight-ed-visits-beat-ensemble-wis`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
