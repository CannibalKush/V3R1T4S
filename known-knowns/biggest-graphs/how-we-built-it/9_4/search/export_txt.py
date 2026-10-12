"""export_txt.py -- written for this release (the original run did not keep the script that wrote these files).

Writes the plain-text inputs of ../rebuild_1700.py from the .npz written by symsearch.py (q = 7, n = 2):
  voltage_q7_Z2.txt  point index, line index, Z_2 voltage of every incidence (in the npz 'ends' order)
  spread_q7.txt      the 50 line indices of the regular spread
  W7_points.txt      coordinates of theta^k (k = 0..399) over GF(7) in the basis 1, t, t^2, t^3 of
                     GF(7^4) = GF(7)[t]/(irreducible polynomial of the galois package), plus the Gram matrix J of
                     B(x, y) = Tr(delta x y^(q^2)) with delta = theta^((q^2+1)/2), the form used by gq4.py
  W7_lines.txt       the 8 point indices of every line
It was checked to reproduce the four shipped files byte for byte from the published voltages
(sha256 de4b89ae...cebe1, the npz written by the seed-1 symsearch.py run).

usage: python export_txt.py sym_q7_n2_s1.npz [--outdir .]
"""
import argparse
import os

import galois
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('npz')
    ap.add_argument('--outdir', default='.')
    a = ap.parse_args()
    z = np.load(a.npz)
    q, P = int(z['q']), int(z['P'])
    assert int(z['n']) == 2 and int(z['bad']) == 0
    ends, alpha, lines, spread = z['ends'], z['alpha'], z['lines'], z['spread']
    shift = (q * q - 1) % P
    os.makedirs(a.outdir, exist_ok=True)

    def out(name):
        return open(os.path.join(a.outdir, name), 'w')

    with out('voltage_q%d_Z2.txt' % q) as f:
        f.write('# point_index line_index alpha (Z_2); invariant under k -> k+%d mod %d (omega = theta^%d)\n'
                % (shift, P, shift))
        for (p, L), v in zip(ends, alpha):
            f.write('%d %d %d\n' % (int(p), int(L) - P, int(v) % 2))

    with out('spread_q%d.txt' % q) as f:
        f.write('# %d line indices of the regular spread {x GF(%d)} of W(%d)\n' % (len(spread), q * q, q))
        f.write(' '.join(str(int(l)) for l in spread) + '\n')

    F = galois.GF(q ** 4)
    theta = F.primitive_element
    delta = theta ** ((q * q + 1) // 2)

    def tr(x):
        return x + x ** q + x ** (q * q) + x ** (q ** 3)

    basis = [theta ** i for i in range(4)]
    J = [[int(tr(delta * basis[i] * basis[j] ** (q * q))) for j in range(4)] for i in range(4)]
    with out('W%d_points.txt' % q) as f:
        f.write('# point index k (= discrete log of theta^k mod P=%d in GF(%d^4) = GF(%d)[t]/(%s)), coordinates of '
                'theta^k in basis 1,t,t^2,t^3 over GF(%d)\n' % (P, q, q, F.irreducible_poly, q))
        f.write('# symplectic form B(x,y) = x^T J y with J = %s (mod %d)\n' % (J, q))
        for k in range(P):
            c = [int(x) for x in (theta ** k).vector()][::-1]
            f.write('%d %s\n' % (k, ' '.join(str(x) for x in c)))

    with out('W%d_lines.txt' % q) as f:
        f.write('# line index l (graph vertex P+l = %d+l), followed by its %d point indices\n' % (P, q + 1))
        for l in range(P):
            f.write('%d %s\n' % (l, ' '.join(str(int(p)) for p in lines[l])))
    print('wrote voltage/spread/points/lines files to', a.outdir)


if __name__ == '__main__':
    main()
