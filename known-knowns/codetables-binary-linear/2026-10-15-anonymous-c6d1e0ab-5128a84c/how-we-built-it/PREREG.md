# Pre-registration

target_id: codetables-binary-linear
frozen_utc: 2026-10-14T17:58:00Z
null_test: not needed because the claim is an explicit code checked by a deterministic exact checker against a table value

**Timing note.** The success rule below was copied verbatim from the bank into the search team's brief at 2026-10-14T17:58Z, before the search started; the code was found less than an hour later. The rule was not chosen by us.

## Success rule (bank criterion, verbatim)

Success means a k x n generator matrix over GF(q) with these properties. (1) Rank is exactly k over GF(q), computed independently. (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible (2^k <= ~2^32), or, for large k (or large k with small n-k, via the dual and MacWilliams identities), by two independent exact minimum-distance implementations that agree; never by sampling. (3) d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/ cell for (q,n,k) at verification time, and at most the upper bound. (4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and no newer arXiv claim already reaches that d.

## Statistic and threshold

- Statistic: the exact minimum distance d, by full enumeration of all 2^k - 1 nonzero codewords with two independent methods, after an exact rank check.
- Threshold: d strictly above the live codetables.de lower bound for (q, n, k), and at most its upper bound.
