# Independent reproduction

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

## Definition and criteria checked

The graph definition and exact numerical claim, quoted from `CLAIM.md`:

> object/G_14_3_N1117.edges is a simple undirected graph on 1117 vertices with maximum degree 14 and diameter 3, strictly more vertices than the live Comellas table entry for (Delta, D) = (14, 3).

The bank definition, quoted:

> For maximum degree Δ and diameter D, find a graph with more vertices than the current entry in the Comellas degree-diameter table. The table covers degree up to 20 and diameter up to 10.

Every clause of the success criterion, quoted (including the externally dependent clauses to make the scope explicit):

> (1) Explicit adjacency list of a simple undirected graph G on N vertices. (2) Maximum degree <= Delta. (3) G connected with diameter <= D, checked by all-pairs BFS, or by one BFS plus a machine-checked vertex-transitivity proof (explicit Cayley group and generators regenerating exactly the submitted edge set). (4) N STRICTLY GREATER than the (Delta,D) entry of the live Comellas general-graph table at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html, re-fetched immediately before claiming (the table changes daily). (5) N <= Moore bound; boldface (proven-optimal) entries cannot be beaten, so beating one signals a bug.

The stated verification method, quoted:

> Load the graph with scipy.sparse. Assert it is symmetric with no loops and no multi-edges, and check the degree array. Run BFS from every vertex: multi-source frontier bitsets in numpy work up to about 2e5 vertices. For Cayley graphs, regenerate the edge set from the stated group and generators, check it equals the submitted list, and then run one BFS. Compare N with the live HTML table. Also confirm N is at most the Moore bound.

Only files in this folder were inspected. There was no network access. I read `CLAIM.md`, the submitted edge list and saved table metadata, wrote `skeptic/check.py`, and completed its first exhaustive run before inspecting `REPRODUCE.md` or anything in `verify-it-yourself/`. The checker uses Python's standard library and imports no author code. It did not require scipy, numpy, mpmath or python-flint.

## Properties and proof steps

1. **Explicit object, vertex count, simplicity and undirectedness.** The saved object is an edge list, an explicit representation of the graph. I required every saved row to contain two nonnegative integer endpoints in `0..1116`, required every one of those 1117 labels to occur, normalized each edge to detect duplicates in either orientation, and rejected loops. I reconstructed adjacency in both directions and checked symmetry. There are 7785 unique undirected edges. This reconstructs an adjacency list without relying on a claimed Cayley representation or on construction history.
2. **Degree.** I counted each reconstructed neighbor set. There are 68 vertices of degree 13 and 1049 of degree 14. Thus the maximum is exactly 14 and satisfies the bound. The handshake check is `68*13 + 1049*14 = 15570 = 2*7785`.
3. **Connectivity and exact diameter, exhaustively.** I ran an uncapped queue BFS independently from every one of the 1117 vertices. The source starts at distance zero. When BFS first discovers a neighbor, its assigned distance is its predecessor's distance plus one. FIFO processing explores distance layers in increasing order; a shorter path would have discovered that vertex from an earlier layer. Induction over those layers therefore gives shortest distances. Each run reached all 1117 vertices and had eccentricity 3. All `1117*1116/2 = 623286` unordered pairs were counted, with distances 1, 2 and 3 occurring 7785, 95671 and 519830 times respectively. No pair was omitted or sampled. The maximum of all these shortest distances is the diameter, exactly 3. Pair `(0,65)` has shortest distance 3 and the BFS witness path is `0,512,513,65`. The saved distance-matrix digest covers all ordered distances, including the diagonal. This direct exhaustive computation makes a vertex-transitivity proof unnecessary.
4. **Moore bound, re-derived.** Starting at any vertex, distance layer 1 contains at most 14 vertices. Each later layer has at most 13 new vertices per vertex of the preceding layer, because one incident edge leads back toward the root; collisions only reduce that count. Connectivity and diameter at most 3 put every vertex in layers 0 through 3, so `N <= 1 + 14 + 14*13 + 14*13^2 = 1 + 14 + 182 + 2366 = 2563`. The submitted order 1117 satisfies this bound.
5. **Saved record arithmetic and object integrity.** The general-graph row in `table-record/README.md` states `(14,3)=1116`, not boldface. I checked `1117 > 1116`, with difference 1. The target, cell, order, recorded table value and fetch time in `INDEX.csv` agree with the package metadata, and its object SHA-256 agrees with an independently computed digest. No fetched HTML is packaged, so its page hash, boldface status, actual fetch event, and live currency cannot be independently authenticated from the saved metadata. I do not make a table-currency or novelty judgment; that is the other skeptic's task. Neither partial win `p1` nor `p2` is invoked by this claim.
6. **Determinism and author comparison.** Two independent runs produced byte-identical complete output. Two runs of the author's graph checker also produced byte-identical output. The author and independent checker agree on vertex and edge counts, degree histogram, maximum degree, exact diameter and Moore bound. The author's suite checked the indexed hash and rejected its corrupted graph control. The first suite launch emitted macOS launcher diagnostics on stderr; the full captured output below preserves them. These diagnostics are environmental and do not affect the graph result; the direct checker receipts repeat exactly.

The original author's `REPRODUCE.md` refers to `verify-it-yourself/RECEIPTS.md`, `how-we-built-it/sa2_opt.c`, `how-we-built-it/PREREG.md`, and an external starting adjacency list that are absent from this folder. Its optimizer seed, timing and historical construction cannot be reproduced here. They supply no proof step needed for this graph claim: the submitted object is present, and every claimed graph property is independently verified directly. I did not rerun a construction search or use a sample as an exhaustive result.

