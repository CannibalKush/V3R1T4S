# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/2x5x6_m47_cr179_ZT_reduced.json (sha256 3d1e40cf65f343ad2edfe3735c1d4eccd1fd4aeaca82b31980779e38a059dcc1) is a ternary straight-line program that I verified exactly over Z (full 2x5x6 tensor identity, all expanded coefficients in {-1,0,1}) to compute a rank-47 scheme with the same 47 products as Perminov's 2x5x6 cr181 file and 179 additions under his reduced convention (U 38, V 65, W 76; V and W programs identical to his, U program 2 additions shorter), below his only 2x5x6 file (181), with no Lille operation count to compare against and COVERAGE.md giving only the naive 332.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 181), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 179, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 181, rank 47 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 256-47       332         189        184        0.43, 0.01, 0          - / 256-47         332       188       184     148   44.6     0.31, 0.01, 0.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
