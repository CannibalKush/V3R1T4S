# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/5x8x8_m230_cr929_ZT_reduced.json (sha256 0fb366e6a2a5cc6bc6fd0b31334b1d859df86c180c0fc30759cbbd41c4867501) is a ternary straight-line program that exactly computes the <5,8,8> product over Z with the same 230 products as Perminov's cr974 scheme and 929 additions under the reduced convention (U 205, V 327, W 397), strictly below the 974 in his only addition_reduced_ZT file for this format and rank, with the Lille 5x8x8 page citing no operation count and COVERAGE.md listing only the naive +2638.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 974), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 929, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 974, rank 230 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: format absent at this rank.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
