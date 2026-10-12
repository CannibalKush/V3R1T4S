#!/usr/bin/env python3
"""write_code.py OUT N npy [npy ...]: union of int64 word arrays -> one 0/1 string per line (format(x,'0Nb'))."""
import sys
import numpy as np
out, n = sys.argv[1], int(sys.argv[2])
ws = np.unique(np.concatenate([np.load(p).astype(np.int64) for p in sys.argv[3:]]))
with open(out, "w") as f:
    for x in ws:
        f.write(format(int(x), f"0{n}b") + "\n")
print(out, len(ws))
