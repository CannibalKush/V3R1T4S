# Honesty gate (fmm-catalogue-small-format-rank)

status: CONFIRMED_SOLUTION
confirmed_scope: The file claim/object/13x13x14_r1479_Q.json (sha256 e738d0f367b67ba740109db2687b58811da516ee74f67c42ccb934eab382548d) is a bilinear scheme with exactly 1479 rank-one terms, all three factors nonzero in every term, whose coefficients are rationals with denominators dividing 1088 and which satisfies all 5597956 Brent equations for the format 13x13x14 exactly over Q, and 1479 is strictly below 1511, the rank listed for the sorted format 13x13x14 in each of fmm_sota.json (createdAt 2026-10-09T11:45:48), the Lille page https://fmm.univ-lille.fr/13x13x14.html, and Perminov's README ZT/Z/Q columns, while MerlijnW70's fmm-schemes held no 13x13x14 scheme, all as fetched by me once on 2026-10-15 between 09:13:40Z and 09:13:43Z.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is the same model family as the builder (codex-fmm, GPT-6.1), so the two Claude skeptics carry the cross-family check; the criterion skeptic verified every Brent equation with its own exact integer code.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The novelty skeptic fetched every source once (all HTTP 200): the digest, the Lille page (which takes its 1511 from Perminov and lists no composition), Perminov's ZT/Z/Q columns (1511 each), the MerlijnW70 tree (no file for any axis order), the trophy case and the 40 open pull requests (no entry), and found nothing at or below 1479 in the last 24 months of literature.
- Full success criterion met, not a partial win: max side 14, format not excluded, exact over Q, strictly below the minimum of all four sources by 32. Table fetched under 6 hours before this gate.
- The scheme rebuilds deterministically from LITA's published 15x15x15 scheme (the builder's REBUILD.md, byte-identical in a clean directory); the package ships that recipe.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than the live table, scope no wider than reproduced).
