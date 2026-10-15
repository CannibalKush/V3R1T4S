# Honesty gate (fmm-catalogue-small-format-rank)

status: CONFIRMED_SOLUTION
confirmed_scope: The file claim/object/15x16x15_r2105_Q.json (sha256 4b68518ac7f293047071df6723a04783e4d38f302c6b98ccaa02f0c66669ae3b) is an exact bilinear scheme over Q for the format 15x16x15 with 2105 rank-one terms, all three factors nonzero in every term, satisfying all 12,960,000 Brent equations in exact rational arithmetic, and 2105 is strictly below 2132, the rank listed for the sorted format 15x15x16 in fmm_sota.json (createdAt 2026-10-09T11:45:48), the Lille 15x15x16 page, and Perminov's README ZT/Z/Q columns, with no 15x15x16 scheme in the MerlijnW70 fmm-schemes tree, all four fetched 2026-10-15T09:31Z.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. This is the second panel on this scheme: the first object file carried a local file path in its free-text note field, so the note was rewritten (the scheme's terms are unchanged) and the full panel was run again on the new file; the first panel also passed on all three counts.
- The final step was built by a Claude Opus agent (opus-fmm) on a parent chain built by a GPT agent (codex-fmm), so each model family checked the other's part; the criterion skeptic verified every Brent equation with its own exact rational code and ran a negative control; its composition null models give 2193 (best split) and 2236 (best padding), so 2105 is not a composition.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word. The object stores the axes as 15x16x15, a cyclic rotation of 15x15x16; rank is invariant under axis permutation and the criterion compares the sorted format.
- The novelty skeptic fetched every source once (all HTTP 200): the best rank anywhere for sorted 15x15x16 is 2132; MerlijnW70 has no file; no trophy-case row or open pull request; nothing at or below 2105 in the last 24 months of literature. Margin 27.
- Full success criterion met, not a partial win. Table fetched under 6 hours before this gate.
- The scheme rebuilds deterministically from LITA's published 17x17x17 scheme (four slices by the GPT builder's pinned recipe to 15x16x16 rank 2176, then one slice and a seeded absorption by the Opus builder); both scripts and their real outputs ship in the package.
- No downgrade triggers found.
