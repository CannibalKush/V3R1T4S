# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/4x6x7_m123_cr469_ZT_reduced.json (sha256 ade76c2eef28cca082e6f87f2ca0294f6a6e5bcdce1e1cb9356fe068bab0dd65) is a ternary straight-line program that, by my exact integer expansion, computes the 4x6x7 product with 123 products (the same products as Perminov's cr517 file, equal to the fmm_sota.json rank) using 469 reduced additions (U 114, V 140, W 215), below the sole live addition_reduced_ZT count of 517, with no Lille operation count and only a naive 1586 count in COVERAGE.md to beat.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 517), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 469, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 517, rank 123 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: no count over Z; 575 over Z2 (Table 3.5, not comparable).
- An open pull request on this repository claims 503 for the same cell; 469 is strictly below it, and the table value compared against is Perminov's 517.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
