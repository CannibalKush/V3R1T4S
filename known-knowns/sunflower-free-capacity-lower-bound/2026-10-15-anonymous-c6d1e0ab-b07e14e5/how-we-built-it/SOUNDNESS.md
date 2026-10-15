# Soundness note for the exact values g(n,r) (written for a referee)

Team sunflower, 2026-10-14. Author: fable-sun (reviewer of the pipeline); the SAT pipeline, the families and
the proofs are opus-sun's. Status of every value: PROMISING until the orchestrator's independent panel.
This note explains why each claimed value is correct given the artifacts in this folder, what each step
relies on, and exactly what a referee has to re-run. Nothing here uses floating point.

## 0. The claim

g(n,r) is the largest size of a family F of r-element subsets of [n] = {1,...,n} such that no three DISTINCT
members A, B, C satisfy A∩B = A∩C = B∩C (a 3-sunflower; the common intersection may be empty, so three
pairwise disjoint members count as a sunflower). For each row of INDEX.md we claim g(n,r) = v, with

- a lower bound: an explicit family of v distinct r-subsets of [n] that is sunflower-free (family.json);
- an upper bound: either a checked UNSAT proof that no sunflower-free family of v+1 r-sets exists (section 2),
  or the link-lemma step g(n,r) <= floor(n g(n-1,r-1)/r) from a previously established value (section 5).

Twenty-two values: g(6,3)=10, g(7,3)=12, g(7,4)=15, g(7,5)=12, g(8,3)=12, g(8,4)=24, g(8,5)=22, g(8,6)=16, g(9,3)=14,
g(9,4)=27, g(9,5)=42, g(9,6)=32, g(9,7)=20, g(10,3)=16, g(10,4)=31 (case split, section 10), g(10,6)=70, g(10,7)=44 (case split, section 10), g(10,8)=25, g(11,3)=16, g(11,7)=110, g(12,3)=20,
g(12,8)=165.

## 1. Lower bounds: the families

Each family.json is checked by two programs written independently (opus-sun):
`tools/check_family.py` (standard library; structure check, then three sunflower tests: A, pairwise cores with
column bitsets; B, per-member trace classes whose residuals must pairwise intersect; C, the literal definition on
all triples) and `tools/sfcheck.c` (for every pair {A,B} every r-set C with C∩(A∪B) = A∩B is looked up in a
hash of the members). `verify_all.py` re-runs both on every family and also checks the controls: a family with
three pairwise disjoint sets must be rejected by both. Family sizes are compared with the claimed values by
`tools/build_index.py`. A referee who trusts neither program can test any family by brute force over all
C(v,3) triples in a few lines; for v = 165 that is 735,130 triples.

## 2. Upper bounds by SAT: what the CNF says

`tools/gen_cnf.py n r k out.cnf --sb {none|alltrans} [--deg D]` writes a DIMACS CNF whose satisfying assignments
are exactly (the indicator vectors of) sunflower-free families of at least k r-subsets of [n], up to the
restrictions discussed in sections 3 and 4. Variables 1..M, M = C(n,r), are the r-subsets in colex order; the
map is printed in the CNF as comment lines `c var i e1 ... er`. The clauses are

(a) one ternary clause (-A -B -C) for every unordered triple {A,B,C} that is a 3-sunflower. The generator
    enumerates them as: a core K of size t (0 <= t <= r-1) and three pairwise disjoint (r-t)-subsets of [n]\K.
    Every 3-sunflower has this form exactly once (its core is K = A∩B, its petals A\K, B\K, C\K are pairwise
    disjoint), and every such triple is a sunflower. INDEPENDENT CHECK: `tools/triples_recheck.py file.cnf`
    re-derives the set of sunflower triples by brute force over all C(M,3) triples of r-sets using the literal
    definition (pairwise equal intersections), and compares it with the set of ternary all-negative clauses over
    the original variables in the file. verify_all.py runs it on every CNF; all 27 CNFs report MATCH (for
    example 2520 triples for (9,5), 17920 for (10,3), 54670 for (11,3), 152680 for (12,3)).
(b) the cardinality constraint sum_i x_i >= k, encoded by PySAT's `CardEnc.atleast` with the sequential
    counter (Sinz 2005). We use only its standard property: for every assignment of x_1..x_M with at least k
    ones, the auxiliary variables can be set so that all clauses of the encoding hold. (A referee who prefers
    not to rely on PySAT can regenerate with `--card totalizer` and re-solve; the UNSAT verdict does not depend
    on the encoding chosen.)
(c) optional degree cuts (section 4) and optional lex-leader symmetry breaking (section 3).

