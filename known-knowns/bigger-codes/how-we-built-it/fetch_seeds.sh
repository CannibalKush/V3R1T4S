#!/bin/sh
# fetch_seeds.sh [DIR] : download the 28 seed codes from A. E. Brouwer's code archive into DIR (default: seeds/)
# and compare them with the sha256 values of the copies we used (SEEDS.sha256, fetched 2026-10-06/07 and, for
# a52..a56.8.7, 2026-10-08).  One plain GET per file, 1 s apart.  The archive is live: a file whose cell has since
# been improved may have been replaced or removed, in which case its line in the check fails.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
DIR=${1:-seeds}
mkdir -p "$DIR"
cut -c67- "$HERE/SEEDS.sha256" | while read -r p; do
  mkdir -p "$DIR/$(dirname "$p")"
  if [ ! -s "$DIR/$p" ]; then
    curl -sS -f -o "$DIR/$p" "https://aeb.win.tue.nl/codes/cwc/$p" || echo "FETCH FAILED: $p"
    sleep 1
  fi
done
cd "$DIR" && shasum -a 256 -c "$HERE/SEEDS.sha256"
