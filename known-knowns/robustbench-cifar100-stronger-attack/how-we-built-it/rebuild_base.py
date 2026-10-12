#!/usr/bin/env python
"""
rebuild_base.py -- reconstructs the stage-5 tensor (output of assemble_final.py, implied count 2758; sha256
193c035e...7d8d) from the published tensor: the two differ only in the 5 rows that stage 6 replaced (557, 2137, 5091,
8141, 9693), whose stage-5 values are stored in stage6-inputs/base_rows.npy.  Together with the three multi-start result
dirs in stage6-inputs/ this lets anyone re-run the last step (assemble.py) and get the published tensor bit for bit.

  python rebuild_base.py --out BASE.npy
"""
import argparse, hashlib, os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FAMILY = os.path.dirname(HERE)
BASE_SHA256 = '193c035e004b4932e9e4aa6127877883bd2dbc1580b00333b03f92f3523a7d8d'

ap = argparse.ArgumentParser()
ap.add_argument('--published', default=os.path.join(FAMILY, 'adversarial-examples', 'x_adv_Addepalli2022Efficient_RN18.npz'))
ap.add_argument('--inputs', default=os.path.join(HERE, 'stage6-inputs'))
ap.add_argument('--out', required=True)
a = ap.parse_args()
x = np.array(np.load(a.published)['x_adv'])
idx = np.load(os.path.join(a.inputs, 'base_rows_idx.npy'))
x[idx] = np.load(os.path.join(a.inputs, 'base_rows.npy'))
np.save(a.out, x)
h = hashlib.sha256(open(a.out, 'rb').read()).hexdigest()
print(f'wrote {a.out} sha256 {h} ({"== stage-5 tensor" if h == BASE_SHA256 else "MISMATCH, expected " + BASE_SHA256})')
raise SystemExit(0 if h == BASE_SHA256 else 1)
