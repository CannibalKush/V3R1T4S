"""Lens generators. Each lens_<name>(file, rng, deadline, state, save) yields (scheme_json, claimed_total).
The worker re-verifies every yielded scheme with fmm_check before trusting it; nothing here is a verifier.

L1 cse        iterated randomized pair-greedy CSE (ruin-and-recreate on the pair order), each map separately.
L2 transpose  Tellegen transposition: run CSE on M^T, transpose the straight-line program back to an SLP for M.
              A different search landscape for the same map; the transposed program has cost L(M^T) - cols + rows.
L3 flipwalk   flip-graph random walk at fixed rank with ternary coefficients, scoring each visited scheme by
              fast greedy CSE; the best visited scheme is rebuilt with iterated CSE.
"""
import time
import numpy as np
import maps, cse


# ---------------------------------------------------------------- shared helpers
def _iterate(M, rng, until, best):
    while time.time() < until:
        if best is None or rng.random() < 0.05:
            r = cse.reduce_map(M, rng.randrange(1 << 30), rng.choice((0.0, 0.05, 0.15, 0.3)))
        else:
            defs = best[3]
            k = rng.randrange(0, max(1, len(defs)))
            r = cse.reduce_map(M, rng.randrange(1 << 30), rng.choice((0.0, 0.1, 0.3)), forced=defs[:k])
        if best is None or r[0] <= best[0]:
            best = r
    return best


def _orig_parts(d):
    return {k: (d.get(k + "_fresh", []), d[k]) for k in ("u", "v", "w")}


def _quick_cost(M, rng, seeds=2):
    return min(cse.reduce_map(M, rng.randrange(1 << 30), 0.1)[0] for _ in range(seeds))


# ---------------------------------------------------------------- L1
def lens_cse(path, rng, deadline, state, save, slice_s=20.0):
    import fmm_check as F
    d, U, V, W = maps.load(path)
    r0 = F.check(d)
    ref_maps = {"u": r0["adds_U"], "v": r0["adds_V"], "w": r0["adds_W"]}
    parts = _orig_parts(d)
    best = {"u": None, "v": None, "w": None}
    cost = dict(ref_maps)
    state["file_maps"] = [r0["adds_U"], r0["adds_V"], r0["adds_W"]]
    first = True
    while time.time() < deadline:
        if first and all(best.values()):
            # one self-built scheme (all three maps from our own SLPs) validates the builder end to end
            first = False
            own = {k: (best[k][1], best[k][2]) for k in best}
            yield maps.scheme_json(d, own), sum(best[k][0] for k in best)
        for k, M in (("u", U), ("v", V), ("w", W)):
            until = min(deadline, time.time() + slice_s)
            best[k] = _iterate(M, rng, until, best[k])
            state.setdefault("map_best", {})[k] = best[k][0]
            save()
            if best[k][0] < cost[k]:
                cost[k] = best[k][0]
                parts[k] = (best[k][1], best[k][2])
                yield maps.scheme_json(d, parts), sum(cost.values())
            if time.time() >= deadline:
                break


