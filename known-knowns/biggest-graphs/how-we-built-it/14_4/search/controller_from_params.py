#!/usr/bin/env python3
"""controller_from_params.py -- written for this release (not part of the original search run).

Writes the 104-vertex (4,4) controller graph that is embedded in G_14_4_n8424.params.json (key
"controller_edges") as a plain edge list, so frame4.py can be run without downloading the controller.
The output is NOT byte-identical to the downloaded file (that one has comment lines and a different edge order),
but frame4.read_controller() parses both to the same graph with the same vertex labels (0..103), so frame4.py
produces the same params JSON and edge list.  The output file name defaults to the original controller's base
name, which frame4.py stores in the params JSON.

usage: python controller_from_params.py [--params ../G_14_4_n8424.params.json] [--out adjD4_104c_d4D4.txt]
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--params', default=os.path.join(HERE, '..', 'G_14_4_n8424.params.json'))
    ap.add_argument('--out', default=None, help='default: <controller_file from the params> in the current dir')
    a = ap.parse_args()
    P = json.load(open(a.params))
    out = a.out or P['controller_file']
    with open(out, 'w') as f:
        for u, w in P['controller_edges']:
            f.write('%d %d\n' % (u, w))
    print('wrote', out, 'with', len(P['controller_edges']), 'edges')


if __name__ == '__main__':
    main()
