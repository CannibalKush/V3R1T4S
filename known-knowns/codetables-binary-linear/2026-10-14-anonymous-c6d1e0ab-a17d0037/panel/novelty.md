# Novelty review: binary linear code [173, 17, 72]

Role: novelty skeptic of the three-skeptic panel for claim `code-2-173-17`
(target `codetables-binary-linear`).
context: Claude Code subagent (Opus 5.5), fresh context

## What I read from the claim

- `CLAIM.md`: sha256 `2333a732c8cfb9eca632e4ef43281428a9ec643a69f90fc3d9408cbadb1cc9c0`. This matches `claim.SHA256SUMS`.
- `table-record/table_snapshot.md`: sha256 `f823703ddb2b234b2ff6dde1bdac96b6530e1f1e2e99504b65649e962b9510a0`. This matches `claim.SHA256SUMS`.
  The author recorded the interval [70, 77] for (2, 173, 17), fetched at 2026-10-14T10:24:01Z.
- `object/`: I read the file name only, `win_q2_n173_k17_d72.json`, as instructed. I did not open the object.
- Claim: a 17 x 173 generator matrix over GF(2) with minimum distance exactly 72. That is +2 over the
  codetables.de lower bound of 70.

## Sources fetched

Each table or repository source got one plain `curl` request with the User-Agent
`V3R1T4S-research (honest client; curl)`. There were no retries, no redirects followed, no cookies and no
proxy. Saved copies are in `novelty_ws/`.

| source | URL | UTC fetch time | HTTP | sha256 of saved page | value read |
|---|---|---|---|---|---|
| codetables.de cell | http://www.codetables.de/BKLC/BKLC.php?q=2&n=173&k=17 | 2026-10-14T16:14:11Z | 200 | `0560a33c46f9527ee08c84d865a63fd1db4226b2d55e217c7d4ad6544b585791` (4141 bytes) | "Bounds on linear codes [173,17] over GF(2)": **lower bound 70, upper bound 77** |
| repo trophy case | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-14T16:14:30Z | 200 | `b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412` (30486 bytes) | no row for this cell or for any binary linear code |
| repo open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-14T16:14:30Z (server Date 16:14:31 GMT) | 200 | `a84f49feb658469f9fded0612b36fba64ab42987c4b05c04fe979e64b142446f` (566072 bytes) | 25 open PRs; none covers this cell |
| LinCodeEvolve paper (literature, via WebFetch) | https://arxiv.org/pdf/2609.37056 (v1) | 2026-10-14T16:15:37Z | not shown by the tool; the full 17-page PDF arrived | `445ecd7658021ab01c4d224c12c7387291b036369d8339840085e27e76554ebc` | no entry at k = 17; at n = 173 only [173,20,68] and [173,21,66] |

There was no challenge page, block or rate-limit response from any table or repository source.

**codetables.de cell detail.** The page shows a [173,17,70] code taken as a subcode of a [173,18,70] code.
That code comes from Construction X on the quasi-cyclic [153,18,62] and [153,10,70] codes, with the entry
"last modified: 2003-04-09". The page also quotes Brouwer's table as of 2007-02-13: Lb(173,17) = 70 (GW2,
Grassl and White, ISIT 2005) and Ub(173,17) = 77 (BK, Berntzen and Kemper, 1993). The author's snapshot
from about six hours earlier read the same interval.

**Trophy case.** It has 53 rows across these families: degree-diameter graphs, constant-weight codes,
matrix multiplication, Lehmer, VNN-COMP, RobustBench and cipher commitments. None is a binary linear code
or a codetables.de row. A search for codetables, BKLC, "linear code", LinCode, GF(2) and 173 hit only two
constant-weight rows, where "173" is part of 1737 and 4173.

**Open pull requests.** The response had no `Link` header, so this one page lists all 25 open PRs. The
target ids in their titles are `packomania-hyperspheres-hsp4-hsp6`, `fmm-catalogue-small-format-rank`,
`thomson-problem-live-tables` and `constant-weight-codes`; the rest are tooling fixes and one review. I
searched titles, bodies, branch names and labels for codetables, binary-linear, BKLC, "linear code",
LinCode, Grassl, 173, k=17, 2609.37056 and GF(2). There was one hit, #130 (matrix multiplication), which
mentions GF(2) ranks in an unrelated context.

## The LinCodeEvolve exclusion (arXiv:2609.37056)

The paper is Seddas, Shashkov, Viazovska and Abbe, "Evolving Towards Better Codes: LLM-Guided Search
for High-Distance Binary Linear Codes". It has a single version, v1, submitted 29 Sep 2026.

- **Seven parent codes** (Table 2, measured against the CodeTables snapshot of 25 Sep 2026): [172,21,66],
  [173,20,68], [176,21,68], [181,21,70], [184,21,72], [189,22,72] and [200,21,77].
