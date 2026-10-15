# Novelty skeptic report: g(7,3) = 12 (target sunflower-free-capacity-lower-bound, partial win p2)

context: Claude Code subagent (Opus 5.5), fresh context

Reviewer role: NOVELTY skeptic, three-skeptic panel. Inputs read: the claim folder (CLAIM.md, INDEX.csv, table-record/README.md, object file names) and claim.SHA256SUMS. Nothing else local was read.

Access discipline: curl, one plain request per URL, User-Agent `V3R1T4S-research (honest client; curl)`, no retries, no redirect following by curl. 25 fetches in total (the cap). Pages are saved in the panel's novelty_ws folder, with FETCHLOG.tsv beside them. Two web searches (search engine, not fetches) were used only to locate the Polymath10 wiki and the Abbott-Exoo paper.

## What the claimed quantity is, and its reformulations

g(n, r) is the largest family of r-subsets of a FIXED ground set [n] with no 3-sunflower; the empty core counts. Here n = 7, r = 3.

- **Unrestricted ground set.** For any n, g(n,3) is at most f(3,3) = 20, the Erdos-Rado sunflower number with no limit on the ground set. So g(n,3) is bounded and reaches 20 once n is large enough. Published values of f(r,3) do not give g(7,3). They give only the ceiling of 20.
- **Complement view.** Take complements in [7]. A 3-sunflower among 3-sets becomes three 4-subsets of [7] whose pairwise unions are all equal. So n - r = 4. That condition forbids three different configurations at once, with common unions of size 5, 6 and 7. None of them is a single standard Turan problem.
  - n - r = 2 would be Mantel's theorem.
  - n - r = 3 is ex(N, K4-), the 3-graph with three edges on four vertices. Markstrom's table covers that case, so it gives g(N, N-3). For example, it gives g(7,4) = ex(7, K4-) = 15 and g(6,3) = ex(6, K4-) = 10.
  - It does NOT give g(7,3), because that case has n - r = 4.
- **Other near neighbours that are not equivalent.** These are different quantities with different extremal values, and none of them is an exact reformulation of g(7,3):
  - Duke-Erdos problems, where the core size is fixed.
  - Weak Delta-systems, where only the intersection SIZES must be equal.
  - Sunflower-free families on [n] with mixed set sizes.

## Sources

1. OEIS, search by the claimed r=3 column `10,12,12,14,16,16,20`.
   - URL: https://oeis.org/search?q=10,12,12,14,16,16,20&fmt=json
   - Fetched 2026-10-15T15:33:44Z, HTTP 200, sha256 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b
   - Body: `null` (no matching sequence).
2. OEIS, search `sunflower`.
   - URL: https://oeis.org/search?q=sunflower&fmt=json
   - Fetched 2026-10-15T15:33:44Z, HTTP 200, sha256 77e3d20ee32853a3d9d8e5ce3b59ecbcc842ac19ce45cae3d0d0ea2dcf2b0a93
   - Four hits:
     - A236397, "Weight of the largest-weight sunflower-free set of width n." (data 1,2,4,8,20,40,96,224)
     - A332077, "Square array of sunflower numbers Sun(m,n) = minimal number of distinct sets of cardinality ≤ m such that there is a sunflower with at least n sets ..."
     - A266696 and A399802, both unrelated.
   - A236397 and A332077 tabulate UNRESTRICTED-ground-set quantities (f(r,3) style; f(3,3) = 20 appears as a term). That is a different quantity from the fixed-n value g(7,3), and neither has a fixed-n row or column.
3. OEIS, search `"delta-system"`.
   - URL: https://oeis.org/search?q=%22delta-system%22&fmt=json
   - Fetched 2026-10-15T15:33:44Z, HTTP 200, sha256 e9ae1d6ef9427d19e16d3632d4cbca335b3ed27793bf39dd272b8d906d6da699
   - Hits: A266696 and A332077 only. There is no fixed-n entry.
