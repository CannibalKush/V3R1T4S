# (13,4), N = 6 630: where the graph comes from

The graph is the end of a local-search chain, not a closed-form construction; the exhaustive all-pairs BFS of
`../../graphs/G_13_4_n6630.edges` is the proof. The search code that produced it is in `search/` (see below); its
first step, the attempt that produced the near-miss and the final step were rerun for this release and reproduce the
original files exactly.

1. **Seed.** Rishabh Rajiv's (13,4) graph Q9(T4)++ on 6 611 vertices (Zenodo 10.5281/zenodo.23052995, CC BY 4.0), a
   compound of generalized-quadrangle incidence graphs with his surgery, formerly the table entry (13,4).
2. **Agent chain (2026-10-04 to 2026-10-08).** Repeated "slack" vertex insertion (a new vertex joined to vertices with
   free degree) followed by simulated annealing over 2-switches and single-edge rewires, minimising the number of
   pairs at distance > 4, reached a valid 6 629-vertex graph and then, with one more insertion, the near-miss
   `near_miss_N6630_cost2.edges`: 6 630 vertices, maximum degree 13, exactly 2 unordered pairs at distance 5.
   (Its first-line comment was shortened for this release; the edge lines are unchanged.)
3. **Closing the near-miss (2026-10-08).** Resuming the annealer from the near-miss at low temperature found a
   5-edge switch (`G_13_4_n6630.diff_vs_near_miss.txt`) that leaves no pair at distance > 4.

```sh
python3 apply_diff.py near_miss_N6630_cost2.edges G_13_4_n6630.diff_vs_near_miss.txt ../../graphs/G_13_4_n6630.edges
#   -> EDGE SETS IDENTICAL
../../verify-it-yourself/ddcheck near_miss_N6630_cost2.edges 13 4 4     # control: 4 ordered far pairs, INVALID
```
The table entry it exceeds, 6 615, is Dharunish Yugeswardeenoo's (Oct 2026).

*Credits:* Rishabh Rajiv for the seed graph and the compound/surgery idea; Gómez and Fiol for the compound-graph
family; our agents for the insertion/annealing chain.

## The search code (`search/`)

| file | role |
|---|---|
| `ddlib.py` | graph arrays, exact bitset count of pairs at distance > D, BFS, edge-list loaders |
| `sa2.py` | `sa2_run`: simulated annealing with sound early rejection (moves: pure addition between free vertices near a far pair, a targeted rewire that adds a shortcut for a far pair and frees the slots it needs, random 2-switch; cost = number of unordered pairs at distance > D) |
| `insert.py` | `initial_insert`: the "slack" warm start for a new vertex; `verify_independent`: scipy all-pairs check |
| `prune.py` | removes edges whose deletion keeps the diameter <= D (frees degree for the next insertion) |
| `decode_sage.py` | reads the sparse6 string of Rajiv's 6 611-vertex graph from his SageMath file |
| `insert_step.py` | one insertion + annealing run (used for 6 611 -> 6 612) |
| `chain.py` | repeated +1 insertions with pruning, near-miss saving and a checkpoint (6 612 -> 6 629 and the 6 630 near-miss) |
| `chain_step.py` | replays one attempt of `chain.py` from a saved state (to check the near-miss without rerunning the chain) |
| `sa2_resume.py` | low-temperature annealing from a saved near-miss (6 630 near-miss -> the shipped graph) |
| `specs/` | the two chain specifications that were run; `expected_logs/` the original chain logs (paths cut to file names) |

Requirements: `search/requirements.txt` (Python 3.12 with numpy 2.5.3, numba 0.68.0, scipy 1.18.1, networkx 3.7; the
annealer and the random choices use numba's `np.random` and numpy's `default_rng`, so the exact trajectory, and hence
the byte-identical outputs below, are only expected with these versions). numba writes its JIT cache next to the
sources unless `NUMBA_CACHE_DIR` is set. All commands run from this directory; outputs go to `rebuilt/` (not part of
the release; `mkdir -p rebuilt`).

### The chain, step by step

| step | command (from `how-we-built-it/13_4/`) | seed(s) | output (sha256) | original runtime | rerun for the release |
|---|---|---|---|---|---|
| 0. seed | download (see below), `python3 search/decode_sage.py 6611_rishabhrajiv_SageMath.txt 6611 rebuilt/G_13_4_n6611_rajiv.edges` | — | `f6953f1a…d936` | seconds | **yes, identical** |
| 1. 6 611 -> 6 612 | `python3 search/insert_step.py rebuilt/G_13_4_n6611_rajiv.edges --delta 13 --diam 4 --k 1 --iters 100000 --T0 0.6 --T1 0.05 --seed 1 --out rebuilt --tag t6611` | 1 | `rebuilt/sa2hit_t6611_13_4_N6612_s1.edges` `48a2f7d9…b7b5` | not logged | **yes, byte-identical** (84 s) |
| 2. 6 612 -> 6 614 | `python3 search/chain.py --spec search/specs/chain_p134.json --out rebuilt/p134` | 9001, 9002 (prune orders 9000, 9001, 9002) | `valid_p134_13_4_N6614_pruned.edges` `b1d839f9…4cea` | 2 x ~9 min | no |
| 3. 6 614 -> 6 629, near-miss | `python3 search/chain.py --spec search/specs/chain_c134.json --out rebuilt/c134` | 13001 … 13079 | `valid_c134_13_4_N6629_pruned.edges` `46ce5e24…ca53`; near-miss `near_c134_N6630_s13064_c2.edges` | ~17 h wall-clock (Oct 5 18:10 to Oct 6 11:00 PDT, four chains in parallel on a loaded laptop) | attempt 13064 only, **identical** |
| 4. near-miss -> 6 630 | `cp near_miss_N6630_cost2.edges rebuilt/near_c134_N6630_s13064_c2.edges && python3 search/sa2_resume.py rebuilt/near_c134_N6630_s13064_c2.edges 13 4 rebuilt/sa2c2 --iters 250000 --T0 0.12 --T1 0.02 --seeds 101` | 101 | `rebuilt/sa2c2_s101_c0.edges` `7c44e128…10a4` = `../../graphs/G_13_4_n6630.edges` | 145 s | **yes, byte-identical** (192 s) |

