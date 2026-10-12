#!/bin/sh
# Check the adversarial CIFAR-100 tensor: sha256 against INDEX.csv, lossless restore (unpack.py), and the model check
# (rbcheck.py: threat model on all 10,000 images, clean and robust counts with the unmodified RobustBench model).
# python3 with numpy, torch, torchvision, robustbench.  The CIFAR-100 test set (~160 MB) and the model weights (~45 MB)
# are downloaded on first use into DATA_DIR / MODEL_DIR (default: ./data, ./models in the current directory).
# N=500 sh run_checks.sh evaluates the model on the first 500 images only (quick); the default is all 10,000.
# Exit 0 iff everything passes.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
SECTION=known-knowns/robustbench-cifar100-stronger-attack
PY=${PYTHON:-python3}
for o in adversarial-examples/x_adv_Addepalli2022Efficient_RN18.npz adversarial-examples/robust_indices.txt; do
  [ -f "$HERE/$o" ] || { echo "missing $SECTION/$o"; exit 2; }
done
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
fail=0
echo "== sha256 against INDEX.csv"
for f in adversarial-examples/x_adv_Addepalli2022Efficient_RN18.npz adversarial-examples/robust_indices.txt; do
  got=$($SHA "$HERE/$f" | cut -d' ' -f1)
  grep -q "$got" "$HERE/INDEX.csv" && echo "$f: matches INDEX.csv" || { echo "$f: sha256 NOT in INDEX.csv ($got)"; fail=1; }
done
echo "== lossless restore"
$PY "$HERE/verify-it-yourself/unpack.py" || fail=1
echo "== model check"
$PY "$HERE/verify-it-yourself/rbcheck.py" --data_dir "${DATA_DIR:-./data}" --model_dir "${MODEL_DIR:-./models}" --n "${N:-10000}" || fail=1
[ $fail = 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECK FAILED"
exit $fail
