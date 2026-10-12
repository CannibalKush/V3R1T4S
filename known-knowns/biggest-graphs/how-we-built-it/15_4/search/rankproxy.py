"""Fast chart scoring for Cayley-controller route-chart lifts: for every reduced word w of length L over the alphabet
{a,a^-1,b,b^-1,c}, compute the controllability matrix M_w (s x L over F_q, q prime) and its rank; an element h
(endpoint of w) is 'covered' if some word ending at h has rank s (then every fibre target is reached in exactly L
steps from every start).  Score = #non-identity elements with words but none of full rank (+ big penalty for
elements with no length-L word, which need pencils / BFS).
Used as a cheap proxy in chart SA; the final answer always comes from exact BFS.
"""
import numpy as np
import numba as nb
import itertools


def reduced_words(L, linv):
    words = [[t] for t in range(5)]
    for _ in range(L - 1):
        words = [w + [t] for w in words for t in range(5) if t != linv[w[-1]]]
    return np.array(words, dtype=np.int64)


def endpoints(words, letters, mul):
    h = np.zeros(len(words), dtype=np.int64)
    for i in range(words.shape[1]):
        h = mul[h, letters[words[:, i]]]
    return h


@nb.njit(cache=True)
def rank_mod(M, q):
    M = M.copy() % q
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        piv = -1
        for i in range(r, rows):
            if M[i, c] % q != 0:
                piv = i; break
        if piv < 0:
            continue
        for j in range(cols):
            tmp = M[r, j]; M[r, j] = M[piv, j]; M[piv, j] = tmp
        inv = 1
        for e in range(1, q):
            if (M[r, c] * e) % q == 1:
                inv = e; break
        for j in range(cols):
            M[r, j] = (M[r, j] * inv) % q
        for i in range(rows):
            if i != r and M[i, c] % q != 0:
                f = M[i, c]
                for j in range(cols):
                    M[i, j] = (M[i, j] - f * M[r, j]) % q
        r += 1
        if r == rows:
            break
    return r


@nb.njit(cache=True)
def word_ranks(words, As, bs, q):
    """As: (5, s, s), bs: (5, s). Returns rank of M_w for each word."""
    nw, L = words.shape
    s = As.shape[1]
    out = np.zeros(nw, dtype=np.int64)
    M = np.zeros((s, L), dtype=np.int64)
    for w in range(nw):
        for i in range(s):
            for j in range(L):
                M[i, j] = 0
        for step in range(L):
            t = words[w, step]
            # apply A_t to existing columns 0..step-1
            for j in range(step):
                col = np.zeros(s, dtype=np.int64)
                for i in range(s):
                    acc = 0
                    for kk in range(s):
                        acc += As[t, i, kk] * M[kk, j]
                    col[i] = acc % q
                for i in range(s):
                    M[i, j] = col[i]
            for i in range(s):
                M[i, step] = bs[t, i] % q
        out[w] = rank_mod(M, q)
    return out


def expand_chart(chart, spec, q):
    """chart: list of (A,b) for [pair1, pair2, inv]; returns As (5,s,s), bs (5,s) in letter order a,a^-1,b,b^-1,c."""
    import rcl
    (A1, b1), (A2, b2), (A3, b3) = chart
    A1i = rcl.mat_inv_mod(A1, q); A2i = rcl.mat_inv_mod(A2, q)
    As = np.stack([A1, A1i, A2, A2i, A3]).astype(np.int64)
    bs = np.stack([b1, (A1i @ b1) % q, b2, (A2i @ b2) % q, b3]).astype(np.int64)
    return As, bs


def proxy_score(ranks, ends, n, s, nowords_mask):
    full = ranks == s
    covered = np.zeros(n, dtype=bool)
    covered[ends[full]] = True
    bad = (~covered) & (~nowords_mask)
    bad[0] = False
    return int(bad.sum()), int(full.sum())
