# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: For format 4x4x6 at rank 73 (the live best rank in fmm_sota.json), claim/object/4x4x6_m73_cr256_ZT_reduced.json (sha256 feea5fbcfd07fd3416d280a9a3d8af5e49c916171b9771d614e51e7a43f98b85) is a ternary straight-line program that exactly computes A*B over Z (Brent identity and random-integer evaluation verified, all expanded coefficients in {-1,0,1}) with 256 reduced additions, strictly below the live minimum of 280 in Perminov's addition_reduced_ZT for the same 73 products, with no lower count cited on the live Lille 4x4x6 page and only a non-comparable naive count in COVERAGE.md.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 280), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 256, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 280, rank 73 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: format absent at this rank.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
