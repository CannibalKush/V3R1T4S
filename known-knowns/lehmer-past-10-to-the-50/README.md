# Lehmer's totient problem: every Lehmer number exceeds 10^50 (computer-verified, not peer reviewed)

**Claim (computer-verified).** There is no composite integer N ≤ 10^50 with φ(N) | N − 1.

**Status in one paragraph.** Lehmer's totient problem **remains open**; this is a lower bound, not a resolution. The
previous bounds are **10^26, certified** (Renze 2004) and **10^30, claimed** (Pinch 2006, no published certificate).
Our 10^50 is **computer-verified** (one exhaustive search run by three engines, two algorithms) and **not peer
reviewed**. A Lean 4 formalization (`lean/`) covers the reduction to the searched case and the soundness of each
pruning rule; it does **not** cover the exhaustive search itself (see `lean/README.md`).

Equivalently, any *Lehmer number* (a composite N whose Euler totient divides N − 1; D. H. Lehmer asked in 1932 whether
one exists) is larger than 10^50. The problem remains open: this is a lower bound obtained by an exact exhaustive
search, not a resolution. It has not been peer reviewed, and the search itself is not formalised in a proof assistant.

**Prior computational bounds.** Cohen and Hagis (1980) proved N > 10^20 (and ω(N) ≥ 14); Renze (2004) certified
N > 10^26 and ω(N) ≥ 15 (a computation published as a Mathematica notebook, not refereed); Richard Pinch's ANTS VII
poster (2006) **claims** N > 10^30 without a published certificate, so 10^26 is the largest previously certified bound
and 10^30 the largest previously claimed one; the Wikipedia article on the problem (revision of 2026-06-24, fetched
2026-10-08) still lists only the 10^20 bound and calls the problem unsolved. The case 3 | N was settled far beyond
this range long ago: Lieuwens (1970) gave ω(N) ≥ 212 and N > 5.5·10^570, Hagis (1988) ω(N) ≥ 298 848 and
N > 10^1 937 042, and Burcsi, Czirbusz and Farkas (2011) ω(N) ≥ 40 000 000 and N > 10^(3.6·10^8); the general reduction
lemmas below follow Lieuwens' and Kishore's (1977) arguments. The most recent related work is Mandal, Bhattacharjee and
Bhattacharya (Zenodo 10.5281/zenodo.23244062, Oct 2026; code at github.com/creelie/eLhmr), who prove ω(N) ≥ 16 with
Lean-formalised lemmas and state no magnitude bound. Yamada (arXiv:2303.16853) surveys the state of the problem.
So 10^50 is 20 orders of magnitude beyond the claimed 10^30 and 24 beyond the certified 10^26, as far as we could find
(arXiv, Zenodo, MathOverflow, OEIS and Wikipedia were searched on 2026-10-08).

## What is being verified, and by what

Write N − 1 = k·φ(N). Standard facts: N is odd and squarefree, k ≥ 2, and no prime factor p of N divides q − 1 for
another prime factor q (otherwise p | φ(N) | N − 1 and p | N); also N/φ(N) = k + 1/φ(N) > k.

1. **Lemma A (3 | N is impossible below 10^50).** If 3 | N every other prime factor is ≡ 2 (mod 3), so φ(N) ≡ 2 and
   N − 1 ≡ 2 (mod 3), hence k ≡ 1 (mod 3) and k ≥ 4, so N/φ(N) > 4. But for N ≤ 10^50 built from 3 and primes ≡ 2
   (mod 3) the ratio N/φ(N) is at most the product of p/(p−1) over the greedy prefix 3, 5, 11, 17, … of length 27, which
   is 2.928933… < 4. (Hagis and Burcsi–Czirbusz–Farkas prove much more for this case; the lemma is included so that
   the result is self-contained.)
