# How we found it

**The task.** Several AI agents were given the same open benchmark problem: produce a saved adversarial tensor for all
10,000 CIFAR-100 test images (L∞, ε = 8/255) against one unmodified RobustBench model whose robust accuracy, recounted
independently on CPU (ties count as robust), is at least 10 images below the best published value for that model.
Each agent got a different angle; rules were to run only open-weight benchmark models locally, keep every claimed
success re-verified on CPU, and use a single GPU process on a shared Apple M5.

**Day 1 (2026-10-09): the base.** One agent's angle was "budget allocation instead of uniform runs": instead of
AutoAttack's fixed 9 targets × 100 APGD steps per image, spend the same 900 steps adaptively. It wrote a continuable
APGD and ran APGD-CE (100 steps) on all clean-correct images of `Addepalli2022Efficient_RN18`, then successive halving
over 45 (target class × loss) arms per surviving image, keeping the most promising arms. An equal-budget comparison
with plain APGD-T on 200 images came first; a sign error in the image order (easiest first instead of closest to the
boundary first) was caught and the job relaunched. The full run took about 6 hours of GPU time and finished after the
agent's shift: 2,763 robust images, 4 below RobustBench's 2,767.

**Day 2 (2026-10-10/11): first another model, then this one.** Most of the second day went into
`Rebuffi2021Fixing_R18_ddpm`, where fifteen first-order attack variants, CR Attack, warm relax/reset, homotopy,
simulated annealing and others all converged on the same handful of images and stopped one image above the honest
bar. The agents then switched to Addepalli, whose bar has no published gain over AutoAttack (CR Attack's own README
also gives 27.67 %):
- CR Attack (Pan et al., AAAI 2025; published settings) on the 771 residual images within 0.5 logits of the boundary:
  3 breaks (2,760).
- A warm-started version of CR's relax/reset schedule from the saved points: 2 breaks (2,758). Targeted variants,
  replica exchange over relaxation radii, basin hopping, a second CR draw, a restart bandit, FAB-T, a surrogate-gradient
  attack and Square from the incumbent all found nothing on the remaining band.
- The last image came from a different question: how are the end margins of many *fresh* random restarts distributed?
  64 fresh restarts each (rotating over 8 loss/start variants) on the 10 closest residuals broke none, but image 2137 came within 4e-5 logits of the
  boundary, and the best restarts clustered just below the warm incumbents (a ceiling, not a long tail). 250 restarts
  of 100 steps over the 5 best variants (25,000 forward-backward passes on that one image) then fooled it on CPU
  (+1.5e-4): 2,757, exactly 10 below.
  Further restarts on the near-tie fooled rows raised their margins (2137 to +3.7e-4) so that a different summation
  order could not flip them; an exhaustive coordinate search and 30 restarts on the next 33 residuals found nothing more.

**What did not work.** Everything aimed at the residual band beyond ~0.002 logits: every mechanism tried saturates a
few thousandths of a logit below the boundary on this model.

**Checks.** Two full CPU recounts by different checkers (2,757; clean 6,545; max perturbation exactly 8/255), a GPU
quick look, a margin-stability study of the three near-tie rows (batch layout, threads, float64, MPS), and three
independent reviewer agents (two recounts with their own code, one re-search of the literature and the live table).

**Time.** First stage started 2026-10-09T09:12Z; the published tensor was assembled 2026-10-11T20:25Z and recounted by
22:08Z. About 9 hours of GPU attack time in total (6 of them in the day-1 successive-halving run).

**Credits.** Model: Addepalli, Jain, Venkatesh Babu (NeurIPS 2022). Benchmark and loader: RobustBench (Croce et al.).
APGD/AutoAttack: Croce and Hein (ICML 2020). CR Attack: Pan, Wu, Tang, Li, Yao (AAAI 2025). Successive halving:
Karnin et al. (2013), Jamieson and Talwalkar (2016). Code and runs: several AI agents working on the same problem in parallel, sharing
intermediate tensors; verification by independent reviewer agents. Stage-by-stage code: `how-we-built-it/`.
