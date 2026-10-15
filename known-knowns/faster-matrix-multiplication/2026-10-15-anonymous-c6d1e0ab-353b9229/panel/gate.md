# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/6x8x8_m266_cr993_ZT_reduced.json (sha256 353b922983ecc35f13d03a9e7136407be941d5a3282630c9eb9c13af94c236ec) is a ternary straight-line program for a rank-266 scheme for <6,8,8>, exact over Z by my own tensor-identity and random-evaluation checks, with 993 reduced additions (U 255, V 274, W 464), against 1161 for the only live Perminov file for this format and rank, with no count for this format and rank on the Lille page or in COVERAGE.md to compare, and the scheme itself is not Perminov's scheme.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 1161), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 993, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 1161, rank 266 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: format absent (the paper stops at 5x7x10).
- The criterion skeptic found that the products are not those of Perminov's file but a Kronecker product of two of his schemes (the construction the Lille catalogue lists for this rank); the author corrected the one-sentence claim before the gate. The criterion compares formats at the best known rank, not schemes.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
