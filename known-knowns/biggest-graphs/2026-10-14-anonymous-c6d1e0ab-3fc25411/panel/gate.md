# Honesty gate (degree-diameter-table)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/G_14_3_N1117.edges (sha256 3fc25411941fa666946464317bc9672386a4923bcb01a24e2c42ec7239b8c3a4) is a simple undirected graph on 1117 vertices with maximum degree 14 (68 vertices of degree 13, 1049 of degree 14), connected with exact diameter 3 by independent all-pairs BFS, of order at most the Moore bound 2563, and its order 1117 strictly exceeds the non-boldface (14,3) entry 1116 of the live Comellas general-graph table as fetched once at 2026-10-14T16:16:12Z (page sha256 aa4e747b76562bc78a8b2a38946d35a2266ef5352cca59e623c3ea77c8720d35, Last-Modified 2026-10-14 13:17:04 GMT).

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`.
- The novelty and criterion skeptics read the first claim folder; the reproduce skeptic read the rebuilt one. Both folders hold the same object (sha256 3fc25411...) and the same claim sentence. Only the shipped checker differs: a new standalone checker replaced one that needed third-party table data.
- Full success criterion met, not a partial win. Table fetched 2026-10-14T16:14:01Z, under 6 hours before this gate.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than the live table, scope no wider than reproduced).
