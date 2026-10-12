#!/usr/bin/env python3
"""peel.py -- generalised one-slice restriction ("peel") of a fast matrix multiplication scheme.

Library used by sweep.py and make_scheme.py.

Conventions (Perminov-style JSON, as in ../schemes/):
  u_k row-major n x m  (u[i*m+j] <-> A_ij),  v_k m x p (v[j*p+l] <-> B_jl),  w_k p x n (w[l*n+i] <-> C_il).

RESTRICTION ALONG AN AXIS (exact statement):
  Restricting <n,m,p> to <n,m,p-1> means B = B~ Q with Q (p-1) x p of rank p-1 and C~ = C Q+ with Q Q+ = I.
  Then v~_k = v_k Q^T and w~_k = (Q+)^T w_k.  Term k vanishes iff every row of v_k is proportional to the
  vector e spanning ker Q (v_k = x e^T), or every column of w_k is proportional to the vector f spanning
  (range Q+)^perp (w_k = f y^T).  Any pair (e, f) with <e,f> != 0 is realisable; e = f = e_l is the
  coordinate peel of slice l.  The other two axes are identical with (A,C) resp. (A,B) in the roles of (B,C):
    axis n (index i): e-side factor u (fibers along i = columns of u), f-side factor w (rows of w);
    axis m (index j): e-side factor u (rows of u),                     f-side factor v (columns of v);
    axis p (index l): e-side factor v (rows of v),                     f-side factor w (columns of w).
  A term dies iff its e-side factor is rank one with fiber direction e, or its f-side factor is rank one
  with fiber direction f.  The projected scheme must be verified exactly afterwards
  (../verify-it-yourself/fmmcheck.py); nothing here is trusted.
"""
import json
from collections import defaultdict
from fractions import Fraction


# ----------------------------------------------------------------------------- field helpers
class Field:
    """Q (mod=None) or GF(mod)."""

    def __init__(self, mod=None):
        self.mod = mod

    def conv(self, x):
        if self.mod is None:
            return x if isinstance(x, Fraction) else Fraction(x)
        x = Fraction(x)
        d = x.denominator % self.mod
        if d == 0:
            raise ValueError(f"denominator divisible by {self.mod}")
        return (x.numerator % self.mod) * pow(d, -1, self.mod) % self.mod

    def zero(self):
        return Fraction(0) if self.mod is None else 0

    def one(self):
        return Fraction(1) if self.mod is None else 1

    def add(self, a, b):
        return a + b if self.mod is None else (a + b) % self.mod

    def sub(self, a, b):
        return a - b if self.mod is None else (a - b) % self.mod

    def mul(self, a, b):
        return a * b if self.mod is None else (a * b) % self.mod

    def inv(self, a):
        # exact: ints are promoted to Fraction (never float division)
        return Fraction(1) / Fraction(a) if self.mod is None else pow(int(a), -1, self.mod)

    def neg(self, a):
        return -a if self.mod is None else (-a) % self.mod

    def is_zero(self, a):
        return a == 0


def mat_of(row, rows, cols):
    return [row[i * cols:(i + 1) * cols] for i in range(rows)]


def fiber_direction(M, F, fibers_are_columns):
    """If M (list of rows) is rank one, return the normalised direction of its fibers
    (columns if fibers_are_columns else rows), as a tuple; else None.  Zero matrix -> None."""
    rows = len(M)
    cols = len(M[0]) if rows else 0
    fibers = [[M[i][j] for i in range(rows)] for j in range(cols)] if fibers_are_columns else [list(r) for r in M]
    ref = None
    for fb in fibers:
        if any(not F.is_zero(x) for x in fb):
            if ref is None:
                a = next(i for i, x in enumerate(fb) if not F.is_zero(x))
                inv = F.inv(fb[a])
                ref = tuple(F.mul(x, inv) for x in fb)
                ref_a = a
            else:
                if F.is_zero(fb[ref_a]):
                    return None
                inv = F.inv(fb[ref_a])
                if any(F.mul(x, inv) != y for x, y in zip(fb, ref)):
                    return None
    return ref


