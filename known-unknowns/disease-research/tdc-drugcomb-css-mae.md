# TDC DrugComb_CSS: lower the leaderboard MAE for drug-combination sensitivity in cancer cell lines

🧬 **Disease research** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Therapeutics Data Commons hosts the DrugCombo benchmark group, built on the DrugComb dataset of drug-pair screens in cancer cell lines. The main endpoint, TDC.DrugComb_CSS, is the drug-combination sensitivity score (derived from relative IC50 values and areas under dose-response curves) for a (drug A, drug B, cell line) triple. TDC fixes the split: 20% of the data held out by the 'drug combination' split, with a train_val set released and a frozen test set released with labels but with a prescribed evaluation protocol (five independent runs, mean +/- std of MAE via group.evaluate_many). As of 2026-10-13 the public leaderboard has exactly ONE entry: an MLP (7,141,297 parameters, contributed by Yusuf Roohani) at MAE 16.858 +/- 0.005, plus a tissue-stratified table (Kidney 14.570, Lung 15.653, Breast 13.432, Hema 28.764, Prostate 15.692, Ovary 15.263, Skin 15.663, Brain 15.694, Colon 17.729). A single shallow baseline occupying a leaderboard for a tabular regression task with ~300k rows and strong cell-line/drug main effects looks like a soft frontier: gradient-boosted trees on Morgan fingerprints plus cell-line omics, or a factorization/mean-effects decomposition, routinely beat generic MLPs on this data shape. Nothing in the task needs a GPU: the data are a few hundred MB and CPU-only training is laptop-hours. Direct measurement on the downloaded benchmark files (2026-10-15) shows how soft: a constant train_val-median predictor scores MAE 16.864, level with the MLP, and a per-cell-line median scores 15.649, beating it by 1.21 without learning anything about drugs. The open question is therefore whether any model beats the per-cell-line median by a convincing margin.

## What counts as a win

Success means a saved prediction vector for the TDC drugcomb_css test set obtained exactly as the TDC protocol prescribes (five seeds via group.get_train_valid_split(benchmark='drugcomb_css', split_type='default', seed=s) for s in [1,2,3,4,5], evaluated with group.evaluate_many) whose mean MAE is STRICTLY LOWER (direction: min) than ALL THREE of: (a) the best MAE on the live leaderboard https://tdcommons.ai/benchmark/drugcombo_group/drugcomb_css/, re-fetched immediately before claiming, by at least 1.0 MAE absolute; (b) a constant predictor set to the median of train_val Y (measured at 16.864 on 2026-10-15), by at least 1.0; and (c) a per-cell-line median predictor fitted on train_val only (measured at 15.649 on 2026-10-15), by at least 0.30 MAE absolute and at least 3x the claimed model's reported std. Both trivial baselines must be re-fitted and re-scored by the attacker in the same run and their values printed verbatim. The claim must ship: (a) the exact tdc package version and the sha256 of the downloaded benchmark files, (b) the five per-seed prediction vectors, (c) the training script, (d) the raw group.evaluate_many output printed verbatim. No test-set label may enter training, validation, early stopping, hyperparameter selection, feature construction or any normalisation statistic; a single use of the test labels for any purpose other than the final evaluate call voids the claim. If TDC's leaderboard gains new entries before the claim, the live best value is the bar.

## Partial wins

- **p1:** Beat BOTH the leaderboard MAE and the per-cell-line median baseline on at least 4 of the 9 tissue-stratified CSS columns, each by >= 0.30 MAE, under the five-seed protocol.
- **p2:** A benchmark-critique result of record: show with verbatim group.evaluate_many output that the current leaderboard entry is matched by a constant predictor (median of train_val) and beaten by a per-cell-line median, and quantify the symmetry leakage (as of 2026-10-15: 2,321 of 59,708 test triples occur in train_val with the drug order reversed). Reported as a critique, not a modelling win.
- **p3:** Beat the Hema column (leaderboard 28.764) by >= 1.0 MAE while beating the per-cell-line median baseline on every other tissue column.

## How a win is checked

