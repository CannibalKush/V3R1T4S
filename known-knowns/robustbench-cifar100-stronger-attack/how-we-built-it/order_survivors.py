#!/usr/bin/env python
"""
order_survivors.py -- the image order for stage 2: the stage-1 survivors that are still robust on CPU (margin <= 0),
closest to the decision boundary first (margin = best_wrong - true <= 0, so DESCENDING margin; stable sort).

  python order_survivors.py --stage1 S1/out --out S1/full_order_idx.npy
(In the original run this was an inline snippet of the job script; its output, full_order_idx_fixed.npy, was checked to
equal this computation on the original stage-1 files.)
"""
import argparse, os

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('--stage1', required=True, help='dir with stage1_cpu_margin.npy and stage1_survivors.npy')
ap.add_argument('--out', required=True)
a = ap.parse_args()
m = np.load(os.path.join(a.stage1, 'stage1_cpu_margin.npy'))
surv = np.load(os.path.join(a.stage1, 'stage1_survivors.npy'))
strict = surv[m[surv] <= 0]
order = strict[np.argsort(-m[strict], kind='stable')]
np.save(a.out, order)
print('survivors', surv.size, 'strict (margin <= 0)', strict.size, 'first', order[:5].tolist())
