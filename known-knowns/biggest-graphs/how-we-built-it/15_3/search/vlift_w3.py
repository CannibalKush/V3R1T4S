#!/usr/bin/env python3
"""
vlift_w3.py -- group multiplication tables for voltage lifts (elements 0..m-1, 0 = identity).
Groups: Zm, Dm (dihedral of order 2m), Zm:r:k (metacyclic Z_m x|_r Z_k, r^k = 1 mod m), ZmxZk.
(Only make_group is kept here; it is used by vsa5.py.  The original module also held a 4-regular voltage-lift
annealer that is not used for the (15,3) graph.)
"""
import numpy as np


def make_group(spec):
    if spec.startswith('D'):
        m = int(spec[1:])
        # elements (r^i s^e), index e*m + i ; (i1,e1)*(i2,e2) = (i1 + (-1)^e1 i2, e1+e2)
        n = 2 * m
        mul = np.zeros((n, n), dtype=np.int64)
        for e1 in range(2):
            for i1 in range(m):
                for e2 in range(2):
                    for i2 in range(m):
                        i = (i1 + (i2 if e1 == 0 else -i2)) % m
                        e = (e1 + e2) % 2
                        mul[e1 * m + i1, e2 * m + i2] = e * m + i
        return mul
    if ':' in spec:
        a, r, k = spec[1:].split(':')
        m, r, k = int(a), int(r), int(k)
        assert pow(r, k, m) == 1
        n = m * k
        # (x, y) with x in Z_m, y in Z_k ; (x1,y1)(x2,y2) = (x1 + r^y1 x2, y1+y2)
        mul = np.zeros((n, n), dtype=np.int64)
        for y1 in range(k):
            ry = pow(r, y1, m)
            for x1 in range(m):
                for y2 in range(k):
                    for x2 in range(m):
                        mul[y1 * m + x1, y2 * m + x2] = ((y1 + y2) % k) * m + (x1 + ry * x2) % m
        return mul
    if 'x' in spec:
        a, b = spec[1:].split('xZ')
        m1, m2 = int(a), int(b)
        n = m1 * m2
        mul = np.zeros((n, n), dtype=np.int64)
        for g in range(n):
            for h in range(n):
                mul[g, h] = ((g // m2 + h // m2) % m1) * m2 + (g % m2 + h % m2) % m2
        return mul
    m = int(spec[1:])
    return np.array([[(g + h) % m for h in range(m)] for g in range(m)], dtype=np.int64)
