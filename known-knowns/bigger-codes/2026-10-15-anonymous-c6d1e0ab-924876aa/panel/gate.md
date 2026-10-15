# Honesty gate (codetables-binary-linear)

status: CONFIRMED_SOLUTION
confirmed_scope: The generator matrix in claim/object/code_q2_n213_k26_d77.json (sha256 924876aa988e3a9da62a776f88c297db6aa005b475fe3ad9e76291685851cd12) has rank 26 over GF(2) and exact minimum distance 77 (A_77 = 1170) by full enumeration of all 67,108,863 nonzero codewords with two agreeing methods, which is strictly above the lower bound 76 and at most the upper bound 90 shown in the live codetables.de [213,26] cell fetched 2026-10-15T00:14:28Z, and it is not one of, nor by the paper's own text derived from, the seven LinCodeEvolve codes of arXiv:2609.37056; a live arXiv search for other newer claims was not completed.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the code's builders (a Claude Fable designer's scan, built and verified by a Claude Opus runner).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word. Its last clause (the arXiv search it did not complete) is covered by the novelty skeptic, whose literature search over the last 24 months found no claim reaching d >= 77 at this cell and no shorter [n',26,77] code.
- The novelty skeptic fetched the live cell at 2026-10-15T00:13:13Z and the criterion skeptic at 00:14:28Z; both pages have the sha256 the author recorded at 00:06:08Z (a0716470...5793): lower bound 76 (construction last modified 2001-01-30), upper bound 90. No open pull request or trophy-case row covers this cell.
- Full success criterion met, not a partial win. Table fetched under 6 hours before this gate.
- One cell per claim. The neighbouring cells (212,26) and (211,26) also show 76; this code gives nothing there by shortening (d would stay 77 at k = 25) so they are not claimed. Dimension 26 is unrelated to the contributor's other codes ([173,17,72], [175,25,61]).
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than the live table, scope no wider than reproduced).
