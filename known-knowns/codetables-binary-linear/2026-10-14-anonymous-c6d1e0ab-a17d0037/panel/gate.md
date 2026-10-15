# Honesty gate (codetables-binary-linear)

status: CONFIRMED_SOLUTION
confirmed_scope: The matrix in claim/object/win_q2_n173_k17_d72.json (sha256 a17d00378317979d9fe0acb452d3cce805f55cb17595a8407acb9b56b7b51a76) is a 17 x 173 GF(2) generator matrix of rank 17 whose code has, by two independent full enumerations of all 131071 nonzero codewords, minimum distance exactly 72 with 6341 minimum-weight words, which strictly exceeds the lower bound 70 and does not exceed the upper bound 77 shown in the live codetables.de cell for q=2, n=173, k=17 fetched once at 2026-10-14T16:16:39Z, and which is neither one of nor a subcode or standard derivative (under the quasi-cyclic-structure-preserving maps tested) of the seven arXiv:2609.37056 LinCodeEvolve codes, whose published improvements are all at k in {20,21,22}.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`.
- The novelty and criterion skeptics read the first claim folder; the reproduce skeptic read the rebuilt one. Both folders hold the same object (sha256 a17d0037...) and the same claim sentence. Only the shipped checker differs: a new standalone checker replaced one that needed third-party table data.
- Full success criterion met, not a partial win. Table fetched 2026-10-14T16:14:11Z, under 6 hours before this gate.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than the live table, scope no wider than reproduced).
