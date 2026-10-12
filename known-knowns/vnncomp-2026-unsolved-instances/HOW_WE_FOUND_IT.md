# How we found it

## The brief

Several AI agents were each given the same target: produce a counterexample, checkable at zero tolerance and strictly
inside the input box, for one VNN-COMP 2026 instance that no participating verifier had resolved (127 instances in
the live `results.txt`). A preparatory pass had already downloaded the results table, the official validator and the
benchmark files, and had listed the 127 instances with notes per benchmark. For the traffic-sign networks it noted
that they contain `Sign` activations and a softmax output, so gradients vanish, and suggested integer perturbation
search that targets first-layer pre-activations close to their sign threshold. Each agent got a different angle; the
one that succeeded was asked to "enumerate unsolved 2026 instances, triage by size, attack small ones with smart search
+ exact validation". A "holds" (no counterexample) claim did not count.

## What was tried

- **Triage.** The agent noticed that the `traffic_signs_recognition_2023` networks are fully binarized (all weights
  ±1, sign activations, integer pixels 0 to 255), which explains why gradient attacks have nothing to follow. In the
  same results table one eps = 1 instance of the same network had been solved (by alpha-beta-CROWN, after 321 s), so
  eps = 1 counterexamples for this network were known to exist.
- **Exact model first.** It wrote an integer model of the smallest network (`3_30_30`) and checked it against
  onnxruntime at box centres and random points: identical logits (maximum deviation 0.0). At the centres the true class
  led the runner-up by 950 (idx 1703) and 940 (idx 178) logit units.
- **Search space with exactness built in.** Every pixel moves by d·(1 − 2^-10) (later 1 − 2^-9 with half-step offsets
  for pixels whose box is clipped at 255), d ∈ {−1, 0, +1}, so every input is strictly inside its interval, exact in
  float32, and the first-layer sign decisions are integer threshold tests.
- **CP-SAT.** The whole network becomes a constraint program: integer pixel variables, one Boolean per neuron that can
  still change sign, and the logit difference (runner-up class minus true class) as the objective. A 60-second trial run
  on idx 1703 closed the gap from −950 to −10; a 900-second run warm-started from that solution reached +10 after 73 s.
  The idx 178 run first crashed (the pixel map assumed every box had the same width, but 315 coordinates have boxes
  clipped at 255); after the fix it reached +4 after 351 s with no warm start. Both runs used 4 CPU cores on a
  heavily loaded laptop.
- **What failed or was not needed.** A parallel agent's straight-through-gradient search on the same two images stalled
  at logit gaps of −294 and −244 after about 25 minutes each. An encoding for the larger 48×48 and 64×64 traffic-sign
  networks (max-pooling, batch normalisation) was drafted but never run or validated; those 7 instances remain open.
  Other ideas on the agent's list (local search, MaxSAT, other benchmarks) were not started because the main line
  succeeded first.

## How long it took

The agent started at 17:54 (US Pacific) on 2026-10-10. The idx 1703 witness was written and validated at 18:12; the
idx 178 search finished at 18:24 and its witness was written at 18:25. The session was interrupted and resumed at
22:13, when the second witness was validated and the live table re-checked; a further re-check of the table and of the
16 published larger-radius counterexamples followed the next morning. Search compute: about 8 minutes of solver wall-clock
time on 4 cores in total.

## Checking

Each witness was checked with the agent's own checker, a checker written independently from the problem statement
before the search, and the unmodified official validator (`correct` at zero tolerance). Three independent reviewer
agents then re-downloaded everything, wrote their own checkers (own VNN-LIB parsers, exact rational input checks,
onnxruntime, onnx.reference and a NumPy forward pass) and re-parsed the live table; all confirmed both witnesses. A
second, separately briefed agent also ran the idx 1703 witness through its own checker.

## Credits

- VNN-COMP 2026 and its organisers (benchmarks, results, validator); the benchmark by Andreea Postovan and Mădălina
  Eraşcu; the competing tools alpha-beta-CROWN, PyRAT and vibecheck (see `README.md`).
- Google OR-Tools (CP-SAT solver), ONNX and onnxruntime.
- The search and witnesses: an AI agent (Claude). Verification: independent reviewer agents (Claude). The generating
  code is in [`how-we-built-it/`](how-we-built-it/README.md).
