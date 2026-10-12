#!/usr/bin/env python3
"""
make_params.py -- convert the outputs of vsa5.py (controller) and k5sat.py (chart) into the two published files
controller_own_k5_n60.adj and G_15_3_n1620.params.json.

This conversion was done by hand (not by a saved script) when the graph was found; this script was written
afterwards for the release and reproduces both published files byte for byte from the original search outputs.
  .adj          one line per controller vertex: its neighbours in increasing order, separated by spaces
  .params.json  E, M, d, T copied from the k5sat output; w[a,b] = T[a,b] d[a,b] (mod q) for every controller edge;
                the controller's voltage data copied from the vsa5 output; json.dumps(indent=0), no trailing newline.
Usage: make_params.py vsa5_out.json k5sat_out.k5sat.json [--adj controller_own_k5_n60.adj]
                      [--params G_15_3_n1620.params.json]
"""
import argparse, json, os

DESCRIPTION = (
    "Route-chart lift over F_3^3 of an OWN 60-vertex 5-regular W3 controller (Z15-voltage lift of a 4-vertex base "
    "multigraph, found by code/vsa5.py; every non-adjacent ordered pair incl. u=u joined by a walk of length exactly 3). "
    "Ports: at every vertex the 4 H-neighbours get the 4 lines of the plane z=0, the matching neighbour (perfect "
    "matching M, chosen by SAT) gets (0,0,1). Lift vertex (u,x) has index u*27 + 9*x0 + 3*x1 + x2. For every "
    "controller edge [a,b] (a<b), every x in F_3^3 and lam in F_3: (a,x) ~ (b, T[a,b] x + lam*w[a,b]) with "
    "w[a,b] = T[a,b] d[a,b] (mod 3). 15-regular, 1620 vertices, diameter 3."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('controller', help='vsa5.py output (prefix.json)')
    ap.add_argument('chart', help='k5sat.py output (prefix.k5sat.json)')
    ap.add_argument('--adj', default='controller_own_k5_n60.adj')
    ap.add_argument('--params', default='G_15_3_n1620.params.json')
    a = ap.parse_args()
    C = json.load(open(a.controller))
    K = json.load(open(a.chart))
    assert C['w3_deficit'] == 0 and K['sat'] and K['lift_bad_pairs'] == 0
    n, q = K['n'], K['q']
    E = [tuple(e) for e in K['E']]
    assert sorted(E) == sorted(set((min(x, y), max(x, y)) for x, y in C['edges'])), 'chart is not for this controller'
    nbrs = [[] for _ in range(n)]
    for x, y in E:
        nbrs[x].append(y); nbrs[y].append(x)
    deg = {len(r) for r in nbrs}
    assert len(deg) == 1
    with open(a.adj, 'w') as f:
        for r in nbrs:
            f.write(' '.join(map(str, sorted(r))) + '\n')
    w = {}
    for x, y in E:
        key = f'{x},{y}'
        T, d = K['T'][key], K['d'][key]
        w[key] = [sum(T[i][j] * d[j] for j in range(3)) % q for i in range(3)]
    P = {'description': DESCRIPTION, 'q': q, 'n': n, 'E': K['E'], 'M': K['M'], 'd': K['d'], 'T': K['T'], 'w': w,
         'controller_file': os.path.basename(a.adj),
         'controller_voltage_data': {'group': C['group'], 'b': C['b'], 'bi': C['bi'], 'bj': C['bj'],
                                     'volt': C['volt'], 'k': deg.pop()}}
    with open(a.params, 'w') as f:
        f.write(json.dumps(P, indent=0))
    print(f'wrote {a.adj} and {a.params}')


if __name__ == '__main__':
    main()
