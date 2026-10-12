"""rcl: route-chart lifts with Cayley controllers (generalising Mizuno, arXiv 2606.15860 App. A.4).

Graph G on V = H x F_q^s (H a finite group given by right-multiplication permutations of its generators).
Alphabet: generators t of H; each t is either paired with an inverse generator t' (t' = t^-1 in H, t' != t) or an
involution (t = t^-1). Each label carries (A_t in GL_s(F_q), b_t in F_q^s, Lambda_t subset of F_q).
Edges: (h, x) ~ (h t, A_t x + lam b_t) for lam in Lambda_t.
Consistency (edge set independent of orientation):
  paired:     A_{t'} = A_t^{-1},  b_{t'} = A_t^{-1} b_t,  Lambda_{t'} = -Lambda_t
  involution: A_t^2 = I, A_t b_t = b_t, Lambda_t = -Lambda_t
Degree = sum_t |Lambda_t| (distinct generators -> distinct controller targets; b_t != 0 -> distinct lam distinct).
H acts on G by left multiplication on the first coordinate, so eccentricities need only the sources (e, x).
q prime only (F_2, F_3, F_5, F_7).  Vectors are encoded base q: x = sum x_i q^i.
"""
import numpy as np
import numba as nb


# ----------------------------------------------------------------------------------------------- linear algebra mod q
def mat_inv_mod(A, q):
    s = A.shape[0]
    M = np.concatenate([A % q, np.eye(s, dtype=np.int64)], axis=1)
    r = 0
    for c in range(s):
        piv = None
        for i in range(r, s):
            if M[i, c] % q:
                piv = i; break
        if piv is None:
            return None
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), q - 2, q)
        M[r] = (M[r] * inv) % q
        for i in range(s):
            if i != r and M[i, c] % q:
                M[i] = (M[i] - M[i, c] * M[r]) % q
        r += 1
    return M[:, s:] % q


def rank_mod(M, q):
    M = M.copy() % q
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i, c] % q:
                piv = i; break
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), q - 2, q)
        M[r] = (M[r] * inv) % q
        for i in range(rows):
            if i != r and M[i, c] % q:
                M[i] = (M[i] - M[i, c] * M[r]) % q
        r += 1
        if r == rows:
            break
    return r


def encode(v, q):
    return int(sum(int(v[i]) * q ** i for i in range(len(v))))


def all_vectors(q, s):
    Q = q ** s
    X = np.zeros((Q, s), dtype=np.int64)
    for x in range(Q):
        y = x
        for i in range(s):
            X[x, i] = y % q; y //= q
    return X


def affine_tables(A, b, q, s, lams):
    """For label (A,b,Lambda): table T[x, j] = encode(A x + lams[j] b)."""
    X = all_vectors(q, s)
    Y = (X @ A.T) % q
    pw = q ** np.arange(s)
    T = np.empty((len(X), len(lams)), dtype=np.int64)
    for j, lam in enumerate(lams):
        T[:, j] = (((Y + lam * b[None, :]) % q) @ pw)
    return T


# ----------------------------------------------------------------------------------------------- groups
def metacyclic(m, k, r):
    """Z_m x|_r Z_k, elements (i,j) -> i*k + j, (i,j)(i',j') = (i + r^j i', j + j').  Requires r^k = 1 mod m."""
    assert pow(r, k, m) == 1 % m
    rp = np.array([pow(r, j, m) for j in range(k)], dtype=np.int64)
    n = m * k

    def rmul(g):
        gi, gj = g
        I = np.arange(n) // k; J = np.arange(n) % k
        return ((I + rp[J] * gi) % m) * k + (J + gj) % k

    def inv(g):
        gi, gj = g
        jj = (-gj) % k
        return ((-rp[jj] * gi) % m, jj)

    def mul(g, h):
        return ((g[0] + rp[g[1]] * h[0]) % m, (g[1] + h[1]) % k)

    return dict(n=n, rmul=rmul, inv=inv, mul=mul, ident=(0, 0), name=f'Z{m}x|_{r}Z{k}', params=(m, k, r))


# ----------------------------------------------------------------------------------------------- graph build
def build_nbr(H, gens, charts, q, s):
    """gens: list of group elements (one per label); charts: list of (A, b, lams).
    Returns nbr (N x Delta) with vertex index h*Q + x."""
    Q = q ** s
    n = H['n']
    cols = []
    for g, (A, b, lams) in zip(gens, charts):
        R = H['rmul'](g)                      # h -> h g
        T = affine_tables(A, b, q, s, lams)   # x -> A x + lam b
        for j in range(T.shape[1]):
            # neighbour of (h,x): R[h]*Q + T[x,j]
            col = (R[:, None] * Q + T[None, :, j]).reshape(-1)
            cols.append(col)
    nbr = np.stack(cols, axis=1).astype(np.int64)
    return nbr