# ---------------------------------------------------------------- L2: transposition principle
def transpose_slp(n_in, fresh, final):
    """Given an SLP (Perminov forms) computing n_out = len(final) linear forms over n_in inputs, return
    (fresh2, final2): an SLP over n_out inputs computing the TRANSPOSED map (n_in outputs). Tellegen: reverse
    every edge of the linear circuit. Unused fresh nodes are dropped. Inputs with no use give an empty output
    form, which the caller must avoid (remove zero columns first)."""
    k = len(fresh)
    n_out = len(final)
    # circuit nodes: inputs 0..n_in-1, fresh n_in..n_in+k-1, outputs n_in+k..n_in+k+n_out-1
    out_edges = {}  # node -> list of (target node, coeff)
    for i, f in enumerate(fresh):
        t = n_in + i
        for term in f:
            out_edges.setdefault(term["index"], []).append((t, term["value"]))
    for j, f in enumerate(final):
        t = n_in + k + j
        for term in f:
            out_edges.setdefault(term["index"], []).append((t, term["value"]))
    # drop fresh nodes with no out-edges (iteratively)
    alive = [True] * k
    changed = True
    while changed:
        changed = False
        for i in range(k):
            t = n_in + i
            if alive[i] and not any(alive[tt - n_in] if n_in <= tt < n_in + k else True for tt, _ in out_edges.get(t, [])):
                alive[i] = False
                changed = True
    # new ids: old outputs -> 0..n_out-1 ; old fresh (alive, reverse order) -> n_out.. ; old inputs -> outputs
    new_id = {}
    for j in range(n_out):
        new_id[n_in + k + j] = j
    nid = n_out
    order = [i for i in range(k - 1, -1, -1) if alive[i]]
    for i in order:
        new_id[n_in + i] = nid
        nid += 1
    fresh2 = []
    for i in order:
        t = n_in + i
        form = [{"index": new_id[tt], "value": c} for tt, c in out_edges.get(t, [])
                if (tt >= n_in + k) or alive[tt - n_in]]
        fresh2.append(form)
    final2 = []
    for i in range(n_in):
        form = [{"index": new_id[tt], "value": c} for tt, c in out_edges.get(i, [])
                if (tt >= n_in + k) or alive[tt - n_in]]
        final2.append(form)
    return fresh2, final2


def reduce_by_transposition(M, seed, eps, forced=None, reducer=None):
    """SLP for M obtained by CSE on M^T plus Tellegen transposition. Returns (cost, fresh, final, defs)
    in the same shape as cse.reduce_map (defs refer to the M^T search and can be fed back as forced)."""
    M = np.asarray(M, np.int8)
    nz_cols = np.nonzero(np.any(M, axis=0))[0]
    Mt = M[:, nz_cols].T.copy()  # rows = used inputs of M, over the rows of M as base variables
    if reducer is None:
        c, fr, fi, defs = cse.reduce_map(Mt, seed, eps, forced=forced)
    else:
        c, fr, fi, defs = reducer(Mt, seed, eps)
    fresh2, final2 = transpose_slp(Mt.shape[1], fr, fi)  # inputs of transposed program = rows of M
    # final2 has one form per row of Mt, i.e. per used input of M: but we need forms per ROW of M.
    # Tellegen gives the map (M^T)^T = M: its inputs are Mt's outputs... careful with roles:
    #   Mt (rows=used inputs of M, cols=rows of M): SLP computes Mt * y for y indexed by rows of M.
    #   transposed SLP computes Mt^T * x = M[:, nz_cols] * x for x indexed by used inputs of M.  <- what we want
    # So transposed program: inputs = Mt outputs (len(final) = #used inputs), outputs = Mt inputs (= rows of M).
    # Remap input indices to the original column positions of M.
    n_used = len(nz_cols)
    k2 = len(fresh2)
    n_in = M.shape[1]
    remap = {}
    for j in range(n_used):
        remap[j] = int(nz_cols[j])
    for i in range(k2):
        remap[n_used + i] = n_in + i

    def rm(form):
        return [{"index": remap[t["index"]], "value": int(t["value"])} for t in form]

    fresh3 = [rm(f) for f in fresh2]
    final3 = [rm(f) for f in final2]
    cost = sum(len(f) - 1 for f in fresh3) + sum(len(f) - 1 for f in final3)
    if any(len(f) == 0 for f in fresh3 + final3):
        cost = 10 ** 9  # invalid; caller discards
    return cost, fresh3, final3, defs


def _iterate_t(M, rng, until, best):
    while time.time() < until:
        if best is None or rng.random() < 0.05:
            r = reduce_by_transposition(M, rng.randrange(1 << 30), rng.choice((0.0, 0.05, 0.15, 0.3)))
        else:
            defs = best[3]
            k = rng.randrange(0, max(1, len(defs)))
            r = reduce_by_transposition(M, rng.randrange(1 << 30), rng.choice((0.0, 0.1, 0.3)), forced=defs[:k])
        if r[0] < 10 ** 9 and (best is None or r[0] <= best[0]):
            best = r
    return best


