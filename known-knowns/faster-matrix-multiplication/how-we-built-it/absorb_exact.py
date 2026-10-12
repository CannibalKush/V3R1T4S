#!/usr/bin/env python3
"""absorb_exact.py -- iterated EXACT simultaneous absorption of pairing dependencies.

For a pairing (Y,Z) in {(v,w), (u,w), (u,v)} with free factor X (u, v, w respectively): the left nullspace of the
pairing matrix {y_k (x) z_k} is computed mod 3 primes (Khatri-Rao projection, pairtools.py), put in canonical RREF
(pivot terms j_s, c^(s)_{j_t} = delta_st), CRT-combined and rationally reconstructed, then EVERY basis vector is checked
exactly over Q (sum_k c_k y_k (x) z_k == 0 with Fractions).  Simultaneous absorption: drop the pivot terms and set
x_k <- x_k - sum_s c^(s)_k x_{j_s} for the others (valid because y_{j_s} (x) z_{j_s} = -sum_{k not pivot} c^(s)_k y_k (x) z_k).
Terms whose new x_k vanishes are dropped too.  Repeat over all three pairings until every pairing has full rank.
The output must still be verified with ../verify-it-yourself/fmmcheck.py.  Deterministic (fixed seeds).
Usage: python3 absorb_exact.py IN.json OUT.json [--max-rounds 10]     (needs numpy and numba)"""
import sys, os, json, time, math
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from pairtools import Pairing, rref_mod, frac_mod

PRIMES = [2147483629, 2147483587, 2147483579]


def modp(rows, p):
    return np.array([[frac_mod(x, p) for x in row] for row in rows], dtype=np.int64)


def left_null_canonical(Y, Z, p, seed):
    r = len(Y)
    P = Pairing(modp(Y, p), modp(Z, p), p=p, extra=20, seed=seed)
    if P.rank == r:
        return P.rank, None, None
    K = P.PR.shape[1]
    aug = np.concatenate([P.PR, np.eye(r, dtype=np.int64)], axis=1)
    rk, piv, A = rref_mod(aug, p)
    rows = [i for i in range(rk) if piv[i] >= K]
    N = A[rows, K:].copy()
    d, piv2, R = rref_mod(N, p)
    return P.rank, R[:d].copy(), [int(x) for x in piv2[:d]]


def ratrec(a, M):
    # rational reconstruction of a mod M with |num|, den <= sqrt(M/2)
    B = math.isqrt(M // 2)
    r0, r1, s0, s1 = M, a % M, 0, 1
    while r1 > B:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > B:
        return None
    x = Fraction(r1, s1)
    return x


def crt_ratrec(mats, primes):
    M = 1
    for p in primes:
        M *= p
    d, r = mats[0].shape
    out = []
    for i in range(d):
        row = []
        for j in range(r):
            x, mod = 0, 1
            for A, p in zip(mats, primes):
                a = int(A[i, j])
                # x = x mod mod, combine with a mod p
                t = ((a - x) * pow(mod, -1, p)) % p
                x = x + mod * t
                mod *= p
            q = ratrec(x, M)
            if q is None:
                return None
            row.append(q)
        out.append(row)
    return out


def exact_zero(c, Y, Z):
    acc = {}
    for k, ck in enumerate(c):
        if ck == 0:
            continue
        ys = [(i, x) for i, x in enumerate(Y[k]) if x]
        zs = [(j, x) for j, x in enumerate(Z[k]) if x]
        for i, x in ys:
            for j, y in zs:
                acc[(i, j)] = acc.get((i, j), 0) + ck * x * y
    return all(v == 0 for v in acc.values())


def load(path):
    d = json.load(open(path))
    T = [[[Fraction(x) for x in d[key][k]] for key in 'uvw'] for k in range(len(d['u']))]
    return d['n'], T


def save(path, n, T, note):
    s = lambda x: int(x) if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)
    js = {'n': n, 'm': len(T), 'ring': 'Q', 'note': note,
          'u': [[s(x) for x in t[0]] for t in T], 'v': [[s(x) for x in t[1]] for t in T],
          'w': [[s(x) for x in t[2]] for t in T]}
    json.dump(js, open(path, 'w'))


def main():
    inp, outp = sys.argv[1], sys.argv[2]
    max_rounds = int(sys.argv[sys.argv.index('--max-rounds') + 1]) if '--max-rounds' in sys.argv else 10
    n, T = load(inp)
    log = []
    PAIRS = {'vw': (1, 2, 0), 'uw': (0, 2, 1), 'uv': (0, 1, 2)}
    for rnd in range(max_rounds):
        changed = False
        for name, (iy, iz, ix) in PAIRS.items():
            t0 = time.time()
            Y = [t[iy] for t in T]
            Z = [t[iz] for t in T]
            res = [left_null_canonical(Y, Z, p, seed=17 + rnd) for p in PRIMES]
            ranks = [x[0] for x in res]
            if all(x[1] is None for x in res):
                print(json.dumps({'round': rnd, 'pairing': name, 'r': len(T), 'rank_modp': ranks, 'nullity': 0,
                                  'sec': round(time.time() - t0, 1)}), flush=True)
                continue
            pivs = [x[2] for x in res]
            if any(pv != pivs[0] for pv in pivs) or any(x[1] is None for x in res):
                print(json.dumps({'round': rnd, 'pairing': name, 'warn': 'pivot mismatch across primes', 'ranks': ranks}))
                continue
            C = crt_ratrec([x[1] for x in res], PRIMES)
            if C is None:
                print(json.dumps({'round': rnd, 'pairing': name, 'warn': 'rational reconstruction failed'}))
                continue
            ok = [exact_zero(c, Y, Z) for c in C]
            piv = pivs[0]
            info = {'round': rnd, 'pairing': name, 'r': len(T), 'nullity': len(C), 'pivot_terms': piv,
                    'exact_ok': all(ok), 'max_den': max(x.denominator for c in C for x in c),
                    'max_num': max(abs(x.numerator) for c in C for x in c)}
            if not all(ok):
                info['warn'] = 'some null vectors failed the exact check; skipping'
                print(json.dumps(info), flush=True)
                continue
            pivset = set(piv)
            newT = []
            for k, t in enumerate(T):
                if k in pivset:
                    continue
                x = list(t[ix])
                for s, j in enumerate(piv):
                    cs = C[s][k]
                    if cs != 0:
                        xj = T[j][ix]
                        x = [a - cs * b for a, b in zip(x, xj)]
                nt = list(t)
                nt[ix] = x
                if any(v != 0 for v in x):
                    newT.append(nt)
            info['r_new'] = len(newT)
            info['sec'] = round(time.time() - t0, 1)
            print(json.dumps(info), flush=True)
            log.append(info)
            T = newT
            changed = True
        if not changed:
            break
    save(outp, n, T, 'iterated exact absorption of %s; log=%s' % (inp.split('/')[-1], json.dumps(log)))
    print(json.dumps({'final_r': len(T), 'out': outp}))


if __name__ == '__main__':
    main()
