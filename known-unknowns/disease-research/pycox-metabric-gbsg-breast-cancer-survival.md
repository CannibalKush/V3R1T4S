# Breast-cancer prognosis benchmark: beat the published time-dependent concordance on METABRIC and Rotterdam/GBSG

🧬 **Disease research** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-minutes · open as of 2026-10-15

## The problem

Two small, fully public breast-cancer cohorts - METABRIC (1,904 patients, gene-expression-derived and clinical covariates) and the Rotterdam tumour bank plus German Breast Cancer Study Group set (GBSG) - have become the standard benchmark for survival models, and Havard Kvamme, Ornulf Borgan and Ida Scheel fixed a careful public scoreboard for them (Journal of Machine Learning Research 20(129), 2019). Their Table 2 reports the time-dependent concordance (C_td, Antolini) averaged over five cross-validation folds: on METABRIC, DeepHit 0.675, Cox-Time 0.662, RSF (C_td) 0.652, RSF (Mortality) 0.649, Cox-MLP (CC) 0.643, Cox-MLP (DeepSurv) 0.636 and classical linear Cox 0.628; on Rotterdam/GBSG, Cox-Time 0.677, Cox-MLP (DeepSurv) 0.674, DeepHit 0.670, Cox-MLP (CC) 0.669, classical Cox 0.666. Table 3 reports the censoring-weighted integrated Brier score, where the ordering changes and DeepHit's discriminative win turns into the worst calibration (METABRIC 0.184 versus Cox-Time 0.172). The datasets ship with the pycox package and download without registration; a full five-fold comparison of several model families takes minutes on a laptop CPU. The frontier is narrow - six years of neural survival models have moved METABRIC C_td by under 0.05 over a linear Cox model - and the discrimination-versus-calibration trade-off in the two tables is still unresolved, which is precisely the kind of small, literal, reproducible bar a stranger can check.

## What counts as a win

Success means, for one named dataset (metabric or gbsg as distributed by pycox, file sha256 logged), a saved per-fold risk or survival-function output under a five-fold cross-validation with the published protocol (hyperparameters selected per fold on a held-out validation subset of the training folds only), such that EITHER (a) the time-dependent concordance C_td, computed with pycox's own EvalSurv implementation, exceeds the maximum value in that dataset's column of Table 2 of https://www.jmlr.org/papers/volume20/18-424/18-424.pdf - re-fetched and re-read immediately before claiming - by at least 0.015 absolute, with the gain surviving 10 repetitions of the five-fold protocol (mean +/- std) and exceeding 2x that std; OR (b) the censoring-weighted integrated Brier score is lower than the minimum in that dataset's column of Table 3 by at least 0.005 absolute under the same repetition requirement, while C_td is not worse than the published best by more than 0.01. The attacker must include same-environment, same-fold re-runs of classical Cox, DeepHit and Cox-Time and must beat both the re-run and the published values. Deliverables: dataset sha256, fold assignments, training code, per-fold predictions, and verbatim EvalSurv output for every model.

## Partial wins

- **p1:** Achieve the published best C_td on METABRIC (0.675) to within 0.005 while improving the integrated Brier score below 0.172, i.e. resolve the discrimination-calibration trade-off that the two published tables expose, with 10 repetitions.
- **p2:** Beat the classical linear Cox C_td by >= 0.03 on BOTH METABRIC and Rotterdam/GBSG with one frozen method and one tuning protocol, reported with all four published metrics, which no published neural method does on both cohorts simultaneously.
- **p3:** A variance-of-record result: run the published protocol 10 times with different fold seeds for classical Cox, Cox-Time and DeepHit, and report the seed-to-seed spread of C_td on each dataset. If the spread exceeds the gaps between published methods, say so plainly - that is a finding about the benchmark, not a win.

## How a win is checked

Skeptic installs pinned pycox in a clean virtual environment, loads the dataset through the package and compares sha256 with the attacker's manifest, verifies that the fold assignment covers every patient exactly once and that no patient's outcome entered feature preprocessing, recomputes C_td and the integrated Brier score from the attacker's saved survival predictions with EvalSurv (seconds), and re-runs the attacker's training plus the three reference models end to end (laptop-minutes). The live record is read by downloading the JMLR PDF and reading Tables 2 and 3. Leakage audit: standardisation and any entity embeddings fitted on training folds only; no hyperparameter chosen using the test fold; the time grid for the Brier score identical to the published convention.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.jmlr.org/papers/volume20/18-424/18-424.pdf>

## Sources

- <https://www.jmlr.org/papers/volume20/18-424/18-424.pdf>
- <https://www.jmlr.org/papers/v20/18-424.html>
- <https://github.com/havakv/pycox>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: discrete-time survival with a flexible baseline hazard and proper calibration terms, trained with a loss that mixes a ranking term and a likelihood term, which directly targets the two metrics the tables report.
- Conventional: aggressive regularisation and ensembling - these cohorts have fewer than 2,000 patients and a handful of covariates, so variance, not model capacity, is the limiting factor; bagged classical models with monotone spline effects are a serious contender.
- Cross-domain import (reliability engineering): accelerated failure time and Weibull mixture models with covariate-dependent shape are the default in equipment-failure analysis and are rarely included in these machine-learning comparisons, yet they handle non-proportional hazards natively.
- Cross-domain import (actuarial science / mortality tables): borrow Lee-Carter style factor models for hazard curves, where the time profile is shared and individuals load on it, which is exactly the structure these small cohorts can estimate well.
- Cross-domain import (information theory / proper scoring rules): optimise and report strictly proper scores (integrated Brier, right-censored log-likelihood) and treat concordance as a secondary read-out; the published tables show the two disagree, and the field's habit of tuning on concordance is likely why calibration is poor.
- Cross-domain import (survey statistics / inverse-probability weighting): model the censoring distribution explicitly and use doubly robust estimation of the survival curve, which protects against the censoring-model misspecification that the integrated Brier score silently depends on.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Preprocessing on the full dataset (standardisation, imputation, feature selection, discretisation of the time grid) leaks test-fold information; with gaps between published methods under 0.05 C_td, this alone can fabricate a record.
- Metric confusion: Harrell's C-index, Uno's C-index and Antolini's time-dependent C_td give different values; the published bar is C_td as implemented in pycox, and the Brier score is censoring-weighted over a specific time grid.
- Tiny cohorts, large variance: METABRIC has 1,904 patients and GBSG 2,232; single-run five-fold estimates move by more than 0.01 between seeds, so repetitions and a 2x-std margin are mandatory.
- Dataset-version drift: several METABRIC and GBSG variants circulate with different covariate sets and different censoring; only the pycox-distributed versions used in the paper are comparable, and the sha256 must be logged.
- Benchmark staleness and novelty: these datasets are heavily used, so the NOVELTY check must search recent literature for higher published C_td on the same pycox splits before any claim.
- Over-claiming: these are retrospective cohorts assembled decades ago under treatment practices that no longer apply; a better concordance is a methods result, not a prognostic tool, and must never be presented as individual risk prediction.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/pycox-metabric-gbsg-breast-cancer-survival.md
```

Already set up? Say `run V3R1T4S on pycox-metabric-gbsg-breast-cancer-survival`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `pycox-metabric-gbsg-breast-cancer-survival`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
