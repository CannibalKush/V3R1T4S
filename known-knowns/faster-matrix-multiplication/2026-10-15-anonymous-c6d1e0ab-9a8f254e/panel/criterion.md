# CRITERION skeptic report: fmm-13x13x15-r1578

Target: `fmm-catalogue-small-format-rank`. Object: claim/object/13x13x15_r1578_Q.json
(sha256 9a8f254ed5b7e15b8f4157da632c5adc686e46c4f020659b924114c8b7c5a618, matches claim.SHA256SUMS; all seven
listed claim files verified against the hash list with shasum -a 256 -c, all OK).

Inputs read: the claim folder and claim.SHA256SUMS only. Before reading the author's checker code I read only
its header docstring for the index convention (u[i*n2+j] is the coefficient of A[i][j], v[j*n3+l] of B[j][l],
w[l*n1+i] of C[i][l]) and then wrote my own checker. Format notation below uses 13x13x15 and (n,m,p) in place of
the bank's bracketed notation.

## Clause-by-clause

### Clause 1: "an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms)"
Met. The JSON holds 1578 rows each of u (169 entries), v (195 entries), w (195 entries) in the encoding
`sparse_flat_pairs` (index, value, index, value, ...); values are integers or "p/q" strings. My parser found no
structural issue: no odd-length rows, no out-of-range index, no duplicate index within a row, row counts of
u, v, w all equal the declared m = 1578.

### Clause 2: "for a format (n,m,p) with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}"
Met. n = [13,13,15]; max side 15 <= 16; sorted format (13,13,15) is neither excluded triple.

### Clause 3: "whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of" the four live sources
Met. I fetched each source exactly once (curl, User-Agent "V3R1T4S-research (honest client; curl)", no retries),
all HTTP 200, all sha256 identical to the author's table-record:

| Source | My fetch (UTC) | sha256 | Cell for sorted format 13x13x15 |
|---|---|---|---|
| fmm_sota.json (createdAt 2026-10-09T11:45:48) | 2026-10-15T09:22:00Z | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | {"format": [13, 13, 15], "rank": 1605} |
| Lille page https://fmm.univ-lille.fr/{n}x{m}x{p}.html with n,m,p = 13,13,15 | 2026-10-15T09:22:01Z | 3f01c282cb2debee57eb71774249022076cbb880bc7442be6ab40ac4225e8d44 | 1605; construction column: decomposition 7x5x5:127 + 7x5x5:127 + 6x... (a composition) |
| Perminov README, "Research Findings & Status" table, columns ZT / Z / Q | 2026-10-15T09:22:05Z | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | row `13x13x15`: 1591 / 1591 / 1591 (no bracketed previous value; no 13x15x13 or 15x13x13 row) |
| MerlijnW70 fmm-schemes repository tree (api.github.com, recursive, truncated=false, 39 entries) | 2026-10-15T09:22:06Z | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | one matching file: schemes/13x13x15_m1591_ZT.json, rank 1591 |

Minimum over the four sources: 1591. Rank of the object, counted by me as the number of terms with all three
factors nonzero: 1578 (zero all-zero-factor terms). 1578 < 1591 (margin 13); 1578 < 1605 and 1578 < 1591 for
every individual source. Rank is invariant under axis permutation, and 13x13x15 is already sorted.

### Clause 4: "verified in exact arithmetic ... over the ring it claims"
Met. Claimed ring Q. The scheme is genuinely rational, not integer: global least common denominators are
U 5440, V 40, W 40 (so it is not a Z or ZT scheme; the relevant Perminov column, Q, is also 1591). My own
checker verified all 169*195*195 = 6,426,225 Brent equations exactly over Q by two independent routes:
(1) exact big-integer matrix products (python-flint fmpz_mat) after scaling U, V, W to integers, comparing
against the scaled identity 5440*40*40; (2) residues modulo five primes near 2^20 whose product (~2^100) exceeds
twice the proven coefficient bound (~2^65) so residue equality implies integer equality. A third sanity check
evaluated the scheme with exact Fractions on random integer A (13x13) and B (13x15) and reproduced A*B.
Real output of my checker (nice -n 19; venv python with numpy and python-flint 0.6.0):

