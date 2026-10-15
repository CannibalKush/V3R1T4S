# Novelty skeptic report: codetables-binary-linear, (q, n, k) = (2, 213, 26), claimed d = 77

context: Claude Code subagent (Opus 5.5), fresh context

Inputs read: claim/CLAIM.md, claim/table-record/README.md, the file names in claim/object/ (one file: code_q2_n213_k26_d77.json, contents not opened), and claim.SHA256SUMS. I opened no other local files.

## Primary sources fetched (each fetched once with curl and User-Agent 'V3R1T4S-research (honest client; curl)', no retries)

| Source | URL | UTC fetch time | HTTP status | sha256 of saved page | Value read |
|---|---|---|---|---|---|
| codetables.de cell | http://www.codetables.de/BKLC/BKLC.php?q=2&n=213&k=26 | 2026-10-15T00:13:13Z | 200 | a0716470e57fc32f112482c5b8e3aabff76a7c1c055dd7d3e6a5b5fac18b5793 | "Bounds on linear codes [213,26] over GF(2) lower bound: 76 upper bound: 90" |
| Repo trophy case | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T00:13:14Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | no binary linear code (codetables) entries; no [213,26] entry |
| Repo open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T00:13:14Z | 200 | 447b529a09c54d5f6c32ef62446dc92ca2fb1db7da0e8d729de1ddc19b37c03d | 28 open PRs; none for this cell |

Codetables cell details: the lower bound 76 comes from a subcode of a [213,28,76] code (ConstructionX [211,28,75], extended by 1, then padded by 1); the page footer says "last modified: 2001-01-30". The upper bound 90 comes from Brouwer's table (Ub(211,23) = 91, BK). The page sha256 is the same as the one in the author's table record (a0716470...b5793, fetched 2026-10-15T00:06:08Z), so the cell did not change between their fetch and mine. Claimed d = 77 is above 76 and at most 90.

Because the table is monotone in n, a lower bound of 76 at (213, 26) also means the table lists no [n', 26, >=77] code for any n' < 213 that zero-padding would carry to n = 213.

## Pull-request search

I scanned the titles and bodies of all 28 open PRs (#1 to #144) for "213", "[*,26", "codetables" and "LinCodeEvolve". Only #142 is a binary linear code claim: [173,17,72], which is a different cell and dimension. No open PR claims a [213,26] code or any code with k = 26. The other matches were incidental: packomania, Thomson, constant-weight and tooling PRs. The pending [175,25,61] claim mentioned in the brief is not among the open PRs, and it is also a different cell.

## Trophy case

TROPHY_CASE.md (100 lines) lists constant-weight codes, graphs, matrix multiplication and other families. It has no codetables binary linear code entry and nothing at [213,26].

## Literature search (last 24 months, Oct 2024 to Oct 2026)

- arXiv:2609.37056 (LinCodeEvolve, Seddas, Shashkov, Viazovska, Abbe, v1 29 Sep 2026), read on its abstract and HTML pages. It has 7 parent codes: [172,21,66], [173,20,68], [176,21,68], [181,21,70], [184,21,72], [189,22,72] and [200,21,77]. Its Table 3 lists 22 derived entries at lengths 171 to 201 with k in {20, 21, 22}; the largest d is [201,21,78]. No entry has k = 26 or n = 213. No entry reaches d >= 77 with k >= 26.
- Derivation note: standard derivations (shortening, puncturing, extending, padding, taking subcodes) cannot raise the dimension from 21 or 22 to 26. So the [213,26] cell is not a standard derivative of the LinCodeEvolve codes. I did not open the object, so whether it is built structurally from those codes is for the structural check to confirm.
- arXiv:2610.11609 (Ota, Osa, Harada, 8 Oct 2026) covers nonlinear codes only: A(22,9), A(24,9), A(25,11). Not relevant to this cell.
- arXiv:2412.15551 (group-code records) covers lengths up to 120 only. Not relevant.
- arXiv:2608.18664 (abelian codes) has its records over GF(3) and GF(4). Not binary.
- An arXiv full-text search ("binary linear codes improved minimum distance", newest first) and web searches for "[213,26", "binary linear code [213,26] minimum distance 77" and "[210-212, 26, 77]" found no other [213,26] claim. They also found no shorter [n',26,>=77] binary code and no other binary record batch at lengths 200 to 256 besides LinCodeEvolve.

Limits: web and arXiv search coverage is not exhaustive, and private emails to Grassl that are not yet in the table cannot be seen.

## Verdict

Best known for binary [213,26] from every source I found: d = 76 (live codetables.de lower bound). Nothing newer reaches 77. The claimed d = 77 is strictly above that, so it is not a tie, and it is at most the upper bound of 90. It is outside the cells that LinCodeEvolve and its derivations cover.

novelty: PASS (subject to the exactness and structural checks of the other skeptics)

pass: true
