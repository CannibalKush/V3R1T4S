#!/bin/sh
# Download LITA's square schemes used as inputs (github.com/khoruzhii/lita, pinned commit) and check their sha256.
# LITA's repository states no license, so these files are not redistributed here.  One GET per file, no retries.
# Usage: sh fetch_lita.sh [OUTDIR]   (default OUTDIR: ./lita)
set -eu
OUT=${1:-lita}
COMMIT=472a79fbc8248423a97bebb3aacbc89e769b9b3e   # 2026-10-07T19:22:13Z, "Merge pull request #1 ... improve-even-lita"
BASE=https://raw.githubusercontent.com/khoruzhii/lita/$COMMIT/schemes
UA=${UA:-"fmm-peel-reproduction (single GET per file)"}
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
mkdir -p "$OUT"
fail=0
while read -r name sum; do
  [ -n "$name" ] || continue
  if [ ! -f "$OUT/$name" ]; then curl -sSf -A "$UA" -o "$OUT/$name" "$BASE/$name"; fi
  got=$($SHA "$OUT/$name" | cut -d' ' -f1)
  if [ "$got" = "$sum" ]; then echo "OK   $name"; else echo "BAD  $name (sha256 $got, expected $sum)"; fail=1; fi
done <<LIST
15x15x15_r1977.npz 94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33
14x14x14_r1593.npz e80390259e0b7f58192f6167595e3da9b57142402665de44e489338a26941110
16x16x16_r2236.npz af5fd100931c22721b7f60277325a430d92b63e60e59a95dc2dd132a7b8767da
13x13x13_r1379.npz 9df0b464793e3c9584c9e95e48dc748a4774afa07bd1b7aa7e6d4421570b40eb
LIST
exit $fail