def lens_transpose(path, rng, deadline, state, save, slice_s=20.0):
    import fmm_check as F
    d, U, V, W = maps.load(path)
    r0 = F.check(d)
    ref_maps = {"u": r0["adds_U"], "v": r0["adds_V"], "w": r0["adds_W"]}
    parts = _orig_parts(d)
    best = {"u": None, "v": None, "w": None}
    cost = dict(ref_maps)
    state["file_maps"] = [r0["adds_U"], r0["adds_V"], r0["adds_W"]]
    first = True
    while time.time() < deadline:
        if first and all(best.values()):
            first = False
            own = {k: (best[k][1], best[k][2]) for k in best}
            yield maps.scheme_json(d, own), sum(best[k][0] for k in best)
        for k, M in (("u", U), ("v", V), ("w", W)):
            until = min(deadline, time.time() + slice_s)
            best[k] = _iterate_t(M, rng, until, best[k])
            if best[k] is None:
                continue
            state.setdefault("map_best", {})[k] = best[k][0]
            save()
            if best[k][0] < cost[k]:
                cost[k] = best[k][0]
                parts[k] = (best[k][1], best[k][2])
                yield maps.scheme_json(d, parts), sum(cost.values())
            if time.time() >= deadline:
                break


# ---------------------------------------------------------------- L3: flip-graph walk
def _flips(U, V, Wt):
    """All valid ternary flips of the scheme given as product triples (U[q], V[q], Wt[q]). A flip uses two
    products i != j with X_i == s*X_j for one factor X in {U,V,Wt}: then Y_i += s*Y_j and Z_j -= Z_i for the
    other two factors (Y,Z) in either order. Returns a list of (factor, i, j, s, which_order)."""
    out = []
    r = U.shape[0]
    for name, X in (("u", U), ("v", V), ("w", Wt)):
        key = {}
        for q in range(r):
            row = X[q]
            nz = np.nonzero(row)[0]
            if len(nz) == 0:
                continue
            s = 1 if row[nz[0]] > 0 else -1
            key.setdefault(tuple((row * s).tolist()), []).append((q, s))
        for lst in key.values():
            if len(lst) < 2:
                continue
            for a in range(len(lst)):
                for b in range(len(lst)):
                    if a == b:
                        continue
                    i, si = lst[a]
                    j, sj = lst[b]
                    out.append((name, i, j, si * sj, 0))
                    out.append((name, i, j, si * sj, 1))
    return out


def _apply_flip(U, V, Wt, flip):
    name, i, j, s, order = flip
    others = {"u": (V, Wt), "v": (U, Wt), "w": (U, V)}[name]
    Y, Z = others if order == 0 else (others[1], others[0])
    yi = Y[i] + s * Y[j]
    zj = Z[j] - Z[i]
    if np.abs(yi).max() > 1 or np.abs(zj).max() > 1:
        return None
    if not yi.any() or not zj.any():
        return "rankdrop"
    Y2, Z2 = Y.copy(), Z.copy()
    Y2[i] = yi
    Z2[j] = zj
    res = {"u": U, "v": V, "w": Wt}
    if name == "u":
        res["v"], res["w"] = (Y2, Z2) if order == 0 else (Z2, Y2)
    elif name == "v":
        res["u"], res["w"] = (Y2, Z2) if order == 0 else (Z2, Y2)
    else:
        res["u"], res["v"] = (Y2, Z2) if order == 0 else (Z2, Y2)
    return res["u"], res["v"], res["w"]


