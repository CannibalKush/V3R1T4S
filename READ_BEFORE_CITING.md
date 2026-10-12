# Read before citing

**V3R1T4S, 2026-10-10 (two families added 2026-10-12).** Six result families (degree-diameter graphs,
constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP counterexamples, a RobustBench attack) and
two cipher-challenge commitments. Cite the commit hash you checked, not `main`.

## Status (please read)

- **Lower bounds and computations, not breakthroughs.** Every graph, code and scheme is an explicit object that
  establishes a bound for one table cell; nothing is a claim of optimality. The five Delsarte values are classical LP
  bounds, new only as table entries. The Lehmer bound is an exhaustive search; the problem remains open. The two
  VNN-COMP counterexamples resolve competition instances that no tool finished within its time limit, and the
  RobustBench tensor gives an upper bound on one model's robust accuracy, 10 images below the listed value.
- **Not peer reviewed; no outside expert yet.** All checkers, including the ones shipped here, were written by AI
  agents. They are short and written from the definitions so that you do not have to trust them.
- **"As of" is part of every claim.** The tables change often. Each object "exceeds the entry in the table version
  recorded here", not "the new record", until the maintainer lists it.
- **Other people's work.** Almost every object builds on published work: graphs of Rajiv, Mizuno, Bhakar and
  Delorme; codes of Boisclair, Gangl, Gippini, Lysenstøen, Echols and Graham–Sloane; the LITA schemes of Khoruzhii,
  Serafin, Gelß and Pokutta; the Lehmer reductions of Lieuwens, Kishore, Cohen and Hagis; the VNN-COMP benchmark of
  Postovan and Eraşcu; the model of Addepalli, Jain and Babu, evaluated with RobustBench and AutoAttack. Per-result credits are in
  each family's README, [`TROPHY_CASE.md`](TROPHY_CASE.md) and [`LICENSING.md`](LICENSING.md). Please cite them.
- **Recorded outputs.** Host-specific fields (absolute paths, temp directories, HTTP `Server:` banners) were removed
  from shipped logs and outputs, and paths in check records are relative to this repository; no number was changed.

## Contents

| path | what |
|---|---|
| [`README.md`](README.md) | overview |
| [`TROPHY_CASE.md`](TROPHY_CASE.md) | summary by significance, then one row per claim with status, snapshot, check command and credits |
| [`READ_BEFORE_CITING.md`](READ_BEFORE_CITING.md) | this file |
| [`DONT_SPOIL_THE_HUNT.md`](DONT_SPOIL_THE_HUNT.md) | what is published for each kind of problem |
| [`LICENSING.md`](LICENSING.md) | licenses by path (`LICENSE`, `LICENSE-DATA`) and required third-party attributions |
| [`CITATION.cff`](CITATION.cff) | citation metadata |
| [`SHA256SUMS`](SHA256SUMS) | sha256 of every file tracked in git |
| [`known-knowns/`](known-knowns/) | the six result families: `biggest-graphs/`, `bigger-codes/`, `faster-matrix-multiplication/`, `lehmer-past-10-to-the-50/`, `vnncomp-2026-unsolved-instances/`, `robustbench-cifar100-stronger-attack/` |
| [`sealed-envelopes/`](sealed-envelopes/) | salted hash commitments for the two Bouchaudy cipher solves |

Each family has `README.md` (scope, comparison, credits, limitations), `RUN_IT_YOURSELF.md` (commands, expected
output), `verify-it-yourself/` (checkers, `run_checks.sh`, and `RECEIPTS.md`: their output on the shipped files),
`how-we-built-it/` (the code that generated the objects, pinned requirements, exact commands, `SMOKE.md`: a small
test run) and `HOW_WE_FOUND_IT.md` (the brief the agent was given, what failed, what worked, credits).

## How to verify

```sh
shasum -a 256 -c SHA256SUMS                    # or: sha256sum -c SHA256SUMS   (every file tracked in git)
sh known-knowns/biggest-graphs/verify-it-yourself/run_checks.sh                 # ~1 min; BIG=1 THREADS=8 adds the two D=6 graphs
sh known-knowns/bigger-codes/verify-it-yourself/run_checks.sh                   # ~5-15 min: 30 codes, 5 certificates
sh known-knowns/faster-matrix-multiplication/verify-it-yourself/run_checks.sh   # ~6-8 min: 7 scheme files, Brent equations (exact), ranks, controls
sh known-knowns/lehmer-past-10-to-the-50/verify-it-yourself/run_checks.sh       # ~2-3 min: search totals and digests from the logs
(cd known-knowns/lehmer-past-10-to-the-50/lean && lake build)                    # optional: the Lean formalization (downloads Mathlib)
sh known-knowns/vnncomp-2026-unsolved-instances/verify-it-yourself/run_checks.sh      # seconds: downloads the benchmark files (pinned commit); OFFICIAL=1 adds the competition's validator
sh known-knowns/robustbench-cifar100-stronger-attack/verify-it-yourself/run_checks.sh # ~10-20 min on CPU (N=500: ~1 min); downloads CIFAR-100 and the model weights
```
Requirements: `python3` with `numpy`, a C compiler with pthreads; for Lean, `elan`; for VNN-COMP, `onnxruntime`
(optionally `onnx`, and `vnnlib==1.0.2` for the official validator); for RobustBench, `torch`, `torchvision` and
`robustbench`. Rebuilding the
objects and comparing with today's tables: each family's `RUN_IT_YOURSELF.md`.

## Corrections

Found an error? Open an issue naming the file, the command and its output. Errors will **never be fixed silently**:
each will be recorded publicly (date, reporter, what was wrong, corrected claim) and the tables here updated, without
rewriting history. Being overtaken after the recorded snapshot is not an error, but will be recorded the same way; the
object stays as a time-stamped bound. Missing or wrong credit counts as an error. Takedown requests from setters,
maintainers and authors will be honoured promptly.

## Credits and license

By **Pliny the Liberator** ([@elder-plinius](https://github.com/elder-plinius)) with Anthropic Claude agents. The
tables of record are maintained by Francesc Comellas, Andries E. Brouwer, the fast-matrix-multiplication catalogue
maintainers (Lille digest, Perminov, MerlijnW70, matmulcatalog), Jean-François Bouchaudy, the VNN-COMP organisers and
the RobustBench maintainers. Thank you.

Code: AGPL-3.0 (`LICENSE`). Data, objects and documentation: CC BY 4.0 (`LICENSE-DATA`). The path-by-path map and the
required third-party attributions are in [`LICENSING.md`](LICENSING.md).
