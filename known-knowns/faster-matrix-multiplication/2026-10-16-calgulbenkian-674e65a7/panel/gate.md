# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: The program in claim/object/2x8x8_m100_cr418_ZT_reduced.json (sha256 674e65a792736a9bf4930d7e529fb901990cafa22ddf52baaf6c2ed0d256a87f) exactly computes the 2x8 by 8x8 product over Z with 100 products, the same 100 products as Perminov's 2x8x8_m100_cr424_cn608_ZT_reduced.json, using 418 reduced additions (U 90, V 154, W 174) with all expanded intermediates ternary, which is below 424, the only and minimum reduced count for this format and rank in his live addition_reduced_ZT directory on 2026-10-15, with no Lille-page complexity variant and no matmulcatalog adds value for 2x8x8 found.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 424), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 418, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 424, rank 100 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: format absent at this rank.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