The clause set is S_n-invariant for (a), (b) and (c-degree): relabelling the points maps sunflowers to
sunflowers, preserves |F| and permutes point degrees.

So if the CNF for (n, r, k=v+1) is unsatisfiable, then there is no sunflower-free family of v+1 r-subsets of
[n] satisfying the added restrictions, and sections 3 and 4 show the restrictions lose no family that matters.
Hence g(n,r) <= v. Since a family of size v exists (section 1), g(n,r) = v. Monotonicity in k is not needed:
a family of size > v+1 contains one of size exactly v+1, and the constraint is `>= k` anyway.

The UNSAT verdicts come from glucose4 (through PySAT) with DRUP proof logging; the solver is NOT trusted.
Each proof is checked by two independent programs (section 6).

## 3. Lex-leader symmetry breaking (rows (9,3), (9,5), (9,6), (10,3), (10,8), (11,3), (12,3))

Nine rows have a proof of the plain CNF (sb=none) and need nothing from this section: (6,3), (7,3), (7,4), (7,5),
(8,3), (8,4), (8,5), (8,6), (9,7). Seven rows currently have proofs only with lex-leader constraints
(`--sb alltrans`); the argument that these constraints are sound follows.

Setup. Fix the variable order 1..M (colex order of the r-subsets S_1, ..., S_M). A family F corresponds to
x in {0,1}^M with x_i = [S_i in F]. For a permutation pi of [n] let pi.F = {pi(A) : A in F}; pi.F is
sunflower-free iff F is, |pi.F| = |F|, and the degree of point pi(p) in pi.F equals the degree of p in F. So
the set of solutions of clauses (a), (b), (c-degree) is a union of S_n-orbits.

The added constraints. For every transposition tau = (a b) of two points, the generator adds the clauses
of "x <=_lex y" where y_i = x_{j(i)} and S_{j(i)} = tau(S_i). Because tau is an involution, y is the indicator
vector of tau.F (equivalently of tau^{-1}.F; they coincide). Positions i with tau(S_i) = S_i are skipped: there
x_i = y_i, so the lexicographic comparison restricted to the moved positions, in increasing index order,
equals the full comparison (the first index where x and y differ is a moved index).

Encoding. With the moved positions i_1 < i_2 < ... < i_m, auxiliary variables e_1, ..., e_{m-1} and e_0 = true:
    (not e_{t-1} or not x_{i_t} or y_{i_t})            for t = 1..m      ("if the prefix agrees and x=1 then y=1")
    (not e_{t-1} or x_{i_t} or y_{i_t} or e_t)         for t = 1..m-1    ("prefix agrees and both 0 -> e_t")
    (not e_{t-1} or not x_{i_t} or not y_{i_t} or e_t) for t = 1..m-1    ("prefix agrees and both 1 -> e_t")
(for t = 1 the literal not e_0 is omitted). Note that nothing forces e_t false; it only ever appears as a
hypothesis, so a referee can read the encoding as "e_t true is allowed to mean: positions up to t agree".

Soundness claim. If the plain CNF (sections 2(a), 2(b), optionally 4) is satisfiable, so is the CNF with all
lex-leader clauses added. Proof. Take any solution F. Its orbit {pi.F : pi in S_n} is a finite set of
solutions; let F* be the one whose indicator vector x* is lexicographically least (in the fixed variable
order). For any transposition tau, tau.F* is in the orbit, so x* <=_lex indicator(tau.F*) = y, which is exactly
the constraint added for tau. For the auxiliary variables set e_t := [x*_{i_s} = y_{i_s} for all s <= t]. Check
the three clause types: if e_{t-1} holds (prefix agrees) and x*_{i_t} = 1, then since x* <=_lex y and all
earlier positions agree we must have y_{i_t} >= x*_{i_t}, i.e. y_{i_t} = 1; if the prefix agrees and
x*_{i_t} = y_{i_t} then e_t is true by definition. All clauses hold, so the extended CNF is satisfiable. QED

Consequently UNSAT of the symmetry-broken CNF implies UNSAT of the plain CNF, which is the statement
g(n,r) <= v. Only the lex-least orbit element is used; completeness of the symmetry breaking (that it
excludes everything but the lex-least element) is neither claimed nor needed. Using only transpositions, a
subset of S_n, adds fewer constraints than full lex-leader breaking and is sound for the same reason.

Mechanical check that the constraints are built as described: `verify_all.py` regenerates every CNF from the
(n, r, k, sb, deg) parameters in its header with `tools/gen_cnf.py` and compares byte-for-byte, so the file
that was proved unsatisfiable is the file this description refers to (for CNFs written before the --deg option
existed only the first comment line differs, by the field 'deg<=none'; the clause bodies are byte-identical).
The generator is 122 lines of Python and the lex-leader block is lines 73-104.

