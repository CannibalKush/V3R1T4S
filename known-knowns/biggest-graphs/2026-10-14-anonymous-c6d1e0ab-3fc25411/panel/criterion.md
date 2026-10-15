# CRITERION skeptic report: panel dd-14-3 (degree-diameter-table, cell (Delta, D) = (14, 3))

Inputs read: the claim folder (`claim/`) and `claim.SHA256SUMS` only. All 9 listed files verify OK against
`claim.SHA256SUMS`, and the folder contains exactly those 9 files. The two object files
`claim/object/G_14_3_N1117.edges` and `claim/object/G_14_3_N1117.txt` are byte-identical
(sha256 `3fc25411941fa666946464317bc9672386a4923bcb01a24e2c42ec7239b8c3a4`).

Own checks (all under `criterion_ws/`, scripts in `criterion_ws/scripts/`, outputs in `criterion_ws/results/`):

- `indep_check.py` (my code, numpy): parses the edge list, builds a dense boolean adjacency matrix, checks
  symmetry/diagonal/labels/degrees, runs a plain BFS from every vertex (exact eccentricities), and separately
  grows distance balls by boolean matrix products. Independent of the author's bitset method.
- `extra_checks_v2.py` (my code): regularity, bipartiteness, triangle count (partial-win applicability), a
  null model (random simple graphs on 1117 vertices with maximum degree 14), and a tightness probe.
- Author's `ddcheck.c` compiled and run (cross-check only), with negative controls D=2 and Delta=13.
- Author's `verify_dd.py` run against a table JSON built from my own live fetch (cross-check only).
- One honest `curl` fetch of the live table, User-Agent `V3R1T4S-research (honest client; curl)`, no retries,
  saved under `criterion_ws/fetch/` with headers and SHA-256.

## Clause-by-clause

### (1) "Explicit adjacency list of a simple undirected graph G on N vertices."

Met. `claim/object/G_14_3_N1117.edges`: 7785 lines, every line two non-negative integers, 0 unparsable
lines, 0 blank/comment lines, 0 self-loops, 0 duplicate edges (exact or reversed), 7785 unique undirected
edges. Labels used are exactly 0..1116 (1117 distinct labels, none missing, no isolated labels), so N = 1117
is unambiguous. Adjacency matrix symmetric with zero diagonal. The file is a one-line-per-edge list rather
than a per-vertex adjacency list; it determines the adjacency list exactly and the bank's own verification
method ("load the graph with scipy.sparse") accepts this form, so I do not treat the format as a gap.

### (2) "Maximum degree <= Delta."

Met. Degree histogram {13: 68, 14: 1049}; minimum degree 13, maximum degree 14 = Delta; degree sum
15570 = 2 x 7785. Negative control: the author's C checker with Delta = 13 reports INVALID, as it should.

### (3) "G connected with diameter <= D, checked by all-pairs BFS, or by one BFS plus a machine-checked vertex-transitivity proof (explicit Cayley group and generators regenerating exactly the submitted edge set)."

Met by the all-pairs-BFS route (the graph is not regular, so the Cayley route is unavailable, see p2 below).
My per-vertex BFS from all 1117 sources: one component of size 1117 (connected); all 1117 eccentricities equal
3; radius 3, exact diameter 3. Ordered-pair distance histogram {0: 1117, 1: 15570, 2: 191342, 3: 1039660},
summing to 1247689 = 1117^2, i.e. zero ordered pairs at distance > 3. My boolean-matrix ball growth agrees:
ordered pairs within distance r = [1117, 16687, 208029, 1247689] for r = 0..3. The author's C bitset checker
gives the identical counts and VALID (exit 0); with D = 2 it reports 1039660 far pairs and INVALID (exit 1),
confirming the diameter is exactly 3, not less. (Diameter 2 is impossible anyway: the Moore bound for
(14, 2) is 197 < 1117.)

### (4) "N STRICTLY GREATER than the (Delta,D) entry of the live Comellas general-graph table at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html, re-fetched immediately before claiming (the table changes daily)."

Met at panel time. My single fetch: 2026-10-14T16:16:12Z, HTTP 200, 46849 bytes,
`Last-Modified: Wed, 14 Oct 2026 13:17:04 GMT`, page sha256
`aa4e747b76562bc78a8b2a38946d35a2266ef5352cca59e623c3ea77c8720d35`. In the row whose header cell is `14`,
the D = 3 column cell is
`<TD style="border: 1px solid black;" bgColor=#99EF99><A href="desc_g/desc_g3.html#143" target="_blank">&lowast;  1 116</A> </TD>`,
i.e. N = 1116 (thousands-separated). 1117 > 1116: strict, margin +1. The page's own legend says
"Entries with * are Cayley graphs or a former entry is a Cayley graph", so the asterisk is a Cayley marker,
not an optimality marker.

