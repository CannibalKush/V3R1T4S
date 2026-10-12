#!/usr/bin/env python3
"""
parse_results.py -- read VNN-COMP 2026 SCORING/results.txt and report the rows of our two instances.

  python3 parse_results.py results.txt
A row is "all-tool-unsolved" when no cell carries '(h)' (holds) or '(v)' (violated), i.e. no participating tool
proved or refuted the instance. Prints the number of such rows, the category header (participating tools) and our
two rows, and whether each is still all-tool-unsolved.
"""
import ast, hashlib, sys

path = sys.argv[1]
raw = open(path, 'rb').read()
print('sha256', hashlib.sha256(raw).hexdigest(), 'bytes', len(raw))
lines = raw.decode().splitlines()
OURS = ['3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30-model_30_idx_1703_eps_1.00000',
        '3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30-model_30_idx_178_eps_1.00000']
rows, unsolved, tools = 0, 0, None
found = {}
for n, l in enumerate(lines):
    if l.startswith('Row: '):
        rows += 1
        r = ast.literal_eval(l[5:].strip())
        u = not any(('(h)' in c or '(v)' in c) for c in r[1:])
        unsolved += u
        if r[0] in OURS:
            found.setdefault(r[0], []).append((r, u))
            if tools is None:
                for k in range(n, max(n - 5, 0), -1):
                    if 'participating tools' in lines[k]:
                        tools = lines[k].strip()
print('Row lines', rows, '; all-tool-unsolved rows', unsolved)
print('category header:', tools)
for name in OURS:
    for r, u in found.get(name, []):
        print(r, '-> all-tool-unsolved' if u else '-> SOLVED by some tool')
    if name not in found:
        print(name, 'NOT FOUND')
