# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/5x5x6_m110_cr413_ZT_reduced.json (sha256 760a6fabaf3fef7778e29b48d9b96dca9ae9dc8686afa84060805ac3be723354) is a straight-line program with all expanded coefficients in {-1,0,1} that computes the 5x5 by 5x6 product exactly over Z with rank 110 (Perminov's own 110 products, equal to the best listed rank) using 413 reduced additions (U 108, V 114, W 191), strictly below the 460 of the only live 5x5x6 addition_reduced_ZT file, with no lower count on the Lille page or in COVERAGE.md.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 460), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 413, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 460, rank 110 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 556-110     1,325     511            492      833    62.9      0.18 , 0.12 , 0.08 / 556-110   1,333     511             495       838    62.9       0.1, 0.12, 0.08 / 556-110   1,325     511             496       829    62.6      0.16, 0.16, 0.08.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
