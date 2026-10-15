# Degree-diameter graph (14, 3) on 1117 vertices

## What

claim/object/G_14_3_N1117.edges (sha256 3fc25411941fa666946464317bc9672386a4923bcb01a24e2c42ec7239b8c3a4) is a simple undirected graph on 1117 vertices with maximum degree 14 (68 vertices of degree 13, 1049 of degree 14), connected with exact diameter 3 by independent all-pairs BFS, of order at most the Moore bound 2563, and its order 1117 strictly exceeds the non-boldface (14,3) entry 1116 of the live Comellas general-graph table as fetched once at 2026-10-14T16:16:12Z (page sha256 aa4e747b76562bc78a8b2a38946d35a2266ef5352cca59e623c3ea77c8720d35, Last-Modified 2026-10-14 13:17:04 GMT).

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/G_14_3_N1117.edges`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 3 seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Comellas, *The degree/diameter problem for general graphs* (table; page Last-Modified 2026-10-14 13:17:04 GMT) | (Delta, D) = (14, 3) | 1116, not boldface (not proved optimal) | 1117 | https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html | 2026-10-14T16:14:01Z |
| Comellas, D = 3 description page | Dhar_1116 | order 1116, D. Yugeswardeenoo, 7 October 2026 | 1117 | https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g3.html | 2026-10-14T16:14:34Z |
| V3R1T4S `TROPHY_CASE.md` and open pull requests | (14, 3) | no entry | 1117 | https://github.com/elder-plinius/V3R1T4S | 2026-10-14T16:14:53Z |
| Moore bound 1 + 14 + 14·13 + 14·13^2 | (14, 3) | 2563 | 1117 | | |

The table changes often; it was edited on the day of this claim. Re-fetch it before relying on the comparison. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed. The Moore bound is 2563.
- No symmetry is claimed. The graph is not claimed to be vertex-transitive or a Cayley graph.
- The margin is one vertex. The graph is the record graph Dhar_1116 with one vertex added and some edges changed, so most of its structure is the earlier authors' work.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Dharunish Yugeswardeenoo**, the (14, 3) graph Dhar_1116 (7 October 2026). It is listed on the Comellas D = 3 page and was the starting graph here: https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g3.html. Most edges of this graph are his. Please credit him whenever this graph is used.
- **R. Rajiv**, the 1088-vertex (14, 3) graph that Dhar_1116 extends, as that page states.
- **Francesc Comellas**, the degree/diameter table compared against: https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html.
- Contributor credit: `anonymous-c6d1e0ab`.
