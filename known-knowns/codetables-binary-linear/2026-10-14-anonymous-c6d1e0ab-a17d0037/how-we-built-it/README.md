# How we built it

- `qc_search.c`: the quasi-cyclic / quasi-twisted code search, as written by the original agent run.
- `bklc_opt.c`: the exact evaluator, puncturing and extension engine from the same run.
- `PREREG.md`: the original run's pre-registration (frozen 2026-10-14T08:41:00Z, before the claim was built). It states `null_test: not needed`, because the claim is an explicit code checked by a deterministic exact checker.

Compile with any C99 compiler, as in `../RUN_IT_YOURSELF.md`. This code is shipped for transparency. The claim does not depend on it.
