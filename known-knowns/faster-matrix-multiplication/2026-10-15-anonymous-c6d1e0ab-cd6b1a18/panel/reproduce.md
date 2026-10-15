REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: pass for the saved-object scope assigned to this skeptic. The saved 5x5x8 program computes the integer matrix product exactly with 144 products and 556 reduced additions. This verdict uses the package's definition of each term list as a sum; an explicit ternary binary association is supplied and replayed below. It makes no judgment about a live record or novelty.

Scope: I read only this folder's package and used the permitted Python interpreter for the author's SymPy cross-check. No network was used. Perminov's third-party reference scheme is not shipped. Its URL and claimed SHA-256 in table-record/README.md are metadata, so I cannot recount its 620 additions, authenticate its hash, or prove that its expanded products equal this object's products. Likewise, the external table responses underlying the other recorded hashes are absent. Best listed rank, live minimum, coefficient-class comparisons, currency, and novelty are outside this verdict and belong to the other two skeptics. The inequality 556 < 620 below is arithmetic against the saved INDEX.csv value, not an independent validation of the external reference.

Definition and criterion quoted from CLAIM.md follow. Only the angle brackets around the format placeholder in the criterion have been changed to braces. The Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only its placeholder brackets have been changed.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The saved-object layout and exact counting definition are:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

The additional expanded-coefficient requirement is quoted from CLAIM.md's description of the verifier:

> the ternary condition on every expanded intermediate

I fixed the definition in skeptic/definition.md and wrote skeptic/check.py before reading any file in verify-it-yourself/ or REPRODUCE.md. The first independent run, the association refinement, the successful full run, and its repeat all preceded author-code access. No author code is imported into either independent checker.

Properties checked and proof reconstructed:

1. Schema, object identity, and order: strict JSON parsing rejects duplicate keys. Dimensions are exactly [5,5,8], all at most 8; m is the integer 144, and z2 is false. U and V have 144 final rows each; W has 40. Each form is nonempty, each index is an integer referring to an input or an earlier fresh variable, and each literal coefficient is exactly integer +1 or -1. Final forms cannot reference other final forms. Every product has nonzero factors and is used. The object's bytes hash to the SHA-256 in INDEX.csv, whose target, cell, file, and value also match.
2. Ternary expansion: start with unit vectors for the 25 A inputs, 40 B inputs, or 144 formal product inputs. For each fresh form, sum its signed source vectors over the integers and append the resulting vector. Expand final forms the same way. All 392 fresh forms and 328 final forms (720 total) have only -1, 0, or +1 as expanded coefficients. W is expanded over independent product symbols, rather than treating those symbols as independent A or B entries.
3. Binary association detail: the initial checker imposed the stronger, unspecified requirement that every term list be left-associated in its listed order. That failed at zero-based w.final[6], after terms 0,1,2: formal product coefficients 32 and 133 were -2. The initial output is retained in skeptic/initial_prefix_diagnostic.txt. CLAIM.md defines a form as a sum of terms and does not fix its binary association. Before reading author code, I therefore constructed, for every form, a term permutation whose partial sums are all ternary, using exact subset reachability. A subset's vector sum is independent of its ordering, so one reachable order per subset suffices. All forms have witnesses; no sampled association search is used. This four-term form uses order [0,1,3,2]. Every term still occurs exactly once, each source reference is unchanged, and a q-term form still costs q-1 additions. skeptic/ternary_orders.json supplies all witnesses. A separate implementation, skeptic/replay_orders.py, replays every witness, verifies each permutation, checks all 1,276 prefixes, and confirms equality with every original saved sum and a total of 556 binary additions. A mandated literal left-to-right interpretation would fail the expanded-prefix condition; that is not the sum-of-terms representation specified in this package.
4. Exactness: write the expanded factors as U[t,a], V[t,b], and W[o,t]. Expanding the 144 products gives tensor coefficient T[o,a,b] = sum_t W[o,t]*U[t,a]*V[t,b]. For every output o=k*5+i, every A index a=ai*5+aj, and every B index b=bj*8+bk, I check T equals 1 exactly when ai=i, bk=k, and aj=bj, and equals 0 otherwise. This checks all 40*25*40 = 40,000 coefficients, including every cancellation: exactly 200 coefficients are 1 and 39,800 are 0. Independence of the formal monomials A[a]*B[b] proves equality with A*B as an integer polynomial, for all inputs. The 64 fixed-seed direct SLP executions are supplementary checks, not the basis of the exactness verdict. C^T in the author output denotes the specified transposed storage order, not a different mathematical product.
5. Count: a nonempty q-term sum uses exactly q-1 binary additions/subtractions; signs are free. Applying this to every saved fresh and final form gives U=133+0, V=161+0, W=181+81, hence 133+161+262=556. These agree with object metadata and INDEX.csv. The certificate also realizes the count using ternary binary intermediates. The 144 bilinear products are excluded from this addition count. Expanded nonzeros are U=660, V=809, W=783, so the declared naive count is independently recovered as 660+809+783-2*144-40=1924. This establishes a 144-product algorithm, without asserting a lower bound or the externally listed best rank.
6. Hashes and determinism: object bytes are unchanged during the independent check. A new process produces byte-identical complete checker output and certificate, including fixed expanded-map and tensor hashes. The two author Python checkers likewise produce identical output on repeated fresh-process runs with the permitted interpreter. All eight original package files remain byte-identical across the author checks; skeptic/package_hashes.json records their SHA-256 values. External-data hashes cannot be authenticated from missing data.

