#!/usr/bin/env python3
"""Decode the graph with N vertices from a SageMath script that defines graphs as Graph(r"<sparse6 or graph6>") and
write it as a plain edge list (no header), labels as in the sparse6 string.

Used for the (13,4) seed: Rishabh Rajiv's Q9(T4)++ on 6611 vertices as hosted on the Comellas table
(desc_g/adjacencies/adjD4/6611_rishabhrajiv_SageMath.txt). The same labelled edge set is in his Zenodo dataset
(graph_d13_k4_n6611.edges.xz); either file gives the same search input, because search/ddlib.load_graph sorts the
edge list.

usage: decode_sage.py SAGE_FILE N OUT.edges
"""
import re, sys, argparse
import numpy as np
import networkx as nx


def from_sage(path, N):
    s = open(path, 'rb').read().decode('latin-1')
    for m in re.finditer(r'Graph\(\s*r?["\']([^"\']+)["\']', s):
        g6 = m.group(1).strip()
        try:
            if g6.startswith(':'):
                G = nx.from_sparse6_bytes(g6.encode())
            else:
                G = nx.from_graph6_bytes(g6.encode())
        except Exception:
            continue
        if G.number_of_nodes() == N:
            G = nx.convert_node_labels_to_integers(G)
            return N, np.array(list(G.edges()), dtype=np.int64)
    return None


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('sage_file'); ap.add_argument('N', type=int); ap.add_argument('out')
    a = ap.parse_args()
    r = from_sage(a.sage_file, a.N)
    if r is None:
        sys.exit(f"no graph with {a.N} vertices found in {a.sage_file}")
    n, E = r
    with open(a.out, 'w') as f:
        for u, v in E:
            f.write(f"{int(u)} {int(v)}\n")
    print(f"wrote {a.out}: N={n} edges={len(E)}")
