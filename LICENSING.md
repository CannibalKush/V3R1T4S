# Licensing

Two licenses apply, by path. When in doubt: **source code is AGPL-3.0, everything else is CC BY 4.0**.

| Path | What it is | License |
|---|---|---|
| `known-knowns/*/verify-it-yourself/*.py`, `known-knowns/*/verify-it-yourself/*.c`, `known-knowns/*/verify-it-yourself/*.sh` | checkers, check scripts | AGPL-3.0 (`LICENSE`) |
| `known-knowns/biggest-graphs/how-we-built-it/**/*.py`, `known-knowns/biggest-graphs/the-record-we-beat/*.py` | rebuild scripts, table parser | AGPL-3.0 |
| `known-knowns/bigger-codes/the-record-we-beat/*.py`, `known-knowns/faster-matrix-multiplication/the-record-we-beat/*.py`, `known-knowns/vnncomp-2026-unsolved-instances/the-record-we-beat/*.py` | table parsers | AGPL-3.0 |
| `known-knowns/lehmer-past-10-to-the-50/engines/*.c`, `known-knowns/lehmer-past-10-to-the-50/engines/*.py` | search engines and tools | AGPL-3.0 |
| `known-knowns/lehmer-past-10-to-the-50/lean/**` (`*.lean`, `lakefile.toml`, `lean-toolchain`, `lake-manifest.json`) | Lean formalization | AGPL-3.0 |
| `known-knowns/biggest-graphs/graphs/`, `known-knowns/biggest-graphs/how-we-built-it/**` (non-code: parameters, certificates, cut sets, near-miss) | graphs and construction data | CC BY 4.0 (`LICENSE-DATA`) + third-party attribution below |
| `known-knowns/bigger-codes/codes/`, `certificates/` | codes and LP certificates | CC BY 4.0 + attribution below |
| `known-knowns/faster-matrix-multiplication/schemes/` | matrix multiplication schemes | CC BY 4.0 + attribution below |
| `known-knowns/vnncomp-2026-unsolved-instances/witnesses/` | VNN-COMP counterexample inputs | CC BY 4.0 + attribution below |
| `known-knowns/robustbench-cifar100-stronger-attack/adversarial-examples/` | adversarial CIFAR-100 test images, robust-image list | CC BY 4.0 for our perturbation, as research data; the underlying CIFAR-100 images keep their own terms (below) |
| `known-knowns/lehmer-past-10-to-the-50/branch_logs/`, `known-knowns/lehmer-past-10-to-the-50/certificates/` | search logs, summaries, certificates | CC BY 4.0 |
| `known-knowns/*/INDEX*.csv`, `known-knowns/*/the-record-we-beat/*` (non-code), `known-knowns/*/verify-it-yourself/RECEIPTS.md` | indexes, table-snapshot metadata, check outputs | CC BY 4.0 |
| `sealed-envelopes/` | salted hash commitments | CC BY 4.0 |
| all Markdown (`*.md`, including `known-knowns/lehmer-past-10-to-the-50/engines/SPEC_*.md`), `CITATION.cff`, `SHA256SUMS`, `.gitignore` | documentation | CC BY 4.0 |

`LICENSE` is the GNU Affero General Public License v3.0 that the repository was created with. `LICENSE-DATA` is the full
legal code of Creative Commons Attribution 4.0 International.

**Suggested attribution** for CC BY material: "V3R1T4S (github.com/elder-plinius/V3R1T4S), CC BY 4.0",
plus the third-party credit below for the object you use.

## Third-party material and attribution (required)

Several objects are derived from other people's published work. Our license covers our modifications; the
underlying works keep their own terms, and their authors must be credited whenever the derived object is used.

- **Rishabh Rajiv, Zenodo doi:10.5281/zenodo.23052995 (CC BY 4.0).** `known-knowns/biggest-graphs/graphs/G_13_6_n535495.edges.gz`
  and `G_15_6_n1424896.edges.gz` are derived from his compound graphs H_9(T_4) and H_11(T_4), and
  `known-knowns/biggest-graphs/graphs/G_13_4_n6630.edges` (with `known-knowns/biggest-graphs/how-we-built-it/13_4/`) descends by local search from his (13,4)
  graph Q9(T4)++. Required attribution: *R. Rajiv, "Large graphs of given degree and diameter from compounds of
  generalized hexagons" dataset, Zenodo, doi:10.5281/zenodo.23052995, licensed CC BY 4.0; modified by the V3R1T4S
  agents (cut sets, surgery vertices, shortcuts, vertex insertion and edge switches).* His base graphs are not
  redistributed; the construction files rebuild our graphs from his published files.
