#!/usr/bin/env python
"""
mask_from_margin.py -- not-fooled mask (True = still correctly classified, ties count as robust) from a row-margin file
(best_wrong - true logit on CPU).  Every residual stage takes --margin_in and --mask_in; in the original run the masks
were written by a checker or by `m <= 0`, and all six masks of the chain were checked to equal (margin <= 0).

  python mask_from_margin.py MARGIN.npy MASK.npy
"""
import sys

import numpy as np

m = np.load(sys.argv[1])
mask = m <= 0
np.save(sys.argv[2], mask)
print('not fooled (implied robust):', int(mask.sum()), 'of', m.size)