Exact independent command, run from this folder (exit status 0):

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

Full real combined output, inserted directly from skeptic/output.txt:

```text
Independent checker: exact integer expansion; no author code imported
Object: object/5x5x8_m144_cr556_ZT_reduced.json
Object SHA-256: cd6b1a181d857f3e993cc6c15338a7f709bd1119c2745a399cfc02eae9b52f03
Checker SHA-256: ba6d42710729339aac22ecc554e29e85d1d7da1a9b86d8cda3837bceee48fa83
Format: 5x5x8; max dimension: 8; products: 144; z2: false
Schema, INDEX.csv object path, target, cell, and SHA-256: PASS
U: inputs=25; fresh=133; final=144; additions fresh=133, final=0, total=133
V: inputs=40; fresh=161; final=144; additions fresh=161, final=0, total=161
W: inputs=144; fresh=98; final=40; additions fresh=181, final=81, total=262
All references precede use; all literal coefficients are +/-1: PASS
Expanded ternary condition: all 720 complete forms PASS
Ternary binary association: all 720 forms have certified term orders; 1276 prefixes PASS
Listed-order diagnostic: 1 nonternary prefixes; term-list sums require the certified associations for ternary binary evaluation
Term-order certificate: skeptic/ternary_orders.json; SHA-256: 11d82a2057f6c751719a8b6ee127d8b625c557fea91d244c9fd773640fedc543
All forms nonzero; all 144 products have nonzero factors and are used: PASS
Reduced additions: 133 + 161 + 262 = 556; object and INDEX.csv agree
Expanded nonzeros U,V,W: [660, 809, 783]; naive additions: 1924; object agrees
Recorded reference arithmetic: 556 < 620 (improvement 64); reference not recounted
Full tensor identity over Z: 40000 / 40000 coefficients checked; 200 unit coefficients; all others zero: PASS
Expanded-map SHA-256: de8df3f65e5fd9387c7d2a0bc67271d6373a9bb3fac45c52e0f8d38ec8ad8711
Tensor SHA-256: dd4dffb599a7b8d0abb44b1fd58b24965b4c7923766dfa846bfc6e6aedad3a4a
Direct SLP execution: 64 fixed-seed integer matrix pairs (including 30-digit inputs): PASS
Object bytes unchanged during check: PASS
Independent saved-object checks: PASS
```

Exact certificate replay command (exit status 0):

```sh
python3 skeptic/replay_orders.py > skeptic/order-replay.txt 2>&1
```

Full real output from skeptic/order-replay.txt:

