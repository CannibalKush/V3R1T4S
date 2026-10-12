#!/bin/sh
# Regenerate the five published schemes from LITA's square schemes and compare sha256 with ../INDEX.csv.
# Usage: sh regenerate_all.sh [LITA_DIR] [OUT_DIR]   (defaults: ./lita, ./regen)
# Run fetch_lita.sh first.  Needs python3 + numpy.  Takes about 3 minutes on one core.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
LITA=${1:-lita}
OUT=${2:-regen}
PY=${PYTHON:-python3}
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
mkdir -p "$OUT"
# <14,15,15>:1843 from LITA <15,15,15>:1977, axis n, e = (1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1), f = e_0
$PY "$HERE/make_scheme.py" "$LITA/15x15x15_r1977.npz" n \
  "1 1 1 1 1 1 1 -5 1 1 1 1 1 1 1" "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0" "$OUT/14x15x15_r1843_Q.json"
# <13,14,14>:1558 from LITA <14,14,14>:1593, axis n, e = e_1 + e_8, f = e_0 - e_1
$PY "$HERE/make_scheme.py" "$LITA/14x14x14_r1593.npz" n \
  "0 1 0 0 0 0 0 0 1 0 0 0 0 0" "1 -1 0 0 0 0 0 0 0 0 0 0 0 0" "$OUT/13x14x14_r1558_Q.json"
# <15,16,16>:2196 from LITA <16,16,16>:2236, axis n, e = e_1 + e_9, f = e_0 - e_1
$PY "$HERE/make_scheme.py" "$LITA/16x16x16_r2236.npz" n \
  "0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0" "1 -1 0 0 0 0 0 0 0 0 0 0 0 0 0 0" "$OUT/15x16x16_r2196_Q.json"
# <14,14,15>:1716 from <14,15,15>:1843 above, axis m, e = e_0, f = (1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1)
$PY "$HERE/make_scheme.py" "$OUT/14x15x15_r1843_Q.json" m \
  "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0" "1 1 1 1 1 1 1 -5 1 1 1 1 1 1 1" "$OUT/14x14x15_r1716_Q.json"
# <13,14,15>:1677 from <14,14,15>:1716 above, axis n, e = e_1 + e_9, f = e_1
$PY "$HERE/make_scheme.py" "$OUT/14x14x15_r1716_Q.json" n \
  "0 1 0 0 0 0 0 0 0 1 0 0 0 0" "0 1 0 0 0 0 0 0 0 0 0 0 0 0" "$OUT/13x14x15_r1677_Q.json"
fail=0
for f in 14x15x15_r1843_Q 13x14x14_r1558_Q 15x16x16_r2196_Q 14x14x15_r1716_Q 13x14x15_r1677_Q; do
  exp=$(grep ",schemes/$f.json," "$HERE/../INDEX.csv" | sed 's/.*,//')
  got=$($SHA "$OUT/$f.json" | cut -d' ' -f1)
  if [ "$got" = "$exp" ]; then echo "IDENTICAL $f.json"; else echo "DIFFERENT $f.json ($got)"; fail=1; fi
done
exit $fail
