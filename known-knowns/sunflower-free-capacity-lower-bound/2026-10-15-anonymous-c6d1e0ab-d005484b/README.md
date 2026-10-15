# Exact value g(8,4) = 24 for 3-sunflower-free 4-uniform families on 8 points

## What

claim/object/family_g8_4_24.json (sha256 d005484b9bf31c11634f4ed9c6cc2e1f4c99b6005a2f471f70fd9726bfbd09ca) is a family of 24 distinct 4-subsets of {1..8} with no three members (empty core included) having pairwise equal intersections, and drat-trim verifies claim/object/sb.drup as a refutation of the lex-leader-symmetry-broken CNF claim/object/sb.cnf for "at least 25 such members", whose clauses (apart from its first comment line, which the shipped generator words differently) the shipped generator regenerates, so g(8,4) = 24 exactly, with no claim about the 1.5545 rate bar or any other (n,r).

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same files, with identical bytes, are `object/family_g8_4_24.json`, `object/sb.cnf` and `object/sb.drup`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later (standard library) and a C compiler for drat-trim; `python-sat` optional (CNF regeneration step).
- **Rough laptop time**: under a minute.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| OEIS (sequences A332077, A236397 and column searches) | g(8,4) | not tabulated (OEIS lists the unrestricted-ground-set quantity f(r,3) only) | 24 | https://oeis.org/ | 2026-10-15 |
| Markström, small 3-uniform Turán numbers | g(n, n-3) only | covers n-r = 3; this claim has n-r = 4 | 24 | http://abel.math.umu.se/~klasm/Data/hypergraphs/turan3.html | 2026-10-15T15:24:53Z |
| arXiv (export API, five queries; arXiv:2609.06175 Sep 2026) | small exact sunflower values | unrestricted ground set only; no fixed-n value | 24 | https://arxiv.org/abs/2609.06175 | 2026-10-15 |
| Polymath10 project table | f(k,3) unrestricted | no fixed-n values | 24 | polymath wiki (archived) | 2026-10-15 |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | no sunflower claim | 24 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15 |

Literature record with fetch times and hashes: `the-record-we-beat/README.md` and `panel/novelty.md`.

## Not claimed

- The full success criterion (a family with rate above 1.5545) is not claimed; this family's rate is 24^(1/8), far below it.
- Only g(8,4). Other exact values from the same computation are separate packages; ten values that turned out to be known (Mantel cases, Markström's table, Abbott-Gardner) are not claimed anywhere.
- The proof is of the lex-leader symmetry-broken CNF (sound by the invariance argument in how-we-built-it/SOUNDNESS.md section 3; a proof of the plain CNF also exists and exceeds the file-size limit).
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **P. Erdős and R. Rado** (1960), the sunflower lemma, and **P. Erdős and E. Szemerédi** (1978) on sunflower-free families: the problem.
- **K. Markström**, tables of small Turán numbers for 3-uniform hypergraphs (http://abel.math.umu.se/~klasm/Data/hypergraphs/turan3.html): used to exclude the n-r = 3 values as known.
- **H. L. Abbott, D. Hanson and N. Sauer** (1972), **H. L. Abbott and G. Exoo** (1992), **Polymath10** (2015-16): the unrestricted-ground-set small values compared against.
- **M. Heule and N. Wetzler**, drat-trim (https://github.com/marijnheule/drat-trim): the proof checker shipped in verify-it-yourself/.
- **python-sat** (A. Ignatiev, A. Morgado, J. Marques-Silva): the cardinality encoding used by gen_cnf.py; **glucose** (G. Audemard, L. Simon): the solver that produced the DRUP proof.
- The bank's reference page: https://github.com/teorth/optimizationproblems/blob/main/constants/49a.md (the rate bar, not claimed here).
- Contributor credit: `anonymous-c6d1e0ab`.
