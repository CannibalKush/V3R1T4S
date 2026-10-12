#!/bin/sh
# run_lcrt5_job.sh -- the driver of the author engine's LCRT-4 run at X = 10^50 (certificates/lcrt5_1e50.*), cleaned:
# run lcrt5 for each exponent E, then merge_lcrt.py -> summary_1eE.json, certify.py -> certificate_1eE.json.
# Resumable: rerun the script; finished tasks (complete JSON lines in out_1eE/tasks_w*.jsonl) are skipped.
#
# usage: run_lcrt5_job.sh LCRT5_BIN ENGINES_DIR [E ...]        (default E list: 50; the original job had 50 52 54 and was
#        stopped after 50).  Environment: PY (python with sympy, default python3), SIEVE (default 1000000000),
#        WORKERS (default 8), D0 (default 11), MODE_ARGS (extra lcrt5 args after EULER, default empty = LCRT-4).
# The certified LCRT-4 run used the engine of lcrt5_v1_LCRT4.patch and the merge of merge_lcrt_v1.patch (README.md);
# the original job ran under `nice -n 10` with a 6 h alarm, and lcrt5 was built with -DORPHAN_EXIT=1 so that workers
# exit if the master is killed.
# (no set -e: like the original, a failing certify.py is reported by its exit code)
BIN=${1:?usage: run_lcrt5_job.sh LCRT5_BIN ENGINES_DIR [E ...]}
ENG=${2:?usage: run_lcrt5_job.sh LCRT5_BIN ENGINES_DIR [E ...]}
shift 2
[ $# -gt 0 ] || set -- 50
PY=${PY:-python3}
SIEVE=${SIEVE:-1000000000}
WORKERS=${WORKERS:-8}
D0=${D0:-11}
for E in "$@"; do
  if [ ! -f out_1e$E/DONE ]; then
    echo "start 1e$E $(date)"
    # shellcheck disable=SC2086
    "$BIN" "$($PY -c "print(10**$E)")" "$SIEVE" "$D0" "$WORKERS" out_1e$E 1 5 1 32 1 0 1 $MODE_ARGS 2>> run_1e$E.err
  fi
  if [ -f out_1e$E/DONE ]; then
    $PY "$ENG/merge_lcrt.py" out_1e$E > summary_1e$E.json
    $PY "$ENG/certify.py" summary_1e$E.json "$E" > certificate_1e$E.json; echo "1e$E certify exit $?"
    echo "1e$E done $(date)"
  else
    echo "1e$E NOT finished (time cap or error) $(date)"; exit 1
  fi
done
