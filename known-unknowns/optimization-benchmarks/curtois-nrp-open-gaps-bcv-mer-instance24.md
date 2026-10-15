# Nurse rostering benchmark (Curtois / schedulingbenchmarks.org): close an open gap on BCV-3.46.1, MER or Instance24

🚚 **Optimization benchmarks** · standard · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Tim Curtois maintains the main public nurse-rostering benchmark collection at schedulingbenchmarks.org, with verified best solutions and lower bounds for real hospital rostering instances (ANROM/BCV from Greet Vanden Berghe's thesis, Montreal hospital instances MER/CHILD/ERRVH/ERMGH, ORTEC, QMC, and the synthetic Instances 1-24 of Curtois and Qu). Almost every instance is now closed (best = lower bound). As of 2026-10-15 the lower-bounds page shows three remaining gaps on downloadable instances: BCV-3.46.1 (best 3277 by Alfonso Gippini Requeijo, Team Banzai, 22 Aug 2026, CP-based LNS; lower bound 2239, also Gippini Requeijo, dated 15 Oct 2026), MER (best 7080, Gippini Requeijo, 17 Aug 2026, from the previous 7081; lower bound 7079 by column generation, 2010) and Instance24 (best 40439, lower bound 40438; 52 weeks, 150 employees, 32 shift types). The 2026 activity shows the table is live.

## What counts as a win

For one of BCV-3.46.1, MER or Instance24 (or another instance that the live pages show with best solution > lower bound), a roster file that RosterViewer (or the organisers' verification) confirms as feasible for the hard constraints with total penalty STRICTLY LOWER (direction: min) than the best known solution listed on https://www.schedulingbenchmarks.org/nrp/bounds.html (and, for Instance24, https://www.schedulingbenchmarks.org/nrp/), re-fetched live immediately before claiming. A new lower bound counts only as a partial win and only with a released, re-runnable model and solver log.

## Partial wins

- **p1:** MER: a feasible roster of penalty 7079 (which would equal the lower bound and close the instance), or a released proof that 7080 is optimal (an exact model run with log showing the bound 7080).
- **p2:** Instance24: a feasible roster of penalty 40438 (closing the instance), checked with an independent re-implementation of the published Instances 1-24 objective that reproduces 40439 on the published best solution.
- **p3:** BCV-3.46.1: any strictly better roster than 3277, or a lower bound above 2239 with released model and log; the gap of over 1000 penalty points is the largest open one in the collection.

## How a win is checked

Skeptic loads the instance XML and the claimed roster in RosterViewer (free download from the benchmark's 'verify' page) and reads feasibility and total penalty; for Instances 1-24 also scores with an independent script written from the published format guide and checks it reproduces the listed best on the published best solution. Then re-fetches the bounds page. Minutes.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.schedulingbenchmarks.org/nrp/bounds.html>

## Sources

- <https://www.schedulingbenchmarks.org/nrp/bounds.html>
- <https://www.schedulingbenchmarks.org/nrp/>
- <https://www.schedulingbenchmarks.org/nrp/verify.html>
- <https://www.schedulingbenchmarks.org/nrp/data/BCV-3.46.1.ros>
- <https://www.schedulingbenchmarks.org/nrp/data/MER.ros>
- <https://www.schedulingbenchmarks.org/nrp/data/instances1_24.zip>
- <https://doi.org/10.5281/zenodo.23377565>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Column generation with branch-and-price on the employee-schedule formulation, starting from the published best roster as an incumbent; on MER and Instance24 the gap is a single unit, so an exact search with strong pruning may be enough.
- CP-SAT large-neighbourhood search over employee subsets and day windows (the method that produced the 2026 improvements), with neighbourhoods chosen by where the current roster pays its penalties.
- Cross-domain import (crew pairing in airlines): pairing/rotation generation with resource-constrained shortest paths, which is the same structure as generating individual nurse schedules.
- Cross-domain import (SAT and MaxSAT solving): encode the instance as weighted partial MaxSAT (as Demirovic, Musliu and Winter did for staff scheduling) and run a core-guided solver to try to certify 7079 or 40438 directly.
- For BCV-3.46.1, compute the lower bound from the LP relaxation of the column-generation master with cuts on weekend and cover patterns, and look for structure that explains the gap before trying to close it.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Objective conventions differ between instance families (weights, how history is treated at the planning-period boundary); score with RosterViewer or with a scorer validated on the published best solution, never with an unvalidated re-implementation.
- Hard constraints in some instances are modelled as very heavily weighted soft constraints; a low 'penalty' that hides a broken heavy constraint is infeasible in the intended sense.
- The bounds page is changing in 2026 (two updates in the last two months); a gap can close between your run and your claim. Re-fetch first.
- A lower bound is only as good as its model: bounds from a relaxed model that drops a constraint family are not valid for the original instance.
- Benchmark rosters are a proxy for real staffing quality; an improvement is an optimisation result, not a claim about nurse wellbeing or safety.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/optimization-benchmarks/curtois-nrp-open-gaps-bcv-mer-instance24.md
```

Already set up? Say `run V3R1T4S on curtois-nrp-open-gaps-bcv-mer-instance24`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `curtois-nrp-open-gaps-bcv-mer-instance24`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