2. **Lemma B (k = 2).** If 3 ∤ N all prime factors are ≥ 5 and N/φ(N) ≤ ∏ p/(p−1) over 5, 7, 11, …, 131 (30 primes),
   which is 2.949927… < 3, so k = 2: **N − 1 = 2 φ(N)** with all prime factors ≥ 5.
   `verify-it-yourself/closures.py` recomputes both lemmas in exact rational arithmetic with its own prime table (both still hold
   at 10^56; Lemma B fails at 10^58, which is where a k = 3 search would become necessary).
3. **Exhaustive search of N − 1 = 2 φ(N), primes ≥ 5, N ≤ 10^50.** A branch-and-bound over prime prefixes
   π = (p_1 < … < p_j): write P = ∏p_i, Φ = ∏(p_i − 1); a prefix is viable only if P < 2Φ (admissibility and the
   deficit A = 2Φ − P > 0 bound the remaining primes), and the remaining cofactor Q must satisfy the congruence
   Q ≡ P⁻¹ (mod 8Φ) when at least two primes remain (Lemma CRT in `engines/SPEC_LCRT_r1.md`). A node with one
   remaining prime is closed by division; a node with exactly two is closed either by scanning the finite interval of
   possible q with the exact divisibility test (A q − 2Φ) | (2Φ(q−1) − 1), or by testing each congruence candidate Q for
   q + r = Q − Ψ + 1 with a perfect-square discriminant; a node with few congruence candidates is closed by Euler's
   criterion 2^((N−1)/2) ≡ 1 (mod N), which every solution of N − 1 = 2φ(N) satisfies. All arithmetic is exact (GMP);
   floating point appears only as a filter with an exact fallback. The exact definitions, the completeness proof of the
   tree and the canonical per-subtree output are in `engines/SPEC_LCAP1.md`, `SPEC_LCRT_r1.md` and `SPEC_LCRT5.md`.

   The search is split into **65 647 subtrees** (prefixes of 11 primes). Each engine run writes one JSON line per
   subtree with per-depth counts (visited nodes, live nodes, Euler closures and passes, integral two-prime completions)
   and two 64-bit digests, so that different engines can be compared subtree by subtree.

4. **Results at X = 10^50.**

   | engine | what it is | run | visited nodes | live nodes | Euler closures (passes) | integral two-prime completions | solutions |
   |---|---|---|---|---|---|---|---|
   | `lcrt5.c` (author engine) | C + GMP, 8 worker processes | mode LCRT-4, prime sieve to 10^9 plus segmented sieve; 1 468 s wall | 2 169 013 803 (digest `74e2002af271a197`) | 130 205 304 (`7c1d8e5190f9754f`) | 102 312 897 (0) | 0 | 0 |
   | `lcrt5.c` | same engine, different mode | mode LCRT-6, sieve to 4 294 967 291, candidate closure + trial division; 784 s | identical on every mode-independent field, all 65 647 subtrees | identical | identical | 0 | 0 |
   | `vlrt2.c` (independent engine 1) | written from the author's specification documents only (author's code not read), so it is independent in code but not in design; C + GMP, pthreads | all 65 647 subtrees (62 061 in one run of 601 s wall / 4 094 s CPU on 8 threads, 3 586 in an earlier partial run) | identical to both author runs, subtree by subtree, on nodes, live, small, Euler closures/passes, c2i, kfilt and both digests | identical | identical | 0 | 0 |
   | `lbb2.c` (independent engine 2) | written from the definition with a different algorithm: a different tree (41 170 depth-11 tasks), different closures, its own prime source, and floating-point pruning of m ≥ 3 branches with one-sided safety margins (see Limitations); C + GMP | full run, 10 workers, 24 min | 3 805 754 261 (summed over generator and workers) | — | 241 524 181 Euler tests (0 passes) | 0 (1 713 809 944 q-tests, 220 780 104 congruence candidates) | 0 |

   The whole 10^50 search was therefore executed three times with two different algorithms, and the two engines that
   share the algorithm agree on every one of the 65 647 subtree records. `verify-it-yourself/recompute_summary.py` re-derives the
   totals and digests above from the shipped per-subtree logs; `verify-it-yourself/diff_runs.py` performs the subtree-by-subtree
   comparison; `verify-it-yourself/lbb2_aggregate.py` checks the lbb2 run for completeness (every task done exactly once with the
   right prefix, no event line). Output at release time: `verify-it-yourself/RECEIPTS.md`.