```text
Listed-order w.final[6] after term positions [0, 1, 2]: [(32, -2), (133, -2)]
Certified w.final[6] term positions (zero-based): [0, 1, 3, 2]
Certificate replay: 720 forms, 1276 ternary prefixes, 556 binary additions: PASS
Each term appears once; every reordered sum equals the original saved form: PASS
```

Exact determinism command (exit status 0):

```sh
python3 skeptic/check_determinism.py > skeptic/determinism.txt 2>&1
```

The repeat's full output is also saved as skeptic/output-repeat.txt. Full real determinism output:

```text
Command: ../../../.venv/bin/python skeptic/check.py (second fresh process)
Second exit status: 0
Complete stdout/stderr matches skeptic/output.txt byte-for-byte: PASS
Term-order certificate matches byte-for-byte: PASS
Output SHA-256: 422ea90ccf44b49e5e3afcc1b13174155362300f4ba75da82a222c4912fe5d22
Determinism: PASS
```

Only after these independent checks did I read and run the author tools. Their exact tensor result, storage order, naive count, and reduced count agree. Their negative control rejects a sign-flipped object. The author's check_slp.py does not actually test expanded coefficients for membership in {-1,0,1}: its expand function builds the vectors, but check discards the fresh vectors and never checks coefficient ranges in the expanded rows. sym_check.py likewise checks literal signs only. This is a verifier coverage gap relative to the documentation, not evidence of a defect in this object; the independent checks above supply the missing test.

The first author comparison through the system python3 launcher emitted timestamped Xcode startup diagnostics on stderr, causing the combined-output equality assertion to fail. The original launch log is retained in skeptic/author-launcher-diagnostic.txt. This was launcher output, not a changing computed result. I bypassed that launcher using the explicitly permitted interpreter, then repeated both author Python checkers with byte-identical results. The shell wrapper also uses that interpreter via skeptic/bin/python3; its temporary files stay in skeptic/tmp. No saved object was changed.

Exact author-comparison command (exit status 0):

```sh
python3 skeptic/compare.py > skeptic/author-output.txt 2>&1
```

The harness records the exact child commands and environment below. Full real combined output from skeptic/author-output.txt:

```text
Environment: TMPDIR=skeptic/tmp; PATH prepends skeptic/bin; PYTHONDONTWRITEBYTECODE=1; PYTHONNOUSERSITE=1
skeptic/bin/python3 forwards to ../../../.venv/bin/python to bypass system launcher diagnostics
Command: ../../../.venv/bin/python verify-it-yourself/check_slp.py object/5x5x8_m144_cr556_ZT_reduced.json
{"file": "5x5x8_m144_cr556_ZT_reduced.json", "format": "5x5x8", "rank": 144, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 133, "adds_V": 161, "adds_W": 262, "adds_total": 556, "naive_total": 1924, "declared_reduced": 556, "VALID": true}
Exit status: 0
Second fresh process output matches byte-for-byte: PASS
Command: sh verify-it-yourself/run_checks.sh
sha256 matches INDEX.csv (cd6b1a181d857f3e993cc6c15338a7f709bd1119c2745a399cfc02eae9b52f03)
== check_slp.py on object/5x5x8_m144_cr556_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x5x8_m144_cr556_ZT_reduced.json", "format": "5x5x8", "rank": 144, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 133, "adds_V": 161, "adds_W": 262, "adds_total": 556, "naive_total": 1924, "declared_reduced": 556, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=556, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
Exit status: 0
Command: ../../../.venv/bin/python verify-it-yourself/sym_check.py object/5x5x8_m144_cr556_ZT_reduced.json
{"file": "5x5x8_m144_cr556_ZT_reduced.json", "format": "5x5x8", "rank": 144, "products": 144, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 556}
Exit status: 0
Second fresh process output matches byte-for-byte: PASS
All 8 original package files unchanged by author checks: PASS
```

No disagreement remains on a saved-object property under the quoted representation. The term-association issue and author-verifier coverage gap are disclosed above. The offline scope excludes the absent third-party object and all live-table or novelty judgments.

pass: true
