# How the value was established

Contributor text and code; the panel audited the object, not the search.

## Method

1. Lower bound: a family of 12 distinct 3-subsets of [8] with no 3-sunflower, found by a randomized local search over
   r-subsets (the team's search code is summarised in TEAM_REPORT.md; the family is checked by two independent checkers).
2. Upper bound: `gen_cnf.py 8 3 13 out.cnf --sb alltrans` writes a CNF with one variable per
   3-subset of [8], one all-negative ternary clause per 3-sunflower (core enumeration: every core C and three pairwise
   disjoint petals outside C), and a sequential-counter encoding of "at least 13 chosen" (python-sat's CardEnc, aux variables above
   the set variables). glucose4 refuted it and wrote a DRUP proof; drat-trim (Heule and Wetzler) and the team's own forward RUP
   checker both verified the proof. The proved CNF carries lex-leader symmetry-breaking clauses (SOUNDNESS.md section 3): for every transposition of two points the chosen-set vector must be lexicographically no larger than its image. Since the sunflower clauses and the cardinality constraint are invariant under all point permutations, the lex-least member of any solution's orbit satisfies every such clause, so the broken CNF is unsatisfiable exactly when the plain one is. A proof of the plain CNF also exists and was verified by both checkers; it exceeds this repository's file-size limit and is not shipped (its size and sha256 are in CLAIM.md of the panel folder and below).

Plain-CNF proof (not shipped): 48,063,525 bytes, sha256 09e70fe81f89da6c1552cfc10d7987ad1c9cedbedb1cd39a608a7210aba443ae; regenerate by running a DRUP-producing solver (glucose4 was used) on the plain CNF produced by `gen_cnf.py 8 3 13 out.cnf --sb none`.
3. Controls (SOUNDNESS.md section 7): a truncated proof and a foreign proof are rejected by both checkers; a family with three
   disjoint members is rejected by both family checkers; the sunflower clauses of every CNF were recomputed by brute force from
   the definition (`triples_recheck.py`, shipped in verify-it-yourself/) and matched; for the smallest cases an exhaustive
   SAT-free branch-and-bound (`exact_bb.py`) found the same maxima.

## Requirements

python3 3.8 or later (standard library) for the checkers; a C compiler for drat-trim.c; python-sat (pinned: python-sat >= 1.8,
the author used 1.9.dev15) only to regenerate the CNF with gen_cnf.py.