Details and expected intermediate hashes:

- **Seed file.** We used Rajiv's SageMath file as hosted on the table's description page,
  `https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/adjacencies/adjD4/6611_rishabhrajiv_SageMath.txt`
  (fetched 2026-10-04 and again 2026-10-06, sha256 `c085973782e2a278776f52f22bec966d3030118222b57b1b5fa2590de258c467`,
  407 098 bytes; the page may change). `decode_sage.py` takes the graph with 6 611 vertices in it. The same labelled
  edge set is in his Zenodo dataset (record 23052995, `data-and-verification.zip`, md5 `5f6b4f07b2d7d300faa3a322c31d93c1`,
  member `graph_d13_k4_n6611.edges.xz`, sha256 `18ca261c689ae99f429549682631dc50cfe6f09f52ace0110a11afd9edae20ae`,
  whose first line is the header `6611 42776`):
  `xz -dc graph_d13_k4_n6611.edges.xz | tail -n +2 > rebuilt/G_13_4_n6611_rajiv.edges` gives the same search input,
  because `ddlib.load_graph` sorts the edge list. Neither file is redistributed here.
- **Step 1** writes `sa2hit_t6611_13_4_N6612_s1.edges` (header names the input file, so keep the name
  `G_13_4_n6611_rajiv.edges`).
- **Step 2** (`expected_logs/chain_p134.log`): prunes 61 edges, then seed 9001 -> 6 613 (`03fb8da9…2476`, pruned
  `e9d644fb…df09`), seed 9002 -> 6 614 (`30ed4897…3e6b`, pruned `b1d839f9…4cea`). The original job was stopped while
  it tried 6 615; stop it once `valid_p134_13_4_N6614_pruned.edges` exists (otherwise it goes on for up to 15
  failed attempts).
- **Step 3** (`expected_logs/chain_c134.log`): 6 615 … 6 627 at seeds 13001–13012 and 13014, 6 628 at 13040, 6 629 at
  13049 (`d01a9895…8390`, pruned `46ce5e24…ca53`, shipped here as `valid_c134_13_4_N6629_pruned.edges.gz`), then 30
  failed attempts at 6 630 (seeds 13050–13079), each saved as a near-miss; the best, seed 13064, has cost 2. The
  near-miss header records the parent path, so compare edge lines, not file hashes (edge lines without the header:
  sha256 `bf4790ac2e82e9f4b82e9e3bc19bea3f4b1d31caff2384305e06ca3a0b54b31a`, the same as `near_miss_N6630_cost2.edges`).
  Intermediate valid files (path-independent): 6 615 `7a7630fa…da55`, 6 618 `905ba10e…8cbb`, 6 628 `f7203352…6244`.
- **Replay of the near-miss attempt alone** (no 17-hour chain needed):
  ```sh
  gzip -dk valid_c134_13_4_N6629_pruned.edges.gz      # sha256 46ce5e24...ca53
  python3 search/chain_step.py valid_c134_13_4_N6629_pruned.edges --delta 13 --diam 4 --seed 13064 --iters 2e5 --T0 0.6 \
          --out rebuilt/near_s13064.edges
  #   N->6630 seed 13064: init 126 best 2 acc 94 full 273 screened 159655  (the original log line)
  diff <(grep -v '^#' rebuilt/near_s13064.edges) <(grep -v '^#' near_miss_N6630_cost2.edges) && echo SAME
  ```
  `chain_step.py` reads the state in file order, which is the order the chain held in memory (`chain.py` itself
  sorts a graph it reads from disk, which is why restarting a chain from a file is not the same as continuing it).
- **Step 4** is deterministic: the original run, a rerun on 2026-10-08 and the rerun for this release (from the
  shipped near-miss, renamed as shown so that the header line matches) all give `7c44e128…10a4`, byte for byte the
  shipped graph: 3 accepted moves, 13 full evaluations.

**What is not recoverable / not confirmed.** All code that produced the chain is here, with its seeds. Steps 2 and 3
were not rerun as a whole (about a day of CPU); that they reproduce the logged trajectory is expected from the
seeding but only checked for the attempt that gave the near-miss (13064), and the first step (6 611 -> 6 612) was
rerun byte for byte. Under other numpy/numba versions the random streams may differ;
the method still works (the chain then finds other graphs), but the specific 6 630 graph is reached only through the
shipped near-miss. Other chains that ran in the same jobs (other cells, and a CP-SAT completion of near-misses that did
not contribute to this graph) are not included.