Empirical check of the claim itself (NUMERICAL, `tools/sb_sanity.py`, output in second_method/sb_sanity.out): for
(n,r,k) = (5,2,5), (6,3,9), (6,3,10), (7,3,11), (7,3,12), (7,4,15), (8,4,24) ALL solutions of the plain CNF were
enumerated (12, 132, 12, 5460, 420, 252, 840 families), grouped into S_n-orbits (1, 2, 1, 3, 1, 1, 1 orbits), and
every orbit was found to contain a family for which the symmetry-broken CNF is satisfiable, while no SB solution
lies outside the plain solution set. The script needs python-sat and runs in under a minute. (Side observation,
NUMERICAL: the extremal families for (5,2), (6,3), (7,3), (7,4) and (8,4) are unique up to isomorphism.)

## 4. Degree cuts (variants sb_deg24 of (9,5), sb_deg6 of (10,3), sb_deg16 of (11,3), sb_deg6 of (12,3))

`--deg D` adds, for every point p, the constraint "at most D members contain p" (PySAT `CardEnc.atmost`,
sequential counter). This is valid when D >= g(n-1, r-1):

Link lemma (core size 1). For a sunflower-free r-uniform F on [n] and a point p, the link
F_p = {A \ {p} : p in A in F} is an (r-1)-uniform family on [n] \ {p}, its members are distinct (A is
recovered as (A\{p}) ∪ {p}), and it is sunflower-free: if A\p, B\p, C\p had pairwise equal intersections K,
then A, B, C would have pairwise equal intersections K ∪ {p}. Hence deg(p) = |F_p| <= g(n-1, r-1).

Justification of each cut used: (9,5) with D = 24 = g(8,4), which has a plain-CNF proof in this folder;
(10,3) with D = 6 = g(9,2); (11,3) with D = 16 >= 6 = g(10,2) (a weaker cut than necessary, still valid); (12,3) with
D = 6 = g(11,2).
The base value g(m,2) = 6 for m >= 6 (PROVED-HERE, elementary): a 2-uniform family is a graph; two distinct
edges meet in at most one vertex, so three edges with pairwise equal intersections are either three pairwise
disjoint edges or three edges through one vertex. Sunflower-free therefore means maximum degree <= 2 and
matching number nu <= 2. Such a graph is a disjoint union of paths and cycles; a path with e edges has
nu = ceil(e/2) >= e/2, a cycle with e >= 3 edges has nu = floor(e/2) >= (e-1)/2 and nu >= 1, so e <= 3 nu for
every component and in total |E| <= 3 nu(G) <= 6. Two disjoint triangles (6 vertices) attain 6. So g(9,2) =
g(10,2) = g(11,2) = 6. (Only these base values are used by any row; `tools/build_index.py` checks every degree cut
against the predecessor value and refuses to mark a row established otherwise.)

Degree cuts are S_n-invariant (section 2), so they combine with lex-leader breaking (section 3) without
further argument: the lex-least element of the orbit of any solution still satisfies them.

## 5. The link-lemma chain (rows (9,4), (10,6), (11,7), (12,8))

Counting both sides of the incidences (p, A) with p in A in F and using section 4's lemma,
    r |F| = sum_p deg(p) <= n g(n-1, r-1),   so   g(n,r) <= floor(n g(n-1, r-1) / r).
Each chain row has `derivation.json` with the predecessor it uses and the integer computation, and a family of
exactly that size (checked as in section 1):
    g(9,4)  <= floor(9*12/4)   = 27   from g(8,3) = 12   (plain proof);        family of 27 exists.
    g(10,6) <= floor(10*42/6)  = 70   from g(9,5) = 42   (section 3 proof);    family of 70 exists (S_5 on pairs of [5]).
    g(11,7) <= floor(11*70/7)  = 110  from g(10,6) = 70  (chain);              family of 110 exists (PSL(2,11) orbit).
    g(12,8) <= floor(12*110/8) = 165  from g(11,7) = 110 (chain);              family of 165 exists (M11 orbit).
`tools/chain_check.py` re-does this arithmetic from the manifests and the derivation files and checks the family
sizes; it refuses a row whose predecessor is not itself established in this folder.