Skeptic installs the pinned tdc version in a clean venv, downloads the benchmark (sha256 of data files compared against the attacker's manifest), loads benchmark = group.get('Drugcomb_CSS'), confirms the attacker's prediction vectors have exactly the test-set length and row order, re-runs group.evaluate_many on the five supplied prediction dicts (minutes), and re-fetches the leaderboard page to read the live best MAE. Then the skeptic re-trains the attacker's script end-to-end from the train_val split on a fresh seed set (laptop-hours) and confirms the MAE is in the same range. Leakage check: grep the training code and any cached artefacts for any read of the test split, and confirm feature-scaling statistics are computed on training rows only.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://tdcommons.ai/benchmark/drugcombo_group/drugcomb_css/>

## Sources

- <https://tdcommons.ai/benchmark/drugcombo_group/drugcomb_css/>
- <https://tdcommons.ai/benchmark/drugcombo_group/overview/>
- <https://tdcommons.ai/benchmark/overview/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: gradient-boosted trees (LightGBM/XGBoost/CatBoost) on concatenated Morgan/ECFP fingerprints plus physicochemical descriptors for both drugs, plus cell-line expression PCs, with symmetric augmentation (swap drug A/B so the model learns the permutation invariance the MLP has to memorise).
- Conventional: explicit mean-effects baseline (global + drug-pair + cell-line + tissue effects) fitted by ridge/ALS, then a learned residual model; this is the single most common reason tabular leaderboards fall, because generic MLPs waste capacity re-learning main effects.
- Cross-domain import (coding theory / compressed sensing): treat the drug-pair x cell-line response matrix as a partially observed low-rank tensor and recover it with a syndrome-decoding-style alternating minimisation under an L1/nuclear-norm penalty; combination screens are massively incomplete, and matrix/tensor completion with side information (fingerprints as row/column codes) exploits exactly the redundancy an MLP ignores.
- Cross-domain import (statistical physics / ecology): model CSS as a pairwise-interaction (Ising / Lotka-Volterra style) energy over drug-target perturbation vectors, fitting per-target fields and pair couplings with a mean-field or TAP approximation; this gives a physically parameterised interaction term with far fewer free parameters than 7M, which is exactly what small-sample tissue strata (Prostate: 2 cell lines) need.
- Cross-domain import (signal processing): dose-response curves are smooth monotone signals; fit a shape-constrained (isotonic / monotone-spline) representation of the per-drug curves and feed the curve coefficients as features instead of scalar summaries, so the model sees the whole response spectrum rather than one summary statistic.
- Ensembling and hyperparameter search under the five-seed protocol: because the protocol averages five runs, variance reduction alone (bagging, seed averaging, snapshot ensembling) buys measurable MAE; check how much of the gap is pure variance before building anything clever.
- Target the loss: MAE is the metric, so train with L1/Huber or quantile (median) objectives rather than MSE, and calibrate predictions to the conditional median per tissue.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The single leaderboard entry performs at the level of a constant predictor (measured MAE 16.864 for the train_val median versus 16.858 for the MLP on 2026-10-15), so any criterion anchored only to the leaderboard is cleared by a model that has learned nothing. Trivial baselines must be re-fitted and beaten in the same run.
- Quantified symmetry leakage - 2,321/59,708 test triples appear in train_val with drugs swapped; augmenting by swapping, or deduplicating across the split boundary, trains on test rows.
- Test labels are shipped locally with the TDC benchmark files, so leakage is trivially easy and invisible: any early stopping, threshold, feature-scaling statistic, drug/cell-line embedding or hyperparameter chosen with reference to the test rows makes the number meaningless. The checker must inspect the code path, not just the output.
- Duplicate-row and near-duplicate leakage: DrugComb contains the same drug pair and cell line measured in multiple studies/doses, and the pair is symmetric (A,B) vs (B,A). If the attacker augments or deduplicates across the split boundary, train and test share rows and the MAE collapses for a fake reason. Verify that no (drug A, drug B, cell line) triple in the test set appears in training in either order.
- Protocol substitution: reporting a single-run MAE, a custom split, a different seed list, a subset of the test set, or MAE computed by the attacker's own code instead of group.evaluate_many. Only the library's own evaluation on the full TDC test set counts.
- Claiming a within-noise gain: the listed std is 0.005, so a 0.02 improvement is noise plus leaderboard staleness. Require the margins in the success criterion (>= 1.0 over the leaderboard, >= 0.30 over the per-cell-line median) and >= 3 sigma.
- Wrong endpoint: DrugComb_CSS is a sensitivity score, not a synergy score; the HSA/Loewe/Bliss/ZIP leaderboards have much smaller MAEs (4-9) and are different benchmarks. Mixing endpoints or comparing against the wrong page is a classic crank error.
- Treating the result as a therapeutic claim. This is a regression benchmark on public cell-line screens; nothing about it says anything about treating a patient and the write-up must not imply it.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/tdc-drugcomb-css-mae.md
```

Already set up? Say `run V3R1T4S on tdc-drugcomb-css-mae`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `tdc-drugcomb-css-mae`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
