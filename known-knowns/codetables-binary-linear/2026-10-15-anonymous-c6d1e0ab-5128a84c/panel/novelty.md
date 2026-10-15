# Novelty review: binary linear code cell (q, n, k) = (2, 175, 25), claimed d = 61

context: Claude Code subagent (Opus 5.5), fresh context

Role: NOVELTY skeptic of the three-skeptic panel. Review date: 2026-10-14.

## What I read from the claim

- `claim/CLAIM.md` and `claim/table-record/README.md`, plus the file name in `claim/object/`
  (`code_q2_n175_k25_d61.json`). I did not open the object, the checker, REPRODUCE.md or INDEX.csv.
- All 7 entries in `claim.SHA256SUMS` match the files (`shasum -a 256 -c`: all OK).
- The claim: a 25 x 175 binary generator matrix of rank 25 with minimum distance exactly 61, against a
  codetables.de lower bound of 60.

## Sources fetched

Each page got one plain curl request with User-Agent `V3R1T4S-research (honest client; curl)`. There were
no retries, no cookies, no proxy and no followed redirects. Every request returned 200, with no challenge
page. Saved copies are in `novelty_ws/` in the panel folder.

| # | Source | URL | UTC fetch time | HTTP | sha256 of saved page | Value read for this cell |
|---|---|---|---|---|---|---|
| 1 | codetables.de cell (primary table) | http://www.codetables.de/BKLC/BKLC.php?q=2&n=175&k=25 | 2026-10-14T19:09:10Z | 200 | 248159ace5ed9e247b42b6e0690518c0a81e32fa2b2527d84c460f1bbe68307e | "Bounds on linear codes [175,25] over GF(2)": **lower bound: 60**, **upper bound: 72**. Construction "[175, 25, 60]" is a subcode of a shortened concatenated code (an algebraic-geometry [22, 7] code over GF(16) with the Reed-Muller [8, 4, 4] code), "last modified: 2001-01-30". Brouwer's table (as of 2007-02-13): Lb(175,25) = 60, Ub(175,25) = 72. |
| 2 | V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-14T19:09:26Z | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 | **No entry for this cell.** 53 rows. The only code family is constant-weight codes (Brouwer's A(n,d,w) tables). There are zero matches for "linear", "codetables", "Grassl", "BKLC" or "175". |
| 3 | V3R1T4S open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-14T19:09:31Z | 200 | e8957e2c6fff06214f21924a6513b63ee283e00dd3efd8544f6e1cf8af827227 | **No PR covers (2, 175, 25).** 28 open PRs on a single page (no Link header). See the PR section below. |
| 4 | MinT, Univ. Salzburg (secondary table), binary [175, 25] | http://mint.sbg.ac.at/query.php?i=c&de=1&b=2&s=175&n=25&d=&t= | 2026-10-14T19:16:25Z | 200 | 280fabd03a6f192fdb956a67ece16f031812ed634e7d057e6c7d398ab049bd54 | "Linear [175, 25, **60**]-Code over F2 — Constructive". Construction XX on length-127 BCH codes gives [178, 29, 59]; a parity bit gives [179, 29, 60], which is shortened to [175, 25, 60]. "Linear [175, 25, **74**]-Code over F2 — Upper bound on d". "Last update to the database: 2024-09-05". |

To find the MinT query format I made two navigation requests: the MinT home page http://mint.sbg.ac.at/
(2026-10-14T19:15:58Z, 200, sha256 34cc6813eb1eb77f23e4943b5c469e79511290a9199fc8eb70587cc9fb43ceb5) and
the codes query form http://mint.sbg.ac.at/query.php?i=c (2026-10-14T19:16:15Z, 200, sha256
ae2be6fe76ae340a2813999fcec6a33f2c3e8d936a02b2b1e69e100eea658258).

My codetables.de page is byte-identical to the author's recorded fetch: the same sha256, taken at
2026-10-14T19:00:20Z. The cell did not change between the two fetches.

## Which known codes would already reach this cell