@nb.njit(parallel=True, cache=True)
def k2_defect(nbr, sources, cap):
    """BFS in K2 x G from (src, side 0) for all sources simultaneously (bitsets).
    Returns (number of (source, vertex-of-K2xG) pairs not reached within cap steps, per-source unreached counts).
    K2xG vertex (v,a) indexed v + a*N; neighbours (w, 1-a) for w in N_G(v)."""
    N = nbr.shape[0]; dg = nbr.shape[1]
    k = sources.shape[0]
    words = (k + 63) // 64
    reach = np.zeros((2 * N, words), dtype=np.uint64)
    for i in range(k):
        reach[sources[i], i // 64] |= np.uint64(1) << np.uint64(i % 64)
    new = reach.copy()
    for step in range(cap):
        for v2 in nb.prange(2 * N):
            v = v2 % N; a = v2 // N
            other = (1 - a) * N
            for w in range(words):
                acc = reach[v2, w]
                for j in range(dg):
                    acc |= reach[nbr[v, j] + other, w]
                new[v2, w] = acc
        for v2 in nb.prange(2 * N):
            for w in range(words):
                reach[v2, w] = new[v2, w]
    miss = np.zeros(k, dtype=np.int64)
    for v2 in range(2 * N):
        for i in range(k):
            if not ((reach[v2, i // 64] >> np.uint64(i % 64)) & np.uint64(1)):
                miss[i] += 1
    return miss.sum(), miss


@nb.njit(parallel=True, cache=True)
def g_defect(nbr, sources, cap):
    """Plain BFS in G from the sources; returns number of (source, vertex) pairs at distance > cap."""
    N = nbr.shape[0]; dg = nbr.shape[1]
    k = sources.shape[0]
    words = (k + 63) // 64
    reach = np.zeros((N, words), dtype=np.uint64)
    for i in range(k):
        reach[sources[i], i // 64] |= np.uint64(1) << np.uint64(i % 64)
    new = reach.copy()
    for step in range(cap):
        for v in nb.prange(N):
            for w in range(words):
                acc = reach[v, w]
                for j in range(dg):
                    acc |= reach[nbr[v, j], w]
                new[v, w] = acc
        for v in nb.prange(N):
            for w in range(words):
                reach[v, w] = new[v, w]
    miss = np.zeros(k, dtype=np.int64)
    for v in range(N):
        for i in range(k):
            if not ((reach[v, i // 64] >> np.uint64(i % 64)) & np.uint64(1)):
                miss[i] += 1
    return miss.sum(), miss


def check_simple(nbr):
    N, dg = nbr.shape
    loops = int((nbr == np.arange(N)[:, None]).sum())
    srt = np.sort(nbr, axis=1)
    multi = int((srt[:, 1:] == srt[:, :-1]).sum())
    # symmetry: each (v, w) must have (w, v)
    a = np.repeat(np.arange(N), dg); b = nbr.reshape(-1)
    f = np.unique(a * N + b); r = np.unique(b * N + a)
    sym = len(f) == len(r) and np.array_equal(f, r)
    return loops, multi, bool(sym)


def edges_from_nbr(nbr):
    N, dg = nbr.shape
    a = np.repeat(np.arange(N), dg); b = nbr.reshape(-1)
    m = a < b
    E = np.stack([a[m], b[m]], 1)
    return E[np.lexsort((E[:, 1], E[:, 0]))]


# ----------------------------------------------------------------------------------------------- random charts
def random_gl(q, s, rng):
    while True:
        A = rng.integers(0, q, size=(s, s))
        if mat_inv_mod(A, q) is not None:
            return A


def random_involution(q, s, rng):
    """Random A with A^2 = I (q odd): P diag(+-1) P^-1 with at least one +1 eigenvalue."""
    while True:
        P = random_gl(q, s, rng)
        d = rng.integers(0, 2, size=s)
        if d.sum() == s:
            d[rng.integers(s)] = 0
        Dm = np.diag(np.where(d == 1, q - 1, 1))
        Pi = mat_inv_mod(P, q)
        A = (P @ Dm @ Pi) % q
        # +1 eigenvector: column of P where d==0
        idx = np.where(d == 0)[0]
        coeffs = rng.integers(0, q, size=len(idx))
        if not coeffs.any():
            coeffs[0] = 1
        bvec = (P[:, idx] @ coeffs) % q
        if bvec.any():
            return A, bvec
