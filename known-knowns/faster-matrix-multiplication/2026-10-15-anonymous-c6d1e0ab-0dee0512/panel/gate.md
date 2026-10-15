# Honesty gate (fmm-catalogue-small-format-rank)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/15x16x16_r2176_Q.json (sha256 0dee0512255d74595673fd8bfa0df20b0ab0a87785b2d11cbb2a94f6dbd5d57c) is an exact bilinear scheme over Q for the 15x16x16 matrix multiplication format with 2176 rank-one terms, all nonzero, satisfying all 14,745,600 Brent equations in exact integer arithmetic, and 2176 is strictly below 2223, the minimum rank for 15x16x16 in the four live sources fetched 2026-10-15 (fmm_sota.json 2223, Lille page 2262, Perminov README ZT 2302 / Z 2302 / Q 2223, MerlijnW70 tree no entry), and below the V3R1T4S trophy case entry of 2180.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is the same model family as the builder (codex-fmm, GPT-6.1), so the two Claude skeptics carry the cross-family check; the criterion skeptic verified every Brent equation with its own exact integer code and ran two negative controls.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The novelty skeptic fetched every source once (all HTTP 200): the lowest known rank is the repository's own trophy-case entry 2180 (its project, 2026-10-12); the public tables are 2223 (digest, Perminov Q), 2262 (Lille, a composition of 8x8x8 and 7x8x8 blocks) and 2302 (Perminov ZT/Z); MerlijnW70 has no file; no open pull request; nothing at or below 2176 in the last 24 months of literature. Margin 4 below the trophy case, 47 below the public tables.
- Full success criterion met, not a partial win. Table fetched under 6 hours before this gate.
- The scheme rebuilds deterministically from LITA's published 17x17x17 scheme (four slices, the builder's pinned recipe, byte-identical in a clean directory); the package ships that recipe.
- No downgrade triggers found.
