#!/usr/bin/env python3
"""pairtools.py -- randomized pairing-rank tools mod p (library for absorb_exact.py and maxkill.py).

Pairing matrices of a scheme {(u_k, v_k, w_k)}: P_uv = rows u_k (x) v_k, P_uw = rows u_k (x) w_k, P_vw = rows v_k (x) w_k.
A linear dependency sum_k c_k v_k (x) w_k = 0 lets one term be absorbed into the u-factors of the others (rank - 1).

Khatri-Rao random projection: for random alpha (dim X x K), beta (dim Y x K) over GF(p),
    (x (x) y) R = (x alpha) * (y beta)    (elementwise),   R = alpha (.) beta  (column-wise Khatri-Rao).
rank_p(P R) <= rank_p(P) <= rank_Q(P) always; equality rank_p(PR) = rank_Q(P) holds with probability >= 1 - 2K/p
(Schwartz-Zippel: the K x K minors are polynomials of degree 2K in alpha, beta that do not vanish identically,
because rank-one vectors span X (x) Y). So "full rank of P R mod p" PROVES full rank over Q; a deficit is only a
FLAG and must be confirmed exactly (absorb_exact.py checks every null vector over Q).
Seeds are fixed, so runs are deterministic.  Needs numpy and numba.
"""
import numpy as np
import numba as nb

P_DEFAULT = 2147483629  # prime < 2^31


def frac_mod(x, p):
    return (x.numerator % p) * pow(x.denominator % p, p - 2, p) % p


@nb.njit(cache=True)
def matmul_mod(A, B, p):
    n, m = A.shape
    m2, k = B.shape
    C = np.zeros((n, k), dtype=np.int64)
    for i in range(n):
        for t in range(m):
            a = A[i, t]
            if a != 0:
                for j in range(k):
                    C[i, j] = (C[i, j] + a * B[t, j]) % p
    return C


@nb.njit(cache=True)
def rref_mod(M, p):
    """Row-reduce a copy of M (r x K) mod p. Returns (rank, pivot columns array, row permutation-free echelon)."""
    A = M.copy()
    r, K = A.shape
    piv = np.full(r, -1, dtype=np.int64)
    row = 0
    for c in range(K):
        if row >= r:
            break
        pr = -1
        for i in range(row, r):
            if A[i, c] != 0:
                pr = i
                break
        if pr < 0:
            continue
        if pr != row:
            for j in range(K):
                tmp = A[row, j]
                A[row, j] = A[pr, j]
                A[pr, j] = tmp
        inv = 1
        b = A[row, c] % p
        e = p - 2
        while e > 0:
            if e & 1:
                inv = (inv * b) % p
            b = (b * b) % p
            e >>= 1
        for j in range(K):
            A[row, j] = (A[row, j] * inv) % p
        for i in range(r):
            if i != row and A[i, c] != 0:
                f = A[i, c]
                for j in range(c, K):
                    A[i, j] = (A[i, j] - f * A[row, j]) % p
        piv[row] = c
        row += 1
    return row, piv, A


class Pairing:
    """Projected pairing matrix PR = (X alpha) * (Y beta) mod p and its rank."""

    def __init__(self, X, Y, p=P_DEFAULT, extra=40, seed=1):
        self.p = p
        r = X.shape[0]
        self.r = r
        K = r + extra
        rng = np.random.default_rng(seed)
        self.alpha = rng.integers(0, p, size=(X.shape[1], K), dtype=np.int64)
        self.beta = rng.integers(0, p, size=(Y.shape[1], K), dtype=np.int64)
        XA = matmul_mod(X, self.alpha, p)
        YB = matmul_mod(Y, self.beta, p)
        self.PR = (XA * YB) % p
        self.rank, piv, _ = rref_mod(self.PR, p)
        self.piv = piv[:self.rank]