Dependency graph (what each value rests on):
    plain CNF proofs: (6,3) (7,3) (7,4) (7,5) (8,3) (8,4) (8,5) (8,6) (9,7)
    lex-leader proofs: (9,3); (9,6); (10,8) [also = floor(10*20/8) from (9,7)]; (9,5) [two encodings: SB alone,
      and SB + deg<=24 using (8,4)]; (10,3) [SB + deg<=6 using g(9,2)=6]; (11,3) [SB + deg<=16 using g(10,2)=6];
      (12,3) [SB + deg<=6 using g(11,2)=6]
    chain: (9,4) <- (8,3);  (10,6) <- (9,5);  (11,7) <- (10,6);  (12,8) <- (11,7)
The single most important node is (9,5) = 42: three further values hang on it. It has THREE UNSAT proofs of
(9,5)@43 from three different CNFs: lex-leader SB alone and SB + deg<=24 (both checked by both checkers, in
opus_packages/g_9_5_42/), and a PLAIN CNF with the degree cut deg<=24 only (no symmetry breaking; glucose4 1289 s,
1.07 GB DRUP, drat-trim `s VERIFIED` in 1005 s, 0 RAT lemmas; record in opus_packages/g_9_5_42/plain_deg24_record/
with the CNF, the verifier output and the SHA-256 of the proof file, which was deleted under the 100 MB rule and can
be regenerated by re-solving). Since g(8,4) = 24 has a plain proof, the values (9,5), (10,6), (11,7), (12,8) do not
depend on section 3 at all; only (9,3), (9,6), (10,3), (10,8), (11,3), (12,3) still rest on the lex-leader argument.

## 6. Proof checking

Each UNSAT proof is in DRUP format (clause additions and deletions; no RAT steps are needed and drat-trim
reports "0 RAT lemmas"). It is checked by

- `drat-trim` (Heule and Wetzler; source `tools/drat-trim.c`, compiled by verify_all.py), backward checking with
  core extraction; success line `s VERIFIED`;
- `tools/drup_check2.c` (opus-sun), a short forward checker: every added lemma must be RUP (unit propagation on
  the formula plus previously added, not yet deleted lemmas, after asserting the lemma's negation, reaches a
  conflict); deletions are applied; success requires the empty clause to be derived or a top-level conflict.
  It accepts the same proofs and rejects the controls (section 7).

Both checkers read the CNF from this folder, so a proof is only accepted for the exact formula described in
sections 2-4. The two checkers share no code.

## 7. What verify_all.py does, and the controls

`./verify_all.sh` (copy the folder anywhere first; needs python3, cc, and for CNF regeneration a python with
python-sat given as PYSAT=...) runs single-threaded: compiles the three C tools; checks every family with both
programs; for every proof variant recomputes the sunflower clauses by brute force, runs both proof checkers,
regenerates the CNF and compares byte-for-byte; negative controls (a truncated proof and a proof of a different
formula must be rejected by both checkers; a family with three disjoint sets must be rejected by both family
checkers); the second method (section 8) on the fast cases; `chain_check.py`; `build_index.py --check`. It prints
one PASS/FAIL line per check and a total; outputs are kept in `verify_out/`. The run on the clean copy made on
2026-10-14 is recorded in REPORT.md.

## 8. Second method, independent of SAT

`tools/exact_bb.py` (fable-sun) is an exhaustive branch-and-bound written directly from the definition with no
SAT or CP library; it finished for (7,3), (7,4), (8,3), (8,4), (9,3) and found the same maxima 12, 15, 12, 24, 14
(second_method/). It fixes the first set to {1..r}, which is valid because S_n is transitive on r-sets, and
prunes with the counting bound and the (r-1)-shadow bound (every (r-1)-set lies in at most two members: three
members through one (r-1)-set form a sunflower with that core). Five of the twenty-two values are thus confirmed
by a method sharing nothing with the SAT pipeline; the others are confirmed only by the two proof checkers.

## 9. What is NOT claimed, and known limits

- Novelty: we could read only the bank's three sources (Naslund-Sawin 2017, Frankl-Pach-Palvolgyi 2024,
  Tang-Zhang 2025) and the bank page; none tabulates g(n,r). Whether any of these values appears in the
  literature on Delta-systems / sunflower-free families (for example in the Abbott-Hanson-Sauer or
  Erdos-Szemeredi line of work) was NOT checked. Partial win p2 requires "not previously published": a referee
  must check this.
- An earlier note by fable-sun claimed g(10,3) = 20 via the stars of K5 on the edges of K5; that family contains
  three pairwise disjoint triples and is NOT sunflower-free. The claim was withdrawn on 2026-10-14 and the
  correct value g(10,3) = 16 is row (10,3) of this candidate (found by opus-sun).
