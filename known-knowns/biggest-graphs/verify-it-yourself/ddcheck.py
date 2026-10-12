#!/usr/bin/env python3
"""ddcheck.py EDGEFILE DELTA D  --  exhaustive all-pairs check with python3 + numpy only.

Checks that the edge list is a simple graph (no loops, no repeated edges, every label 0..N-1 used) with maximum
degree <= DELTA and diameter <= D, by growing bitset balls from every vertex (batches of up to 64*W sources).

Suitable for graphs up to a few tens of thousands of vertices (memory ~ 2*edges*W*8 bytes per round).  For the two
large graphs in this package (535,495 and 1,424,896 vertices) use the C checker ddcheck.c instead.

Output: one JSON object; the field "valid" is the verdict.  Exit code 0 iff valid.
Control: run with D-1; a graph of diameter exactly D must then give far_pairs > 0 and valid=false.
"""
import json
import sys

import numpy as np


def popcount64(a):
    if hasattr(np, "bitwise_count"):
        return np.bitwise_count(a).astype(np.int64)
    tbl = np.array([bin(i).count("1") for i in range(256)], dtype=np.int64)
    return tbl[a.view(np.uint8).reshape(a.shape + (8,))].sum(axis=-1)


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    path, Delta, D = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rows = []
    bad = 0
    with open(path) as fh:
        for ln in fh:
            s = ln.strip()
            if not s or s.startswith("#"):
                continue
            parts = s.split()
            if len(parts) != 2 or not all(p.isdigit() for p in parts):
                bad += 1
                continue
            rows.append((int(parts[0]), int(parts[1])))
    E = np.array(rows, dtype=np.int64).reshape(-1, 2)
    loops = int((E[:, 0] == E[:, 1]).sum())
    E = E[E[:, 0] != E[:, 1]]
    E = np.sort(E, axis=1)
    N = int(E.max()) + 1 if len(E) else 0
    keys = E[:, 0] * N + E[:, 1]
    dup = int(len(keys) - len(np.unique(keys)))
    deg = np.bincount(E.ravel(), minlength=N)
    unused = int((deg == 0).sum())
    out = {"file": path, "N": N, "edges": int(len(E)), "loops": loops, "duplicates": dup, "unparsable_lines": bad,
           "unused_labels": unused, "mindeg": int(deg.min()) if N else None, "maxdeg": int(deg.max()) if N else None,
           "DELTA": Delta, "D": D,
           "degree_histogram": {int(d): int(c) for d, c in enumerate(np.bincount(deg)) if c and d > 0}}
    if bad or loops or dup or unused or N == 0:
        out["valid"] = False
        out["reason"] = "format/loops/duplicates/unused labels"
        print(json.dumps(out))
        sys.exit(1)

    # CSR adjacency (both directions)
    src = np.concatenate([E[:, 0], E[:, 1]])
    dst = np.concatenate([E[:, 1], E[:, 0]])
    order = np.argsort(src, kind="stable")
    adj = dst[order]
    off = np.zeros(N + 1, dtype=np.int64)
    off[1:] = np.cumsum(deg)
    starts = off[:-1]  # every vertex has degree >= 1 here, so reduceat is well defined

    W = max(1, min(64, (N + 63) // 64))
    per_batch = 64 * W
    within = [0] * (D + 1)
    for s0 in range(0, N, per_batch):
        ns = min(per_batch, N - s0)
        A = np.zeros((N, W), dtype=np.uint64)
        idx = np.arange(ns)
        A[s0 + idx, idx // 64] |= (np.uint64(1) << (idx % 64).astype(np.uint64))
        mask = np.zeros(W, dtype=np.uint64)
        full, rem = divmod(ns, 64)
        mask[:full] = np.uint64(0xFFFFFFFFFFFFFFFF)
        if rem:
            mask[full] = np.uint64((1 << rem) - 1)
        within[0] += int(popcount64(A & mask).sum())
        for r in range(1, D + 1):
            B = np.bitwise_or.reduceat(A[adj], starts, axis=0)
            A = A | B
            within[r] += int(popcount64(A & mask).sum())
    far = N * N - within[D]
    out["ordered_pairs_within_distance"] = {r: within[r] for r in range(D + 1)}
    out["far_pairs"] = int(far)
    out["valid"] = bool(far == 0 and out["maxdeg"] <= Delta)
    print(json.dumps(out))
    sys.exit(0 if out["valid"] else 1)


if __name__ == "__main__":
    main()