Hidden-quantifier notes on this clause:
- The author's `table-record/` records a fetch at 2026-10-14T07:37:19Z with page sha256 `69e48062...`.
  That hash differs from my fetch, and the server's Last-Modified (13:17:04 GMT today) shows the page
  changed between the author's fetch and mine. The (14, 3) cell is still 1116 in my fetch, and the page's
  "Latest Updates" line lists (14, 3) last under "July 2026" (absent from the August and September 2026
  lists), so (14, 3) is not what changed. I cannot verify the author's recorded hash (the earlier page
  version is not retrievable); it is immaterial because the clause is decided on the live value.
- "Re-fetched immediately before claiming": the author's record file is dated 6 minutes after its recorded
  fetch time (file mtime 01:43 MDT = 07:43Z vs fetch 07:37:19Z), which is consistent with the clause, though
  I can only confirm the live value as of my own fetch.
- Subsumption was checked against the live table only. The author's record says the (14, 3) cell has no
  TROPHY_CASE entry; that file is outside my permitted reads, so that statement is unverified by me.

### (5) "N <= Moore bound; boldface (proven-optimal) entries cannot be beaten, so beating one signals a bug."

Met. Moore bound M(14, 3) = 1 + 14 + 14*13 + 14*13^2 = 2563; 1117 <= 2563 (ratio 0.436). Boldface: the live
page wraps optimal entries in `<B>...</B>`; the only boldface cells on the fetched page are (3,2)=10,
(3,3)=20, (3,4)=38, (4,2)=15, (5,2)=24, (6,2)=32 and (7,2)=50. The (14, 3) cell carries no `<B>` tag (raw
markup quoted under clause 4), so the (14, 3) entry is NOT a proven-optimal (boldface) entry and beating it
signals no bug.

## Partial wins considered

- `p1` (overtaken snapshot): not needed and not applicable. The live entry at panel time is 1116 < 1117;
  nothing has overtaken the claim.
- `p2` (special-class table): not applicable and not claimed. The graph is not regular (68 vertices of
  degree 13), hence not Cayley, circulant or vertex-transitive; it is not bipartite (568 triangles). No
  bipartite, Cayley or circulant table applies.

## Null model and tightness

- Null model: three random simple graphs on 1117 vertices with maximum degree 14 (greedy stub matching,
  7818-7819 edges, minimum degree 13-14) all have diameter 4, with about 120,000 ordered pairs at distance
  > 3 each; the claimed graph has 0. Diameter 3 at this order is therefore not a null-model artefact, and
  diameter 2 is impossible by the Moore bound 197.
- Tightness (informational, not a clause): a greedy probe attaching an 1118th vertex to at most 14 of the 68
  degree-13 vertices covers at most 1071/1117 vertices within radius 2, so no trivial +1 extension was found.

## Other observations (not clause failures)

- `REPRODUCE.md` says to run `verify-it-yourself/run_checks.sh`, but as shipped it expects an `INDEX.csv` at
  the package root and a `verify-it-yourself/live_general_cells.json`, neither of which is in the claim
  folder; it fails at its sha step with an empty expected hash. The underlying `verify_dd.py` and `ddcheck.c`
  run standalone and agree with my independent results (verify_dd.py with my live value: valid true,
  beats_record true, margin 1; with D=2: valid false).
- The claim's `table-record/README.md` refers to fetches "by the independent NOVELTY panelist"; treated as
  data, not verified by me.

## Verdict

PASS. Every numbered clause (1)-(5) of the full success criterion is met on my own independent evidence: a
simple graph on 1117 vertices, maximum degree 14, connected with exact diameter 3 by all-pairs BFS, 1117 at
most the Moore bound 2563, and 1117 strictly greater than the live, non-boldface (14, 3) entry 1116 fetched
once at 2026-10-14T16:16:12Z. The win is a genuine +1 over the live table and is not subsumed by any entry on
it; no partial win is needed.

confirmed_scope: claim/object/G_14_3_N1117.edges (sha256 3fc25411941fa666946464317bc9672386a4923bcb01a24e2c42ec7239b8c3a4) is a simple undirected graph on 1117 vertices with maximum degree 14 (68 vertices of degree 13, 1049 of degree 14), connected with exact diameter 3 by independent all-pairs BFS, of order at most the Moore bound 2563, and its order 1117 strictly exceeds the non-boldface (14,3) entry 1116 of the live Comellas general-graph table as fetched once at 2026-10-14T16:16:12Z (page sha256 aa4e747b76562bc78a8b2a38946d35a2266ef5352cca59e623c3ea77c8720d35, Last-Modified 2026-10-14 13:17:04 GMT).
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
