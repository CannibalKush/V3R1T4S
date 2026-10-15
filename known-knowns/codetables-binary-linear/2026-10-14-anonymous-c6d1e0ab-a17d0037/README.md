# Binary linear code [173, 17, 72] over GF(2)

## What

The matrix in claim/object/win_q2_n173_k17_d72.json (sha256 a17d00378317979d9fe0acb452d3cce805f55cb17595a8407acb9b56b7b51a76) is a 17 x 173 GF(2) generator matrix of rank 17 whose code has, by two independent full enumerations of all 131071 nonzero codewords, minimum distance exactly 72 with 6341 minimum-weight words, which strictly exceeds the lower bound 70 and does not exceed the upper bound 77 shown in the live codetables.de cell for q=2, n=173, k=17 fetched once at 2026-10-14T16:16:39Z, and which is neither one of nor a subcode or standard derivative (under the quasi-cyclic-structure-preserving maps tested) of the seven arXiv:2609.37056 LinCodeEvolve codes, whose published improvements are all at k in {20,21,22}.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/win_q2_n173_k17_d72.json`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 2 seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| codetables.de (M. Grassl), bounds on linear codes | q = 2, n = 173, k = 17 | lower bound 70, upper bound 77 | d = 72 | http://www.codetables.de/BKLC/BKLC.php?q=2&n=173&k=17 | 2026-10-14T16:14:11Z |
| LinCodeEvolve, arXiv:2609.37056 | k = 17 | no entry; its improvements are at k = 20, 21 and 22 | d = 72 | https://arxiv.org/abs/2609.37056 | 2026-10-14T16:15:37Z |
| V3R1T4S `TROPHY_CASE.md` and open pull requests | binary linear codes | no entry for this cell | d = 72 | https://github.com/elder-plinius/V3R1T4S | 2026-10-14T16:14:30Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed. The table's upper bound for this cell is 77.
- The derived cells are not claimed separately. Puncturing gives [172, 17, 71], [171, 17, 70] and [170, 17, 69], and a zero coordinate gives [174, 17, 72]. These follow from this code.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Markus Grassl**, *Bounds on the minimum distance of linear codes and quantum codes*, http://www.codetables.de/. This is the table the result is compared against.
- **N. J. A. Sloane, R. M. Reddy and C. L. Chen**, "New Binary Codes", *IEEE Trans. Information Theory* IT-18 (1972), 503-510 (https://neilsloane.com/doc/pub.html, entry 23). Its code-combining constructions include the one usually called Construction X, which the search's last step uses.
- **LinCodeEvolve**, arXiv:2609.37056 (https://arxiv.org/abs/2609.37056). Recent related work, compared against.
- Contributor credit: `anonymous-c6d1e0ab`.
