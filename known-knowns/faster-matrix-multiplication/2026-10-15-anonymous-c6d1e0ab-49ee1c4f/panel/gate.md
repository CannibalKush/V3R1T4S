# Honesty gate (fmm-catalogue-small-format-rank)

status: CONFIRMED_SOLUTION
confirmed_scope: The file claim/object/13x14x15_r1645_Q.json (sha256 49ee1c4f6642d1245e5af697eeb2f342024d04f06a0cc9113501ce8f45177144) is an exact bilinear scheme over Q for the matrix multiplication format 13x14x15 with 1645 rank-one terms (all three factors nonzero, no duplicates), verified by an independent exact-integer check of all 7,452,900 Brent equations, and 1645 is strictly below 1681, the minimum rank for the sorted format 13x14x15 in fmm_sota.json (createdAt 2026-10-09T11:45:48), the Lille per-format page, Perminov's ZT/Z/Q columns and MerlijnW70's fmm-schemes tree as fetched live on 2026-10-15T09:13Z, and below the V3R1T4S TROPHY_CASE.md entry 1677 for this format; rank over Q only.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is the same model family as the builder (codex-fmm, GPT-6.1), so the two Claude skeptics carry the cross-family check; the criterion skeptic verified every Brent equation with its own exact integer code.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The novelty skeptic fetched every source once (all HTTP 200): every public source gives 1681 (digest, Lille page, Perminov ZT/Z/Q, matmulcatalog); the repository's own trophy case holds 1677 (its project, 2026-10-10), which this claim beats by 32; MerlijnW70 has no file for this format; no open pull request mentions it; nothing at or below 1645 in the last 24 months of literature.
- Full success criterion met, not a partial win. Table fetched under 6 hours before this gate.
- The scheme rebuilds deterministically from LITA's published 15x15x15 scheme (the builder's REBUILD.md, byte-identical in a clean directory); the package ships that recipe.
- No downgrade triggers found.