4. OEIS, search `"pairwise equal intersections"`.
   - URL: https://oeis.org/search?q=%22pairwise+equal+intersections%22&fmt=json
   - Fetched 2026-10-15T15:36:34Z, HTTP 200, sha256 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b
   - Body: `null` (no hit).
5. Klas Markstrom, 3-uniform Turan hypergraphs.
   - URL: http://abel.math.umu.se/~klasm/Data/hypergraphs/turan3.html
   - Fetched 2026-10-15T15:33:45Z, HTTP 200, sha256 abc2fd8d0142a7c993eaf5a635eb1f9c95035d48ed4904d1f9141ba70538b26f
   - Quote: "H=K4- This is the unique hypergraph obtained by removing an edge from the 3-uniform K4."
   - Table cells (N, ex(H,N), number of Turan graphs): 6 10 1; 7 15 1; 8 22 5; 9 32 6; 10 44 43; 11 60 1; 12 80 1; 13 101 1; ... 19 322 1; 20 ?.
   - Other tables on the page: K4 (N=4: 3), K5 (N=5: 9), K6 (N=6: 19), and a 2-colourable K4- variant.
   - Relevance: this is the n - r = 3 case. It fixes g(N, N-3) and is consistent with g(6,3) = 10, but it says nothing about n - r = 4. There is no 4-uniform table on this page.
6. arXiv export API query 1: all:sunflower AND all:uniform AND all:exact, newest first.
   - The http URL returned 301 at 2026-10-15T15:34:12Z, with an empty body. I followed the redirect once at the https URL: https://export.arxiv.org/api/query?search_query=all:sunflower+AND+all:uniform+AND+all:exact&max_results=50&sortBy=submittedDate&sortOrder=descending
   - Fetched 2026-10-15T15:34:34Z, HTTP 200, sha256 7427a5926637c68d94b1c4b7b76befea254b4f50a67d12724697f840fe883d57
   - totalResults 4. Within the last 24 months:
     - arXiv:2511.17142 (Kupavskii-Noskov, Nov 2025), "Exact results and the structure of extremal families for the Duke--Erdos forbidden sunflower problem". See source 11.
     - arXiv:2410.23611, "Focal-free uniform hypergraphs and codes". A different notion.
   - The other two hits are unrelated (coloring channels; spectral radius).
7. arXiv query 2: all:sunflower AND all:SAT.
   - The http URL returned 301 at 15:34:15Z. Followed once at https: https://export.arxiv.org/api/query?search_query=all:sunflower+AND+all:SAT&max_results=50&sortBy=submittedDate&sortOrder=descending
   - Fetched 2026-10-15T15:34:38Z, HTTP 200, sha256 f338efa4ca20c42b2de8d9c13cceb11c76f1a8550a71d04b73843cfb69415e80
   - totalResults 5. All are SAT-complexity papers (2009-2024). None computes sunflower values.
8. arXiv query 3: all:"delta system" AND all:"three sets".
   - The http URL returned 301 at 15:34:18Z. Followed once at https: https://export.arxiv.org/api/query?search_query=all:%22delta+system%22+AND+all:%22three+sets%22&max_results=50&sortBy=submittedDate&sortOrder=descending
   - Fetched 2026-10-15T15:34:41Z, HTTP 200, sha256 901fb94467fc327726fe521c0ec5d4eae90344a6a8a0f903be714cbc7ae5cb0e
   - totalResults 0.
9. arXiv query 4: all:sunflower-free AND all:"small cases".
   - The http URL returned 301 at 15:34:22Z. Followed once at https: https://export.arxiv.org/api/query?search_query=all:sunflower-free+AND+all:%22small+cases%22&max_results=50&sortBy=submittedDate&sortOrder=descending
   - Fetched 2026-10-15T15:34:46Z, HTTP 200, sha256 a03bb33220ca67f93f96565847ca324a2629f45c30a756452178bc46a1e3f25e
   - totalResults 0.
   - Note on the four arXiv queries: each one was issued once. The only extra request per query was the single follow of the server's own http-to-https redirect. No query was repeated after a block.
