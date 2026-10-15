# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: The program claim/object/4x6x6_m105_cr373_ZT_reduced.json (sha256 0daeb11814025acb716cc2cb7432d358a83e8bff7985faec2ef73e5efad21bda) is a ternary straight-line program that exactly computes the 4x6 by 6x6 product at rank 105 (the live best rank) with 373 additions under Perminov's reduced convention (U 95, V 106, W 172), strictly below the single live addition_reduced_ZT file for 4x6x6 at rank 105 (cr 430, recounted as 430 by the same counter), with no comparable lower count on the Lille page or in COVERAGE.md.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 430), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 373, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 430, rank 105 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: no count at rank 105; 464 over Z at rank 106 (another scheme, Table 3.4).
- The criterion skeptic found that the products are not those of Perminov's file but a Kronecker product of two of his schemes (the construction the Lille catalogue lists for this rank); the author corrected the one-sentence claim before the gate. The criterion compares formats at the best known rank, not schemes.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
