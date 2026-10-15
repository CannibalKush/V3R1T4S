# Honesty gate (fmm-catalogue-small-format-rank)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/11x13x16_r1445_Q.json (sha256 d2d1c96812918b46fa34436c66cdd27e51383b12a9686a975d715d69e6480c75) is an exact bilinear scheme over Q (coefficients are the integers from -8 to 8 and the fractions plus or minus 1/2, 1/4, 1/8, so it is valid wherever 2 is invertible and is not a Z, ternary or GF(2) scheme) for the 11x13x16 format with 1445 rank-one terms, each with all three factors nonzero and no two mergeable, verified by my own exact-rational Brent-equation check, and 1445 is strictly below 1446, the minimum over the four criterion sources as I re-fetched them on 2026-10-14 between 17:26:49Z and 17:26:59Z (fmm_sota.json 1446; Lille 11x13x16 page 1446; Perminov README ZT 1458, Z 1458, Q 1446; MerlijnW70 fmm-schemes no 11x13x16 scheme in its complete tree), while the repository TROPHY_CASE.md dedup check was outside my permitted reading and is not asserted here.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`.
- The reproduce and criterion reports recorded here are second runs. The first runs also passed, but quoted the bank's Lille URL template with angle brackets, which the kit's checker reads as an unfilled placeholder.
- The criterion skeptic scoped its sentence to the four live tables. The novelty skeptic checked the V3R1T4S trophy case and open pull requests (fetched 2026-10-14T16:58:48Z) and found no entry for this format.
- Full success criterion met: 1445 is strictly below 1446, the minimum over the four live tables, re-fetched by the criterion skeptic at 17:26Z, under 6 hours before this gate. The margin is one multiplication. No downgrade triggers found.
