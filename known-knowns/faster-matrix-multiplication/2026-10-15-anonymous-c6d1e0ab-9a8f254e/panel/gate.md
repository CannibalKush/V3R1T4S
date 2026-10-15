# Honesty gate (fmm-catalogue-small-format-rank)

status: CONFIRMED_SOLUTION
confirmed_scope: The file claim/object/13x13x15_r1578_Q.json (sha256 9a8f254ed5b7e15b8f4157da632c5adc686e46c4f020659b924114c8b7c5a618) is an exact bilinear matrix multiplication scheme over Q for the format 13x13x15 with exactly 1578 rank-one terms, each with all three factors nonzero, verified by my own exact big-integer and multi-prime Brent-equation checks, and 1578 is strictly below the rank for the sorted format 13x13x15 in each of the four named sources as fetched live on 2026-10-15 (fmm_sota.json 1605, Lille page 1605, Perminov README ZT/Z/Q 1591/1591/1591, MerlijnW70 file 13x13x15_m1591_ZT.json), whose minimum is 1591.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The final step was built by a Claude Opus agent (opus-fmm) on a parent chain built by a GPT agent (codex-fmm), so each model family checked the other's part; the criterion skeptic verified every Brent equation with its own exact code and ran two negative controls.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The novelty skeptic fetched every source once (all HTTP 200): the strictest value is 1591 (Perminov ZT/Z/Q and a MerlijnW70 ternary file); the Lille page and digest list 1605, a composition of 15 block schemes; no trophy-case row, no open pull request, nothing at or below 1590 in the last 24 months of literature. Margin 13.
- Full success criterion met, not a partial win. Table fetched under 6 hours before this gate.
- The scheme rebuilds deterministically from LITA's published 15x15x15 scheme: the GPT builder's pinned chain to 13x14x15 rank 1649, then one slice with exact absorption by the Opus builder (both scripts and their real outputs ship in the package; the GPT builder also reproduced the full chain byte for byte).
- No downgrade triggers found.
