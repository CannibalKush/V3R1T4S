"""gq4.py: W(q) in the GF(q^4) model with a semiregular cyclic automorphism group, for SYMMETRIC voltage search.

V = GF(q^4) as a 4-dim GF(q)-space, symplectic form B(x,y) = Tr_{q^4/q}(delta * x * y^(q^2)), where
delta + delta^(q^2) = 0 (q odd: delta = theta^((q^2+1)/2); q even: delta = 1).  B is GF(q)-bilinear, alternating,
non-degenerate.  Points = <x> = theta^k GF(q)^*  <->  k mod P, P = (q+1)(q^2+1)  (discrete log).
omega = theta^(q^2-1) has order q^2+1 and preserves B (omega^(1+q^2) = 1), so x -> omega x is an automorphism of
W(q); on point indices it is k -> k + (q^2-1) mod P.  It acts semiregularly on points, lines and flags with orbits
of size (q^2+1)/gcd(2,q-1).  The q^2+1 lines x*GF(q^2) are totally isotropic and form the regular spread.

self-test: python gq4.py 7   (uses gq.py)

build(q) -> dict(P, lines (P x (q+1) point ids), adj (2P x (q+1)), shift (int), spread (list of line ids),
                 point_orbit, line_orbit)
"""
import os
import sys
import numpy as np
import galois


def build(q):
    Q4 = q ** 4
    F = galois.GF(Q4)
    theta = F.primitive_element
    P = (q + 1) * (q * q + 1)
    order = Q4 - 1
    # discrete log table
    # powers theta^k for k = 0..order-1
    pw = np.empty(order, dtype=np.int64)
    x = F(1)
    # vectorised: compute in chunks
    ks = np.arange(order)
    pw = np.array(theta ** ks, dtype=np.int64)
    log = np.empty(Q4, dtype=np.int64)
    log[pw] = ks
    log[0] = -1
    # delta
    if q % 2 == 1:
        delta = theta ** ((q * q + 1) // 2)
    else:
        delta = F(1)
    assert delta + delta ** (q * q) == 0
    # trace to GF(q): Tr(z) = z + z^q + z^(q^2) + z^(q^3)
    def tr(z):
        return z + z ** q + z ** (q * q) + z ** (q ** 3)
    # point representatives: theta^k, k = 0..P-1
    reps = F(pw[:P])
    # B(theta^i, theta^j) = Tr(delta theta^i theta^(j q^2)); orthogonality only depends on point classes.
    # For each point i compute the set of points j with B = 0 (vectorised over j).
    repsq2 = reps ** (q * q)
    lines = {}
    pt_lines = [[] for _ in range(P)]
    GFq_elems = F(pw[np.arange(0, order, order // (q - 1))]) if q > 2 else F([1])   # GF(q)^*
    for i in range(P):
        vals = tr(delta * reps[i] * repsq2)
        perp = np.where(np.array(vals, dtype=np.int64) == 0)[0]
        for j in perp:
            if j == i:
                continue
            # points of the line <theta^i, theta^j>: theta^j and theta^i + c theta^j, c in GF(q)
            pts = {int(j) % P}
            base_i = reps[i]
            base_j = reps[j]
            for c in [F(0)] + list(GFq_elems):
                z = base_i + c * base_j
                pts.add(int(log[int(z)]) % P)
            key = tuple(sorted(pts))
            if key not in lines:
                lines[key] = len(lines)
    L = sorted(lines.keys())
    assert len(L) == P, (len(L), P)
    lines = np.array(L, dtype=np.int64)
    k = q + 1
    adj = np.zeros((2 * P, k), np.int64)
    fill = np.zeros(P, np.int64)
    for l in range(P):
        for p in lines[l]:
            adj[p, fill[p]] = P + l
            fill[p] += 1
        adj[P + l] = lines[l]
    assert (fill == k).all()
    adj.sort(axis=1)
    shift = (q * q - 1) % P
    # line action
    lidx = {tuple(r): i for i, r in enumerate(lines.tolist())}
    line_img = np.array([lidx[tuple(sorted(((lines[l] + shift) % P).tolist()))] for l in range(P)], np.int64)
    # spread: lines x GF(q^2) -> the line containing theta^0 = 1 and theta^(q^2+1) (a generator of GF(q^2)^* is
    # theta^((q^4-1)/(q^2-1)) = theta^(q^2+1)); its orbit under multiplication by theta covers the spread.
    g2 = (q * q + 1)
    spread = set()
    for kk in range(P):
        a = kk % P
        b = (kk + g2) % P
        # find line containing both a and b
        for l in np.where((lines == a).any(axis=1))[0]:
            if b in lines[l]:
                spread.add(int(l))
                break
    spread = sorted(spread)
    cov = np.zeros(P, np.int64)
    for l in spread:
        cov[lines[l]] += 1
    assert len(spread) == q * q + 1 and (cov == 1).all(), (len(spread), cov.min(), cov.max())
    return dict(q=q, P=P, lines=lines, adj=adj, shift=shift, line_img=line_img, spread=np.array(spread))


if __name__ == '__main__':
    import time
    q = int(sys.argv[1])
    t = time.time()
    g = build(q)
    print('q', q, 'P', g['P'], 'shift', g['shift'], 'spread', len(g['spread']), '%.1fs' % (time.time() - t))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import gq
    gq.selftest(dict(q=q, P=g['P'], adj=g['adj']))
    # orbit sizes
    P = g['P']
    o = 0
    seen = np.zeros(P, bool)
    sizes = []
    for i in range(P):
        if not seen[i]:
            j = i
            s = 0
            while not seen[j]:
                seen[j] = True
                j = (j + g['shift']) % P
                s += 1
            sizes.append(s)
    print('point orbit sizes', sorted(set(sizes)), 'count', len(sizes))
