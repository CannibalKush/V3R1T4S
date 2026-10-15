# Binary linear code [175, 25, 61] over GF(2)

## What

The 25 x 175 matrix in claim/object/code_q2_n175_k25_d61.json (sha256 5128a84caf064a0c4b0b6bd46d4c8d26e02cddac4bbc988437a72c947859e17c) has rank 25 over GF(2) and generates a binary linear [175,25,61] code with exactly 95 codewords of weight 61, established by two independent full enumerations of all 33,554,431 nonzero codewords, and 61 exceeds the lower bound 60 and is below the upper bound 72 shown in the live codetables.de cell for q=2, n=175, k=25 fetched once at 2026-10-14T19:15:17Z, while the code is not one of, and by dimension cannot be a standard derivative of, the seven LinCodeEvolve codes of arXiv:2609.37056 (all of dimension 20 to 22), and a single arXiv API query on 2026-10-14 found no newer claim of a binary [175,25] code with minimum distance 61 or more.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/code_q2_n175_k25_d61.json`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 2 minutes (two full enumerations of 2^25 - 1 codewords).
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| codetables.de (M. Grassl), bounds on linear codes | q = 2, n = 175, k = 25 | lower bound 60 (construction dated 2001-01-30), upper bound 72 | d = 61 | http://www.codetables.de/BKLC/BKLC.php?q=2&n=175&k=25 | 2026-10-14T19:09:10Z |
| MinT (Univ. Salzburg) | binary linear [175, 25] | best constructive d = 60 | d = 61 | http://mint.sbg.ac.at/ | 2026-10-14T19:16:25Z |
| LinCodeEvolve, arXiv:2609.37056 | k = 25 | no entry; its codes and derived entries all have k = 20, 21 or 22 | d = 61 | https://arxiv.org/abs/2609.37056 | 2026-10-14 |
| V3R1T4S `TROPHY_CASE.md` and open pull requests | binary linear codes | no entry for this cell | d = 61 | https://github.com/elder-plinius/V3R1T4S | 2026-10-14T19:09:26Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed. The table's upper bound for this cell is 72.
- Derived cells are not claimed separately. Adding a parity bit gives [176, 25, 62] (table lower bound 61 there), and a zero coordinate gives [176, 25, 61]; both follow from this code.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Markus Grassl**, *Bounds on the minimum distance of linear codes and quantum codes*, http://www.codetables.de/. This is the table the result is compared against.
- **R. Schürer and W. Ch. Schmid**, *MinT: the database of optimal net, code, OA and OOA parameters*, http://mint.sbg.ac.at/. Second table checked.
- **N. J. A. Sloane, R. M. Reddy and C. L. Chen**, "New Binary Codes", *IEEE Trans. Information Theory* IT-18 (1972), 503-510: code-lengthening constructions of the kind used in the last step.
- **LinCodeEvolve**, arXiv:2609.37056 (https://arxiv.org/abs/2609.37056). Recent related work, compared against.
- Contributor credit: `anonymous-c6d1e0ab`.