10. arXiv:2609.06175 abstract.
    - URL: https://arxiv.org/abs/2609.06175
    - Fetched 2026-10-15T15:34:25Z, HTTP 200, sha256 a7b82aac7c91bd0b086e73252a4f022e1e504e4d7566e1b5f707e0bdc8085fb8
    - Axante, Budala, Chitic, Dumitru, Nacu, "Sunflower-Free Uniform Families: Recursive Constructions and Explicit Bounds", 2026-09-05.
    - Quote: "Let f(w,k) be the maximum size of a w-uniform family containing no sunflower with k petals. ... Our results give 39≤f(3,4)≤49, f(3,5)≤146, 153≤f(3,6)≤255, 259≤f(3,7)≤474, and 54≤f(4,3)≤83. In addition, we prove that the maximum size of an intersecting 4-uniform family containing no sunflower with three petals is 27."
    - All of these values are on an unrestricted ground set. The abstract gives no fixed-n value and nothing for g(7,3).
11. arXiv:2511.17142 abstract.
    - URL: https://arxiv.org/abs/2511.17142
    - Fetched 2026-10-15T15:35:53Z, HTTP 200, sha256 e4ef7994f885126dc048e85cd7194b16ef18888c7e18c6f9da552e94f96ef88f
    - Quote: "What is the largest size of a family F subset of ([n] choose k) that does not contain a sunflower with s petals and core of size exactly t - 1? ... we answer this question exactly for t=2, odd s and k≥5, provided n is large enough."
    - This is a fixed-core-size problem, for k at least 5 and large n. It is a different quantity and gives no small-n value for k = 3.
12. Polymath10 announcement, used to locate the wiki.
    - URL: https://polymathprojects.org/2015/11/06/polymath10-is-now-open/
    - Fetched 2026-10-15T15:35:23Z, HTTP 200, sha256 90e6978a6c8b9bc56f17ffd1d002fcb5bb143bc5c5d625fccb21a888470c9a47
    - It links the wiki page "The_Erdos-Rado_sunflower_lemma" on michaelnielsen.org/polymath1.
13. Polymath wiki, The Erdos-Rado sunflower lemma.
    - First request: http://michaelnielsen.org/polymath1/index.php?title=The_Erdos-Rado_sunflower_lemma. Fetched 2026-10-15T15:35:29Z, HTTP 301 (moved to https), sha256 6711c70ead6a8046ff5242bf2379c1335e81a7f0a9d9147d95bda82ba7c03d3b.
    - Redirect followed once: https://michaelnielsen.org/polymath1/index.php?title=The_Erdos-Rado_sunflower_lemma. Fetched 2026-10-15T15:35:37Z, HTTP 404 ("The requested URL was not found on this server."), sha256 d5a89e26beae0bc03ad18a0b0d1d3d75f87c32047879d25da11970cb5c4662a3.
    - Archive attempt 1: https://web.archive.org/web/2017/http://michaelnielsen.org/polymath1/index.php?title=The_Erdos-Rado_sunflower_lemma. Fetched 2026-10-15T15:35:46Z, HTTP 302 with an empty body, not followed. sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty).
    - Archive attempt 2: https://archive.org/wayback/available?url=michaelnielsen.org/polymath1/index.php%3Ftitle%3DThe_Erdos-Rado_sunflower_lemma. Fetched 2026-10-15T15:36:14Z, HTTP 503 ("Internet Archive services are temporarily offline."), sha256 e084d527921708642a79724e9f0210da659bbc0905c6ce9a3a1f416e4628091c. Not retried.
    - Result: the wiki contents could not be read (unresolved).
14. Abbott and Exoo, "On set systems not containing delta systems", Graphs and Combinatorics 8 (1992) 1-9, DOI 10.1007/BF01271703.
    - URL: https://link.springer.com/article/10.1007/BF01271703
    - Fetched 2026-10-15T15:35:49Z, HTTP 303 with an empty body, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855. Not followed.
    - Search-snippet abstract, which is not a fetch: "Some constructions of systems of n-sets not containing Delta(k) systems are given. The constructions were produced by both analytical and computational methods." These are constructions on an unrestricted ground set. I could not read the full text (unresolved).