5. **Side checks** (recorded in `certificates/` and `branch_logs/`, not needed for the theorem):
   the 60 two-prime intervals that the LCRT-4 run had to scan beyond its main sieve were closed a second way by
   factoring D = 4Φ² − 2ΦA − A (`xcheck_segc2_1e50.jsonl`; the factors are BPSW probable primes, so this check is
   numerical) and their prime counts agree with an independent prime-counting function (`…_primepi.jsonl`); both
   author modes and vlrt2 find the six known solutions of the companion equation N + 1 = 2φ(N) (15, 255, 65535,
   83623935, 4294967295, 6992962672132095) and all planted solutions in positive-control runs; lbb2 matched a plain
   reference enumeration on planted instances in 49/49 configurations up to 10^16 (`lbb2_planted_final.out`) and its
   segmented sieve agrees with sympy's primes on sampled ranges (`lbb2_selftest.log`).

## Limitations

- **Internal verification only.** The three engines were written by three agents of the same team within
  one day on one machine; two of them (lcrt5, vlrt2) implement the same specification: vlrt2 was written from the
  author's spec documents without reading the author's code, so a mistake in the spec itself would be shared. lbb2 is
  the engine with a different algorithm.
  No outside number theorist has rerun anything yet. A rerun of `vlrt2` and `lbb2` from source on a different machine
  and compiler, reproducing the digests above and 0 solutions, is the verification we are asking for.
- **Partly formalised.** `lean/` (Lean 4 + Mathlib, no `sorry`, standard axioms only) proves the reduction
  (a Lehmer number N ≤ 10^56 has 3 ∤ N, all prime factors ≥ 5 and N = 2φ(N) + 1) and that every pruning or closing
  rule of the search is a necessary condition on a genuine N ≤ 10^56. It does **not** verify the exhaustive search,
  nor that the C code walks exactly the tree those lemmas describe. See `lean/README.md`.
- The lbb2 engine prunes its m ≥ 3 branches with a double-precision bound carrying one-sided safety margins; it can
  only fail to prune, never prune wrongly, but it is the one non-integer step in any of the three engines. Its
  completeness was tested on planted instances up to 10^16, not proved.
- The D-factorisation side check labels its factors "prime" on the strength of sympy's BPSW test; it is a cross-check,
  not part of the proof.
- The author engine's runs beyond 10^50 (10^52 and a 10^54 run in progress at release time) are **not** part of this
  release: they have no independent reproduction.
- Lower bound only; the problem is open. Computer-verified, not peer reviewed.

## Files

How the shipped logs and certificates were generated, step by step (engine build, runs, merge, union, certificates,
tarballs), is in [`how-we-built-it/README.md`](how-we-built-it/README.md); how the search was found and what failed
along the way is in [`HOW_WE_FOUND_IT.md`](HOW_WE_FOUND_IT.md).

