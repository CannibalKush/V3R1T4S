# Random Promoter DREAM Challenge: beat the best published Pearson/Spearman score for predicting yeast expression from promoter sequence

🦠 **Biology** · standard · tractability ★★☆☆☆ · compute: laptop-days (GPU shortens training; scoring is minutes) · open as of 2026-10-15

## The problem

The Random Promoter DREAM Challenge 2022 (Rafi, de Boer and the DREAM consortium, Nature Biotechnology 2024) released 6.7 million random 80-bp yeast promoter sequences with measured expression, and a 71,103-sequence test set with designed subsets (high, low, native yeast, random, challenging, SNV pairs, motif perturbation, motif tiling). Scores are a weighted 'Pearson score' and 'Spearman score' across subsets. The test labels and the evaluation notebook are now public on Zenodo (record 10633252), together with the weights of the Prix Fixe-optimised DREAM-CNN, DREAM-RNN and DREAM-Attn models reported as improving on the individual challenge solutions (Autosome.org, BHI, Unlock_DNA) in Rafi et al. 2024, to be re-scored by the claimant rather than taken on trust. The open question is whether a better model, or a principled ensemble, beats the best released model on the official scoring.

## What counts as a win

Predictions for all sequences in the official test file whose Pearson score AND Spearman score, computed by the skeptic with the challenge's Evaluation.ipynb from Zenodo record 10633252 (re-fetched live immediately before claiming), are STRICTLY HIGHER (direction: max) than the best value reported in Rafi et al. 2024 and than the best released Prix Fixe model re-scored the same way, by at least 0.002 on each score. The model may be trained only on train.txt (and val.txt); hyperparameters and ensemble weights must be chosen without the test labels.

## Partial wins

- **p1:** Beat the best released model on the SNV subset (Pearson on predicted vs measured expression differences), the subset most relevant to variant effects, under the same rules.
- **p2:** A leakage-free ensemble of the three released Prix Fixe models (weights fitted on val.txt only) that beats each individual released model on both overall scores, with an honest note on whether this exceeds the paper's best.

## How a win is checked

Skeptic downloads test sequences, the filtered test labels and Evaluation.ipynb from Zenodo, scores the attacker's prediction file (one value per test sequence, order checked by sequence id), re-scores the released Prix Fixe weights the same way, and checks training logs show no read of the test label file. Minutes for scoring; retraining is the attacker's cost.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://zenodo.org/records/10633252>

## Sources

- <https://zenodo.org/records/10633252>
- <https://github.com/de-Boer-Lab/random-promoter-dream-challenge-2022>
- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12339383/fullTextXML>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Start from the released DREAM-CNN/RNN weights and ensemble or distil them; ensembling well-trained but architecturally different models is the cheapest gain and needs only CPU inference.
- Copy the winning idea and push it: Autosome.org recast regression as soft classification over expression bins, mirroring how the measurement was made (sorting cells into bins); model the full binning likelihood (as in MAUDE) instead of a softmax over bins.
- Cross-domain import (speech recognition): train on noisy labels with a known measurement channel; use the experiment's sort-bin noise model as a differentiable observation layer (like CTC handles alignment noise).
- Cross-domain import (physics-informed models): a thermodynamic layer where predicted expression is a Boltzmann-weighted occupancy of learned transcription-factor motifs, giving interpretable features that generalise to the native and SNV subsets.
- Use reverse-complement equivariant convolutions and test-time augmentation over strand and small flank runs.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The test labels are public on Zenodo: selecting a checkpoint or ensemble weight with them is leakage. Use val.txt only.
- The challenge weighted Pearson score uses r^2 on some subsets and differences for SNV pairs; any home-made metric will disagree. Use the official notebook only.
- Sequences must be scored with the same fixed flanks the challenge used; dropping or changing flanks silently changes inputs.
- Matching rather than beating the released models within noise is not a result; the 0.002 margin is small, so report bootstrap intervals over test sequences.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/dream-random-promoter-yeast-expression.md
```

Already set up? Say `run V3R1T4S on dream-random-promoter-yeast-expression`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `dream-random-promoter-yeast-expression`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
