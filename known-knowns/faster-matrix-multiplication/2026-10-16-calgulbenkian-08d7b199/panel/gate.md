# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/4x5x5_m76_cr281_ZT_reduced.json (sha256 08d7b199e9ecc9f7254dc46c23ecf2128e83444277b19eac6bbcb678a107f819) is a ternary straight-line program that, by my own exact checker, computes the full 4x5 by 5x5 product over Z with Perminov's 76 products (expanded U, V, W rows identical to his) using 281 additions under the reduced convention (U 75, V 84, W 122), against 299 in the only 4x5x5 file of his live addition_reduced_ZT directory, with no cited count on the Lille 4x5x5 page and COVERAGE.md giving only a naive +549.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 299), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 281, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 299, rank 76 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 455-76       549         322        310      0.26, 0.01, 0.11       437 / 455-76        1,107      469         451      656    59.2       0.17, 0.1, 0.104 / 455-76     1,015          388       372      643     63.3     0.145, 0.11, 0.005 / 455-76          549      325       310     239   43.5    0.19, 0.1, 0.1.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
