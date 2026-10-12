#!/bin/bash
# run_lbb2_parallel.sh -- parallel run of the independent engine lbb2 (as for branch_logs/lbb2_e50_S1000000000_tasks.tar.gz):
# one generator process writes the depth-D0 task list (TASK lines + TOTAL for the top tree) to gen.out, then W worker
# processes each take every W-th task.  Output directory: OUTROOT/e${E}_S${S} with gen.out, w0.out .. w{W-1}.out, run.info.
#
# usage: run_lbb2_parallel.sh LBB2_BIN OUTROOT E W D0 SMAX [extra lbb2 args]
#   the 10^50 run:  run_lbb2_parallel.sh ./lbb2 runs 50 10 11 1000000000      (24 min wall on 10 workers)
# then:            python3 ../verify-it-yourself/lbb2_aggregate.py runs/e50_S1000000000 > lbb2_agg_e50.json
set -e
BIN=$(cd "$(dirname "$1")" && pwd)/$(basename "$1"); OUTROOT=$2; E=$3; W=$4; D0=$5; S=$6; shift 6
OUTD=$OUTROOT/e${E}_S${S}
mkdir -p "$OUTD"
cd "$OUTD"
"$BIN" -X 1e$E -S $S -D $D0 -gen "$@" > gen.out 2>&1
NT=$(grep -c '^TASK' gen.out)
echo "E=$E tasks=$NT D0=$D0 W=$W S=$S $(date)" > run.info
for ((w=0; w<W; w++)); do
  "$BIN" -X 1e$E -S $S -tasks gen.out -w $w $W "$@" > w$w.out 2>&1 &
done
wait
echo "finished $(date)" >> run.info
