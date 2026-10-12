# (14,4), N = 8424: parameter search

These scripts produce [`../G_14_4_n8424.params.json`](../G_14_4_n8424.params.json). [`../rebuild_lift.py`](../rebuild_lift.py) turns that file into the edge list.

## Files

| file | what it does |
|---|---|
| `frame4.py` | The search that was actually run. It reads a 4-regular controller graph of diameter at most 4. It orients the controller along an Euler circuit and draws random local data for each vertex: points of a fixed plane in F_3^4, complements, and in-fibre translations. For each arc it lists every "frame transport" matrix over GF(3) that meets the local conditions. A SAT solver (CaDiCaL 1.5.3 through python-sat) then picks one transport per arc so that a covering condition holds at every vertex. The script writes the params JSON and the lifted edge list (vertex (u, p) = 81u + code(p)). The resulting lift is 14-regular on 81 x 104 = 8424 vertices. |
| `gf3.py` | Small exact GF(3) linear-algebra helpers that `frame4.py` imports. |
| `controller_from_params.py` | **Written for this release, not part of the original run.** It writes the controller that is already embedded in `../G_14_4_n8424.params.json` (key `controller_edges`) as a plain edge list. With it you can run `frame4.py` without downloading anything. The output parses to the same graph as the downloaded file. Rerunning `frame4.py` on it gave the same hashes (see below). |

## Input: Bhakar's (4,4) graph on 104 vertices

This is the table entry for (4,4) on F. Comellas' degree-diameter page.

- URL: https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/adjacencies/adjD4/104c_d4D4.txt
- Save it as `adjD4_104c_d4D4.txt`. `frame4.py` stores the base name of the controller file in the params JSON, so the name has to match for a byte-identical output.
- sha256 of the copy we used (fetched 2026-10-04): `30002ef72940ccd9959b482b8b170ba67d16437600de0f63e935a67527210f3a`

```bash
curl -sSL -o adjD4_104c_d4D4.txt https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/adjacencies/adjD4/104c_d4D4.txt
shasum -a 256 adjD4_104c_d4D4.txt
# or, offline, from the published params:
python controller_from_params.py            # writes adjD4_104c_d4D4.txt in the current directory
```

## Command (seed 1)

```bash
pip install -r requirements.txt
python -W ignore frame4.py adjD4_104c_d4D4.txt --seed 1 --tries 5 --out G14_4_104c_s1
shasum -a 256 G14_4_104c_s1.params.json G14_4_104c_s1.edges.txt
```

Expected output: `attempt 0: arcs without P0-candidates: 0/208; min/avg #cands 432/540.0`, then
`lift N=8424, edges=58968 unique=58968, loops=0, deg min/max=14/14`.

| output | sha256 |
|---|---|
| `G14_4_104c_s1.params.json` (= `../G_14_4_n8424.params.json`) | `4276a7a12d8fbb8906fef646cc0e1dbd2a8693f6ccfc3b3aa90a3f101155c22b` |
| `G14_4_104c_s1.edges.txt` (= [`graphs/G_14_4_n8424.edges.txt`](../../../graphs/G_14_4_n8424.edges.txt)) | `71ef820b5804f77c626209fbcda3a8bd50c546a5fb70175cbe36a9f98f22f281` |

The search is deterministic for a given seed. All randomness comes from `numpy.random.default_rng(seed)`, and seed 1 succeeds on the first attempt. The original run took about 55 s. A rerun from these repo copies used the controller written by `controller_from_params.py`, one thread, Python 3.12.13 and the versions below on an Apple M5 Mac. It took 12 to 32 s wall-clock over two runs, and both runs reproduced both sha256 values exactly. During the original work, seeds 2 to 6 on the same controller also gave diameter-4 lifts. Those lifts are different graphs and are not published here.

## Packages

Python 3.12.13; `numpy==2.5.3`, `python-sat==1.9.dev15` (see `requirements.txt`).

## Third-party credits

- **python-sat** (PySAT), by A. Ignatiev, J. Marques-Silva and A. Morgado. MIT license. It provides the SAT interface and the card-encoding helper (`CardEnc`, pairwise encoding).
- **CaDiCaL 1.5.3**, by A. Biere and co-authors. MIT license. It ships inside python-sat and is used as `Cadical153`.
- **NumPy**: BSD-3-Clause.
- **Controller graph**: N. Bhakar's (4,4) graph on 104 vertices, from F. Comellas' degree-diameter table. It is not copied here as a separate file, but it is embedded in the params JSON.
