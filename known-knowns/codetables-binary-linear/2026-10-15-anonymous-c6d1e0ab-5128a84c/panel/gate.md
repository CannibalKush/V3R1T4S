# Honesty gate (codetables-binary-linear)

status: CONFIRMED_SOLUTION
confirmed_scope: The 25 x 175 matrix in claim/object/code_q2_n175_k25_d61.json (sha256 5128a84caf064a0c4b0b6bd46d4c8d26e02cddac4bbc988437a72c947859e17c) has rank 25 over GF(2) and generates a binary linear [175,25,61] code with exactly 95 codewords of weight 61, established by two independent full enumerations of all 33,554,431 nonzero codewords, and 61 exceeds the lower bound 60 and is below the upper bound 72 shown in the live codetables.de cell for q=2, n=175, k=25 fetched once at 2026-10-14T19:15:17Z, while the code is not one of, and by dimension cannot be a standard derivative of, the seven LinCodeEvolve codes of arXiv:2609.37056 (all of dimension 20 to 22), and a single arXiv API query on 2026-10-14 found no newer claim of a binary [175,25] code with minimum distance 61 or more.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the code's builder (a Claude Opus agent with a Claude Fable reviewer on the team).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The novelty skeptic fetched the live cell at 2026-10-14T19:09:10Z and the criterion skeptic at 19:15:17Z; both pages have the sha256 recorded by the author at 19:00:20Z (248159ac...307e), with lower bound 60 and upper bound 72. The novelty skeptic also found MinT's lower bound 60, and no open pull request or trophy-case row covering this cell.
- Full success criterion met, not a partial win. Table fetched under 6 hours before this gate.
- One cell per claim: the parity extension [176,25,62] (lower bound 61 there) follows from this code and is not claimed separately.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than the live table, scope no wider than reproduced).
