# Integrated Healthcare Timetabling (IHTC-2024): lower the best known cost of a public (i01-i30) or competition (m01-m30) hospital instance

🚚 **Optimization benchmarks** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

The Integrated Healthcare Timetabling Problem (IHTP) combines three hospital decisions in one model: surgical case planning (which patients are admitted on which day and to which operating theatre and surgeon), patient-to-room assignment, and nurse-to-room assignment per shift, with hard constraints (room capacity, gender mixing, surgeon and theatre time, mandatory admissions) and weighted soft costs (delays, unscheduled optional patients, skill and continuity-of-care penalties, open theatres). It was posed as the Integrated Healthcare Timetabling Competition 2024 by Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf and Eugenia Zanazzo (University of Udine) with Pieter Smet and Greet Vanden Berghe (KU Leuven). The organisers maintain a post-competition upper-bound table at ihtc2024.github.io/ihtp/ for 30 public instances (i01-i30) and 30 competition instances (m01-m30), each with a downloadable JSON solution and an official C++ validator. As of 2026-10-15 the table lists, for example, i01 3842, i10 20705, i28 75172 and m01 3380, m26 69730. The table has already moved after the competition (for example m01 3380 and m04 3318 are below the best competition-round costs 3384 and 3345 by SDU), so the bounds are live but not saturated; no instance is listed as proven optimal.

## What counts as a win

A solution JSON for one instance from ihtc2024_competition_instances.zip (i01-i30) or ihtc2024_final_instances.zip (m01-m30) that the official IHTP_Validator.cc (compiled from the organisers' repository) reports with ZERO hard-constraint violations and a total cost STRICTLY LOWER (direction: min) than the cost listed for that instance on https://ihtc2024.github.io/ihtp/index.html, re-fetched live immediately before claiming, and lower than any value for that instance found by the NOVELTY check in the 2025-2026 special issue on the IHTP (Operations Research, Data Analytics and Logistics) and other papers. Any strict improvement counts; ties do not.

## Partial wins

- **p1:** Strictly improve the listed upper bound on any one of the 60 instances, validated with zero violations.
- **p2:** Strictly improve the listed bounds on 5 or more instances with a single published method and fixed settings (one seed per instance, wall-clock budget stated), which shows a method rather than a lucky run.
- **p3:** A certified lower bound (for example from a MIP or Lagrangian relaxation whose model file and solver log are released) for one of the i-instances that shows the listed upper bound is within 1% of optimal, or a feasible improvement that proves the gap is larger than assumed.

## How a win is checked

Skeptic downloads the instance archive and the official validator source from the organisers' GitHub repository, compiles it with g++ and nlohmann/json, runs ./IHTP_Validator instance.json solution.json, and reads the reported violations (must be 0) and total cost. Then re-fetches the upper-bound table and compares. Seconds per instance. Also re-runs the published listed solution through the same validator to confirm the validator build reproduces the listed cost.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://ihtc2024.github.io/ihtp/index.html>

## Sources

- <https://ihtc2024.github.io/ihtp/index.html>
- <https://ihtc2024.github.io/>
- <https://ihtc2024.github.io/assets/files/ihtc2024_competition_instances.zip>
- <https://ihtc2024.github.io/assets/files/ihtc2024_final_instances.zip>
- <https://github.com/ihtc2024/ihtc2024.github.io/blob/main/assets/files/IHTP_Validator.cc>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Start from the published best solution JSON and run a large-neighbourhood search that destroys one day, one theatre or one ward at a time and repairs it exactly with a small CP-SAT or MIP model; the published solutions are the obvious warm start.
- Decompose by subproblem: fix the admission/theatre schedule and solve room assignment and nurse assignment exactly (both are near-assignment problems), then iterate; the competition overview paper identifies the coupling costs that make this fail naively.
- Cross-domain import (VLSI placement / simulated annealing with adaptive move mix): tune the probability of each move type online by its recent acceptance gain, as placement annealers do.
- Cross-domain import (vehicle routing, ruin-and-recreate): SISR-style string removal applied to consecutive days of a patient's stay rather than to customers on a route.
- Cross-domain import (statistical physics, parallel tempering): run replicas at several temperatures and swap, which is cheap on 10 laptop cores and resists the deep local minima typical of nurse-continuity penalties.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Validator mismatch: costs computed by your own evaluator are not claims. Only the official IHTP_Validator output counts, and it must report zero violations.
- Stale table: the page is updated by email submissions; a value that beats a cached copy may already be beaten. Re-fetch immediately before claiming and check the special-issue papers.
- Wrong instance file: the public i-instances, the hidden m-instances, the 9 small instances with known optima and the 24 longer-horizon instances are different sets; compare only against the same file.
- Competition-time rules (time limits, single run) do not apply to the upper-bound table; do not claim a competition-style result from an unlimited run, or the reverse.
- This is an operations benchmark built from realistic but synthetic hospital data; a better schedule here is not evidence of better patient outcomes.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/optimization-benchmarks/ihtp-ihtc2024-upper-bounds.md
```

Already set up? Say `run V3R1T4S on ihtp-ihtc2024-upper-bounds`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ihtp-ihtc2024-upper-bounds`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
