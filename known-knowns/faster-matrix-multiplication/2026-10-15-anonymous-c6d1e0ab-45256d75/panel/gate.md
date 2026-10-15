# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/4x6x8_m140_cr476_ZT_reduced.json (sha256 45256d75a05660145a239129ba59524edf864bbda68bcf5297be8fdf7c38158e) is a ternary straight-line program that exactly computes the full 4x6 by 6x8 product over Z with 140 products (the best listed rank) using 476 reduced additions (U 108, V 136, W 232), strictly below the single live Perminov addition_reduced_ZT value of 551 for this format and rank, with no count published for it on the live Lille page or in the live COVERAGE.md adds column.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 551), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 476, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 551, rank 140 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: format absent.
- The criterion skeptic found that the products are not those of Perminov's file but a Kronecker product of two of his schemes (the construction the Lille catalogue lists for this rank); the author corrected the one-sentence claim before the gate. The criterion compares formats at the best known rank, not schemes.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
