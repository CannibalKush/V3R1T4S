# JARVIS-Leaderboard small-data materials properties (exfoliation energy, superconducting Tc): beat the best listed test MAE

⚛️ **Physics** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Two small JARVIS-DFT property tasks on the JARVIS-Leaderboard (Kamal Choudhary et al., NIST) are realistic on a CPU: dft_3d_exfoliation_energy (812 layered materials, fixed 650/81/81 train/val/test split; best listed test MAE 40.887 meV/atom, matminer_xgboost, University of Toronto, May 2023) and dft_3d_Tc_supercon (electron-phonon superconducting transition temperatures from the JARVIS BCS workflow; best listed test MAE 1.5187 K, AtomGPT, May 2024). Structures and splits are public in the GitHub repository. Both tasks have few submissions and no entries since 2024. Checked live 2026-10-15: both pages HTTP 200.

## What counts as a win

Success means a trained model, training script and predictions file for dft_3d_exfoliation_energy or dft_3d_Tc_supercon such that the test MAE, recomputed by the checker on the official test ids of the benchmark json, is STRICTLY LOWER (direction: min) than the best MAE on that task's live leaderboard page re-fetched immediately before claiming, by at least 5% relative AND by more than the half-width of a 1000-sample bootstrap 90% confidence interval of the claimed model's MAE; AND the model was trained only on train (and val) ids with no external data containing the test materials' labels; AND re-running the saved model reproduces the predictions file.

## Partial wins

- **p1:** The same rules on one further small JARVIS AI single-property task with fewer than 2000 materials and at least three listed entries (for example dft_3d_max_efg or dft_3d_dfpt_piezo_max_dij), named before the run starts.
- **p2:** A 5-fold cross-validation study on the union of train and val showing the claimed model's advantage over a reproduced matminer_xgboost (or AtomGPT) baseline with a paired test, published with the predictions.

## How a win is checked

Checker (< 15 min): download the benchmark json.zip from jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/; load the claimed model; predict the test ids from the JARVIS-DFT structures (jarvis-tools dft_3d dataset); compute MAE and bootstrap interval; compare with the live page; inspect the training script for test-id use.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy/>

## Sources

- <https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy/>
- <https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_Tc_supercon/>
- <https://github.com/usnistgov/jarvis_leaderboard>
- <https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy.json.zip>
- <https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/dft_3d_Tc_supercon.json.zip>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Physics features for exfoliation: interlayer distance, layer-normal vdW contact area, layer charge transfer and a dispersion-only (D3-like) interlayer energy computed directly from the structure, fed to gradient boosting; exfoliation energy is largely a vdW-contact quantity.
- Superconductivity priors (McMillan / Allen-Dynes): predict lambda and omega_log-like proxies (light-element content, Debye-temperature estimates from a universal potential's phonons) and map them through the Allen-Dynes formula, learning only the residual.
- Transfer from universal potentials: use frozen MACE-MP or CHGNet embeddings as descriptors for a small kernel ridge or boosted-tree head (pretraining labels are energies/forces, not exfoliation energies or Tc, but confirm no Tc labels leak).
- Small-data statistics: nested cross-validation for hyperparameters, monotone constraints, and ensembles; the 81-structure exfoliation test set punishes overfitting.
- Geometry import from topology/crystallography: dimensionality and layer-identification algorithms (lattice-graph connected components) to compute per-layer descriptors robustly.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Test sets are tiny (81 materials for exfoliation); a 2-3% MAE gain is noise. The bootstrap margin is mandatory.
- Test labels are public in the repository and in JARVIS-DFT; any use of them, or of models pretrained on JARVIS property labels (for example AtomGPT checkpoints trained on full JARVIS-DFT), is leakage.
- Some leaderboard rows are mislabeled or duplicated (rows named after other tasks appear on some pages); compare with the best genuine row for the exact task and note anomalies rather than treating them as the bar.
- Units: exfoliation energy in meV/atom, Tc in K; per-formula-unit or eV values give fake improvements.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/jarvis-small-data-exfoliation-tc-mae.md
```

Already set up? Say `run V3R1T4S on jarvis-small-data-exfoliation-tc-mae`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `jarvis-small-data-exfoliation-tc-mae`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
