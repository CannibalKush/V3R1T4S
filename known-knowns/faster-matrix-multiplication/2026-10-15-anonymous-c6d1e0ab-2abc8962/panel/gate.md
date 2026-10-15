# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: The program in claim/object/5x7x7_m176_cr699_ZT_reduced.json (sha256 2abc89623e051336de20440c1e68300d56656b98733b8df7e66808bbd60174be) is an exact ternary straight-line program for the same 176 products as Perminov's cr788 5x7x7 file, verified over Z by my own Brent and random-matrix checks, and costs 699 reduced additions (U 179, V 206, W 314) against his sole 5x7x7 addition_reduced_ZT file at 788, with the Lille page citing no operation count and matmulcatalog's naive +2745 not on the reduced convention, as of my fetches.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 788), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 699, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 788, rank 176 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: no count over Z; 817 to 826 over Z2 (Table 3.5, not comparable).
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
