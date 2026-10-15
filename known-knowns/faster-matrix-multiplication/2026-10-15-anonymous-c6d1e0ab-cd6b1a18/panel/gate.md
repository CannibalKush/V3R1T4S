# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/5x5x8_m144_cr556_ZT_reduced.json (sha256 cd6b1a181d857f3e993cc6c15338a7f709bd1119c2745a399cfc02eae9b52f03) is a ternary straight-line program for the Perminov rank-144 scheme of the 5x5x8 format that computes A*B exactly over Z with 556 additions under the reduced convention, versus 620 for the only 5x5x8 file in Perminov's live addition_reduced_ZT, with no operation count for this rank on the Lille page and only a different naive count in COVERAGE.md; it shows no rank improvement and no evidence for any other format.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 620), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 556, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 620, rank 144 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: format absent.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
