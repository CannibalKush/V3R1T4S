# Honesty gate (hadamard-maxdet-records)

status: CONFIRMED_SOLUTION
confirmed_scope: The 109 x 109 {+1,-1} matrix in claim/object/M109_2119202655125403624550373680790052808829003860176536932438843923020304438454497.txt (sha256 0108345c2f3cbffdd58f23eef8aba73546583f02062a013a5b64ab95e198faa6) has exact |det| = 2^108 * 291 * 27^53 = 2^108 * 2119202655125403624550373680790052808829003860176536932438843923020304438454497 (Bareiss, 8-prime CRT and 120-digit mpmath agree), which is strictly below the Barba bound for n = 109 (ratio 0.731643) and strictly above the only n = 109 value carried by the criterion's enumerated sources at verification time on 2026-10-14 16:16-16:23 UTC, Rokicki's 2005 two-circulant record 1877483841834222713683125485573890072927341503771574105042244268774869908324352 (= 1.877483842E78 in the Archive-It copy of Orrick's MaxDet table, itself strictly below the bound at ratio 0.648191, reproduced exactly from Rokicki's published first rows), while the arXiv:2608.22518v3 / Math-AI-Caltech CSV and EinsteinArena order-51 sources carry no n = 109 value and an arXiv search found no newer n = 109 value.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`.
- The novelty and criterion skeptics read the first claim folder; the reproduce skeptic read the rebuilt one. Both hold the same object (sha256 0108345c...) and the same claim sentence. Only the shipped checker and record notes differ.
- An earlier reproduce run failed only because sympy, which the success criterion names for a cross-check, was not installed. The run recorded here had sympy and its cross-check agreed.
- The criterion skeptic found that the original package attributed the record to the Math-AI-Caltech CSV, which has no order-109 row. The rebuilt package attributes it to Tomas Rokicki's entry in Orrick's archived table, the source the panel verified.
- Full success criterion met. Table fetched 2026-10-14T16:16:58Z, under 6 hours before this gate. No downgrade triggers found.
