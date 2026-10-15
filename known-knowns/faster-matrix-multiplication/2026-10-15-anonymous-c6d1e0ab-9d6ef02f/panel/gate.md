# Honesty gate (fmm-catalogue-small-format-rank)

status: CONFIRMED_SOLUTION
confirmed_scope: The file claim/object/14x16x16_r2117_Q.json (sha256 9d6ef02f8162d9d5a53e56ecff6821459727c32d5a5fecb24283bd0c716fdf10) is an exact bilinear scheme over Q for the 14x16x16 matrix multiplication format with 2117 rank-one terms, each with all three factors nonzero, verified by my own exact integer check of all 12,845,056 Brent equations, and 2117 is strictly below 2128, the minimum rank for the sorted format 14x16x16 in fmm_sota.json, the Lille 14x16x16 page, Perminov's README ZT/Z/Q columns and MerlijnW70's fmm-schemes tree as I fetched them on 2026-10-15.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is the same model family as the builder (codex-fmm, GPT-6.1), so the two Claude skeptics carry the cross-family check; the criterion skeptic verified every Brent equation with its own exact integer code and ran two negative controls.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The novelty skeptic fetched every source once (all HTTP 200): digest 2128, Lille 2128 (imported from Perminov, not a composition), Perminov ZT 2170 / Z 2170 / Q 2128 (previously 2142), MerlijnW70 no file, no trophy-case row, no open pull request, nothing at or below 2117 in the last 24 months of literature. The cheapest composition of listed ranks is 2142. Margin 11.
- Full success criterion met, not a partial win. Table fetched under 6 hours before this gate.
- The scheme rebuilds deterministically from the repository's own published 15x16x16 rank-2180 scheme (one slice, the builder's pinned recipe, byte-identical in a clean directory); the package ships that recipe.
- No downgrade triggers found.
