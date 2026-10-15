# Honesty gate (sunflower-free-capacity-lower-bound)

status: CONFIRMED_PARTIAL
partial_win: p2
confirmed_scope: g(7,3) = 12, meaning the family claim/object/family_g7_3_12.json (sha256 b07e14e50f5669104565b4f3252e88b2589e80a346037127d0c0f02975aad8e0) is a 3-uniform 3-sunflower-free family of 12 distinct members on [7], and the proof claim/object/nosb.drup is verified by drat-trim as an UNSAT proof of the proved CNF claim/object/nosb.cnf (exactly the 315 sunflower clauses plus an "at least 13" counter), which the shipped generator regenerates identically in all variables and clauses but not byte-for-byte (its first comment line differs); no claim is made about the 1.5545 rate bar or any other (n,r).

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the team that found the value (Claude Opus and Claude Fable agents).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own family checker, recomputed every sunflower triple, tested the cardinality block with its own solver, regenerated the CNF with python-sat 1.9.dev15, compiled drat-trim and verified the proof, and rejected truncated proofs and bad families.
- A first reproduce run failed on one point: the shipped CNF's first comment line did not match the current generator's wording. The author replaced the CNF files with the generator's output (clauses and variable map byte-identical, proofs unchanged and still verified) and reran the reproduce skeptic from scratch on the fixed package; the rerun passes. Both runs are kept in the panel folder.
- The novelty skeptic found no publication or tabulation of this value or of an exactly equivalent reformulation (OEIS, arXiv, Markström's Turán table, Polymath10, this repository); its unresolved sources (paywalled 1972 and 1992 papers on the unrestricted-ground-set problem) are listed in novelty.md.
- Partial win p2 only. The full success criterion (rate above 1.5545) is not claimed and not met by this family.
- One cell per claim: other exact values from the same computation are separate packages or not claimed.
- No downgrade triggers found.