```
README.md, RUN_IT_YOURSELF.md, HOW_WE_FOUND_IT.md
engines/
  lcrt5.c                 author engine (C + GMP); SPEC_LCAP1.md, SPEC_LCRT_r1.md, SPEC_LCRT5.md define its tree, modes and output
  merge_lcrt.py           sums an lcrt5 run directory into a summary JSON (the author's tool)
  certify.py              author's certificate script: Lemmas A/B + bookkeeping of a summary (needs sympy)
  taskdiff_r2.py          author's per-task diff for two lcrt5 runs
  xcheck_segc2.py         author's algebraic closure of beyond-sieve two-prime intervals (needs sympy)
  vlrt2.c                 independent engine 1 (spec-only reimplementation, C + GMP + pthreads)
  lbb2.c, lemmas.py       independent engine 2 (different algorithm, C + GMP) and its own re-derivation of Lemmas A/B (needs sympy)
branch_logs/
  lcrt5_1e50_LCRT4_tasks.tar.gz          author run, mode LCRT-4: master.json + 65 647 task lines + DONE
  lcrt6_1e50_bigsieve_LCRT6_tasks.tar.gz author run, mode LCRT-6
  vlrt2_full50_union.tasks.jsonl.gz      independent engine 1, all 65 647 subtrees (= r50c run + earlier partial run)
  vlrt2_r50c.tasks.jsonl.gz, vlrt2_r50c.summary.json, vlrt2_r50c.log   the 62 061-subtree run and its top-tree record
  vlrt2_verifier_v6_50_merged.tasks.jsonl.gz                          the earlier 3 586-subtree run
  lbb2_e50_S1000000000_tasks.tar.gz      independent engine 2: generator output (41 170 tasks) and 10 worker logs
  lbb2_agg_e50.json, lbb2_selftest.log, lbb2_planted_final.out
certificates/
  certificate_lcrt5_1e50.json, certificate_lcrt6_1e50_bigsieve.json   certify.py output for the two author runs
  lcrt5_1e50.summary.json, lcrt6_1e50_bigsieve.summary.json, *.log   the summaries and run logs they certify
  xcheck_segc2_1e50.jsonl, xcheck_segc2_1e50_primepi.jsonl             side checks (section 5)
lean/                     Lean 4 formalization of the reduction and of each pruning rule (sources only; see lean/README.md)
verify-it-yourself/
  closures.py, recompute_summary.py, diff_runs.py, lbb2_aggregate.py, run_checks.sh   (python3 only, no dependencies)
  RECEIPTS.md             output of the checks (2026-10-10 run)
how-we-built-it/
  README.md               end-to-end pipeline with the recorded commands and runtimes; SMOKE.md (tiny rerun)
  run_lcrt5_job.sh, run_lbb2_parallel.sh   drivers of the certified LCRT-4 run and of the lbb2 run
  lcrt5_v1_LCRT4.patch, merge_lcrt_v1.patch   the engine/merge revision that produced the LCRT-4 log and summary
  vlrt2_union.py          task-list, merge and union steps that assembled the vlrt2 log
```

## References

- D. H. Lehmer, *On Euler's totient function*, Bull. Amer. Math. Soc. 38 (1932) 745–751.
- E. Lieuwens, *Do there exist composite numbers M for which kφ(M) = M − 1 holds?*, Nieuw Arch. Wisk. (3) 18 (1970) 165–169.
- M. Kishore, *On the number of distinct prime factors of n for which φ(n) | n − 1*, Nieuw Arch. Wisk. (3) 25 (1977) 48–53.
- G. L. Cohen, P. Hagis Jr., *On the number of prime factors of n if φ(n) | (n − 1)*, Nieuw Arch. Wisk. (3) 28 (1980) 177–185.
- P. Hagis Jr., *On the equation M·φ(n) = n − 1*, Nieuw Arch. Wisk. (4) 6 (1988) 255–261.
- J. Renze, *Computational evidence for Lehmer's totient conjecture* (Mathematica notebook, 2004), as cited by Yamada.
- R. G. E. Pinch, *A note on Lehmer's totient problem*, poster, ANTS VII (2006).
- P. Burcsi, S. Czirbusz, G. Farkas, *Computational investigation of Lehmer's totient problem*, Ann. Univ. Sci. Budapest. Sect. Comput. 35 (2011) 43–49.
- T. Yamada, arXiv:2303.16853 (v3, 2023).
- Mandal, Bhattacharjee, Bhattacharya, Zenodo doi:10.5281/zenodo.23244062 (2026).