15. Abbott-Hanson-Sauer 1972, "Intersection theorems for systems of sets" (J. Combin. Theory Ser. A 12).
    - Tried https://doi.org/10.1016/0097-3165(72)90103-3. Fetched 2026-10-15T15:36:34Z, HTTP 302 to an Elsevier linkinghub record, sha256 246626bcfb1aefd1064cd34e6c8729f6fed2df25613a19f0d53a567aea1cdf49.
    - I did not follow the redirect (the fetch cap was reached). The DOI was taken from memory and was not confirmed to be the AHS paper.
    - Also fetched the Cambridge Core page with the same title: https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/intersection-theorems-for-systems-of-sets/9C7C0F7282A73F9124ABAE5C1813E877. Fetched 2026-10-15T15:35:49Z, HTTP 200, sha256 f31af8c01eaf91dddfab4a804163fa744f7b69f23d3cec1c7486c36a21e56dc4.
    - That page is a different paper with the same title, in the Canadian Mathematical Bulletin. Its abstract says: "Denote by phi(n, k) the least positive integer such that if F is any family of more than phi(n, k) sets, each set with n elements, then some k members of F have pairwise the same intersection. In this paper we obtain a new asymptotic upper bound for phi(n, k), k fixed, n approaching infinity."
    - That is unrestricted-ground-set and asymptotic. It gives no fixed-n value.
16. V3R1T4S TROPHY_CASE.md.
    - URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
    - Fetched 2026-10-15T15:35:48Z, HTTP 200, sha256 b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412
    - A case-insensitive search for sunflower, delta, Erdos-Rado and g(7 found no match. There is no sunflower trophy.
17. V3R1T4S open pull requests.
    - URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
    - Fetched 2026-10-15T15:35:48Z, HTTP 200, sha256 48c623ce3a79aaba234d4ce2137c013a3aa8385426a61d6e53054d64384ee511
    - 66 open PRs (fewer than 100, so the list is complete). No title or body mentions sunflower, delta-system, g(7, 49a or C_49. There is no competing or prior sunflower claim.

## Assessment

- No source fetched publishes or tabulates g(7,3).
- No source fetched gives its exact complement reformulation: 4-subsets of [7], no three with pairwise equal unions.
- The general bounds I know do not force the value 12:
  - The Erdos-Rado ceiling f(3,3) = 20 is not tight at n = 7.
  - The pair-codegree bound, that a pair lies in at most 2 members, gives only 2*21/3 = 14.
- Markstrom's table settles only the n - r = 3 diagonal. The neighbouring published values (Duke-Erdos fixed core, unrestricted f(r,k), weak Delta-systems) are for different quantities.
- Residual risk: three sources could not be read in full:
  - the Polymath10 wiki (404, and the archive returned 503);
  - Abbott-Exoo 1992 (303 paywall redirect);
  - Abbott-Hanson-Sauer 1972 (302, not followed).
  - Of these, the 1992 paper used computer search and could in principle list small fixed-n cases. Its abstract describes only constructions on an unrestricted ground set.
- This is a p2 exact-value claim, not a table record, so "strictly beats" here means "not previously known". No equal or prior value was found, so there is no tie.

unresolved: Polymath wiki page The_Erdos-Rado_sunflower_lemma returned 404, its Internet Archive copy returned 302 and then 503 on the availability API (not retried); Abbott-Exoo 1992 on link.springer.com returned 303 (paywall/cookie redirect, not followed); Abbott-Hanson-Sauer 1972 DOI returned 302 to Elsevier (not followed, fetch cap reached, DOI not confirmed); full texts of these three were not checked for fixed-n tables.

verdict: NOT FOUND. No publication or tabulation of g(7,3) = 12, or of an exactly equivalent reformulation, was found in OEIS, Markstrom's Turan tables, arXiv (last 24 months, including arXiv:2609.06175 and arXiv:2511.17142), the V3R1T4S trophy case or its open PRs.

pass: true
