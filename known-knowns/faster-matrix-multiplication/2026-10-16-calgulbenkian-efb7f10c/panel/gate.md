# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: The file claim/object/5x6x8_m170_cr667_ZT_reduced.json (sha256 efb7f10c7e3a5dcd2481aacbd72ae5e308550dd825927d1c1114574354447c80) is a ternary straight-line program that exactly computes the full 5x6 times 6x8 product over Z at rank 170 (Brent identity verified, every expanded coefficient in {-1,0,1}) using 667 reduced additions (U 159, V 196, W 312), strictly below the 720 of the only addition_reduced_ZT file for 5x6x8 rank 170, on the same products as that file, and no source checked (the live Lille page, COVERAGE.md) gives a comparable lower count.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 720), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 667, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 720, rank 170 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: format absent at this rank.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
