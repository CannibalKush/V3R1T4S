# Binary linear code [213, 26, 77] over GF(2)

## What

The generator matrix in claim/object/code_q2_n213_k26_d77.json (sha256 924876aa988e3a9da62a776f88c297db6aa005b475fe3ad9e76291685851cd12) has rank 26 over GF(2) and exact minimum distance 77 (A_77 = 1170) by full enumeration of all 67,108,863 nonzero codewords with two agreeing methods, which is strictly above the lower bound 76 and at most the upper bound 90 shown in the live codetables.de [213,26] cell fetched 2026-10-15T00:14:28Z, and it is not one of, nor by the paper's own text derived from, the seven LinCodeEvolve codes of arXiv:2609.37056; a live arXiv search for other newer claims was not completed.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/code_q2_n213_k26_d77.json`. The arXiv search the criterion reviewer did not complete was done by the novelty reviewer (`panel/novelty.md`), who found no claim reaching d = 77 at this cell.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 5 minutes (two full enumerations of 2^26 - 1 codewords).
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| codetables.de (M. Grassl), bounds on linear codes | q = 2, n = 213, k = 26 | lower bound 76 (construction last modified 2001-01-30), upper bound 90 | d = 77 | http://www.codetables.de/BKLC/BKLC.php?q=2&n=213&k=26 | 2026-10-15T00:13:13Z |
| LinCodeEvolve, arXiv:2609.37056 | k = 26 | no entry; its codes and derived entries all have k = 20, 21 or 22 | d = 77 | https://arxiv.org/abs/2609.37056 | 2026-10-15 |
| V3R1T4S `TROPHY_CASE.md` and open pull requests | binary linear codes | no entry for this cell | d = 77 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T00:13:14Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed. The table's upper bound for this cell is 90.
- Derived cells are not claimed separately. Adding a parity bit gives [214, 26, 78] (table lower bound 77 there) and a zero coordinate gives [214, 26, 77]; both follow from this code.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Markus Grassl**, *Bounds on the minimum distance of linear codes and quantum codes*, http://www.codetables.de/. This is the table the result is compared against.
- **N. J. A. Sloane, R. M. Reddy and C. L. Chen**, "New Binary Codes", *IEEE Trans. Information Theory* IT-18 (1972), 503-510: the code-lengthening construction usually called Construction X, used in the last step.
- **LinCodeEvolve**, arXiv:2609.37056 (https://arxiv.org/abs/2609.37056). Recent related work, compared against.
- Contributor credit: `anonymous-c6d1e0ab`.
