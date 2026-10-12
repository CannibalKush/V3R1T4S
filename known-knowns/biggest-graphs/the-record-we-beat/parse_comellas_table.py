#!/usr/bin/env python3
"""Own parser for Comellas' table_degree_diameter.html.
Walks <TR> rows; <TH> = degree; each <TD> holds an <A href="desc_g/desc_gD.html#<deg><D>">value</A>.
Value text may contain thin spaces, '*' (Cayley), <b> (optimal). Emits JSON {"(deg,D)": {...}}.
Usage: parse_table.py <html> [json-out]
"""
import re, sys, json, html as htmlmod

src = sys.argv[1]
h = open(src, encoding="utf-8", errors="replace").read()

# isolate the main table
lo = h.lower()
ts = lo.find("<table")
te = lo.find("</table>", ts)
tbl = h[ts:te]

cells = {}
rows = re.findall(r"<tr[^>]*>(.*?)</tr>", tbl, flags=re.S | re.I)
for row in rows:
    m = re.search(r"<th[^>]*>\s*(\d+)\s*</th>", row, flags=re.I)
    if not m:
        continue
    deg = int(m.group(1))
    tds = re.findall(r"<td([^>]*)>(.*?)</td>", row, flags=re.S | re.I)
    for attrs, inner in tds:
        a = re.search(r'href="desc_g/desc_g(\d+)\.html#(\d+)"[^>]*>(.*?)</a>', inner, flags=re.S | re.I)
        if not a:
            continue
        D = int(a.group(1))
        anchor = a.group(2)
        # sanity: anchor should be f"{deg}{D}"
        if anchor != f"{deg}{D}":
            print(f"WARN anchor mismatch deg={deg} D={D} anchor={anchor}", file=sys.stderr)
        raw = a.group(3)
        bold = bool(re.search(r"<b>|<strong>", raw, flags=re.I)) or bool(re.search(r"<b>|<strong>", inner, flags=re.I))
        txt = re.sub(r"<[^>]+>", "", raw)
        txt = htmlmod.unescape(txt)
        cayley = "*" in txt
        digits = re.sub(r"[^0-9]", "", txt)
        if not digits:
            print(f"WARN no digits deg={deg} D={D} raw={raw!r}", file=sys.stderr)
            continue
        bg = re.search(r"bgcolor=\s*#?([0-9a-fA-F]{6})", attrs, flags=re.I)
        cells[f"({deg},{D})"] = {
            "deg": deg, "D": D, "N": int(digits), "raw": txt.strip(),
            "cayley": cayley, "bold": bold,
            "bg": bg.group(1).upper() if bg else None,
            "border": "border" in attrs.lower(),
        }

print(f"parsed {len(cells)} cells", file=sys.stderr)
out = json.dumps(cells, indent=1, sort_keys=True)
if len(sys.argv) > 2:
    open(sys.argv[2], "w").write(out)
else:
    print(out)
