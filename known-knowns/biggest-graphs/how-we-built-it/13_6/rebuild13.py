#!/usr/bin/env python3
"""rebuild13.py RAJIV_EDGES_XZ RAJIV_WITNESS_JSON SP_JSON SL_JSON EXTRA_EDGES_TXT OUT_EDGES

Rebuild the (13,6) graph on 535 495 vertices from Rishabh Rajiv's published H_9(T_4) compound
(Zenodo 10.5281/zenodo.23052995: graph_d13_k6_n534234.edges.xz and witnesses/cs_d13_k6_n534234.json), the two relaxed
cut sets shipped here (SP_relaxed_t4055.json, SL_relaxed_t4055.json) and the certificate file
G_13_6_n535495.extra_vs_compound.txt (every edge of our graph that is not in the bare compound: attachments of the
4 055 surgery vertices, their 5-regular graph, and the 2 643 shortcut edges).

Steps: (1) read block 0 of Rajiv's file (the H(9) incidence graph) and his witness; (2) self-test: rebuilding the
compound with HIS cut sets must reproduce his published edge set exactly; (3) rebuild the compound with OUR cut sets
(compound_edges from compound.py, which does not require Lemma 5's one-per-line hypothesis); (4) append the certificate
edges, sort, check simplicity, write OUT and print its sha256 (expected 4ed4fc62000b3cbc6c23b08d9db4af383aa28b01e69fc802b5b1bbdbab170e94).
Requires python3 with numpy and pandas; compound.py must sit next to this script.
"""
import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compound import read_all, block0, compound_edges  # noqa: E402


def main():
    if len(sys.argv) != 7:
        print(__doc__)
        sys.exit(2)
    raj, wit, spf, slf, extra, out = sys.argv[1:7]
    W = json.load(open(wit))
    q, m = W['q'], W['m']
    P = (q ** 6 - 1) // (q - 1)
    B = 2 * m * P
    print('Rajiv file sha256', hashlib.sha256(open(raj, 'rb').read()).hexdigest(), flush=True)
    n0, R = read_all(raj)
    Cr = R[(R[:, 0] < B) & (R[:, 1] < B)]
    _, pt_lines, _ = block0(Cr, P)
    SP = np.array(json.load(open(spf))['set'], np.int64)
    SL = np.array(json.load(open(slf))['set'], np.int64)
    print('our cut sets: %d points, %d lines' % (len(SP), len(SL)))
    SPr = np.array(W['deleted_points'], np.int64)
    SLr = np.array(W['deleted_lines'], np.int64)
    if SLr.max() >= P:
        SLr = SLr - P
    E0 = compound_edges(pt_lines, P, m, W['tournament'], W['H'], SPr, SLr)
    key = lambda E: np.sort(E[:, 0] * B + E[:, 1])
    assert len(E0) == len(Cr) and np.array_equal(key(E0), key(np.sort(Cr, 1))), 'self-test failed'
    print("self-test: rebuilt C' with Rajiv's cut sets == his published C'", flush=True)
    C = np.sort(compound_edges(pt_lines, P, m, W['tournament'], W['H'], SP, SL), 1)
    X = np.loadtxt(extra, dtype=np.int64, comments='#')
    E = np.concatenate([C, X], 0)
    E = np.sort(E, 1)
    E = E[np.lexsort((E[:, 1], E[:, 0]))]
    N = int(E.max()) + 1
    kk = E[:, 0] * N + E[:, 1]
    assert len(np.unique(kk)) == len(kk) and (E[:, 0] != E[:, 1]).all(), 'not simple'
    pd.DataFrame(E).to_csv(out, sep=' ', header=False, index=False)
    print('REBUILT', out, 'N', N, 'M', len(E), 'sha256', hashlib.sha256(open(out, 'rb').read()).hexdigest())


if __name__ == '__main__':
    main()
