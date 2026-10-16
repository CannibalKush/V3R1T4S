# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/4x4x7_m85_cr294_ZT_reduced.json (sha256 a6655488fc692a5a552aed8c46ae58eff2a384d66f33966f3a53c0a33b3fec2e) is a ternary straight-line program that exactly computes the 4x4 by 4x7 matrix product over Z with Perminov's rank-85 scheme using 294 additions under the reduced convention (U 72, V 83, W 139), against 319 in Perminov's only addition_reduced_ZT file for 4x4x7 rank 85 as fetched on 2026-10-15, with no lower operation count on the fetched Lille 4x4x7 page or in the fetched COVERAGE.md.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 319), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 294, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 319, rank 85 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 447-85       631         326        320        0.25, 0.25, 0          - / 447-85         631       325      *322     309   49.0     0.21, 0.01, 0.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
