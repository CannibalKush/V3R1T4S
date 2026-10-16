# Honesty gate (fmm-catalogue-small-format-rank)

status: CONFIRMED_SOLUTION
confirmed_scope: The object claim/object/13x15x15_r1762_Q.json (sha256 5b97769fb1c3115c7195f0c508e0cae9ded013ef2543a7f0d5aa4147410e1647) is, by my own exact rational check using Perminov's index convention (C stored transposed), a correct bilinear scheme over Q for the 13x15x15 matrix product with 1762 terms having all three factors nonzero, strictly below 1776 (fmm_sota.json and the Perminov table minimum), 1797 (Lille), the absent MerlijnW70 entry, and the repository's merged 1763, as fetched 2026-10-15.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the scheme's builder (a Claude Opus agent, opus-fmm) and the orchestrator.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The reproduce skeptic verified all 8,555,625 Brent equations over Q with its own exact checker (termwise common denominator) and found 1,762 nonzero terms; repeated runs identical; the negative control (last term removed) is rejected.
- A first reproduce run verified the object identically but failed on one documentary point: the claim sentence attributed the 1763 baseline to the live tables, while the catalogues list 1776 and 1763 is the repository's own merged scheme (pull request #130). The author corrected the sentence (object unchanged) and reran the reproduce skeptic from scratch; the rerun passes. Both runs are kept in the panel folder.
- The bar is 1763: the merged rank-1763 scheme in known-knowns/faster-matrix-multiplication (PR #130, merged 2026-10-15 16:33 UTC). The live catalogues give 1776 (fmm_sota.json, Perminov README Q) and 1797 (Lille); MerlijnW70 has no entry; TROPHY_CASE.md had not been regenerated to list 1763 at fetch time. The maintainer's comment on PR #164 invites this rank-1762 scheme as "one below the merged #130". 1762 is a strict improvement by one.
- Full success criterion met for this cell; not a partial win. One cell per claim.
- No downgrade triggers found.