A known binary linear [n', k', d'] code reaches [175, 25, 61] by standard means if some s shortenings and
p puncturings give n' - s - p <= 175 (pad with zero columns), k' - s >= 25 (then take a subcode) and
d' - p >= 61. Examples are any [n' <= 175, k' >= 25, d' >= 61], [176, 26, 61], [176, 25, 62] or
[179, 29, 61]. None of these steps can raise the dimension. I searched for any code in this range,
including shorter [n' < 175, 25, 61] codes that zero-padding would carry into this cell.

## LinCodeEvolve (arXiv:2609.37056), excluded by the success criterion

- "Evolving Towards Better Codes: LLM-Guided Search for High-Distance Binary Linear Codes", by Seddas,
  Shashkov, Viazovska and Abbe. Only one version exists, v1 of 29 Sep 2026. I read the abstract page and
  the HTML full text.
- Seven record codes: [172,21,66], [173,20,68], [176,21,68], [181,21,70], [184,21,72], [189,22,72] and
  [200,21,77].
- Its Table 3 lists 22 improved table entries, all derived from those seven codes. Their lengths run from
  171 to 201 and their dimension k is 20, 21 or 22. One entry is [175, 21, 67]. The only dimension-25 code
  in the paper is [50, 25, 10], which only meets the known bound.
- Every LinCodeEvolve code and derived entry has k <= 22. So none of them reaches or implies
  [175, 25, 61] by the steps above. The claimed parameters are not those of any of the seven codes.
- Limit: I saw only the object's file name, so I did not check whether the object was built with a
  LinCodeEvolve code as an ingredient in a step that raises the dimension (for example as the subcode in
  Construction X). That provenance question belongs to the criterion review.

## Pull-request search

I listed all 28 open PRs and scanned each title, body and branch name for code-table terms ("175",
"codetables", "BKLC", "linear code", "LinCode", "Grassl", "generator matrix", "minimum distance",
[1xx,25 patterns, n = 175, k = 25).

- The only other `codetables-binary-linear` claim is #142, a [173, 17, 72] code at a different cell. Its
  dimension of 17 cannot give a dimension-25 code by shortening, puncturing, extension, subcodes or
  zero-padding.
- The other "175" matches were substrings of a sha256 inside #142, of an energy value in #78
  (926576.1175606) and of "1175" in #8.
- #28 and #8 are constant-weight-code items. The rest cover hypersphere packing, the Thomson problem,
  degree-diameter graphs, matrix multiplication, stable matchings and harness fixes.
- No open PR covers (2, 175, 25) or a code with these parameters.

## Literature search, October 2024 to October 2026

What I covered:

- Web searches in standard and extended modes, and arXiv's own search sorted by announcement date.
- Query topics: "codetables"; "best known" binary linear codes; "record-breaking" codes; new quasi-cyclic
  binary codes with improved minimum distance; quasi-twisted codes (the Aydin group); LLM, AlphaEvolve and
  FunSearch code searches; new binary linear codes in DCC, IEEE Trans. IT, AMC and Cryptography and
  Communications.
- Exact-parameter strings: "175,25,61", "[175,25,60]", "[176,26", "[176,25", "[174,25", "[173,25",
  "176,25,61" and "176,26,61". None returned anything relevant.

What I found and checked:

- arXiv:2412.15551 (Yu, Zhu, Chen, Li, Zhang, Dec 2024): record binary codes from group codes. All have
  n <= 120, and the largest d is 42. Not relevant.
- arXiv:2607.22137 (Heng, Hu, Jul 2026): cyclic codes of length 2^s - 1 at rate near 1/2. Not relevant.
- arXiv:2606.02262: self-dual cyclic codes, dimension n/2. Not relevant.
- arXiv:2511.03323 (Chen, Sha, Nov 2025, revised May 2026): constacyclic codes of dimension about n/2.
  Not relevant.
- arXiv:2512.23872 (McMillon, Haymaker, Dec 2025): hierarchical quasi-cyclic codes with small
  parameters. They only meet known bounds.
- arXiv:2605.14603 (Yadav, Mondal, Sarma, May to Oct 2026): Z4 codes whose binary Gray images have
  dimension at most 8. I read the full text.
- arXiv:2509.03337 (Lin, Zhang, Chen, Liu, Sep 2025): restrictions on codeword weights. These are
  non-existence results, with no new codes.
- arXiv:2608.18664: abelian codes with records over F3 and F4 only.
- Also not relevant: arXiv:2504.11010 (cyclic codes of length 2^m - 1); an AIMS Mathematics 2026 paper
  on Goppa-code distance bounds; arXiv:2511.02864 (AlphaEvolve's 67 problems, none in coding theory);
  arXiv:2610.11609 (small nonlinear codes); arXiv:2607.19550 (constant-weight codes).

Result: no publication or preprint in the window claims a binary [175, 25] code with d >= 61. None claims
any code from which one follows by shortening, puncturing, subcodes or zero-padding.

## Verdict

- Live codetables.de lower bound: 60, with upper bound 72. MinT: 60, with upper bound 74.
- The best d known from all sources searched is 60.
- The claimed d = 61 is one more than 60. That is a strict improvement, not a tie, and it is within the
  upper bound of 72.
- No newer arXiv claim reaches 61. LinCodeEvolve covers only k = 20 to 22.
- novelty: PASS. d = 61 strictly beats everything found.

Limits:

- Search-engine indexing of arXiv for Sep and Oct 2026 may be incomplete. arXiv's own date-sorted search
  was used to make up for this.
- Not checked: Chen's legacy binary quasi-cyclic database (its codes feed codetables.de), closed or
  merged PRs (outside the kit's scope) and conference papers that are not indexed.
- MinT's database was last updated 2024-09-05.
- This review covers novelty only. It does not check the object's rank or minimum distance.

pass: true
