# Honesty gate (sunflower-free-capacity-lower-bound)

status: CONFIRMED_PARTIAL
partial_win: p2
confirmed_scope: The 3-uniform 3-sunflower-free (empty core included) maximum family size on [8] is exactly 12, shown by claim/object/family_g8_3_12.json (sha256 f50c754478941fea73040430cfecc91e76de235b97ad541fcd59955eda163fa7, 12 distinct triples, no sunflower) and by claim/object/sb.drup, a DRUP proof drat-trim verifies against the lex-leader CNF claim/object/sb.cnf (a sound symmetry-broken form of "at least 13 members", whose clauses regenerate from gen_cnf.py with python-sat 1.9.dev15 identically except for one stale header comment line); no claim about the 1.5545 rate bar, other (n,r), or novelty.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the team that found the value (Claude Opus and Claude Fable agents).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own family checker, recomputed every sunflower triple, tested the cardinality block with its own solver, regenerated the CNF with python-sat 1.9.dev15, compiled drat-trim and verified the proof, and rejected truncated proofs and bad families.
- A first reproduce run failed on one point: the shipped CNF's first comment line did not match the current generator's wording. The author replaced the CNF files with the generator's output (clauses and variable map byte-identical, proofs unchanged and still verified) and reran the reproduce skeptic from scratch on the fixed package; the rerun passes. Both runs are kept in the panel folder.
- The novelty skeptic found no publication or tabulation of this value or of an exactly equivalent reformulation (OEIS, arXiv, Markström's Turán table, Polymath10, this repository); its unresolved sources (paywalled 1972 and 1992 papers on the unrestricted-ground-set problem) are listed in novelty.md.
- Partial win p2 only. The full success criterion (rate above 1.5545) is not claimed and not met by this family.
- One cell per claim: other exact values from the same computation are separate packages or not claimed.
- No downgrade triggers found.
