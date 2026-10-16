# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/5x5x7_m127_cr483_ZT_reduced.json (sha256 1e59f08cf1870f4ade6b3ab5efc2d004e5bb1a0edb455b7e250ed4a7cfc6a65a) is a ternary straight-line program that exactly computes the 5x5 by 5x7 product with rank 127, equal to the fmm_sota.json best rank, using 483 additions under the reduced convention (U 116, V 137, W 230) against 531 for Perminov's only live addition_reduced_ZT file at this format and rank, over the same 127 products, with no lower reduced count on the Lille page or COVERAGE.md.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 531), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 483, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 531, rank 127 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 557-127     1,518     577            566      952    62.7       0.0 , 0.1 , 0.08 / 557-127   1,518     584             560       958    63.1        0, 0.18, 0.06 / 557-127   1,554     584             568       986    63.4      0.02, 0.08, 0.06 / 557-127   1,590     570             563      1027    64.6      0.02, 0.16, 0.06.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