def lens_flipwalk(path, rng, deadline, state, save, rebuild_s=15.0, walk_s=45.0, transposed=False):
    import fmm_check as F
    d, U, V, W = maps.load(path)
    r0 = F.check(d)
    state["file_maps"] = [r0["adds_U"], r0["adds_V"], r0["adds_W"]]
    Wt = W.T.copy()
    cur = (U.copy(), V.copy(), Wt.copy())
    if not _flips(*cur):
        # no two products share a factor up to sign: the flip graph has no move from this scheme
        state["walk_no_moves"] = True
        save()
        return
    cur_cost = _quick_cost(U, rng) + _quick_cost(V, rng) + _quick_cost(W, rng)
    best_cost, best_scheme = cur_cost, cur
    state.update({"walk_steps": 0, "walk_best_quick": cur_cost, "rankdrops": 0, "walk_restarts": 0})
    yielded_best = None
    while time.time() < deadline:
        until = min(deadline, time.time() + walk_s)
        while time.time() < until:
            fl = _flips(*cur)
            if not fl:
                cur = best_scheme
                state["walk_restarts"] += 1
                break
            res = _apply_flip(*cur, rng.choice(fl))
            if res is None:
                continue
            if res == "rankdrop":
                state["rankdrops"] += 1
                continue
            state["walk_steps"] += 1
            U2, V2, Wt2 = res
            c = _quick_cost(U2, rng, 1) + _quick_cost(V2, rng, 1) + _quick_cost(Wt2.T.copy(), rng, 1)
            # accept sideways and slightly uphill moves; restart from best occasionally
            if c <= cur_cost + rng.choice((0, 0, 1, 2)):
                cur, cur_cost = res, c
            if c < best_cost:
                best_cost, best_scheme = c, res
                state["walk_best_quick"] = c
            if rng.random() < 0.002:
                cur, cur_cost = best_scheme, best_cost
                state["walk_restarts"] += 1
        save()
        if best_scheme is not yielded_best:
            # rebuild the best visited scheme with iterated CSE on each map and hand it to the verifier
            U2, V2, Wt2 = best_scheme
            W2 = Wt2.T.copy()
            parts = {}
            tot = 0
            for k, M in (("u", U2), ("v", V2), ("w", W2)):
                b = _iterate(M, rng, min(deadline, time.time() + rebuild_s / 3), None)
                if transposed:
                    bt = _iterate_t(M, rng, min(deadline, time.time() + rebuild_s / 3), None)
                    if bt is not None and bt[0] < b[0]:
                        b = bt
                parts[k] = (b[1], b[2])
                tot += b[0]
            yielded_best = best_scheme
            state["walk_best_rebuilt"] = tot
            yield maps.scheme_json(d, parts), tot


# ---------------------------------------------------------------- L5: flip walk + transposed rebuild (run 2026-10-15-0934)
def lens_fliptrans(path, rng, deadline, state, save):
    """Flip-graph walk as in lens_flipwalk; each best visited scheme is rebuilt with BOTH direct and transposed
    iterated CSE per map, keeping the shorter program."""
    return lens_flipwalk(path, rng, deadline, state, save, rebuild_s=30.0, transposed=True)


# ---------------------------------------------------------------- L6: Boyar-Peralta with ternary cancellation (run 2026-10-15)
# Method: Boyar-Peralta shortest-linear-program heuristic; the ternary-cancellation variant on U, V and W^T (W via the
# transposition principle) as described by calgulbenkian's team in elder-plinius/V3R1T4S PR #161. Own numba code (tools/bp.py).
def lens_bp(path, rng, deadline, state, save, slice_s=30.0):
    import fmm_check as F, bp
    d, U, V, W = maps.load(path)
    r0 = F.check(d)
    cost = {"u": r0["adds_U"], "v": r0["adds_V"], "w": r0["adds_W"]}
    parts = _orig_parts(d)
    state["file_maps"] = [r0["adds_U"], r0["adds_V"], r0["adds_W"]]
    best = {"u": None, "v": None, "w": None}
    red = lambda M, s, e: bp.reduce_map_bp(M, s, e, deep=False)
    while time.time() < deadline:
        for k, M in (("u", U), ("v", V), ("w", W)):
            until = min(deadline, time.time() + slice_s)
            while time.time() < until:
                sd, e = rng.randrange(1 << 30), rng.choice((0.0, 0.3, 0.6))
                if k == "w":
                    r = reduce_by_transposition(M, sd, e, reducer=red)
                else:
                    r = bp.reduce_map_bp(M, sd, e, deep=False)
                if r[0] < 10 ** 9 and (best[k] is None or r[0] < best[k][0]):
                    best[k] = r
            if best[k] is not None:
                state.setdefault("map_best", {})[k] = best[k][0]
                save()
                if best[k][0] < cost[k]:
                    cost[k] = best[k][0]
                    parts[k] = (best[k][1], best[k][2])
                    yield maps.scheme_json(d, parts), sum(cost.values())
            if time.time() >= deadline:
                break