This filesystem treats the requested `reproduce.md` and the author's `REPRODUCE.md` as the same filename. Writing the report replaced that original path; the author's complete original text, as read before replacement, is preserved in `skeptic/author-REPRODUCE.md`. The report's on-disk filename is now the requested lowercase `reproduce.md`.

## Exact commands and captured output

All commands were executed from this folder. The independent first run, repeat run, and byte comparison all exited 0:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1 && cmp skeptic/output.txt skeptic/output-repeat.txt
```

Full actual first-run output, inserted directly from `skeptic/output.txt`:

```text
Independent checker: simple undirected graph; exhaustive all-pairs BFS
Parameters: N=1117, Delta=14, D=3
PASS: object exists: object/G_14_3_N1117.edges
Object SHA-256: 3fc25411941fa666946464317bc9672386a4923bcb01a24e2c42ec7239b8c3a4
Saved rows: 7785; distinct non-loop undirected edges: 7785
Distinct endpoint labels: 1117
PASS: two nonnegative integer endpoints per row
PASS: all endpoint labels in 0..1116
PASS: no loops
PASS: no repeated undirected edges
PASS: all 1117 declared vertices present as endpoint labels
PASS: symmetric reconstructed adjacency
Degree histogram (degree: vertices): {13: 68, 14: 1049}
Minimum degree: 13; maximum degree: 14
PASS: maximum degree <= 14
PASS: one-sentence claim: maximum degree exactly 14
PASS: degree sum equals twice edge count
BFS sources completed: 1117 of 1117 (all vertices)
Reachable-vertex-count histogram: {1117: 1117}
Eccentricity histogram: {3: 1117}
Unordered-pair shortest-distance histogram: {1: 7785, 2: 95671, 3: 519830}
Unordered pairs checked: 623286
Complete distance matrix SHA-256 (comma-separated integer rows): e8834e9eb3e51c254d03ed46c289dea26fe16b5be3e420e0baa1f9a1facb1d9f
PASS: every unordered vertex pair examined
PASS: connected (all vertices reached from every source)
Diameter: 3
Maximum finite distance witness: pair=(0, 65), shortest path=[0, 512, 513, 65]
Unordered pairs unreachable or distance > 3: 0
PASS: diameter <= 3
PASS: one-sentence claim: diameter exactly 3
Moore bound derivation: 1 + 14 + 182 + 2366 = 2563
PASS: 1117 <= Moore bound
PASS: saved table metadata exists: table-record/README.md
PASS: exactly one saved (14, 3) cell value
Saved metadata table value: 1116; claimed order: 1117; difference: 1
PASS: 1117 strictly greater than saved metadata cell
Scope: fetched HTML is absent; source hashes, boldface, freshness, and novelty cannot be independently established from metadata.
Scope: table currency and novelty are reserved for the separate skeptic; no network used.
Independent saved-graph verdict: PASS
Failed checks: 0
```

The author's direct checker and its repeat comparison both exited 0:

```sh
python3 verify-it-yourself/check_dd.py object/G_14_3_N1117.edges --delta 14 --diameter 3 --expect-n 1117 > skeptic/author-output.txt 2>&1
python3 verify-it-yourself/check_dd.py object/G_14_3_N1117.edges --delta 14 --diameter 3 --expect-n 1117 > skeptic/author-output-repeat.txt 2>&1 && cmp skeptic/author-output.txt skeptic/author-output-repeat.txt
```

Full actual output, inserted directly from `skeptic/author-output.txt`:

```text
N=1117 edges=7785 degree histogram=[(13, 68), (14, 1049)] max degree=14 exact diameter=3 (BFS from all 1117 vertices) Moore bound=2563
PASS (Delta,D)=(14,3) N=1117 max_degree=14 diameter=3
```

The author's suite exited 0. `TMPDIR` keeps its temporary artifacts inside this folder:

```sh
TMPDIR=skeptic sh verify-it-yourself/run_checks.sh > skeptic/author-suite-output.txt 2>&1
```

Full actual output, inserted directly from `skeptic/author-suite-output.txt`:

```text
sha256 matches INDEX.csv (3fc25411941fa666946464317bc9672386a4923bcb01a24e2c42ec7239b8c3a4)
== check_dd.py on object/G_14_3_N1117.edges
2026-10-14 10:43:58.366 xcodebuild[65416:69760793]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-14 10:44:01.097 xcodebuild[65416:69760791] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
N=1117 edges=7785 degree histogram=[(13, 68), (14, 1049)] max degree=14 exact diameter=3 (BFS from all 1117 vertices) Moore bound=2563
PASS (Delta,D)=(14,3) N=1117 max_degree=14 diameter=3
== negative control: a corrupted copy must FAIL
negative control rejected as expected (FAIL an isolated vertex (or a gap in the vertex numbering))
ALL CHECKS PASS
```

The comparison and report assembly command:

```sh
python3 skeptic/write_report.py
```

Its actual comparison output (also saved as `skeptic/comparison-output.txt`):

```text
PASS: independent checker reports PASS with zero failed checks
PASS: independent rerun is byte-for-byte identical
PASS: author checker rerun is byte-for-byte identical
PASS: INDEX.csv object SHA-256 matches saved object
PASS: INDEX.csv target and cell match CLAIM.md
PASS: INDEX.csv order, table value and fetch time match saved metadata
PASS: author suite reports ALL CHECKS PASS
PASS: independent and author order, edges, degree histogram, maximum degree, diameter and Moore bound agree
```

## Verdict

There is no mismatch in any checked graph property, claimed numerical value, saved object hash, or repeated checker result. Every graph check is exhaustive. This reproduction verdict concerns the explicit saved graph and independently checkable package arithmetic; it does not certify table currency, novelty, or absent construction history.

pass: true