- SPECULATION (unverified memory of both agents, no source read): Abbott, Hanson and Sauer may have shown that a
  3-uniform family with no 3-sunflower has at most 20 members on any ground set; our row g(12,3) = 20 and the
  sequence 10, 12, 12, 14, 16, 16, 20 for n = 6..12 would be consistent with that. If true, g(12,3) is a known value.
- CP-SAT and local search were used only to FIND families; nothing depends on them.
- The exact comparison with the 1.5545 bar in the family checker is integer arithmetic; it is irrelevant here
  (no value comes near the bar) and included only because the checker is shared with the main target.
- All runs were on one machine; the proofs are machine-checked but a referee should re-run verify_all.sh on
  their own machine (minutes; the longest single step is drat-trim on the 48 MB plain proof of (8,3), about
  45 s).

## 10. Case-split proofs: g(10,4) = 31, g(10,7) = 44, the bound g(11,4) <= 38, and the earlier bound g(10,4) <= 32

Row (10,4) = 31 is proved by a case split rather than by one UNSAT proof (ARGUMENT.md in its folder; the
index marks it 'case-split'). The simpler bound g(10,4) <= 32 in bounds/g_10_4_le32/ shows the method: a 33-family would have a point of degree
14 = g(9,3) (4*33 = 132 > 13*10), whose link is an extremal (9,3)-family; all such families are classified into two
isomorphism classes A and B (enumeration of all 18 lex-leader models of `gen_cnf 9 3 14 --sb alltrans --deg 6`, a
verified UNSAT proof that no further model exists, canonical forms by brute force over 9!); after relabelling, the
link of point 1 is exactly A or exactly B, and the two resulting CNFs (NO symmetry breaking, valid restricted-link
cuts, 84 unit clauses) are UNSAT with verified DRUP proofs. The ingredients are the ones of sections 2-4 plus one
new one, the restricted-link cuts: for disjoint point sets I, O the members X with I subset X and X disjoint from O,
with I removed, form a sunflower-free (r-|I|)-uniform family on [n] minus (I u O) (a subfamily of the link at I), so
their number is at most any valid upper bound U(n-|I|-|O|, r-|I|); the bounds used are rows of this candidate. Note
that symmetry breaking must NOT be combined with the unit clauses that fix the link (fixing breaks the symmetry);
the case CNFs have none. The folder's README.md gives the full argument, the dependencies and fable-sun's
independent re-checks (fable_check/). The exact row g(10,4) = 31 (opus_packages/g_10_4_31/) refines this: a 32-family has maximum degree 14 (link A or B,
2 cases, no degree cap) or exactly 13 (4*32 = 128 > 120), and then some point of degree 13 has as link one of the 13
isomorphism classes of sunflower-free 13-triple families on 9 points (classified by enumerating all 162 lex-leader
models of `gen_cnf 9 3 13 --sb alltrans --deg 6`, verified completeness proof, canonical forms by brute force; the
deg <= 13 cap is valid in this branch). All 15 case CNFs (NO symmetry breaking, cuts, 84 units) are UNSAT with
verified proofs. The classification argument for 13-families: the lex-least relabelling of any 13-family is a model,
hence contains an enumerated model, which has size <= 13 and therefore equals it. fable-sun re-derived the model
partition into the 13 classes with an independent isomorphism search, checked the blocking clauses, headers and
units of every case CNF, re-ran drat-trim on all 19 proofs and regenerate.sh in a clean copy (NOTES.md section 11).
The same method gives g(10,7) = 44 (opus_packages/g_10_7_44/: a 45-family has a point of degree 32 = g(9,6); the 311
lex-leader models of (9,6)@32 fall into 6 classes; 6 fixed-link cases UNSAT) and the upper bound g(11,4) <= 38
(opus_packages/bound_g_11_4_le38/: max degree 16 or 15; one class of 16-families and two of 15-families on (10,3);
3 fixed-link cases UNSAT; two proofs stored gzipped with the raw files' SHA-256). fable-sun re-ran the same
independent checks on both (fable_check/ in each folder). Bound packages appear in INDEX.md in a separate table;
they are never used as predecessors for exact rows.
What the index checks mechanically for a case-split row: every case CNF claims |F| >= v+1 with sb=none, has a proof,
and both checkers report VERIFIED in solve_log.txt; verify_all.py re-runs both checkers and the brute-force clause
recheck on every case and completeness proof and the package's regenerate.sh. The COMPLETENESS of the case list
(that the cases cover every possible family) is a mathematical argument (ARGUMENT.md), not a machine check; a
referee should read it. The consequence is g(14,8) <= floor(1001*31/70) = 443 < 482.