```
n = (13, 13, 15) declared m = 1578 ring = Q encoding = sparse_flat_pairs
structural issues: none
terms with all three factors nonzero (rank): 1578 ; all-zero-factor terms: 0
global LCDs: U 5440 V 40 W 40 (scheme is over Z iff all 1)
max |U'|,|V'|,|W'| = 14131200 35308 35334 ; worst-case |sum| bound = 27819669391176499200 (~2^65.0)
[flint exact] Brent equations checked: 6426225; violated: 0; max |deviation|: 0; time 17.1s
modular primes [1048573, 1048571, 1048559, 1048549, 1048517] ; product ~2^100 > 2*(bound+scale): True
[modular x5 primes] residue mismatches: 0; time 56.4s
random exact-Fraction evaluation A*B reproduced: True
RESULT: EXACT SCHEME OVER Q, RANK 1578
```

Negative controls on my checker (both rejected): dropping the last term gives rank 1577 with 14,820 violated
equations (74,100 residue mismatches); flipping the sign of one w coefficient in term 0 gives 289 violated
equations (1,445 residue mismatches). No pair of terms shares a proportional (u,v), (u,w) or (v,w) pair, so the
1578 terms are not trivially mergeable.

The author's own script (run on a copy of the claim folder inside my workspace) also ends `ALL CHECKS PASS`
with `PASS format=13x13x15 rank=1578` and its built-in negative control rejected.

### Clause 5: "a scheme valid only over GF(2) counts here ONLY if ..."
Not applicable: the scheme is verified over Q (characteristic 0), so the F2/COVERAGE.md branch and partial
win p2 do not arise.

### Clause 6: "A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed"
Met (clause does not bite). 1578 equals no value listed in any of the four sources (listed values: 1605, 1605,
1591/1591/1591, 1591). The object's embedded note says it was derived from a 13x14x15 rank-1649 scheme by
restricting the middle axis (raw 1613) and then absorbing 35 terms; a restriction followed by term absorption
is not a composition yielding a listed rank. Null model from public tables: Lille's own composition gives 1605;
restriction of Perminov's 13x14x15 (1681) or 13x13x16 (1704) cannot be shown to go below 1591 without work; the
split 13x13x14 + 13x13x1 gives 1511 + 169 = 1680. None reaches 1578.

### Clause 7 (scope splits): "Ternary/integer re-derivations of a rank already attained over Q are NOT this target ... fewer additions at an existing rank is NOT this target"
Met. 1578 is a new rank for the format, not a ring upgrade at an existing rank (the existing Q rank is 1591)
and not an additions-count claim.

### Clause 8 (bank): "every one re-fetched live immediately before claiming"
Met on the evidence: the author's table-record gives fetch times 2026-10-15T09:07:43Z to 09:07:54Z with
sha256 values identical to my own fetches at 09:22Z the same day.

## Partial wins considered
- p1 (17 <= max side <= 32): not applicable, max side is 15; the claim is the full criterion, not p1.
- p2 (GF(2)-only improvement): not applicable, the scheme is over Q.
Neither partial win is the right classification; the result meets the full success criterion.

## Non-subsumed check
One GET of the V3R1T4S trophy case (2026-10-15T09:29:51Z, HTTP 200, sha256
b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412) shows no 13x13x15 row. Existing FMM rows are
for 14x15x15 (1842), 13x14x14 (1558), 15x16x16 (2180), 14x14x15 (1716) and 13x14x15 (1677); the only one that
restricts to 13x13x15 is 13x14x15 at 1677, far above 1578, so this result is not subsumed by a prior entry.

## Limits
- I verified the scheme and the four live cells myself; I did not independently reproduce the search that
  produced the scheme (the "13x14x15 rank 1649" intermediate named in the object's note is not public and is not
  needed for the criterion).
- Perminov's CHANGELOG and the Lille main table were not fetched; the criterion names the README table and the
  per-format page, both fetched.

## Verdict
PASS. The object is an exact bilinear scheme over Q for 13x13x15 with 1578 rank-one terms, strictly below the
live minimum 1591 of all four named sources, meeting every clause of the full success criterion literally.

