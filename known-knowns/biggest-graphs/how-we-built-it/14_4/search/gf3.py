"""gf3.py -- small exact GF(3) linear-algebra helpers for F_3^4 (vectors coded 0..80, big-endian base 3)."""
import itertools
import numpy as np

Q = 3
S = 4
ALL = np.array(list(itertools.product(range(Q), repeat=S)), dtype=np.int64)  # ALL[c] = vector with code c
POW = Q ** np.arange(S - 1, -1, -1)                                             # [27, 9, 3, 1]


def code(v):
    return int((np.asarray(v, dtype=np.int64) % Q) @ POW)


def codes(V):
    """V: (..., S) int array -> (...) codes."""
    return (np.asarray(V, dtype=np.int64) % Q) @ POW


def vec(c):
    return ALL[c].copy()


def rank(rows):
    M = np.array(rows, dtype=np.int64).reshape(-1, S) % Q
    r = 0
    nr = M.shape[0]
    for col in range(S):
        piv = None
        for i in range(r, nr):
            if M[i, col] % Q:
                piv = i
                break
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * (1 if M[r, col] == 1 else 2)) % Q
        for i in range(nr):
            if i != r and M[i, col]:
                M[i] = (M[i] - M[i, col] * M[r]) % Q
        r += 1
        if r == nr:
            break
    return r


def span(vs):
    """frozenset of codes of the F_3-span of the given vectors."""
    vs = [np.asarray(v, dtype=np.int64) % Q for v in vs]
    out = set()
    for co in itertools.product(range(Q), repeat=len(vs)):
        s = np.zeros(S, dtype=np.int64)
        for a, v in zip(co, vs):
            s = s + a * v
        out.add(code(s))
    return frozenset(out)


def inv(M):
    """inverse of a 4x4 matrix over GF(3) (None if singular)."""
    M = np.array(M, dtype=np.int64) % Q
    n = M.shape[0]
    Aug = np.concatenate([M, np.eye(n, dtype=np.int64)], axis=1)
    for c in range(n):
        piv = None
        for i in range(c, n):
            if Aug[i, c] % Q:
                piv = i
                break
        if piv is None:
            return None
        Aug[[c, piv]] = Aug[[piv, c]]
        Aug[c] = (Aug[c] * (1 if Aug[c, c] == 1 else 2)) % Q
        for i in range(n):
            if i != c and Aug[i, c]:
                Aug[i] = (Aug[i] - Aug[i, c] * Aug[c]) % Q
    return Aug[:, n:] % Q


def proj_point(v):
    """normalised representative (first nonzero coord = 1) of a nonzero vector, as a code; None for 0."""
    v = np.asarray(v, dtype=np.int64) % Q
    nz = np.nonzero(v)[0]
    if len(nz) == 0:
        return None
    a = v[nz[0]]
    return code((v * (1 if a == 1 else 2)) % Q)