def dot(a, b, F):
    s = F.zero()
    for x, y in zip(a, b):
        s = F.add(s, F.mul(x, y))
    return s


def perp_basis(e, F):
    """rows: a basis of e^perp (d-1 vectors), for e normalised with e[a] = 1 at its first nonzero a."""
    d = len(e)
    a = next(i for i, x in enumerate(e) if not F.is_zero(x))
    assert e[a] == F.one()
    rows = []
    for t in range(d):
        if t == a:
            continue
        b = [F.zero()] * d
        b[t] = F.one()
        b[a] = F.neg(e[t])
        rows.append(b)
    return rows


def mat_mul(A, B, F):
    n, k, m = len(A), len(B), len(B[0])
    out = [[F.zero()] * m for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        for t in range(k):
            a = Ai[t]
            if F.is_zero(a):
                continue
            Bt = B[t]
            oi = out[i]
            for j in range(m):
                oi[j] = F.add(oi[j], F.mul(a, Bt[j]))
    return out


def mat_inv(M, F):
    n = len(M)
    A = [list(r) + [F.one() if i == j else F.zero() for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        piv = next((r for r in range(c, n) if not F.is_zero(A[r][c])), None)
        if piv is None:
            raise ValueError("singular")
        A[c], A[piv] = A[piv], A[c]
        inv = F.inv(A[c][c])
        A[c] = [F.mul(x, inv) for x in A[c]]
        for r in range(n):
            if r != c and not F.is_zero(A[r][c]):
                f = A[r][c]
                A[r] = [F.sub(x, F.mul(f, y)) for x, y in zip(A[r], A[c])]
    return [r[n:] for r in A]


def transpose(M):
    return [list(c) for c in zip(*M)]


# ----------------------------------------------------------------------------- the peel
AXES = {
    # axis: (dimension index, e-side factor name, e fibers are columns?, f-side factor name, f fibers are columns?)
    0: ("n", "u", True, "w", False),
    1: ("m", "u", False, "v", True),
    2: ("p", "v", False, "w", True),
}


def factor_matrices(fmt, u, v, w, k):
    n, m, p = fmt
    return {"u": mat_of(u[k], n, m), "v": mat_of(v[k], m, p), "w": mat_of(w[k], p, n)}


def peel_census(fmt, u, v, w, F, axis):
    """Return dict with per-term e/f directions and the best (e,f) pair for this axis."""
    _, ename, ecols, fname, fcols = AXES[axis]
    r = len(u)
    e_dirs, f_dirs = [], []
    for k in range(r):
        mats = factor_matrices(fmt, u, v, w, k)
        e_dirs.append(fiber_direction(mats[ename], F, ecols))
        f_dirs.append(fiber_direction(mats[fname], F, fcols))
    e_groups, f_groups = defaultdict(set), defaultdict(set)
    for k, e in enumerate(e_dirs):
        if e is not None:
            e_groups[e].add(k)
    for k, f in enumerate(f_dirs):
        if f is not None:
            f_groups[f].add(k)
    d = fmt[axis]
    # coordinate peels for reference
    coord = {}
    for l in range(d):
        el = tuple(F.one() if t == l else F.zero() for t in range(d))
        coord[l] = len(e_groups.get(el, set()) | f_groups.get(el, set()))
    best = (0, None, None, set())
    f_sorted = sorted(f_groups.items(), key=lambda kv: -len(kv[1]))
    e_sorted = sorted(e_groups.items(), key=lambda kv: -len(kv[1]))
    units = [tuple(F.one() if t == j else F.zero() for t in range(d)) for j in range(d)]
    top_f = len(f_sorted[0][1]) if f_sorted else 0
    # every compatible (e, f) pair, pruned by the size bound len(ks)+len(kf) <= best
    for e, ks in e_sorted:
        if len(ks) + top_f <= best[0] and len(ks) <= best[0]:
            break
        for f, kf in f_sorted:
            if len(ks) + len(kf) <= best[0]:
                break
            if not F.is_zero(dot(e, f, F)):
                tot = ks | kf
                if len(tot) > best[0]:
                    best = (len(tot), e, f, tot)
        if len(ks) > best[0]:  # e alone: partner = any unit vector with <e,f> != 0 (always exists)
            for f in units:
                if not F.is_zero(dot(e, f, F)):
                    tot = ks | f_groups.get(f, set())
                    if len(tot) > best[0]:
                        best = (len(tot), e, f, tot)
                    break
    for f, kf in f_sorted:  # f alone
        if len(kf) <= best[0]:
            break
        for e in units:
            if not F.is_zero(dot(e, f, F)):
                tot = kf | e_groups.get(e, set())
                if len(tot) > best[0]:
                    best = (len(tot), e, f, tot)
                break
    return dict(axis=axis, coord=coord, best_z=best[0], best_e=best[1], best_f=best[2], dead=best[3],
                n_e_rank1=sum(1 for x in e_dirs if x is not None), n_f_rank1=sum(1 for x in f_dirs if x is not None),
                n_e_dirs=len(e_groups), n_f_dirs=len(f_groups))


def project(fmt, u, v, w, F, axis, e, f):
    """Build the <..d-1..> scheme for directions (e, f) (normalised, <e,f> != 0). Returns (fmt2, u2, v2, w2)."""
    n, m, p = fmt
    Q = perp_basis(e, F)                 # (d-1) x d, rows span e^perp, ker Q = span(e)
    Fm = transpose(perp_basis(f, F))     # d x (d-1), columns span f^perp
    M = mat_mul(Q, Fm, F)                # (d-1) x (d-1), invertible iff <e,f> != 0
    Qp = mat_mul(Fm, mat_inv(M, F), F)   # d x (d-1): Q Qp = I, range Qp = f^perp  (ker (Qp)^T = span(f))
    QT = transpose(Q)                    # d x (d-1)
    QpT = transpose(Qp)                  # (d-1) x d
    u2, v2, w2 = [], [], []
    for k in range(len(u)):
        U, V, W = mat_of(u[k], n, m), mat_of(v[k], m, p), mat_of(w[k], p, n)
        if axis == 0:      # A = P A~ with P = Q^T (n x (n-1)): u~ = P^T u = Q u ; w~ = w (P+)^T = w Qp
            U2, V2, W2 = mat_mul(Q, U, F), V, mat_mul(W, Qp, F)
            fmt2 = (n - 1, m, p)
        elif axis == 1:    # A = A~ Q, B = Q+ B~ : u~ = u Q^T ; v~ = (Q+)^T v
            U2, V2, W2 = mat_mul(U, QT, F), mat_mul(QpT, V, F), W
            fmt2 = (n, m - 1, p)
        else:              # B = B~ Q, C~ = C Q+ : v~ = v Q^T ; w~ = (Q+)^T w
            U2, V2, W2 = U, mat_mul(V, QT, F), mat_mul(QpT, W, F)
            fmt2 = (n, m, p - 1)
        fu = [x for row in U2 for x in row]
        fv = [x for row in V2 for x in row]
        fw = [x for row in W2 for x in row]
        if any(not F.is_zero(x) for x in fu) and any(not F.is_zero(x) for x in fv) and any(not F.is_zero(x) for x in fw):
            u2.append(fu); v2.append(fv); w2.append(fw)
    return fmt2, u2, v2, w2


# ----------------------------------------------------------------------------- IO helpers
def load_lita_npz(path):
    """LITA *.npz (github.com/khoruzhii/lita, schemes/): CSR arrays {u,v,w}_{indptr,indices,numerators,denominators}
    and metadata_json with tensor=[n1,n2,n3] and rank, as described in LITA's README.  U indexes A (n1*n2) and
    V indexes B (n2*n3) row-major; W indexes C row-major (i*n3+l) and is converted here to the C^T convention
    (l*n1+i) used by the JSON files.  Loaded with allow_pickle=False."""
    import numpy as np
    z = np.load(path, allow_pickle=False)
    meta = json.loads(z["metadata_json"].item())
    n1, n2, n3 = [int(x) for x in meta["tensor"]]
    r = int(meta["rank"])

    def axis(name, cols):
        indptr = z[f"{name}_indptr"]
        idx = z[f"{name}_indices"]
        num = z[f"{name}_numerators"]
        den = z[f"{name}_denominators"]
        rows = []
        for q in range(len(indptr) - 1):
            row = [Fraction(0)] * cols
            for t in range(int(indptr[q]), int(indptr[q + 1])):
                row[int(idx[t])] += Fraction(int(num[t]), int(den[t]))
            rows.append(row)
        return rows

    u = axis("u", n1 * n2)
    v = axis("v", n2 * n3)
    w_c = axis("w", n1 * n3)
    if not (len(u) == len(v) == len(w_c) == r):
        raise ValueError(f"npz rank mismatch: {len(u)},{len(v)},{len(w_c)} vs {r}")
    w = []
    for row in w_c:  # C row-major (i*n3+l) -> C^T (l*n1+i)
        wt = [Fraction(0)] * (n3 * n1)
        for i in range(n1):
            for l in range(n3):
                wt[l * n1 + i] = row[i * n3 + l]
        w.append(wt)
    return (n1, n2, n3), u, v, w, {"declared_rank": r, "z2": False, "lita_metadata": meta}


def load_json(path):
    """Perminov-style JSON scheme; coefficients ints or "p/q" strings."""
    d = json.load(open(path))
    n = tuple(int(x) for x in d["n"])

    def conv(x):
        if isinstance(x, bool):
            raise ValueError("bool")
        if isinstance(x, int):
            return x
        if isinstance(x, float):
            f = Fraction(x).limit_denominator(10**6)
            if abs(float(f) - x) > 1e-12:
                raise ValueError("float")
            return int(f) if f.denominator == 1 else f
        f = Fraction(str(x).strip())
        return int(f) if f.denominator == 1 else f
    u = [[conv(x) for x in row] for row in d["u"]]
    v = [[conv(x) for x in row] for row in d["v"]]
    w = [[conv(x) for x in row] for row in d["w"]]
    if not (len(u) == len(v) == len(w)):
        raise ValueError("ragged")
    for mat, width in ((u, n[0] * n[1]), (v, n[1] * n[2]), (w, n[2] * n[0])):
        if any(len(r) != width for r in mat):
            raise ValueError("width")
    return n, u, v, w, {"z2": bool(d.get("z2", False)), "declared_rank": d.get("m")}


def load_scheme(path):
    if path.endswith(".npz"):
        return load_lita_npz(path)
    if path.endswith(".json"):
        return load_json(path)
    raise ValueError(f"unsupported scheme file {path} (expected .npz or .json)")


def to_json(fmt, u, v, w, F, note=""):
    def s(x):
        if F.mod is not None:
            return int(x)
        x = Fraction(x)
        return int(x) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return {"n": list(fmt), "m": len(u), "z2": (F.mod == 2), "ring": ("GF(%d)" % F.mod if F.mod else "Q"),
            "note": note, "u": [[s(x) for x in row] for row in u], "v": [[s(x) for x in row] for row in v],
            "w": [[s(x) for x in row] for row in w]}


def note_for(source_basename, axis_name, e, f):
    """The `note` string written into each scheme (same text as in ../schemes/)."""
    return (f"peel of {source_basename} axis {axis_name} e={' '.join(str(x) for x in e)} "
            f"f={' '.join(str(x) for x in f)}")