confirmed_scope: The file claim/object/13x13x15_r1578_Q.json (sha256 9a8f254ed5b7e15b8f4157da632c5adc686e46c4f020659b924114c8b7c5a618) is an exact bilinear matrix multiplication scheme over Q for the format 13x13x15 with exactly 1578 rank-one terms, each with all three factors nonzero, verified by my own exact big-integer and multi-prime Brent-equation checks, and 1578 is strictly below the rank for the sorted format 13x13x15 in each of the four named sources as fetched live on 2026-10-15 (fmm_sota.json 1605, Lille page 1605, Perminov README ZT/Z/Q 1591/1591/1591, MerlijnW70 file 13x13x15_m1591_ZT.json), whose minimum is 1591.
context: Claude Code subagent (Fable 5.1), fresh context

## Appendix: my checker source (my_check.py)

```python
"""CRITERION skeptic's own exact Brent-equation check (written before reading the author's checker code).
Convention (from the claim's description): u[i*n2+j] corresponds to A[i][j]; v[j*n3+l] corresponds to B[j][l]; w[l*n1+i] corresponds to C[i][l].
Brent: sum_t u_t[i,j] v_t[j',l] w_t[i',l'] == [i==i'][j==j'][l==l'] for all indices.
Method: parse values as exact Fractions, scale U,V,W by their global LCDs to integers, compute the full
Brent tensor with int64 matmuls under a proven overflow bound, compare slot-by-slot with scaled identity."""
import json, sys, time
from fractions import Fraction
import numpy as np

path = sys.argv[1]
d = json.load(open(path))
n1, n2, n3 = d["n"]
m = d["m"]
enc = d.get("encoding")
print("n =", (n1, n2, n3), "declared m =", m, "ring =", d.get("ring"), "encoding =", enc)
assert enc == "sparse_flat_pairs", "this checker handles sparse_flat_pairs only"
lens = {"u": n1 * n2, "v": n2 * n3, "w": n3 * n1}
assert len(d["u"]) == len(d["v"]) == len(d["w"]) == m, ("row counts", len(d["u"]), len(d["v"]), len(d["w"]), m)

def parse_val(x):
    if isinstance(x, bool): raise ValueError("bool value")
    if isinstance(x, int): return Fraction(x)
    if isinstance(x, str): return Fraction(x)  # "p/q"
    raise ValueError(f"bad value {x!r}")

issues = []
mats = {}
for key, L in lens.items():
    M = [[Fraction(0)] * L for _ in range(m)]
    for t, row in enumerate(d[key]):
        if len(row) % 2: issues.append(f"{key}[{t}] odd length")
        seen = set()
        for idx, val in zip(row[0::2], row[1::2]):
            if not isinstance(idx, int) or not (0 <= idx < L): issues.append(f"{key}[{t}] index {idx} out of range")
            if idx in seen: issues.append(f"{key}[{t}] duplicate index {idx}")
            seen.add(idx)
            M[t][idx] += parse_val(val)
    mats[key] = M
print("structural issues:", issues if issues else "none")

# rank = terms with all three factors nonzero
nz = [all(any(mats[k][t][c] != 0 for c in range(lens[k])) for k in "uvw") for t in range(m)]
rank = sum(nz)
print("terms with all three factors nonzero (rank):", rank, "; all-zero-factor terms:", m - rank)

# denominators / ring
from math import lcm
def lcd(M): 
    D = 1
    for row in M:
        for x in row: D = lcm(D, x.denominator)
    return D
DU, DV, DW = lcd(mats["u"]), lcd(mats["v"]), lcd(mats["w"])
print("global LCDs: U", DU, "V", DV, "W", DW, "(scheme is over Z iff all 1)")
def to_int(M, D): return [[int(x * D) for x in row] for row in M]
Ui, Vi, Wi = to_int(mats["u"], DU), to_int(mats["v"], DV), to_int(mats["w"], DW)
mu = max(abs(x) for r in Ui for x in r); mv = max(abs(x) for r in Vi for x in r); mw = max(abs(x) for r in Wi for x in r)
bound = m * mu * mv * mw
print("max |U'|,|V'|,|W'| =", mu, mv, mw, "; worst-case |sum| bound =", bound, "(~2^%.1f)" % (bound.bit_length()))
scale = DU * DV * DW

# ---- Route 1: exact big-integer arithmetic (python-flint fmpz_mat) ----
import flint
Vf = flint.fmpz_mat(Vi); Wf = flint.fmpz_mat(Wi)
t0 = time.time(); bad = 0; checked = 0; maxdev = 0
for a in range(n1 * n2):
    i, j = divmod(a, n2)
    Ua = flint.fmpz_mat([[Ui[t][a]] for t in range(m)])          # m x 1
    # S = (Ua .* V)^T W   computed as V^T diag(Ua) W = (V^T * diag) ... do: X = diag(Ua) * V  (m x n2n3)
    X = flint.fmpz_mat([[Ui[t][a] * Vi[t][b] for b in range(n2 * n3)] for t in range(m)])
    S = X.transpose() * Wf                                      # (n2n3) x (n3n1), exact integers
    for b in range(n2 * n3):
        jp, l = divmod(b, n3)
        for c in range(n3 * n1):
            lp, ip = divmod(c, n1)
            tgt = scale if (jp == j and ip == i and lp == l) else 0
            checked += 1
            dev = int(S[b, c]) - tgt
            if dev: bad += 1; maxdev = max(maxdev, abs(dev))
print(f"[flint exact] Brent equations checked: {checked}; violated: {bad}; max |deviation|: {maxdev}; time {time.time()-t0:.1f}s")

# ---- Route 2: multi-prime modular check with stated bound ----
# primes < 2^20 so that (X mod p)^T (W mod p) fits int64: entries < 2^20, products < 2^40, sum over m < 2^51.
primes = [1048573, 1048571, 1048559, 1048549, 1048517]
P = 1
for p in primes: P *= p
assert P > 2 * (bound + scale), "prime product must exceed twice the deviation bound"
print("modular primes", primes, "; product ~2^%d > 2*(bound+scale): True" % P.bit_length())
Uo = np.array(Ui, dtype=object); Vo = np.array(Vi, dtype=object); Wo = np.array(Wi, dtype=object)
t0 = time.time(); bad2 = 0
for p in primes:
    Up = (Uo % p).astype(np.int64); Vp = (Vo % p).astype(np.int64); Wp = (Wo % p).astype(np.int64)
    sc = scale % p
    for a in range(n1 * n2):
        i, j = divmod(a, n2)
        X = (Up[:, a][:, None] * Vp) % p
        S = (X.T @ Wp) % p
        Tgt = np.zeros((n2 * n3, n3 * n1), dtype=np.int64)
        for l in range(n3): Tgt[j * n3 + l, l * n1 + i] = sc
        bad2 += int(np.count_nonzero(S - Tgt))
print(f"[modular x{len(primes)} primes] residue mismatches: {bad2}; time {time.time()-t0:.1f}s")

# Independent sanity check on the convention: exact Fraction evaluation on random integer A, B
import random
random.seed(1578)
A = [[Fraction(random.randint(-3, 3)) for _ in range(n2)] for _ in range(n1)]
B = [[Fraction(random.randint(-3, 3)) for _ in range(n3)] for _ in range(n2)]
C = [[Fraction(0)] * n3 for _ in range(n1)]
for t in range(m):
    ua = sum(mats["u"][t][i * n2 + j] * A[i][j] for i in range(n1) for j in range(n2) if mats["u"][t][i * n2 + j])
    vb = sum(mats["v"][t][j * n3 + l] * B[j][l] for j in range(n2) for l in range(n3) if mats["v"][t][j * n3 + l])
    p = ua * vb
    if p:
        for c in range(n3 * n1):
            w = mats["w"][t][c]
            if w:
                l, i = divmod(c, n1)
                C[i][l] += w * p
ok = all(C[i][l] == sum(A[i][j] * B[j][l] for j in range(n2)) for i in range(n1) for l in range(n3))
print("random exact-Fraction evaluation A*B reproduced:", ok)

verdict = (bad == 0 and bad2 == 0 and ok and not issues and rank == m)
print("RESULT:", "EXACT SCHEME OVER Q, RANK", rank if verdict else "FAILED")
sys.exit(0 if verdict else 1)
```

pass: true
