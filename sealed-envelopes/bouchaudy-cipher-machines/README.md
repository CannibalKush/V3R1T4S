# J.-F. Bouchaudy's Cipher Machines Challenge: two solves (salted commitments only)

| challenge | status | author's solver table |
|---|---|---|
| Hebern 5-rotor, Problem 8 | solved; listed by the author as "Pliny the Liberator 08/10/26" | http://www.jfbouch.fr/crypto/challenges/H5/index.html |
| Kryha (version 2), Problem 5 | solved; listed by the author as "Pliny the Liberator 08/10/26" | http://www.jfbouch.fr/crypto/challenges/KRYHA2/index.html |

The solutions are **held privately at the author's request**, so that the problems stay open for other solvers. This
directory contains nothing about the solutions except the salted commitments below. See `../../DONT_SPOIL_THE_HUNT.md`.

Both solver tables were re-fetched on 2026-10-13 (one plain GET each): the setter rates Problem 8 "hard" and Kryha
version 2 Problem 5 "difficult", and "Pliny the Liberator 08/10/26" is the only solver listed for either problem.

## Salted commitments

Each commitment is `sha256(salt || file bytes)` with a fresh 32-byte random salt per file; the salts are kept
privately and are not in this repository. The files were frozen on 2026-10-06, before the solutions were sent to the
author. They will be revealed (files and salts) only with the author's explicit permission, and not while others are
actively competing.

| challenge | file | frozen (UTC) | commitment |
|---|---|---|---|
| Hebern-5 Problem 8 | solution file 1 (key) | 2026-10-06T08:38:49Z | `3c8da0fc9f76c0ebf785098718294810c3672e74b59b8e73320df7d9c6402c90` |
| Hebern-5 Problem 8 | solution file 2 (decryption, structured) | 2026-10-06T08:25:20Z | `d718c6ceaf29f1ffa885d3ac2d0ebaf3f56db4896c0ad3e0319b0c50427fcf69` |
| Hebern-5 Problem 8 | solution file 3 (decryption, readable) | 2026-10-06T08:31:04Z | `eb37bfa329199ef4557b4d4423143f702b458ac47ea14dbe7702400b2e5e8a02` |
| Kryha v2 Problem 5 | solution file 1 (key) | 2026-10-06T09:43:11Z | `0cd60475019d1abff50ec3627a8dfbfc8f78dc3e4a0321e82a64611c9f20a1b6` |
| Kryha v2 Problem 5 | solution file 2 (verification output) | 2026-10-06T09:43:51Z | `25d32553b6b249085c33dcf13e63ac59dfe25fd793b2f1cf833a7464344c7e30` |

To check a future reveal: `cat salt.bin file | sha256sum` must print the commitment.

## Credits

The challenges, the machine descriptions and the solver tables are J.-F. Bouchaudy's (jfbouch.fr). Please solve the
problems yourself and send your solution to him as his pages describe; do not ask us for the solutions.