- **Nishant Bhakar.** `known-knowns/biggest-graphs/how-we-built-it/14_4/G_14_4_n8424.params.json` contains his (4,4) graph on 104
  vertices ("Bhakar_104", F. Comellas' table, 27 Aug 2026), reproduced only because the lift cannot be rebuilt
  without it. Credit him for that graph.
- **Ryosuke Mizuno** (arXiv:2606.15860, github.com/rmizuno42/ddp): route-chart lift method for the (15,3) and (15,4)
  graphs (our own controllers; his are not redistributed). **Charles Delorme** (1985): polarity quotient for (15,4).
- **Constant-weight codes**: each code is a local-search polish of a code from A. E. Brouwer's table and archive
  (https://aeb.win.tue.nl/codes/Andw.html) or of a Graham–Sloane code; the seed of every cell is named in
  `known-knowns/bigger-codes/INDEX.csv` (Jordan Boisclair, Daniel Gangl, Alfonso Gippini (doi:10.5281/zenodo.23075336),
  Christian Lysenstøen (arXiv:2607.19550), William Echols (arXiv:2608.13906), unlabelled archive codes). Most words of
  each code are the seed author's words; credit them.
- **LITA** (Kirill Khoruzhii, Luzian Serafin, Patrick Gelß, Sebastian Pokutta, github.com/khoruzhii/lita):
  our five schemes in `known-knowns/faster-matrix-multiplication/schemes/` are derived from (restrictions of) their public square schemes.
  Their repository has no license; we will remove or relicense the derived schemes on request. Cite LITA with the BibTeX under "Please cite" in `known-knowns/faster-matrix-multiplication/README.md`.
- **VNN-COMP 2026** (github.com/VNN-COMP/vnncomp2026_benchmarks, vnncomp2026_results): the benchmark files (ONNX
  networks, VNN-LIB properties), the results table and the official validator are **not redistributed**; the checkers
  download them from a pinned commit and check their sha256. We publish only our two witnesses. Each witness lies within
  ±1 per pixel of an image encoded in the benchmark's property file, so it is derived from the benchmark of Andreea
  Postovan and Mădălina Eraşcu (`traffic_signs_recognition_2023`, arXiv:2310.03033): credit them and the VNN-COMP
  organisers whenever the witnesses are used.
- **CIFAR-100 and RobustBench.** `known-knowns/robustbench-cifar100-stronger-attack/adversarial-examples/x_adv_Addepalli2022Efficient_RN18.npz`
  is derived from the CIFAR-100 test set (A. Krizhevsky, *Learning Multiple Layers of Features from Tiny Images*, 2009):
  3,455 of its 10,000 images are unchanged copies and the others differ by at most 8/255 per pixel. CIFAR-100 is
  distributed by its authors (cs.toronto.edu/~kriz/cifar.html) without a formal license, with the request to cite the
  report above; its images were collected from the web for the 80 Million Tiny Images project and their original
  owners may hold rights in them. Our CC BY 4.0 covers only our contribution (the perturbation and the robust-image
  list); the tensor is offered as research data, for checking this result and for research use, and anyone reusing it
  should follow the CIFAR-100 terms and cite Krizhevsky (2009). The model weights (S. Addepalli, S. Jain, R. Venkatesh
  Babu, NeurIPS 2022) and RobustBench's code and tables are **not redistributed**; the checker downloads them through
  RobustBench. We will remove or relicense the tensor on request.
- **Reference tables and catalogues** (F. Comellas' degree-diameter table, A. E. Brouwer's constant-weight table, the
  fast-matrix-multiplication catalogues, J.-F. Bouchaudy's challenge pages, the VNN-COMP results table, RobustBench's
  model_info files) are **never redistributed**. `the-record-we-beat/`
  directories hold only fetch metadata (URL, time, selected HTTP headers, sha256 of the page) and the values we parsed
  for our own cells.

Contributions are accepted under the same terms (inbound = outbound).
