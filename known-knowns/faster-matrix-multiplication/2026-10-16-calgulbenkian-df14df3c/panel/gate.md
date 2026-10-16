# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: The program claim/object/4x4x5_m61_cr222_ZT_reduced.json (sha256 df14df3c1a01189e540ab5a0eedebc331cd08e12714d795df0884481da292366) is a ternary straight-line program that, with its 61 products identical to those of Perminov's 4x4x5_m61_cr233 scheme (rank 61, the best rank in fmm_sota.json), computes the 4x4 by 4x5 product exactly over Z (full tensor identity and random integer evaluation, all expanded forms in {-1,0,1}) using 222 additions under Perminov's reduced convention (U 59, V 61, W 102), below his single live reduced file's 233 and below any count on the Lille 4x4x5 page (none cited) or in COVERAGE.md (+455 naive); it does not lower the rank and I judged no novelty beyond these sources.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 233), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 222, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 233, rank 61 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 445-61       455         248        238        0, 0.01, 0.12          - / 445-61         455       248       238     217   47.7      0, 0.01, 0.1.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
