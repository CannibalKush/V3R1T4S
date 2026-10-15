# Honesty gate (sunflower-free-capacity-lower-bound)

status: CONFIRMED_PARTIAL
partial_win: p2
confirmed_scope: claim/object/family_g8_4_24.json (sha256 d005484b9bf31c11634f4ed9c6cc2e1f4c99b6005a2f471f70fd9726bfbd09ca) is a family of 24 distinct 4-subsets of {1..8} with no three members (empty core included) having pairwise equal intersections, and drat-trim verifies claim/object/sb.drup as a refutation of the lex-leader-symmetry-broken CNF claim/object/sb.cnf for "at least 25 such members", whose clauses (apart from its first comment line, which the shipped generator words differently) the shipped generator regenerates, so g(8,4) = 24 exactly, with no claim about the 1.5545 rate bar or any other (n,r).

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the team that found the value (Claude Opus and Claude Fable agents).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own family checker, recomputed every sunflower triple, tested the cardinality block with its own solver, regenerated the CNF with python-sat 1.9.dev15, compiled drat-trim and verified the proof, and rejected truncated proofs and bad families.
- A first reproduce run failed on one point: the shipped CNF's first comment line did not match the current generator's wording. The author replaced the CNF files with the generator's output (clauses and variable map byte-identical, proofs unchanged and still verified) and reran the reproduce skeptic from scratch on the fixed package; the rerun passes. Both runs are kept in the panel folder.
- The novelty skeptic found no publication or tabulation of this value or of an exactly equivalent reformulation (OEIS, arXiv, Markström's Turán table, Polymath10, this repository); its unresolved sources (paywalled 1972 and 1992 papers on the unrestricted-ground-set problem) are listed in novelty.md.
- Partial win p2 only. The full success criterion (rate above 1.5545) is not claimed and not met by this family.
- One cell per claim: other exact values from the same computation are separate packages or not claimed.
- No downgrade triggers found.