- **All 22 improved entries** (Table 3, page 17):
  - k = 20 at n = 172 and 173;
  - k = 21 at n = 171–178, 180–187, 200 and 201;
  - k = 22 at n = 188 and 189.

  None has k = 17. At n = 173 the only entries are [173,20,68] and [173,21,66].
- **Standard derivations** (subcode, shortening, puncturing, extension) from the seven parents reach at
  most d = 68 at (173, 17):
  - a subcode of [173,20,68];
  - [176,21,68] shortened three times and then cut to a subcode.

  [184,21,72] gives at most 65 (four shortenings and seven puncturings). [189,22,72] gives at most 61
  and [200,21,77] at most 54.
- **My extra check, beyond the paper's own list.** I rebuilt the five parents with block length 85 from
  the paper's Appendix A. Each matched the paper's published d and A_d exactly: A_d = 2720, 1156, 2992,
  3502 and 9826. Their tail coordinates depend only on r = b mod (x^5 - 1), so some 17-dimensional
  subcodes make tail coordinates vanish or repeat. I searched every such subcode with every way of
  keeping 3 tail coordinates to reach length 173. I tried both the paper's own tail patterns and any 3
  functionals of r on the same quasi-cyclic core. The best result at (173, 17) is d = 69, from
  [181,21,70] and [184,21,72]. That is below 72 and below the table's 70.
  - The script and its output are `novelty_ws/lce_derivation_check.py` and
    `novelty_ws/lce_derivation_check.out.txt`.
  - [189,22,72] (index 3, no tail) and [200,21,77] were not run. Reaching n = 173 at k = 17 from them
    takes 16 or 27 deletions with only 5 or 4 dimensions to give up, so shortening and puncturing alone
    cannot keep d = 72.
- **Limit.** I did not open the claimed object, so I cannot rule out that it is a subcode or variant of
  a LinCodeEvolve code built by a route outside those above. That provenance question belongs to the
  object-level review. On parameters alone, nothing in the paper or its derivations reaches d >= 70 at
  this cell, let alone 72.

## Literature search (window 2024-10-14 to 2026-10-14)

All queries ran between about 16:15Z and 16:26Z on 2026-10-14.

**arXiv listings.** These used the arXiv API, sorted by submission date, newest first.

| abstract query | coverage |
|---|---|
| "binary linear codes" | newest 100, reaching back past 2024-10-21 |
| "quasi-cyclic" AND "new" AND "binary" | |
| "record-breaking" AND "codes" | |
| "quasi-twisted" AND "codes" | all 30 |
| codetables OR "best known linear codes" | |
| "new binary codes" OR "new binary linear codes" OR "Construction X" | |

**Web searches** covered:
- the exact string "[173,17,72]";
- length 173, dimension 17, distance 71 or 72;
- new binary linear codes improving codetables in 2025 and 2026;
- AlphaEvolve and FunSearch work on linear codes;
- LLM agents beating codetables.de in 2026 (extended search);
- codetables claims on GitHub and Zenodo;
- Springer and IEEE journal papers from 2025–2026;
- "V3R1T4S codetables-binary-linear".

**Items found and checked:**

| paper | what it covers | reaches (173, 17)? |
|---|---|---|
| arXiv:2609.37056 (Sep 2026) | LinCodeEvolve; see the section above | no |
| arXiv:2412.15551 (Yu et al., Dec 2024) | record binary codes from group codes, lengths up to 120 only | no |
| arXiv:2608.18664 (Aug 2026) | abelian codes; records over F3 and F4 only, no binary record claimed | no |
| arXiv:2609.02096 (Sep 2026) | binary optimal LCD codes, dimensions 7 and 8 only | no |
| arXiv:2511.05440 (Nov 2025) | self-orthogonal embeddings; parameters at k = 8 | no |
| arXiv:2609.39081 (Sep 2026) | coding agents on quaternary edit-distance codes, lengths 6–9 | no |
| arXiv:2610.11609 (Oct 2026) | nonlinear A2(n, d) at n = 22, 24, 25 | no |
| AIMS Math doi 10.3934/math.20261194 (Sep 2026) | Goppa-code distance bounds; no table records | no |

No source, paper, trophy-case row or open PR claims any binary [173, 17, d] code with d >= 71. Nothing
newer than the 2003 construction exists at this cell at all.

One incidental web lookup returned 403: a science.ecosyste.ms project page that came up as a generic
search hit. It is not a table or status source, and I did not retry it.

## Verdict

The best known value at (q, n, k) = (2, 173, 17) across everything I found is d = 70:
- the live codetables.de lower bound, fetched at 2026-10-14T16:14:11Z, unchanged since 2003;
- LinCodeEvolve reaches at most 68 here by standard derivation and 69 by the structured routes I computed;
- no newer arXiv or web claim, trophy-case row or open pull request covers this cell.

The claimed d = 72 is strictly greater than 70, by 2, and does not exceed the upper bound of 77. On
novelty, the claim strictly beats everything known. Whether the object really has d = 72, and whether it
is unrelated to the LinCodeEvolve codes, is for the object-level skeptics.

pass: true
