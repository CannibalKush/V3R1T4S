# Honesty gate (fmm-catalogue-small-format-rank)

status: CONFIRMED_SOLUTION
confirmed_scope: The file claim/object/13x14x14_r1538_Q.json (sha256 4b613512756bdb5c0303dc17236ad63b3b8a4e931d898e75e863d95d6dd9ab9e) is an exact bilinear scheme over Q for the matrix multiplication format 13x14x14 with 1538 rank-one terms, each with all three factors nonzero, satisfying every Brent equation in exact arithmetic by my own independent check, and 1538 is strictly below the 13x14x14 rank in each of the four criterion sources as fetched on 2026-10-15 (fmm_sota.json 1582, Lille per-format page 1614, Perminov README minimum over ZT/Z/Q 1582, MerlijnW70 repository none) and below the TROPHY_CASE.md entry of 1558.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is the same model family as the builder (codex-fmm, GPT-6.1), so the two Claude skeptics carry the cross-family check; the criterion skeptic verified all 6,492,304 Brent equations with its own exact code and rejected five corrupted variants.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The novelty skeptic fetched every source once (all HTTP 200): the lowest known rank is the repository's own trophy-case entry 1558 (its project, 2026-10-10); the public tables are 1582 (digest, Perminov) and 1614 (Lille); MerlijnW70 has no file; no open pull request; nothing at or below 1538 in the last 24 months of literature. The cheapest composition of listed ranks is 1633. Margin 20 below the trophy case.
- Full success criterion met, not a partial win. Table fetched under 6 hours before this gate.
- The scheme rebuilds deterministically from LITA's published 15x15x15 scheme (four slices, the builder's pinned recipe, byte-identical in a clean directory); the package ships that recipe.
- No downgrade triggers found.
