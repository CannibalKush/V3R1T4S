import re, sys, html
src = open(sys.argv[1], encoding='utf-8', errors='replace').read()
def strip(c): return html.unescape(re.sub(r'<[^>]+>', '', c)).strip()
cells = {}
sections = []
for m in re.finditer(r'<a name="d(\d+)">|<h3>Values of A\(n,(\d+),(\d+)\)</h3>|<h3><a name="d8.8">Lower bounds for A\(n,8,8\)|<h3>Bounds on A\(n,(\d+),(\d+)\)</h3>', src):
    if m.group(1): sections.append((m.start(), 'main', int(m.group(1)), None))
    elif m.group(2): sections.append((m.start(), 'values', int(m.group(2)), int(m.group(3))))
    elif m.group(4): sections.append((m.start(), 'values', int(m.group(4)), int(m.group(5))))
    else: sections.append((m.start(), 'values', 8, 8))
def section_at(p):
    cur=None
    for s in sections:
        if s[0] <= p: cur=s
    return cur
for tm in re.finditer(r'<table border="1">(.*?)</table>', src, re.S):
    sec = section_at(tm.start())
    if sec is None: continue
    rows = [[strip(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)] for r in re.findall(r'<tr>(.*?)</tr>', tm.group(1), re.S)]
    if sec[1]=='main':
        d=sec[2]; hdr=None
        for vals in rows:
            if not vals: continue
            if vals[0].lower().startswith('n') and len(vals)>1 and all(v.isdigit() for v in vals[1:]): hdr=vals; continue
            if hdr and vals[0].isdigit():
                n=int(vals[0])
                for i,v in enumerate(vals[1:],1):
                    if i<len(hdr) and hdr[i].isdigit() and v: cells[(n,d,int(hdr[i]))]=v
    else:
        d,w=sec[2],sec[3]
        # sub-table: rows alternate n-rows (all ints) and value rows; skip separator rows
        i=0
        while i < len(rows):
            a=rows[i]
            if a and all(x.isdigit() for x in a) and i+1 < len(rows):
                b=rows[i+1]
                if len(b)==len(a) and not all(x.isdigit() and int(x)<70 for x in b):
                    for j in range(len(a)):
                        if b[j]: cells[(int(a[j]),d,w)]=b[j]
                    i+=2; continue
            i+=1
targets=[l.strip().split(',') for l in open(sys.argv[2]) if l.strip()]
print("cell\tours\tkind\tlive_cell\tlive_lb\tlive_ub\tverdict")
for t in targets:
    n,d,w,ours,kind=int(t[0]),int(t[1]),int(t[2]),int(t[3]),t[4]
    v=cells.get((n,d,w)) or cells.get((n,d,n-w))
    lb=ub=None
    if v:
        m=re.match(r'(\d+)[^\d-]*(?:-(\d+|\.\.\.))?',v)
        if m:
            lb=int(m.group(1)); ub=m.group(2)
            ub=int(ub) if ub and ub.isdigit() else None
    if kind=='lb':
        verdict = 'STRICT_BEAT' if lb is not None and ours>lb else ('TIE' if lb==ours else 'BELOW/UNKNOWN')
        if ub is not None and ours>ub: verdict+=' !!EXCEEDS_UB'
    else:
        verdict = 'STRICT_BELOW_UB' if ub is not None and ours<ub else ('TIE' if ub==ours else 'UNKNOWN')
        if lb is not None and ours<lb: verdict+=' !!BELOW_LB'
    print(f"A({n},{d},{w})\t{ours}\t{kind}\t{v}\t{lb}\t{ub}\t{verdict}")
print(f"# cells parsed: {len(cells)}", file=sys.stderr)
