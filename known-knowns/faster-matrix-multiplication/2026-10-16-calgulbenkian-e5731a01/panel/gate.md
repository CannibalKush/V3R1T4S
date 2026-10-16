# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: The program claim/object/3x4x5_m47_cr156_ZT_reduced.json (sha256 e5731a01ecf58de14b5fc4a6e9a0de880b11146aeeeef4df6844dd83bfbb83a8) is a ternary straight-line program (all expanded forms in {-1,0,1}) computing the exact 3x4 by 4x5 integer matrix product with the same 47 products as Perminov's 3x4x5_m47_cr161 file (rank 47 equals the fmm_sota.json best), using 156 additions under his reduced convention (U 38, V 44, W 74, W program unchanged from his), against his live-directory minimum of 161 and no lower count on the Lille 3x4x5 page or in COVERAGE.md (naive +287), as fetched on 2026-10-15.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 161), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 156, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 161, rank 47 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 345-47         714       284         276      438    61.3         0, 0.11, 0.08 / 345-47      668           254       242      426     63.8       0, 0.005, 0.07 / 345-47          287      171       161     126   43.9   0.23, 0.01, 0.01 / 345-47          288    176         165     123   42.7   0.21, 0.01, 0.08.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
