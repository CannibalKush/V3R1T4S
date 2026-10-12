# Lean 4 formalization: the reduction and the pruning rules of the Lehmer search

Lean 4 + Mathlib, written by our agents on 2026-10-09. Toolchain `leanprover/lean4:v4.35.0-rc4`, Mathlib
`v4.35.0-rc4` (exact revisions in `lake-manifest.json`). Sources only: `lake build` fetches Mathlib and builds
`.lake/`, which is not shipped.

```sh
lake build                                   # expect: Build completed successfully
echo 'import LehmerProof
#print axioms LehmerOracle.reduction
#print axioms LehmerOracle.node_conditions' > Axioms.lean && lake env lean Axioms.lean
```
There is no `sorry`, no `native_decide` and no added `axiom`. Every theorem depends only on Lean's standard axioms
`propext`, `Classical.choice` and `Quot.sound`. The prime lists used in the reduction are checked by the kernel
(`decide +kernel` on explicit divisor witnesses). Build output at release time: `../verify-it-yourself/RECEIPTS.md`.

## What it covers

**1. The reduction to the searched case below 10^56** (`LehmerProof/Reduction.lean`). `IsLehmer N` means
1 < N, N is not prime, and φ(N) | N − 1. Proved:
- Lehmer numbers are odd and squarefree, and their prime factors form a C-set: `odd_of_lehmer`, `squarefree_of_lehmer`,
  `cset_of_lehmer`.
- If N − 1 = k·φ(N) then k ≥ 2, and k ≡ 1 (mod 3) when 3 | N: `index_ge_two`, `index_mod_three`.
- An exact exchange argument bounds N/φ(N) by the smallest allowed primes: `dominate`, `ratio_bound`.
- **`reduction`**: `IsLehmer N → N ≤ 10^56 → ¬ 3 ∣ N ∧ (∀ p ∈ N.primeFactors, 5 ≤ p) ∧ N = 2 * φ N + 1`.
  This is Lemmas A and B of `../README.md`, formalized with the bound 10^56 (the search uses 10^50).

**2. Soundness of each pruning rule** (`LehmerProof/Search.lean`). For a genuine Lehmer number N ≤ 10^56, a prefix
T of its prime factors and the rest R, each rule the search uses to discard or close a node is a *necessary*
condition, so pruning by it cannot discard N:
- `c1` (prefix invariant P < 2Φ), `lo_bound` (q > 2Φ/A), `c2` (C-sequence gcd test), `cap` (c3/cap condition);
- `crt` (Lemma CRT: P·Q ≡ 1 (mod 8Φ) with P a unit), `euler` (Euler closure 2^((N−1)/2) ≡ 1 (mod N)),
  `child_dvd` (child filter), `c4` (next-primes ratio bound and the cap fixing m);
- `c2_closure` (two-prime closure and the candidate-closure quadratic identities);
- `node_conditions` bundles them.

## What it does NOT cover

- **The exhaustive search itself.** That no node of the 10^50 tree survives (65 647 subtrees, 0 solutions) is a
  computation by the C engines in `../engines/`, checked by rerunning them and by comparing their branch logs
  (`../verify-it-yourself/`), not by Lean.
- **That the C code walks that tree.** Nothing here proves that `lcrt5.c`, `vlrt2.c` or `lbb2.c` enumerate exactly the
  nodes these lemmas describe, apply the rules as stated, or implement the monotone scan stop and the next-prime
  enumeration correctly. The lemmas show the rules are sound; whether the programs follow them is established only by
  testing (positive controls, planted solutions, three engines agreeing).
- `lbb2.c`'s floating-point pruning (with one-sided safety margins) is not one of the formalized rules.

So the formal part removes the mathematical side of the argument from the list of things to trust; the computational
side still rests on the engines. The result as a whole is computer-verified and not peer reviewed.

## Files

`LehmerProof.lean` (root module), `LehmerProof/Reduction.lean`, `LehmerProof/Search.lean`, `lakefile.toml`,
`lean-toolchain`, `lake-manifest.json`, `.gitignore`. The default `LehmerProof/Basic.lean` placeholder of the Lake
template was not imported by anything and is not shipped.
